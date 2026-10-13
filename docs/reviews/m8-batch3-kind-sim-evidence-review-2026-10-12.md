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

# M8 batch 3 "kind/sim evidence" review record (2026-10-12)

> **Recorded on: 2026-10-12.** This file is the review vehicle for the 7 evidence items of
> [`../handoff/2026-10-12-m8-batch3-prompt.md`](../handoff/2026-10-12-m8-batch3-prompt.md)
> (F-15, NF-2, NF-9, NF-10, NF-4, NF-5, 2.5 backup/restore).
> **The agent proposes verdicts based on measured evidence and does not replace the maintainer's final judgement; this file signs off no REQ, does not change
> `docs/acceptance/m8-test-plan-matrix.md` status, and does not change report.md counts.**
> The environment is always `dev-win03ib7niepf0`.

## Current Status

- **Evidence completion: all 7/7 items executed** (2026-10-12). F-15/NF-10, NF-2, NF-9, NF-5, 2.5 backup/restore are **PASS (5 evidence files)**; NF-4 is **FAILCLOSED (1 file, not passing evidence)**; during evidence collection **1 P0 product defect** was found and fixed (1 PASS evidence file + code change).
- **P0 defect (auth-mode distribution lifecycle always 409): fixed, verified closed** (real cluster behaviour + 629 passed).
- **NF-4: the maintainer adjudicated on 2026-10-12 and signed off pass** (framing = rolling behaviour verified by measurement + in-flight call-loss scope accepted by the current release; **zero loss has NOT been achieved**); strict zero-loss rolling upgrade is registered as an enhancement feature for a future release (not raised as an item in this version). Evidence PASS-nf4-rolling-upgrade-accepted-loss-2026-10-12.txt; matrix REQ-NF-4 has been updated to pass (16→17), blocked 7→6.
- **Gate: `make gate` fully green** (on this machine, 2026-10-12): ruff format 546 files already formatted; ruff check All checks passed; mypy Success: no issues found in 90 source files; pytest `-m "unit or contract"` **1140 passed, 227 deselected, 11 warnings**. Evidence discipline test 117 passed.
- **config-service full suite (including integration, compose PG12.22): 629 passed, 3 skipped** (skips are due to wal_level=replica / PG version environment limits).
- **No REQ signed off; matrix and report.md unchanged; no git write operations whatsoever.**
- **Leftover items pending the maintainer**: whether to raise an item for config-service's single connection not auto-reconnecting (B3-04), and working-tree disposition (commit splitting is the maintainer's decision).

## 1. Review scope and method

| Item | Matrix row | Topology | Evidence file |
|---|---|---|---|
| F-15 true AS full stack (distribution/health/auto-rollback/manual rollback) | REQ-F-15 / 5.4-F-15 | kind-as-m5 / ns as-m5 / release `as` (bundled PG12.22 + Redis7) | PASS-f15-distribution-lifecycle-rollback-2026-10-12.txt |
| NF-10 canary distribution/rollback | REQ-NF-10 | Together with F-15 | Same as above |
| NF-2 dual-Deployment isolation | REQ-NF-2 | kind-as-m5 / ns as-m5 | PASS-nf2-deployment-isolation-2026-10-12.txt |
| NF-9 namespace isolation | REQ-NF-9 | kind-as-m5: ns as-m5 (release `as`) + ns as-m5b (release `asb`) | PASS-nf9-namespace-isolation-2026-10-12.txt |
| NF-4 rolling upgrade zero loss | REQ-NF-4 | kind-as-m71 / ns as-sut (product AS single replica, headless) | FAILCLOSED-nf4-rolling-restart-inflight-loss-2026-10-12.txt (**not passing evidence**) |
| NF-5 simulator neutrality (UDP/TCP/TLS) | REQ-NF-5 | kind-as-m71: ims-sim + as-sut | PASS-nf5-simulator-transport-consistency-2026-10-12.txt |
| 2.5 backup/restore drill | productization plan §2.5 / backup-restore.md §2/§4/§5 | kind-as-m5 bundled PG | PASS-backup-restore-drill-bundled-pg-2026-10-12.txt |
| P0 defect fix (found during evidence collection) | — | as-m5 measured + compose PG integration tests | PASS-config-service-auth-distribution-409-fix-2026-10-12.txt |

