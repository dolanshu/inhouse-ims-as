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

# Grafana Dashboard Templates — In-house IMS Application Server

> **Status**: deliverable **2.1 Grafana dashboard templates** ([`docs/product-packaging-plan.md`](../../product-packaging-plan.md) §1 second batch #2.1; review comment **G-P0-4** implemented: no Diameter Sh panels, and `sh-interface.json` is **not created** (**G-P2-3**). This directory contains two dashboards: `overview.json` and `sip-signaling.json`.
>
> **⚠️ Availability prerequisite (must read first)**: the AS Pod template has **no** `prometheus.io/scrape` annotation, and the chart has **no** ServiceMonitor / PodMonitor (no grep hits across the entire `deploy/helm/templates/` directory, self-verified 2026-10-10). The `/metrics` endpoint exists and renders the container port `health-http` (`platform/src/as_platform/runtime/health.py`, `health.port` defaults to 8080), but **no scraper is wired to it by the chart**. **Until the scraping wiring is closed, all panels depending on `as_*` will have no data**; panels that do not depend on it (kube-state-metrics / cAdvisor series) depend only on whether the cluster has the corresponding components installed. "Absent in Prometheus" ≠ "the process produced nothing" — for manual verification methods see [`../runbook-l1.md`](../runbook-l1.md) §1 check 4.
>
> **Zero capacity numbers / no latency panels**: this directory **contains no capacity numbers** (no CPS / CAPS / BHCA / concurrency / throughput / latency / resource quotas); the O1 capacity target is **undecided**, and `AGENT.md` §2 prohibits publishing any such numbers before M6 real-socket measurements, so this directory **does not cite** M6 dev-host measurements. **Latency panels likewise do not exist**: this repo has no histogram / summary — `MetricKind` only has `COUNTER` and `GAUGE` (`platform/src/as_platform/telemetry/metrics.py`), and the registry has no latency or throughput series; the "latency P50/P95/P99" wording in the original plan document 2.1 is therefore **undeliverable**, and building it would be a fake panel (§4).
>
> **No Sh panels / terminology discipline**: `AGENT.md` §2 explicitly says **no Diameter Sh**, which is an out-of-scope non-goal (N/A, not a defer), so not even a placeholder panel is built. "v1" and "v1.1" are **not release versions**; nothing in this directory **constitutes an acceptance conclusion** — M5 engineering closure ≠ REQ acceptance, **M8 RC readiness ≠ closure**, E1/E4/E5 are still not accepted, and e2e: `pytest -m e2e` **8 tests pass stably** (fail, not skip, when native is missing), REQ-F-1 = automated subset covered / full text still open (performance is accept-all harness only, not the business decision path).
>
> **B6 review status**: this document has been reviewed under B6 with a review record left — [`../../reviews/product-packaging-review-checklist-2026-10-12.md`](../../reviews/product-packaging-review-checklist-2026-10-12.md) §6 (2026-10-12 first review) and §7 (2026-10-12 closure re-review); **the conclusion awaits maintainer confirmation** and must not serve as a basis for external delivery or acceptance before confirmation (`AGENT.md` §3.3).

---

## 1. Positioning and Panel List of the Two Dashboards

`overview.json` (`uid: as-overview`, 15 panels) — overall health / session counts / throughput observation / state store / runtime.
`sip-signaling.json` (`uid: as-sip-signaling`, 7 panels) — SIP signaling details and decisions.

### 1.1 `overview.json`

| # | Panel | Metric / expression key points | Data source | Prerequisite | Wording reminder |
|---|---|---|---|---|---|
| 1 | State store reachability (current value) | `min by (use_case) (as_state_store_available)` | AS `/metrics` | Scraping wiring + `REDIS_URL` non-empty | Series **absent ≠ 0**; reachability state, not capacity |
| 2 | Pod Ready status (current value) | `max by (pod) (kube_pod_status_ready{namespace=~"$AS_NAMESPACE", condition="true"})` | kube-state-metrics | Cluster has kube-state-metrics installed | While draining, `/health/ready` returns 503 (ADR-0009) |
| 3 | Deployment replicas: desired / available | `kube_deployment_spec_replicas` / `..._status_replicas_available` | kube-state-metrics | Same as above | Only reflects the published integers, **does not say how many replicas the system should have** (O1) |
| 4 | In-flight calls per use case | `sum by (use_case) (as_active_calls)` | AS `/metrics` | Scraping wiring | Written unconditionally every 15s; a quantity observation, no upper-bound threshold |
| 5 | In-flight calls per Pod | Single target: `as_active_calls` (not aggregated; legend `{{pod}} / {{use_case}}`, refId `A`) | AS `/metrics` | Scraping wiring | The downscale guard needs **per-instance** values (ADR-0010); aggregated averages mask single points |
| 6 | Downscale guard status | `max by (pod, use_case) (as_downscale_removable)` | AS `/metrics` | Scraping wiring | 1 = drainable, 0 = carrying calls **or** draining; no threshold ("greater than 0 means protected" is an implementation wording, not a capacity conclusion) |
| 7 | SIP response rate | `sum by (use_case, status_class) (rate(as_sip_responses_total[5m]))` | AS `/metrics` | Scraping wiring + **no producer in production** | A rate observation, not throughput capability |
| 8 | Failed response ratio | Ratio expression with the same wording as `ASHighErrorRatio` | AS `/metrics` | Same as above | **A ratio is not a capacity metric**; the panel draws no threshold line, the sole maintenance point for thresholds is `as-alerts.yaml` |
| 9 | Rule hit rate | `sum by (rule) (rate(as_rule_hits_total[5m]))` | AS `/metrics` | **No caller at all → no data expected** | The panel is retained only to make the gap discoverable; the anomaly wording can only be relative to baseline |
| 10 | State store reachability history | `min by (use_case) (as_state_store_available)` | AS `/metrics` | Same as panel 1 | The historical view of panel 1 |
| 11 | Telemetry drop rate | `sum by (use_case) (rate(as_telemetry_dropped_total[5m]))` | AS `/metrics` | Scraping wiring + `OTEL_EXPORTER_OTLP_ENDPOINT` non-empty | The chart defaults `telemetry.otlpEndpoint: null` → no data |
| 12 | CPU usage (per Pod) | `sum by (pod) (rate(container_cpu_usage_seconds_total{namespace=~"$AS_NAMESPACE", container!="POD"}[5m]))` | kubelet / cAdvisor | Cluster provides kubelet metrics | Resource observation; no requests/limits commitment |
| 13 | Memory working set (per Pod) | `sum by (pod) (container_memory_working_set_bytes{...})` | kubelet / cAdvisor | Same as above | **Must not be used as a session leak baseline** (would reverse-engineer capacity numbers) |
| 14 | Pod container restart increase | `sum by (pod) (increase(kube_pod_container_status_restarts_total{namespace=~"$AS_NAMESPACE"}[1m]))` | kube-state-metrics | Cluster has kube-state-metrics installed | The only panel independent of AS scraping wiring; crash loop ≠ overload |
| 15 | Service available endpoint count | `sum by (service) (kube_endpoint_address_available{namespace=~"$AS_NAMESPACE"})` | kube-state-metrics | Same as above | Routing state, not a connection pool, not capacity |

### 1.2 `sip-signaling.json`

| # | Panel | Metric / expression key points | Data source | Prerequisite | Wording reminder |
|---|---|---|---|---|---|
| 1 | SIP response rate (by use_case + status_class) | `sum by (use_case, status_class) (rate(as_sip_responses_total[5m]))` | AS `/metrics` | Scraping wiring + no producer in production | **No inbound/outgoing leg dimension**: the repo has no `direction` label, so it is not split and not fabricated |
| 2 | Response status class distribution | `sum by (status_class) (rate(as_sip_responses_total[5m]))` | AS `/metrics` | Same as above | 487 is a normal cancel; 404/603 are decision results |
| 3 | Response code counts of interest 403 / 404 / 603 / 502 | 4 queries with exact `status_code` filtering + `increase(...[5m])` | AS `/metrics` | Same as above | **403** inbound leg not authorized; **404 / 603 are decision results, expected behavior**; **502** is the unified mapping of downstream non-2xx (outside the passthrough set {408,480,486,503,504}) — wording evidence see [`../../product/compliance-matrix.md`](../../product/compliance-matrix.md) §3 |
| 4 | Decision hit rate by rule | `sum by (rule) (rate(as_rule_hits_total[5m]))` | AS `/metrics` | **No producer → no data expected** | An absolute threshold is a capacity number in disguise, prohibited |
| 5 | Alert status (firing / pending) | `count by (alertname, severity) (ALERTS{alertstate="firing"\|"pending"})`, `instant: true` | Prometheus computed series | **Requires Alertmanager + `as-alerts.yaml` loaded** | Having data ≠ rules are triggerable (see `deploy/alerts/README.md` §Metric contract); handling see [`../alert-response-matrix.md`](../alert-response-matrix.md) |
| 6 | Session and draining linkage | `as_active_calls` (left axis) + `as_downscale_removable` (right axis, right axis override `max: 1`) | AS `/metrics` | Scraping wiring | "Both 0 yet persistently not decreasing" = draining not converging (`ASDownscaleBlocked`) |
| 7 | Failed response ratio per use case | Ratio with the same wording as `ASHighErrorRatio`, split by `use_case` | AS `/metrics` | Scraping wiring + no producer in production | A ratio, not capacity; no threshold line drawn |

> **Why there is no "inbound leg / outgoing leg" panel**: the delivery requirement mentions inbound/outgoing leg response rates, but `as_sip_responses_total`'s labels are only `use_case` / `status_class` / `status_code` (`metrics.py`'s `_LABEL_*` constants), and there is **no** label like `direction`; the two-leg distinction of the two-legged B2BUA is an internal product structure (independent Call-IDs per leg), with no corresponding metric label currently. Therefore **no panel is built and no label is fabricated**; the closing path see §4.

