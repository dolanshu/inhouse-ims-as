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

"""Guard: evidence carries its own verdict, its own machine and its own date.

Three facts about this repository were true at the same time for weeks:

* a file said ``promtool check rules`` produced ``SUCCESS: 5 rules found``;
* a file recorded ``==> helm lint /home/shudong/project/3rdparty-as/deploy/helm``
  — the same user name, the same project path;
* the workstation the work was being discussed on had **no** helm, kubectl, kind
  or promtool at all (measured 2026-10-11).

So the evidence came from a *second machine*, and the anonymous 「本机」 in the
prose was pointing at two different machines depending on who read it. That is
not a comprehension failure — **the facts had no metadata**. Every re-litigation
of 「does this project have infra capability?」 started there.

This module guards the four-layer mechanism approved in
``docs/handoff/2026-10-11-open-adjudication-register.md`` §7.4:

1. **The file name is the verdict** — evidence under ``docs/acceptance/artifacts/**``
   is prefixed ``PASS-`` / ``FAIL-`` / ``FAILCLOSED-``. A reader who sees only a
   filename still knows whether they are holding a pass, a command that failed, or
   the deliberate 「refuse rather than guess」 transcript.
2. **A machine has a name — and it is measured, not typed.**
   ``docs/environments.md`` carries one row per *measured* machine. The data is
   produced by ``tools/env-probe.sh``: the script exists, it is executable, the
   register links to it, and the register carries no half-filled placeholder row
   waiting for a human who never comes back to fill it.
3. **A status claim is a triple** — ``(verdict, evidence file, date)``; asserted here
   structurally, via the entry-point links that carry the convention.
4. **This file** — the regression guard.

Scope note (why some directories are not scanned by rule 5)
------------------------------------------------------------
Rule 5 bans the anonymous 「本机无 …」 phrasing in prose. Three directory trees are
**excluded**, because rewriting them would destroy a preserved audit chain rather
than fix a live statement:

* ``docs/handoff/**`` — session handoff records. Their own §0.1 forbids deleting or
  silently rewriting entries; the historical 「本机无 promtool」 rows *are* the
  record of the confusion this guard was written to stop.
* ``docs/reviews/**`` — review records, including maintainer-signed ones.
* ``docs/acceptance/**`` — historical runbook originals; ``docs/README.md``
  states they are 不删除、不移动、不改写.

Everything else under ``docs/**/*.md`` **is** scanned, including ``plan.md``,
``product-packaging-plan.md`` and the ADR directory — which is why those files
now name the environment (``dev-win03ib7niepf0``) instead of 「本机」.

The proximity test is deliberately **same-line**: a hit is 「本机无」 plus one of
helm / kubectl / kind / promtool on one physical line. A same-line rule has no
false positives on prose that merely *mentions* a tool near the word 「本机」, and
it is a rule a writer can satisfy by naming the machine.

See ADR-0018 for why this repository guards structure with tests instead of
convention, and tests/test_workspace_layout.py for the sibling guards.

The tool behind layer (2) gets its own guard
---------------------------------------------
The rules above police evidence *file names*. They say nothing about the tools
that **produce** the evidence, and that gap was live: ``tools/env-probe.sh``
passed ``bash -n`` and then failed on every single invocation with
``tr: when not truncating set1, string2 must be non-empty`` (measured 2026-10-11;
it had never been run, only syntax-checked). **``bash -n`` verifies syntax, not
runtime behaviour** — a bad ``tr`` argument, a ``case`` with no default branch, or
an unescaped backtick inside double quotes all pass it and all break the script.
So the availability of the tool scripts is locked here too: the probe is actually
executed, and the installer is checked for the two flags that make a dry run
possible at all.
"""

from __future__ import annotations

import os
import re
import shutil
import subprocess
from pathlib import Path

import pytest

pytestmark = pytest.mark.unit

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
DOCS = REPOSITORY_ROOT / "docs"
ARTIFACTS = DOCS / "acceptance" / "artifacts"
M5_INDEX = ARTIFACTS / "m5" / "README.md"
ENVIRONMENTS = DOCS / "environments.md"
ENV_PROBE = REPOSITORY_ROOT / "tools" / "env-probe.sh"
BOOTSTRAP_INFRA = REPOSITORY_ROOT / "tools" / "bootstrap-infra.sh"
ARCHITECTURE_README = DOCS / "architecture" / "README.md"