Method: everything was evidenced on real kind clusters + real helm releases + real SIP (M7.1 simulated S-SBC, native reSIProcate runtime); for each item the raw command output is kept verbatim in the evidence file; failed items are faithfully recorded as FAILCLOSED and are not forced to pass.

## 2. Per-item review conclusions

### 2.1 F-15 + NF-10: PASS (control-plane behaviour verified)

- CO-1 both batches healthy: distribution 201 start (first batch notified only) → first batch health in_progress → last batch health completed and the change order auto-applied (order_rev=5); the explicit apply idempotently replayed r1-1 with 200.
- CO-2 last batch set unhealthy: auto rolled_back (rolled_back_to=1, reason="health check failed"), the change order rolled_back, state persisted.
- CO-3 manual rollback after the first batch: rolled_back (rolled_back_to=2, reason="batch3 manual evidence drill").
- fleet-a actually received all notifications inside the cluster (change_id/version/bundle_version consistent with the API); fleet-b only got selftest — "notify the first batch only" is designed behaviour (pinned by test_fleet_api).
- **Boundary**: the product AS has no notify/bundle receiving end (lld fact), fleet-a/fleet-b are protocol stubs; the evidence proves the config-service control plane, not that the AS consumes bundles; the bundled single replica does not cover production HA.

### 2.2 NF-2: PASS

Across the whole window of deleting the translation Pod and having it recreated by the Deployment, anti-fraud's /health/live + /health/ready returned 42/42 as 200; the anti-fraud Pod's name/UID/startTime/restartCount stayed unchanged throughout, and translation obtained a new UID.

### 2.3 NF-9: PASS (with 1 observation)

While the PostgreSQL process in ns-A was stopped and the translation/anti-fraud Deployments were deleted, the independent ns-B full stack probed 58/58 as 200, and the identities of ns-B's 7 Pods (UID/startTime/restartCount) were unchanged item by item before and after the drill; ns-A was fully recovered via helm upgrade.
Observation: after PG recovery the config-service's single shared connection does not reconnect automatically (login 500), recovering after restarting the Deployment (measured 5.25s). Not changed in this batch; listed as Adjudication B3-04.

### 2.4 NF-4: in-flight call loss measured → maintainer adjudicated 2026-10-12 to accept it and signed off pass (zero-loss rolling upgrade listed as a future release feature)

- Topology: product AS single replica (values-product-as.yaml `replicaCount: null` → default 1; the comment explains that a second process would bind the same set of SIP ports), headless Service, RollingUpdate 25%/25%, preStop sleep 5 + terminationGracePeriodSeconds=300.
- Traffic: UDP, all-success scenario T1/T5/F1, 5cps×70s=350 calls per round, rollout restart at the 12s mark.
- Round 1 (20:47:37): 347/350 established; timeout_invite 3, bye_sip_481 6, timeout_bye 4; unresolved 10.
- Round 2 (20:51:15, independently reproduced): 346/350; timeout_invite 4, bye_sip_481 7, timeout_bye 3; unresolved 10.
- Root cause: ① the single-replica headless switchover window has a path with no INVITE answer (UDP, the peer addresses by Pod IP); ② dialog state exists only in the old process's memory (reSIProcate DUM has no serialize/deserialize API), so after the switchover the BYE goes to the new process → 481/timeout. Same origin as the registered native gap (M2 intends to remedy it with an S-SBC transparent bridge + StateStore). preStop/grace does not equal in-flight dialog migration.
- **Handling**: this batch does not change product code and does not change chart defaults; FAILCLOSED registration; the matrix stays blocked; whether to raise an item awaits maintainer adjudication (B3-02).