---

## 2. Prerequisites and Current Wiring Status

| What is needed | Current status | Evidence | Suggested closing method (suggestion only; this deliverable does not modify the chart) |
|---|---|---|---|
| AS `/metrics` scraping | ❌ **Not wired.** The Pod template has no `prometheus.io/scrape` annotation (the only annotation is `checksum/config`); the chart has no ServiceMonitor and no PodMonitor | `deploy/helm/templates/deployment.yaml`; no grep hits for `prometheus.io/scrape` / `ServiceMonitor` / `PodMonitor` across the entire `deploy/helm/templates/` directory; `deploy/alerts/README.md` §Scrape wiring status | Either: ① add `prometheus.io/scrape` + `prometheus.io/port` (port name `health-http`, `health.port` defaults to 8080) annotations to the Pod template; ② add a `PodMonitor`/`ServiceMonitor` pointing at `health-http`. This is chart work and needs a separate change |
| OTLP export backend | ❌ Not configured. `telemetry.otlpEndpoint` defaults to `null`, in which case the sink is `NoOp`; even with an endpoint configured, the exporter still defaults to `NoOpExporter` | `deploy/helm/values.yaml` (telemetry section); `deploy/alerts/README.md` §Metric contract | Point to a real OTLP collector on the deployment side. **Note: this only affects whether `as_telemetry_dropped_total` has data, not the `/metrics` text export** |
| `$AS_NAMESPACE` substitution | ⚠️ The dashboards use the Grafana template variable `AS_NAMESPACE` (`type: custom`, default value `as-prod`); in the alert rule file it is the literal placeholder `$AS_NAMESPACE` | `deploy/alerts/as-alerts.yaml` file header; the `templating.list` of the two JSON files in this directory | After import, change it to the customer namespace in the dashboard variables; on the alert side, substitute at load time with `envsubst` or `PrometheusRule` templating. **One namespace = one complete system** (REQ-NF-9), which is also the isolation boundary of all kube-state-metrics selectors |
| kube-state-metrics | ⚠️ **Provided by the cluster side; neither this repo nor the chart installs it.** Not installed → panels 2 / 3 / 14 / 15 have no data | `deploy/alerts/README.md` §Kubernetes standard series | Installed in the cluster by operations; this dashboard does not depend on a chart change |
| cAdvisor / kubelet metrics | ⚠️ Provided by the cluster side. Panels 12 / 13 depend on `container_cpu_usage_seconds_total` / `container_memory_working_set_bytes` and the `namespace` / `pod` / `container` labels | Same as above | If the cluster drops the `container` label during the relabel stage, panels aggregated by `pod` remain usable (the dashboards do not rely on narrowing by the `container` label) |
| Alertmanager | ⚠️ Provided by the cluster side. Panel 5 depends on the `ALERTS` series, which Prometheus computes from loaded rules | `deploy/alerts/as-alerts.yaml`; `deploy/alerts/README.md` §Loading | Load the rule file (`rule_files:` or `PrometheusRule`) and validate with `promtool check rules` |