# Layer 1. `<verdict>-<subject>[-sample]-<date>.txt`; lowercase, kebab-case subject.
# `FAILCLOSED-` is listed before `FAIL-` so the longer prefix wins. The three
# verdicts are not interchangeable: PASS- is a green run, FAIL- is a command that
# ran and exited non-zero, FAILCLOSED- is the deliberate 「refuse rather than
# guess」 path. All three were needed the moment deploy/kind/scripts/m5-record-artifacts.sh
# started naming files after the exit code it actually observed.
EVIDENCE_NAME = re.compile(
    r"^(?P<verdict>PASS|FAILCLOSED|FAIL)-[a-z0-9-]+(-sample)?-\d{4}-\d{2}-\d{2}\.txt$"
)

# Layer 2. An environment name is kebab-case and never empty.
ENVIRONMENT_NAME = re.compile(r"^[a-z0-9][a-z0-9-]*$")

# Layer 2. The historical defect: a registry row whose hostname is an
# angle-bracket placeholder. Such a row reads as 「there is a machine, nobody has
# filled it in」 — which is exactly how a machine with no name keeps being cited
# as if it had one.
ANGLE_PLACEHOLDER = re.compile(r"<\s*hostname\s*>", re.IGNORECASE)

# Layer 5. The anonymous denial phrasing, and the tools that make it a claim.
ANONYMOUS_DENIAL = "本机无"
INFRA_TOOLS = ("helm", "kubectl", "kind", "promtool")

# Rule 5 scope exclusions — see the module docstring for why each is preserved.
DOCS_SCAN_EXCLUDED = (
    DOCS / "handoff",
    DOCS / "reviews",
    DOCS / "acceptance",
)

# What a FAILCLOSED- entry must say nearby before it may sit in an index.
# docs/acceptance/artifacts/m5/README.md labels these rows "**Not pass evidence**".
NOT_PASS_MARKERS = ("Not pass evidence",)


def _markdown_files(root: Path) -> list[Path]:
    return sorted(path for path in root.rglob("*.md"))


def _evidence_files() -> list[Path]:
    return sorted(ARTIFACTS.rglob("*.txt"))


def _excluded(path: Path) -> bool:
    return any(path == root or root in path.parents for root in DOCS_SCAN_EXCLUDED)


# ---------------------------------------------------------------------------
# Layer 1 — the file name is the verdict
# ---------------------------------------------------------------------------


def test_artifacts_directory_exists() -> None:
    """An empty scan would make every rule below pass vacuously."""
    assert ARTIFACTS.is_dir(), f"{ARTIFACTS.relative_to(REPOSITORY_ROOT)} is missing"
    assert _evidence_files(), f"no .txt evidence found under {ARTIFACTS}"


@pytest.mark.parametrize("evidence", _evidence_files(), ids=lambda p: p.name)
def test_evidence_filename_states_its_verdict(evidence: Path) -> None:
    """`PASS-` / `FAIL-` / `FAILCLOSED-` prefix, kebab-case subject, ISO date suffix."""
    assert EVIDENCE_NAME.match(evidence.name), (
        f"{evidence.relative_to(REPOSITORY_ROOT)} does not say what it is. Rule (1) of the "
        f"four-layer evidence mechanism: every file under docs/acceptance/artifacts/ is named "
        f"'<结论>-<被验项>[-sample]-<日期>.txt' with the verdict in the prefix — PASS-<subject>-"
        f"<YYYY-MM-DD>.txt, FAIL-<subject>-<YYYY-MM-DD>.txt (the command ran and failed), or "
        f"FAILCLOSED-<subject>-<YYYY-MM-DD>.txt (it refused rather than guessed). Rename it with "
        f"`git mv`. A file recording a failure must never carry a PASS- prefix, and a "
        f"FAILCLOSED- file is not pass evidence either."
    )


@pytest.mark.parametrize("evidence", _evidence_files(), ids=lambda p: p.name)
def test_failclosed_evidence_records_an_actual_transcript(evidence: Path) -> None:
    """A verdict prefix with an empty body proves nothing; the body must be a transcript."""
    if evidence.name.startswith(("FAILCLOSED-", "FAIL-")):
        assert evidence.stat().st_size > 0, (
            f"{evidence.relative_to(REPOSITORY_ROOT)} is empty. A FAIL-/FAILCLOSED- file must "
            f"record the actual output (exit code, error text); otherwise it is a claim, not "
            f"evidence."
        )


