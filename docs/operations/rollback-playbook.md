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

# Traffic Removal / Rollback Playbook (Rollback Playbook) — In-house IMS Application Server

> **Deliverable ownership**: [`../product-packaging-plan.md`](../product-packaging-plan.md) §1 second batch **2.4 Post-ISC business grayscale / traffic removal plan + coordination with S-CSCF-side iFC grayscale**. Per §3.2 of that plan, the **documentation part** of this deliverable is class A; the **real-cluster drill part is class B**, blocked by the M8 real-cluster environment (**7.2d still blocked**) and S-CSCF / HSS side cooperation (review **G-P1-10**). **M8 exit sign-off is still shelved**.
>
> **⚠️ The iFC triggering logic belongs to the S-CSCF / HSS, not the AS side (review G-P0-5 adjudicated)**. This product **only implements the business decision and traffic removal / rollback after ISC triggering**, and **does not implement iFC**. The **iFC triggering** by number range / percentage must be configured on the OP-NET / OP-HSS side; the AS side cannot do it on their behalf. This document **only defines the AS-side cooperation interface and process**, and does not write iFC as an AS-side deliverable.
>
> **The AS side does not proactively remove in-flight calls.** What we can guarantee is "**not proactively removing in-flight calls**"; **whether a call enters this AS is decided by the S-SBC / S-CSCF-side iFC configuration and traffic removal actions** (G-P0-5 / G-P1-10).
>
> **Draining evidence boundary**: existing draining / downscale / rolling-upgrade no-dropped-call evidence comes from `AS_M5_SIMULATED_ACTIVE_CALLS` **simulated** in-flight calls on kind (**G-P1-1**). **Not dropping calls under real SIP load awaits M7 / M8 acceptance**.
>
> **Zero capacity numbers**: this document contains no CPS / CAPS / BHCA / concurrency / throughput / latency / percentage capacity, and does not cite M6 dev-host numbers (O1 undecided, `AGENT.md` §2). **This document contains no recovery duration commitments**; the "recovery time magnitude" column in the table uses only **relative wording**.
>
> **Cross-links**: [`runbook-l1.md`](runbook-l1.md) (daily operations), [`runbook-l2.md`](runbook-l2.md) (deep troubleshooting), [`fault-demarcation.md`](fault-demarcation.md) (demarcation), [`backup-restore.md`](backup-restore.md) (stateful component maintenance windows), [`../product/responsibility-matrix.md`](../product/responsibility-matrix.md) (RACI).
>
> **Status note**: the outdated "not created" annotations in upstream documents were cleaned up uniformly on 2026-10-10; the blocked states described in this document (**M8 real-cluster environment / drills**) **still hold**.
>
> **B6 review status**: this document has been reviewed under B6 with a review record left — [`../reviews/product-packaging-review-checklist-2026-10-12.md`](../reviews/product-packaging-review-checklist-2026-10-12.md) §6 (2026-10-12 first review) and §7 (2026-10-12 closure re-review); **the conclusion awaits maintainer confirmation** and must not serve as a basis for external delivery or acceptance before confirmation (`AGENT.md` §3.3).

---

## 1. Boundary Statement (Three-Part)

