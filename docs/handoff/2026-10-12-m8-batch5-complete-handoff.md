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

# M8 Batch 5 "Performance and Capacity (kind)" Completion Handoff (2026-10-12)

## 0. Nature and Boundaries of This Document

This is the M8 batch 5 completion handoff, with the accompanying review record `docs/reviews/m8-batch5-performance-capacity-review-2026-10-12.md`.

- It does not sign off any REQ, does not change matrix status, and does not change report.md counts.
- It does not constitute a capacity/SLA commitment; internal engineering target values must not be written into external material.
- Execution environment: dev-win03ib7niepf0 (cluster kind-as-m5).
- No git write operation was performed; all changes remain in the working tree for the maintainer to split into commits.

## 1. Completion List (4/4) and Triples

| Item | Triple (conclusion, evidence, date) |
| --- | --- |
| NF-15 multi-replica measurement | (verified, docs/acceptance/artifacts/m5/2026-10-12/PASS-nf15-multi-replica-measurement-2026-10-12.txt, 2026-10-12) |
| O1 loopback 1280 (internal) | (verified, docs/acceptance/artifacts/m5/2026-10-12/PASS-o1-loopback-cps-1280-2026-10-12.txt, 2026-10-12) |
| HPA threshold fill-in | (verified, docs/acceptance/artifacts/m5/2026-10-12/PASS-hpa-threshold-filled-2026-10-12.txt, 2026-10-12) |
| performance gate final state | (failure registered - pending adjudication, docs/acceptance/artifacts/m5/2026-10-12/FAILCLOSED-performance-gate-terminal-state-2026-10-12.txt, 2026-10-12) |

## 2. Summary of Key Results

- **NF-15**: 2 replicas at five tiers (20/80/320/640/1280 CPS × 15s, hold=0, accept-all UDP) with zero failures. Per-pod resources (requests 200m/256Mi as the denominator): CPU about 2%/11%/50%/105%/214%, memory about 7%/8%/14%/26%/59%; call-setup latency p95 52.7/8.3/7.7/4.4/29-36ms (the first tier is cold start). 4 replicas @1280 direct-connecting via podIP are perfectly balanced with linear resources. Architecture finding: ClusterIP UDP short flows are pinned to an endpoint by conntrack, so multi-replica balancing cannot go through the ClusterIP path.
- **O1**: loopback 1280 CPS, 19200/19200 established, zero unresolved, p95 12.79ms (internal re-measurement).
- **HPA**: `deploy/helm/values-onprem.example.yaml` +37 lines for the autoscaling section (enabled, minReplicas 2 / maxReplicas 4, CPU/MEM 70 each, customMetric null), annotated verbatim "measured on kind, not an external commitment, must be re-measured in the target environment before go-live"; the default values.yaml and hpa.yaml have zero changes; rendering yields 2 HPA (example) / 0 HPA (default), both guards are effective in measurement, chart-check OK.
- **performance gate**: FAILCLOSED has been registered; awaiting the maintainer's adjudication between (a) implementing a `make gate` blocking layer and (b) written risk acceptance at the M8 final review.

## 3. List of Changed Files (all uncommitted)

| File | Change |
| --- | --- |
| deploy/helm/values-onprem.example.yaml | +37 lines for the autoscaling section (the only code/config change in this batch) |
| docs/acceptance/artifacts/m5/2026-10-12/PASS-nf15-multi-replica-measurement-2026-10-12.txt | New evidence |
| docs/acceptance/artifacts/m5/2026-10-12/PASS-o1-loopback-cps-1280-2026-10-12.txt | New evidence |
| docs/acceptance/artifacts/m5/2026-10-12/PASS-hpa-threshold-filled-2026-10-12.txt | New evidence |
| docs/acceptance/artifacts/m5/2026-10-12/FAILCLOSED-performance-gate-terminal-state-2026-10-12.txt | New evidence |
| docs/acceptance/artifacts/m5/README.md | +4 lines of index (the FAILCLOSED row is annotated "not a pass-evidence artifact") |
| docs/reviews/m8-batch5-performance-capacity-review-2026-10-12.md | New review record |
| docs/handoff/2026-10-12-m8-batch5-complete-handoff.md | New handoff (this document) |