def test_failclosed_entries_are_labelled_as_not_pass_evidence() -> None:
    """An index must never let a FAILCLOSED- file pass for a green result."""
    assert M5_INDEX.is_file(), f"{M5_INDEX.relative_to(REPOSITORY_ROOT)} is missing"
    text = M5_INDEX.read_text(encoding="utf-8")

    mentioned = sorted(set(re.findall(r"FAILCLOSED-[a-z0-9-]+-\d{4}-\d{2}-\d{2}\.txt", text)))
    assert mentioned, (
        "the m5 evidence index mentions no FAILCLOSED- file at all. Rule (1): the index must "
        "list every file in the directory so a FAILCLOSED- transcript cannot be mistaken for a "
        "missing one."
    )

    for name in mentioned:
        line = next((line for line in text.splitlines() if name in line and "|" in line), text)
        assert any(marker in line for marker in NOT_PASS_MARKERS), (
            f"{M5_INDEX.relative_to(REPOSITORY_ROOT)} lists {name} without saying it is not pass "
            f"evidence. Rule (1) of the four-layer mechanism: a FAILCLOSED- transcript (here: "
            f'exit=1, M5_STRICT=1 with no kind-as-m5 cluster) must be labelled "Not pass '
            f'evidence" in the same table row, so nobody counts it towards the pass list.'
        )


def test_fail_entries_are_labelled_as_not_pass_evidence() -> None:
    """A FAIL- transcript in the index must carry the same 「not pass evidence」 label.

    ``FAIL-`` is the verdict for a command that ran and exited non-zero — the case
    that used to be mislabelled ``PASS-`` because the recorder read the exit code
    of its own output filter. A failing run recorded next to passing ones is
    exactly the shape of claim this guard exists to prevent, so the label is
    mandatory in the index row.
    """
    assert M5_INDEX.is_file(), f"{M5_INDEX.relative_to(REPOSITORY_ROOT)} is missing"
    text = M5_INDEX.read_text(encoding="utf-8")

    # `FAIL-` cannot match `FAILCLOSED-`, so no boundary handling is needed here.
    mentioned = sorted(set(re.findall(r"FAIL-[a-z0-9-]+-\d{4}-\d{2}-\d{2}\.txt", text)))

    for name in mentioned:
        line = next((line for line in text.splitlines() if name in line and "|" in line), text)
        assert any(marker in line for marker in NOT_PASS_MARKERS), (
            f"{M5_INDEX.relative_to(REPOSITORY_ROOT)} lists {name} without saying it is not pass "
            f"evidence. Rule (1) of the four-layer mechanism: a FAIL- transcript records a command "
            f'that exited non-zero and must be labelled "Not pass evidence" in the same table row.'
        )


# ---------------------------------------------------------------------------
# Layer 2 — a machine has a name
# ---------------------------------------------------------------------------


def test_environment_register_exists() -> None:
    """The register is the only place a machine may be named."""
    assert ENVIRONMENTS.is_file(), (
        f"{ENVIRONMENTS.relative_to(REPOSITORY_ROOT)} is missing. Rule (2) of the four-layer "
        f"mechanism: documents must reference a machine by the name registered in "
        f"docs/environments.md, never by an anonymous 「本机」. Without the register there is "
        f"nowhere to look a machine up, and the ambiguity this repository kept re-litigating "
        f"returns."
    )


def test_environment_probe_exists_and_is_executable() -> None:
    """The register is generated by a tool, so the tool itself must exist and run.

    Layer (2) of the four-layer mechanism: 「a machine has a name」 is no longer
    maintained by hand. It is produced by ``tools/env-probe.sh`` — the script
    that reads the hostname, the OS and the toolchain off the machine it runs on.
    A register that still has to be typed in drifts, and drifted metadata is what
    this whole mechanism was built to kill.
    """
    assert ENV_PROBE.is_file(), (
        f"{ENV_PROBE.relative_to(REPOSITORY_ROOT)} is missing. Layer (2) of the four-layer "
        f"mechanism: docs/environments.md is generated by a probe, not by a human remembering a "
        f"hostname. Restore the script, or point the register at whatever replaces it."
    )
    assert os.access(ENV_PROBE, os.X_OK), (
        f"{ENV_PROBE.relative_to(REPOSITORY_ROOT)} is not executable. It is invoked as "
        f"`tools/env-probe.sh`, not `bash tools/env-probe.sh`; a non-executable probe is a probe "
        f"nobody runs, and the register goes back to being typed in by hand."
    )


