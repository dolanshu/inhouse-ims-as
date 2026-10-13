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

# M8 test-plan sign-off matrix (Phase C)

> **Source**: `docs/acceptance/test-plan.md` §1–§5 (v1 scope).
> **Traceability note**: this matrix maps onto the sections of the M8 task draft's appendix (that file is a REQ checklist appendix and is not modified by this exercise;
> note: no `M8任务草稿.md` file was found in this repository, so traceability is based on the test-plan section numbers `§1.1–§5`).
> **No claim of all green**: this matrix is not a "all REQs green" declaration; `signed_by` on every row is `maintainer pending signature`,
> and M8 may only be declared all green once the matrix has no unexplained v1 `open` items and maintainers confirm in the M8 exit review (`docs/reviews/m8-exit-review-*.md`).
> `blocked` must point to `docs/plan.md` §5 (an O/D number) or v1.1; `n-a` must carry a rationale and is never recorded as pass.
> While maintainers are absent, this matrix records only verifiable evidence and self-adjudicated status; it does not replace maintainer sign-off.

Basis plan: `docs/handoff/2026-10-06-m8-release-candidate-plan.md` §4 Phase C + §3.1 scope.

## Evidence baseline (measured locally, 2026-10-06, not fabricated)

- `make gate` → **978 passed, 2 skipped** (exit 0). Both skips are in
  `test_derived_baseline.py`: the S1 baseline has no Route header / no Record-Route and needs M2 probe recapture.
- `uv run pytest platform/tests/test_resip_runtime_log_contract.py -q` → **13 passed**.
- `uv run pytest platform/tests/test_e1_contract_resip_runtime_full.py -m contract -q` → **4 passed**.
- `uv run pytest platform/tests/test_m7_forward_two_leg_integration.py platform/tests/test_req_f4_sdp_identity_integration.py -m integration -q` → **4 passed**.
- `uv run pytest platform/tests/test_d10_product_recovery_integration.py -q` → **1 passed**.
- `uv run pytest testbed/simulators/tests/test_derived_baseline.py -m contract -q` → **10 passed, 2 skipped** (same as above).
- `uv run pytest tests/test_version_consistency.py -q` → **9 passed**; `tests/test_workspace_layout.py` → **32 passed**.
- `python3 scripts/check_adr_annotations.py` → **checked 69 files, clean**.
- `make chart-check` → **chart-check: OK** (engineering-shape evidence, not used as a REQ pass basis).
- NF-6 grep: `rg -il 'rtp|G.711|G.729|dtmf|transcod' apps/ platform/src/ services/` has a single hit in
  `services/console/web/console.js`, which on inspection is a false positive on the `rtp` substring inside the DOM id `distributionStartPanel` (Start**P**anel);
  there is no real RTP/media implementation; inside `platform/src` the `media/seam` occurrences are only comment wording (call_checkpoint stores no media, the ingress seam-switch comment).
- NF-7 grep: `rg -il 'cdr|批价|计费|billing' apps/ platform/src/ services/` → **no hits**.
- NF-8 grep: `rg -il 'lawful_intercept|\bIRI\b|intercept' apps/ platform/src/ services/` → **no hits**;
  see also `docs/architecture/hld.md` for the scope exclusions (single-tenant on-prem boundary: media/CDR/LI/Diameter Sh excluded).
- NF-5 grep: `rg -n 'is_intranet|is_extranet|network_mode' apps/` → **no hits (exit 1)**.
- NF-10 grep: no configuration-loading logic of the `import git / from git / github.com / gitlab / git clone-pull` kind;
  the only occurrence of `git` is a comment line in `services/config-service/src/as_config_service/change_order.py:4`
  ("instead of GitOps" explanatory text, not code logic).
- NF-11 grep: `rg -n 'VERSION=' platform/ apps/ services/` → **no hits** (no component owns a VERSION).
- NF-14: `deploy/alerts/as-alerts.yaml` exists (with rules such as 5xx>1%, a surge in active_calls, certificate expiry in 30 days; `make chart-check` covers the template shape).
- NF-15: `docs/requirements/req-nf-15-testbed-performance.md` exists; ADR-0014's `Responds to REQ` points at REQ-NF-15;
  dev-host measurements are in `docs/acceptance/m6-o1-measurement-report-2026-10-05.md` (not an SLA).

## §1 Functional sign-off (REQ-F-*)

