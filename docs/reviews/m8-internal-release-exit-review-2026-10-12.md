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

**This document is the "internal release wrap-up review", not the M8 exit sign-off.**

# M8 Internal Release Wrap-Up Review Record (2026-10-12)

- **Review target (object)**: M8 internal release wrap-up; scope covers the outputs of all six batches from batch 1 "release and packaging" to batch 6 "docs and reports".
- **Review date (date)**: 2026-10-13 (document batch date: 2026-10-12).
- **Reviewer (reviewer)**: AI agent (maintainer-authorized to execute batches 1–6); **the maintainer confirmation block is left blank pending signature**.
- **Conclusion (conclusion)**: **internal release wrap-up complete (conditional)**. The condition is that the M8 exit sign-off remains deferred, placed after closure of the external hard dependencies. **This is not the M8 exit sign-off, and not a "pass" conclusion.**
- **Execution environment**: `dev-win03ib7niepf0`.

---

## 1. Items Completed in This Release

### 1.1 Batch 1: Release and Packaging

Dockerfile carries a SIP listener; the internal image tag is `as-platform:0.2.0-internal-20261012`; the build digest, runtime SIP listener, desensitization check and environment documentation alignment boundary have been recorded.

- `(verified, docs/acceptance/artifacts/m5/2026-10-12/PASS-docker-build-digest-2026-10-12.txt, 2026-10-12)`
- `(verified, docs/acceptance/artifacts/m5/2026-10-12/PASS-desensitization-check-2026-10-12.txt, 2026-10-12)`

### 1.2 Batch 2: SIP Cross-Check (A3 Phase D)

- `(verified, docs/acceptance/artifacts/m5/2026-10-12/PASS-s5-call-id-stability-2026-10-12.txt, 2026-10-12)`
- `(verified, docs/acceptance/artifacts/m5/2026-10-12/PASS-s6-multi-rule-priority-2026-10-12.txt, 2026-10-12)`
- `(verified, docs/acceptance/artifacts/m5/2026-10-12/PASS-s7a-sdp-corpus-expansion-2026-10-12.txt, 2026-10-12)`
- `(verified, docs/acceptance/artifacts/m5/2026-10-12/PASS-s8-baseline-recapture-2026-10-12.txt, 2026-10-12)`
- `(verified, docs/acceptance/artifacts/m5/2026-10-12/PASS-s9-in-dialog-bye-routing-2026-10-12.txt, 2026-10-12)`
- `(verified, docs/acceptance/artifacts/m5/2026-10-12/PASS-s10-non-2xx-passthrough-2026-10-12.txt, 2026-10-12)`
- `(verified, docs/acceptance/artifacts/m5/2026-10-12/PASS-s11-cancel-race-branch1-2026-10-12.txt, 2026-10-12)`

### 1.3 Batch 3: kind / sim Evidence

- `(verified, docs/acceptance/artifacts/m5/2026-10-12/PASS-nf2-deployment-isolation-2026-10-12.txt, 2026-10-12)`
- `(verified-accepted measured call loss, docs/acceptance/artifacts/m5/2026-10-12/PASS-nf4-rolling-upgrade-accepted-loss-2026-10-12.txt, 2026-10-12)`
- `(verified, docs/acceptance/artifacts/m5/2026-10-12/PASS-nf5-simulator-transport-consistency-2026-10-12.txt, 2026-10-12)`
- `(verified, docs/acceptance/artifacts/m5/2026-10-12/PASS-nf9-namespace-isolation-2026-10-12.txt, 2026-10-12)`
- `(verified, docs/acceptance/artifacts/m5/2026-10-12/PASS-f15-distribution-lifecycle-rollback-2026-10-12.txt, 2026-10-12)`
- `(verified, docs/acceptance/artifacts/m5/2026-10-12/PASS-backup-restore-drill-bundled-pg-2026-10-12.txt, 2026-10-12)`

### 1.4 Batch 4: Sign-off and Review

- `(verified-rejection scenarios only, docs/acceptance/artifacts/m5/2026-10-12/PASS-s1-whitelist-rejection-2026-10-12.txt, 2026-10-12)`
- `(verified, docs/acceptance/artifacts/m5/2026-10-12/PASS-s4-audit-append-only-2026-10-12.txt, 2026-10-12)`
- `(verified, docs/acceptance/artifacts/m5/2026-10-12/PASS-s4-rbac-permission-matrix-2026-10-12.txt, 2026-10-12)`

