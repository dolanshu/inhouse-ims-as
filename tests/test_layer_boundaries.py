"""Guard: the horizontal layering boundaries between workspace members.

AGENT.md §4 (Layering) defines three horizontal boundaries that the repository
layout alone cannot enforce, because inside a uv workspace every import
resolves:

1. **Apps are mutually exclusive.** One app must never import another app;
   each use case is one process, one failure domain and one canary unit.
2. **Product packages never depend on the testbed.** ``apps/`` and
   ``services/`` must not import any ``testbed/`` member at runtime. The
   kernel-facing half of this rule (``platform/`` must not import consumers)
   is guarded by ``platform/tests/test_library_independence.py``; this module
   guards the product-facing half.
3. **Every internal import is a declared dependency.** An ``as_*`` package
   imported from a member's ``src/`` must either be that member's own package
   or map to an ``as-*`` entry in that member's ``pyproject.toml``
   dependencies. Only "imported but undeclared" is checked; a declared but
   unused dependency is not a layering violation.
4. **Declared internal dependencies stay acyclic.** Services may depend on
   each other along the internal-API direction (see AGENT.md §4), but a cycle
   between members is a layering violation.

A last, structural test classifies every workspace member into exactly one
of the four layers (kernel / apps / services / testbed) by its path prefix,
so that a newly added member can never silently escape the boundary guards
above.

Everything is derived from repository files (the root workspace manifest and
each member's hatch package/dependency declarations); no member or import
root list is hard-coded here. Only ``<member>/src/`` is scanned, never test
directories, and no product package is imported.

Fixing a failure:
* cross-app import: delete the import; shared logic belongs in ``platform/``;
* product-to-testbed import: delete the import, the testbed is a dev asset;
* undeclared internal dependency: either add the distribution name (hyphens,
  e.g. ``as-platform``) to the member's ``[project].dependencies`` (plus the
  ``[tool.uv.sources]`` workspace entry), or delete the import;
* dependency cycle: remove one direction of the edge, or extract the shared
  API into ``platform/``;
* unclassified member: extend ``_classify_layer`` in this guard.
"""

from __future__ import annotations

import ast
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import pytest

pytestmark = pytest.mark.unit

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
ROOT_MANIFEST = REPOSITORY_ROOT / "pyproject.toml"


def _load_toml(path: Path) -> dict[str, Any]:
    """Read a TOML manifest on both 3.10 (tomli) and 3.11+ (tomllib)."""
    try:
        import tomllib
    except ModuleNotFoundError:
        import tomli as tomllib  # type: ignore[no-redef]

    return tomllib.loads(path.read_text(encoding="utf-8"))


def _distribution_to_import_root(distribution: str) -> str:
    """Map an internal distribution name to its import root.

    Only ``as-*`` internal distributions are mapped (``-`` -> ``_``); the
    version specifier / extra suffix, if any, is stripped first. Third-party
    distributions must never reach this function.
    """
    name = distribution
    for index, char in enumerate(distribution):
        if char not in "abcdefghijklmnopqrstuvwxyz0123456789-":
            name = distribution[:index]
            break
    return name.replace("-", "_")


@dataclass(frozen=True)
class Member:
    """One workspace member, as derived from its manifests."""

    path: str
    layer: str | None
    import_root: str
    declared_internal_roots: frozenset[str]


def _classify_layer(member_path: str) -> str | None:
    """Classify a member path into kernel/apps/services/testbed.

    Returns None for any shape this guard does not know about, which makes the
    structural test fail loudly instead of letting the member escape the
    boundary checks.
    """
    if member_path == "platform":
        return "kernel"
    first = member_path.split("/", 1)[0]
    if first in {"apps", "services", "testbed"} and "/" in member_path:
        return first
    return None


def _members() -> list[Member]:
    manifest = _load_toml(ROOT_MANIFEST)
    members: list[Member] = []
    for member_path in manifest["tool"]["uv"]["workspace"]["members"]:
        member_manifest = _load_toml(REPOSITORY_ROOT / member_path / "pyproject.toml")
        package = member_manifest["tool"]["hatch"]["build"]["targets"]["wheel"]["packages"][0]
        import_root = Path(package).name
        dependencies: list[str] = member_manifest.get("project", {}).get("dependencies", [])
        declared = frozenset(
            _distribution_to_import_root(dep)
            for dep in dependencies
            if dep.split("[", 1)[0].startswith("as-")
        )
        layer = _classify_layer(member_path)
        members.append(
            Member(
                path=member_path,
                layer=layer,
                import_root=import_root,
                declared_internal_roots=declared,
            )
        )
    return members