| req_id | test_plan_ref | milestone | phase | evidence | status | signed_by |
|---|---|---|---|---|---|---|
| REQ-F-1 | §1.1 basic call, 14 messages | M7 | C | `test_e1_contract_resip_runtime_full.py -m contract` 4 passed; `test_m7_forward_two_leg_integration.py` (one of the 4 integration passed); `test_derived_baseline.py -m contract` 10 passed. The engineering slice passes; formal REQ sign-off awaits the maintainer M8 exit review | open | maintainer pending signature |
| REQ-F-2 | §1.1 the two legs have independent Call-IDs | M7 | C | The E1 contract suite passes inside `make gate` (978 passed); REQ-level sign-off of the C_in≠C_out / within-leg consistency assertions awaits the M8 review | open | maintainer pending signature |
| REQ-F-3 | §1.1 Request-URI translation | M7 | C | The S1 translation scenario of `test_derived_baseline.py` (+8613800138000→013800138000) is within the 10 passed; REQ sign-off awaits the M8 review | open | maintainer pending signature |
| REQ-F-4 | §1.1 SDP passthrough is byte-identical | M7 | C | `test_req_f4_sdp_identity_integration.py` (one of the 4 integration passed) + D11 fixtures; `plan.md` §5.2 D11 states explicitly that "formal pass for REQ-F-4 still requires M8 review + a broader corpus, and must not be declared green on its own" | open | maintainer pending signature |
| REQ-F-5 | §1.1 Route/Record-Route | M7 | C | 2 skipped in `test_derived_baseline.py`: the S1 baseline has no Route header and no Record-Route, "M2 probe recapture required". Acceptance of real product-path behaviour is tracked under O3; not signed as pass before recapture | open | maintainer pending signature |
| REQ-F-6 | §1.2 no match 404 | M7 | C | Kernel 5.1 decide matrix (case 5 NO_MATCH→404) is within `make gate` 978 passed; REQ sign-off awaits the M8 review | open | maintainer pending signature |
| REQ-F-7 | §1.2 reject 603 + priority | M7 | C | Kernel 5.1 decide matrix (cases 3/7 block takes priority) is within `make gate` 978 passed; REQ sign-off awaits the M8 review | open | maintainer pending signature |
| REQ-F-8 | §1.3 CANCEL three branches | M7 | C | M7 call-control cases such as `test_call_controller.py` are within `make gate` 978 passed; REQ-level sign-off of the three branches awaits the M8 review (the branch coverage conclusion is per the review; this document does not claim all branches are green here) | open | maintainer pending signature |
| REQ-F-9 | §1.3 in-dialog routing | M7 | C | M7.3 context restoration engineering slice (`restore_from_checkpoint` / `route_in_dialog_bye`, see plan §5.2 D10 TODO); REQ sign-off of the re-INVITE/UPDATE/BYE comparison scenarios awaits the M8 review | open | maintainer pending signature |
| REQ-F-10 | §1.3 486/480/408 passthrough | M7 | C | The D9 product adapter's 486 mapping engineering issue is resolved (plan §5.2 D9); REQ sign-off of "passthrough without rewriting the code" plus non-2xx cleanup awaits the M8 review | open | maintainer pending signature |
| REQ-F-11 | §1.3 final-response race, two branches | M7 | C | D9 forking/final-response race coverage belongs to M8 acceptance (plan §5.2 D9); REQ sign-off awaits the M8 review | open | maintainer pending signature |
| REQ-F-12 | §1.4 console rule CRUD (M4: callee + prefix) | M4/M4b | C | M4 engineering close-out; dev HTTPS evidence per `docs/acceptance/m4b-8-runbook.md`; plan §5.4 states that formal all-green for §1.4 belongs to M8 or is signed off separately by maintainers | open | maintainer pending signature |
| REQ-F-13 | §1.4 Call-ID trace query | M4/M4b | C | M4b-7.4: no trace store/API, M4b-8 marks it BLOCKED (test-plan header note + `m4b-8-runbook.md`). Points to plan §5.4; live environment evidence belongs to Phase D | blocked | maintainer pending signature |
| REQ-F-14 | §1.4 approval flow | M4/M4b | C | M4 engineering close-out (create → pending approval → approve/reject + reason, self-approve forbidden); formal all-green belongs to M8 (plan §5.4 §1.4 row), awaiting maintainer sign-off | open | maintainer pending signature |
| REQ-F-15 | §1.4 canary distribution/rollback (control plane) | M4/M4b | C | M4 has delivered inventory + notify + testbed probe + browser distribution start; **full AS stack supplementary testing** is deferred (plan §5.4), see the 5.4-F-15 row below. Not signed as pass as a whole | blocked | maintainer pending signature |
| REQ-F-16 | §1.5 translation decision chain | M7 | C | The decide translation cases pass inside gate; trace correlation (numbers/rules ID/version before and after translation) depends on the F-13 trace; REQ sign-off awaits the M8 review | open | maintainer pending signature |

## §2 Non-functional sign-off (REQ-NF-*)

| req_id | test_plan_ref | milestone | phase | evidence | status | signed_by |
|---|---|---|---|---|---|---|
| REQ-NF-1 | §2 kill/restart does not lose state | M7 | C/D | The engineering harness is in `test_d10_product_recovery_integration.py` (1 passed) and similar. Customer K8s live is a **restriction** (2026-10-07: no customer cluster testing before Close): [`m8-environment-evidence.md`](m8-environment-evidence.md) D-2. Cannot be signed as pass | blocked | maintainer pending signature |
| REQ-NF-2 | §2 dual Deployment isolation | cross-cutting | C | Architecture ADR-0002 (a separate process/Deployment per use case); `make chart-check` OK (template shape). Live verification that killing translation does not affect anti-fraud awaits a K8s environment (Phase D); not signed as pass | open | maintainer pending signature |
| REQ-NF-3 | §2 HPA scaling + capacity figures | M5 | B/C | **Blocked**: the test-plan carries fixed capacity figures (a 500 active_calls threshold, 1000 concurrent, 3→≥5 replicas), which conflicts with AGENT §2 "no capacity figures published before M6". Points to plan §5.1 **O1**: the maintainer's target adjudication is still open, and the M6 O1 report is a non-SLA measurement. Awaiting maintainers to rewrite the acceptance criterion or mark it N/A | blocked | maintainer pending signature |
| REQ-NF-4 | §2 zero-loss rolling upgrade | M5 | C/D | Kernel 5.5 draining unit tests are within gate 978 passed; the M7 process-shell harness is an engineering slice. **M8 batch 3 live has been verified** (kind-as-m71, UDP 5cps×70s=350 calls/round ×2 rounds, rollout restart at second 12: 200 OK 347/346; timeout_invite 3/4, bye_sip_481 6/7, timeout_bye 4/3, unresolved 10 each; mechanism = headless single-replica switchover window + DUM dialog state only in process memory). **Maintainer adjudication on 2026-10-12: the current release accepts this level of call loss and signs it as pass under "measured behaviour verified + loss scope accepted" (not "zero loss achieved"); strict zero-call-loss rolling upgrade is listed as a future release enhancement feature and is not started in this version**. Evidence: artifacts/m5/2026-10-12/PASS-nf4-rolling-upgrade-accepted-loss-2026-10-12.txt; raw record FAILCLOSED-nf4-rolling-restart-inflight-loss-2026-10-12.txt | pass | maintainer sign-off 2026-10-12 |
| REQ-NF-5 | §2 simulator neutrality | cross-cutting | C | `rg 'is_intranet\|is_extranet\|network_mode' apps/` has no hits (the code has no internal/external network branch); verifying consistent behaviour with a different simulator (Kamailio) awaits a sim environment; REQ sign-off awaits the M8 review | open | maintainer pending signature |
| REQ-NF-6 | §2 no media plane implementation | cross-cutting | C | The production-code grep is in the header note: no RTP/G.711/G.729/DTMF/transcoding implementation (the only hit is a false positive on a console.js DOM id substring); seam exists only in comments. This non-goal item takes "absence" as its basis for passing | pass | maintainer pending signature |
| REQ-NF-7 | §2 trace retention + no billing | cross-cutting | C | Half of it holds — there is no CDR/batch pricing/billing implementation (grep has no hits); but trace query depends on F-13 (plan §5.4 BLOCKED), the retention period in days awaits the O4 freeze, and cleanup-task verification is undecided. Points to plan §5.4 + §5.1 **O4**, belongs to Phase C (criterion) / D (live) | blocked | maintainer pending signature |
| REQ-NF-8 | §2 no LI implementation | cross-cutting | C | The production-code grep has no `lawful_intercept/IRI/intercept` hits; the HLD states explicitly that LI comes from the network and is outside our delivery boundary. This non-goal item takes "absence" as its basis for passing | pass | maintainer pending signature |
| REQ-NF-9 | §2 namespace isolation | M5 | B/C | `make chart-check` OK (separate namespace template shape, an engineering slice, not a REQ pass); live fault isolation (a downed Redis / crashed AS must not affect the other namespace) awaits a cluster environment. See the dedicated row below for the D12/O5 conditions | open | maintainer pending signature |
| REQ-NF-10 | §2 control plane: draft → approval → distribution → rollback → audit | M4/M4b | C | The config-service suite (change_order/distributor/audit store) is within `make gate` 978 passed; the code has no git/github/gitlab configuration-loading logic (see the header note); `make chart-check` covers the template shape. Live canary distribution/rollback follows F-15 real AS (Phase D); not signed as pass | open | maintainer pending signature |
| REQ-NF-11 | §2 VERSION uniqueness | cross-cutting | C | `tests/test_version_consistency.py` 9 passed; `rg 'VERSION=' platform/ apps/ services/` has no hits. The mechanism holds; the final sign-off of release consistency follows Phase E (VERSION/CHANGELOG) | pass | maintainer pending signature |
| REQ-NF-12 | §2 uv workspace | cross-cutting | C | `tests/test_workspace_layout.py` 32 passed; `[tool.uv.workspace]` exists in `pyproject.toml`. The mechanism holds | pass | maintainer pending signature |
| REQ-NF-13 | §2 observability: metrics/traces/JSON logs | M5 | B/C | `test_resip_runtime_log_contract.py` 13 passed (a slice of the timestamp/level/trace_id/call_id/direction/method field contract); the decide/telemetry kernel (5.4) is inside gate. Prometheus/Grafana live collection and span-chain verification await an environment (Phase D); not signed as pass | open | maintainer pending signature |
| REQ-NF-14 | §2 alert rules | M5 | B/C | `deploy/alerts/as-alerts.yaml` exists (5xx>1%, surge in active_calls, certificate in 30 days, etc.); `make chart-check` OK is shape evidence. Real Alertmanager firing verification awaits an environment (the notification channel is a continuation of the frozen M2 item); not signed as pass | open | maintainer pending signature |
| REQ-NF-15 | §2 testbed performance harness | M6 | C | The PRD + `docs/requirements/req-nf-15-testbed-performance.md` exist, ADR-0014's responded-to REQ points at REQ-NF-15 (D8 is closed); dev-host batches are in the m6-o1 report (not an SLA). The production multi-replica saturation point / HPA thresholds / `performance` blocking gate stay open before M8; the M6 O1 maintainer target adjudication is still open (plan §5.1 O1) | open | maintainer pending signature |
| REQ-NF-16 | §2 version lifecycle and EOL policy | cross-cutting | C | Evidence one (the technical decision has been made): `docs/architecture/adr/0027-version-lifecycle-and-eol.md` Status: accepted (line 3) and "Responds to REQ: REQ-NF-16" (line 6); ADR-0027 is accepted. Evidence two (the acceptance evidence chain is not closed): `docs/acceptance/test-plan.md` has acceptance criteria only for REQ-NF-1 through REQ-NF-15 (ending at line 322), and **no REQ-NF-16 acceptance criteria section**; the status block of `docs/product/version-lifecycle.md` states "this document has not yet been reviewed" (line 10) and **there is currently no review record**. Search scope: `docs/architecture/adr/0027-version-lifecycle-and-eol.md` (search Status / Responds to REQ), `docs/acceptance/test-plan.md` (search REQ-NF-16), `docs/product/version-lifecycle.md` (search review / review record), the `docs/reviews/` directory (search for version-lifecycle-related review files; no hits) | open | maintainer pending signature |

