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

# M0 skeleton review — Gap Register

> Reviewer: AI agent (grilling session)
> Date: 2026-09-27
> Scope: the M0 skeleton on the current `master`, checked against `docs/plan.md` §2–§3 and the §0 decision ledger of `docs/architecture/system-architecture.md`
> Status: **M0 signed off** (the maintainer authorised the AI agent to sign on their behalf, 2026-09-28). O-F/O-H/G1/G4 are closed; G3/G5/G6/G7/G8/G9/G10/G11/G12 are deferred to later milestones (they do not block the M0 sign-off)

## Review method

1. Run `make gate` to confirm the current gate state.
2. Check against the M0 exit criteria of `plan.md` item by item.
3. Check against the 18 confirmed decisions in §0 of the architecture document and verify how the ADRs were landed.
4. Check the responsibility boundaries between `AGENT.md` and `plan.md` / the architecture documents / `migration/triage.md`.

---

## 1. Gate status

| Check | Command | Result |
|---|---|---|
| ruff format --check | `uv run ruff format --check .` | Pass (36 files already formatted) |
| ruff check | `uv run ruff check .` | Pass |
| mypy | `uv run mypy` | Pass (7 source files) |
| unit / contract | `uv run pytest -m "unit or contract" -q` | Pass (44 passed) |
| integration | `uv run pytest -m integration -q` | **Fail**: 44 deselected, pytest exit 5 |
| e2e / performance | not reached | — |

**Conclusion**: `make gate` is currently not green. The reason for the failure is that the `test` target of the `Makefile` calls the integration layer directly at the skeleton stage, while there are no integration tests at all.

---

## 2. Gap list

### G1 — `make gate` fails at the skeleton stage

- **Location**: `Makefile` lines 24–28
- **Symptom**: `make test` calls `uv run pytest -m integration -q`, and pytest returns exit 5 when there are no tests
- **Impact**: violates the `AGENT.md` §8 rule that nothing may be committed while the local gate is not green; M0 cannot be signed off
- **Suggested fix**:
  - Option A: change the `gate` target to `lint type test-unit` so that locally only layer ① runs (recommended)
  - Option B: use a shell condition in the `test` target to skip markers that currently have no tests, and remove it at M2/M3/M6

### G3 — 18 ADRs have only a registry, no body files

- **Location**: `docs/architecture/adr/README.md`
- **Symptom**: all 18 decision statuses are `skeleton`
- **Analysis**: by the `AGENT.md` rule, an ADR is written together with the change it authorises. M0 does not authorise concrete behaviour changes, only structure, so skeletons are acceptable for M0 itself; however, the first batch of ADRs that must be written before M1 needs to be made explicit
- **Suggestion**: immediately after the M0 sign-off, write ADR-0001, 0002, 0003 and 0018 as the landed structural decisions; the rest follow with the milestones

### G4 — `platform/pyproject.toml` comment is inconsistent with the dual-stack decision

- **Location**: `platform/pyproject.toml` lines 18–20
- **Symptom**: the comment says "One SIP stack version in one interpreter"
- **Analysis**: architecture decision 8 is dual-stack in parallel (sippy in production + go-b2bua as a pilot), not a single stack
- **Suggested fix**: update the comment to "sippy is currently the only Python production dependency; go-b2bua is the M7 experimental stack and is not brought in through the uv workspace"

### G5 — `AGENT.md` duplicates a lot of `plan.md` / architecture-document content

- **Location**: `AGENT.md` in full
- **Symptom**: details such as the directory structure, milestones, the ADR registry and open items are duplicated with `plan.md` / `adr/README.md` / `system-architecture.md`
- **Analysis**: maintainer Q3 explicitly stated that AGENT.md should focus on "consistency rules" and must not duplicate the plan
- **Suggested fix**: rewrite `AGENT.md`, pointing duplicated content back to the dedicated documents via links, and retaining: positioning, non-goals, layering, coding conventions, test-strategy principles, ADR rules, version-dependency principles, the gate, AI assistance, Git rules, POC adoption rules, security, DoD, open-item references

