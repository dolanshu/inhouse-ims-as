# Inhouse-IMS-AS — Copyright 2026 Dolan Shu <dolan.d.shu@gmail.com>, Apache-2.0
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.

"""Guard: the requirements registry and the acceptance matrix must agree.

The project has exactly one source of truth for requirements:
``docs/requirements/prd.md``. It carries four prefixes — ``REQ-F-*``
(functional), ``REQ-NF-*`` (non-functional), ``REQ-S-*`` (security) and
``REQ-G-*`` (governance) — and every REQ in the acceptance matrix must
trace back to one of those.

Four specific drift modes are guarded here:

1. **Numbering gaps** — a prefix that skips a number silently loses the
   requirement it stood for.
2. **Out-of-order appearance inside a section** — grouping by semantic
   subsection comes first (e.g. NF P0 vs NF P1 are separate groups and
   each must be internally ascending), but within the same subsection the
   REQ numbers must still go up so a reader never double-backs.
3. **A row in the acceptance matrix that does not exist in the PRD** —
   the matrix can only reference REQ ids the PRD actually declares.
4. **A PRD REQ that has no row in the acceptance matrix** — every
   requirement must have a place in the sign-off matrix, even if it is
   ``open`` or ``blocked``.

A fifth guard checks the test-layer markers: every ``-m`` flag used in
the Makefile ``test`` target must be declared in ``pyproject.toml`` so
``--strict-markers`` does not surprise anyone when a new layer is added.

See ``tests/test_version_consistency.py`` and
``tests/test_workspace_layout.py`` for the sibling guards.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

import pytest

pytestmark = pytest.mark.unit

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
PRD = REPOSITORY_ROOT / "docs" / "requirements" / "prd.md"
MATRIX = REPOSITORY_ROOT / "docs" / "acceptance" / "m8-test-plan-matrix.md"
MAKEFILE = REPOSITORY_ROOT / "Makefile"
PYPROJECT = REPOSITORY_ROOT / "pyproject.toml"

PREFIXES = ("F", "NF", "S", "G")

# Matches a REQ id anywhere in text: REQ-F-3, REQ-NF-16, etc.
REQ_ID = re.compile(r"\bREQ-(?P<prefix>F|NF|S|G)-(?P<number>\d+)\b")

# Matches a markdown heading starting with ### (third-level), used to
# identify subsections inside the PRD.
H3 = re.compile(r"^###\s+(?P<title>.+?)\s*$", re.MULTILINE)

# The two REQ-NF subsections that each must be internally ascending.
NF_P0_HEADING = "3.1 Core architectural constraints (P0)"
NF_P1_HEADING = "3.2 Scaling and governance (P1)"


def _load_toml(path: Path) -> dict[str, Any]:
    """Read a TOML manifest on both 3.10 (tomli) and 3.11+ (tomllib)."""
    try:
        import tomllib
    except ModuleNotFoundError:
        import tomli as tomllib  # type: ignore[no-redef]

    return tomllib.loads(path.read_text(encoding="utf-8"))


def _prd_all_req_ids() -> dict[str, list[int]]:
    """Return every REQ id declared in the PRD, grouped by prefix.

    Returns:
        A dict mapping prefix (``"F"``, ``"NF"``, ``"S"``, ``"G"``) to a
        list of integer numbers, in the order they first appear in the
        document.
    """
    text = PRD.read_text(encoding="utf-8")
    seen: dict[str, set[int]] = {p: set() for p in PREFIXES}
    ordered: dict[str, list[int]] = {p: [] for p in PREFIXES}

    for match in REQ_ID.finditer(text):
        prefix = match.group("prefix")
        number = int(match.group("number"))
        if number not in seen[prefix]:
            seen[prefix].add(number)
            ordered[prefix].append(number)

    return ordered


def _prd_req_ids_by_subsection() -> list[tuple[str, str, list[int]]]:
    """Group REQ ids by the H3 subsection in which their #### heading appears.

    Only the ``#### REQ-<prefix>-<N>:`` headings count — i.e. the lines
    that *define* a requirement. Cross-references inside user stories or
    prose ("对应 REQ-F-1") are not definitions and must not affect the
    ordering assertion.

    Returns a list of ``(heading, prefix, numbers_in_order)`` tuples, one
    per (subsection, prefix) pair that contains at least one REQ
    definition.
    """
    text = PRD.read_text(encoding="utf-8")
    lines = text.splitlines()

    # Find all H3 headings with their line numbers.
    headings: list[tuple[int, str]] = []
    for i, line in enumerate(lines):
        m = H3.match(line)
        if m:
            headings.append((i, m.group("title")))

    # Pattern for a fourth-level heading that *defines* a requirement.
    req_heading = re.compile(r"^####\s+REQ-(?P<prefix>F|NF|S|G)-(?P<number>\d+)")

    result: list[tuple[str, str, list[int]]] = []

    for idx, (start_line, heading) in enumerate(headings):
        end_line = headings[idx + 1][0] if idx + 1 < len(headings) else len(lines)

        by_prefix: dict[str, list[int]] = {p: [] for p in PREFIXES}
        for line in lines[start_line:end_line]:
            m = req_heading.match(line)
            if m:
                prefix = m.group("prefix")
                number = int(m.group("number"))
                by_prefix[prefix].append(number)

        for prefix in PREFIXES:
            if by_prefix[prefix]:
                result.append((heading, prefix, by_prefix[prefix]))

    return result


def _matrix_req_ids_first_column() -> set[str]:
    """Return every REQ id that appears in the matrix's req_id column.

    Only the first column (``req_id``) counts as "the matrix has a row
    for this REQ". Non-REQ row ids (KERNEL-§5, 5.4-F-13, etc.) are
    excluded by the regex shape.
    """
    text = MATRIX.read_text(encoding="utf-8")
    ids: set[str] = set()

    for line in text.splitlines():
        # Table rows start with |. First real column is after the first |.
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if not cells:
            continue
        first = cells[0]
        m = REQ_ID.match(first)
        if m:
            ids.add(first)

    return ids


def _matrix_req_ids_all() -> set[str]:
    """Return every REQ id that appears anywhere in the matrix.

    This includes ids mentioned in the ``evidence`` column, used for the
    "matrix never references a REQ the PRD does not declare" assertion.
    """
    text = MATRIX.read_text(encoding="utf-8")
    return {m.group(0) for m in REQ_ID.finditer(text)}


def _makefile_test_markers() -> list[str]:
    """Extract every marker name used by ``-m`` in the Makefile test target.

    Handles compound expressions like ``-m "unit or contract"`` by
    splitting on ``or`` and trimming whitespace / quotes.
    """
    text = MAKEFILE.read_text(encoding="utf-8")
    lines = text.splitlines()

    # Find the test: target and collect lines until the next target.
    in_test = False
    test_lines: list[str] = []
    for line in lines:
        if re.match(r"^test:", line):
            in_test = True
            test_lines.append(line)
            continue
        if in_test:
            # Recipe lines start with a tab; non-recipe lines end the target.
            if line.startswith("\t"):
                test_lines.append(line)
            elif line.strip() == "" or line.startswith("#"):
                # blank or comment inside the recipe block — keep going
                continue
            else:
                break

    markers: list[str] = []
    # Match -m followed by a quoted or unquoted marker expression.
    # The expression stops at the next flag (another -x) or end of line.
    marker_re = re.compile(r"-m\s+[\"']([^\"']+)[\"']|-m\s+(\S+)")
    for line in test_lines:
        for match in marker_re.finditer(line):
            expr = match.group(1) or match.group(2) or ""
            expr = expr.strip()
            if not expr:
                continue
            # Split on boolean operators; we just want each marker name.
            parts = re.split(r"\s+(?:or|and|not)\s+", expr)
            for part in parts:
                name = part.strip()
                if name:
                    markers.append(name)

    return markers


def _pyproject_markers() -> set[str]:
    """Return the set of marker names declared in pyproject.toml."""
    manifest = _load_toml(PYPROJECT)
    raw_markers = manifest["tool"]["pytest"]["ini_options"]["markers"]
    return {m.split(":", 1)[0].strip() for m in raw_markers}


# ---------------------------------------------------------------------------
# Assertion 1 — numbering is gap-free per prefix
# ---------------------------------------------------------------------------


def test_prd_req_numbering_is_contiguous_per_prefix() -> None:
    """Each REQ prefix in prd.md has no gaps: 1..N with nothing missing.

    A gap means a requirement silently disappeared (or was never added)
    and the matrix / design / tests may not cover it. Fix by either
    restoring the missing REQ or — if it was deliberately removed —
    renumbering and updating every downstream reference.
    """
    by_prefix = _prd_all_req_ids()

    for prefix in PREFIXES:
        numbers = sorted(by_prefix[prefix])
        assert numbers, (
            f"prd.md contains zero REQ-{prefix}-* entries. That cannot be right — "
            f"the PRD is supposed to carry all four prefixes. Check that the file "
            f"is intact and the REQ id pattern still matches."
        )
        expected = list(range(1, numbers[-1] + 1))
        assert numbers == expected, (
            f"REQ-{prefix}-* numbering has gaps in prd.md: "
            f"found {numbers}, expected 1..{numbers[-1]} (contiguous). "
            f"Missing: {sorted(set(expected) - set(numbers))}. "
            f"Fix: either restore the missing REQ-{prefix}-N entry, or — if it "
            f"was deliberately removed — renumber downstream and update every "
            f"reference in docs/ and code/."
        )


# ---------------------------------------------------------------------------
# Assertion 2 — within each subsection, REQ ids appear in ascending order
# ---------------------------------------------------------------------------


def test_prd_req_ids_ascend_within_each_subsection() -> None:
    """Inside each H3 subsection, REQ numbers of the same prefix ascend.

    Grouping comes first (e.g. REQ-NF is split into P0 and P1 subsections,
    and NF-6/7/8 live in the P1 group while NF-9 lives in P0 — that cross-
    section jump is not a failure). But *within* one subsection the list
    must still go up, so a reader never reads 3 → 1 → 2.

    For REQ-NF specifically, the two groups are:
    ``### 3.1 Core architectural constraints (P0)`` and
    ``### 3.2 Scaling and governance (P1)``.
    """
    grouped = _prd_req_ids_by_subsection()

    offenders: list[str] = []
    for heading, prefix, numbers in grouped:
        if numbers != sorted(numbers):
            offenders.append(f"§{heading} / REQ-{prefix}-*: order {numbers} is not ascending")

    assert not offenders, (
        "REQ ids do not ascend within their subsection in prd.md:\n  "
        + "\n  ".join(offenders)
        + "\n\nRule: grouping by semantic subsection takes priority over global "
        "numbering (跨小节跳变不算失败), but within one subsection the numbers "
        "must still go up. Fix by reordering the entries inside that subsection "
        "or moving the out-of-order REQ to the subsection where it belongs."
    )


def test_prd_nf_has_two_named_subsections() -> None:
    """The PRD must still carry the two named NF subsections.

    If these headings are renamed, the "group semantics" assertion above
    would silently compare the wrong groups. This check makes sure the
    section names the assertion relies on still exist.
    """
    text = PRD.read_text(encoding="utf-8")
    for heading in (NF_P0_HEADING, NF_P1_HEADING):
        assert f"### {heading}" in text, (
            f"prd.md no longer contains the subsection '### {heading}'. "
            f"Assertion 2 (grouped ordering) relies on these two NF groups. "
            f"If the heading was renamed, update NF_P0_HEADING / NF_P1_HEADING "
            f"in tests/test_requirements_registry.py to match."
        )


# ---------------------------------------------------------------------------
# Assertion 3 — every REQ id mentioned in the matrix exists in the PRD
# ---------------------------------------------------------------------------


def test_matrix_never_references_unknown_req_ids() -> None:
    """Every REQ-<prefix>-<number> in the matrix exists in prd.md.

    The matrix can mention REQ ids in the req_id column *and* in the
    evidence column. Both must resolve to a real PRD entry; a typo or a
    stale reference must not pass. Non-REQ row ids (KERNEL-§5, etc.) are
    excluded by the regex shape and are not checked.
    """
    matrix_ids = _matrix_req_ids_all()
    prd_ids = _prd_all_req_ids()
    prd_flat = {f"REQ-{p}-{n}" for p in PREFIXES for n in prd_ids[p]}

    unknown = sorted(matrix_ids - prd_flat)
    assert not unknown, (
        "m8-test-plan-matrix.md references REQ ids that do not exist in prd.md:\n  "
        + "\n  ".join(unknown)
        + "\n\nViolation of 文档链一致性 (AGENT.md §3). Fix: either add the "
        "missing REQ to docs/requirements/prd.md, or correct the reference in "
        "the matrix so it points to a real REQ id."
    )


# ---------------------------------------------------------------------------
# Assertion 4 — every PRD REQ has a row in the matrix
# ---------------------------------------------------------------------------


def test_every_prd_req_has_a_matrix_row() -> None:
    """Every REQ declared in prd.md gets its own row in the sign-off matrix.

    A requirement with no matrix row is a requirement nobody will ever
    sign off on. Fix by adding the missing row (with status ``open`` and
    ``signed_by = 维护者待签``) to docs/acceptance/m8-test-plan-matrix.md.
    """
    matrix_rows = _matrix_req_ids_first_column()
    prd_ids = _prd_all_req_ids()
    prd_flat = {f"REQ-{p}-{n}" for p in PREFIXES for n in prd_ids[p]}

    missing = sorted(prd_flat - matrix_rows)
    assert not missing, (
        "These REQ ids are declared in prd.md but have no row in "
        "m8-test-plan-matrix.md:\n  "
        + "\n  ".join(missing)
        + "\n\nRule: every requirement must have a place in the sign-off "
        "matrix (§2 非功能签收 or the appropriate section). Fix by adding a "
        "row with status=open and signed_by=维护者待签, plus evidence pointing "
        "at the relevant ADR / test plan / engineering run."
    )


# ---------------------------------------------------------------------------
# Assertion 5 — every -m marker in the Makefile test target is declared
# ---------------------------------------------------------------------------


def test_makefile_test_markers_are_all_declared() -> None:
    """Every pytest marker used by ``make test`` is declared in pyproject.toml.

    ``--strict-markers`` is on, so an undeclared marker turns the whole
    run red. Compound expressions like ``-m "unit or contract"`` are
    split and each marker is checked individually. Fix by either adding
    the marker to ``[tool.pytest.ini_options] markers`` in pyproject.toml
    or removing the ``-m`` invocation from the Makefile test target.
    """
    used = _makefile_test_markers()
    declared = _pyproject_markers()

    assert used, (
        "Makefile test target uses zero pytest markers. That means this guard "
        "has nothing to check — either the test target was emptied or the "
        "marker extraction logic is broken."
    )

    undeclared = sorted(m for m in used if m not in declared)
    assert not undeclared, (
        "Makefile test target uses pytest markers that are not declared in "
        "pyproject.toml:\n  "
        + "\n  ".join(undeclared)
        + "\n\nWith --strict-markers an undeclared marker fails the whole run. "
        "Fix: add each marker to [tool.pytest.ini_options].markers in "
        "pyproject.toml, or remove the -m invocation from the Makefile "
        "test target."
    )