**The dashboards themselves do not change any wiring status**: before row 1 in §2 is closed, `overview.json` panels 1, 4–13 and `sip-signaling.json` panels 1–4, 6, 7 will all **have no data**; this directory does not describe "not wired" as "in effect".

---

## 3. Import Steps

1. **Grafana UI import**: `Dashboards → New → Import → Upload JSON file`, uploading `overview.json` and `sip-signaling.json` respectively. On import, Grafana will prompt for a data source; just pick the Prometheus instance; the `uid`s are fixed (`as-overview` / `as-sip-signaling`), so re-importing overwrites the same one, avoiding duplicate copies.
2. **Change the namespace variable**: after import, open the dashboard → top right Dashboard settings → Variables → `AS_NAMESPACE`, and change the default value `as-prod` to the actual customer namespace. You can also temporarily override it in the URL with `?var-AS_NAMESPACE=<ns>`. Both non-`as_*` (kube-state-metrics / cAdvisor) queries go through this variable.
3. **Data source variable**: the `datasource` variable in `templating` (`type: datasource`, `query: prometheus`) automatically lists instances; all panels' `datasource` fields reference `${datasource}`, so in multi-Prometheus-instance scenarios, switching once takes effect globally.
4. **provisioning directory placement** (recommended for delivery environments, versionable):
   ```yaml
   # grafana/provisioning/dashboards/as.yaml (example; this repo does not provide this file)
   apiVersion: 1
   providers:
     - name: as
       orgId: 1
       folder: AS
       type: file
       disableDeletion: false
       updateIntervalSeconds: 60
       options:
         path: /etc/grafana/provisioning/dashboards/as
   ```
   Put the two JSON files in the directory pointed to by `path`, and Grafana will load them idempotently by `uid` (auto-refresh when `updateIntervalSeconds` expires). **provisioning only solves "the dashboards exist", not the scraping wiring in §2**.
