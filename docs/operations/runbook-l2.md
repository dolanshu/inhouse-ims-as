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

# L2 Operations Runbook (Deep Troubleshooting and Signaling Analysis) — In-house IMS Application Server

> **Audience**: L2 / second-line engineering. For daily patrols and alert first response see [`runbook-l1.md`](runbook-l1.md).
>
> **Evidence wording (must read)**: **E1 / E4 / E5 not accepted** (reSIProcate production path behavior / TLS hot rotation / state externalization still open, [`../plan.md`](../plan.md) §5.1 O2/O3); **current e2e state**: `pytest -m e2e` **8 tests pass stably** (Wave 1 five tests `tests/e2e/test_sip_first_edition.py` + Wave 2 three tests `tests/e2e/test_s1_replay_contract.py`; **fail, not skip**, when the native extension is missing), REQ-F-1 = **automated subset covered / full text still open** (covered: two-leg normalized message sequence differential comparison, C_in ≠ C_out, byte-identical SDP offer; **per-message header differential comparison of the 14 messages is still not covered**); performance is accept-all harness only, **not the business decision path**; **M4b-7.2d / M8 7.2d still blocked**; **zero capacity numbers** (O1 undecided; the 1% / 30% / 3 times per minute in the text are **pre-existing alert thresholds, not capacity metrics**); kind / compose packet captures are **not production evidence** (ADR-0014: the testbed is not a v1 deliverable); the test CA does not sign REQ-S-2 / S-3.
>
> **B6 review status**: this document has been reviewed under B6 with a review record left — [`../reviews/product-packaging-review-checklist-2026-10-12.md`](../reviews/product-packaging-review-checklist-2026-10-12.md) §6 (2026-10-12 first review) and §7 (2026-10-12 closure re-review); **the conclusion awaits maintainer confirmation** and must not serve as a basis for external delivery or acceptance before confirmation (`AGENT.md` §3.3).
>
> **Originals preserved**: this page is collected from existing runbooks and field contracts under [`../acceptance/`](../acceptance/); the originals are **not deleted, not moved, not rewritten**. Per-section sources see §10.

## 1. Troubleshooting Methodology

**Fixed order: deployment layer → access layer → control plane layer → decision layer → state store layer.** Reversing it (suspecting the decision first) is the most common waste. Each layer's boundary and typical faults:

- **Deployment layer** (Helm / Secret / ingress-nginx / state store Pods / migration Job): CrashLoop, placeholder DSN, Job not reaching completion, annotations rewritten.
- **Access layer** (SIP trunk / TLS / peer whitelist, peer S-SBC trust boundary ADR-0016): 403, handshake failures, calls not arriving at all.
- **Control plane layer** (config-service: change orders / approval / grayscale distribution / versions): configured but not in effect, version drift.
- **Decision layer** (pure function `decide()`, no socket / no clock / no global state): 404 / 603 decision results not matching expectations.
- **State store layer** (Redis: session / dialog / anti-fraud rate windows, ADR-0002 / ADR-0007): `as_state_store_available=0`.

**"Prove in 5 minutes it is not your fault" — what the AS side can self-certify**: process ready status (`/health/live`, `/health/ready`); which SIP messages were received / sent (runtime logs by Call-ID, §2); whether `CONFIG_VERSION` is consistent across replicas; `as_*` series such as `as_state_store_available` / `as_downscale_removable`; the decision path (pure function, replayable).

**What the AS side cannot self-certify**: the S-CSCF → S-SBC segment's iFC trigger context and result (that segment **does not pass through the AS at all**); the **peer-side** signaling landing result of the S-SBC → AS trunk segment (the peer **captures on its own side**); what the outgoing leg signaling was received by at the downstream network element; the **capacity boundary** (O1 undecided, so no capacity number holds, `AGENT.md` §2); long-term retention and query of call traces (O4 / D5 **values adjudicated (G6, 2026-10-10)**: retention default 10 days, deployment-configurable; storage selection in-cluster PostgreSQL — **not yet implemented**, and trace storage / query / deletion capabilities do not currently exist). **No prior demarcation when AS-side evidence is insufficient** — first align both timelines jointly with OP-NOC ([`../product/responsibility-matrix.md`](../product/responsibility-matrix.md) §4).

## 2. Log Forensics

