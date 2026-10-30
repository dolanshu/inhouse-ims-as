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

# Operations documentation — In-house IMS Application Server

> **Status**: this directory is a **newly created** operations-document directory (created 2026-10-09, corresponding to `docs/product-packaging-plan.md` §2 and review comment **G-P2-1**). The directory content is a **collection and reorganization** —— re-organizing the acceptance-state runbooks formerly scattered in `docs/acceptance/` into on-shift-facing operations text.
>
> **Originals preserved untouched**: `docs/acceptance/*-runbook.md` are **not deleted, not moved, not rewritten**, remaining the historical originals and the audit/traceability source. This directory only does "index + links + on-shift-facing operations text".
>
> **Evidence wording (important)**: the content of this directory is **engineering-slice evidence**. **M5 engineering closure ≠ REQ acceptance** (`docs/acceptance/report.md` §0.4 B-2); **M8 RC ready ≠ closure** (`report.md` §0.1). The sign-off matrix is currently pass 9 / fail 0 / **blocked 12** / n-a 4 / **open 24** (`report.md` §0.5) —— nothing in this directory may be read as "accepted".
>
> **Zero capacity numbers**: this directory **contains no capacity numbers** (no CPS / CAPS / BHCA / concurrency / throughput / latency / percentage capacity). O1 capacity target **unresolved**, `AGENT.md` §2 forbids publishing any such numbers before the M6 real-socket measurement. The M6 dev-host measurement is internal reference, not external O1/SLA, and this directory **does not cite it**.
>
> **Out of scope**: **no Diameter Sh**, **no CDR / billing**, **no media** (`AGENT.md` §2). This directory therefore **contains** no Sh-related alert, dashboard, or CDR billing content.

---

## 1. Readers and layering

| Sub-book | Reader | Questions answered | Depth |
|---|---|---|---|
| [`runbook-l1.md`](runbook-l1.md) | **L1 / NOC on-call** | "What to look at now, what counts as abnormal, what to do first, when to call someone" | Daily inspection + alert first-response + common operations |
| [`runbook-l2.md`](runbook-l2.md) | **L2 / second-line engineering** | "Why this symptom, can the AS side self-prove, which party owns the fault, how to gather evidence" | Deep troubleshooting + signaling/log forensics + ownership demarcation |
| **Cross-layer references (above L1 / L2)**: [`alert-response-matrix.md`](alert-response-matrix.md) (alert-action map), [`fault-demarcation.md`](fault-demarcation.md) (demarcation), [`rollback-playbook.md`](rollback-playbook.md) (rollback), [`backup-restore.md`](backup-restore.md) (backup-restore), [`grafana-dashboards/`](grafana-dashboards/README.md) (visualization) | Consulted during L1 / L2 handling | "What level is this alert, what to do first, when to call, what evidence to keep" / "which party owns the fault" / "how to roll back" / "how to backup-restore" / "what the dashboard points to" | Gives level / action / escalation path, demarcation, rollback, backup-restore, and visualization, for L1 / L2 to consult |

**Escalation path**: L1 → L2 → maintainer.

- **L1 → L2**: hit any condition marked "escalate L2" in this book; or L1's four-step check completes without a determined owner.
- **L2 → maintainer**: needs to adjudicate a product position (**O1 still unresolved**), or change the execution surface of a resolved item (**O4 / O5 / D3 / D5 values resolved (G6 / G7, 2026-10-10)**, related implementation not delivered, changing the execution surface still needs maintainer authorization), or needs to overturn an existing adjudication. L2 **must not** modify open items on its own (`AGENT.md` §15).

---

## 2. Directory contents

| File | Content | Reader | Source runbook (original preserved) | Status |
|---|---|---|---|---|
| [`runbook-l1.md`](runbook-l1.md) | Daily inspection checklist, L1 handling of 10 alerts (3 groups), manual scale-down / rolling upgrade / console operations / cert hot-update / backup-restore daily commands, upgrade and help, redaction rules | L1 / NOC | [`../acceptance/m5-downscale-runbook.md`](../acceptance/m5-downscale-runbook.md), [`../acceptance/m5-state-stores-runbook.md`](../acceptance/m5-state-stores-runbook.md), [`../acceptance/m5-7.2d-ingress-runbook.md`](../acceptance/m5-7.2d-ingress-runbook.md), [`../../deploy/alerts/as-alerts.yaml`](../../deploy/alerts/as-alerts.yaml) | Created (this delivery) |
| [`runbook-l2.md`](runbook-l2.md) | Troubleshooting methodology, log-field forensics contract, signaling-capture alignment, 7-category layered fault tree, change and canary troubleshooting, migration troubleshooting, sign-off environment prep, misleading-pitfall list | L2 / second-line | [`../acceptance/m8-resip-runtime-log-contract.md`](../acceptance/m8-resip-runtime-log-contract.md), [`../acceptance/m8-native-consistency-runbook.md`](../acceptance/m8-native-consistency-runbook.md), same L1 sources | Created (this delivery) |

