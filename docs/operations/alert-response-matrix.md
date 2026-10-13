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

# Alert-Action Matrix — In-house IMS Application Server

> **Deliverable**: **2.2 Alert rule reinforcement + alert-action matrix** ([`../product-packaging-plan.md`](../product-packaging-plan.md) §1 second batch 2.2).
> **Sole authority for rules**: [`../../deploy/alerts/as-alerts.yaml`](../../deploy/alerts/as-alerts.yaml) (REQ-NF-14). **The rule file is authoritative for thresholds**; this page only answers "when I see this alert, what do I do first, when do I escalate, and what evidence must I keep".
> **Loading and validation**: [`../../deploy/alerts/README.md`](../../deploy/alerts/README.md) (`promtool check rules` / `make alert-check`) — `promtool check rules` passed on 2026-10-11 (verified, [`../acceptance/artifacts/m5/2026-10-11/PASS-alert-check-2026-10-11.txt`](../acceptance/artifacts/m5/2026-10-11/PASS-alert-check-2026-10-11.txt), 2026-10-11): `SUCCESS: 10 rules found` (3 groups, 10 rules; promtool 2.55.1). **Boundary: passing syntax validation ≠ closed scraping wiring** (X1 still awaits the operator's monitoring-integration standard input).
> **Position of this booklet**: [`README.md`](README.md) §1 layering, the "cross-layer reference (above L1 / L2)" row — L1 gives the first response, L2 gives demarcation and forensics, this page gives **severity, actions, escalation path**.
>
> **Status: draft, not accepted.** This page is **engineering slice evidence**, not an acceptance conclusion:
> - **M5 engineering closure ≠ REQ acceptance**; **M8 RC readiness ≠ closure** ([`../acceptance/report.md`](../acceptance/report.md) §0).
> - **Current e2e state**: `pytest -m e2e` **8 tests pass stably** (Wave 1 five tests `testbed/e2e/test_sip_first_edition.py` + Wave 2 three tests `testbed/e2e/test_s1_replay_contract.py`; **fail, not skip**, when the native extension is missing), REQ-F-1 = **automated subset covered / full text still open** (covered: two-leg normalized message sequence differential comparison, C_in ≠ C_out, byte-identical SDP offer; **per-message header differential comparison of the 14 messages is still not covered**); performance is accept-all harness only, **not the business decision path** (G-P1-2).
> - **E1 / E4 / E5 not accepted** (production stack reSIProcate behavior, TLS hot rotation, state externalization), see [`../product/ne-datasheet.md`](../product/ne-datasheet.md).
> - **7.2d / M8 real-cluster evidence still blocked** (G-P1-10): every command on this page is an **executable action**, and **none** has been run on a production cluster and filed.
>
> **⚠️ Known blind spots in the current alert surface** (details in §3): scraping wiring gap, insufficient e2e end-to-end backstop (`pytest -m e2e` has 8 tests passing stably, REQ-F-1 full text still open), M8 exit sign-off shelved, 7.2d blocked.
> **Zero capacity numbers**: this page contains no CPS / CAPS / BHCA / concurrency ceiling / latency threshold / throughput numbers. O1 is undecided ([`../../AGENT.md`](../../AGENT.md) §2 / §6); capacity alerts are deferred to a new `as.capacity` group after O1 is adjudicated.
> **Out of scope**: no Diameter Sh / no CDR and billing / no media ([`../../AGENT.md`](../../AGENT.md) §2). This page has no Sh-related alerts.
>
> **B6 review status**: this document has been reviewed under B6 with a review record left — [`../reviews/product-packaging-review-checklist-2026-10-12.md`](../reviews/product-packaging-review-checklist-2026-10-12.md) §6 (2026-10-12 first review) and §7 (2026-10-12 closure re-review); **the conclusion awaits maintainer confirmation** and must not serve as a basis for external delivery or acceptance before confirmation (`AGENT.md` §3.3).

---

## 1. Alert Severity Definitions and Escalation Path

### 1.1 Severity Mapping

Prometheus's `severity` label is the **sole severity source** in the rules. P-levels are a grading from the on-duty perspective; the two are hard-mapped per the table below, and "the same rule written differently in two places" is not allowed.

| Prometheus `severity` | This document's level | Meaning | First-response requirement (process discipline, not a duration promise) |
|---|---|---|---|
| `critical` | **P1** | Business unavailable or in-flight calls cannot be sustained | **Intervene immediately**, no shift waiting; notify second line (L2) in parallel; handle and collect evidence at the same time, do not investigate fully before acting |
| `warning` | **P2** | State deviated but business not yet interrupted, or self-healable | Handle during the shift; first follow the matrix's first-check action, and if any "escalation path" condition is hit, switch to P1 handling |
| `info` / unclassified | **P3** | Record and trend observation | Record in the on-duty log, no immediate action needed; if persistent or recurring, handle as P2 |

> **This page writes no minute counts.** Response time limits are a matter of on-site SLA and customer agreement; this repo commits to no specific minute counts; the table above only states process discipline (`docs/product-packaging-plan.md` §0.2 gap 9: SLA / EOL strategy not yet initiated).

### 1.2 Escalation Path

```text
On-duty NOC (L1)
   │  any condition in the matrix's "escalation path" column hit
   ▼
Second-line engineering (L2) — demarcation, forensics, configuration changes when necessary
   │  needs adjudication of product wording / touching undecided items (O1 still undecided; O4 / O5 / D3 / D5 values already adjudicated (G6 / G7), execution-side changes require authorization) / overturning existing adjudications
   ▼
Maintainer / architecture
   │
   ▼
Customer-side contact (only when ownership falls on the peer: S-CSCF / HSS / S-SBC / customer PKI / customer network)
```

- **L1 → L2**: see the "escalation path" column of each row in §2; [`runbook-l1.md`](runbook-l1.md) §4 gives the complete help evidence checklist.
- **L2 → Maintainer**: when wording needs adjudication or undecided items need changing. L2 **must not** on its own treat an undecided item as resolved ([`../../AGENT.md`](../../AGENT.md) §15).
- **→ Customer-side contact**: when the demarcation conclusion falls on the peer. The AS side has **only** its own logs, metrics, and configuration versions; forensics of peer links (S-CSCF → S-SBC trigger segment, S-SBC → AS trunk segment) **must** be cooperated on by the peer ([`runbook-l2.md`](runbook-l2.md) §3, [`../product/responsibility-matrix.md`](../product/responsibility-matrix.md) §3/§4).
- **Discipline when AS-side evidence is insufficient**: **no prior demarcation without evidence**. If evidence is missing, write the gap into the help ticket; do not substitute speculative conclusions.

---

## 2. Alert-Action Matrix (Main Table)

Covers **all 10 rules** of `as-alerts.yaml` item by item: 5 pre-existing in `as.call-path` + 5 added on 2026-10-10 (`as.runtime` 3, `as.platform` 2).
All thresholds are **pre-existing alert thresholds or state conditions**, **not capacity metrics**.

### 2.1 `as.call-path` — pre-existing 5 (unchanged this round)

| # | Alert | Level | Trigger condition (expression semantics) | First-check action | Handling action | Escalation path | Rollback / stop-loss | Evidence to keep | Current triggerability |
|---|---|---|---|---|---|---|---|---|---|
| 1 | **`ASHighErrorRatio`** | P2 `warning`<br/>`signalling` | Sum of 5xx and **non-487** 4xx ÷ all SIP responses > **1%**, sustained for **10m**. The denominator `clamp_min(..., 1)` avoids division by zero on zero samples; **487 (caller cancel) is explicitly excluded** and is normal behavior | 1) Confirm whether `as_sip_responses_total` **really has samples** (after `kubectl -n <ns> port-forward deploy/<release>-<use-case> 8080:8080`, run `curl -s localhost:8080/metrics \| grep '^as_sip_responses_total'`)<br/>2) No samples → **do not** judge it as a failure; check the scraping wiring first<br/>3) Samples present → break it down by `status_class` / `status_code` to see which category | First distinguish decision-class from fault-class: 404 = no matching rule, 603 = policy rejection, **both are expected decisions** ([L2 §4.3](runbook-l2.md)). Only if there are genuine 5xx, check Redis reachability, S-SBC-side rejection reasons, decision module anomalies | Real samples with a persistently rising ratio → L2 ([L2 §4.3](runbook-l2.md) / [L2 §4.4](runbook-l2.md)); ownership falls on the S-SBC → customer-side contact | Business-side stop-loss: switch runtime override to pass through to the next stage by number range / percentage (ADR-0021); the AS side **does not proactively remove in-flight calls** (traffic removal is the peer's action) | Expression evaluation time series + `status_code` distribution + Call-ID (cross-leg Call-IDs **differ**, keep both) + same-period `helm history` / change order revision | **Not triggerable.** The only write point is the one-time startup probe `AS_M5_PROBE_SIP_STATUS` (`__main__.py:_apply_m5_metrics_probes`), not set in production on-prem; the path called by the product SIP adapter on every response awaits M7 |
| 2 | **`ASTelemetryDropped`** | P2 `warning`<br/>`observability` | `as_telemetry_dropped_total` `increase` ≥ **50** within a **15m** window, sustained for **15m** | 1) Confirm whether an OTLP endpoint is configured (chart `telemetry.otlpEndpoint`, default `null`)<br/>2) Not configured → this series **never produces data in the first place**, not a failure<br/>3) Configured → check backend reachability and queue logs | Dropped telemetry is **acceptable by design**; applying backpressure to the call path is **unacceptable**; sustained drops usually mean the backend is unreachable or too slow. First confirm whether the call path is affected, then fix the export chain | Configured backend yet sustained drops → L2; impact spreads to the call path → handle as P1 | No business stop-loss needed; if necessary, **silence** export (does not block the call path, ADR-0005) | `/metrics` snippet + backend reachability evidence + drop amount and window | **Not triggerable (under default configuration).** `BoundedQueueSink` is created only when `OTEL_EXPORTER_OTLP_ENDPOINT` is non-empty; and the exporter defaults to `NoOpExporter`, so the queue is hard to fill |
| 3 | **`ASRestartLoop`** | P1 `critical`<br/>`runtime` | Single Pod container restart count `increase(...[1m])` > **3**, `for: 0m` | 1) `kubectl -n <ns> describe pod <pod>`<br/>2) Get the previous container's logs: `kubectl -n <ns> logs <pod> --previous`<br/>3) Check the latest configuration version (`printenv CONFIG_VERSION`) | CrashLoop. First distinguish **repeated restarts** from **a single rolling update**; repeated restarts go as P1 without waiting for business feedback | Repeated restarts / involves multiple Pods → L2 (config-service section of [L2 §4.6](runbook-l2.md), §4.7 downscale section) | `kubectl -n <ns> rollout undo deploy/<release>-<use-case>`; image / manifest rollback uses [`rollback-playbook.md`](rollback-playbook.md) (**written to disk**; but relies on peer cooperation, real-cluster drill still blocked, G-P1-10) | `describe` output + `--previous` logs + `CONFIG_VERSION` + change order revision (avoid treating "not checked" as "ruled out") | **Triggerable (the only class with no configuration precondition).** The data source is cluster-provided kube-state-metrics; the cluster only needs KSM installed |
| 4 | **`ASCallStateStoreUnavailable`** | P1 `critical`<br/>`state` | `min by (use_case) (as_state_store_available) == 0`, sustained for **2m**. Binary reachability state | 1) Read `/metrics` to confirm the series **exists and is 0** (series absent ≠ 0, see below)<br/>2) Check the Redis Pod: `kubectl -n <ns> get pods -l app.kubernetes.io/component=state-redis`<br/>3) First confirm the deployment form: the chart's built-in Redis is single replica (`stateStores.enabled`), **no Sentinel object to query**<br/>4) If the customer deploys external Redis (topology already adjudicated: primary/replica + Sentinel, G7), check failover status with customer-side tools | Session, dialog, and anti-fraud rate-window state all live in Redis (ADR-0002 / ADR-0007) → in-flight calls cannot be sustained, new decisions lose counters. Handle immediately as P1 | **Immediate** L2. Do not wait | Before recovery, **do not** let the AS continue to accept new calls; pause change order approval on the config-service side (a governance action, do not touch the data plane) | `/metrics` snippet (proving it is 0, not absent) + Redis Pod state + failover window (Redis HA topology values already adjudicated — **O5 / D3 (G7)**: primary/replica + Sentinel; the chart still renders single replica, no evidence of measured failover behavior) + affected use_case list | **Triggerable, provided `REDIS_URL` is configured**: at that point the metrics loop really `PING`s Redis and writes the series. When `REDIS_URL` is empty the **series does not exist (not 0)**, so the rule never triggers |
| 5 | **`ASActiveCallsSurge`** | P2 `warning`<br/>`signalling` | Current `as_active_calls` per `use_case` > **1.3×** its own **30m sliding average**, sustained for **10m**. **Relative change**, structurally contains no absolute call count | 1) First look at whether there is **any change / traffic removal / upstream action** (the most common cause)<br/>2) Compare whether `ASHighErrorRatio` is rising at the same time<br/>3) Check whether `AS_M5_SIMULATED_ACTIVE_CALLS` was set by mistake | Judge it as "**the traffic shape changed**", not a failure itself. If confirmed to be caused by a business change, record and observe; dig deeper only if there is no corresponding change | Accompanied by a rising error ratio or state store alert → L2 (switch to P1 handling); with a corresponding change → **do not escalate**, record only | **Must not** infer a capacity ceiling or apply a temporary cap based on this. Investigate real load anomalies with the M6 harness and internal measurements | `as_active_calls` curves for both time windows + same-period change records + whether any simulated values were involved | **The series is always produced** (the `__main__.py` metrics loop writes unconditionally), but the values depend on dialog events from the SIP runtime; does not trigger with no traffic or a constant count of 0. **Also see the §3 scraping wiring gap** |

