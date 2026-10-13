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

# M1 exit review record (Milestone Exit Review)

> Review target: M1 — screening and behavioural baseline. Scope covers `docs/plan.md` §4.1 gate adjudication, `docs/acceptance/report.md`, `docs/migration/triage.md`, `testbed/contracts/sip-baseline/`
> Review date: 2026-09-28
> Reviewer: AI agent (cross-checking gate and DoD evidence)
> Review conclusion: **conditional pass** — the condition is retroactive creation of HLD/LLD, which is listed as an M2 prerequisite; the M1 conclusion is not rolled back

## Review method

| Dimension | Method |
|---|---|
| Gate achievement | Item-by-item check of the original text of the M1 gate in `plan.md` §4, with a re-check of repository artifacts |
| DoD evidence | Evidence gathered item by item for the ten clauses of `AGENT.md` §14; code-related clauses require real execution evidence |
| Baseline completeness | Counting the `.txt` message files in each directory under `testbed/contracts/sip-baseline/` one by one |
| Documentation chain | Whether the six links requirement → ADR → HLD/LLD → contract → acceptance → review record are connected end to end |

## Findings and adjudication

| # | Finding | Evidence | Adjudication | Status |
|---|---|---|---|---|
| F1 | The S5 / S6 / S7a / S8 baseline directories contain only a README and zero message files | Measured from the directories; corresponds to REQ-F-2 / F-3 / F-4 / F-5 (P0) | Accepted as a **derived baseline**: these four acceptance items in `test-plan.md` were already written as "extract X after completing the basic call of REQ-F-1", so they can be derived from `S1-basic-call`; re-capturing only increases the maintenance surface | Adjudicated (written into `plan.md` §4.1) |
| F2 | The S10 / S11 baselines were not captured | Measured from the directories; POC ReturnUas only returns 200 OK, with no busy branch or race construction | Accepted as an **M2 probe backfill**, consistent with the known-gap table in `prd.md` §2.4 | Adjudicated |
| F3 | `plan.md` status lags behind (the §0 says M1 in progress, the §4 says M1 not started), yet the actual output is already in the repository | Commits `b27bb3d` / `92c244c` / `e30c426` / `2341166` / `c9d4899` | Accepted: updated to M1 completed, current step M2, and a new §4.1 recording the gate adjudication | Modified |
| F4 | No M1 acceptance report | `docs/acceptance/` originally had only a README and the test-plan | Accepted: newly created `docs/acceptance/report.md`, containing real-execution gate evidence and item-by-item DoD | Modified |
| F5 | No M1 exit review record | Existing records in `docs/reviews/` all concern an ADR or the PRD | Accepted: this file | Modified |
| F6 | No M1 entry in CHANGELOG; `VERSION` still 0.1.0 | `CHANGELOG.md`, `VERSION` | Accepted: add an M1 entry to CHANGELOG; `VERSION` **stays at 0.1.0** — M1 delivers no product code and the delivered content is unchanged, so per ADR-0018 there is no bump | Modified |
| F7 | HLD / LLD have not yet been created | There is no `hld.md` or `lld.md` under `docs/architecture/` | Accepted as a **condition**: the M1 conclusion is not rolled back, but it is made the first action of M2 (AGENT.md §3.1 requires HLD/LLD as a prerequisite for entering Code) | Pending M2 |
| F8 | Counting error: the number of S4 messages was recorded as 9, but is actually 12 | `S4-caller-cancel/` measures 12 txt files, while the README states "message sequence (12 entries)" | Accepted: `plan.md` §4.1 and `report.md` have been corrected | Modified |
| F9 | During the PRD review the RFC 3261 basis was at the "table of contents confirmed" level only | `docs/reviews/prd-v0.1-review.md` | Accepted: full-text slices were fetched with `curl` for supplementary verification, and §9 / §9.1 / §9.2 / §15 / §15.1.2 / §16.4 were all raised to L1 verbatim checking, clearing all remaining items | Modified |

## Adjudication summary

| Category | Count | Disposition |
|---|---|---|
| Adjudicated and landed | 8 (F1-F6, F8, F9) | Modifications have been made in `plan.md` / `report.md` / `CHANGELOG.md` / `prd-v0.1-review.md` |
| Conditional items (handed over to M2) | 1 (F7 HLD/LLD) | Made the first action of M2; does not block the M1 conclusion |

## Confirmation and sign-off

| Item | Value |
|---|---|
| Review conclusion | conditional pass (condition: retroactively create HLD/LLD in M2) |
| M1 gate | achieved |
| Reviewer | AI agent, 2026-09-28 |
| Maintainer sign-off | to be filled in |
