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

# M8 Batch 3 "kind/sim Evidence" Completion Handoff (2026-10-12)

## 0. Nature and Scope of This Document

- This document is the completion handoff for [`2026-10-12-m8-batch3-prompt.md`](2026-10-12-m8-batch3-prompt.md), paired with the review record
  [`../reviews/m8-batch3-kind-sim-evidence-review-2026-10-12.md`](../reviews/m8-batch3-kind-sim-evidence-review-2026-10-12.md).
- **It signs off no REQ, changes no state in `docs/acceptance/m8-test-plan-matrix.md`, and changes no report.md; it constitutes no capacity/SLA/RPO/RTO commitment.**
- Environment: `dev-win03ib7niepf0`; tools `tools/bin` (kind 0.24.0 / kubectl 1.31.4 / helm 3.16.4).
- **No git write operation was performed**; all changes remain in the work tree, and splitting them into commits is the maintainer's decision.

## 1. Completion Checklist (7/7) and Evidence Triples

| Item | Verdict | Evidence (triple) |
|---|---|---|
| F-15 Real AS Full Stack (incl. NF-10) | verified (PASS) | (verified, docs/acceptance/artifacts/m5/2026-10-12/PASS-f15-distribution-lifecycle-rollback-2026-10-12.txt, 2026-10-12) |
| NF-2 Dual Deployment Isolation | verified (PASS) | (verified, docs/acceptance/artifacts/m5/2026-10-12/PASS-nf2-deployment-isolation-2026-10-12.txt, 2026-10-12) |
| NF-9 Namespace Isolation | verified (PASS) | (verified, docs/acceptance/artifacts/m5/2026-10-12/PASS-nf9-namespace-isolation-2026-10-12.txt, 2026-10-12) |
| NF-4 Rolling Zero Loss | **failure registered (FAILCLOSED, not pass evidence)** | (failure registered, docs/acceptance/artifacts/m5/2026-10-12/FAILCLOSED-nf4-rolling-restart-inflight-loss-2026-10-12.txt, 2026-10-12) |
| NF-5 UDP/TCP/TLS Consistency | verified (PASS) | (verified, docs/acceptance/artifacts/m5/2026-10-12/PASS-nf5-simulator-transport-consistency-2026-10-12.txt, 2026-10-12) |
| 2.5 Backup Restore Drill | verified (PASS, elapsed time is order of magnitude, not a commitment) | (verified, docs/acceptance/artifacts/m5/2026-10-12/PASS-backup-restore-drill-bundled-pg-2026-10-12.txt, 2026-10-12) |
| P0 Defect Fix (found during evidence collection) | verified (PASS) | (verified, docs/acceptance/artifacts/m5/2026-10-12/PASS-config-service-auth-distribution-409-fix-2026-10-12.txt, 2026-10-12) |

Index updated: docs/acceptance/artifacts/m5/README.md (+7 lines, the FAILCLOSED line is marked "**not pass evidence**").

## 2. Summary of Key Results

- **F-15/NF-10**: first batch healthy → auto-applied (order_rev=5) → explicit apply idempotent 200; last batch unhealthy → auto rolled_back (rolled_back_to=1, health check failed); manual rollback after the first batch (rolled_back_to=2). fleet-a genuinely received notify inside the cluster; "notify the first batch only" is by design. fleet is a protocol stub (AS has no notify/bundle receiver).
- **NF-2**: during the delete-and-recreate window of translation, anti-fraud was 42/42 ×200 with unchanged identity.
- **NF-9**: while ns-A had PG stopped and both AS Deployments deleted, ns-B was 58/58 ×200 with 7 Pod identities unchanged; ns-A restored via helm.
- **NF-4**: 350 calls/round ×2 rounds, 347/346 established respectively; timeout_invite 3/4, bye_sip_481 6/7, timeout_bye 4/3, unresolved 10/10. Root cause: single-replica headless handover window + DUM dialog state held only in process memory. **Awaiting maintainer adjudication**.
- **NF-5**: all three rounds over UDP/TCP/TLS gave 200×9, 404×3, 603×3, unresolved=0; TLS used the test CA.
- **2.5**: pg_dump 0.259s / cp 0.143s / drop+create 1.123s / pg_restore 0.704s (rc=0, stderr 0) / config-service restart 5.252s; 12 counters plus three roles consistent; the 8 audit append-only guards all rejected as expected; login 200, rules rows=2, audit continued appending.
- **P0**: distribution in auth mode always returned 409; the redundant idle check was removed (net -10 lines) plus 2 end-to-end regressions.

## 3. Code/File Change List (all uncommitted)