### G6 — `AGENT.md` lacks the subagent / collaboration rules already present in the POC

- **Location**: `AGENT.md` §9 (AI assistance)
- **Symptom**: only 3 high-level rules exist; the delegation policy, team mode rules, message timing, branch-conflict prevention etc. from POC `AGENT.md` §14 are missing
- **Impact**: the current project is more complex than the POC (monorepo, multiple milestones, cross-language), yet it lacks agent collaboration details
- **Suggested fix**: add an "AI Agent collaboration rules" section to `AGENT.md` that specifies:
  - reading/writing subagents must use team mode (`name` + `acceptEdits`)
  - exploratory tasks use a synchronous search subagent
  - only one writing subagent may operate on a worktree at a time
  - how to handle asynchronous / possibly-lost messages
  - the milestone handover protocol
  - agents are forbidden from creating branches, pushing or tagging on their own

### G7 — `services/config-service` and `services/console` declare no dependencies

- **Location**: `services/config-service/pyproject.toml`, `services/console/pyproject.toml`
- **Symptom**: `dependencies = []`
- **Analysis**: empty dependencies are acceptable at the skeleton stage, but the READMEs should state the future dependency direction (PG, platform contracts, OTel, etc.)
- **Suggested fix**: list the "workspace members / external packages that will be depended on in future" in each `README.md`

### G8 — All READMEs are placeholders

- **Location**: `apps/*/README.md`, `services/*/README.md`, `testbed/*/README.md`, `deploy/*/README.md`, `platform/README.md`
- **Symptom**: there are only titles, no responsibility description
- **Analysis**: `plan.md` §2.1 requires "every directory carries a README explaining what belongs there"
- **Suggested fix**: add 3–5 lines of responsibility description plus links to `plan.md` / the architecture documents to each README; do not write future implementation details

### G9 — Missing `.env.example` / configuration sample

- **Location**: repository root directory
- **Symptom**: there is no `.env.example`
- **Analysis**: the POC has an `.env.example`; M0 does not need a full configuration, but an environment-variable list template helps clarify process boundaries
- **Suggested fix**: add a minimal `.env.example` listing the env vars each process will read (addresses, ports, rule file paths, peer allowlists, etc.), with placeholder values

### G10 — `deploy/helm/` and `deploy/compose/` contain only a README

- **Location**: `deploy/helm/README.md`, `deploy/compose/README.md`
- **Symptom**: there is no `Chart.yaml`, `values.yaml` or `compose.yml`
- **Analysis**: an empty chart is acceptable for M0, but there should be a minimal skeleton describing the target shape
- **Suggested fix**:
  - `deploy/compose/`: add a minimal `compose.yml` (to eventually run platform, apps, services, redis, postgres)
  - `deploy/helm/`: add a minimal `Chart.yaml` + an empty `values.yaml` + a `templates/` directory

### G11 — The current commit has been pushed, but the maintainer states it is "not a roadmap"

- **Location**: `docs/plan.md` §0, §3
- **Symptom**: the baseline state of the current `master` is not recorded
- **Analysis**: it needs to be made clear that the current commit is the pre-roadmap skeleton, and that the first formal commit after the M0 sign-off is the baseline
- **Suggested fix**: add a note in `CHANGELOG.md` or `plan.md` §0 distinguishing the "pushed pre-roadmap skeleton" from the "formal baseline after the M0 sign-off"

### G12 — The POC freeze point is not recorded

- **Location**: `docs/migration/triage.md` §1
- **Symptom**: the commit hash of `3rtparty_AS_POC` is not recorded
- **Analysis**: the M1 behavioural baseline capture needs a reproducible POC version
- **Suggested fix**: record the current POC HEAD hash at the top of `migration/triage.md`

---

## 3. Suggested M0 correction order

