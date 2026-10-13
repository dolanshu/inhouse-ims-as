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

# M8 Batch 4 "Sign-off and Review" — New Session Prompt

## Opening Ritual
1. Read AGENT.md, docs/README.md, docs/plan.md (M8 section), docs/acceptance/m8-test-plan-matrix.md
2. `git status` to verify the working tree
3. Confirm that the evidence files of batches 2/3/5 are already on disk (docs/acceptance/artifacts/m5/2026-10-12/)

## Current State
- Completed: batch 1 (release and packaging), batch 2 (SIP differential testing), batch 3 (kind/sim evidence), batch 5 (performance and capacity)
- Branch master, all changes uncommitted (committing is forbidden)
- This batch depends on all evidence produced by the preceding batches
- Environment name: dev-win03ib7niepf0

## Core Boundary (most important)
**This batch does not counter-sign any REQ.** "Accepting engineering evidence" ≠ REQ-level acceptance passed ≠ milestone sign-off.
All pass transitions must be confirmed by the maintainer in the M8 exit review; the agent only does:
1. Review line by line whether the evidence is sufficient
2. Backfill missing measurements (engineering layer only, do not touch external environments)
3. Give a pass/n-a/defer recommendation + rationale
4. Prepare a draft update for the matrix rows (do not modify the matrix directly; wait for maintainer approval)

## Work Scope
### 1. S-1 (whitelist) review
- Review existing evidence: whitelist logic (ingress.py allowlist/peer) + changes go through approval (F-14 linkage)
- Backfill missing measurements: whitelist rejection scenarios, whitelist change taking effect after approval
- Evidence: PASS/FAILCLOSED-s1-whitelist-review-2026-10-12.txt

### 2. S-4 (RBAC + tamper-proof audit) review
- The durable audit engineering slice is already in place (PostgresAuditStore + owner trigger blocking mutation/truncate)
- Backfill what is missing for a formal all-green: audit append-only verification, RBAC permission matrix verification
- Evidence: PASS/FAILCLOSED-s4-rbac-audit-review-2026-10-12.txt

### 3. Finalize each `open` row of the matrix
For each `open` row in docs/acceptance/m8-test-plan-matrix.md, give a recommended final state:
- **pass**: must have new evidence from this version (triple archived), with the evidence file path attached
- **n-a**: attach a rationale (e.g. v1.1 scope, non-goal item)
- **defer**: attach a rationale (e.g. depends on external environment X1, customer cluster, carrier PKI)

Open rows to review (defer to the matrix's actual contents):
- F-1 ~ F-16 (basic call, Call-ID, translation, SDP, Route, 404, block, CANCEL, in-dialog, non-2xx, race, console, approval, decision chain)
- NF-2, NF-5, NF-9, NF-10, NF-13, NF-14, NF-15
- S-1, S-4
- D12/O5-HA

**Rows that depend on external environments (NF-13 live capture, NF-14 real alarm triggering, etc.) move to defer with a rationale and are submitted to the maintainer for review.**

### 4. Matrix update draft
- Produce a matrix update draft document (docs/acceptance/m8-matrix-finalization-draft-2026-10-12.md)
- Per row: original status → recommended final state → rationale → evidence file
- **Do not modify m8-test-plan-matrix.md directly**; after the maintainer approves the draft, the maintainer or an authorized agent executes it

## Hard Discipline
- The main agent does not write files; dispatch a writing subagent (general_purpose_task), only one at a time in a single working tree
- Do not perform any git write operation
- **Do not modify matrix status directly, do not modify report.md counts** — only produce a draft
- Four-layer evidence: PASS-/FAILCLOSED- prefix → docs/acceptance/artifacts/m5/2026-10-12/; environment name dev-win03ib7niepf0; triple
- Backfilling missing measurements covers the engineering layer only (unit/contract/integration); do not touch external environments (customer cluster, carrier PKI)
- Before the maintainer confirms, no row may move from open to pass

## Key Files
- Matrix: docs/acceptance/m8-test-plan-matrix.md
- Execution basis: docs/handoff/2026-10-12-m8-scope-revision-internal-release-plan.md §2.4
- Batch 2 evidence: docs/acceptance/artifacts/m5/2026-10-12/PASS-s5~s11-*.txt
- Batch 3 evidence: docs/acceptance/artifacts/m5/2026-10-12/PASS-nf*/f15*/2-5-*.txt
- Batch 5 evidence: docs/acceptance/artifacts/m5/2026-10-12/PASS-nf15*/o1*/hpa*.txt
- Whitelist implementation: platform/src/as_platform/sip/ingress.py
- Audit implementation: platform/src/as_platform/config/audit_store.py and others

## Wrap-up
- S-1/S-4 review evidence lands on disk
- Matrix finalization draft lands on disk (docs/acceptance/m8-matrix-finalization-draft-2026-10-12.md)
- Once everything is done: `make gate` fully green + `git status` verification
- Write the review record: docs/reviews/m8-batch4-signoff-review-2026-10-12.md
- Write the handoff: docs/handoff/2026-10-12-m8-batch4-complete-handoff.md

## Caveats
- The core discipline of this batch is "no counter-signing" — every pass recommendation must be annotated "pending maintainer confirmation at the M8 exit review"
- If the evidence for a row is insufficient, prefer marking defer over marking pass
- Rows depending on X1 (capture wiring) or external environments are always defer; do not force backfill measurements