def test_environment_register_carries_a_named_row() -> None:
    """Generated or not, the table must still hold at least one usable row."""
    text = ENVIRONMENTS.read_text(encoding="utf-8")
    header = "| Environment name | hostname |"
    assert header in text, (
        "docs/environments.md must carry the registry table with the columns "
        "Environment name / hostname / Tools present / Tools missing / Evidence produced "
        "here / Notes."
    )

    rows = [line for line in text.splitlines() if line.startswith("| `")]
    named = [
        row
        for row in rows
        if ENVIRONMENT_NAME.match(row.split("|")[1].strip().strip("`"))
        and row.split("|")[2].strip()
    ]
    assert named, (
        "docs/environments.md registers no usable environment. Run "
        "`tools/env-probe.sh --markdown` on a machine and paste the result: each row needs a "
        "kebab-case environment name (column 1) and a real hostname (column 2)."
    )


def test_environment_register_has_no_empty_hostname_placeholder() -> None:
    """A row waiting for someone to fill in the hostname is not a machine.

    The register used to carry an infra row whose hostname cell was unfillable.
    It read as 「a machine exists but nobody wrote it down」, which is how an
    unnamed machine kept getting cited as evidence. Machines enter this table by
    being probed, not by being promised.
    """
    text = ENVIRONMENTS.read_text(encoding="utf-8")
    here = ENVIRONMENTS.relative_to(REPOSITORY_ROOT)
    offenders: list[str] = []

    for number, line in enumerate(text.splitlines(), 1):
        if ANGLE_PLACEHOLDER.search(line):
            offenders.append(f"{here}:{number}: {line.strip()}")
        if line.startswith("|") and ("<" in line or ">" in line):
            offenders.append(f"{here}:{number}: {line.strip()}")

    assert not offenders, (
        "the environment register carries an empty-hostname placeholder:\n  "
        + "\n  ".join(offenders[:5])
        + "\n\nLayer (2): do not reserve a row for a machine that has not been measured. A "
        "placeholder row reads as an existing-but-unnamed machine, which is the exact confusion "
        "this register exists to remove. Probe the machine with `tools/env-probe.sh` and add the "
        "row when it produces a hostname."
    )


def test_environment_register_links_the_probe() -> None:
    """A generated register must say how to regenerate itself."""
    text = ENVIRONMENTS.read_text(encoding="utf-8")
    assert "tools/env-probe.sh" in text, (
        "docs/environments.md never mentions tools/env-probe.sh. The register is generated, so "
        "the reader needs the command that regenerates it — otherwise the next reader edits the "
        "table by hand, which is how it drifted in the first place."
    )
    assert "--markdown" in text, (
        "docs/environments.md does not tell the reader how to get a paste-ready row. "
        "`tools/env-probe.sh --markdown` is the documented way to add or refresh an environment."
    )


# ---------------------------------------------------------------------------
# Layer 2 (continued) — the probe must RUN, not merely parse
# ---------------------------------------------------------------------------


def test_environment_probe_markdown_mode_actually_runs() -> None:
    """`env-probe.sh --markdown` must exit 0 and emit a table header.

    Existence and the executable bit are not enough. On 2026-10-11 the probe was
    present, executable, and passed `bash -n`, and it still failed on every run —
    so the register layer this module guards was unmaintained in practice.

    The probe is read-only by contract (it installs nothing, writes nothing, needs
    no root), so running it here is safe; it only does `command -v` lookups plus
    one `--version` per tool found, which keeps it in the second-scale range.

    Args:
        None — the machine under test is this one.

    Raises:
        AssertionError: if the script is missing, exits non-zero, or prints no header.
    """
    bash = shutil.which("bash")
    if bash is None:
        pytest.skip("no bash on PATH; the probe's shebang cannot be exercised here")

    completed = subprocess.run(
        [bash, str(ENV_PROBE), "--markdown"],
        capture_output=True,
        text=True,
        timeout=60,
        check=False,
        cwd=REPOSITORY_ROOT,
    )
    first_line = completed.stdout.splitlines()[0] if completed.stdout else ""

    assert completed.returncode == 0, (
        f"`bash tools/env-probe.sh --markdown` exited {completed.returncode}; the probe "
        f"itself must exit 0 whenever it completed — a missing tool is a normal result, "
        f"only a usage error "
        f"exits 2. stderr was: {completed.stderr.strip()[:400]!r}. Reproduce it by hand with "
        f"`bash tools/env-probe.sh --markdown`. Remember that `bash -n` passing proves nothing "
        f"here: it checks syntax only, and this failure was a runtime argument error."
    )
    assert "环境名" in first_line, (
        f"the Markdown output does not start with a table header: {first_line!r}. The probe's "
        f"--markdown mode is what gets pasted into docs/environments.md, so the first line must "
        f"carry the 环境名 column; check the header block in tools/env-probe.sh."
    )