Ordered by dependency: fix the blocking items first, then fill in the documentation:

1. **G1**: fix the `Makefile` so that `make gate` is green
2. **G5 + G6**: rewrite `AGENT.md`, focusing on consistency rules and adding subagent collaboration details
3. **G3**: write the first batch of ADRs (0001, 0002, 0003, 0018) after the M0 sign-off
4. **G4**: update the dual-stack comment in `platform/pyproject.toml`
5. **G8**: populate the READMEs of each directory
6. **G9 + G10**: add `.env.example`, a minimal compose file and a minimal helm skeleton
7. **G7**: describe future dependencies in the service READMEs
8. **G11 + G12**: record the baseline and the POC freeze point

---

## 4. Major decision deviation (exposed during the 2026-09-27 session)

### SIP stack selection: from "dual-stack in parallel" to "replacing sippy"

The maintainer made explicit in grilling Q5: **the starting point of the new project is to swap out sippy**. The specific replacement target is still under evaluation:

- `go-b2bua` (the official Go port by the sippy author)
- a C/C++-based SIP stack (such as reSIProcate, libre/baresip, sofia-sip, etc.)

Before the final selection is complete, **we must not rush ahead**.

#### Impact on the current skeleton

| Original assumption | Current state | Impact |
|---|---|---|
| Architecture decision 8: dual-stack in parallel, sippy stays in production + go-b2bua pilot | needs to be overturned or rewritten | decision 8 in §0 of `docs/architecture/system-architecture.md`, the §10 dual-stack migration path and ADR-0011 all need updating |
| `platform/pyproject.toml` pins `sippy==2.4.2` | conflicts with "swapping out sippy" | needs to become a pluggable seam, or at minimum state explicitly that sippy is only a current placeholder |
| M2 plan: build the kernel on platform/ based on sippy | blocked | M2 cannot write sippy-bound code before the SIP stack selection is complete |
| M7 Go migration | may be pulled forward or cancelled | if go-b2bua is finally selected, M7 is not a "migration" but the "primary implementation"; if a C/C++ stack is selected, go-b2bua is only one of the evaluation candidates |
| `testbed/simulators` based on sippy | needs re-evaluation | must the simulated network element share the same stack as the AS? the POC does it this way, but the product may not |

#### Questions requiring an immediate answer

