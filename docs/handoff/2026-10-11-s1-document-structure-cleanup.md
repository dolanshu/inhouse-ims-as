<!--
Inhouse-IMS-AS — Copyright 2026 Dolan Shu <dolan.d.shu@gmail.com>, Apache-2.0

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
-->

# S1 · Document and Structural Consistency Cleanup (First Batch)

> **Landed: 2026-10-11. Status: landed, awaiting maintainer review.**
>
> **This document is an "execution instruction", not a review record.** It does not depend on any conversation context: reading section 2 is enough to do the work.
> After executing, please **write a separate execution record**; do not backfill the execution results into this document's "completed" state.
>
> This batch **signs off no REQ and closes no milestone**. All review records are marked "landed, awaiting maintainer review".

## 0. Reading Order

| You are | Which sections to read |
|---|---|
| Executor (an AI agent in a new session, or a person) | §1 → §2 → §3 → §4 → §5 → §6, then start with the first item of §2. **§2.6 is a decided item, not a to-do** |
| Maintainer | §2.6 (the audit trace of the decided item) → §3 → §5 → §6 |

---

## 1. Background

The 2026-10-11 review found **several inconsistencies between documents in this repository, as well as process instructions pointing at files that do not exist**. They do not involve product code,
but they cause two practical consequences: **readers misjudge the project status** (for example thinking a milestone's acceptance items are in some file),
and **automation falls through** (for example some target inevitably fails). This batch only handles the **verified, reproducible** five of them,
and each gives the location, evidence of the current state, the goal and the acceptance criterion.

Note on the review method: all the "current state" items below were measured/searched on this machine on 2026-10-11. But **documents in this repository are continuously appended to, so line numbers drift** ——
the executor **must re-verify each item before changing anything** and must not copy the line numbers given here.

---

## 2. Scope

### 2.1 Task 1 · Fix the broken link in `AGENT.md`

| Item | Content |
|---|---|
| **Location** | step 4 of "10.4 Handover protocol → opening ritual" in `AGENT.md` (measured at `:238` on 2026-10-11) |
| **Current state (evidence)** | the original text of that step is "read the acceptance items for that milestone in `docs/acceptance/criteria.md`". Measured: **there is no `criteria.md` under `docs/`** (0 hits in a repo-wide search). The step cannot be executed, and the opening ritual of every milestone conversation follows it to read a file that does not exist |
| **True location (evidence)** | the acceptance items are actually in `docs/acceptance/m8-test-plan-matrix.md`, whose §1 functional sign-off table header is `req_id \| test_plan_ref \| milestone \| phase \| evidence \| status \| signed_by` (measured at `:42`), with the REQ-NF segment at `:63`, the REQ-S segment at `:83` and the REQ-G segment at `:92` of the same shape |
| **Goal** | change the target of step 4 to the acceptance items for that milestone in `docs/acceptance/m8-test-plan-matrix.md` |
| **Acceptance criterion** | ① a repo-wide search for `docs/acceptance/criteria.md` has 0 hits; ② the newly targeted file really exists and contains the 7-column acceptance items table described above |

⚠️ **Change discipline (`AGENT.md` is the operating manual for all agents; a change affects every subsequent session)**:

- **Minimal change**: only change the target of that one line; do not reorder and do not rewrite the remaining steps of that section, and **do not delete the step itself**.
- **Append an annotation**: **append** a short sentence to that line explaining the reason and date of the correction (2026-10-11).
- **Preserve history**: if the original reference wording is retained, it must be immediately followed by the correction note, and **readers must not still believe that `docs/acceptance/criteria.md` exists**.

### 2.2 Task 2 · Confirm the within-group numbering order of REQ-NF in `docs/requirements/prd.md` (**a checking task, no file change**)

> ✅ **Decided (2026-10-11)**: **grouping semantics take priority over numbering order**, see §2.6.
> **This task does not require changing the REQ-NF order of `prd.md`** — the originally envisaged "strictly ascending across the whole file" action has been withdrawn (doing that would downgrade requirements).

| Item | Content |
|---|---|
| **Location** | `docs/requirements/prd.md`, where each REQ-NF is organized as `#### REQ-NF-n：title`, belonging to two subsections |
| **Current state (evidence)** | measured: `### 3.1 核心架构约束（P0）` is at `:329` and contains NF-1 (`:333`) → NF-2 (`:341`) → NF-3 (`:349`) → NF-4 (`:357`) → NF-5 (`:365`) → **NF-9 (`:373`)**; `### 3.2 扩展与治理（P1）` is at `:381` and contains NF-6 (`:387`) → NF-7 (`:395`) → NF-8 (`:403`) → NF-10 (`:411`) → … → NF-16 (`:459`) |
| **Goal** | **ascending numbering within each group**. NF-1…NF-5 ascend inside the P0 segment with NF-9 located in that segment; NF-6…NF-16 ascend inside the P1 segment. **Numbering jumps across segments are not treated as errors** |
| **Acceptance criterion** | ① after splitting the output of `grep -n "^#### REQ-NF-"` by `### 3.1` / `### 3.2`, the numbering **inside each segment** is strictly ascending; ② the P0 segment contains NF-1…NF-5 and NF-9, the P1 segment contains NF-6/7/8/10…16; ③ **`prd.md` has not changed by a single byte from before execution** |
| **Forbidden actions** | **do not** move NF-9 across the `### 3.2` boundary; **do not** change the title or body of any entry by a single character; **do not** adjust subsection boundaries in order to satisfy "globally ascending" |

Measured conclusion: the two subsections **were already internally ascending**, so the actual output of this task is "check passed + state that conclusion in the execution record",
and **`prd.md` needs no change at all**. Only if the executor's re-check finds genuine out-of-order content inside a segment may the block positions be adjusted within that segment, with an explanation in the report.

### 2.3 Task 3 · `REQ-NF-16` is missing from the sign-off matrix (a real gap)

| Item | Content |
|---|---|
| **Location** | `docs/requirements/prd.md:459` (measured; the entity's line range is `:459-470`) defines `REQ-NF-16：版本生命周期与 EOL 策略`; whereas the §2 non-functional sign-off segment of `docs/acceptance/m8-test-plan-matrix.md` (measured `:61-79`) **has no `REQ-NF-16` row**, ending at `REQ-NF-15` (`:79`) |
| **Current state (evidence)** | searching that matrix for `REQ-NF-16`, "版本生命周期" and "EOL" only hits the `NA-D1` row at `:121`, which is a **Python 3.10 EOL risk registration** unrelated to REQ-NF-16 |
| **Corroborating evidence (the executor must re-check it before citing)** | ① `docs/architecture/adr/0027-version-lifecycle-and-eol.md` exists; measured `:3` is `Status: accepted` and `:6` is `回应 REQ: REQ-NF-16`; ② `docs/product/version-lifecycle.md` exists, and its status block states that REQ-NF-16 and ADR-0027 have landed while also stating "this document has not been reviewed and there is currently no review record"; ③ ⚠️ the **acceptance criteria** of that entry in `prd.md` reads "see `../acceptance/test-plan.md §2-REQ-NF-16`", but measured `docs/acceptance/test-plan.md` contains **only `REQ-NF-15 验收标准` (`:317`) and no `REQ-NF-16`** — that is, the acceptance criteria of this REQ **point at a section that does not exist**. This is a finding that must be recorded faithfully during this task |
| **Goal** | add a row for `REQ-NF-16` in §2 of the matrix, with column structure **exactly identical** to the existing rows of that segment (7 columns, `req_id \| test_plan_ref \| milestone \| phase \| evidence \| status \| signed_by`), and `signed_by` following the existing convention "maintainer pending signature" |
| **Acceptance criterion** | `REQ-NF-16` can be found in that file; every path cited in its `evidence` column **is confirmed by the executor to really exist**; the value in the `status` column is traceable (see below) |

⚠️ **The `status` column must not be invented.**

> ✅ **Decided (2026-10-11): fill `status` with `open`.** Rationale: ADR-0027 has been accepted (the `回应 REQ` pointer targets REQ-NF-16),
> which shows that **the technical decision has been made**; but the `test-plan.md §2-REQ-NF-16` section that `prd.md:470` points at **does not exist**,
> and `docs/product/version-lifecycle.md` states that **there is still no review record** — the two together **do not constitute a sign-off**.
> `signed_by` still reads "maintainer pending signature".

The `evidence` column **must contain the following two verifiable paths + line numbers** (correct them to the actual line numbers after the executor's re-check):

1. `docs/architecture/adr/0027-version-lifecycle-and-eol.md:3` (`Status: accepted`) and `:6` (`回应 REQ: REQ-NF-16`)
   — the technical decision has been made;
2. the section `docs/acceptance/test-plan.md §2-REQ-NF-16` pointed at by `docs/requirements/prd.md:459-470` **does not exist**
   (that file has only the one section `REQ-NF-15 验收标准`), and the status block of `docs/product/version-lifecycle.md` states **this document has not been reviewed and
   there is currently no review record** — the acceptance evidence chain is not closed.

And note the search scope (which files were searched, with which keywords).

| Verification result | What to fill `status` with | What to write in the `evidence` column |
|---|---|---|
| (the established value for this batch) | **`open`** | the two above: ADR-0027 exists + acceptance section missing / no review record, plus the search scope |
| if the executor's re-check finds **stronger** evidence than the above | report it up first, **do not** re-adjudicate unilaterally | —— |

**Do not fill in `pass` / `blocked` just to make the table look good.** Writings such as "a non-goal item passes by absence" (see the NF-6 / NF-8 rows of the same file)
**do not apply to REQ-NF-16**: it is a lifecycle strategy that needs positive delivery, not an absence-type clause that "passes by not existing".

### 2.4 Task 4 · The `test` target of `Makefile` currently inevitably fails

| Item | Content |
|---|---|
| **Location** | the `test` target of `Makefile` (measured `:41-44`), three lines in order: `pytest -m "unit or contract" -q`, `pytest -m integration -q`, `pytest -m e2e -q` |
| **Current state (evidence)** | measured on 2026-10-11, `uv run pytest -m e2e -q` has **exit code 5** (pytest's `NO_TESTS_COLLECTED`). Repo-wide, `pytest.mark.e2e` appears only in prose under `docs/**` and has **0 hits in test code**. That is, the e2e layer does not have a single case yet, so `make test` currently **inevitably fails on the third line**. The e2e landing plan is `docs/acceptance/2026-10-09-e2e-test-plan.md` (that file's status block states "a plan, **not implemented**, `pytest -m e2e` currently has **0** cases"), which belongs to **another batch** |
| **Collateral fact (the executor must be aware; this batch does not authorize handling it)** | the standalone `test-e2e` target in the same file (measured `:74-75`) likewise fails with exit code 5 |
| **Goal** | make `make test` no longer fail because of an "empty marker", while **not concealing the fact that "not a single e2e case exists"** |
| **Acceptance criterion (both must hold)** | ① `make test` runs to completion with exit code 0; ② it remains immediately obvious from documents and code that the e2e layer is currently empty |

Optional options (**not mandatory**; the executor chooses one and explains the rationale in the report):

1. Explicitly register the empty marker, and when that layer collects nothing give an **explicit warning** instead of silently passing;
2. Move the e2e layer out of the `test` target and note in the comment "the e2e cases have not landed yet; the landing plan is in `docs/acceptance/2026-10-09-e2e-test-plan.md`".

**Red line**: **do not** use something like `|| true` that swallows real failures too. If option 1 is chosen, the warning must let the reader see at a glance that "e2e = 0 cases".

### 2.5 Task 5 · New guard test `tests/test_requirements_registry.py`

Create that file, following the existing guard style of this repository — refer to `tests/test_version_consistency.py`,
`tests/test_workspace_layout.py`, `tests/test_evidence_discipline.py`: Google docstring module description,
`pytestmark = pytest.mark.unit`, and assertion messages that clearly state both "**which rule was violated**" and "**how to fix it**".

Cover at least the following five assertions:

| # | Assertion content | Purpose |
|---|---|---|
| 1 | the `REQ-<prefix>-<number>` numbering in `docs/requirements/prd.md` is **contiguous with no gaps**, with four prefixes each forming a segment (F / NF / S / G) | prevent numbering gaps |
| 2 | the entries of the same prefix appear in **ascending numeric order within their own subsection** | prevent within-group ordering from being disturbed — ✅ stance settled, see §2.6: **grouping semantics take priority over numbering order**, and a numbering jump across subsections **is not a failure** |
| 3 | every REQ-id appearing in `docs/acceptance/m8-test-plan-matrix.md` **exists in** `prd.md` | prevent the matrix from gaining requirements out of thin air |
| 4 | every REQ-id in `prd.md` **can find a corresponding row in the matrix** | prevent a recurrence of the gap in 2.3 |
| 5 | every `-m` marker referenced in the `test` target of `Makefile` is **defined in** the `markers` of `[tool.pytest.ini_options]` in `pyproject.toml` | prevent drift between definitions and usages |

**Implementation notes (current state as measured, for reference)**:

- `prd.md` currently has 40 REQs: F-1…F-16, NF-1…NF-16, S-1…S-4, G-1…G-4. Assertion 1 therefore passes as-is.
- Assertion 3 must **match only the `REQ-<prefix>-<digits>` form**. The matrix also contains many row ids that are not REQ-ids
  (measured examples: `KERNEL-§5`, `5.4-F-13`, `D12/O5-HA`, `NA-主叫/正则`, `ADR-0008-演练`),
  and those are not REQ-ids, so assertion 3 must not block them. REQ-ids appearing inside the text of the `evidence` column (such as "same source as REQ-F-13") should also count towards the coverage judgement.
- The marker set of assertion 5: the `markers` of `pyproject.toml` (measured `:48-54`) are
  `unit` / `contract` / `integration` / `e2e` / `performance`; the `test` target of `Makefile` uses
  `unit`, `contract`, `integration`, `e2e`. Note when parsing that `"-m \"unit or contract\""` contains `or` and must be split and compared item by item.
- **Assertion 4 should pass once `REQ-NF-16` is added. If the executor fails to add it for lack of evidence, that assertion will fail —
  in that case do not relax the assertion; keep the failure faithfully and explain it in the report.**

**Self-check requirement**: `uv run pytest tests/ -q` should be all green; also run `uv run ruff check tests/` and
`uv run ruff format --check tests/`.

⚠️ **Do not relax assertions or modify existing guards in order to make tests pass** (`test_version_consistency.py`,
`test_workspace_layout.py`, `test_evidence_discipline.py` are not to be touched by a single byte).

### 2.6 ✅ Decided item: grouping semantics take priority over numbering order (adjudicated 2026-10-11)

> **This section is a decided item, not a to-do.** The previous round listed this point as "needs a maintainer call"; it has now been adjudicated.
> The **discovery process and misjudgement traces below are preserved verbatim per the history-preservation convention** — they record how this review corrected itself and must not be deleted.

**Adjudication content**: the REQ-NF grouping semantics of §3 of `prd.md` (`### 3.1 核心架构约束（P0）` / `### 3.2 扩展与治理（P1）`)
**takes priority over** numbering order. The acceptance stance is **ascending numbering within each group**, and a numbering jump across subsections **does not constitute a defect**.
Therefore the REQ-NF order of `prd.md` is **not changed**, §2.2 is correspondingly downgraded to a checking task, and assertion 2 of §2.5 adopts the within-group stance.

**Discovery process (audit trace, preserved)**:

1. Measured in the 2026-10-11 review: `### 3.1 核心架构约束（P0）` is at `:329` and contains NF-1…NF-5 and **NF-9** (`:373`);
   `### 3.2 扩展与治理（P1）` is at `:381` and contains NF-6, NF-7, NF-8, NF-10…NF-16 (ending at `:459`).
   On the surface, "NF-9 comes before NF-6" looks like out-of-order numbering.
2. The review further identified that: REQ-NF is not flat but **split into two segments by P0 / P1**. Therefore this phenomenon
   **is very likely the result of semantic grouping rather than a layout mistake**.
3. Risk quantification: to force "strictly ascending across the whole file", the only way is to move `REQ-NF-9` across the `### 3.2` boundary into the P1 segment,
   which **equals downgrading a core architecture requirement to an extension requirement** — that is a requirement priority change.
4. **Correction**: the premise of the previous round's instruction, "arrange the REQ-NF entries in ascending numeric order (NF-1 … NF-16)", was **incorrect**, and that action is withdrawn on that basis.
   **Lesson**: before reading "non-contiguous numbering" directly as "a layout mistake", first check whether there is semantic grouping. This item has been merged into the meta-rule of §2.7 as a general defence for such cases.

**What the executor must know**: this section **leaves nothing for you to do**. Do not move NF-9, do not change subsection boundaries, do not reopen this topic.

### 2.7 Task 6 · Append a meta-rule to the pending-adjudication register

| Item | Content |
|---|---|
| **Location** | `docs/handoff/2026-10-11-open-adjudication-register.md` |
| **Action** | **append only, do not rewrite existing content.** Append a meta-rule after that document's list, noting that it emerged from the 2026-10-11 review |
| **Text of the rule to append** | "This document's list has no minimum length. Once an issue is resolved it is removed from the list, and the list getting shorter is a normal outcome; entries must not be added in order to maintain the form, to pad the item count, or to make the register look complete. If an entry was previously listed as pending adjudication by mistake, it should be withdrawn rather than kept." |
| **Background note to append** | This rule emerged from the 2026-10-11 review; the background is that on that day "already-adjudicated items were re-listed as pending adjudication" and "items already resolved by actual work were still listed as pending adjudication" kept recurring |
| **Acceptance criterion** | "This document's list has no minimum length" can be found in that document; the existing content is **unchanged verbatim**. ⚠️ That document is currently **not tracked by git**, so `git diff` produces no output for it; **do not** use that as the criterion: before changing it, record the file's **line count and byte count**, and compare afterwards — **lines may only increase and existing lines must be unchanged verbatim**; when line-by-line evidence is needed, first `cp` a copy, then after the change use `diff` to compare the copy with the current file, and **only added lines may appear** in the differences |

⚠️ **Discipline**: append only. **Do not** take the opportunity to reorder that document's existing entries and **do not** delete any existing entry
(including those that look "actually already resolved" — whether to remove them is the maintainer's decision).

---

## 3. Global Constraints

| # | Constraint |
|---|---|
| 1 | **history-preservation convention**: every change is an append or a status-field update, and **existing original text is never silently deleted or rewritten**; superseded wording is retained with a correction note appended |
| 2 | **must not be modified**: `VERSION`, `deploy/helm/Chart.yaml`, scripts under `tools/`, existing rows of the §0 decision record table of `docs/plan.md`, the **existing content** of `docs/handoff/2026-10-11-open-adjudication-register.md` (task 6 only allows appending), **any product code** |
| 3 | **must not be executed**: any target of `make` (the `Makefile` itself **may be read and changed**, but **must not be run** — the exception is §4 item 4), `git commit` / `push` / `tag` / branch creation / remote change, `docker` |
| 4 | **must not add REQ / ADR**; **must not sign off** any REQ or milestone; review records are always marked "landed, awaiting maintainer review" |
| 5 | **all cited line numbers must be read and verified before being written**, and must not be copied from this document (documents are appended to and line numbers drift) |
| 6 | dates are uniformly written as **2026-10-11**; all in Chinese |
| 7 | **decided items must not be reopened** (see §2.6). When a phenomenon contrary to a decided item appears, first assume you misread the semantic grouping, then report it |

---

## 4. Self-Check List

After execution, confirm item by item and state the actual output in the execution record:

| # | Check item | Passing standard |
|---|---|---|
| 1 | `uv run pytest tests/ -q` | all green (or the failures kept faithfully, as explained in §2.6) |
| 2 | `uv run ruff check tests/` | no output / exit 0 |
| 3 | `uv run ruff format --check tests/` | "N files already formatted" |
| 4 | **measured exit code** of `make test` | **exit 0**. ⚠️ This batch **allows and requires** running this item, because it is the acceptance criterion of task 4 (the exception to §3 item 3). If the measurement takes too long or triggers network/container dependencies, **do not skip it**; faithfully describe the phenomenon and the elapsed time |
| 5 | the **line numbers and paths of every citation were verified by me personally** | compared item by item against the actual files, without relying on the numbers given here |
| 6 | repo-wide search for `docs/acceptance/criteria.md` | 0 hits |
| 7 | `grep -n "^#### REQ-NF-" docs/requirements/prd.md` | consistent with the §2.6 decision |
| 8 | the paths cited in the `evidence` of `REQ-NF-16` in the matrix | each one really exists |

---

## 5. Stop Line

When encountering any of the following, **stop and report to the maintainer**; do not work around it:

- the need to push / tag / create a branch / change the remote;
- the need to modify `VERSION` or `deploy/helm/Chart.yaml`;
- the need to write e2e cases (belongs to another batch, see `docs/acceptance/2026-10-09-e2e-test-plan.md`);
- the need to **adjudicate the acceptance status of any REQ** (`pass` / `blocked` / `open` / `n-a` may only be filled in from evidence and must keep "maintainer pending signature";
  the final signing authority rests with the maintainer);
- the need to move `REQ-NF-9` across the P0/P1 subsection boundary (see §2.6: **adjudicated — grouping semantics take priority, NF-9 must not be moved**);
- the need to add a REQ / ADR;
- the need to relax assertions or modify existing guards in order to make new tests green.

---

## 6. Out of Scope for This Batch

This batch **does not** do the following, even though they look adjacent:

| Not done | Ownership / reason |
|---|---|
| **e2e case landing** | another batch (A4), plan in `docs/acceptance/2026-10-09-e2e-test-plan.md` |
| **ADR system cleanup** | does not belong to this batch; the current state of `docs/architecture/adr/` is untouched |
| **Deduplication of design documents** | `docs/architecture/README.md` has already established a priority decision line; this batch **does not repeat it** |
| **Any adjudication of a REQ's acceptance status** | the final signing authority rests with the maintainer; this batch only adds the "gap row", it does not adjudicate status |
| Fixing the reference in `prd.md` to the non-existent `test-plan.md §2-REQ-NF-16` (corroborating evidence ③ of 2.3) | discovering and recording it faithfully is enough; whether to add the test-plan section is the maintainer's decision |
| Touching the original text of other historical runbooks under `docs/acceptance/` | `docs/README.md` states that directory is not deleted, moved or rewritten |

---

## 7. Reporting Requirements After Execution

After the executor has written the execution record, it must report to the maintainer (containing at least):

1. the actual changes of each of the five tasks (file + line number + before/after comparison);
2. the **actual output** of the 8 items of the §4 self-check list (not "should pass");
3. the option chosen for task 4 and its **rationale**;
4. what was filled into the `status` of `REQ-NF-16` in task 3, on what basis, and what the search scope was;
5. whether §2.6 has been adjudicated; if not, whether assertion 2 currently passes or fails;
6. anything that needs the maintainer's call and that you **did not** call;
7. whether this instruction document itself has errors or omissions that you found by measurement.