def test_bootstrap_infra_offers_a_dry_run_and_help() -> None:
    """The installer must expose `--dry-run` and `--help`.

    `bootstrap-infra.sh` is deliberately **not** executed by this guard: outside a
    dry run it downloads and installs four binaries, which no unit test may do.
    What can be locked statically is that the two flags making a no-op run
    possible still exist — without them there is no way to inspect the plan
    without side effects.

    This is a text assertion, so it cannot catch a script that accepts `--dry-run`
    and then crashes before printing anything. Please run it by hand once:
    `bash tools/bootstrap-infra.sh --dry-run` and `bash tools/bootstrap-infra.sh --help`.
    """
    assert BOOTSTRAP_INFRA.is_file(), (
        f"{BOOTSTRAP_INFRA.relative_to(REPOSITORY_ROOT)} is missing. It is the only supported way "
        f"to get helm / kubectl / kind / promtool on this machine without root and without apt; "
        f"without it the register's 缺失 rows have no remedy attached."
    )
    text = BOOTSTRAP_INFRA.read_text(encoding="utf-8")
    for flag in ("--dry-run", "--help"):
        assert flag in text, (
            f"{BOOTSTRAP_INFRA.relative_to(REPOSITORY_ROOT)} no longer accepts {flag}. Both flags "
            f"are what allow a side-effect-free inspection; remove one and the only remaining way "
            f"to look at the plan is a real install. Restore the flag in the argument loop, then "
            f"verify by hand: `bash tools/bootstrap-infra.sh --dry-run` and "
            f"`bash tools/bootstrap-infra.sh --help`."
        )


# ---------------------------------------------------------------------------
# Layer 3 — the entry point must carry the convention, not just the files
# ---------------------------------------------------------------------------


def test_architecture_entry_point_exists_and_links_the_conventions() -> None:
    """docs/architecture/README.md ties the map, the boundary and the evidence together."""
    assert ARCHITECTURE_README.is_file(), (
        "docs/architecture/README.md is missing. It is the entry point for the architecture "
        "tree: which document is normative (hld.md / lld.md), what is delivered versus "
        "scaffolding, how evidence is graded, and what is still undecided."
    )

    text = ARCHITECTURE_README.read_text(encoding="utf-8")
    required = {
        "hld.md": "must name the normative high-level design",
        "lld.md": "must name the normative low-level design",
        "docs/environments.md": (
            "must point at the environment register, otherwise a reader lands on a conclusion "
            "with no machine attached — the failure this guard exists to prevent"
        ),
    }
    for reference, why in required.items():
        assert reference in text, (
            f"docs/architecture/README.md never mentions {reference}: {why}. Restore the link; "
            f"do not delete the requirement."
        )


def test_status_claims_in_the_entry_point_use_the_triple() -> None:
    """The entry point must state the triple convention, not merely use it once."""
    # The triplet phrase is line-wrapped in the source (§3), so collapse whitespace
    # before matching — the full literal must still appear in order.
    text = " ".join(ARCHITECTURE_README.read_text(encoding="utf-8").split())
    assert "(conclusion, evidence file, date)" in text, (
        "docs/architecture/README.md must state the status-claim triplet "
        "(conclusion, evidence file, date). Rule (3) of the four-layer mechanism: "
        '"verified / unverified" is never a bare sentence — it always names the '
        "evidence file and its date."
    )


# ---------------------------------------------------------------------------
# Layer 2 (continued) / rule 5 — no anonymous 「本机无」 in live prose
# ---------------------------------------------------------------------------


def test_live_prose_never_denies_tooling_on_an_anonymous_machine() -> None:
    """`本机无 helm` in live documentation is the sentence this repository retracted."""
    offenders: list[str] = []

    for markdown in _markdown_files(DOCS):
        if _excluded(markdown):
            continue
        for number, line in enumerate(markdown.read_text(encoding="utf-8").splitlines(), 1):
            if ANONYMOUS_DENIAL not in line:
                continue
            if any(tool in line for tool in INFRA_TOOLS):
                offenders.append(
                    f"{markdown.relative_to(REPOSITORY_ROOT)}:{number}: {line.strip()[:120]}"
                )

    assert not offenders, (
        "anonymous machine denial found in live documentation:\n  "
        + "\n  ".join(offenders)
        + "\n\nRule (2) of the four-layer evidence mechanism: never write 「本机」 as a machine. "
        "Say which machine — name it from docs/environments.md, e.g. "
        "「环境 dev-win03ib7niepf0 无 helm」 — so the reader knows whether the conclusion can be "
        "reproduced where they are. The prose that produced these sentences is preserved in "
        "docs/handoff/ and docs/reviews/, which is exactly why they are excluded from this scan "
        "rather than deleted from history."
    )
