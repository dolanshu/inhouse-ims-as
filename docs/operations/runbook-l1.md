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

# L1 Operations Runbook (NOC Daily and Alert Handling) — In-house IMS Application Server

> **Audience**: L1 / NOC on-duty. **Does not include** deep signaling analysis (see [`runbook-l2.md`](runbook-l2.md)).
>
> **Evidence wording (must read)**: **all conclusions on this page are based on engineering slice evidence**.
> - **M5 engineering closure ≠ REQ acceptance**; **M8 RC readiness ≠ closure** ([`../acceptance/report.md`](../acceptance/report.md) §0).
> - **Current e2e state**: `pytest -m e2e` **8 tests pass stably** (Wave 1 five tests `testbed/e2e/test_sip_first_edition.py` + Wave 2 three tests `testbed/e2e/test_s1_replay_contract.py`; **fail, not skip**, when the native extension is missing), REQ-F-1 = **automated subset covered / full text still open** (covered: two-leg normalized message sequence differential comparison, C_in ≠ C_out, byte-identical SDP offer; **per-message header differential comparison of the 14 messages is still not covered**); performance is accept-all harness only, **not the business decision path** (G-P1-2).
> - **Evidence boundary for simulated `active_calls`**: no-dropped-call evidence for downscale / draining / rolling upgrade comes from `AS_M5_SIMULATED_ACTIVE_CALLS` simulation on kind; **not dropping calls under real SIP load awaits M7 / M8 acceptance** (G-P1-1).
> - **Zero capacity numbers**: this page has no CPS / CAPS / BHCA / concurrency / throughput / latency / percentage capacity (O1 undecided). Percentages and fixed-window counts appearing in the table are **pre-existing alert thresholds**, not capacity metrics.
> - **Originals preserved**: this page is a **collection and reorganization** of existing runbooks under [`../acceptance/`](../acceptance/); the original files are **not deleted, not moved, not rewritten**. Source links are given at the end of each section; the evidence originals are there.
>
> **B6 review status**: this document has been reviewed under B6 with a review record left — [`../reviews/product-packaging-review-checklist-2026-10-12.md`](../reviews/product-packaging-review-checklist-2026-10-12.md) §6 (2026-10-12 first review) and §7 (2026-10-12 closure re-review); **the conclusion awaits maintainer confirmation** and must not serve as a basis for external delivery or acceptance before confirmation (`AGENT.md` §3.3).

---

## 1. Daily Patrol Checklist

Prerequisites: kubeconfig points at the target cluster; namespace per the site (examples on this page use the chart default `as-prod`; in practice, follow `helm get values` / installation parameters).