Matrix final-state registration pointer: `(verified, "M8 Batch 4 Final-State Countersign (2026-10-13)" section of docs/acceptance/m8-test-plan-matrix.md, 2026-10-13)`. The current counts are pass 27 / defer 4 / blocked 9 / n-a 9 / open 0 / fail 0; all sign-off bases are "engineering evidence accepted", all are agent countersignatures (maintainer-authorized), not the maintainer's own signature.

### 1.5 Batch 5: Performance and Capacity

- `(verified-non-saturation point, docs/acceptance/artifacts/m5/2026-10-12/PASS-nf15-multi-replica-measurement-2026-10-12.txt, 2026-10-12)`
- `(verified-internal use only, docs/acceptance/artifacts/m5/2026-10-12/PASS-o1-loopback-cps-1280-2026-10-12.txt, 2026-10-12)`
- `(verified, docs/acceptance/artifacts/m5/2026-10-12/PASS-hpa-threshold-filled-2026-10-12.txt, 2026-10-12)`

The CPS 1280 in `PASS-o1-loopback-cps-1280-2026-10-12.txt` is only an internal engineering target and must not be written into external materials.

### 1.6 Batch 6: Docs and Reports

- `(verified, docs/acceptance/artifacts/m5/2026-10-12/PASS-e6-packaging-recheck-2026-10-12.txt, 2026-10-12)`

---

## 2. Known Gaps and Final-State Boundaries

The following `FAILCLOSED-` / `FAIL-` files are **never pass evidence**:

1. Zero-loss rolling upgrade was not achieved; the current release only accepts the range of measured call loss already tested: `(failure registered-not pass evidence, docs/acceptance/artifacts/m5/2026-10-12/FAILCLOSED-nf4-rolling-restart-inflight-loss-2026-10-12.txt, 2026-10-12)`.
2. The original FAILCLOSED registration for the terminal state of the performance-layer gate is still not pass evidence; B5-04 of batch 4 has been adjudicated to adopt `(b)`, closed by written risk acceptance from the overall M8 review, and this release does not implement the `make gate` blocking layer: `(failure registered-not pass evidence, docs/acceptance/artifacts/m5/2026-10-12/FAILCLOSED-performance-gate-terminal-state-2026-10-12.txt, 2026-10-12)`.
3. The whitelist-change approval capability does not exist: `(capability absent-not pass evidence, docs/acceptance/artifacts/m5/2026-10-12/FAILCLOSED-s1-whitelist-change-approval-not-wired-2026-10-12.txt, 2026-10-12)`.
4. in-dialog re-INVITE / UPDATE are not implemented: `(not implemented-not pass evidence, docs/acceptance/artifacts/m5/2026-10-12/FAILCLOSED-s9-reinvite-update-not-implemented-2026-10-12.txt, 2026-10-12)`.
5. The CANCEL-before-any-downstream-response branch is not implemented: `(not implemented-not pass evidence, docs/acceptance/artifacts/m5/2026-10-12/FAILCLOSED-s11-cancel-before-any-downstream-response-2026-10-12.txt, 2026-10-12)`.
6. The PostgreSQL 15 integration run failed; the standard environment is PostgreSQL 12.22, and this batch did not change product code: `(failed-not pass evidence, docs/acceptance/artifacts/m5/2026-10-12/FAIL-integration-pg15-2026-10-12.txt, 2026-10-12)`.

There are also 4 `defer` rows: F-5 / F-8 / F-9 / F-11, all not accepted in this release and already earmarked for v1.1; plus 9 `blocked` rows, which are restriction / constrained items registered in the current matrix. The definitions of `defer`, `blocked` and `n-a` are governed by section three of the matrix's "M8 Batch 4 Final-State Countersign (2026-10-13)" section.

---

## 3. List of Issues and Corresponding Fixes / Disposition

| # | Issue Found | Corresponding Fix / Disposition | Current Status |
|---|---|---|---|
| 1 | The manifest digest of the rebuilt image differs from the value recorded in batch 1 | Preserve the batch 1 historical digest, and record in the E-6 evidence the new digest, the buildx attestation / manifest-list difference and the "do not claim byte-for-byte identity" boundary | Recorded; no claim of image content change is made on this basis |
| 2 | `report.md` §0.5 still holds the 2026-10-06 historical counts | Only append §0.10 to sync the current counts; the historical paragraph is left unchanged | Synced |
| 3 | The old M8 exit review signature table does not reflect the internal release wrap-up status | Only append §3.2; M8 remains unsigned, and M1/M2/M6/M7 keep the authorized-countersign engineering-complete basis | Registered |
| 4 | The M8 row of `plan.md` has not yet been written back for the internal release wrap-up | Only produce the `m8-plan-m8-row-draft-2026-10-12.md` draft and wait for maintainer confirmation; `plan.md` was not changed | Pending maintainer confirmation |
| 5 | External hard dependencies and v1.1 gaps are not yet closed | External dependencies stay `blocked`, F-5/F-8/F-9/F-11 stay `defer`; internal evidence does not substitute for customer / carrier environments | Deferred, not equivalent to cancelled |
| 6 | M5 REQ-level acceptance still does not pass | Keep the existing conclusion; do not override REQ-level conclusions with the internal release wrap-up | Unchanged |