## §3 Security sign-off (REQ-S-*)

| req_id | test_plan_ref | milestone | phase | evidence | status | signed_by |
|---|---|---|---|---|---|---|
| REQ-S-1 | §3 whitelist | cross-cutting | C | Whitelist logic exists (`platform/src/as_platform/sip/ingress.py` and other files containing allowlist/peer references, covered by gate 978 passed); whitelist changes go through approval (linked to F-14). REQ sign-off awaits the M8 review (M2 REQ-S-* engineering coverage + maintainer M2 exit) | open | maintainer pending signature |
| REQ-S-2 | §3 AS↔S-SBC TLS + operator PKI | M2 | C/D | Local TLS engineering tests are inside gate. Operator PKI + external-network S-SBC is a **restriction** (2026-10-07: no joint debugging before Close): [`m8-environment-evidence.md`](m8-environment-evidence.md) D-1. Cannot be signed as pass | blocked | maintainer pending signature |
| REQ-S-3 | §3 lossless certificate rotation | M2 | C/D | The operator certificate rotation window on a real peer is a **restriction** (2026-10-07, same as D-1). Rotation on a test certificate does not substitute for this item. Cannot be signed as pass | blocked | maintainer pending signature |
| REQ-S-4 | §3 RBAC + tamper-proof audit | M4/M4b | C | The config-service audit/authentication suite (`test_audit_store.py`, `test_auth.py`, etc.) is within `make gate` 978 passed; M4b-6b is an engineering slice. plan §5.4 states that formal all-green for REQ-S-4 belongs to M8 or is signed off separately by maintainers; pending signature | open | maintainer pending signature |

## §4 Governance sign-off (REQ-G-*)

| req_id | test_plan_ref | milestone | phase | evidence | status | signed_by |
|---|---|---|---|---|---|---|
| REQ-G-1 | §4 feature gating, two states | cross-cutting | C | Kernel 5.3 two-state unit tests are inside gate; `check_adr_annotations.py` 69 files clean (no unannotated architectural code). Recorded as pass-mechanism: reviewing removal conditions per change still requires maintainers to do it per PR | pass | maintainer pending signature |
| REQ-G-2 | §4 PR checklist + REQ traceability | cross-cutting | C | The review-record convention exists (each record under `docs/reviews/` references a REQ/ADR number, such as the d8/m5 series); the mechanism holds. Per-change traceability still requires maintainer confirmation at each review; recorded as pass-mechanism | pass | maintainer pending signature |
| REQ-G-3 | §4 ADR annotation scan blocking | cross-cutting | A/C | `check_adr_annotations.py` clean (69 files); the four steps of `make gate` exclude the AST scan, consistent with the test-plan criterion (the scan is triggered separately by `make gate-strict`). The mechanism currently holds; recorded as pass-mechanism | pass | maintainer pending signature |
| REQ-G-4 | §4 gate green + gate blocking + pre-commit | cross-cutting | C | `make gate` exit 0 (978 passed, 2 skipped, see the header note). The terminal state of the inter-layer blocking and pre-commit semantics belongs to Phase A (A-4/A-6) confirmation; the local gate itself is green, recorded as pass | pass | maintainer pending signature |

## §5 Kernel rows (test-plan §5, cited from gate, not re-proved)

