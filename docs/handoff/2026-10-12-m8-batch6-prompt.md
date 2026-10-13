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

# M8 Batch 6 "Documentation and Reports" — New Session Prompt

## Opening Ritual
1. Read AGENT.md, docs/README.md, docs/plan.md (M8 section), docs/acceptance/m8-test-plan-matrix.md
2. `git status` to verify the working tree
3. Confirm that the evidence and review documents of batches 1~5 are already on disk

## Current State
- Completed: batch 1 (release and packaging), batch 2 (SIP differential testing), batch 3 (kind/sim evidence), batch 4 (sign-off and review), batch 5 (performance and capacity)
- Branch master, all changes uncommitted (committing is forbidden)
- This is the final batch; it depends on all preceding output
- Environment name: dev-win03ib7niepf0

## Already Adjudicated (do not re-ask, do not change)
- **VERSION is not bumped**: stays 0.2.0
- **CHANGELOG**: append an internal build entry inside the 0.2.0 section (batch 1 already did this)
- **Image tag**: as-platform:0.2.0-internal-<date>, chart not synchronized
- **M8 is not signed**: the M8 row in the milestone signature sheet stays blank; M1/M2/M6/M7 engineering completion are already counter-signed on authorization

## Work Scope (E-1 ~ E-6)
### E-1: Promote report.md to the M8 RC report
- Synchronize the §0.5 counts in docs/acceptance/report.md with the matrix's current values
- Count values follow the batch 4 finalization draft (pass / open / blocked / n-a / fail)
- The report header must state clearly "internal version, not the M8 exit sign-off"

### E-2: VERSION / CHANGELOG
- VERSION stays 0.2.0 (already adjudicated, do not change)
- Confirm that the 0.2.0 section of CHANGELOG contains an internal build (2026-10-12) entry
- If it is already in place, only confirm it; do not append again

### E-3: Write back the M8 row in plan.md §0 / §4
- Write back the M8 row according to the actual wrap-up state of this version
- The final wording of the M8 row is confirmed by the maintainer — the agent produces a draft first and does not modify plan.md directly

### E-4: Internal-version exit review document
- Create docs/reviews/m8-internal-release-exit-review-2026-10-12.md
- Contents: items completed in this version, evidence list, known gaps (FAILCLOSED items), limitation statements
- **State explicitly that this is not the M8 exit sign-off**

### E-5: Milestone signature sheet
- M1 / M2 / M6 / M7 "engineering completion" are already counter-signed under maintainer authorization (keep as is)
- **M8 is not signed** — annotate the M8 row of the signature sheet with "internal version, no sign-off"

### E-6: Packaging re-check
- Run tests/test_version_consistency.py (fully green)
- Image and Helm are reproducibly buildable (rebuild once; the digest matches batch 1 or record the new digest)
- Sanitization re-check: no secrets/certificates/packet captures/password-bearing logs inside the image
- README and runbook are consistent with the AS_SIP_*/AS_TLS_* implementation (check every environment variable)
- Evidence: PASS-e6-packaging-recheck-2026-10-12.txt

## Hard Discipline
- The main agent does not write files; dispatch a writing subagent (general_purpose_task), only one at a time in a single working tree
- Do not perform any git write operation
- Do not sign any REQ, do not sign the M8 milestone
- Four-layer evidence: PASS-/FAILCLOSED- prefix → docs/acceptance/artifacts/m5/2026-10-12/; environment name dev-win03ib7niepf0; triple
- When writing documentation, always "keep the original text unchanged and append a correction"
- Writing back the M8 row in plan.md requires a draft first; wait for maintainer confirmation

## Key Files
- Execution basis: docs/handoff/2026-10-12-m8-scope-revision-internal-release-plan.md §2.6
- Report: docs/acceptance/report.md
- Version: VERSION, CHANGELOG.md
- Plan: docs/plan.md
- Matrix: docs/acceptance/m8-test-plan-matrix.md
- Batch 4 finalization draft: docs/acceptance/m8-matrix-finalization-draft-2026-10-12.md
- Version consistency test: tests/test_version_consistency.py
- Dockerfile: deploy/docker/Dockerfile
- Helm: deploy/helm/

## Wrap-up
- E-1~E-6 all completed
- `make gate` fully green + `tests/test_version_consistency.py` + `tests/test_evidence_discipline.py` fully green
- `git status` to verify all changes
- Write the review record: docs/reviews/m8-batch6-docs-report-review-2026-10-12.md
- Write the final handoff: docs/handoff/2026-10-12-m8-batch6-complete-handoff.md
- State explicitly in the handoff: all changes are uncommitted; the maintainer decides the commit split

## Caveats
- This batch changes no code, only documentation and reports
- If evidence from a preceding batch is found missing, register FAILCLOSED- and note it in the handoff; do not backfill it on your own
- The internal-version exit review is not the M8 exit sign-off; the wording must be strictly distinguished