| Part | Content |
|---|---|
| **Our responsibility** | ① the **business decision** after ISC triggering (`decide()` pure function, replayable); ② **business rule grayscale**: the evaluation granularity of runtime overrides is fixed as **number range + stable-hash percentage** (ADR-0021, `in_bucket` uses `fnv1a32(call_id) % 100`, **judged by Call-ID, idempotent**); ③ **execution of traffic removal / rollback** (draining, Pod-level draining, image rollback); ④ **configuration version rollback** (change order state machine, ADR-0006); ⑤ the **field contract and log search keys** provided to the peer for alignment |
| **Peer responsibility** | ① **iFC subscription and trigger configuration** (triggering ISC by number range / percentage) — OP-NET **A/R**, OP-HSS R; ② trunk establishment, topology and priority, traffic removal actions — OP-SBC; ③ the decision power over whether a call enters this AS; ④ change window approval (the network-side window's A role is OP-NET) |
| **Joint actions** | ① the **joint calibration** of the iFC trigger ratio and the AS-side override ratio; ② the joint observation of behavior distribution during the grayscale period; ③ the joint verification of traffic removal and pass-through; ④ rollback drill and mutual recognition of evidence (§5) |

**In one sentence**: the AS side only owns "the decision, traffic removal, and rollback after ISC triggering"; all pre-trigger access decisions (iFC subscription, triggering, grayscale) are on the OP-NET / OP-HSS / OP-SBC side.

---

## 2. Rollback Levels

**Levels from light to heavy**. Selection principle: **first use the level with the smallest blast radius and least need for peer cooperation**; only descend a level when the previous level cannot achieve the goal. **Descending is not escalating** — L4 traffic removal can still be decided by AS-Vendor + executed by OP-NOC.

| Level | Trigger condition | Action | Blast radius | Recovery time magnitude (**relative wording, no duration commitment**) | Dependencies |
|---|---|---|---|---|---|
| **L0** Business rule grayscale narrowing | New decision logic behaves unexpectedly in the grayscale pool, but limited to some number ranges | Narrow via **runtime override**: set `enabled=false` by **number range**, or tune the stable-hash **percentage** smaller | Only affects the number ranges / proportions covered by the **override**; **hot evaluation, no restart** | Shortest (hot evaluation, takes effect at the next decision, no restart, no peer action) | The **current implementation status of the override see the note below** |
| **L1** Change order rollback | Abnormal behavior after configuration version vN takes effect | Initiate `roll_back` from the console / config-service → the change order enters `ROLLED_BACK` (terminal state), the effective marker rolls back one immutable version row (vN-1); grayscale distribution rolls back accordingly | That configuration version across all instances; **the audit chain is fully preserved** | Short (via the existing distribution chain + health checks); **a failed health check triggers automatic rollback** (see §2.1) | No peer cooperation needed |
| **L2** AS business logic overall off / traffic removal | The AS business logic itself decides wrong, with blast radius covering all number ranges | Use the **deployment-level master switch** to turn off the AS business logic, and calls are **passed through to the next stage** (i.e., the AS side no longer rewrites / no longer rejects) | All use cases, all number ranges | Heavier than L1 (still goes through the change pipeline, **not** an independent channel); **must not** use an L0 override covering all number ranges as a substitute for the master switch | The deployment-level master switch goes through the ADR-0006 change pipeline (ADR-0020); **current implementation status see §2.2** |
| **L3** Image version rollback | New image introduces defects, or is incompatible with the rule schema | `helm history` → `helm rollback <revision>` → `kubectl rollout status` (commands as written see §2.3) | The image / manifest of all Pods; **draining takes effect on the exit path** (ADR-0009) | Heaviest (requires the full Pod replacement cycle, and existing calls must run to completion naturally) | Requires a maintenance window |
| **L4** Traffic removal (Pod-level draining) | Downscale / upgrade / instance anomaly, need to move an instance out of rotation | readiness to `503` → Endpoint traffic removal → wait for `as_active_calls` to reach zero → delete the Pod (**must not SIGKILL**) | A single Pod / a single use case | Correlated with the duration of existing calls, **not compressible** (ISSU = draining, ADR-0009) | No peer cooperation needed; **no in-flight state migration needed** |

### 2.1 L1's Automatic Rollback Semantics (copied verbatim from the implementation)

During grayscale distribution, **a failed health check in any batch triggers automatic rollback**:

- Distribution state machine: `pending` → `in_progress` → `completed`; on anomaly, `rolled_back` (`src/services/config-service/src/as_config_service/distributor.py`).
- Automatic rollback reason constant: `_AUTOMATIC_ROLLBACK_REASON = "health check failed"` (`distributor.py`).
- Rollback target: `rolled_back_to` must be **the version immediately preceding the planned version** (validated by `distribution_store.py`).
- Change order side: `APPLIED | DISTRIBUTING --roll_back--> ROLLED_BACK` (`change_order.py`); `REJECTED` / `APPLIED` / `ROLLED_BACK` are **terminal states**.
- **Automatic rollback still needs human confirmation**: NOTES.txt §3a explicitly states "always needs a human to confirm afterwards".

### 2.2 L2's Implementation Status (stated factually, not overstated)

- **Deployment-level master switch (layer ①)**: ADR-0020 defines it as two layers, "deployment-level master switch + runtime fine-grained override". In implementation, the switch rides the **same bus as the configuration change order** in the form of `ToggleDTO` (`ConfigBundle.toggles` → `toggle_deployment()` → `gating.is_enabled`), **opening no new channel**; `is_enabled` is **fail-closed** (an unregistered switch name evaluates to `False`). Its "on / off states" are covered by the change order pipeline's end-to-end tests.
- **Runtime fine-grained override (layer ②)**: the evaluation function `match_override` (`src/platform/src/as_platform/gating/overrides.py`) is implemented as a **pure function**, with granularity of number range + stable-hash percentage, longest-prefix-first, explicit `enabled=false` above percentage, and returning `None` (fail-closed) when not covered. ⚠️ **The current production path has no caller of this module** (unit test coverage only), and the console's live scope is also only **called party + prefix rules**.
- **Therefore**: the **mechanism and evaluation semantics of L0 and L2 hold, and the governance channel holds**, but **"turn off AS business logic in one click in seconds and pass through to the next stage" is wording in the product packaging plan, not a delivered, accepted operations action**. Before it lands, the following must be added first: a switch and override management entry on the console / API, production path wiring, and acceptance evidence for the on / off states. **Must not** write it in this document as a button executable on the spot.
- **L2's boundary**: turning off AS business logic only changes **AS-side behavior**; **diverting calls away from this AS still requires S-SBC / S-CSCF-side cooperation** (G-P1-10).

### 2.3 L3's Rollback Commands (copied verbatim from `deploy/helm/templates/NOTES.txt` §3)

NOTES.txt §3 explicitly states "two things are both called rollback, do not conflate them": **(a) configuration rollback** goes through the change order (= L1); **(b) image / manifest rollback** reverts the Helm release to roll the Deployment back, with **draining taking effect on the exit path** (ADR-0009):

**Version mapping prerequisite (mandatory before executing `helm rollback`)**: first execute `helm -n <ns> history <release>`, record the **revision ↔ chart `version` / `appVersion`** correspondence, and cross-check it with the root `VERSION` (currently `0.2.0`); the rollback evidence chain must record **all three of revision → chart version → product VERSION**, otherwise it is externally unverifiable.

**Factually noting the current desync (known gap)**: `deploy/helm/Chart.yaml` currently has `version: 0.0.0-skeleton` / `appVersion: "0.0.0"` with **no `kubeVersion`**, desynced with the root `VERSION` (`0.2.0`); validation uses `scripts/sync-chart-version.sh --check` (read-only by default, drift exits 1); **the timing and value of the first `--apply` are decided separately by the maintainer** (G4's "do not modify `VERSION` and `Chart.yaml` for now" remains in effect); `kubeVersion` has been set to `>=1.23.0-0` (reverse-derived from the chart's actual APIs) but is **not yet written into Chart.yaml**. This document **must not** claim it is drilled or synced — as of this document's closure date (2026-10-12), the above sync actions are **not executed**.

> **Note (added 2026-10-13)**: the previous paragraph's statement that the chart is still `0.0.0-skeleton` / `"0.0.0"` is outdated at the factual level (the first sync was executed on 2026-10-12); the handling (original text preserved + note appended) see [`../next-release-v1.1-plan.md`](../next-release-v1.1-plan.md) §5-1, pending the maintainer's decision on whether to sync.

```sh
helm -n <ns> history <release>
helm -n <ns> rollback <release> <revision>
kubectl -n <ns> rollout status deploy --selector app.kubernetes.io/part-of=3rdparty-as
```

> The original Helm template placeholders `{{ include "as.namespace" . }}` / `{{ .Release.Name }}` are written here as `<ns>` / `<release>`. ⚠️ NOTES.txt §3b mentions that `ASConfigRollbackTriggered` will alert, but **there is no such rule** in `deploy/alerts/as-alerts.yaml` (`deploy/alerts/README.md` explicitly lists it as deferred) — searching the alerting system by name will find nothing.

### 2.4 L4's Four Traffic Removal Steps

Commands as written see [`runbook-l1.md`](runbook-l1.md) §3.1 and [`../acceptance/m5-downscale-runbook.md`](../acceptance/m5-downscale-runbook.md): ① compute `plan_scale_down`; ② for each removable Pod, confirm `active_calls==0` before `kubectl delete pod`; ③ for Pods still carrying calls, **do not delete**, wait for natural completion, with readiness `503` after `request_terminate`, and the Endpoint should have traffic removed; ④ if `blocked`, only shrink the removable subset or wait. **Must not SIGKILL.**

---

## 3. Coordination with S-CSCF / HSS-side iFC Grayscale

> **This chapter is the core boundary of this playbook.** The **iFC triggering** by number range / percentage is configured on the S-CSCF / HSS side, and **we do not implement iFC**; what this chapter defines is the **cooperation interface, joint verification points, and failure rollback**.

### 3.1 Cooperation Interface

| Interface item | What we provide | What the peer provides |
|---|---|---|
| **Correlation key** | inbound leg `inbound_call_id` ↔ outgoing leg `outgoing_call_id` (the two legs of the B2BUA have different Call-IDs, REQ-F-2) | The trigger-side call identifier (Call-ID or equivalent) |
| **Evaluation granularity** | AS-side override: **number range prefix + stable-hash percentage** (ADR-0021) | iFC-side trigger granularity: **number range / percentage** (G-P0-5) |
| **Effect observation** | `as_active_calls`, decision result distribution (404/603 ratio), `CONFIG_VERSION` | Trigger volume observation, trigger success rate |
| **Traffic removal signal** | readiness `503` + Endpoint removal during draining (the AS side only removes itself) | The action of the peer stopping to send new calls to this AS |
| **Alignment method** | Both sides **capture on their own side**; TLS decryption is each party's own responsibility, and **keys are not shared across parties** | Same as left |

### 3.2 Joint Stage Table

| Stage | Peer action (S-CSCF / HSS / S-SBC) | Our action (AS-Vendor) | Joint verification point | Rollback on failure |
|---|---|---|---|---|
| **0. Pre-alignment** | Provide the iFC-side current trigger granularity and effective scope | Provide the AS-side override granularity and current effective configuration version | Both sides agree on "which number ranges are in grayscale" | Inconsistent → **stop the change**; align wording first, without touching either side |
| **1. Grayscale ratio adjustment** | Adjust the iFC trigger ratio / number range | Observe changes in `as_active_calls` and the decision result distribution | The AS-side inbound call volume and the peer's trigger volume are **consistent in direction and comparable in magnitude** (**relative comparison, no absolute numbers preset**) | Inconsistent direction → check correlation key alignment first, do not tune the AS-side override |
| **2. AS-side business grayscale** | None (AS-side overrides are self-managed by us) | Set or narrow overrides by number range / percentage | Different `call_id`s within the same number range land in different buckets — **this is the design expectation** (`FNV-1a 32-bit(call_id)`); first look at which bucket the `call_id` lands in | If the hit cannot be determined → judge with `call_id` + effective rule version + decision path; **do not use `as_rule_hits_total`** (no production caller) |
| **3. Traffic removal** | Stop introducing new calls to this AS (iFC / trunk side actions) | Pod-level draining: readiness `503` → Endpoint removal → wait for `active_calls` to reach zero | The convergence process of `as_downscale_removable` and `as_active_calls`; existing calls end naturally | Not converging → do not delete the Pod, switch to L2 / L3 (§2) |
| **4. Call pass-through** | Calls continue on their original path | When the AS-side business logic is off, **no rewriting, no rejecting** (L2's semantics) | Calls are **not rejected** and **not rewritten** on the AS side | The AS side still rewrites → override / master switch not in effect, return to §2.2 and the change pipeline |
| **5. Wrap-up** | Confirm the iFC-side configuration is stable | Confirm `CONFIG_VERSION` is consistent across replicas and audit rows have been produced | Both sides each keep a change record | — |

### 3.3 Joint Verification Checklist (checkable)

- [ ] The peer has confirmed the currently effective trigger number ranges / ratios on the iFC side, and provided a written record.
- [ ] We have confirmed the currently effective number ranges / ratios of AS-side overrides, with `CONFIG_VERSION` **consistent** across replicas.
- [ ] Both sides' time bases are aligned (not "appears simultaneous").
- [ ] After grayscale ratio adjustment, the AS-side inbound call volume and the peer's trigger volume are consistent in direction (**relative wording, no absolute values preset**).
- [ ] Changes in the decision result distribution (404 / 603 ratio) are explainable, and 404 / 603 are treated as **business decisions** rather than failures.
- [ ] During traffic removal, AS-side readiness is `503`, the Endpoint has been removed, and `as_active_calls` shows a convergence trend.
- [ ] Call pass-through verification passes: the AS side no longer rewrites and no longer rejects.
- [ ] Both sides each keep a change record and timeline, with filing path `artifacts/<milestone>/<YYYY-MM-DD>/` (per the directory designated by the maintainer).
- [ ] Redaction check: no passwords / tokens / cookies / private keys, no real packet captures (`AGENT.md` §11 / §13).

> ⚠️ **Risk note (G-P1-10)**: the checklist above **depends on the S-CSCF-side cooperation window and real-cluster drills**. Currently **7.2d is still blocked**, there are **no real-cluster drill records**, and **M8 exit sign-off is shelved**. What this document provides is an **executable process and verification points**, **not** a drilled-and-passed conclusion.

---

## 4. Change Windows and Decision Makers

| Item | Content |
|---|---|
| **Who decides rollback** | **AS-side decision + OP-NOC execution + OP-NET cooperation** (RACI §5.2). AS-Vendor is responsible for the choice of L0–L4; **whether calls enter this AS** is outside our decision scope |
| **Network-side window** | iFC subscription / trigger grayscale, trunk priority, and traffic removal tickets and approvals are at **OP-NET**, and **the AS side does not submit or approve on their behalf** |
| **The special nature of stateful component windows** | PostgreSQL / Redis maintenance requires an OP-NOC-approved window. ⚠️ **Brief runtime unavailability is expected within the Redis maintenance window** — in-flight call state (session / dialog / anti-fraud rate windows) is all in Redis, and Redis unavailable means in-flight calls cannot be sustained. **This is not a defect, it is known window behavior**; handling and recovery see [`backup-restore.md`](backup-restore.md) |
| **PG / Redis topology reminder** | The chart's built-in stores are **single replica**, **not HA**; the Redis HA topology values are adjudicated (**O5 / D3, G7**: in-site N+1 + cross-site 1+1 warm standby, Redis primary/replica + Sentinel, following the ADR-0008 topology, not Redis Cluster; the chart still renders single replica, with no evidence of measured failover behavior); production PG HA is owned by the customer (ADR-0008 / ADR-0026) |
| **Post-rollback re-verification items** | ① the effective configuration version rolled back into place (`CONFIG_VERSION` consistent across replicas); ② the decision result distribution back to expectations; ③ `as_active_calls` and draining status converge; ④ **audit rows have been produced** (append-only, the rollback itself also leaves a trace); ⑤ the change order enters a terminal state and **cannot be touched again**; ⑥ both sides' timelines archived |
| **Rollback is not "one-click, zero impact"** | L0 / L2 only change AS-side behavior; **diverting calls away from this AS still requires S-SBC / S-CSCF-side cooperation** |

---

## 5. Rollback Drill Record Template

**Current state: ⚠️ No real-cluster drill record.** The table below is a template, **with no rows currently filled in**. M8 **7.2d blocked**, M8 exit sign-off shelved; the iFC-side cooperation window is not scheduled (G-P1-10). **Must not** use kind / compose / `testbed/` simulation results as drill records (ADR-0014: the testbed is not a v1 deliverable).

| Field | Fill-in requirement |
|---|---|
| **Date** | Actual execution date of the drill (including time zone) |
| **Environment** | Cluster identifier / namespace / chart release; ⚠️ **no real cluster currently** |
| **Version from → to** | The version before rollback → the version after rollback (configuration version fills in `CONFIG_VERSION` / change order number; image / manifest version fills in `helm history` revision + chart `version` / `appVersion`, recorded in alignment with the root `VERSION` — the chart and `VERSION` are currently desynced (`0.0.0-skeleton` / `"0.0.0"` vs `0.2.0`), and all three must be recorded factually) |
| **Trigger reason** | Symptom + judgment basis; state which playbook (which level of §2's L0–L4) |
| **Level** | L0 / L1 / L2 / L3 / L4 |
| **Both sides' participants** | AS-Vendor (decision maker / executor), OP-NOC (execution), OP-NET / OP-SBC (cooperation); **names and roles are recorded by each party itself**, this template does not fill them in on their behalf |
| **Observation items** | Check item by item the §3.3 joint verification checklist + the §4 post-rollback re-verification items |
| **Result** | Pass / conditional pass / fail; **evidence path** (`artifacts/...`, after redaction) |
| **Open issues** | Unclosed items, responsible party, who needs to adjudicate |

> Record discipline: per `AGENT.md` §3.2/ §3.3, drill records are evidence and **must have a corresponding review record** to complete the documentation chain; the records themselves **do not constitute an acceptance conclusion**.

---

## 6. Undecided and Blocked

| Item | Blocking source | Impact on this document | Responsible party |
|---|---|---|---|
| **iFC-side grayscale joint testing** | OP-NET / OP-HSS configuration (G-P0-5 / G-P1-10) | §3 as a whole **cannot be closed end-to-end**; the AS side can only self-certify override effectiveness | OP-NET / OP-HSS |
| **Real-cluster drill** | M8 **7.2d blocked**, exit sign-off shelved | §5 has **no filled-in records**; the timing of each level in §2 is all **not drilled** wording | Maintainer + OP-NOC |
| **L2 deployment-level master switch's operations entry** | The console's live scope is only called party + prefix rules; the override production path has no caller | §2.2: "one-click off" is currently **mechanism holds, entry not delivered** | AS-Vendor (M4b / M8) |
| **L0 runtime override production wiring** | `match_override` has unit test coverage only | The L0 row in §2 is **currently not executable on the spot** | AS-Vendor |
| **Real SIP no-dropped-calls** | G-P1-1; draining evidence is **simulated** `active_calls` | The convergence of §2.4 and §3.2 stage 3 is **not accepted** | AS-Vendor (M7 / M8) |
| **E1 / E4 / E5** | M8 acceptance (O2 / O3) | Post-L3-rollback behavior judgment lacks production evidence | AS-Vendor |
| **O5 / D3 (disaster recovery / Redis Sentinel)** | Customer SLA | Values adjudicated (G7): in-site N+1 + cross-site 1+1 warm standby, Redis primary/replica + Sentinel (ADR-0008); **not yet implemented** (the chart still renders single replica, with no evidence of measured failover behavior); the PG / Redis window tiering in §4 is to be finalized after customer-side topology lands | OP-NET + maintainer |
| **Alert-side confirmation** | `ASConfigRollbackTriggered` / `ASConfigDrift` **do not exist** in `as-alerts.yaml` | After rollback there is **no alert evidence** to automatically leave a trace, so it can only be recorded manually | AS-Vendor (decided separately after M6 / after O1 adjudication) |
| **This document's review status** | `AGENT.md` §3.3 requires an independent review record | A review record has been left under B6 review — [`../reviews/product-packaging-review-checklist-2026-10-12.md`](../reviews/product-packaging-review-checklist-2026-10-12.md) §6 (2026-10-12 first review) and §7 (2026-10-12 closure re-review); **the conclusion awaits maintainer confirmation** and must not serve as a basis for external delivery or acceptance before confirmation | Maintainer |