| req_id | test_plan_ref | milestone | phase | evidence | status | signed_by |
|---|---|---|---|---|---|---|
| KERNEL-§5 | §5.1 decide matrix / §5.2 StateStore contract / §5.3 gating two states / §5.4 telemetry not blocking / §5.5 draining (unit/contract level) | M2/M3 | C | `make gate` 978 passed, 2 skipped (2026-10-06). The M3 contract replay is already in gate; the 2 skipped are the Route/Record-Route probe gap (see F-5), not hidden | pass | maintainer pending signature |

## §5.4 Supplementary test rows (plan §5.4, does not block the M4 close-out, blocks any all-green REQ claim)

| req_id | test_plan_ref | milestone | phase | evidence | status | signed_by |
|---|---|---|---|---|---|---|
| 5.4-F-13 | §1.4 REQ-F-13 live trace (M4b-7.4) | M4/M4b→ integrated stack | C/D | Same source as REQ-F-13: no trace store/API (test-plan header note BLOCKED). Live trace query evidence belongs to Phase D (environment + known Call-ID, to be filled in); nothing may be recorded as passed before then | blocked | maintainer pending signature |
| 5.4-F-15真AS | §1.4 REQ-F-15 full AS stack (not testbed notify/health) | after M7 integration | C/D | M4 only delivered inventory + notify + testbed probe + browser distribution start; the real AS full-stack staged distribution/health/automatic + manual rollback awaits supplementary testing after integration (Phase D environment, to be filled in). Points to plan §5.4 | blocked | maintainer pending signature |

## Conditional / environmental / explicitly excluded rows

| req_id | test_plan_ref | milestone | phase | evidence | status | signed_by |
|---|---|---|---|---|---|---|
| D12/O5-HA | §2 NF-1/NF-9/NF-10 (production Redis/PG HA) | M5 | B/C | ADR-0026 accepted; the Helm `stateStores` skeleton has landed. **Production** Redis/PG HA is a **restriction** (2026-10-07): there is no customer production topology before Close. kind bundled state is not this item. Cannot be signed as pass | open | maintainer pending signature |
| ADR-0008-演练 | architecture ADR-0008 cross-site | — | C/D/E | The cross-site switchover drill is a **restriction** (2026-10-07): no customer/production dual site before Close. Cannot be signed as pass. See [`m8-environment-evidence.md`](m8-environment-evidence.md) | blocked | maintainer pending signature |
| D6-testbed验收 | outside test-plan (D6) | — | D | plan §5.2 D6: whether the testbed must support customer acceptance in v1; the architecture defers it to v1.1, awaiting a maintainer decision (v1 vs v1.1). Belongs to Phase D (D-3) | blocked | maintainer pending signature |
| NA-主叫/正则 | §1.4 F-12 four-dimensional UI (caller ID / regex) | — | — | plan §5.4: it belongs to **v1.1**; M4 live covers only callee + prefix. Not accepted in M8, never recorded as pass | n-a | maintainer pending signature |
| NA-PM/AM/UM | outside §2 NF-13/NF-14 | — | — | plan §5.3: the full product requirements have not been filled in; M8 only contains the REQ-NF-13/14 engineering slices. Not accepted in M8 | n-a | maintainer pending signature |
| NA-D1 | global (Python 3.10 EOL) | — | — | plan §5.2 D1: a risk register entry, not a default blocker for RC. The M8 matrix does not accept runtime version migration | n-a | maintainer pending signature |
| NA-D10ext | outside §2 NF-1 (mid-transaction crash / owner-CAS extremes) | — | — | plan §5.2 D10: "do not extend D10 to mid-transaction recovery during a crash; do not extend to Redis failover extreme scenarios". Not accepted in M8 | n-a | maintainer pending signature |

## Status tally

- pass: 9 (NF-6, NF-8, NF-11, NF-12, G-1, G-2, G-3, G-4, KERNEL-§5; of which G-1/G-2/G-3 are pass-mechanism and still require maintainer review per change)
- fail: 0
- blocked: 12 (F-13, 5.4-F-13, F-15, 5.4-F-15真AS, NF-1, NF-3, NF-4, NF-7, S-2, S-3, ADR-0008-演练, D6-testbed验收). Of these, NF-1, S-2, S-3 and ADR-0008-演练 were marked on 2026-10-07 as pre-Close **restrictions** (not done on a real customer network); the status term is still blocked and they cannot be signed as pass. D12/O5-HA is still counted under open, and is likewise a restriction.
- n-a: 4 (caller ID / regex in v1.1, PM/AM/UM, D1, the D10 extreme extension; all with rationale, never recorded as pass)
- open: 24 (F-1/2/3/4/5/6/7/8/9/10/11/12/14/16, NF-2/5/9/10/13/14/15, S-1/S-4, D12/O5-HA; each has engineering evidence plus an explicit rationale for awaiting maintainer M8 exit review sign-off, with no unexplained open)

**Items not claimed green**: all 24 open and 12 blocked (including all live-environment tail items S-2/S-3, NF-1 live, F-13 live, F-15 real AS, NF-3 capacity criterion, NF-4 real-traffic rolling upgrade, NF-7 trace/O4, the ADR-0008 drill, D6) are not claimed green;
the 4 n-a items are explicitly excluded. **No claim of all green**, pending maintainer confirmation in the M8 exit review.

---

## M8 N2 countersignature result (2026-10-12; the body rows are kept unmodified, this section registers signature-field entries and status changes)

> **Authorization source**: on **2026-10-12 maintainers explicitly authorized the agent to countersign** the nine written M8 N2 adjudications
> (source: `docs/handoff/2026-10-07-m8-next-step-plan.md` §N2; the authorization record is at
> [`../handoff/2026-10-12-m8-n2-countersign-record.md`](../handoff/2026-10-12-m8-n2-countersign-record.md)).
> **This section is not a maintainer's own signature**: every item is marked "agent countersignature" with its basis attached, for traceability.

### Countersignature entries / change overview

| # (N2) | Row affected in this matrix | Action | Basis |
|---|---|---|---|
| **5** | `D6-testbed验收` (body `:119`) | status changed from `blocked` to terminal `n-a`, rationale: D6 testbed customer acceptance is **deferred to v1.1** (not accepted in this cycle, never recorded as pass); `signed_by` filled with "agent countersignature (maintainer authorization dated 2026-10-12)" | **D-3** of [`m8-environment-evidence.md`](m8-environment-evidence.md): option (a) of the follow-up either/or, "accept the recommendation → D-3 is closed and the D6 row is handled as v1.1 (matrix `D6-testbed验收` moves to terminal state, with rationale)" |
| **6** | `REQ-NF-3` (body `:67`) | status changed from `blocked` to `n-a`, rationale: fixed capacity figures conflict with `AGENT.md` §2 "no capacity figures published before M6", and the **O1 target is still not published**; `signed_by` same as above | The rationale column carried by that body row; the value of `plan.md` §5.1 **O1** is still open (on 2026-10-12 only an "internal engineering target lower-bound baseline" was landed, not a target value) |
| **7** | `NA-主叫/正则`, `NA-PM/AM/UM`, `NA-D1`, `NA-D10ext` (body `:120`–`:123`) | **Confirm the four exclusions**: `signed_by` changes from "maintainer pending signature" to "agent countersignature (maintainer authorization dated 2026-10-12)"; status stays `n-a` (**never recorded as pass**) | The rationale column carried by each row (pointing respectively to `plan.md` §5.4, §5.3, §5.2 D1, §5.2 D10) |