5. **Post-import self-check**: whether panels 2 / 3 / 14 / 15 have data → judge whether the cluster has kube-state-metrics installed; whether panels 1 / 4 have data → judge whether the scraping wiring is closed; panels 9 / 3 (SIP side) **having no data is the expected result** (no producer), not an import failure.

---

## 4. Deliberately Omitted Panels and Reasons

| Not doing | Reason | When it can be done |
|---|---|---|
| **Diameter Sh related panels** (including placeholder panels) | **N/A, not a defer.** `AGENT.md` §2 explicitly says no Sh; review **G-P0-4** requires removing Sh panels and alerts, and **G-P2-3** requires deleting the `sh-interface.json` file entry | **Never** (unless a new requirement + a new ADR appears). If someone asks for an Sh panel again, that is a new requirement, not a gap in this dashboard |
| **Latency P50 / P95 / P99, ISC round-trip latency, SIP processing time** | The repo has **no** histogram / summary: `MetricKind` only has `COUNTER` / `GAUGE`, and the registry has no latency series (`metrics.py`; `docs/product/ne-datasheet.md` §5 explicitly states "there are currently no latency-type KPIs"). `histogram_quantile` would forever point at empty series — building it would be a **fake panel**, worse than none | First add latency instrumentation (histogram or summary) in `telemetry/metrics.py` → a producer on the real SIP path → scraping wiring closed. **And** any absolute latency threshold is still bound by O1: relative regression can be stated, but "must respond within N ms" cannot be stated before M6 measurements |
| **Capacity panels** (CPS / concurrent sessions / per-Pod load ceiling / HPA targets) | **O1 undecided**; publishing any capacity number before M6 measurements is prohibited (`AGENT.md` §2; the `deploy/helm/values.yaml` autoscaling section is all blank with a note "filled values must come from M6 measurements"). The `as.capacity` group deliberately does not exist | After O1 is adjudicated by the maintainer based on M6 real-socket measurements, create it per measured values, **must not be written by intuition** |
| **Inbound / outgoing leg response rates** (split by direction) | `as_sip_responses_total` has only three labels `use_case` / `status_class` / `status_code`, and **no** `direction`. Fabricating a label would make the dashboard forever have no data | The SIP adapter layer adds a `direction` (or equivalent) label when writing on the real response path, and synchronously updates the `metrics.py` contract table and `deploy/alerts/README.md` |
| **Rule hit anomaly panels** (threshold line / absolute ceiling) | `as_rule_hits_total` **has no caller at all**, so the series is never written; and an absolute threshold is a capacity number in disguise | ① connect a real producer on the decision path; ② change the anomaly wording to a **relative** change against its own rolling baseline. Only when both conditions are met can it be added |
| **Session leak panels** (using as_active_calls as baseline) | There is no "legitimate in-flight call count" — that is exactly O1. Using it as a baseline is inventing a capacity number | O1 adjudicates a legitimate in-flight volume, or export paired "session open / close" counts to make a leak a **ratio** |
| **Connection pool / connection count panels** | The plan document 2.1's original text mentions "connection pool", but the repo **does not export any connection pool or connection count metric**, and Redis / PostgreSQL client connection counts have no series. Panel 15 (Service available endpoint count) is the closest cluster-side substitute, indicating routing state only | The state store client exports connection-related gauges, synced with the `deploy/alerts/README.md` contract table |
| **TLS certificate expiry panel** | The metric does not exist (`as_tls_certificate_expiry_seconds` is only an illustrative name in the naming conventions table; there is no such constant in the code and no producer) | The SIP transport layer exports an expiry gauge per `tls.secretName`, refreshed via the ADR-0016 hot rotation path, and the scraping wiring is closed |
| **Configuration drift / rollback panel** | config-service does not export related series. `ASConfigDrift` / `ASConfigRollbackTriggered` appear only in `deploy/helm/templates/NOTES.txt` — **a name appearing in NOTES.txt does not mean a metric exists** (`../runbook-l2.md` §8 item 6) | config-service connects drift / rollback event series into the same scraping path |
| **CDR / billing / media (RTP / transcoding) panels** | **N/A, not a defer.** ADR-0017 does no CDR / billing, ADR-0004 has no media plane — there is nothing observable | **Never** (new requirement + a new ADR counted separately) |