**Maintainer adjudication (2026-10-12)**: the current release accepts this level of call loss, NF-4 is marked pass, and the call loss will be addressed in a future release via feature enhancement. The acceptance framing is "measured behaviour verified + loss scope accepted", not that zero loss has been achieved.

**Switchover timing (k8s events measured to follow surge order)**: t≈0 the new Pod is created while the old Pod is still in the endpoints; t≈1-3s before the new Pod passes readiness, headless DNS returns both old and new A records simultaneously, and the S-SBC does a per-message getaddrinfo with no caching, so INVITEs land on either the old or the new Pod; t≈3s the old Pod goes Terminating — endpoint removal and preStop sleep 5 run in parallel with no ordering guarantee, and the sleep is opaque while the process is not marked not-ready and does not drain; t≈3-8s the old process still holds in-flight dialogs but is no longer in DNS; t≈8s+ SIGTERM exit.

**Two loss mechanisms**: ① timeout_invite (3/4) = during the UDP switchover window the INVITE goes to the old IP whose endpoint has already been removed, with no ICMP feedback and no terminal state within 6s; the new Pod does not reject any INVITE, so there are no 5xx and everything is a silent timeout. ② in-flight dialogs unresolved (exactly 10 per round) = dialog state lives only in the old process's DUM memory, and the BYE is routed by headless name to the new process and gets 481, or hits the exited old IP and times out; many times when the BYE fails the old process is still alive inside preStop, but it has been removed from DNS and dialogs are not sticky to the instance.

**Structural corroboration**: 5cps×hold 2s ≈ steady-state 10 concurrent, and the 10 unresolved in each of the two rounds = the whole window of in-flight dialogs at the switchover moment was damaged, not random packet loss.

**Candidate directions for a future release enhancement feature (not raised as an item in this version, no preselection)**: A process-level drain (preStop triggers not-ready/reject new requests + sleep ≥ the longest call duration); B S-SBC transparent bridge + StateStore externalization of dialog state (the route already established in M2, covering long calls); C Contact/Record-Route instance stickiness; D maintenance window / draining traffic first as an operational practice. See PASS-nf4-rolling-upgrade-accepted-loss-2026-10-12.txt for the full analysis.

### 2.5 NF-5: PASS (with a PKI boundary)

15 calls each over UDP/TCP/TLS (T1/T4/T5/F1/F2), with the three-round decision distribution identical bucket by bucket: 200×9 / 404×3 / 603×3, unresolved=0, no transport-level errors. TLS uses a test CA (not carrier PKI), so REQ-S-2/S-3 are not signed off; the call counts/latencies are values from this run, not a capacity commitment.

### 2.6 2.5 backup/restore: PASS (durations are orders of magnitude, not commitments)

After a real DROP (terminate+DROP, since PG12 does not support WITH FORCE), pg_restore rc=0 with 0 bytes on stderr; the 12 counts plus the three roles were consistent before and after, and both schemas were restored; the 8 audit append-only guards rejected as designed (UPDATE/DELETE/TRUNCATE/change_orders_events/uppercase outcome CHECK/id column/post-insert tampering rollback); console login 200, managed-rules 200 rows=2, audit continued appending. Measured: dump 0.259s, cp 0.143s, drop+create 1.123s, restore 0.704s, config-service restart 5.252s — **this only describes this lab's small dataset and does not presuppose RPO/RTO**; customer drills still follow the backup-restore.md §5 template.

### 2.7 P0 defect: auth-mode distribution lifecycle always 409 (fixed and closed)

- Symptom: on a real cluster, HTTPS login + CSRF followed by distribution start consistently returned 409 "distribution connection is not idle", and reports/apply/rollback were affected the same way; the path without auth does not trigger it, so earlier tests did not expose it.
- Root cause: the single shared psycopg connection is put into INTRANS by the SELECTs that the auth routes depend on (resolve_session/verify_csrf), so the internal require_idle_distribution_connection always fails; the entry middleware serialize_api_request already has an IDLE check + outbound rollback, making the internal check redundant and wrongly layered.
- Fix: deleted that function and its 4 call sites (net -10 lines); added 2 new real-PG + HTTPS-login + CSRF end-to-end regressions (start→reports→auto applied→idempotent apply; manual rollback).
- Verification: target file 19 passed (including the 2 new ones); config-service full suite 629 passed/3 skipped; after the fix the real-cluster F-15 full chain is 200/201.