**Search contract.** REQ-NF-13's forensics mounting point is JSON logs, with fields fixed as **`timestamp` / `level` / `trace_id` / `call_id` / `direction` / `method`** (`trace_id` is the Call-ID). The authoritative document is the **field contract** (not the runbook): [`../acceptance/m8-resip-runtime-log-contract.md`](../acceptance/m8-resip-runtime-log-contract.md). The contract freezes the C++ binding (`src/platform/native/resip_runtime/runtime_module.cxx`) to output `key=value` lines via `cout/cerr`; the parser is `src/platform/src/as_platform/sip/resip_runtime_log_contract.py` (`parse_resip_runtime_log_line` / `is_resip_runtime_log_line` / `ResipRuntimeLogEvent.to_nf13_fields`), guarded by `src/platform/tests/test_resip_runtime_log_contract.py` (`contract` marker, 13 cases) — **renaming or changing keys in C++ turns it red**.

**Event → fields → NF-13 mapping (copied verbatim from the contract table)**

| event (C++ line location) | fields | NF-13 mapping (`to_nf13_fields`) |
|---|---|---|
| `RESIP_RUNTIME_LISTENING` (`runListener`, three lines for udp/tcp/tls) | `address, advertised, udp_port/tcp_port/tls_port` | `level=info`, the rest `None` (no call context) |
| `RESIP_RUNTIME_UAC_INVITE_SENT` (`onNewSession` forwarding) | `outgoing_call_id, inbound_call_id, route_uri` | `call_id/trace_id=outgoing_call_id`, `direction=outbound`, `method=INVITE` |
| `RESIP_RUNTIME_UAC_NEW_SESSION` (`onNewSession` UAC) | `outgoing_call_id` | Same as above (`outbound/INVITE`) |
| `RESIP_RUNTIME_UAC_FAILURE` (`onFailure`) | `outgoing_call_id, status` | Same as above (`outbound/INVITE`, `level=info`: downstream failure is a business event) |
| `RESIP_RUNTIME_UAS_FAILURE_MAPPED` (`onFailure` after mapping) | `outgoing_call_id, downstream_status, upstream_status` | Same as above (`outbound/INVITE`) |
| `RESIP_RUNTIME_OUTBOUND_CANCEL_FORWARD` (`onTerminated` RemoteCancel) | `inbound_call_id` | `call_id/trace_id=inbound_call_id`, `direction=inbound`, `method=CANCEL` |
| `RESIP_RUNTIME_UAS_ANSWER_RELAYED` (`onAnswer` 200 relay) | `outgoing_call_id` | `outbound/INVITE` |
| `RESIP_RUNTIME_RELOAD_CERTIFICATES` (`runListener`) | `detail=invoked` (the only fixed literal without `=`) | `level=info`, the rest `None` |
| `*_ERROR / *_CALLBACK_ERROR / *_CORRELATION_MISS / *_WORKER_ERROR` (each `cerr` point) | `message=<single word>` or the corresponding id field; **message lines containing spaces are fail-closed on format drift (returns `None`)** | `level=error`, `call_id/trace_id` takes `outgoing_call_id/inbound_call_id` (if present) |

**Example lines (copied verbatim, directly usable for searching)**

```text
RESIP_RUNTIME_LISTENING address=127.0.0.1 advertised=127.0.0.1 udp_port=5060
RESIP_RUNTIME_UAC_INVITE_SENT outgoing_call_id=out-1@127.0.0.1 inbound_call_id=in-1@127.0.0.1 route_uri=sip:downstream@127.0.0.1:5070
RESIP_RUNTIME_UAC_NEW_SESSION outgoing_call_id=out-1@127.0.0.1
RESIP_RUNTIME_UAC_FAILURE outgoing_call_id=out-1@127.0.0.1 status=486
RESIP_RUNTIME_UAS_FAILURE_MAPPED outgoing_call_id=out-1@127.0.0.1 downstream_status=486 upstream_status=486
RESIP_RUNTIME_OUTBOUND_CANCEL_FORWARD inbound_call_id=in-1@127.0.0.1
RESIP_RUNTIME_UAS_ANSWER_RELAYED outgoing_call_id=out-1@127.0.0.1
```

**How to read**: ① the anchor point of a B2BUA call is **`RESIP_RUNTIME_UAC_INVITE_SENT`** — the only event carrying both `inbound_call_id` and `outgoing_call_id`, the **only entry point for cross-leg correlation** (§3). ② Only `inbound_call_id` with no corresponding `outgoing_call_id` → the outgoing leg was not sent (check the downstream / decision). ③ Only `outgoing_call_id` with no `inbound_call_id` → correlation missing, check `*_CORRELATION_MISS`. ④ `*_ERROR` lines containing spaces → the parser **returns `None`** (fail-closed); **do not** manually assemble fields to fit — use `message=` single-word-form events and adjacent timestamps to locate.