### 2.2 `as.runtime` — 3 added on 2026-10-10

| # | Alert | Level | Trigger condition (expression semantics) | First-check action | Handling action | Escalation path | Rollback / stop-loss | Evidence to keep | Current triggerability |
|---|---|---|---|---|---|---|---|---|---|
| 6 | **`ASPodNotReady`** | P1 `critical`<br/>`runtime` | The Pod's `Ready` condition (`condition="true"`) is 0, sustained for **5m**. Ready = the process is **rejecting new work** | 1) `kubectl -n <ns> get pod <pod> -o wide` to see `READY`<br/>2) Access `/health/ready`: **503 = draining (normal traffic removal)**, sustained 503 is the anomaly<br/>3) `describe pod` to see Events (probe failures / mounts / image) | First distinguish **normal draining** from **stuck**: 503 + about to be rebuilt = normal rolling; 503 unchanged for a long time = draining not converging, switch to [L2 §4.7](runbook-l2.md) | Draining not converging / repeatedly not-ready → L2; appears together with #3 → handle as CrashLoop | `kubectl -n <ns> rollout undo deploy/<release>-<use-case>`; **must not** directly SIGKILL in-flight calls (drain first, ADR-0009) | `get pod -o wide` + `describe` Events + `/health/ready` response code and timing + `CONFIG_VERSION` | **Triggerable (provided the cluster has kube-state-metrics installed).** Note it **does not distinguish components**: AS engine Pods, `state-redis`, `state-postgres`, and `config-service` are all in the same namespace, distinguished by `pod` name |
| 7 | **`ASDeploymentReplicasUnavailable`** | P2 `warning`<br/>`runtime` | Same Deployment's `kube_deployment_status_replicas_available` < `kube_deployment_spec_replicas`, sustained for **10m** | 1) Look at the `deployment` label in the alert — it may refer to the **use-case Deployment**, `state-redis`, or `config-service`<br/>2) `kubectl -n <ns> get deploy <deployment>` + `describe`<br/>3) Judge together with #6 (usually two views of the same event) | Route by component per the previous step: use-case Deployment → check rolling / probes; `state-redis` → check Redis (merge with #4); `config-service` → check the console chain | Insufficient use-case replicas affecting business → P1, switch to L2; `state-redis` unavailable → same path as #4, escalate immediately | Image / manifest rollback: `helm -n <ns> rollback <release> <revision>` (the rollback path and **configuration rollback are two different things**, do not conflate, [`runbook-l1.md`](runbook-l1.md) §3.2) | `deployment` name + `get deploy` `READY/AVAILABLE` + ReplicaSet events + current `helm history` revision | **Triggerable (provided KSM).** The selector **is limited by namespace**, so it also covers the two Deployments `state-redis` and `config-service` |
| 8 | **`ASDownscaleBlocked`** | P2 `warning`<br/>`runtime` | On the same `pod`/`use_case`, `as_downscale_removable == 0` **and** `as_active_calls == 0`, sustained for **30m**. ADR-0010's guard has only two interception reasons: **in-flight calls** and **already draining** → with both excluded, only "**draining stuck**" remains | 1) `curl -s localhost:8080/metrics \| grep -E '^as_(downscale_removable\|active_calls)'` to confirm the two series<br/>2) Check whether that Pod's `/health/ready` is 503 for a long time<br/>3) Merge with #6: very likely not-ready appears on the same Pod at the same time | Confirm draining is not converging: in-flight calls cannot reach zero, or the process does not exit after `preStop` / SIGTERM. Handle per [L2 §4.7](runbook-l2.md) | Not converging for more than 30m → L2; involves multiple Pods or affects the release window → escalate immediately | **Must not** directly delete the Pod or SIGKILL — drain fully first; after confirming calls reach zero, `kubectl -n <ns> delete pod <pod>` (triggers `preStop sleep` + SIGTERM) | Time series of the two series (proving same `pod`/`use_case`) + Pod events + whether in a change window (`helm history` / change order) | **The series is always produced** (the metrics loop writes unconditionally, not dependent on OTLP), but **the values depend on real SIP dialog activity** — does not trigger with no traffic. **Also see the §3 scraping wiring gap** |

