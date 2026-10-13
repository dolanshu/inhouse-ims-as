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

# ADR-0006 Review Record

> Review target: `docs/architecture/adr/0006-config-governance.md` (newly created on 2026-09-28, Status: draft)
> Review date: 2026-09-28
> Reviewer: AI agent (cross-checked against the AGENT.md red lines and non-goals, PRD REQs, and the ADRs already on record)
> Review conclusion: **Pass** — moved to accepted; 3 gaps in total, none of them blocking

## Review Method

| Dimension | Method |
|---|---|
| Consistency with red lines | Clause-by-clause comparison against the original text of `AGENT.md` §2 (non-goal: configuration does not go through GitOps), §4 (layering), §13 (security) |
| Consistency with requirements | Checked PRD v0.2 REQ-NF-10 / REQ-F-12 / REQ-F-14 / REQ-G-1 / REQ-S-4 |
| Consistency with existing ADRs | Whether it conflicts with ADR-0007 (governance state in PG), ADR-0002 (state externalization), ADR-0020 (feature flags reuse the pipeline) |
| Structural completeness | Whether it has Context / Decision / Consequences / Alternatives / Evidence / Related |

## Findings and Adjudication

| # | Finding | Adjudication |
|---|---|---|
| 1 | The Context is based directly on the original text of the AGENT.md §2 non-goal ("operators must not be required to learn Git just to change a number range"), and quotes PRD REQ-NF-10 verbatim rather than paraphrasing from memory | Accept, as the L1 basis; the argument that the two constraints (no GitOps / must be versionable and rollbackable) jointly squeeze out the design space holds |
| 2 | The decision covers the four elements "immutable version rows + change-ticket state machine + canary distribution + automatic rollback", corresponding item by item to REQ-NF-10's "versionable, traceable, canary-able, rollbackable"; storing the approver and approval time corresponds to REQ-F-14 | Accept; none of the four requirements is missing, and "write a new version only after approval passes" turns approval from a process step into a precondition for writing |
| 3 | The version reporting contract is already in place in the kernel: `ConfigBundle` and `AppliedVersionReport` are already defined in `platform/src/as_platform/api/contract.py`; it is not an interface still to be added | Accept; "the configuration plane considers it effective" and "the runtime actually has it effective" can be aligned, avoiding the need to infer the effective state from the write timestamp |
| 4 | No conflict with ADR-0007 (governance state in PG) or ADR-0020 (feature flags reuse the pipeline), and they support each other; this ADR explicitly does not re-argue the storage choice and defines only the shape of governance state and the change flow | Accept; the boundary is clear, there is no duplicate adjudication, and no circular reference |
| 5 | Three known gaps: ① PostgreSQL becomes the single point of failure for governance state (the degraded mode is described, and M5 high availability covers it); ② canary granularity and the configuration schema are undecided (D7); ③ the audit data retention period is undefined | Accept as **known gaps**, none blocking; ① and ② are written into the negative part of Consequences with the resolution points marked (M5 / before control-plane design) |
| 6 | Entries in Related that point at ADRs not yet implemented have been downgraded to plain text; only existing files are linked (0007 / 0020 / system-architecture.md) | Accept; no dead links |

## Adjudication Summary

| Category | Count | Disposition |
|---|---|---|
| Accepted with no changes needed | 4 (findings 1, 2, 3, 4) | — |
| Accepted as known gaps | 2 (the gap entries in findings 5, 6) | The three items of finding 5 are assigned respectively to M5 high availability / D7 before control-plane design / the retention policy; finding 6 has no gap |
| Changes required | 0 | — |

## Sign-off

| Item | Value |
|---|---|
| Review conclusion | Pass |
| State transition | ADR-0006 `draft` → `accepted`; registry synchronized |
| Reviewer | AI agent, 2026-09-28 |
| Maintainer sign-off | To be filled in |