**Python-side JSON enrichment and its boundaries.** `src/platform/src/as_platform/sip/resip_runtime.py::emit_native_log_event` (~30 lines added): parses one native line → uses `to_nf13_fields()` to fill in `timestamp` (`time.time()`, injectable) and `level/trace_id/call_id/direction/method` (`trace_id` can be overridden) → outputs a single `json.dumps` line via the `as_platform.sip.resip_runtime.native` logger. Three boundaries: ① native lines **do not themselves pass through Python logging**; enrichment happens on the **collection-forwarding side** (grab the worker console and call it line by line), and when the cluster does not do this step, Pod logs still contain the native `key=value` lines, **not** JSON; ② **this is not the complete OTel three signals** — **no traces**, the OTLP exporter is currently `NoOpExporter`, real backend wiring is **not yet complete**, so do not infer "the call path did not happen" from "not in the trace view"; ③ the complete C++→Python JSON callback is **deferred to post-RC**, at which point this section's event / field table becomes the schema starting point for the callback payload.

## 3. Signaling Packet Capture and Alignment

Per-segment responsibility table see [`../product/responsibility-matrix.md`](../product/responsibility-matrix.md) §3: **the S-CSCF → S-SBC (ISC triggering) and AS → downstream (outgoing leg) two segments are captured by the peer** (the AS side has no iFC trigger log for the former segment, nor does it hold the outgoing leg's landing result); **the S-SBC → AS trunk (SIP over TLS `5061`) is captured by both sides on their own side**; **the AS internal and `testbed/` simulated link are captured by us** (simulation results are **not production evidence**).

**Method**

1. Both sides capture on **their own side** against their own processes / network elements. **Decryption under TLS is each party's responsibility, and keys are not shared across parties**; the AS side **does not accept** copying peer private keys for decryption.
2. Correlation key: the AS side uses §2's `inbound_call_id` / `outgoing_call_id`. **The two legs of the two-legged B2BUA have different Call-IDs** — cross-leg correlation uses "**timestamp + Route / Record-Route**": starting from the inbound leg's `inbound_call_id`, following `route_uri` and the `Record-Route` returned by the downstream, then aligning the outgoing leg's `outgoing_call_id`.
3. Align the time base before comparison; when the window is insufficient, **do not** use "appears simultaneous" as evidence.
4. **Never commit real packet captures** (`AGENT.md` §13). Only commit redacted fields / text lines — §2's `key=value` lines are themselves a committable form.

## 4. Layered Fault Tree

When judging ownership, cross-reference [`../product/responsibility-matrix.md`](../product/responsibility-matrix.md) §4 and [`../product/compliance-matrix.md`](../product/compliance-matrix.md) (the latter holds file:line evidence).

### 4.1 Call Did Not Reach the AS (no inbound leg logs)

1. Pod and Service Endpoints (`kubectl -n <ns> get pods -l app.kubernetes.io/part-of=3rdparty-as`) anomalous → **AS (deployment layer)**.
2. `as_downscale_removable{use_case,pod}` all 0 (protected while draining) → **AS (draining not converging)**, switch to §4.7.
3. ingress / network policy rejects the peer, or `AS_PEER_ALLOWED_ADDRESSES` / `AS_PEER_ALLOWED_CERT_FINGERPRINTS` did not hit → **AS (boundary policy)**, see §4.2.
4. In `/metrics`, that `use_case` has the series but no inbound leg logs → **peer (OP-SBC / OP-NET)**, switch to the next hop for alignment. **No prior demarcation when the AS side has no evidence.**

### 4.2 AS-side 403 (peer whitelist / cleartext rejected)

**Cleartext rejected when TLS is required** and **peer whitelist not matched** both **share 403** (`sip/resip_runtime.py:39,334-346`; `sip/ingress.py:178-194`, any transport other than `tls` / `sips` is rejected) → owned by the **AS side (boundary policy)**. Next step: confirm whether the peer initiated with TLS; confirm the CA pointed to by `AS_TLS_CA_PATH` contains the peer's issuing chain; confirm the peer address / fingerprint is in `AS_PEER_ALLOWED_ADDRESSES` / `AS_PEER_ALLOWED_CERT_FINGERPRINTS`. Policy correct but the peer is still rejected → switch to customer PKI / network department. **Corroboration**: the host's `http_proxy` makes `curl localhost` go through a proxy → **403 / 000** (§4.6); such 403 is an **evidence-collection path** issue, not a product fault.

### 4.3 AS-side 404 / 603 — **expected behavior, not a failure**

| Code | Business meaning | Next step |
|---|---|---|
| `404 Not Found` | **No matching rule**, the default result of the decision chain (`adapter.py:25`; contract scenario S2) | Check whether the number range / prefix rules cover the called party; should have hit → rule issue, go through the **change order** (ADR-0006) |
| `603 Decline` | **Policy rejection / policy decision rejection**, e.g., anti-fraud limit exceeded (`adapter.py:24`; contract scenario S3) | Check the effective rule version and the hit policy; if it does not match expectations → roll back through the change order |

**Neither `603` nor `404` is usually a failure**: ask "what is the expected decision" before asking "why it did not hit". For the `608` wording discrepancy see §8.

### 4.4 Downstream Failure Codes

**Per-code passthrough set `{408, 480, 486, 503, 504}`** (`sip/call_controller.py:19-21,98-104`; same logic in native `runtime_module.cxx:466-484`); all other non-2xx are **mapped to `502`**. ⚠️ **the native product path has end-to-end tests only for `486`** (`test_resip_two_leg_integration.py`, `test_m7_forward_two_leg_integration.py`), **the other four codes have no product path evidence** — when seeing 408 / 480 / 503 / 504 on the native product path, **do not yet** report defects as verified behavior. The full code table and file:line see [`../product/compliance-matrix.md`](../product/compliance-matrix.md) §3.6.

### 4.5 State Store Unavailable

`as_state_store_available{use_case}` is `0` for `2m` → `ASCallStateStoreUnavailable` (critical), owned by the **AS side**; in-flight call state (session / dialog / anti-fraud rate windows) is all in Redis (ADR-0002 / ADR-0007), so **Redis unavailable = in-flight calls cannot be sustained**. Note that when `REDIS_URL` is not configured the **series does not exist (not 0)**, so the rule never triggers — do not read "no data" as "failure". The Redis HA topology values are adjudicated (**O5 / D3, G7**): in-site N+1 + cross-site 1+1 warm standby, Redis primary/replica + Sentinel (following the ADR-0008 topology, not Redis Cluster); the chart currently still renders single replica, with no evidence of measured failover behavior; the split-brain window idempotence contract is still not implemented → escalate to the maintainer when the execution side needs changing or the adjudication needs overturning.

### 4.6 config-service CrashLoop / Ingress Not Ready

Source: [`../acceptance/m5-7.2d-ingress-runbook.md`](../acceptance/m5-7.2d-ingress-runbook.md) (check items 1–6, M5-1d, admission webhook, company HTTP proxy, 7.2d wording tiers) and [`../acceptance/m5-state-stores-runbook.md`](../acceptance/m5-state-stores-runbook.md) §Re-run config-service + ingress.

| Symptom | AS-side check | Handling / wording |
|---|---|---|
| config-service **CrashLoop** | Is the DSN hostname the placeholder `postgres:5432` | The placeholder DSN is **the in-cluster Service name only**; CrashLoop when compose is not installed into kind (or the customer cluster has no same-named Service). The Ingress object can still be created, but the **Ready evidence** depends on M5-1d → use an external PG / external Service name |
| **403 Forbidden** (console / API) | Whether the controller retains the `nginx.ingress.kubernetes.io` annotation **prefix** (check the annotation key name via `kubectl describe ingress`) | Rewritten → the prefix was overwritten; rebuild the Ingress |
| **403 / 000** (host curl) | Whether `http_proxy` is set | Use `NO_PROXY=127.0.0.1,localhost kubectl port-forward` or `make m5-kind-verify` — **an evidence-collection path issue, not a product 403** |
| **empty reply (curl 52)** | kind's default `m5-kind-up.sh` does **not** map hostPort 80/443 | **empty reply is treated as not passed**; the environment must be fixed (`extraPortMappings`) or the evidence path changed; **must not** tick 7.2d closure in the plan |
| **port-forward 200 but 7.2d not passed** | Distinguish the two tiers of wording | **M5-1c / §4.5 slice evidence**: Ingress object + annotations (check items 1–3, 6) + config-service **Ready** + port-forward HTTP 200 suffices; **M5 maintainer sign-off / §217③ / M4b-7.2d closure**: **must** complete check items **4–5** (301/308 via the ingress + browser HTTPS-only), **port-forward cannot substitute** |
| admission webhook Job timeout / failure | `kubectl -n ingress-nginx get jobs,pods` | The script **WARNs** + logs `admission_job_ok=0` → **do not delete the VWC without a record**; kind development exceptions must record the reason in the evidence log, and the production path must either have the Job succeed or be configured per the customer's ingress standards. ⚠️ The `kubectl delete validatingwebhookconfigurations ingress-nginx-admission 2>/dev/null \|\| true` in `m5-state-stores-runbook.md` is a **development environment** fallback; **copying it in production is equivalent to abandoning closure evidence** |
| trusted-proxy misconfiguration | `forwarded_allow_ips` / `AS_CONFIG_TRUSTED_PROXIES` | Must be **explicit IP / CIDR**; `*` and the default route `0.0.0.0/0` are **not accepted** (`src/services/config-service/src/as_config_service/runtime.py:105-116` fail-closed); enabling proxy headers without setting this item → `AS_CONFIG_TRUSTED_PROXIES must be set when proxy headers are enabled` |
| TLS Secret not mounted | `tls.enabled=true` and `tls.secretName` empty | Render-time fail-closed; the customer PKI Secret must be provided before going live (NOTES.txt §1) |

### 4.7 Downscale Without Dropped Calls / Draining Not Converging

Symptom: the Pod is cordoned / deleted, but `as_active_calls` does not drop and `as_downscale_removable` is persistently 0. AS-side checks: whether readiness is **503**; whether the Endpoint has traffic removed; whether `AS_DOWNSCALE_GUARD_ENABLED` / `AS_DOWNSCALE_GUARD_PROTECT_ABOVE` were correctly injected by Helm; whether the `preStop sleep` + SIGTERM path was taken (**must not SIGKILL**). The four-step operation see [`runbook-l1.md`](runbook-l1.md) §3.1 and [`../acceptance/m5-downscale-runbook.md`](../acceptance/m5-downscale-runbook.md). ⚠️ **Evidence boundary**: existing draining / downscale evidence uses `AS_M5_SIMULATED_ACTIVE_CALLS=N` to **simulate** in-flight calls (decreasing by 1 per second after SIGTERM), which is mechanism evidence on kind; **not dropping calls under real SIP load awaits M7 / M8 acceptance** (G-P1-1), and **must not** use simulated evidence to promise the peer "no dropped calls in production". For the complete playbook see [`fault-demarcation.md`](fault-demarcation.md) (**written to disk**; but the complete playbook's real-cluster evidence is still blocked, M8 7.2d not unlocked).

## 5. Change and Grayscale Troubleshooting

**Two state machines** (ADR-0006; `src/services/config-service/src/as_config_service/change_order.py:17-23`, `distributor.py:49-55`):

```text
change order:  DRAFT → submitted → approved → distributing → applied
                                          ↓ roll_back        ↓ roll_back
                                      rolled_back        rolled_back
         (submitted → rejected is a terminal state; REJECTED / APPLIED / ROLLED_BACK are all terminal states)
distribution:  pending → in_progress → completed   /   rolled_back
```

- **Configuration changed but not in effect**: whether the change order reached the "applied" state; whether grayscale distribution is `completed`; whether `CONFIG_VERSION` reported by each instance is consistent (`printenv CONFIG_VERSION`, L1 §1 #3).
- **Cannot judge rule hits** — ⚠️ **`as_rule_hits_total` currently has no production caller** (`src/platform/src/as_platform/telemetry/metrics.py:254-260` defines the write interface, but the production path has no caller, and it is **not** in the `deploy/alerts/README.md` metric contract table) → **cannot rely on it to judge hits**. Judge with `call_id` + effective rule version + decision path (pure function, replayable).
- **Inconsistent behavior during the grayscale period**: runtime override granularity = number range + **stable-hash percentage** (ADR-0021, `FNV-1a 32-bit(call_id)`). Different calls behaving differently within the same number range is **design expectation**; the first step is to look at which bucket the `call_id` lands in; returns `None` (fail-closed) when no hit is found.
- **Widespread anomaly after a rule change**: roll back through the change order (`rolled_back`); **do not** modify the database directly (configuration does not go through GitOps, `AGENT.md` §2).
- **Hard prerequisite**: the rule schema's **bidirectional compatibility** is a hard prerequisite for ISSU upgrades — during old/new coexistence, incompatibility in either direction constitutes a blocker. `as-alerts.yaml` has **no** configuration rollback / drift alerts (`deploy/alerts/README.md` explicitly defers them); the `ASConfigDrift` / `ASConfigRollbackTriggered` mentioned in `deploy/helm/templates/NOTES.txt:39-42,57-60` are **not in the rule file** (§8).
- **iFC / traffic removal boundary**: the iFC triggering logic belongs to the S-CSCF / HSS and is **not on the AS side**; the AS only implements the business decision and runtime override after ISC triggering, and **does not proactively remove in-flight calls**. iFC triggering by number range / percentage requires S-CSCF / HSS-side cooperation configuration; for the complete process see [`rollback-playbook.md`](rollback-playbook.md) (**written to disk**; but depends on S-CSCF / HSS-side cooperation configuration, and real-cluster drills are still blocked, G-P1-10).

## 6. Database and Migration Troubleshooting

Source: [`../acceptance/m5-state-stores-runbook.md`](../acceptance/m5-state-stores-runbook.md) §Schema migrate / §Helm migrate Job / §PostgreSQL HA / PITR and [`../acceptance/m5-7.2d-ingress-runbook.md`](../acceptance/m5-7.2d-ingress-runbook.md) §M5-1d. **The first thing in troubleshooting: tell which DSN you are holding.**

| Purpose | Role / environment variable | Hard rule |
|---|---|---|
| Migration | `AS_CONFIG_OWNER_DSN` (`as_config_owner`) | **The owner DSN never goes into Deployment / runtime Secret**; used only on trusted hosts or in a one-time Job |
| Runtime (config-service Pod) | `AS_CONFIG_DSN`, the role must be **`as_config_web`** (not the owner); plus `AS_AUDIT_RESOURCE_HMAC_KEY_B64` | Using the wrong role manifests as API permission errors, not crashes |
| Least privilege | `as_config_runtime` (`NOLOGIN`) | Audit append-only related |

**Migration command as written (run once per schema version)**

```sh
kubectl -n <ns> port-forward pod/as-3rdparty-as-postgres-0 15432:5432
export AS_CONFIG_OWNER_DSN="postgresql://as_config_owner:<password>@127.0.0.1:15432/as_config"
export AS_CONFIG_RUNTIME_ROLE=as_config_runtime
export AS_AUDIT_SCHEMA=console_audit
export AS_CONFIG_SCHEMA=as_config
uv run as-config-migrate
```

**Helm migrate Job (production / repeatable)**: Secret `as-config-migrate-owner`'s key `AS_CONFIG_OWNER_DSN` (owner login only).

```sh
helm upgrade --install as deploy/helm -f deploy/helm/values-onprem.example.yaml ...
kubectl -n <ns> delete job/as-3rdparty-as-config-migrate --ignore-not-found
kubectl -n <ns> wait --for=condition=complete job/as-3rdparty-as-config-migrate --timeout=300s
```

⚠️ **Job reuse pitfall**: a same-named Job is not rebuilt → must `delete job ... --ignore-not-found` first, then `wait`, otherwise you will **wait on an already-completed old Job and misjudge success**. **Order and dependencies**: a new empty database must run migrate first (owner DSN, manual); when compose init has already created roles, usually only the schema and M4b need to be consistent; the built-in PG uses a **headless** Service, with a DSN host like `…-postgres-0.…-postgres` (`deploy/helm/templates/_helpers.tpl`); after first boot of PG, `as-config-migrate` is still needed.

**First administrator bootstrap (after migrate)**

```sh
kubectl -n <ns> exec -it deploy/as-3rdparty-as-config-service -- \
  as-config-bootstrap-admin   # reads env; interactive getpass
```

> The original document notes: the exact CLI name is per `pyproject.toml` console script / image entry documentation — verify before executing.

**Troubleshooting comparison**: ① config-service CrashLoop → whether the DSN is the placeholder `postgres:5432`, whether the runtime Secret was stuffed with the owner DSN (§4.6); ② migration Job fails in seconds → whether Secret `as-config-migrate-owner` exists and its key name is correct, and whether the database is reachable; ③ `as-config-migrate` reports a permission error → whether you are using the owner DSN or the runtime DSN; ④ audit writes fail → the audit table is append-only (`BEFORE UPDATE OR DELETE` / `BEFORE TRUNCATE` triggers), and the write path must use the correct role.

**PG HA / PITR and restore drill**: the chart ships only a **single-replica** StatefulSet; production HA is owned by the customer (Patroni / cloud RDS, or external `postgres.host` + `stateStores.enabled=false`); the customer must record **RPO / RTO**, using `pg_dump -Fc` (commands see [`runbook-l1.md`](runbook-l1.md) §3.5) or WAL archiving out of cluster; restore drill = restore to a new instance → re-run `as-config-migrate` if the schema version changed → point the runtime Secret to the new host. **Drill records belong to deliverable 2.5; see [`backup-restore.md`](backup-restore.md) (written to disk; the real-cluster restore drill record is still blocked, depends on a real cluster, M8 7.2d)**. The Redis HA topology values are adjudicated (**O5 / D3, G7**: in-site N+1 + cross-site 1+1 warm standby, Redis primary/replica + Sentinel, following the ADR-0008 topology, not Redis Cluster), and the chart's single Redis is still non-HA (single-replica rendering, no evidence of measured failover behavior).

## 7. Test and Acceptance Environment Preparation

Source: [`../acceptance/m8-native-consistency-runbook.md`](../acceptance/m8-native-consistency-runbook.md) (that file is one sentence, commands copied verbatim). **The order must not be reversed: before running acceptance, you must first build the native extension corresponding to the evidence under test.**

```sh
make m2-platform-resip-build
# additionally for two-leg / recovery evidence:
make m7-platform-two-leg-build
make m7-platform-recovery-build
```

Then run the acceptance commands:

```sh
AS_REQUIRE_NATIVE_EXTENSIONS=1 uv run pytest src/platform/tests/test_e1_contract_resip_runtime_full.py -m contract -q
AS_REQUIRE_NATIVE_EXTENSIONS=1 uv run pytest src/platform/tests/test_m7_forward_two_leg_integration.py src/platform/tests/test_req_f4_sdp_identity_integration.py -m integration -q
```

**Key behavior (the most commonly misread point during troubleshooting)**: **when the native extension is missing, cases fail, not skip** (`AS_REQUIRE_NATIVE_EXTENSIONS=1`; `make gate-native` and `make m2-native-smoke` are blocking targets). Therefore **forgetting `make m2-platform-resip-build` will yield a wall of red**, which **will be misread as a product defect** — when seeing native-related cases fail en masse, the first step is to confirm whether the extension has been built, before talking about defects.

> **Wording ambiguity note**: the original document says "then run the §7 commands from the plan", but `docs/plan.md`'s §7 is "risk register" and `docs/acceptance/test-plan.md` has no §7 — that reference **cannot be resolved to a specific section**. The two `pytest` commands listed above are all the commands given in the original document; this page copies them **verbatim as written** and does not infer other case sets on its behalf.

## 8. Known Pitfalls That Mislead Troubleshooting

| # | Pitfall | Fact |
|---|---|---|
| 1 | **Treating simulated `active_calls` as production no-dropped-call evidence** | `AS_M5_SIMULATED_ACTIVE_CALLS=N` is a **test / evidence only** simulation of in-flight calls; real SIP no-dropped-call awaits M7 / M8 acceptance (G-P1-1) |
| 2 | **Treating accept-all harness as the production path** | The performance layer is accept-all harness only, **not the business decision path** (does not go through `decide()`'s rule matching); the harness covering 100/180/200 **does not equal** the 14-message B2BUA full replay having been signed off |
| 3 | **Thinking the test CA can verify REQ-S-2 / S-3** | **The test CA does not sign REQ-S-2 / S-3**, and the test page does not sign REQ-S-4; TLS evidence on kind is testbed-only narrow-scope evidence |
| 4 | **Thinking `AS_M5_PROBE_SIP_STATUS` can continuously produce response counts** | It is a **one-time probe at process startup** (`__main__.py:88-97`, not set in production on-prem); using it to derive `ASHighErrorRatio` will yield wrong conclusions |
| 5 | **Thinking Prometheus can scrape the AS's metrics** | ⚠️ **The chart has not wired scraping**: the Pod template has **no** `prometheus.io/scrape` annotation, and the chart has **no** ServiceMonitor / PodMonitor (no hits across the entire `deploy/helm/templates/` directory). The `/metrics` endpoint exists and renders the `health-http` port, but **no scraper is wired to it by the chart** → under standard deployment, Prometheus **cannot receive** these series |
| 6 | **Thinking all alert names in NOTES.txt exist** | `templates/NOTES.txt:39-42,57-60` mentions `ASConfigDrift` / `ASConfigRollbackTriggered`, but they are **not** in `as-alerts.yaml`; `deploy/alerts/README.md` explicitly lists them as **deferred**. Searching the alerting system by their names will find nothing |
| 7 | **Treating `608 Rejected` as a product rejection code** | The product path **currently only sends `603 Decline`**; `608` appears only in the **operator-side peer** declaration of the POC packet capture baseline ([`../product/compliance-matrix.md`](../product/compliance-matrix.md) §3.8) |
| 8 | **Treating all 403s as a whitelist problem** | 403 has two causes sharing one code (cleartext rejected / whitelist not matched), plus the evidence-collection path issue of curl 403/000 caused by the host proxy (§4.2 / §4.6) |
| 9 | **Treating "no data" from `as_state_store_available` as 0** | It probes and writes the series only when `REDIS_URL` is non-empty; when not configured, the **series does not exist (not 0)** |
| 10 | **Treating 404 / 603 as failures** | 404 = no matching rule, 603 = policy rejection, **both expected decisions** (§4.3); additionally, using capacity numbers for demarcation does not hold either — O1 undecided, `as-*` has no capacity rules, and M6 dev-host numbers must not be cited (`AGENT.md` §2) |
| 11 | **Treating "in effect immediately after change" as the default** | Configuration **does not go through GitOps**; it must go through the change order state machine + grayscale distribution + instance version reporting (§5) |

## 9. Escalation Boundaries

**L2's own boundaries**: **cannot** modify undecided items on its own, cannot overturn existing adjudications, and cannot describe unaccepted items as accepted (`AGENT.md` §15). **Escalate to the maintainer**: ① product wording needs adjudication (e.g., whether a status code counts as a defect); ② undecided items need changing (**O1 still undecided**) or execution-side changes to already-adjudicated items (**O4 / O5 / D3 / D5 values adjudicated (G6 / G7)**, related implementations not landed, execution-side changes still need maintainer authorization); ③ any conclusion of M5 engineering closure or M8 RC needs overturning; ④ evidence needs collecting on a **real cluster / real peer** (depends on S-CSCF / HSS-side cooperation and the customer environment, G-P1-10, which the AS side cannot complete unilaterally); ⑤ involving Sh / billing / CDR / media (**out of scope** — submit a correspondingly-scoped proposal instead).

**Explicitly N/A (handle as N/A on appearance and give the reason)**: Diameter Sh (data comes from our own data plane); CDR / call records / billing (replaced by call traces by Call-ID, and traces **are not** call records, ADR-0017); media / RTP / transcoding / DTMF / MRF (ADR-0004); LI / IRI (an in-network network element function, ADR-0016).

## 10. Source Mapping

| Section on this page | Original file and location | Collection method |
|---|---|---|
| Status block | [`../acceptance/report.md`](../acceptance/report.md) §0; [`../plan.md`](../plan.md) §0 / §5.1; [`../product-packaging-plan.md`](../product-packaging-plan.md) §0.3 | Summary |
| §1 self-certification boundary | [`../product/responsibility-matrix.md`](../product/responsibility-matrix.md) §3/§4 | Summary |
| §2 whole chapter | [`../acceptance/m8-resip-runtime-log-contract.md`](../acceptance/m8-resip-runtime-log-contract.md) §1–§5 (**field contract table and 7 example log lines copied verbatim**) | Index links + copied verbatim |
| §3 packet capture | [`../product/responsibility-matrix.md`](../product/responsibility-matrix.md) §3 | Index links + summary |
| §4.1–§4.3 / §4.7 | [`../product/responsibility-matrix.md`](../product/responsibility-matrix.md) §4; [`../product/compliance-matrix.md`](../product/compliance-matrix.md) §3.6 | Summary |
| §4.2 / §4.4 | `sip/resip_runtime.py:39,334-346`, `sip/ingress.py:178-194`, `sip/call_controller.py:19-21,98-104`, `src/platform/native/resip_runtime/runtime_module.cxx:466-484` | Self-verified (consistent with the compliance matrix) |
| §4.6 | [`../acceptance/m5-7.2d-ingress-runbook.md`](../acceptance/m5-7.2d-ingress-runbook.md) (check items 1–6, M5-1d, admission webhook table, proxy section, 7.2d wording tiers); [`../acceptance/m5-state-stores-runbook.md`](../acceptance/m5-state-stores-runbook.md) §Re-run config-service + ingress | Rewritten operation body + **conflict annotation** |
| §5 | `change_order.py:17-23`; `distributor.py:49-55`; [ADR-0021](../architecture/adr/0021-runtime-override-granularity.md); `telemetry/metrics.py:254-260` | Self-verified + index links |
| §6 | [`../acceptance/m5-state-stores-runbook.md`](../acceptance/m5-state-stores-runbook.md) §Schema migrate / §Helm migrate Job / §PG HA / PITR; [`../acceptance/m5-7.2d-ingress-runbook.md`](../acceptance/m5-7.2d-ingress-runbook.md) §M5-1d | Rewritten operation body (commands copied verbatim) |
| §7 | [`../acceptance/m8-native-consistency-runbook.md`](../acceptance/m8-native-consistency-runbook.md) (**in full**) | Rewritten operation body |
| §8 | `report.md` §0.5 / §0.6; [`../product/ne-datasheet.md`](../product/ne-datasheet.md) §5; `deploy/alerts/README.md`; `deploy/helm/templates/NOTES.txt`; [`../plan.md`](../plan.md) §0 | Summary + self-verified |