### 2.8 Evidence-gathering engineering handling (not product functionality)

- Product image base bullseye→bookworm (after the native extensions were recompiled on 2026-10-12 they link libssl.so.3, which bullseye does not have): only `testbed/sim-platform/Dockerfile.product` was changed.
- kind load of multi-architecture manifest lists failed: the three images postgres:12.22 / redis:7-alpine / calico v3.28.2 were transferred as single-architecture via `docker build --platform linux/amd64` and then loaded; calico additionally had its image set to the `-kind` tag. This is an on-site operational means, with no repository file changes.
- The batch 2 commit (090312c) brought in 3 ruff non-compliance issues (test_s1_replay_contract.py formatting, UP041, F541); this batch made pure formatting/equivalence fixes to get the gate fully green (from Python 3.10 onwards socket.timeout is an alias of TimeoutError).

## 3. Summary of boundaries (not done / not proven by this batch)

1. No REQ is signed off; the status words of matrix rows F-15/5.4-F-15/NF-2/NF-4/NF-5/NF-9/NF-10 stay as-is (NF-4 is still blocked).
2. The fleet stub is not the AS bundle receiving end; a single-node kind does not prove node-level fault tolerance; the bundled single replica does not prove production HA (D12/O5).
3. NF-5's TLS uses a test CA; all call counts/latencies/backup durations are not capacity, SLA, RPO/RTO commitments.
4. NF-4's loss is not absorbed by tuning parameters or changing wording; the FAILCLOSED and root cause are archived faithfully.
5. Contains no credentials/tokens/packet captures; dump files stay in a temporary directory and are not committed.

## Adjudication