1. Does "swapping out sippy" mean **absolutely excluding sippy**, or "sippy is not the production stack but may still serve as a reference during the evaluation period"?
2. What are the **hard constraints** of the selection (licence, capacity targets, the team's Go/C++ skills, behavioural compatibility, vendoring feasibility)?
3. Are **parallel spikes** of multiple candidate stacks allowed, or should the evaluation framework be defined first and each candidate tried in turn?
4. Does this decision block the M0 sign-off? I.e. can M0 be signed off in the "stack not yet selected" state, with the selection becoming a standalone research task after M0?
5. Is `sippy==2.4.2` in the current skeleton to be removed immediately, or retained as a "current placeholder dependency to be replaced after the ADR update"?

---

## 5. Open questions requiring maintainer adjudication

| # | Question | Current suggestion |
|---|---|---|
| O-A | Should `make gate` run only layer ① during M0? | Yes, until M2 introduces the first integration test |
| O-B | Should ADR-0001/0002/0003/0018 be the first batch after the M0 sign-off? | Yes; but if the SIP stack selection overturns the original ADR-0011, then ADR-0011/0019 take priority |
| O-C | Does the rewritten `AGENT.md` need a separate review? | Yes, confirmed by maintainer Q7 |
| O-D | Are `.env.example` and the minimal compose/helm part of M0? | Yes, as placeholders for the target shape; but if the stack is undecided, do not bind a specific SIP image in helm/compose |
| O-E | Is the history of the pre-roadmap commit on the current `master` to be preserved? | For the maintainer to decide; recommended to preserve it, but annotate the baseline in the documents |
| O-F | Does the SIP stack selection block the M0 sign-off? | **Adjudicated: it blocks the M0 sign-off.** The SIP stack selection must be completed and the corresponding ADR written before the M0 sign-off |
| O-G | Is the current `sippy==2.4.2` to be kept as a placeholder or removed immediately? | **Adjudicated: remove immediately from `platform/pyproject.toml`**. sippy is downgraded to a reference for the POC behavioural baseline and does not enter the product production dependencies |
| O-H | Should a new ADR-0019 be added to replace the original ADR-0011? | Pending adjudication; recommended to use a new ADR when overturning the original decision rather than overwriting the old number |

---

## Adjudication

> Maintainer adjudication date: 2026-09-28
> Adjudicator: maintainer

| ID | Source | Question summary | Adjudication | Change plan | Status | Verification method | Notes |
|---|---|---|---|---|---|---|---|
| G1 | §2 G1 | `make gate` fails at the skeleton stage (no tests in the integration layer causes exit 5) | Accept | Change the `gate` target to `lint type test-unit`, M0 runs only layer ① | Modified | `make gate` fully green | G1 and O-A are two sides of the same problem, as gap and open question respectively |
| G3 | §2 G3 | 18 ADRs have only a registry and no bodies | Accept | Write the first batch of ADRs (0001/0002/0003/0018) after the M0 sign-off | Pending modification | ADR files exist and pass review | Corresponds to O-B |
| G4 | §2 G4 | `platform/pyproject.toml` comment is inconsistent with the dual-stack decision | Partially accept | Change the comment to reflect the current candidate status of ADR-0019 (sippy out of the production stack, selection in progress) | Closed | the comment at platform/pyproject.toml L18-24 has been updated and explicitly records that ADR-0019 records the selection result | already updated in an earlier session, resolved automatically |
| G5 | §2 G5 | `AGENT.md` heavily duplicates `plan.md` / architecture documents | Accept | Rewrite `AGENT.md`, focus on consistency rules, use links for duplicated content | Closed | AGENT.md points to plan.md / the architecture documents via links with no duplicated content (see §1 L14, §4 L112, §15 L273) | G5 and G6 fall within the scope of the AGENT.md rewrite |
| G6 | §2 G6 | `AGENT.md` lacks subagent / collaboration rules | Accept | Add an "AI Agent collaboration rules" section to `AGENT.md` | Closed | AGENT.md §10 now contains the complete subagent collaboration rules (§10.1-10.4, see L168-224) | G6 and G5 fall within the scope of the AGENT.md rewrite |
| G7 | §2 G7 | services declare no dependencies | Accept | List the future dependency direction in each service README | Closed | `services/config-service/README.md` and `services/console/README.md` have added a future-dependency section (including the dependency directions of platform/PG/Redis/OTel etc.) | |
| G8 | §2 G8 | All READMEs are placeholders | Accept | Add 3–5 lines of responsibility description + links to each README | Closed | a repository-wide README scan confirms all contain substantive content (apps/translation, apps/anti-fraud, platform, services/*, testbed/*, deploy/* all have 10+ lines of content + links to the ADR/architecture documents) | |
| G9 | §2 G9 | Missing `.env.example` | Accept | Add a minimal `.env.example` listing the env vars of each process | Closed | a repository-root `.env.example` has been created, listing environment-variable templates for the SIP signalling plane / Redis Sentinel / PostgreSQL / OTel / common process variables in 5 sections | |
| G10 | §2 G10 | deploy/helm and deploy/compose contain only a README | Accept | Add a minimal compose.yml and Chart.yaml + values.yaml | Closed | the skeleton files `deploy/helm/Chart.yaml` + `values.yaml` + `deploy/compose/compose.yml` have been created | Corresponds to O-D |
| G11 | §2 G11 | The current commit has been pushed but does not count as roadmap | Accept | Add a baseline note in plan.md §0 or the CHANGELOG | Closed | plan.md §0 has a new baseline-note subsection | Corresponds to O-E |
| G12 | §2 G12 | The POC freeze point is not recorded | Accept | Record the POC HEAD hash at the top of `migration/triage.md` | Closed | `docs/migration/triage.md` L14 records the POC freeze point `4ddf3df3` | |
| O-A | §5 O-A | Should `make gate` run only layer ① during M0 | Accept | During M0 `gate` depends on `test-unit`; it is adjusted once M2 introduces integration tests | Modified | `make gate` fully green | Same problem as G1 |
| O-B | §5 O-B | Should ADR-0001/0002/0003/0018 be the first batch after the M0 sign-off | Accept | Prioritise these four ADRs after the M0 sign-off; if ADR-0019 is Accepted first it takes priority | Pending modification | ADR files exist and pass review | Corresponds to G3 |
| O-C | §5 O-C | Does the rewritten `AGENT.md` need a separate review | Accept | Separate maintainer review after the rewrite | Pending modification | there is an independent review record | Corresponds to G5/G6 |
| O-D | §5 O-D | Are `.env.example` and the minimal compose/helm part of M0 | Accept | Include in M0 as placeholders for the target shape; do not bind a specific SIP image | Pending modification | files exist | Corresponds to G9/G10 |
| O-E | §5 O-E | Is the history of the pre-roadmap commit on the current master to be preserved | Pending adjudication | For the maintainer to decide; recommended to preserve it and annotate the baseline | Pending modification | maintainer sign-off confirmation | Corresponds to G11 |
| **O-F** | **§5 O-F** | **Does the SIP stack selection block the M0 sign-off** | **Accept (original adjudication maintained)** | **M0 can only be signed off after ADR-0019 is Accepted** | **Closed** | **The status of ADR-0019 has moved to Accepted, plan.md O2 unblocked** | **The maintainer completed the selection on 2026-09-28 (reSIProcate)** |
| O-G | §5 O-G | Is the current `sippy==2.4.2` a retained placeholder or to be removed immediately | Accept | Remove immediately from `platform/pyproject.toml`; sippy is downgraded to a testbed baseline reference | Pending modification | platform/pyproject.toml contains no sippy production dependency | The original adjudication has taken effect, execution pending |
| O-H | §5 O-H | Should a new ADR-0019 be added to replace the original ADR-0011 | Accept | Add ADR-0019, do not overwrite the original ADR-0011 number | Modified | the ADR-0019 draft already exists | ADR-0019 moved to Accepted on 2026-09-28, selecting reSIProcate |

---

## 6. M0 sign-off record

- **Sign-off date**: 2026-09-28
- **Signatory**: maintainer authorised the AI agent to sign on their behalf
- **Authorisation basis**: verbal authorisation from the maintainer (current conversation)
- **Sign-off conditions**:
  - ✅ `make gate` fully green (44 passed)
  - ✅ ADR-0019 is Accepted (reSIProcate selected, O2 unblocked)
  - ✅ architecture document decision 8 has been synchronised
  - ✅ G1 (make gate) has been fixed
  - ✅ G4 (platform/pyproject.toml comment) resolved automatically
  - ✅ O-F (ADR-0019 blocking) is closed
  - ✅ O-H (ADR-0019 replacing ADR-0011) is closed
- **Known follow-up items** (not blocking the M0 sign-off): G3 (ADR skeleton), G5+G6 (AGENT.md rewrite), G7–G12 (README / configuration / deployment skeleton) — folded into M1+ handling

---

## 7. M0 gap backfill record for the M1 phase

- **Backfill date**: 2026-09-28
- **Backfill scope**: G5/G6/G12 (completion confirmed) + G7–G11 (actually backfilled) + G3 (ADR-0001/0002/0003/0018 from skeleton → draft)
- **Not handled**: none. All M0 gaps are closed or moved to draft status pending later review
- **Gate**: `make gate` fully green (49 files formatted, ruff/mypy clean, 44 tests passed)