### Update to the count criterion following this change (the original counts are kept unmodified; only the new values are registered here)

- **blocked: 12 → 10** (`NF-3` and `D6-testbed验收` each moved to `n-a`)
- **n-a: 4 → 6** (adding `NF-3` and `D6-testbed验收`; both **carry a rationale and are never recorded as pass**)
- open 24 / pass 9 / fail 0 **unchanged**

### Boundaries (no excessive conclusions may be drawn from this section)

1. This section handles **only** the parts of N2 items 5 / 6 / 7 that land in this matrix; the authoritative text of the other six N2 items is elsewhere — see the full countersignature record.
2. `NF-3` moving to `n-a` **does not mean** REQ-NF-3 is abandoned — per the G5 adjudication, REQ-NF-3 **remains applicable and blocked**;
   what moves to `n-a` is only the **acceptance criterion** of this one matrix row (the fixed numeric assertion conflicts with `AGENT.md` §2),
   and the adjudication "do not record an entire requirement as N/A" remains in force.
3. **M5 REQ level still fails; M8 is still "RC ready, awaiting exit sign-off"** (the last sentence of the N2 original text); this section does not change that conclusion.
4. This matrix **still does not claim all green**.

---

## M8 N3 execution result (later on 2026-10-12; the body rows and the "status tally" are kept unmodified, this section registers only the countersignature result and the count changes)

> **Authorization source**: the maintainer's 2026-10-12 instruction "the B1 capacity target value + N3 of B5 …… complete everything else,
> make the judgement yourself, execute, don't ask" — N3 falls under it. The N3 criterion comes from
> [`2026-10-07-m8-next-step-plan.md`](2026-10-07-m8-next-step-plan.md) §N3:
> "for rows in the matrix whose evidence is already aligned …… the signature note reads 'engineering evidence accepted'; do not mark an entire test-plan sentence as green".
>
> **This section is not a maintainer's own signature**: all 7 row signatures uniformly read "agent countersignature (maintainer authorization dated 2026-10-12)".
> The candidate rows are the 7 rows named in the N3 original text (F-1, F-2, F-3, F-6, F-7, F-12, F-14), executed after checking the current evidence row by row.

### Countersignature entry overview (7 rows, open → pass)

| req_id | Signature note (scope of the "engineering evidence accepted") | Basis (current evidence as of 2026-10-12) |
|---|---|---|
| **REQ-F-1** | Engineering evidence accepted: e2e Wave 1 (5 final-state assertions) + Wave 2 (3 normalized-skeleton comparisons) + E1 contract + `make gate-native` all green. **The 14 header-by-header comparisons are still not implemented**, so this sign-off **does not constitute full sign-off of REQ-F-1** (the gap continues to be tracked in [`2026-10-11-wave2-replay-register.md`](2026-10-11-wave2-replay-register.md)) | `(verified, 2026-10-11/PASS-e2e-2026-10-11.txt, 2026-10-11)`; `(verified, 2026-10-11/PASS-gate-native-2026-10-11.txt, 2026-10-11)` |
| **REQ-F-2** | Engineering evidence accepted: Wave 2 `test_e2e_s1_replay_second_leg_starts_a_new_call_id` (C_in ≠ C_out) + E1 contract + `test_m7_forward_two_leg_integration.py` | same as above |
| **REQ-F-3** | Engineering evidence accepted: e2e E2E-SIP-1 outbound-leg user number contains the translation result + the S1 translation scenario of `test_derived_baseline.py` + `test_product_path.py` T1 | same as above |
| **REQ-F-6** | Engineering evidence accepted: kernel 5.1 decide matrix case 5 (NO_MATCH→404, inside `make gate`) + e2e E2E-SIP-2 (404) | same as above |
| **REQ-F-7** | Engineering evidence accepted: decide matrix cases 3 / 7 (block takes priority, inside `make gate`) + e2e E2E-SIP-3 (603) | same as above |
| **REQ-F-12** | Engineering evidence accepted: M4 engineering close-out + dev HTTPS evidence (`m4b-8-runbook.md`). **Scope = callee + prefix** (caller ID / regex are `n-a`, deferred to v1.1) | the evidence column of that body row |
| **REQ-F-14** | Engineering evidence accepted: M4 engineering close-out (create → pending approval → approve/reject + reason, self-approve forbidden) + the config-service suite inside `make gate` | the evidence column of that body row |

### Update to the count criterion following this change (the original counts are kept unmodified; only the new values are registered here)

- **pass: 9 → 16** (adding F-1 / F-2 / F-3 / F-6 / F-7 / F-12 / F-14)
- **open: 24 → 17** (the remaining 17 rows match the N4 stop-line list row by row: F-4 / F-5 / F-8 / F-9 / F-10 / F-11 / F-16, NF-2 / NF-5 / NF-9 / NF-10 / NF-13 / NF-14 / NF-15, S-1 / S-4, D12/O5-HA)
- blocked 10 / n-a 6 / fail 0 **unchanged**

### Boundaries (no excessive conclusions may be drawn from this section)

1. **Not a single character of open 24 / blocked 12 in `report.md` §0.5 has been changed** — the matrix's counts are the matrix's own criterion (the same discipline as the N2 countersignature section).
2. **It does not claim that an entire test-plan sentence is green** — the N3 original criterion; 17 open rows + 10 blocked rows remain.
3. **"Engineering evidence accepted" ≠ REQ-level acceptance passed ≠ milestone sign-off** — M5 REQ level still fails and M8 is still "RC ready, awaiting exit sign-off"; the M8 final review confirmation field is left blank and no tag is made.
4. **The N4 stop line was not crossed** — 16+1 unchanged pass rows; not a single `- [ ]` in `test-plan.md` was ticked (the full 14 items of REQ-F-1 remain open).
5. **The sign-off scope of F-12 / F-14 is limited to callee + prefix** — caller ID / regex remain `n-a` (v1.1).

---