### 2.3 `as.platform` — 2 added on 2026-10-10

| # | Alert | Level | Trigger condition (expression semantics) | First-check action | Handling action | Escalation path | Rollback / stop-loss | Evidence to keep | Current triggerability |
|---|---|---|---|---|---|---|---|---|---|
| 9 | **`ASStatefulSetUnavailable`** | P1 `critical`<br/>`state` | Some StatefulSet's `kube_statefulset_status_replicas_ready` < `kube_statefulset_replicas`, sustained for **5m**. In-chart this is the **governance database PostgreSQL** (ADR-0008) | 1) Confirm the `statefulset` name in the alert (expected `<release>-postgres`)<br/>2) `kubectl -n <ns> get sts <name>` + `describe`<br/>3) Check the recent migrate Job: `kubectl -n <ns> get jobs \| grep config-migrate`<br/>4) Run `pg_isready` on the governance database host | The governance PG holds configuration versions, change orders, and the append-only audit chain → **configuration cannot be approved or distributed**, and the console change order process stalls. Handle as P1 | **Immediate** L2 → maintainer (involves data plane recovery) | Configuration-side stop-loss: pause change order approval; **do not** directly UPDATE configuration tables on the database (configuration does not go through GitOps, and operations staff are not allowed to modify the database directly, `AGENT.md` §2 / ADR-0006). Recovery methods see [`backup-restore.md`](backup-restore.md) (**written to disk**; but the real-cluster restore drill record is still blocked, G-P1-10) | `statefulset` name + `describe` Events + migrate Job status + `pg_isready` output + latest backup time (if recovery is claimed, there must be a backup record) | **Triggerable (provided KSM).** The built-in PG is **single replica, non-HA**; HA is owned by the customer (Patroni / cloud RDS, or switch to external `postgres.host` + `stateStores.enabled=false`). Single replica is a design fact, **not** a capacity conclusion |
| 10 | **`ASServiceEndpointsAbsent`** | P2 `warning`<br/>`state` | The sum of some Service's `kube_endpoint_address_available` is **0**, sustained for **5m** → the selector matches no Ready Pod, and clients cannot route. In-chart covers the two Services `state-redis` and `config-service` | 1) Confirm the `service` name in the alert<br/>2) `kubectl -n <ns> get endpoints <service> -o yaml` (empty ENDPOINTS confirms it)<br/>3) `get pods -l app.kubernetes.io/component=<component>` to align the Deployment and Pods | Distinguish from #4: #4 is "the AS cannot reach Redis", this one is "**the Service has no backend at all**" (Pod does not exist / not Ready / rolling). Look at Pods first, then whether the Service selector matches | Affects `state-redis` → same path as #4, escalate immediately; affects `config-service` → console unavailable, switch to L2 ([L2 §4.6](runbook-l2.md)) | Recover on the Pod side: fix Pod / probes / rolling first, do not directly change the Service selector (the selector is the Deployment contract; changing it silently mismatches) | `service` name + `get endpoints` output + corresponding Pod's `get pods` / `describe` + whether in a rolling window | **Triggerable (provided KSM).** A failure mode **different** from #4: configuration is correct but the Service has no backend |