Besides the two books above, the rest of this directory's deliverables (fault demarcation, rollback, backup-restore, alert-action map, Grafana dashboards) **are all persisted**, and their content status is in §4.

---

## 3. Collection mapping

Three tiers of "collection method": **rewrite operations text** = rewrite for on-shift, copy command originals verbatim; **index link** = only give pointers and wording, no rewrite; **summary** = keep conclusions and status, don't move the process.

| Existing acceptance document | Which section it maps to here | Collection method |
|---|---|---|
| [`../acceptance/m5-downscale-runbook.md`](../acceptance/m5-downscale-runbook.md) | L1 §3.1 manual scale-down and drain; L2 §4.7 scale-down no-call-drop / draining non-convergence | Rewrite operations text (`plan_scale_down` criteria, four-step order, draining readiness 503 copied verbatim) |
| [`../acceptance/m5-state-stores-runbook.md`](../acceptance/m5-state-stores-runbook.md) | L1 §3.2 rolling upgrade, §3.5 backup and restore daily commands; L2 §6 database and migration troubleshooting, §4.6 config-service CrashLoop | Rewrite operations text (`helm upgrade` parameter surface, `as-config-migrate` owner DSN, the two `pg_dump -Fc` lines copied verbatim) + summary (PG HA/PITR three tiers, Restore drill, upgrade discipline) |
| [`../acceptance/m5-7.2d-ingress-runbook.md`](../acceptance/m5-7.2d-ingress-runbook.md) | L1 §1 inspection item 5, §2 alert-triggerability note; L2 §4.6 Ingress not Ready, §8 pitfall list | Index link (the 6 closure-check items preserved verbatim in the referenced file) + summary (301/308 expectations, admission webhook WARN wording, proxy 403/000, empty reply curl 52 treated as not passed) |
| [`../acceptance/m4b-8-runbook.md`](../acceptance/m4b-8-runbook.md) | L1 §3.3 console daily operations (browser path for rule change orders and BLOCKED rules) | Summary + index link (5-step operation path, BLOCKED rules, Playwright container rollback, redaction requirements kept in the original) |
| [`../acceptance/m8-native-consistency-runbook.md`](../acceptance/m8-native-consistency-runbook.md) | L2 §7 tests and sign-off environment prep | Rewrite operations text (`make` targets and the two `pytest` commands copied verbatim) |
| [`../acceptance/m8-resip-runtime-log-contract.md`](../acceptance/m8-resip-runtime-log-contract.md) | L2 §2 log forensics | Index link + field-contract table and 7 sample-log lines **copied verbatim** (this is a field contract, not a runbook) |
| [`../acceptance/report.md`](../acceptance/report.md) §0 and open-item list | Both books' status blocks; L2 §8 pitfall list | Summary (terminology discipline: RC ready ≠ passed) |
| [`../plan.md`](../plan.md) §0 / §5.1 | Both books' status blocks (v1/v1.1 are not release versions, O1 unresolved); L1 §3.3 note | Summary |
| [`../../deploy/alerts/as-alerts.yaml`](../../deploy/alerts/as-alerts.yaml) + [`README.md`](../../deploy/alerts/README.md) | L1 §2 alert handling | Summary (**10 rules / 3 groups** expressions and levels) + index link (thresholds take the rule file as single authority) |
| [`../product/ne-datasheet.md`](../product/ne-datasheet.md) §5/§6 | L1 §1 inspection, §2 alert triggerability | Summary (KPI wording and alert list single source, to avoid drift in two places) |
| [`../product/compliance-matrix.md`](../product/compliance-matrix.md) | L2 §4.3 / §4.4 decision and failure codes | Index link (file:line evidence for 404 / 603 / 403 / passthrough set {408,480,486,503,504} is in the matrix) |
| [`../product/responsibility-matrix.md`](../product/responsibility-matrix.md) §3/§4 | L2 §3 capture responsibility, §4 fault-tree ownership judgment | Index link + summary (what the AS side can / cannot self-prove) |

---

## 4. Current status of this directory's other deliverables

The following files belong to this plan's operations-document deliverables, **all persisted** (directly openable). But **the parts depending on a real cluster / peer coordination are still blocked**, and every reference in the two books is marked in place —— **blocked parts do not constitute drilled, executable steps**:

| File | Collected from / depends on | Persisted status | Still-blocked parts |
|---|---|---|---|
| [`fault-demarcation.md`](fault-demarcation.md) — fault-demarcation manual | [`../product/responsibility-matrix.md`](../product/responsibility-matrix.md) §3/§4 already gives first-round ownership in the product book | **Persisted** | **Full-playbook real-cluster evidence still missing** (M8 7.2d still blocked) |
| [`backup-restore.md`](backup-restore.md) — backup-restore plan + drill record | [`../acceptance/m5-state-stores-runbook.md`](../acceptance/m5-state-stores-runbook.md) §PG HA/PITR + §Restore drill; [`../product-packaging-plan.md`](../product-packaging-plan.md) deliverable 2.5 | **Persisted** | **Real-cluster restore-drill record still blocked** (M8 real-cluster evidence currently on hold, G-P1-10) |
| [`rollback-playbook.md`](rollback-playbook.md) — service drain / rollback + iFC coordination | ADR-0006 config rollback + ADR-0021 runtime-override granularity; G-P1-10 | **Persisted** | **iFC / drain part depends on S-CSCF/HSS-side coordinated config, real-cluster drill still blocked** (G-P1-10) |
| [`alert-response-matrix.md`](alert-response-matrix.md) — alert-action map | [`../../deploy/alerts/as-alerts.yaml`](../../deploy/alerts/as-alerts.yaml) **10 rules / 3 groups**; product book 2.2 | **Persisted** | None (capacity-class alerts continue to defer to post-O1 adjudication) |
| [`grafana-dashboards/overview.json`](grafana-dashboards/overview.json), [`grafana-dashboards/sip-signaling.json`](grafana-dashboards/sip-signaling.json) — Grafana dashboard templates (see [`grafana-dashboards/README.md`](grafana-dashboards/README.md)) | Product book 2.1 | **Persisted** | **Availability depends on AS metric scrape wiring, currently not closed** (no scrape annotation, no ServiceMonitor / PodMonitor); **no Sh dashboard** (Sh out of scope, G-P2-3 deleted `sh-interface.json`) |

---

## 5. Whole-book unified disclaimer

1. **This directory is not an acceptance conclusion.** All content is based on engineering-slice evidence; **M5 engineering closure ≠ REQ acceptance**, **M8 RC ready ≠ closure**.
2. **Zero capacity numbers.** No CPS / CAPS / BHCA / concurrency / throughput / latency / percentage capacity. O1 unresolved. Ratio-type alert thresholds (e.g., 1%, 30%) and fixed-window counts (e.g., 3 per minute) are **existing alert thresholds**, **not** capacity metrics.
3. **Do not cite M6 dev-host numbers.** M6 measurement is internal reference, not external O1/SLA.
4. **e2e status.** `pytest -m e2e` currently has **8 stably passing** (Wave 1 five `tests/e2e/test_sip_first_edition.py` + Wave 2 three `tests/e2e/test_s1_replay_contract.py`; when native extension is missing they **fail, not skip**), REQ-F-1 = **automated subset covered / full text still open** (covered: two-leg normalized message-sequence diff, C_in ≠ C_out, SDP offer byte-identical; **the 14-message header-by-header diff still not covered**); performance only accept-all harness, **not the business-decision path**.
5. **No Diameter Sh / no CDR / no billing / no media.** Where present, mark N/A; rationale in `AGENT.md` §2 and [`../product/compliance-matrix.md`](../product/compliance-matrix.md).
6. **Do not actively drain in-flight calls.** The AS side does not drain in-flight calls; drain is the other party's (OP-SBC / OP-NET) action.
7. **Under TLS, decryption is each party's responsibility, keys not shared across parties.** Do not copy the peer's private key for decryption.
8. **testbed / kind / compose captures are not live-network evidence.** ADR-0014 explicitly excludes testbed from v1 deliverables.
9. **Terminology discipline.** "v1" / "v1.1" **are not release versions** (`docs/plan.md` §0, 2026-10-07 maintainer wording); the product version number only looks at the root `VERSION`. Any calling-party / regex rules in the docs are marked **v1.1 (not a release version)**.
10. **Naming discipline.** The product name is **In-house IMS Application Server**, **formally adopted as the product / documentation descriptor name** (G8-2; **not a trademark / not a brand claim**); chart name / image name / OTel service name remain `3rdparty-as` unchanged.
11. **Keys and captures.** Storing passwords / tokens / cookies / private keys is forbidden; **never commit real captures** (`AGENT.md` §13).

---

> **Review entry**: the **execution record** for each sub-book in this directory is in [`../reviews/product-packaging-execution-record-2026-10-10.md`](../reviews/product-packaging-execution-record-2026-10-10.md). That file is **the packaging-delivery execution record, not a maintainer-signed review record** —— the independent review record required by `AGENT.md` §3.3 is still pending maintainer review.
>
> **B6 review status**: this document has left a review record with the B6 review —— [`../reviews/product-packaging-review-checklist-2026-10-12.md`](../reviews/product-packaging-review-checklist-2026-10-12.md) §6 (2026-10-12 initial review) and §7 (2026-10-12 closed-loop re-review); **conclusion pending maintainer confirmation**, and before confirmation it is not used as a basis for external delivery or acceptance (`AGENT.md` §3.3).