| File | Change | Origin |
|---|---|---|
| services/config-service/src/as_config_service/api.py | removed require_idle_distribution_connection and its 4 call sites (-10 lines) | P0 fix in this batch |
| services/config-service/tests/test_postgres_auth_api_integration.py | +212 lines (PgHarness store extension; 2 real PG/HTTPS/CSRF distribution regressions) | P0 fix in this batch |
| testbed/sim-platform/Dockerfile.product | bullseye→bookworm (OpenSSL 3 factual note) | prerequisite for NF-5 evidence in this batch |
| testbed/e2e/test_s1_replay_contract.py | ruff format pure-format line collapse | gate fix in this batch (non-compliance brought in by the batch 2 commit) |
| platform/tests/test_req_f6_f7_rule_priority_integration.py | except socket.timeout → TimeoutError (equivalent) | same as above |
| platform/tests/test_req_f11_cancel_race_integration.py | removed f-string prefix without placeholders (F541) | same as above |
| docs/acceptance/artifacts/m5/2026-10-12/*.txt (7 new evidence files) | see §1 | this batch |
| docs/acceptance/artifacts/m5/README.md | +7 index lines | this batch |
| docs/reviews/m8-batch3-kind-sim-evidence-review-2026-10-12.md | new | this batch |
| docs/handoff/2026-10-12-m8-batch3-complete-handoff.md | this file | this batch |

Not part of this batch, untouched by this batch: `.dockerignore` (leftover change from batch 1), `docs/handoff/2026-10-12-m8-batch5-prompt.md` (untracked, the next-batch prompt preset by the maintainer), `docs/intro.md` (untracked, origin unknown).

## 4. Verification Results

- `make gate` (2026-10-12, local machine, exit 0): ruff format 546 files already formatted; ruff check All checks passed; mypy Success 90 files; pytest `-m "unit or contract"` **1140 passed, 227 deselected, 11 warnings**.
- `uv run pytest tests/test_evidence_discipline.py -q`: **117 passed**.
- config-service full run (compose PG12.22 :55432, AS_PG_TEST_DSN specified, credentials not committed): **629 passed, 3 skipped** (wal_level=replica / PG version environment limits).
- Raw evidence records are kept in a temporary directory on the execution host (not committed): /tmp/m8b3/ (f15-run4.log, nf2-redrill.log, nf9-redrill.log, nf4.log, nf4-run2.log, nf5.log, drill2/, gate3.log, etc.).

## 5. In-Situ Cluster State

- **kind-as-m5**: ns `as-m5` release `as` (revision 4+, full stack Running after helm upgrade restore, migrate Completed; fleet-a/fleet-b protocol stubs retained); ns `as-m5b` release `asb` retains an independent full stack. Cleanup: `kubectl --context kind-as-m5 delete deploy fleet-a fleet-b -n as-m5`; the whole second full stack can be removed with `helm --kube-context kind-as-m5 -n as-m5b uninstall asb`.
- **kind-as-m71**: ims-sim (scscf/ssbc-north/ssbc-south/uas/call-load) and as-sut (bookworm base image as-sut:dev, single-architecture postgres:12.22 / redis re-hosted image, Calico v3.28.2 local -kind images) are all Running/migrate Completed. The call-load UI is reachable via `kubectl -n ims-sim port-forward svc/ims-sim-ui 8088:8088`.
- Local compose: as-m4b8-dev-postgres-1 (PG12.22 :55432), as-redis-test :6379, as-pg15-test :55434 are still running.

## 6. Items Awaiting the Maintainer

1. **B3-02 NF-4 adjudication**: whether FAILCLOSED becomes a tracked project (StateStore/S-SBC transparent bridge, multi-replica dialog ownership, or maintenance-window operating stance); the matrix stays blocked until adjudicated.
2. **B3-04**: whether config-service not auto-reconnecting after a single-connection PG restart (500 → recovery on restart) becomes a tracked project.
3. **Work tree disposition**: how to split the §3 changes into commits (including the 3 lint/format fixes brought in by the batch 2 commit, the leftover .dockerignore from batch 1, and the two untracked docs files).
4. In the review record's Adjudication section, rows B3-01/02/04 are marked "awaiting maintainer confirmation/adjudication"; please give a final verdict row by row.
5. `docs/handoff/2026-10-12-m8-batch5-prompt.md` is already in the work tree; please confirm its content before the next batch starts.

> **Destination pointer (added 2026-10-13; the five maintainer items above are retained verbatim and unchanged)**: the destinations of the items in this section that have not yet been closed are ——
> **Item 1** (whether B3-02 FAILCLOSED becomes a tracked project as zero-call-loss rolling upgrade enhancement) has been moved to v1.1 as a tracked project, see
> [`../next-release-v1.1-plan.md`](../next-release-v1.1-plan.md) **§3-8** (REQ-NF-4 signs pass in this version on the basis of "accept measured call loss",
> **not** "zero loss achieved"); **items 2 / 4** (B3-04 config-service single-connection reconnect, the final verdicts for the review record Adjudication rows)
> are scheduled into v1.1 together with that section and belong to **§3**; **items 3 / 5** (work tree commit split, unattributed/untracked files such as `batch5-prompt.md`)
> see **§5-6** (the on-site `git status` is authoritative; items are not frozen one by one).
> Any subsequent status inventory, report, handoff, or new-session opening that touches the leftovers of this section must **only cite this pointer**; do not expand them item by item and do not list them again as "maintainer actions".

## 7. Discipline Compliance Declaration

- The main agent wrote no file directly; all file changes were landed via a general-purpose writing subagent and verified item by item with git status/diff; only one writing subagent ran in the same work tree at any time.
- No git add/commit/tag/push/branch; no REQ sign-off, no matrix/report count changes; evidence files contain no credentials/token/cookie; FAILCLOSED is marked "not pass evidence" in the m5 README index.

## 8. Maintainer Adjudication Added 2026-10-12: NF-4 Signed as pass (Measured Call Loss Accepted)

- Adjudication (key points, original wording): the current release accepts this degree of call loss; NF-4 marked pass; the call loss will be addressed in future releases as a feature enhancement.
- Stance: rolling upgrade behaviour verified by measurement + the accepted scope of in-flight call loss (UDP two rounds: 13/14 calls affected, unresolved 10 each) = pass; this is **not** zero loss achieved.
- Landed: PASS-nf4-rolling-upgrade-accepted-loss-2026-10-12.txt (with full mechanism and candidate enhancement directions); the original FAILCLOSED record has the adjudication pointer appended, with the facts retained unchanged; two lines in the m5 README index; the matrix REQ-NF-4 row flipped to pass + an adjudication section appended at the end of the document (pass 16→17, blocked 7→6); the plan.md §0 decision row; review record B3-02 closed.
- "Rolling upgrade zero call loss" is a future-release enhancement feature and is not tracked as a project in this version (same process as FM and call tracing).
- No git write operation was performed after this section was added.
