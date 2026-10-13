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

# M8 Batch 5 "Performance and Capacity (kind)" — New Session Prompt

## Opening Ritual
1. Read AGENT.md, docs/README.md, docs/plan.md (M8 section), docs/acceptance/m8-test-plan-matrix.md
2. `git status` to verify the working tree
3. `export PATH="$PWD/tools/bin:$PATH"`

## Current State
- Completed: batch 1 (release and packaging), batch 2 (SIP differential testing), batch 3 (kind/sim evidence, if already done)
- Branch master, all changes uncommitted (committing is forbidden)
- kind cluster: as-m5 (context kind-as-m5)
- Tools: tools/bin (kind 0.24.0 / kubectl 1.31.4 / helm 3.16.4)
- Load harness: testbed/load/ (`uv run python -m as_load --cps --duration --hold --workers --timeout`)
- loopback measurement script: testbed/load/scripts/m6-o1-formal-report.sh
- Environment name: dev-win03ib7niepf0

## Evidence Collection Scope (in order)
1. **NF-15 multi-replica measurement**
   - Deploy multi-replica AS on kind (set replicaCount > 1 in helm)
   - Drive SIP load with the testbed/load harness, record per-pod CPU/memory utilization
   - Measure several CPS tiers (e.g. 20/40/80/160/320/640/1280)
   - Evidence: PASS-nf15-multi-replica-measurement-2026-10-12.txt (contains per-pod CPU/memory, CPS tiers, call-setup latency p50/p95/p99)

2. **O1 internal engineering target re-measurement**
   - loopback CPS 1280 with no failures (internal only, not written into external material)
   - Reuse m6-o1-formal-report.sh or invoke as_load directly
   - Evidence: PASS-o1-loopback-cps-1280-2026-10-12.txt (internal only)

3. **Filling in the HPA thresholds**
   - Based on the kind measurements, fill the autoscaling section of deploy/helm/values-onprem.example.yaml:
     - minReplicas / maxReplicas
     - targetCPUUtilizationPercentage / targetMemoryUtilizationPercentage
   - **The default values.yaml stays null (do not touch)**
   - The example must state: "measured on kind, not an external commitment, must be re-measured in the target environment before go-live"
   - Evidence: PASS-hpa-threshold-filled-2026-10-12.txt (contains the values-onprem diff + measurement basis)

4. **Final state of the performance-layer gate**
   - Choose one: (a) implement it as a `make gate` blocking layer, or (b) written risk acceptance by the M8 final review
   - **Do not implement it on your own initiative, do not accept the risk on your own** — the maintainer must adjudicate
   - If it cannot be decided in this batch, register FAILCLOSED- with a note pending maintainer adjudication

## Hard Discipline
- The main agent does not write files; dispatch a writing subagent (general_purpose_task), only one at a time in a single working tree
- Do not perform any git write operation (add/commit/tag/push/branch)
- Do not sign any REQ, do not change matrix status, do not change report.md counts
- **Do not publish any external capacity figures** (AGENT.md §2); internal engineering target values must not be written into external material
- Four-layer evidence: filename PASS-/FAILCLOSED- prefix → docs/acceptance/artifacts/m5/2026-10-12/; environment name dev-win03ib7niepf0; triple (conclusion, evidence file, date); run tests/test_evidence_discipline.py
- No new capacity-class alarms; ne-datasheet capacity values and the 4.1 formal report stay blocked

## Key Files
- Execution basis: docs/handoff/2026-10-12-m8-scope-revision-internal-release-plan.md §2.5
- Matrix: docs/acceptance/m8-test-plan-matrix.md (NF-15 row)
- Load harness: testbed/load/ + testbed/load/scripts/m6-o1-formal-report.sh
- Helm HPA template: deploy/helm/templates/hpa.yaml (fail-fast: minReplicas/maxReplicas required, at least one target threshold)
- Helm values: deploy/helm/values.yaml (autoscaling section all null, **do not touch**) + values-onprem.example.yaml (to be filled)
- O1 historical report: docs/acceptance/m6-o1-measurement-report-2026-10-05.md

## Wrap-up
- Every item produces a PASS-/FAILCLOSED- evidence file
- Once everything is done: `make gate` fully green + `git status` verification
- Write the review record: docs/reviews/m8-batch5-performance-capacity-review-2026-10-12.md
- Write the handoff: docs/handoff/2026-10-12-m8-batch5-complete-handoff.md

## Caveats
- kind has limited resources; during multi-replica measurement watch CPU/memory limits and avoid node OOM
- as_load is IPv4-only (testbed/load/README.md current limitation #5)
- CPS 1280 is the loopback model's lower bound, not the saturation point and not a committed value
- If kind resources are insufficient for some CPS tier, record the highest tier actually measured; do not force 1280