## Major-gap adjudication: F-13 / 5.4-F-13 / NF-7 move to v1.1 (2026-10-12; the body rows are kept unmodified, this section registers the adjudication)

> **Authorization source**: the maintainers' **2026-10-12 adjudication** "there is no time left, a major gap! Note it in the documents, delay it to V1.1 - as a feature".
> **This section is not a rewrite of the body**: the three body rows (REQ-F-13 `:56`, 5.4-F-13 `:110`, REQ-NF-7 `:71`) are kept unmodified,
> and this section registers only the adjudication result for status / signed_by and the count changes, following the append-only discipline of N2 / N3.

### Row-by-row adjudication (three rows blocked → terminal n-a)

| Matrix row (body line number) | Original status | New status | Rationale | signed_by |
|---|---|---|---|---|
| REQ-F-13 (body `:56`) | `blocked` | **`n-a`** | Major gap (a regression against the POC baseline), delayed to v1.1 as a feature; not accepted in this cycle, never recorded as pass | maintainer 2026-10-12 |
| 5.4-F-13 (body `:110`) | `blocked` | **`n-a`** | same as above | maintainer 2026-10-12 |
| REQ-NF-7 (body `:71`) | `blocked` | **`n-a`** | same as above | maintainer 2026-10-12 |

**Basis for the major-gap determination**: the capability existed as early as the POC — `migration/triage.md` classified `observability/tracing.py` as "the product capability survives, the in-process ring does not", while the product-level implementation (PG trace store + API + retention cleanup) is **still zero**, which is a functional regression relative to the POC baseline; root cause = from M4 onwards it was mistakenly placed into the "supplementary testing" framework + it had no owner across milestones + RC plan §3.1 excluded it from v1. When v1.1 starts it goes through the new feature process (requirement → ADR → design → review, the same pattern as FM's P6 clarification).

### Update to the count criterion following this adjudication (the original counts are kept unmodified; only the new values are registered here)

- **blocked: 10 → 7** (F-13, 5.4-F-13 and NF-7 each moved to `n-a`; remaining: F-15, 5.4-F-15真AS, NF-1, NF-4, S-2, S-3, ADR-0008-演练)
- **n-a: 6 → 9** (adding F-13, 5.4-F-13 and NF-7; all three carry a rationale and are never recorded as pass)
- pass 16 / open 17 / fail 0 **unchanged**

### Boundaries (no excessive conclusions may be drawn from this section)

1. **"n-a" ≠ abandonment** — when v1.1 starts it goes through the new feature process (requirement → ADR → design → review, the same pattern as FM's P6 clarification); the values of O4 (10-day configurable) / D5 (in-cluster PostgreSQL) are unchanged and land with that feature.
2. **For F-16, only the non-trace part is signed; the trace-correlation part is not** (the F-16 body row text is kept unmodified).
3. This adjudication **signs off no other row and does not change the `report.md` counts**.
4. The root-cause record (the POC `observability/tracing.py` was classified as a surviving product capability with zero implementation; from M4 onwards it entered the "supplementary testing" framework by mistake) has been written into [`../plan.md`](../plan.md) §5.4 and the §0 decision record.
5. **No git write operation was performed.**

---

## Additional adjudication on 2026-10-12: REQ-NF-4 signed as pass under "accept the measured call loss" (M8 batch 3)

**Maintainer adjudication on 2026-10-12 (key points verbatim)**: the current release can accept a loss of this magnitude; persist the analysis; mark NF-4 as pass; the call loss becomes an enhancement feature in future releases.

- The REQ-NF-4 body row has been updated from `blocked` to `pass` (maintainer sign-off). The acceptance criterion = **rolling-upgrade measured behaviour verified + the measured scope of in-flight call loss explicitly accepted**; it is **not** "zero loss achieved".
- Measured scope (two independent reproductions, kind-as-m71, UDP, 350 calls/round): 13/14 calls affected (3.7%/4.0%) = INVITE timeout 3/4 + in-flight dialog teardown unresolved 10/10 (bye_sip_481 6/7, timeout_bye 4/3). Mechanism: the single-replica headless switchover window (the UDP black hole with no answer) + reSIProcate DUM dialog state residing only in process memory (no serialize/deserialize API, so an in-flight BYE reaching the new process gets a 481 or a timeout).
- **"Zero call loss on rolling upgrade" is registered as an enhancement feature for future releases**: it is not started, defined, or implemented in this version; when started it goes through the new feature process (requirement → ADR → design → review, the same pattern as FM (P6) and call tracing (F-13/NF-7)). Candidate directions (process-level drain, S-SBC transparent bridge + StateStore, instance stickiness, maintenance-window criterion) are in the PASS evidence and batch 3 review record B3-02.

### Update to the count criterion following this adjudication (the original counts are kept unmodified; only the new values are registered here)

- **pass: 16 → 17** (REQ-NF-4)
- **blocked: 7 → 6** (remaining: F-15, 5.4-F-15真AS, NF-1, S-2, S-3, ADR-0008-演练)
- open 17 / n-a 9 / fail 0 unchanged
- Boundary: this pass is based only on UDP measurements and is not extrapolated to TCP/TLS; it does not constitute a zero-loss or SLA commitment; the simulated S-SBC does not represent operator S-SBC behaviour; the `report.md` counts are unchanged; no git write operation was performed.

---

## M8 batch 4 terminalization countersignature (2026-10-13; the body rows and the "status tally" are kept unmodified, this section registers only terminal states and count changes)

> **Authorization source**: the maintainers' exact words on **2026-10-13**, "**accept the recommendation, authorize you to countersign**" — adopting
> the row-by-row recommended values of §1, the `defer` status term of §2, the count projection of §3 in
> [`m8-matrix-finalization-draft-2026-10-12.md`](m8-matrix-finalization-draft-2026-10-12.md),
> as well as the recommended values of the three adjudications **D4-01 / D4-02 / D4-05** in that draft's §4.
>
> **This section is not a maintainer's own signature**: every signature field uniformly reads "**agent countersignature (maintainer authorization dated 2026-10-13)**".
> **The M8 milestone is still unsigned** (internal version, not signed off); this batch signs no milestone.
> **Execution environment**: `dev-win03ib7niepf0` (registered in `docs/environments.md`).
>
> **Append-only discipline**: the matrix body rows, the "status tally" section and the existing appended sections (N2 / N3 / major gap / NF-4 adjudication) are **all kept unmodified**; this section registers terminal states and count changes only at the end of the file.

### One. The three adjudications landed together this time (the recommended values have been adopted)

| Item | Adjudication | Where it landed / evidence |
|---|---|---|
| **B5-04** (terminal state of the performance layer gate, leftover from batch 5) | **(b) The M8 final review accepts the risk in writing**: this version does not implement a `make gate` blocking layer | The item awaiting adjudication registered in `docs/acceptance/artifacts/m5/2026-10-12/FAILCLOSED-performance-gate-terminal-state-2026-10-12.txt` is closed on this basis; the NF-15 row consequently moves to pass, with a scope that excludes the saturation point and excludes external thresholds |
| **S-1 either/or** (D4-01) | **① Revise the matrix L86 description** — delete the unsupported claim "whitelist changes go through approval (linked to F-14)"; "bringing the whitelist into the change order" becomes a separate **v1.1 feature candidate** and does not block this row | The L86 body text is kept unmodified and registered in this section; evidence `docs/acceptance/artifacts/m5/2026-10-12/FAILCLOSED-s1-whitelist-change-approval-not-wired-2026-10-12.txt` (`ConfigBundle` has no peer entity; `ManagedRuleChange` only covers rules; `gate.install` / `install_with_overlap` inside `platform/src` have no product call site) |
| **Whitelist address / certificate OR semantics** (D4-02) | **OR is accepted in this version** (no code change, no ADR); tightening it to AND is listed as a **v1.1 security enhancement candidate**, pending confirmation of whether an S-SBC must present a client certificate | Evidence `docs/acceptance/artifacts/m5/2026-10-12/PASS-s1-whitelist-rejection-2026-10-12.txt` (the 9th case in the new `platform/tests/test_req_s1_whitelist_rejection.py` pins the OR semantics: an address hit admits immediately, no peer certificate required) |

### Two. Terminal state of the 17 rows (original status = open)

| req_id | Original status | Terminal state | Scope / destination | Evidence (triple) | signed_by |
|---|---|---|---|---|---|
| **F-4** | open | **pass** | This version; scope = testbed corpus (environment `dev-win03ib7niepf0`) 5 cases byte-identical; the live proof of `docs/plan.md` §5.2 **D11** is tracked independently | `(verified, docs/acceptance/artifacts/m5/2026-10-12/PASS-s7a-sdp-corpus-expansion-2026-10-12.txt, 2026-10-12)` | agent countersignature (maintainer authorization dated 2026-10-13) |
| **F-5** | open | **defer** | → **v1.1 feature**: the product AS forwards trunk-side Record-Route (`PASS-s8` states it still does not) | `(verified-baseline recapture only, docs/acceptance/artifacts/m5/2026-10-12/PASS-s8-baseline-recapture-2026-10-12.txt, 2026-10-12)` | agent countersignature (maintainer authorization dated 2026-10-13) |
| **F-8** | open | **defer** | → **v1.1 engineering supplementary test**: three-branch real-stack comparison + native C++→Python JSON callback (N2 #3 already deferred post-RC); **no new evidence in this version** | No new evidence in this version — does not constitute a triple; existing pointer `docs/reviews/m8-phase-a-f6-f8-note-2026-10-06.md` N2 #3 | agent countersignature (maintainer authorization dated 2026-10-13) |
| **F-9** | open | **defer** | → **v1.1 feature**: in-dialog re-INVITE / UPDATE; the BYE branch works in this version | `(verified-BYE branch only, docs/acceptance/artifacts/m5/2026-10-12/PASS-s9-in-dialog-bye-routing-2026-10-12.txt, 2026-10-12)`; `(not implemented, docs/acceptance/artifacts/m5/2026-10-12/FAILCLOSED-s9-reinvite-update-not-implemented-2026-10-12.txt, 2026-10-12)` | agent countersignature (maintainer authorization dated 2026-10-13) |
| **F-10** | open | **pass** | This version; passthrough of the three codes 486 / 480 / 408 | `(verified, docs/acceptance/artifacts/m5/2026-10-12/PASS-s10-non-2xx-passthrough-2026-10-12.txt, 2026-10-12)` | agent countersignature (maintainer authorization dated 2026-10-13) |
| **F-11** | open | **defer** | → **v1.1 defect fix**: CANCEL preceding any downstream response (native `runtime_module.cxx` L1143-1162 guard); branch ① works in this version | `(verified-branch ① only, docs/acceptance/artifacts/m5/2026-10-12/PASS-s11-cancel-race-branch1-2026-10-12.txt, 2026-10-12)`; `(not implemented, docs/acceptance/artifacts/m5/2026-10-12/FAILCLOSED-s11-cancel-before-any-downstream-response-2026-10-12.txt, 2026-10-12)` | agent countersignature (maintainer authorization dated 2026-10-13) |
| **F-16** | open | **pass** | This version, **the non-trace part only** (the decide translation cases, the same criterion as N3 used for F-6 / F-7); trace correlation moves to v1.1 with F-13 | `(verified-non-trace part, docs/acceptance/artifacts/m5/2026-10-11/PASS-gate-native-2026-10-11.txt, 2026-10-11)`; reproduced by the batch-closeout `make gate` 1174 passed on 2026-10-12 | agent countersignature (maintainer authorization dated 2026-10-13) |
| **NF-2** | open | **pass** | This version; boundary = excludes node-level faults and network partitions | `(verified, docs/acceptance/artifacts/m5/2026-10-12/PASS-nf2-deployment-isolation-2026-10-12.txt, 2026-10-12)` | agent countersignature (maintainer authorization dated 2026-10-13) |
| **NF-5** | open | **pass** | This version; boundary = TLS uses the test CA, does not sign REQ-S-2 / REQ-S-3 | `(verified, docs/acceptance/artifacts/m5/2026-10-12/PASS-nf5-simulator-transport-consistency-2026-10-12.txt, 2026-10-12)` | agent countersignature (maintainer authorization dated 2026-10-13) |
| **NF-9** | open | **pass** | This version; boundary = the two namespaces share the same kind node, excludes node-down | `(verified, docs/acceptance/artifacts/m5/2026-10-12/PASS-nf9-namespace-isolation-2026-10-12.txt, 2026-10-12)` | agent countersignature (maintainer authorization dated 2026-10-13) |
| **NF-10** | open | **pass** | This version; boundary = the fleet is a protocol stub and **does not prove that an AS process consumes a bundle**; the bundled PG / Redis are single-replica and do not cover production HA | `(verified, docs/acceptance/artifacts/m5/2026-10-12/PASS-f15-distribution-lifecycle-rollback-2026-10-12.txt, 2026-10-12)` | agent countersignature (maintainer authorization dated 2026-10-13) |
| **NF-13** | open | **blocked** | The engineering slice is inside gate; **live collection moves to the next release with X1** (adjudicated by maintainers on 2026-10-12, pending the operator's monitoring-integration standard input) | `(verified-engineering slice, platform/tests/test_resip_runtime_log_contract.py 13 passed (inside gate), 2026-10-12)`; restriction pointer: the X1 row in `docs/plan.md` §0 | agent countersignature (maintainer authorization dated 2026-10-13) |
| **NF-14** | open | **blocked** | Rule syntax has passed (promtool 3 groups of 10 rules); **real firing awaits Alertmanager + a notification channel** (customer environment, a continuation of the frozen M2 item). Syntax validation ≠ real firing | `(verified-syntax validation only, docs/acceptance/artifacts/m5/2026-10-11/PASS-alert-check-full-2026-10-11.txt, 2026-10-11)` | agent countersignature (maintainer authorization dated 2026-10-13) |
| **NF-15** | open | **pass** | This version, **condition = B5-04 adjudication (b) has landed**; scope = harness landed + multi-replica measurement, **excluding the saturation point and excluding external thresholds** | `(verified-not saturation point, docs/acceptance/artifacts/m5/2026-10-12/PASS-nf15-multi-replica-measurement-2026-10-12.txt, 2026-10-12)`; `(verified-internal only, docs/acceptance/artifacts/m5/2026-10-12/PASS-o1-loopback-cps-1280-2026-10-12.txt, 2026-10-12)`; `(verified, docs/acceptance/artifacts/m5/2026-10-12/PASS-hpa-threshold-filled-2026-10-12.txt, 2026-10-12)` | agent countersignature (maintainer authorization dated 2026-10-13) |
| **S-1** | open | **pass** | This version, **condition = S-1 adjudication ① has landed** (the matrix L86 description revised to match the facts); scope = whitelist rejection / fail-closed; **the OR semantics is accepted in this version** | `(verified-rejection scenarios only, docs/acceptance/artifacts/m5/2026-10-12/PASS-s1-whitelist-rejection-2026-10-12.txt, 2026-10-12)`; `(capability does not exist-registered, docs/acceptance/artifacts/m5/2026-10-12/FAILCLOSED-s1-whitelist-change-approval-not-wired-2026-10-12.txt, 2026-10-12)` | agent countersignature (maintainer authorization dated 2026-10-13) |
| **S-4** | open | **pass** | This version; RBAC HTTP boundary matrix + append-only audit (measured against real Postgres); boundaries = structural assertions ≠ database-side measurement (the latter is covered by the real PG integration), each permission takes only one representative endpoint, escalation traceability verified only for the submit×viewer cell, excludes external IAM / SSO and operator PKI | `(verified, docs/acceptance/artifacts/m5/2026-10-12/PASS-s4-audit-append-only-2026-10-12.txt, 2026-10-12)`; `(verified, docs/acceptance/artifacts/m5/2026-10-12/PASS-s4-rbac-permission-matrix-2026-10-12.txt, 2026-10-12)` | agent countersignature (maintainer authorization dated 2026-10-13) |
| **D12/O5-HA** | open | **blocked** | A **restriction** in table A (customer production Redis / PG HA), of the same kind as NF-1 / S-2 / S-3; kind bundled state is not this item; no v1.1 item is created, and verification happens in the customer environment before go-live | `(restriction, docs/acceptance/m8-environment-evidence.md, 2026-10-07)` | agent countersignature (maintainer authorization dated 2026-10-13) |

### Three. The status term `defer` (newly introduced this time)

| Status term | Definition | How it differs from neighbouring status terms | Can it be turned back into pass |
|---|---|---|---|
| **defer** | **Not accepted in this release**, **already assigned to v1.1**; when started it goes through the new feature process (requirement → ADR → design → review); this version **neither starts nor implements it** | Differs from `blocked` (a restriction, where what is missing is an external environment) and from `n-a` (never accepted) | Yes — once the feature lands it is accepted through the v1.1 process |
| **blocked** | A **restriction** — no customer environment / no operator input, not a feature gap | Cannot be lifted by engineering effort in this version; not entered into v1.1 planning | Acceptable once the environment is in place |
| **n-a** | **Never accepted, never recorded as pass** (all with rationale) | The opposite of `defer`; not entered into v1.1 planning | No |

**The 4 `defer` rows this time and their v1.1 planning inputs**:

| req_id | v1.1 category | Planning input (evidence / registration file) |
|---|---|---|
| **F-5** | v1.1 feature (the product AS forwards trunk-side Record-Route) | Self-declared in `docs/acceptance/artifacts/m5/2026-10-12/PASS-s8-baseline-recapture-2026-10-12.txt` (out-of-scope section: trunk-side Record-Route still not forwarded) |
| **F-8** | v1.1 engineering supplementary test (three-branch real-stack comparison + native C++→Python JSON callback) | `docs/reviews/m8-phase-a-f6-f8-note-2026-10-06.md` N2 #3 |
| **F-9** | v1.1 feature (in-dialog re-INVITE / UPDATE) | `docs/acceptance/artifacts/m5/2026-10-12/FAILCLOSED-s9-reinvite-update-not-implemented-2026-10-12.txt` |
| **F-11** | v1.1 defect fix (CANCEL preceding any downstream response) | `docs/acceptance/artifacts/m5/2026-10-12/FAILCLOSED-s11-cancel-before-any-downstream-response-2026-10-12.txt` |

### Four. Update to the count criterion following this change (the original counts are kept unmodified; only the new values are registered here)

- **pass: 17 → 27** (adding F-4 / F-10 / F-16 / NF-2 / NF-5 / NF-9 / NF-10 / NF-15 / S-1 / S-4)
- **open: 17 → 0**
- **defer: 0 → 4** (F-5 / F-8 / F-9 / F-11)
- **blocked: 6 → 9** (adding NF-13 / NF-14 / D12/O5-HA; remaining F-15, 5.4-F-15真AS, NF-1, S-2, S-3, ADR-0008-演练)
- **n-a 9 unchanged**, **fail 0 unchanged**

### Five. Boundaries (no excessive conclusions may be drawn from this section)

1. **Not a single character of the §0.5 counts of `docs/acceptance/report.md` has been changed** — the sync belongs to batch 6 (E-1), and the values are those in "Four" of this section.
2. "Engineering evidence accepted" ≠ REQ-level acceptance passed ≠ milestone sign-off; **the M8 milestone is still unsigned** (internal version, not signed off); this batch signs no milestone.
3. The 4 `defer` rows are assigned to v1.1 and are **neither started nor implemented in this version**; the 3 `blocked` rows (NF-13 / NF-14 / D12/O5-HA) are restrictions and are **not entered into v1.1 planning**.
4. This section's signature is an **agent countersignature (maintainer authorization dated 2026-10-13)** and is **not a maintainer's own signature**.
5. **No git write operation was performed** (no add / commit / tag / push / branch / stash); all changes stay in the working tree, and maintainers decide how to split the commits.