Not part of this batch (do not mix into this batch's commit): `.dockerignore` modified (leftover from batch 1); `docs/handoff/2026-10-12-m8-batch4-prompt.md` and `docs/handoff/2026-10-12-m8-batch6-prompt.md` are newly added by the maintainer and untracked. The maintainer already committed 004904b "m8 batch3 done" during the measurement period; this batch performed no git write operation.

## 4. Verification Results

`make gate` (2026-10-12, dev-win03ib7niepf0, exit 0):

- 550 files already formatted;
- ruff: All checks passed;
- mypy: Success, 90 files;
- pytest: 1150 passed, 227 deselected, 11 warnings;
- tests/test_evidence_discipline.py: 127 passed.

`make chart-check`: chart-check: OK. The raw error messages of the two helm guards are recorded verbatim in the PASS-hpa-threshold-filled-2026-10-12.txt evidence file.

## 5. Cluster and Execution Host State (not cleaned up; deletion is an irreversible action)

kind-as-m5 gained the new namespace **nf15-perf**, containing:

- helm release `nf15`: anti-fraud 2 replicas + bundled PG/Redis + config-service;
- Deployment `sut-direct`: currently 4 replicas (for podIP broadcast direct-connect);
- Pod `as-load-gen`: `sleep infinity`, containing the /tmp/as_load driver.

Cleanup command (the maintainer decides the timing):

```
kubectl --context kind-as-m5 delete namespace nf15-perf
```

The helm release and the temporary Deployment are both inside that ns, so deleting the ns removes them; no separate cleanup is needed.

Not touched: the existing kind-as-m5 namespaces as-m5 / as-m5b (batch 3 state), kind-as-m71 (batch 3 ims-sim/as-sut), local compose containers (as-m4b8-dev-postgres-1, etc.).

Raw measurement data: `/tmp/m8b5/` (nf15-2rep/, nf15-direct-2rep/, nf15-direct-4rep/, o1-loopback/, values and manifest snapshots, driver scripts), retained until the maintainer cleans up.

## 6. Items Pending the Maintainer

1. **B5-04 adjudication**: the final state of the performance-layer gate — implement a `make gate` blocking layer, or written risk acceptance at the M8 final review.
2. The final adjudication and signature for B5-04 in review record items B5-01..B5-07 (the other 6 are already closed/changed).
3. Working tree commit split: the values-onprem example + evidence + index + review/handoff form one group; the `.dockerignore` leftover is handled separately.
4. Timing of the nf15-perf namespace cleanup (see the command in §5).
5. The NF-15 matrix row stays `open`; whether to finalize it per the criteria in batch 4 "Sign-off and Review" is decided by that batch — this batch does not touch it.

> **Destination pointer (appended 2026-10-13; the original text of the five items above is retained unchanged)**: the destinations of the items in this section that are not yet closed are —
> **Item 5**: the NF-15 matrix row stays `open` and whether to finalize it is adjudicated together with the measurement batch →
> [`../next-release-v1.1-plan.md`](../next-release-v1.1-plan.md) **§5-5**; the body itself (HPA thresholds already adjudicated as filling
> `values-onprem.example.yaml`, the default `values.yaml` stays null, and the lack of a measurement batch **with per-pod CPU / memory
> utilization**; the 2026-10-12 saturation probe recorded no resource data) see **§4-9** of the same document;
> **Items 3 / 4**: working tree commit split, timing of the `nf15-perf` namespace cleanup → same document **§5-6** (governed by the `git status` state, not itemized);
> **Items 1 / 2**: final adjudication and signature for the B5-04 performance-layer gate final state — the branch of accepting the risk in writing was exercised on 2026-10-13 via path C;
> whether a `make gate` blocking layer is still needed is confirmed separately by the maintainer, and any remaining leftovers afterwards are scheduled separately per the startup prerequisites in **§9** of the same document.
> Subsequent status reviews, reports, and handoffs that touch the leftover items in this section always **cite only that pointer**, do not itemize, and no longer list them as "actions for the maintainer".

## 7. Discipline Compliance Statement

- The main agent did not write any repository file directly; all repository file changes were written by a general-purpose writing subagent and verified with git status/diff; only one writing subagent at a time in the same working tree.
- Under /tmp only scripts and raw measurement data were operated on.
- No git add/commit/tag/push/branch.
- No REQ sign-off, no matrix/report count changes.
- Evidence files contain no credentials/tokens/cookies.
- FAILCLOSED is annotated in the index as "not a pass-evidence artifact"; no capacity-class alarms were added.

## 8. Maintainer Additional Adjudication 2026-10-13: batch 5 judged pass + next release enhancement

- **Batch 5 judged pass** (maintainer 2026-10-13): engineering acceptance at the batch level; **this is not a REQ-NF-15 sign-off**, the NF-15 row of the matrix stays open, report.md counts are unchanged, and it does not constitute the M8 exit sign-off.
- **A plain-language explanation has been appended**: the two measurement evidence files (PASS-o1-loopback-cps-1280, PASS-nf15-multi-replica-measurement) each gained a "plain-language explanation" section at the end — role division (as_load=UAC, AS=UAS), the 7 messages per call and the 4-message setup-latency window, the cause of accept-all's single leg (the accept_all_invites branch in resip_runtime.py answers directly instead of forwarding), why the production B2BUA two-leg path was not covered this time, and the exact meaning and limits of the numbers.
- **Next release enhancement direction** (B5-09): turn off the accept_all_invites switch, stand up a real downstream UAS, and run real-socket load testing over the complete "inbound leg + outbound leg" B2BUA two-leg path, so that capacity measurement covers the business decision and forwarding path; not initiated for implementation in this version.
- **B5-04 is not covered by this pass**: the performance-layer gate final state ((a) blocking layer or (b) written risk acceptance at the M8 final review) still awaits the M8 final review's adjudication; the FAILCLOSED evidence remains valid.
- This round only appends documentation (2 evidence files + this handoff + review record); no git write operation was performed.