### 2.4 Three Disciplines for Using This Page

1. **No data ≠ healthy, and ≠ failure.** The §3 blind-spot table explains that in most cases what you get is `no data`. **First judge "is there data", then judge "what the data says"**.
2. **Do not treat ratio thresholds as capacity.** `1%`, `1.3×`, `3 times/minute`, `50 events/15m` are all **pre-existing alert thresholds**, used to detect problems first **when there is no capacity baseline**; **none of them is an answer to O1**.
3. **Demarcation must leave evidence.** If evidence is missing, write the gap into the help ticket; do not substitute speculative conclusions ([`runbook-l1.md`](runbook-l1.md) §4 help evidence checklist).

---

## 3. Blind Spots Not Covered by Alerts

This table matters more than the main table: **it explains "what is not covered right now, why it is not covered, what covers it instead, and what condition can close the gap"**. It must be handed over together during operations handover.

| Blind spot | Reason | Current alternative | Exit condition for closing the gap |
|---|---|---|---|
| **No latency / processing-time alerts** | The repo has **no histogram or summary** at all — `MetricKind` only has `COUNTER` / `GAUGE` ([`metrics.py`](../../platform/src/as_platform/telemetry/metrics.py)). Without a distribution there are no quantiles, so `histogram_quantile` can never get samples | Manual comparison of SIP message timestamps (L2 packet-capture alignment, [`runbook-l2.md`](runbook-l2.md) §3) | ① Add latency instrumentation in `telemetry/metrics.py`; ② a producer on the real SIP path (M7, not a startup probe); ③ scraping wiring closed. **Note**: even if usage-latency ratios or relative regression thresholds are acceptable, **absolute latency thresholds** are equally bound by the O1 discipline (O1 undecided, AGENT.md §2) |
| **No ISC timeout alert** | Same as above: **no timeout counter, and no latency** is exported. Moreover, ownership of ISC triggering lies on the S-CSCF side | Two-sided message alignment forensics (L2); manual cross-checking during integration | ① The SIP adapter exports an ISC timeout counter (with a real producer); ② **negotiate clearly with the operator's S-CSCF side "who judges the timeout"** (an ownership question — resolve it before writing rules) |
| **No session leak alert** | There is no "expected in-flight call count" to serve as a leak baseline. `as_active_calls` is an absolute-unit gauge; using it as a leak threshold is a **capacity number invented ahead of time** (prohibited by AGENT.md §2) | `ASDownscaleBlocked` (#8) covers the **adjacent** failure mode: draining stuck. A genuine "call opened but never closed" can currently only be traced back via complaints / Call-ID traces (ADR-0017) | Either of the two: ① O1 adjudicates a legitimate in-flight call count from M6 measurements; ② export paired "session open / session close" counters, making a leak a **ratio** rather than a threshold |
| **No TLS certificate expiry alert** | **The metric does not exist.** `as_tls_certificate_expiry_seconds` appears only as a naming example in the naming conventions table of `deploy/alerts/README.md`; there is **no such constant** in the code and no producer (that example has been changed to a real metric name in this round's sync) | Customer PKI calendar + customer-side expiry tracking; rotation itself goes through configuration hot update (ADR-0016, [`runbook-l1.md`](runbook-l1.md) §3.4) | The SIP transport exports an expiry gauge per `tls.secretName`, refreshed on the hot rotation path, and the scraping wiring is closed. **The alert target is the customer PKI calendar, not a restart trigger** — rotation never restarts the process, never drops in-flight calls (AGENT.md §13). **E4 / REQ-S-2 / REQ-S-3 currently have no lab evidence** |
| **No configuration drift / rollback alert** | config-service does not export drift and rollback event series. The two names `ASConfigDrift` / `ASConfigRollbackTriggered` **appear only in `templates/NOTES.txt`** and are not in the rule file — searching the alerting system by name will find nothing ([`runbook-l2.md`](runbook-l2.md) §8 item 6) | Query the change order state machine directly ([`runbook-l1.md`](runbook-l1.md) §3.3) + `CONFIG_VERSION` consistency across replicas | config-service exports drift / rollback series to the same scraping path |
| **No rule hit anomaly alert** | `as_rule_hits_total` **has no caller at all**: `record_rule_hit` is defined but nobody calls it in `src/`, so the series is never written | None | ① Connect a producer on the decision path; ② define the anomaly threshold as **relative to its own rolling baseline**, not "hits must not exceed N" (the latter is a capacity number in disguise) |
| **`as_*` metrics cannot be scraped under standard deployment** | ⚠️ **The biggest blind spot.** The Pod template has **no** `prometheus.io/scrape` annotation, and the chart has **no** ServiceMonitor / PodMonitor (no hits across the entire `deploy/helm/templates/` directory). The `/metrics` endpoint works fine, but **no scraper is wired to it** | Manual pull: `kubectl port-forward` + `curl` from check 4 of L1 §1 | The chart adds a Pod annotation or `PodMonitor` / `ServiceMonitor` (chart work, **outside the scope of this deliverable's changes**). **Until closed, do not externally claim the `as_*` rules are "in effect"** |
| **Telemetry drop alert does not trigger under default configuration** | `OTEL_EXPORTER_OTLP_ENDPOINT` defaults to `null` → `BoundedQueueSink` is not created → the series is not written; even if configured, the exporter defaults to `NoOpExporter`, so the queue is hard to fill | No action needed if the call path is unaffected (dropped telemetry is acceptable by design, ADR-0005) | Configure a real OTLP backend and connect a collector. **This is a configuration problem, not a rule problem** — the rule itself is correct |
| **No SIP failure-rate samples under default deployment** | The only write point of `as_sip_responses_total` is the **one-time startup probe** `AS_M5_PROBE_SIP_STATUS`, not set in production on-prem; the path called by the product SIP adapter on every response awaits M7 | Packet-capture alignment (L2 §3) | M7 wiring complete + scraping wiring closed |
| **No test backstop** | **Insufficient e2e end-to-end backstop**: `pytest -m e2e` **8 tests pass stably** (fail, not skip, when the native extension is missing), REQ-F-1 = automated subset covered / full text still open (per-message header differential comparison of the 14 messages still not covered); performance is accept-all harness only, **not the business decision path** (G-P1-2) | Engineering evidence scripts on kind (M5 / ISSU downscale evidence) — **engineering evidence, not production evidence** | M7 / M8 land the e2e layer and make it blocking (AGENT.md §9) |
| **No capacity alerts (`as.capacity`)** | **O1 undecided.** M6 real-socket measurements not complete; AGENT.md §2 / §6 prohibit publishing any capacity number before measurements | Investigate abnormal load with `ASActiveCallsSurge` (#5) + M6 harness; **must not** use numbers made up ahead of time | After O1 is adjudicated by the maintainer based on M6 measurement results, **create** a new `as.capacity` group with thresholds taken from measurements |
| **Diameter Sh / CDR / billing / media alerts** | **N/A, not a blind spot.** All are decided non-goals ([`../../AGENT.md`](../../AGENT.md) §2; review G-P0-4 has removed Sh alerts) | Not applicable | None. If a new requirement arises, it is a new requirement + a new ADR, not a new alert |

---

## 4. Threshold Discipline

### 4.1 Classification of Every Threshold on This Page and in `as-alerts.yaml`

Only three classes of thresholds are **allowed** in the rule file, and every rule's `annotations.description` must self-certify which class it belongs to:

| Class | Meaning | Examples on this page |
|---|---|---|
| **Ratio** | Numerator and denominator same unit, independent of system scale | `ASHighErrorRatio`'s 1% (denominator has `clamp_min(..., 1)`) |
| **Relative change** | Compared against the series' **own** historical baseline, contains no absolute target | `ASActiveCallsSurge`'s 1.3× (30m sliding average) |
| **State condition / fixed-window count** | Boolean reachability, observability, or event count within a fixed window | `ASCallStateStoreUnavailable` (== 0), `ASRestartLoop` (> 3 times/1m), `ASTelemetryDropped` (≥ 50 / 15m), and all 5 added this round (`Ready` being 0, replica count comparison, guard state, StatefulSet ready replicas, Endpoint addresses being 0) |

### 4.2 Why Absolute Capacity Thresholds Are Prohibited

- **AGENT.md §2**: **publish no capacity numbers before M6 measurements** (CPS, concurrency).
- **AGENT.md §6 / §15**: performance testing **may use only real sockets**, never driving callbacks; and before O1 is adjudicated, no capacity number may be assumed.
- **`docs/plan.md` §5.1**: O1 is the largest undecided item, with its own M6 research milestone.
- **Review discipline**: G-P0-3 / G-P0-8 explicitly prohibit capacity alerts and capacity commitment numbers; G-P1-2 requires e2e coverage.
- **The rule file and this page are two carriers of the same discipline**: [`deploy/alerts/README.md`](../../deploy/alerts/README.md) §"Why there is no capacity alert" and §4.1 of this page must be consistent.

### 4.3 Three Questions Before Adding a Threshold

1. Is this number a **ratio / relative change / state**? No → stop and go through O1 + M6.
2. Will it vary with system scale? Yes → it is an absolute number → unqualified.
3. Will someone cite it as "system capacity" a year from now? If the rule description does not state "this is not a capacity metric" → the description is unqualified; return it for rewrite (this is one of the acceptance conditions for new rules).

---

## 5. Consistency Checklist with Other Documents

The following is a self-check list. **Checking a box means this change has been verified item by item**, not that any item has been validated in production.

**Consistency with `runbook-l1.md`**

- [x] **All 10 alerts (3 groups: `as.call-path` 5 + `as.runtime` 3 + `as.platform` 2)** levels, trigger conditions, and L1 actions are **item-by-item consistent** with the [`runbook-l1.md`](runbook-l1.md) §2 table
- [x] `runbook-l1.md` §2's discipline about **series absent (not 0) when `REDIS_URL` is empty** is adopted by #4 on this page
- [x] `runbook-l1.md` §2's pitfall about **`AS_M5_PROBE_SIP_STATUS` being a one-time startup probe** is adopted by §3 and #1 on this page
- [x] `runbook-l1.md` §2's boundary about **`AS_M5_SIMULATED_ACTIVE_CALLS` being an evidence-use simulated value** is adopted by #8 on this page
- [x] The patrol item 4 alert "**absent in Prometheus ≠ the process produced nothing**" is expanded by this page's §3 blind-spot table into a standalone row
- [x] The scraping gap is **consistent in wording** with [`runbook-l2.md`](runbook-l2.md) §8 item 5 (Pod has no scrape annotation, chart has no ServiceMonitor/PodMonitor)
- [x] `ASConfigDrift` / `ASConfigRollbackTriggered` in `NOTES.txt` **do not exist in the rule file** — consistent with [`runbook-l2.md`](runbook-l2.md) §8 item 6
- [x] The 5 new alerts have been **backfilled with corresponding rows** in [`runbook-l1.md`](runbook-l1.md) §2 (including group labels `as.runtime` / `as.platform`), item-by-item consistent

**Consistency with product documents**

- [x] The alert list is item-by-item consistent with **all 10** in [`../product/ne-datasheet.md`](../product/ne-datasheet.md) §6 (trigger condition summary, severity/component, triggerability wording)
- [x] Decision wording is consistent with [`../product/compliance-matrix.md`](../product/compliance-matrix.md): **404** = no matching rule, **603** = policy rejection, both **expected decisions**; the pass-through set {408, 480, 486, 503, 504} is unchanged by this alert
- [x] **487 is excluded** from the failure ratio (caller cancel is normal behavior), consistent with the rule expression
- [x] Ownership judgment wording is consistent with [`../product/responsibility-matrix.md`](../product/responsibility-matrix.md) §3 / §4; the AS side has only its own logs / metrics / configuration versions
- [x] **Zero capacity numbers**: this page contains no CPS / CAPS / BHCA / concurrency ceiling / latency threshold / throughput numbers (§4 classification self-certifies)
- [x] **Contains no Diameter Sh alerts** (removed by G-P0-4; non-goal, `AGENT.md` §2)
- [x] **Contains no CDR / billing / media alerts** (non-goals; appearance means N/A + reason)
- [x] Naming discipline: the product name uses "In-house IMS Application Server"; chart / image / OTel service name `3rdparty-as` unchanged

> **2026-10-12 addition (G8-2)**: the original "naming discipline" row in this block read "In-house IMS Application Server (provisional documentation name)" — the "provisional documentation name" qualifier is outdated: `In-house IMS Application Server` has been formally adopted as the product/documentation description name (G8-2; not a trademark / not a brand claim). This row's checked state and verification conclusion are unchanged; only the naming wording is synced.

**The rule file's own consistency**

- [x] The expressions / labels / annotations of the 5 pre-existing `as-alerts.yaml` rules are **unmodified** (field-by-field validation passed via script comparison against the `HEAD` version)
- [x] All new rules carry `severity` + `component` labels, a one-line `summary`, and a `description` containing the self-certification "this is not a capacity metric"
- [x] kube-state-metrics selectors uniformly use the `$AS_NAMESPACE` placeholder, with no hardcoded namespace
- [x] The metrics of new rules have **all been producer-verified**: `as_downscale_removable` / `as_active_calls` (metrics loop writes unconditionally) + kube-state-metrics (cluster-provided, already used by `ASRestartLoop`)
- [x] No rules were written for **non-exported** metrics (explicit README rule: "Do not add PromQL rules for metrics that are not emitted")
- [x] The file-header SCOPE comment has been updated: stating which two groups were added, why, why there are still no capacity alerts, and declaring it is **not an acceptance record**

---

## 6. Undecided and Blocked

| # | Item | Type | Impact | Ownership / exit condition |
|---|---|---|---|---|
| 1 | **Scraping wiring gap**: Pod has no `prometheus.io/scrape` annotation, chart has no ServiceMonitor / PodMonitor | Blocked | All `as_*` rules (#1–#5, #8) have **no data** under standard deployment, and dashboards are likewise unusable | Requires a chart change (Pod annotation or `PodMonitor`). **Outside the scope of this change**; dashboards and scraping wiring belong to the same pending batch |
| 2 | **O1 capacity target undecided** | Blocked | The `as.capacity` group cannot be established; all absolute thresholds are prohibited | The maintainer adjudicates based on **M6 real-socket measurements** ([`../../AGENT.md`](../../AGENT.md) §2 / §15) |
| 3 | **No latency / ISC timeout metrics** (no histogram / summary) | Blocked | The "ISC timeout" item in deliverable 2.2 **cannot be delivered as an alert** | Requires instrumentation + a real producer + M7 wiring first; ISC timeout also requires negotiating timeout-judgment ownership with the operator's S-CSCF side |
| 4 | **No session leak judgment metric** | Blocked | The "session leak" item in deliverable 2.2 **cannot be delivered as an alert** | Requires O1 to adjudicate a legitimate in-flight call count, or exporting paired "open / close" counts to make it a ratio |
| 5 | **No certificate expiry metric** | Blocked | Certificate expiry reminders can only rely on the customer PKI calendar | Requires exporting an expiry gauge from the SIP transport; and **E4 / REQ-S-2 / REQ-S-3 currently have no lab evidence** |
| 6 | **Insufficient e2e backstop** (G-P1-2) | Blocked | Alert logic has **no end-to-end test backstop**, relying only on static review + kind engineering evidence; `pytest -m e2e` has 8 tests passing stably (REQ-F-1 = automated subset covered / full text still open) | e2e already has 8 tests; the end-to-end backstop and M7 / M8 gating remain pending |
| 7 | **M8 exit sign-off shelved** ([`../plan.md`](../plan.md) §0) | Blocked | **No production-cluster execution records** for all actions on this page | Maintainer sign-off |
| 8 | **7.2d / real-cluster evidence blocked** (G-P1-10) | Blocked | `rollback-playbook.md` and `backup-restore.md` are **written to disk**, but their **real-cluster drill / restore drill records are still blocked**; references on this page are annotated in place; the handling actions on this page **have not been rehearsed on a real cluster** | Requires a real cluster environment + peer (S-CSCF / HSS) cooperation |
| 9 | **O5 / D3 (Redis HA)** | Blocked | Topology values already adjudicated (G7): in-site N+1 + cross-site 1+1 warm standby, Redis primary/replica + Sentinel (ADR-0008, Redis Cluster not chosen); `ASCallStateStoreUnavailable`'s failover window still has no measured evidence (chart renders single replica) | Failover measured behavior forensics + customer-side topology landing; RPO / RTO values still not adjudicated |
| 10 | **Alert list sync between `runbook-l1.md` §2 and `ne-datasheet.md` §6** | **Resolved** | The 5 new rules (`as.runtime` 3 + `as.platform` 2) have been backfilled into both lists; the alert entry sets across the three documents are now consistent with `as-alerts.yaml` (10 rules / 3 groups) | Closed; future new rules must still sync these two places per item 8 of `deploy/alerts/README.md` §Adding a rule |
| 11 | **`ASRestartLoop` selector converges by namespace rather than by Pod** (pre-existing rule, **unchanged** this round, reported only) | Observation | This rule matches restarts of **any** Pod in the namespace (including non-AS workloads). Equivalent to REQ-NF-9's "one namespace, one complete system" under the current chart, but if the customer deploys bypass workloads in the same namespace, the false-positive surface grows | Requires maintainer adjudication: whether to narrow it to `app.kubernetes.io/part-of=3rdparty-as` (depends on KSM's label allowlist, a cluster-side setting). **This round, per discipline, only raises it in the report, without unilaterally modifying the pre-existing rule** |

---

## 7. Source Mapping

| Section on this page | Source |
|---|---|
| Status block and disclaimer | [`../../AGENT.md`](../../AGENT.md) §2 / §6 / §9 / §15; [`../product-packaging-plan.md`](../product-packaging-plan.md) §0.3 and §1 deliverable 2.2; [`../reviews/product-packaging-plan-review-2026-10-09.md`](../reviews/product-packaging-plan-review-2026-10-09.md) (G-P0-3 / G-P0-4 / G-P0-8 / G-P1-2 / G-P1-10); [`../acceptance/report.md`](../acceptance/report.md) §0 |
| §2 pre-existing 5 | [`../../deploy/alerts/as-alerts.yaml`](../../deploy/alerts/as-alerts.yaml) `as.call-path` (original expression, **unchanged this round**); L1 actions taken from [`runbook-l1.md`](runbook-l1.md) §2, triggerability verified from `platform/src/as_platform/__main__.py` and [`ne-datasheet.md`](../product/ne-datasheet.md) §6 |
| §2 new 5 | Same file's `as.runtime` / `as.platform` (added 2026-10-10); producer verification: `platform/src/as_platform/telemetry/metrics.py`, `platform/src/as_platform/__main__.py:_start_metrics_loop`, `platform/src/as_platform/ops/downscale_guard.py`, `deploy/helm/templates/_helpers.tpl`, `deploy/helm/templates/state-{postgres,redis}.yaml`, `deploy/helm/templates/config-service-deployment.yaml` |
| §3 blind spots | [`runbook-l2.md`](runbook-l2.md) §8 pitfall list (items 4/5/6/9/10); scraping gap self-verified: no `prometheus.io/scrape` / ServiceMonitor / PodMonitor across the entire `deploy/helm/templates/` directory; [`../../deploy/alerts/README.md`](../../deploy/alerts/README.md) §Deferred alerts |
| §4 threshold discipline | [`../../deploy/alerts/README.md`](../../deploy/alerts/README.md) §"Why there is no capacity alert"; [`../../AGENT.md`](../../AGENT.md) §2 / §6; the `as-alerts.yaml` file-header SCOPE comment |
| §5 consistency verification | [`runbook-l1.md`](runbook-l1.md) §1 / §2; [`runbook-l2.md`](runbook-l2.md) §4.3 / §4.4 / §4.6 / §4.7 / §8; [`../product/ne-datasheet.md`](../product/ne-datasheet.md) §6; [`../product/compliance-matrix.md`](../product/compliance-matrix.md); [`../product/responsibility-matrix.md`](../product/responsibility-matrix.md) §3 / §4; [`rollback-playbook.md`](rollback-playbook.md), [`backup-restore.md`](backup-restore.md), [`fault-demarcation.md`](fault-demarcation.md) |
| Validation wording | `promtool check rules` / `make alert-check` ([`../../deploy/alerts/README.md`](../../deploy/alerts/README.md) §Loading, §Adding a rule; [`../../Makefile`](../../Makefile) `alert-check`) |