@pytest.fixture(scope="module")
def members() -> list[Member]:
    """Every declared workspace member with its layer and dependency facts."""
    return _members()


def _imported_roots(tree: ast.AST) -> set[str]:
    """Return the top-level package of every absolute import in one module."""
    roots: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            roots.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
            roots.add(node.module.split(".")[0])
    return roots


def _imports_by_member(members: list[Member]) -> dict[str, dict[str, set[str]]]:
    """Scan each member's src/ and map import root to the files using it.

    Only ``<member>/src/**/*.py`` is scanned and ``__pycache__`` is excluded;
    test directories are never scanned.
    """
    result: dict[str, dict[str, set[str]]] = {}
    for member in members:
        source_root = REPOSITORY_ROOT / member.path / "src"
        used: dict[str, set[str]] = {}
        for path in sorted(source_root.rglob("*.py")):
            if "__pycache__" in path.parts:
                continue
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
            for root in _imported_roots(tree):
                if root.startswith("as_"):
                    used.setdefault(root, set()).add(str(path.relative_to(REPOSITORY_ROOT)))
        result[member.path] = used
    return result


@pytest.fixture(scope="module")
def imports_by_member(members: list[Member]) -> dict[str, dict[str, set[str]]]:
    """The internal ``as_*`` import roots used by each member, per file."""
    return _imports_by_member(members)


def test_apps_do_not_import_each_other(
    members: list[Member], imports_by_member: dict[str, dict[str, set[str]]]
) -> None:
    """An app member must not import the package of another app member.

    Violates AGENT.md §4: "one app must never import another app" — a use case
    is one process, one failure domain and one canary unit. Fix by removing
    the import; logic two apps genuinely share must move down to the kernel
    (``platform/``), never sideways to a sibling app.
    """
    apps = [member for member in members if member.layer == "apps"]
    violations: list[str] = []
    for member in apps:
        sibling_roots = {other.import_root for other in apps if other.path != member.path}
        for root in sorted(sibling_roots & imports_by_member[member.path].keys()):
            files = ", ".join(sorted(imports_by_member[member.path][root]))
            violations.append(f"app {member.path} imports sibling app package '{root}' in: {files}")

    assert apps, "no apps-layer members found; the workspace manifest or this guard is broken"
    assert not violations, (
        "AGENT.md §4 violation — one app must never import another app:\n  "
        + "\n  ".join(violations)
        + "\nFix: remove the cross-app import; if the logic is shared, move it "
        "down into platform/ (the kernel). Do not couple app processes."
    )


def test_product_packages_never_import_testbed(
    members: list[Member], imports_by_member: dict[str, dict[str, set[str]]]
) -> None:
    """An apps/ or services/ member must not import any testbed package.

    Violates AGENT.md §4: the testbed is R&D asset and must never become a
    runtime dependency. The kernel-facing half is enforced by
    ``platform/tests/test_library_independence.py``; this is the product-side
    half. Fix by removing the import; product code must be shippable without
    the testbed.
    """
    testbed_roots = {member.import_root for member in members if member.layer == "testbed"}
    product_members = [member for member in members if member.layer in {"apps", "services"}]
    violations: list[str] = []
    for member in product_members:
        for root in sorted(testbed_roots & imports_by_member[member.path].keys()):
            files = ", ".join(sorted(imports_by_member[member.path][root]))
            violations.append(
                f"product member {member.path} imports testbed package '{root}' in: {files}"
            )

    assert testbed_roots, (
        "no testbed-layer members found; the workspace manifest or this guard is broken"
    )
    assert product_members, (
        "no apps/services members found; the workspace manifest or this guard is broken"
    )
    assert not violations, (
        "AGENT.md §4 violation — product packages (apps/, services/) must never "
        "depend on the testbed:\n  "
        + "\n  ".join(violations)
        + "\nFix: remove the import and relocate any needed logic into platform/ "
        "or the product member itself; testbed/ is a development-only asset."
    )


