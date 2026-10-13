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

# M8 Batch 3 "kind/sim Evidence" — New Session Prompt

## Opening Ritual
1. Read AGENT.md, docs/README.md, docs/plan.md (M8 section), docs/acceptance/m8-test-plan-matrix.md
2. Verify the work tree with `git status`
3. `export PATH="$PWD/tools/bin:$PATH"`

## Current Status
- Done: Batch 1 (release and packaging), Batch 2 (SIP dual-run S8/S5/S7a/S6/S10/S9/S11)
- Branch master, all changes uncommitted (committing is not allowed)
- kind cluster: as-m5 (context kind-as-m5)
- Tools: tools/bin (kind 0.24.0 / kubectl 1.31.4 / helm 3.16.4)
- Image: as-platform built (with native SIP listener)
- Environment name: dev-win03ib7niepf0

## Evidence Collection Scope (in order)
1. **F-15 Real AS Full Stack** (first, everything else depends on it)
   - helm deploy to kind (translation + antiFraud + config-service + bundled PG + Redis)
   - Verify: distribute → healthy → automatic rollback → manual rollback
   - Reference deploy/helm/values-onprem.example.yaml
2. **NF-2 Dual Deployment Isolation**: kill the translation Pod, antiFraud unaffected
3. **NF-9 Namespace Isolation**: kill PG / delete AS in ns-A, ns-B unaffected
4. **NF-10 Canary Distribution/Rollback**: collect evidence together with F-15
5. **NF-4 Rolling Upgrade Zero Loss**: under continuous SIP call load, helm rollout restart; verify no interruption
6. **NF-5 Simulator-Swap Consistency**: M7.1 simulator S-SBC (UDP/TCP/TLS) behaves consistently
7. **2.5 Backup Restore Drill**: kind bundled PG pg_dump → drop data → pg_restore → verify audit chain; record measured elapsed time (RTO order of magnitude, not a commitment); reference docs/operations/backup-restore.md §2

## Hard Discipline
- The main agent does not write files; dispatch a writing subagent (general_purpose_task), only one per work tree at a time
- Do not perform any git write operations (add/commit/tag/push/branch)
- Do not sign off any REQ, do not change matrix status, do not change report.md counts
- Four-layer evidence: filename `PASS-`/`FAILCLOSED-` prefix → docs/acceptance/artifacts/m5/2026-10-12/; environment name `dev-win03ib7niepf0`; triple `(verdict, evidence file, date)`; run tests/test_evidence_discipline.py
- Do not invent new numbering, do not publish external capacity numbers

## Key Files
- Execution basis: docs/handoff/2026-10-12-m8-scope-revision-internal-release-plan.md §2.3
- Matrix: docs/acceptance/m8-test-plan-matrix.md
- Helm: deploy/helm/values-onprem.example.yaml
- Backup runbook: docs/operations/backup-restore.md §2
- State store: docs/acceptance/m5-state-stores-runbook.md
- SIP simulators: testbed/simulators/

## Wrap-Up
- Land a `PASS-`/`FAILCLOSED-` evidence file for each item
- Once all are done: `make gate` all green + verify with `git status`
- Write review record: docs/reviews/m8-batch3-kind-sim-evidence-review-2026-10-12.md
- Write handoff: docs/handoff/2026-10-12-m8-batch3-complete-handoff.md

## Cautions
- The kind cluster has only as-m5; inspect the current state with `kubectl get all -A` before deploying
- Images require `kind load docker-image as-platform:<tag> --name as-m5`
- Register a FAILCLOSED- artifact for anything that cannot be evidenced; do not force a pass