---

## 5. Metric Contract and Change Discipline

- **Sole authority**: `platform/src/as_platform/telemetry/metrics.py`. These dashboards use only the **6** `as_*` metrics defined therein: `as_active_calls{use_case,pod}`, `as_downscale_removable{use_case,pod}`, `as_state_store_available{use_case}`, `as_sip_responses_total{use_case,status_class,status_code}`, `as_rule_hits_total{rule}`, `as_telemetry_dropped_total{use_case}`. The authoritative description and per-item producer verification see [`../../../deploy/alerts/README.md`](../../../deploy/alerts/README.md) §Metric contract.
- **Non-`as_*` metrics** (kube-state-metrics / cAdvisor / `ALERTS`) are provided by the **cluster or Prometheus**, not produced by this repo; the selector discipline is consistent with `as-alerts.yaml`: only `namespace=~"$AS_NAMESPACE"` is used, **without narrowing by `label_*`** — kube-state-metrics only exposes `label_*` series when a label allowlist is configured, which is a cluster-side setting, and the chart must not assume it.
- **`$AS_NAMESPACE` appears only in kube-state-metrics / cAdvisor selectors**. The `as_*` series' own labels are only those in the table above (**no `namespace`**); adding a namespace matcher to it would make queries perpetually empty when the scraping configuration does not inject that label. Instance ownership of `as_*` is identified by the `pod` label.
- **Renaming must be synced in the same change**: both rules and dashboards depend on metric names. If a rename is not synced, rules will **silently stop matching** — worse than having no rules. Therefore any metric rename must update in the **same commit**: `metrics.py` → the `deploy/alerts/README.md` contract table → `as-alerts.yaml` → **the two JSON files in this directory** → `docs/product/ne-datasheet.md` §5 → `docs/operations/alert-response-matrix.md`.
- **New metrics must have a producer first**: before writing a panel, first grep the metric name and read the write point. For metrics that are only startup probes, test harnesses, or have no caller at all, the panel can only be "no data expected" (panels 9 / SIP panel 4 are of this kind), and the reason must be stated in the `description`.
- **Thresholds are maintained in one place only**: panels **deliberately draw no** alert threshold lines. All thresholds are written in `deploy/alerts/as-alerts.yaml`, whose `description` already notes "not a capacity metric". Drawing it once each in both dashboards and rules will drift.
- **Do not promise things not in effect**: the fact that the scraping wiring is not closed (row 1 in §2) must be delivered together with the dashboards, and the `as_*` rules or panels must not be described as "already in effect in production" in customer materials.