def test_internal_imports_are_declared_dependencies(
    members: list[Member], imports_by_member: dict[str, dict[str, set[str]]]
) -> None:
    """Every used ``as_*`` root must be the member's own root or a declared dep.

    An internal import that is not declared in the importing member's
    ``pyproject.toml`` is an accidental dependency that only works because the
    workspace installs everything together. Only "imported but undeclared" is
    checked — a declared-but-unused dependency is out of scope. Fix by either
    declaring the distribution name (hyphens, e.g. ``as-platform``) in the
    member's ``[project].dependencies`` with a ``[tool.uv.sources]`` workspace
    entry, or by removing the import.
    """
    violations: list[str] = []
    for member in members:
        allowed = {member.import_root} | set(member.declared_internal_roots)
        for root in sorted(set(imports_by_member[member.path]) - allowed):
            files = ", ".join(sorted(imports_by_member[member.path][root]))
            violations.append(
                f"member {member.path} imports '{root}' in: {files}, but '{root}' "
                f"is neither its own package ({member.import_root}) nor declared "
                "in its [project].dependencies"
            )

    assert not violations, (
        "AGENT.md §4 violation — internal imports must be declared dependencies "
        "of the importing member:\n  "
        + "\n  ".join(violations)
        + "\nFix: add the as-* distribution name (hyphens, e.g. as-platform) to "
        "the member's pyproject.toml dependencies with a [tool.uv.sources] "
        "workspace entry, or remove the import."
    )


def test_internal_dependencies_do_not_form_a_cycle(members: list[Member]) -> None:
    """The graph of declared internal dependencies must be acyclic.

    AGENT.md §4 permits services to depend on each other along the
    internal-API direction but a cycle (A -> B -> A) couples release, failure
    domains and reasoning. Fix by removing one direction of the edge, or by
    extracting the shared API into ``platform/``.
    """
    root_to_path = {member.import_root: member.path for member in members}
    graph: dict[str, set[str]] = {
        member.path: {
            root_to_path[root]
            for root in member.declared_internal_roots
            if root in root_to_path and root_to_path[root] != member.path
        }
        for member in members
    }

    cycles: list[list[str]] = []
    visited: set[str] = set()
    stack: list[str] = []
    on_stack: set[str] = set()

    def visit(node: str) -> None:
        visited.add(node)
        on_stack.add(node)
        stack.append(node)
        for neighbour in sorted(graph[node]):
            if neighbour in on_stack:
                start = stack.index(neighbour)
                cycles.append(stack[start:] + [neighbour])
            elif neighbour not in visited:
                visit(neighbour)
        stack.pop()
        on_stack.remove(node)

    for path in sorted(graph):
        if path not in visited:
            visit(path)

    assert not cycles, (
        "AGENT.md §4 violation — declared internal dependencies form a cycle:\n  "
        + "\n  ".join(" -> ".join(cycle) for cycle in cycles)
        + "\nFix: remove one direction of the dependency from the corresponding "
        "pyproject.toml, or extract the shared internal API into platform/."
    )


def test_every_workspace_member_classifies_into_one_layer(members: list[Member]) -> None:
    """Members split, without remainder, into kernel/apps/services/testbed.

    Classification is by path prefix (``platform``, ``apps/*``,
    ``services/*``, ``testbed/*``) and is read from the workspace manifest,
    not hard-coded. An unclassified member fails the gate so it cannot
    silently bypass the three boundary guards; all four layers must stay
    populated so none of the guards passes vacuously.
    """
    layers: dict[str, list[str]] = {"kernel": [], "apps": [], "services": [], "testbed": []}
    unclassified: list[str] = []
    for member in members:
        if member.layer is None:
            unclassified.append(member.path)
        else:
            layers[member.layer].append(member.path)

    assert members, "no workspace members found; the root pyproject manifest is empty or broken"

    assert not unclassified, (
        f"workspace member(s) {unclassified} cannot be classified into any of "
        "kernel/apps/services/testbed by path prefix; such a member silently "
        "bypasses the boundary guards. Fix: place it under platform/, apps/*, "
        "services/* or testbed/*, or extend _classify_layer in "
        "tests/test_layer_boundaries.py and the corresponding guard."
    )

    empty_layers = [name for name, paths in layers.items() if not paths]
    assert not empty_layers, (
        f"layer(s) {empty_layers} have no workspace members; the boundary guards "
        "for an empty layer pass vacuously. If the layer was deliberately removed, "
        "update tests/test_layer_boundaries.py; otherwise restore its member."
    )

    assert sum(len(paths) for paths in layers.values()) == len(members), (
        "a workspace member ended up in more than one layer classification; "
        f"classifications: {layers}"
    )