---

## 4. Limitation Notes

1. Simulator / kind evidence is engineering- and integration-level evidence; **it is not upgraded to carrier or customer acceptance**.
2. Test CA ≠ carrier PKI; REQ-S-2 / REQ-S-3 are not signed off.
3. kind bundled state ≠ production Redis / PostgreSQL HA; D12 / O5 are not accepted.
4. M7.1 simulated transparent bridge ≠ carrier S-SBC.
5. accept-all harness ≠ business adjudication path, therefore **the external commitment value for O1 is still left blank**; the internal engineering target of loopback CPS 1280 is internal-only and must not be written into external materials.
6. Internal version ≠ release version: VERSION remains `0.2.0`, is not tagged, and the chart does not change with the internal build.
7. **This document does not constitute the M8 exit sign-off.** The M8 exit sign-off is placed after the external hard dependencies D-1 (carrier PKI + external-network S-SBC), D-2 (customer K8s), the ADR-0008 cross-site drill, and closure of D12 / O5 production HA.
8. This batch performed no git write operations; the commit split is decided by the maintainer.

---

## 5. Post-Fix Confirmation Sign-off

| Item | Record |
|---|---|
| Review conclusion | **Internal release wrap-up complete (conditional)**; not a "pass" conclusion |
| Condition | The M8 exit sign-off stays deferred, placed after closure of the external hard dependencies |
| Reviewer | AI agent (maintainer-authorized to execute batches 1–6) |
| M8 exit sign-off block | **Unsigned (pending maintainer signature)** |
| Maintainer confirmation | **Pending signature** |
| Required maintainer actions | (1) Confirm the final wording of the M8 row in `docs/plan.md`; (2) provide a schedule for the external hard dependencies or written risk acceptance; (3) decide the commit split; (4) decide on and perform the tag, by the maintainer only |

---

## 6. Path C Correction (2026-10-13; all preceding sections preserved unchanged)

> This section only appends a correction; §1–§5 are unchanged down to the character.

The maintainer made the **M8 exit sign-off** on **2026-10-13** following **path C** — i.e. "sign the M8 exit sign-off + at the same time **accept the external hard dependency risk in writing**". Accordingly:

1. The document-opening statement "**This document is the 'internal release wrap-up review', not the M8 exit sign-off**" and the sign-off block in §5 (M8 exit sign-off block = unsigned) are **preserved as the historical conclusion of the internal release wrap-up stage**, and are neither rewritten nor treated as invalidated by this sign-off.
2. **The current status is governed by §3.3 of [`m8-exit-review-2026-10-06.md`](m8-exit-review-2026-10-06.md) and the risk-acceptance premise document [`m8-external-dependency-risk-acceptance-2026-10-13.md`](m8-external-dependency-risk-acceptance-2026-10-13.md)**.
3. This document is still retained as an **internal release wrap-up review archive**, and **all of its FAILCLOSED / gap / limitation notes remain in force** — **they are not invalidated by the M8 sign-off**:
   - The determination in §2 that the six `FAILCLOSED-` / `FAIL-` files are **never pass evidence** remains in force;
   - The eight limitation notes in §4 (test CA ≠ carrier PKI, kind bundled state ≠ production HA, accept-all harness ≠ business adjudication path, internal version ≠ release version, etc.) remain in force;
   - Item 7 of §4, "this document does not constitute the M8 exit sign-off", is preserved as **this document's own historical positioning**; the M8 exit sign-off is now registered in §3.3 of `m8-exit-review-2026-10-06.md`.
4. **Risk acceptance ≠ verified pass ≠ these rows becoming final**: the four external hard dependencies (D-1 / D-2 / ADR-0008 drill / D12-O5) stay `blocked` and roll over to the next release; the restart condition = a separate maintainer adjudication + external resources in place; deferred ≠ cancelled.
5. **The sign-off covers milestone exit, not REQ-level acceptance** —— M5 REQ-level is still a fail; no claim is made that M8 is all green.
6. This section performed no git write operations; the tag is performed by the maintainer only (`AGENT.md` §10.4). Execution environment `dev-win03ib7niepf0`.