| # | Check item | Command / method | Expected result | Where to jump on anomaly | Basis |
|---|---|---|---|---|---|
| 1 | Pod status and ready | `kubectl -n as-prod get pods -l app.kubernetes.io/part-of=3rdparty-as` | Every use-case Pod `Running` with all READY true; no CrashLoop / no Pending | READY not true → §4; restarts → §2 `ASRestartLoop` | Label definitions `deploy/helm/templates/_helpers.tpl:55,71` |
| 2 | Health endpoints | In-container probes are configured; for manual checking use `kubectl -n as-prod port-forward deploy/<release>-<use-case> 8080:8080` then access `/health/live`, `/health/ready` | `/health/live` 200; `/health/ready` 200 | `/health/ready` **503** = draining (normal traffic removal in progress), see §3.1; persistent 503 → §4 | The port comes from Helm `health.port` (`deploy/helm/values.yaml:281-282`) → ConfigMap `AS_HEALTH_PORT` (`templates/configmap.yaml:58`); paths from `values.yaml:286-303` |
| 3 | Configuration version consistency | `kubectl -n as-prod exec deploy/<release>-<use-case> -- printenv CONFIG_VERSION` | All replicas' `CONFIG_VERSION` are identical and equal to the console's currently effective version | Inconsistent → §3.3; empty value = instance has not reported yet → §4 | Commands as written see `deploy/helm/templates/NOTES.txt:47-51` (injected by config-service grayscale distribution, ADR-0006) |
| 4 | Metric availability | `kubectl -n as-prod exec deploy/<release>-<use-case> -- curl -s :8080/metrics \| grep '^as_'` (the port comes from `health.port`; when `curl` is not in the image, use `kubectl -n as-prod port-forward deploy/<release>-<use-case> 8080:8080` then locally `curl -s localhost:8080/metrics \| grep '^as_'`) | Can list session / decision related `as_*` series | Cannot list → §4. **Note: the chart has not wired scraping** (no scrape annotation, no ServiceMonitor), so "absent in Prometheus" does not equal "the process produced nothing" | Endpoint implementation `platform/src/as_platform/runtime/health.py`; ⚠️ gap see L2 §8 |
| 5 | ingress HTTPS redirect | `curl -I -H 'Host: <ingress-host>' http://ingress-nginx-controller.ingress-nginx.svc/` | **301 / 308** (HTTP via the ingress is redirected or rejected) | Not 301/308 → §4; **empty reply (curl 52) is treated as not passed**, the environment must be fixed or the evidence path changed | [`../acceptance/m5-7.2d-ingress-runbook.md`](../acceptance/m5-7.2d-ingress-runbook.md) check item 4; **port-forward HTTP 200 cannot substitute for this item** |
| 6 | Redis availability | Metric `as_state_store_available{use_case}` (method same as #4) | `1` | `0` → §2 `ASCallStateStoreUnavailable` + §4; **series absent ≠ 0** (not produced when `REDIS_URL` is not configured) | `deploy/alerts/README.md` §Metric contract |
| 7 | PostgreSQL availability | Executed by the platform side on the governance database host with `pg_isready` (owner / operations account, not the application role) | Accepts connections | Failure → §4 | Role and DSN wording see §3.5 and L2 §6 |
| 8 | Console can log in | Access the console HTTPS entry from a browser and log in as operator | Login succeeds and the approval queue is visible | Failure → §4; **do not save credentials**, do not file session cookie screenshots | [`runbook-l2.md`](runbook-l2.md) §4.6 |

> ⚠️ **Current limitation (factually noted)**: execution records of the above check items on a **real production cluster are currently blocked** — M4b-7.2d / M8 7.2d are still **blocked** (source: `docs/product-packaging-plan.md` §3.2 deliverable 2.4 row "2.4 / 2.5 real-cluster drills (iFC cooperation, backup and restore)… M8 real-cluster environment (7.2d still blocked), and 2.4 additionally requires S-CSCF/HSS side cooperation"). What this page gives is **executable actions**, and **must not** be used to write "already validated in production" in any material. Likewise, L1's evidence base is kind / compose, **not production**.

---

## 2. Alert Handling (L1 Perspective)

Sole authority for rules: [`../../deploy/alerts/as-alerts.yaml`](../../deploy/alerts/as-alerts.yaml) (REQ-NF-14); loading and validation see [`../../deploy/alerts/README.md`](../../deploy/alerts/README.md). **The table below covers all 10 rules and 3 groups of that file item by item** (`as.call-path` 5 + `as.runtime` 3 + `as.platform` 2). This table only does the L1 first response; **escalation path** and demarcation see [`alert-response-matrix.md`](alert-response-matrix.md) (written to disk; item-by-item consistent with this table).

| Alert | Level / component | One-sentence meaning | L1 action | When to escalate to L2 | Current triggerability (self-verified) |
|---|---|---|---|---|---|
| `ASHighErrorRatio` | `warning` / `signalling` | Ratio of 5xx and non-487 4xx to all SIP responses > **1%**, sustained for `10m` (**pre-existing alert threshold, not a capacity metric**) | Note the time window; confirm whether `as_sip_responses_total` really has samples; do not judge it as a "failure" when there is no data | Real samples with a persistently rising ratio → L2 (L2 §4.3 / §4.4) | **Not triggerable**: depends on `as_sip_responses_total`, which has no data producer on the production path (the only write point is the one-time startup probe `AS_M5_PROBE_SIP_STATUS`, not set in production on-prem) |
| `ASTelemetryDropped` | `warning` / `observability` | `as_telemetry_dropped_total` increase ≥ **50** within a `15m` window, sustained for `15m` (**event count within the window, not a capacity metric**) | Confirm whether `telemetry.otlpEndpoint` is configured; if not configured, this series never produces data in the first place | Configured backend yet sustained drops → L2 | **Not triggerable**: the bounded queue is enabled only when an OTLP endpoint is configured (the chart defaults to `null`), and the exporter is currently `NoOpExporter` |
| `ASRestartLoop` | `critical` / `runtime` | Single Pod container restarts **> 3 times / 1 minute** (**fixed-window liveness signal, not a capacity metric**) | `kubectl -n as-prod describe pod <pod>` + get the previous container's logs; check the latest configuration version | Repeated restarts / involves multiple Pods → L2 | **Triggerable (currently the only one with no prerequisite)**: the data source is external **kube-state-metrics**'s `kube_pod_container_status_restarts_total`, requiring only that the cluster has kube-state-metrics installed |
| `ASCallStateStoreUnavailable` | `critical` / `state` | `min by (use_case) (as_state_store_available) == 0`, sustained for `2m` (**reachability state condition, not a capacity metric**) | Escalate to L2 immediately; the AS side's session / dialog / anti-fraud rate-window state is all in Redis | **Immediately** (critical, and in-flight calls cannot be sustained) | **Triggerable (provided `REDIS_URL` is configured)**: at that point it really `PING`s Redis and writes the series. When `REDIS_URL` is empty the **series does not exist (not 0)**, so the rule never triggers |
| `ASActiveCallsSurge` | `warning` / `signalling` | Current `as_active_calls` per use case > **1.3×** its own `30m` sliding average, sustained for `10m` (**relative change, structurally contains no absolute call count, not a capacity metric**) | Judge it as "the traffic shape changed"; first look at whether there is any change / traffic removal / upstream action; **must not** infer a capacity ceiling from this | Accompanied by a rising error ratio or state store alert → L2 | **The series is always produced**, but the values depend on dialog events from the SIP runtime; does not trigger when that runtime is not enabled or the count is constantly 0. Also see the scraping wiring gap in §1 #4 |
| `ASPodNotReady` (`as.runtime`) | `critical` / `runtime` | That Pod's `Ready` condition is **0**, sustained for `5m`; ready = the process is **rejecting new work** (**readiness state condition, not a capacity metric**) | First distinguish "normal traffic removal" from "stuck": `/health/ready` **503 = draining (normal traffic removal in progress)**, persistent 503 is the anomaly; then look at `describe pod`'s Events (probes / mounts / image) | Draining not converging / repeatedly not-ready → L2 (L2 §4.7); appears together with `ASRestartLoop` → handle as CrashLoop | **Triggerable (provided the cluster has kube-state-metrics installed)**: looks only at Pods in the AS namespace, **without distinguishing components** (AS engine / `state-redis` / `state-postgres` / `config-service`), distinguished by `pod` name |
| `ASDeploymentReplicasUnavailable` (`as.runtime`) | `warning` / `runtime` | The same Deployment's available replica count < desired replica count, sustained for `10m` (**replica availability state condition, not a capacity metric**) | First look at the `deployment` label in the alert — it may be the use-case Deployment, `state-redis`, or `config-service`; then `get deploy` + `describe`; judge together with `ASPodNotReady` (usually two views of the same event) | Insufficient use-case replicas affecting business → L2; `state-redis` unavailable → same path as `ASCallStateStoreUnavailable`, escalate immediately | **Triggerable (provided KSM)**: the selector **is limited by namespace**, so it also covers the two built-in Deployments `state-redis` and `config-service` |
| `ASDownscaleBlocked` (`as.runtime`) | `warning` / `runtime` | On the same `pod` / `use_case`, `as_downscale_removable == 0` **and** `as_active_calls == 0`, sustained for `30m`. ADR-0010's guard has only two interception reasons (in-flight calls / already draining), and with both excluded only "**draining stuck**" remains (**guard state condition, not a capacity metric**) | Confirm both series are produced (method same as §1 #4); look at whether that Pod's `/health/ready` is persistently **503**; merge with `ASPodNotReady`: very likely not-ready at the same time on the same Pod | Persistently not converging → L2 (L2 §4.7); involves multiple Pods or affects the release window → escalate immediately. **Must not** directly delete the Pod or SIGKILL — drain fully first (ADR-0009 / ADR-0010) | **The series is always produced** (the metrics loop writes unconditionally, not dependent on OTLP), but the values depend on real SIP dialog activity — does not trigger with no traffic. Also see the scraping wiring gap in §1 #4 |
| `ASStatefulSetUnavailable` (`as.platform`) | `critical` / `state` | Some StatefulSet's ready replica count < desired replica count, sustained for `5m`; in-chart this is the **governance database PostgreSQL** (ADR-0008) (**replica readiness state condition, not a capacity metric**) | Confirm the `statefulset` name in the alert (expected `<release>-postgres`); `get sts` + `describe`; check the recent migrate Job; `pg_isready` on the governance database host | **Immediately** L2 → maintainer. The governance PG holds configuration versions, change orders, and the append-only audit chain → **configuration cannot be approved or distributed**; pause change order approval first | **Triggerable (provided KSM)**: the built-in PG is **single replica, non-HA** (HA owned by the customer; the Redis HA topology values are adjudicated — **O5 / D3 (G7)**: in-site N+1 + cross-site 1+1 warm standby, Redis primary/replica + Sentinel, following the ADR-0008 topology, not Redis Cluster; the chart currently still renders single replica, with no evidence of measured failover behavior) — single replica is a design fact, **not** a capacity conclusion |
| `ASServiceEndpointsAbsent` (`as.platform`) | `warning` / `state` | Some Service's available endpoint address count is **0**, sustained for `5m` → the selector matches no Ready Pod, and clients cannot route (**routing state condition, not a capacity metric**) | Confirm the `service` name in the alert; `get endpoints <service> -o yaml` (empty ENDPOINTS confirms it); align the corresponding Pod | Affects `state-redis` → same path as `ASCallStateStoreUnavailable`, escalate immediately; affects `config-service` → console unavailable, switch to L2 (L2 §4.6). Recover on the Pod side, **do not** change the Service selector | **Triggerable (provided KSM)**: a failure mode **different** from `ASCallStateStoreUnavailable` — this one is "the Service has no backend at all", that one is "the AS cannot reach Redis" |

> **Capacity alerts: deferred.** `as-alerts.yaml` currently has **no CPS ceiling or concurrency ceiling alerts** at all; this is deliberate. Capacity alerts will be a new independent group **after O1 is adjudicated**, with values taken from measurements. Until then, investigate abnormal load with `ASActiveCallsSurge` and internal measurements; **must not** use a number made up ahead of time (`AGENT.md` §2 / §6).
>
> **This page contains no Sh-related alerts at all**: not doing Diameter Sh is a decided non-goal (`AGENT.md` §2). Control-plane alerts (configuration rollback / drift / certificate expiry) are **explicitly deferred** in `deploy/alerts/README.md` until the corresponding metrics are exported — they are **not** in `as-alerts.yaml`.

---

## 3. Common Operations

Each section is structured: prerequisites → commands as written → expected output → failure handling → source.

### 3.1 Manual Downscale and Traffic Removal

Source: [`../acceptance/m5-downscale-runbook.md`](../acceptance/m5-downscale-runbook.md) (criteria implementation `platform/src/as_platform/ops/downscale_guard.py`, ADR-0010; ISSU = draining, ADR-0009).

**Prerequisites**: each Pod can query **`as_active_calls`** (`GET :8080/metrics` or telemetry export); `AS_DOWNSCALE_GUARD_ENABLED` / `AS_DOWNSCALE_GUARD_PROTECT_ABOVE` are injected by the Helm ConfigMap (enabled by default + threshold 0); HPA **need not be enabled** (no thresholds before O1 / M6); downscaling may be manual or a cluster autoscaler proposed replica count.

**Criteria (`plan_scale_down` inputs and invocation)**

```python
from as_platform.ops.downscale_guard import InstanceLoad, plan_scale_down

plan = plan_scale_down(
    (
        InstanceLoad("as-translation-abc", active_calls=0, draining=False),
        InstanceLoad("as-translation-def", active_calls=3, draining=False),
    ),
    desired_replicas=1,
    protect_above=0,  # consistent with AS_DOWNSCALE_GUARD_PROTECT_ABOVE
)
```

**Commands as written (recommended four-step order)**

1. **Compute** `plan_scale_down` (or an operations script wrapper).
2. For each Pod in **removable**: confirm `active_calls==0` before `kubectl delete pod`; Kubernetes deletion triggers `preStop sleep` + SIGTERM.
3. For Pods **still carrying calls**: do not delete; wait for natural completion, or have the business layer end the call; readiness is **503** after `request_terminate`, and the Endpoint should have traffic removed.
4. If `blocked`: only shrink the `removable` subset, or wait.

**Expected output**: `plan.allowed == True` and `plan.candidates` lists the drainable instances; during traffic removal, `/health/ready` returns **503**.

**Failure handling**

- `plan.allowed` is `False`: there are not enough zero-call instances to delete → **do not delete the Pod**, or first initiate draining on high-load instances.
- **Must not SIGKILL**: instances in `plan.candidates` **must still go through the draining process**.
- readiness is not 503, the Endpoint has no traffic removed → escalate to L2 (L2 §4.7).

> ⚠️ **Evidence boundary**: `AS_M5_SIMULATED_ACTIVE_CALLS=N` is a **test / evidence only** simulation of in-flight calls (decreasing by 1 per second after SIGTERM), used by kind evidence scripts to verify draining and the criteria. **It is not evidence of no-dropped-calls under production load** — real SIP no-dropped-call awaits M7 / M8 acceptance (G-P1-1).

### 3.2 Rolling Upgrade

Source: [`../acceptance/m5-state-stores-runbook.md`](../acceptance/m5-state-stores-runbook.md) §Upgrade discipline; [`../../deploy/helm/templates/NOTES.txt`](../../deploy/helm/templates/NOTES.txt) §3.

**Prerequisites**: confirm this change window; confirm the current revision in `helm history`; confirm that the state store and use-case replicas can absorb traffic removal (draining semantics = ISSU, ADR-0009).

**Commands as written (only change these three groups of parameters)**

| Change scope | Command focus |
|---|---|
| AS image / SIP knobs only | `helm upgrade` with only `image.*`, `sip.*`, `useCases` |
| PG image / PVC | Maintenance window; follow the Postgres upgrade runbook |
| Redis | Maintenance window; brief runtime unavailability expected |

label selectors: `app.kubernetes.io/component=state-postgres|state-redis` for state stores, distinguished from use-case Deployments.

**Rollback (image / manifest rollback, which is a different thing from configuration rollback — do not conflate)** — the following three lines come verbatim from `deploy/helm/templates/NOTES.txt` §3, only writing the Helm template placeholders `{{ include "as.namespace" . }}` / `{{ .Release.Name }}` as `<ns>` / `<release>`:

```sh
helm -n <ns> history <release>
helm -n <ns> rollback <release> <revision>
kubectl -n <ns> rollout status deploy --selector app.kubernetes.io/part-of=3rdparty-as
```

**Expected output**: during the rolling, `/health/ready` turns **503** per Pod before rebuilding; after the upgrade completes, `CONFIG_VERSION` in §1 #3 is consistent across replicas.

**Failure handling**: Pod stuck not ready → §4; for the complete process of business traffic removal / rollback see [`rollback-playbook.md`](rollback-playbook.md) (**written to disk**; but its iFC / traffic removal part **depends on S-CSCF / HSS-side cooperation and real-cluster drills**, still blocked currently, G-P1-10).

> **ISSU semantics**: traffic removal (draining) is the existing semantics of the exit path and is **not** a capacity conclusion.

### 3.3 Console Daily Operations (Rule Change Orders)

Source: [`../acceptance/m4b-8-runbook.md`](../acceptance/m4b-8-runbook.md) (browser acceptance 5-step path); governance semantics ADR-0006; state machine implementation `services/config-service/src/as_config_service/change_order.py`.

**Path**: edit draft → submit → approval → grayscale distribution → rollback. Configuration **does not go through GitOps**, and is **not** operations staff directly UPDATE-ing the database (`AGENT.md` §2).

```
DRAFT --submit--> SUBMITTED
SUBMITTED --approve--> APPROVED
SUBMITTED --reject--> REJECTED
APPROVED --begin_distribution--> DISTRIBUTING
DISTRIBUTING --roll_back--> ROLLED_BACK
APPLIED --roll_back--> ROLLED_BACK
```

`REJECTED` / `APPLIED` / `ROLLED_BACK` are terminal states. Distribution status (`services/config-service/src/as_config_service/distributor.py`): `pending` → `in_progress` → `completed`, and `rolled_back` on anomaly.

**Scope (be sure to answer users per this wording)**

- The current live console exposes only **called party + prefix** rules.
- **Caller / regex rules are v1.1, not a release version** (`docs/plan.md` §0: "v1" and "v1.1" in documents must not be treated as scope basis).
- Runtime override granularity = **number range + stable-hash percentage** (ADR-0021); **the AS side does not proactively remove in-flight calls**.

**BLOCKED rules (must not be written as passed)**

- Call-ID live trace (REQ-F-13 / M4b-7.4): M4 closure adjudication deferred, **no live trace source / API** → `BLOCKED: missing backend`; browser acceptance of injected health-failure automatic rollback / manual rollback depends on the complete distribution chain → still `BLOCKED`.

**Expected output**: the change order completes `submitted → approved → distributing → applied`, each instance reports a `CONFIG_VERSION` update and they are consistent; audit rows are produced (append-only).

**Failure handling**: configuration changed but not in effect → L2 §5. Console cannot log in / privilege escalation → L2 §4.6 and responsibility boundaries.

> Automation alternative: `cd deploy/compose && export M4B8_E2E_PASSWORD='<12+ chars, dev-only>' && ./scripts/m4b-8-browser-evidence.sh`. On Ubuntu 20.04, if `playwright install chromium` is not possible, the script falls back to the `mcr.microsoft.com/playwright` container (`--network host`). Artifacts are written to `artifacts/m4b-8/<date>/` by default. **This is an engineering checklist and does not constitute M4b / M4 / REQ acceptance pass** (the maintainer's 2026-10-04 sign-off only means the engineering chain ran through).

### 3.4 Configuration Hot Update for Certificate Rotation

Source: `AGENT.md` §13; `deploy/helm/templates/NOTES.txt` §1; ADR-0016; implementation semantics `platform/src/as_platform/sip/tls_rotation.py`.

**Prerequisites**: the customer PKI Secret is ready (`tls.secretName` points to `tls.crt` / `tls.key` / `ca.crt`) — if `tls.enabled=true` but `tls.secretName` is empty, the chart **mounts no certificate** and the SIP TLS path points to a non-existent file, which must be supplied before going live (NOTES.txt §1); the dual-certificate overlap window policy is decided (`retiring` + `overlap_deadline_monotonic`).

**Principle (not a command, but a hard constraint)**: certificate rotation is a **configuration hot update** — **never restart the process, never drop in-flight calls** (`AGENT.md` §13). At the start of overlap, the rotation request asks the stack for `reloadCertificates`; already-registered connections continue to use the retiring material until the overlap deadline, and new connections use the new material.

**Expected output**: `RESIP_RUNTIME_RELOAD_CERTIFICATES` (`detail=invoked`) appears in the runtime log (see L2 §2). **Failure handling** → L2.

> ⚠️ **E4 / REQ-S-2 / REQ-S-3 currently have no lab evidence**: certificate hot rotation (E4) and operator PKI / peer certificate validation are **not yet accepted**. This section is operational discipline, **not** a verified process.

### 3.5 Backup and Restore Daily Commands

Source: [`../acceptance/m5-state-stores-runbook.md`](../acceptance/m5-state-stores-runbook.md) §Backup & restore (ADR-0008 minimum set).

**Prerequisites**: the governance PG is reachable; executed with a role with backup privileges; `kubectl cp` requires `pg_dump` inside the Pod (the official PostgreSQL image has it).

**Commands as written (PostgreSQL — governance state, the audit chain must be preserved)**

```sh
kubectl -n <ns> exec as-3rdparty-as-postgres-0 -- \
  pg_dump -U postgres -d as_config -Fc -f /tmp/as_config.dump
kubectl -n <ns> cp as-3rdparty-as-postgres-0:/tmp/as_config.dump ./as_config.dump
```

**Expected output**: `./as_config.dump` lands on disk and is non-zero in size.

**Failure handling**: `kubectl cp` reports not found → confirm the Pod name and namespace; `pg_dump` permission error → switch to a role with backup privileges; **do not** write the owner DSN into a Deployment for convenience (see L2 §6).

**Three limitations to know**

- **The chart does not ship a backup Job.** Scheduling is borne by the customer's backup tooling (Velero, cron Job, or out-of-cluster WAL archiving in HA scenarios).
- **The built-in Redis / PG is single replica, not HA.** The Redis HA topology values are adjudicated (**O5 / D3, G7**): in-site N+1 + cross-site 1+1 warm standby, Redis primary/replica + Sentinel (following the ADR-0008 topology, not Redis Cluster; the chart currently still renders single replica, with no evidence of measured failover behavior; RPO / RTO values are still not adjudicated); production PG HA is owned by the customer (Patroni / cloud RDS, or switch to external `postgres.host` and set `stateStores.enabled=false`). The customer must record **RPO / RTO** themselves.
- Redis (runtime state) loss ≈ call failure, so backup is optional (ADR-0007), but RPO / RTO must still be recorded jointly with the customer.
- **Restore drills, backup validation scripts, and periodic drill records** belong to deliverable 2.5; see [`backup-restore.md`](backup-restore.md) (**written to disk**; but the **real-cluster restore drill record is still blocked**, M8 real-cluster evidence currently shelved, G-P1-10).

---

## 4. Escalation and Help

**Escalation path**: L1 → L2 ([`runbook-l2.md`](runbook-l2.md)) → maintainer.

**Trigger conditions for escalating to L2**: any item in §1 whose ownership cannot be determined; the "escalate to L2" mark in the §2 table; `/health/ready` persistently 503; Pod repeatedly restarting; configuration changed but not in effect.

**Trigger conditions for escalating to the maintainer**: product wording needs adjudication (**O1 still undecided**), execution-side changes to already-adjudicated items (**O4 / O5 / D3 / D5 values adjudicated (G6 / G7)**, related implementations not landed, execution-side changes still need maintainer authorization), or overturning existing adjudications. Neither L1 nor L2 **may** on its own treat an undecided item as resolved (`AGENT.md` §15).

**Evidence checklist that must accompany help requests**

| Item | Description |
|---|---|
| Alert name and full expression evaluation result | e.g., `ASCallStateStoreUnavailable` + the time series of `min by (use_case) (as_state_store_available)` |
| Namespace / Pod names / use_case | Output of `kubectl -n as-prod get pods -l app.kubernetes.io/part-of=3rdparty-as` |
| Time window (including time zone) | First occurrence, persistence, most recent |
| `/metrics` snippet + redacted logs | Only capture the relevant `as_*` series; redaction rules see §5 |
| Call-ID | If related to a specific call; the two legs' Call-IDs of the cross-leg B2BUA **differ**, so bring both |
| Change record + already-ruled-out possibilities | The most recent `helm upgrade` / change order revision and time; what has been done and with what results (avoid treating "not checked" as "ruled out") |

**Discipline when AS-side evidence is insufficient**: **no prior demarcation without evidence**. The AS side has only its own logs, metrics, and configuration version; forensics of peer links (S-CSCF → S-SBC trigger segment, S-SBC → AS trunk segment) require peer cooperation ([`../product/responsibility-matrix.md`](../product/responsibility-matrix.md) §3).

---

## 5. Evidence and Redaction Rules

Source: `AGENT.md` §11 / §13; [`../acceptance/m4b-8-runbook.md`](../acceptance/m4b-8-runbook.md) §5/§8.

**Prohibited (no exceptions)**

- **Saving passwords, tokens, cookies, sessions, private keys (`BEGIN PRIVATE KEY`), or any Secret contents is prohibited**; using real addresses, customer names, or real numbers as examples is **prohibited**.
- **Committing real packet captures (pcap) into the repo or evidence directories is prohibited**.
- Payload logs (SIP body / SDP) are **off** by default (`AS_PAYLOAD_LOGS_ENABLED` / `telemetry.payloadLogsEnabled` default `false`); enabling is an explicit, auditable operation.

**Before screenshots / screen recordings**: mask cookie, session, CSRF, and password fields; confirm the address bar is **HTTPS** (do not access the login page via `http://`); confirm on the browser side that the API is **same-origin** (e.g., `https://<host>/internal/v1/...`), with no mixed content.

**When exporting / querying audit records**: confirm the output contains no password / token; the runtime role's INSERT/UPDATE/DELETE/TRUNCATE on the audit table should be rejected (append-only, fail-closed).

**Archive location** (placeholder, per the directory designated by the maintainer): `artifacts/<milestone>/<YYYY-MM-DD>/`. After archiving, fill in the path, commit, and blocked-items summary in the corresponding `report.md` subsection of the lower volume.

---

## 6. Source Mapping

| Section on this page | Original file and location | Collection method |
|---|---|---|
| Status block | [`../acceptance/report.md`](../acceptance/report.md) §0.1/§0.4/§0.5; [`../plan.md`](../plan.md) §0 | Summary |
| §1 #1–#3 Pod / health endpoints / configuration version | `deploy/helm/templates/_helpers.tpl:55,71`; `templates/NOTES.txt:37-51`; `deploy/helm/values.yaml:281-303`; `templates/configmap.yaml:58`; `platform/src/as_platform/runtime/health.py` | Index links (self-verified) |
| §1 #4/#6 metrics and Redis availability | `deploy/alerts/README.md` §Metric contract; scraping gap self-verified (no `prometheus.io/scrape` / ServiceMonitor / PodMonitor across the entire `deploy/helm/templates/` directory) | Summary + self-verified |
| §1 #5 ingress 301/308 | [`../acceptance/m5-7.2d-ingress-runbook.md`](../acceptance/m5-7.2d-ingress-runbook.md) check item 4, §"host 80/443 and in-cluster ingress curl" | Summary |
| §1 #6 Redis availability | `deploy/alerts/README.md` §Metric contract | Index links |
| §1 #8 console | [`../acceptance/m4b-8-runbook.md`](../acceptance/m4b-8-runbook.md) §8 | Index links |
| §2 full table | [`../../deploy/alerts/as-alerts.yaml`](../../deploy/alerts/as-alerts.yaml) **10 rules / 3 groups**; [`../../deploy/alerts/README.md`](../../deploy/alerts/README.md); triggerability taken from [`alert-response-matrix.md`](alert-response-matrix.md) §2 and [`../product/ne-datasheet.md`](../product/ne-datasheet.md) §6, and self-verified via `platform/src/as_platform/__main__.py` | Summary (the rule file is the sole authority for thresholds) |
| §3.1 downscale | [`../acceptance/m5-downscale-runbook.md`](../acceptance/m5-downscale-runbook.md) §1–§5 (**commands and order copied verbatim in full**) | Rewritten operation body |
| §3.2 rolling upgrade | [`../acceptance/m5-state-stores-runbook.md`](../acceptance/m5-state-stores-runbook.md) §Upgrade discipline; `templates/NOTES.txt` §3 | Rewritten operation body |
| §3.3 console | [`../acceptance/m4b-8-runbook.md`](../acceptance/m4b-8-runbook.md) §1/§2/§4/§7; `services/config-service/src/as_config_service/change_order.py:17-23`; `distributor.py:49-55` | Summary + index links |
| §3.4 certificate hot update | `AGENT.md` §13; `templates/NOTES.txt` §1; `platform/src/as_platform/sip/tls_rotation.py:1-18` | Summary |
| §3.5 backup and restore | [`../acceptance/m5-state-stores-runbook.md`](../acceptance/m5-state-stores-runbook.md) §Backup & restore, §PostgreSQL HA / PITR (**two commands copied verbatim**) | Rewritten operation body + summary |
| §4 escalation path | [`../product/responsibility-matrix.md`](../product/responsibility-matrix.md) §4 | Summary |
| §5 redaction | `AGENT.md` §11 / §13; [`../acceptance/m4b-8-runbook.md`](../acceptance/m4b-8-runbook.md) §5/§8 | Summary |