---

## 6. Maintenance and Validation

**JSON structure validation** (both files must pass):

```sh
python3 -c "import json; [json.load(open(f)) for f in ['docs/operations/grafana-dashboards/overview.json','docs/operations/grafana-dashboards/sip-signaling.json']]"
```

**Recommended minimal self-check before import** (not dependent on a Grafana instance):

1. The JSON parsing above passes (syntax level);
2. Every panel has `id` / `type` / `title` / `gridPos` / `datasource` / `targets` / `fieldConfig` / `options`;
3. `as_*` metric names appearing in `targets[].expr` ⊆ the 6 whitelist in §5, and only the labels that actually exist are used for `as_*`: `use_case` / `pod` / `status_class` / `status_code` / `rule`;
4. The full text contains no `histogram_quantile`, no Sh-related panel titles, and no capacity numbers or threshold lines;
5. The `datasource` and `AS_NAMESPACE` variables both exist in `templating.list`, and all PromQL uses variables rather than hardcoded namespaces.

**Suggested inclusion in gates**: use step 1's `python3 -c` as the minimum bar (on par with `promtool check rules`); the semantic checks in steps 3 and 4 currently rely on manual review, and if automation is needed later, a read-only validation script can be added — but **this deliverable adds no new script files**, to avoid conflicting with the "only create 3 files" scope constraint.

**Panel review discipline**: before changing a panel, first ask "does this metric have a producer", and if the answer is "no", do not build the panel (if it must be built, state "no data expected" and the reason); any new panel must state its wording, the **not a capacity metric** reminder (for amount / ratio panels), and prerequisites in the `description` (JSON has no comments, so descriptions can only go in `description` or this README).
Panel wording is kept consistent with `docs/product/ne-datasheet.md` §5/§6, `docs/product/compliance-matrix.md` §3, and `deploy/alerts/README.md`; on inconsistency, the code and the above authoritative documents prevail, and the dashboards are corrected accordingly. Terminology discipline: the product name is uniformly **In-house IMS Application Server** (formally adopted as the product/documentation description name, G8-2; not a trademark / not a brand claim); the chart / image / OTel service name remains `3rdparty-as`; `state-*` refers to the bundled Redis / PostgreSQL (ADR-0026 Option E), with HA belonging to the customer side (O5 / D3 values adjudicated (G7): in-site N+1 + cross-site 1+1 warm standby, Redis primary/replica + Sentinel; the chart still renders single replica, with no evidence of measured failover behavior).