| ID | Source | Issue summary | Verdict | Fix plan | Status | Verification method | Notes |
|---|---|---|---|---|---|---|---|
| B3-01 | F-15 evidence | With auth enabled, distribution start/reports/apply/rollback always return 409 (the shared connection is put into INTRANS by auth SELECTs + a redundant idle check) — P0 product defect | Accept | Deleted require_idle_distribution_connection and its 4 call sites (net -10 lines), added 2 real-PG/HTTPS/CSRF end-to-end regression tests | Verified | Target file 19 passed; config-service 629 passed/3 skipped; after the fix the real-cluster F-15 full chain is 200/201 | Fix evidence PASS-config-service-auth-distribution-409-fix-2026-10-12.txt; pending maintainer confirmation |
| B3-02 | NF-4 two rounds of traffic | In-flight loss on rollout restart under a single-replica headless topology: timeout_invite 3/4, bye_sip_481 6/7, timeout_bye 4/3, unresolved 10/10 (3.7%/4.0% affected) | Accept | Maintainer adjudication 2026-10-12: the current release accepts this level of call loss, REQ-NF-4 signed pass under "measured behaviour verified + loss scope accepted" (zero loss has NOT been achieved); strict zero-loss rolling upgrade is listed as a future release enhancement feature, not raised as an item in this version, and starting it goes through requirement→ADR→design→review (candidate directions A process-level drain / B transparent bridge+StateStore / C instance stickiness / D maintenance window) | Closed | Maintainer confirmation 2026-10-12; PASS-nf4-rolling-upgrade-accepted-loss-2026-10-12.txt; matrix REQ-NF-4 row moves to pass (pass 16→17, blocked 7→6) | The original failure record FAILCLOSED-nf4-...txt is retained (not passing evidence); UDP measurements only, no extrapolation to TCP/TLS |
| B3-03 | F-15 notify record | fleet-b only received selftest, suspected missed notifications | Rejected (as a defect) | No code change; the evidence file faithfully annotates "notify the first batch only" as designed behaviour and fleet as a protocol stub | Closed | Existing test_fleet_api + raw F-15 notify | Design semantics, not a regression |
| B3-04 | NF-9 / backup drill | After PG restart the config-service's single shared connection does not reconnect automatically (login 500 before restart, 200 after restarting the Deployment, measured 5.25s) | Partially accepted | Registration only in this batch, no change; recommend evaluating connection reconnection / connection pooling later | Pending modification | Two drills measured 500→200 after restart; PASS-nf9 / PASS-backup-restore | Operational observation item; whether to raise it awaits the maintainer |
| B3-05 | NF-5 environment | The TLS certificate is from a test CA (self-signed) | Accept (as a boundary) | REQ-S-2/S-3 are not signed off; the evidence boundary section is annotated "not carrier PKI" | Closed | PASS-nf5 evidence boundary section + UI pki_notice | — |
| B3-06 | as-sut deployment | The product image on bullseye cannot load the native extensions (libssl.so.3 missing, CrashLoop) | Accept | testbed/sim-platform/Dockerfile.product base raised to bookworm (the comment records the OpenSSL 3 fact) | Verified | translation Pod listening on three ports RESIP_RUNTIME_LISTENING + NF-5 all 200 across three transports | Testbed product image only; the release image is handled separately |
| B3-07 | Image loading | kind load of multi-architecture manifest lists reports content digest not found / ImagePullBackOff | Accept (operational means) | postgres:12.22, redis:7-alpine, calico v3.28.2 converted to single architecture (--platform linux/amd64) and then loaded; calico image set to the -kind tag | Verified | The workloads related to the three kind clusters are Running/Completed | No repository file changes; the process is described in the handoff |
| B3-08 | make gate | The batch 2 commit (090312c) brought in ruff non-compliance: test_s1_replay_contract.py formatting, UP041 in test_req_f6_f7, F541 in test_req_f11 | Accept | ruff format on the single file + two equivalence fixes (socket.timeout→TimeoutError; remove the placeholder-less f prefix) | Verified | make gate fully green (1140 passed) | From Python 3.10 onwards the two are the same object; pure formatting/equivalence |
| B3-09 | 2.5 drill | Whether the second-level measured durations of backup/restore can serve as RTO/RTO basis | Rejected (as a commitment) | The evidence only states "order of magnitude measured this time, not a commitment"; customer values are still filled in by the drill party per backup-restore.md §5 | Closed | PASS-backup-restore evidence boundary section | Not to be cited externally as an SLA |
| B3-10 | First restore of the backup drill | PG12 does not support DROP DATABASE WITH(FORCE); the first DROP failed and the restore fell back to the old database | Accept (process correction) | Switched to pg_terminate_backend + a normal DROP, first verifying tables_fresh_db=0 and then restoring | Verified | Second drill: restore rc=0, 0 bytes on stderr, counts consistent | The runbook commands themselves do not use that syntax |
| B3-11 | Close-out site | Whether the fleet-a/fleet-b protocol stubs and the second full stack as-m5b should be cleaned up | Accept (retained) | Kept in kind-as-m5 by default; the handoff explains their purpose and how to clean them up | Closed | This record + the site section of the handoff | Not placed in the repository (/tmp-driven + in-cluster YAML) |
| B3-12 | Working-tree check | .dockerignore is a leftover change from batch 1; docs/handoff/2026-10-12-m8-batch5-prompt.md and docs/intro.md are not files of this batch | Rejected (merged into this batch's commit) | This batch neither changes nor commits them; handed to the maintainer for disposition | Closed | git status already listed in the handoff | Commit splitting is the maintainer's decision |
| B3-13 | Audit append verification | The failed/rolled-back drill INSERTs consumed sequence values (id holes 94/95/96) | Rejected (as an issue) | No change; this is normal PostgreSQL sequence behaviour | Closed | Noted in the PASS-backup-restore evidence | — |
