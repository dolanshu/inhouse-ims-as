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

# M5 Full-Chain Review Record — Requirement / ADR / Design / Code / Testing

- **Review target**: the full-chain M5 milestone (operations) delivery —— Helm chart, custom-metric HPA, scale-down guard controller, draining / ISSU, alert rule set, control-plane cluster deployment proof (including M4b-7.2d ingress/trusted-proxy), D12 in-cluster PostgreSQL/Redis (ADR-0026).
  - Plan and gate-closure records: `docs/plan.md` §4.4 / §4.5 / §4.6
  - Code scope: `deploy/helm/**`、`deploy/alerts/**`、`deploy/kind/**`、`platform/src/as_platform/{runtime,ops,telemetry}/`、`platform/src/as_platform/__main__.py`、`services/config-service/src/as_config_service/runtime.py`
  - Gate scope: `Makefile`、`pyproject.toml` pytest configuration
- **Review date**: 2026-10-05
- **Reviewer**: AI agent (full-chain review assigned by the maintainer; the maintainer judged the existing M5 review records under `docs/reviews/` to be untrustworthy)
- **Review method**: read-only inspection. Each link of the document chain was checked per AGENT.md §3 (requirements → ADR → HLD/LLD → contracts → code + tests → acceptance).
- **Evidence exclusion statement**: this review **did not accept** any M5 review record under `docs/reviews/` (the `m5-*` series) as an evidence source. All conclusions come from the verbatim text of `docs/plan.md`, the ADRs, HLD/LLD, the code, and the Makefile.

---

## 1. Review conclusion

**Conclusion: fail (Not approved). Recommend revoking / downgrading the 2026-10-04 M5 engineering-closure sign-off.**

This is not a problem of "the docs are incomplete" but of three classes of hard defects:

1. **The core deliverables are dead** —— of the 8 alerts, 6 can never fire; the scale-down guard configuration is read but takes no part in the decision; the production profile cannot start as rendered.
2. **The evidence is fake** —— 5 checks that "look like they pass but cannot fail"; the only check that can actually turn red (`make chart-check`) is in no gate at all; the cluster log evidence lives in the gitignored `artifacts/`.
3. **The design docs stop before M5** —— HLD/LLD still say "PG/Redis 在 chart 外" "真实集群滚动升级与缩容未跑", which directly contradicts the actual delivery of ADR-0026 / §4.6.

### 1.1 Positive confirmations (should be kept; not the target of this rejection)

- **The pure-logic core is real and of high test quality**: `plan_scale_down` is a pure function with socket/clock/randomness probe tests (`platform/tests/test_downscale_guard.py:138-163`); the `ProcessShell` draining state machine (`test_shell.py`)、`MetricsRegistry` (`test_metrics.py`)、the bounded queue and background export thread (`test_telemetry.py`、`test_telemetry_export_integration.py`, real UDP socket), and the health HTTP server (real socket) are all real implementations.
- **The four steps of `make gate` really do go red**: `ruff format --check` → `ruff check` → `mypy` → `pytest -m "unit or contract"` (`Makefile:21,22,25,33`), with no `|| true`, no `-` prefix, and no trailing `exit 0`.
- **The three structural guards are effective and do go red**: `tests/test_workspace_layout.py`、`tests/test_version_consistency.py`、`platform/tests/test_library_independence.py`, and all carry anti-idle assertions.
- **ADR-0026 is not a paper-only ADR**: `values.stateStores` + `state-{postgres,redis,networkpolicy,config-runtime-secret,migrate-job}.yaml` + the `chart-check` bundled matrix + kind `M5_BUNDLED_STATE=1` + `values-onprem.example.yaml` + the runbook have all landed.
- **Some kind evidence is a real assertion**: `m5-issu-scale-evidence.sh` (503 must be observed during drain)、`m5-plan-scale-down-from-metrics.sh` (invokes the real `plan_scale_down`; the reject path raises `SystemExit(1)`)、the 7.2d browser script (successful login and "no plaintext HTTP POST" both raise an error).

---

## 2. Requirement chain

Of M5's 7 classes of deliverable, 5 are traceable to `REQ-NF-3 / REQ-NF-4 / REQ-NF-9 / REQ-NF-13 / REQ-NF-14`, so the sources exist. The chain breaks in two places: the **acceptance-document layer** and the **ops-code layer**.

| # | Phenomenon | Evidence | Impact | Severity |
|---|---|---|---|---|
| R-1 | **7.2d (ingress/trusted-proxy) is one of M5's three gate-closure conditions, but the PRD contains no corresponding requirement at all.** `REQ-S-2` is SIP signaling TLS with the S-SBC, and `REQ-S-4` only covers authentication and auditing; neither covers console HTTPS redirect / `X-Forwarded-Proto` trust / ingress proxy CIDR allowlist | `docs/plan.md:217,392` vs the full text of `docs/requirements/prd.md` | The gate-closure condition has no requirement origin, so there is no decidable acceptance item; in `test-plan.md:183-191` it is only a BLOCKED precondition of §1.4 | **Blocker** |
| R-2 | The 5 M5 acceptance / runbook documents and the full text of `report.md` have **REQ-\* reference count = 0** | `docs/acceptance/m5-*.md`; `report.md:167-227` | Violates the REQ-G-2 acceptance item (`test-plan.md:339-342` requires a review record to be traceable to at least one REQ number); M5 evidence cannot be aligned with REQ-NF-3/4/13/14 | Major |
| R-3 | The REQ-NF-3 acceptance criteria include capacity numbers (threshold 500, 1000 concurrent, 3→≥5 replicas), which is mutually exclusive with the project's hard rules | `test-plan.md:231-233` vs `plan.md:249,403` | Filling in per the acceptance item violates "M6 前不发布容量数字", while obeying the prohibition makes it impossible to ever pass; requirements / acceptance / engineering rules are mutually exclusive across the three parties | Major |
| R-4 | REQ-NF-14 acceptance is written as "manually trigger **any one** condition" + "notification channel TBD (frozen at M2)" | `test-plan.md:295-301` | 4 requirements need only 1 of them to fire to be checkmarked, and with the channel undetermined "the alert was sent correctly" cannot be asserted at all | Major |
| R-5 | The scale-down guard criteria (ADR-0010's core decision) have **zero acceptance assertions** in `test-plan` | `test-plan.md:230-235` vs `ADR-0010:6` | M5 claims "scale-down guard is delivered", but the acceptance side has no way to decide it | Major |
| R-6 | All of M5's cluster runtime evidence sits in the gitignored `artifacts/m5/<date>/` and cannot be reviewed inside the repo | `m5-evidence-summary.md:3,22-29`; `.gitignore:25` | Nobody except on the maintainer's own machine can review it; every "PASS" in `report.md` / the closure record is a restatement about files that do not exist | Major |
| R-7 | All ISSU / scale-down "no dropped call" evidence comes from the injected counter `AS_M5_SIMULATED_ACTIVE_CALLS` | `m5-downscale-runbook.md:48-56`; `deploy/kind/m5-issu-scale-evidence.sh:27-28,97` | It can only prove that the criteria are wired; it cannot prove "existing calls complete / no calls are lost" (those are REQ-NF-1/3/4 assertions, belonging to M7) | Major |
| R-8 | Sourceless deliverables (implemented but with no REQ origin): the PDB template、NetworkPolicy、the `simulatedActiveCalls` chart field, D12's HA / PITR / RPO-RTO / restore-drill promises | `pdb.yaml:4`; `state-networkpolicy.yaml`; `deployment.yaml:99-102`; `m5-state-stores-runbook.md:70-105` | Impossible to decide whether they were done or to what extent; same source as the "requirement to be added" PM/AM/UM admitted in `plan.md:369-379` | Minor |
| R-9 | Missing REQ traceability on the code side: `downscale_guard.py` / `downscale_config.py` cite only ADR-0010/0009, with no REQ numbers | `platform/src/as_platform/ops/downscale_guard.py:9,22,46,86,88,118` | REQ-G-2 is traceable only indirectly via the ADR, lengthening the chain by one hop | Minor |

**M5 evidence-grade verdict**: real kind cluster evidence covers the deployment shape and template rendering; simulated-injection evidence covers "mechanism wiring"; the engineering slice (`make gate` / integration) covers REQ-G-4. **No item reaches REQ-level acceptance.** M5's own documentation also declares "Not claimed | REQ / test-plan acceptance" (`m5-engineering-closure-2026-10-04.md:76`), so the problem is characterized as "passing off an engineering slice + simulated-injection evidence as milestone closure", rather than as a false acceptance.

---

## 3. ADR

All 7 M5-related ADRs (0005 / 0008 / 0009 / 0010 / 0013 / 0014 / 0026) have status accepted, all consequences are non-empty, and there is no case of "a proposed ADR being used as accepted". The conflicts concentrate in:

| # | Conflict / gap | Evidence | Severity |
|---|---|---|---|
| A-1 | **ADR-0008's "zero single point of failure within the site" directly conflicts with ADR-0026's built-in single-replica PG/Redis.** 0008 requires Redis Sentinel (1 master, 2 replicas, 3 sentinels) + PG streaming replication + backup + PITR; 0026's standard path renders a StatefulSet with `replicas: 1` and a Redis Deployment with `replicas: 1`, and the runbook itself admits "Production HA is customer-owned". 0008 has no Amendment registering this gap | `0008:27-29` vs `state-postgres.yaml:35`、`state-redis.yaml:12`、`m5-state-stores-runbook.md:72,80` | **Blocker** |
| A-2 | ADR-0008 **explicitly assigns** the cross-site switchover drill to M5; M5's closure checklist has no such item and no deferral was registered | `0008:49,76`; `plan.md:236-241,314-325` (the full text contains no "温备/切换/演练/RTO/RPO") | Major |
| A-3 | Only 1 of ADR-0005's three signals is implemented: no `opentelemetry` dependency anywhere in the repo, no OTLP exporter implementation, no `trace_id`/`span_id`, no structured JSON logs, and the `cps` metric does not exist | `telemetry/__init__.py:77-86,129`; `__main__.py:147-150`; `metrics.py:34-37` | Major |
| A-4 | After ADR-0019 overturned the SIP stack, the architecture doc was not updated: `system-architecture.md:348` still treats `sippy==2.4.2` as a "premise fact" of ADR-0009, and ADR-0009's re-review clause is precisely built on that premise | `system-architecture.md:348,225,391,442` vs `0009:22,30`; AGENT.md §7 | Major |
| A-5 | The body Decision / Consequences of ADR-0013 still say "the chart does not deploy PG/Redis"; the revision exists only in the Amendment paragraph at the end | `0013:27,44` vs `0013:82-89` | Minor |
| A-6 | The diagram in architecture §6.3 says scale-down protection "picks the Pod with the **fewest** active_calls", contradicting ADR-0010 / the implementation / the values "≤ threshold (default 0)" —— implementing per the diagram would drop calls | `system-architecture.md:377` vs `0010:25`、`downscale_guard.py:85-88`、`values.yaml:254` | Minor (the implementation is correct, the diagram is wrong) |
| A-7 | The alert rule set (REQ-NF-14) has no dedicated ADR; the `as_` prefix naming contract was never adjudicated by an ADR | `deploy/alerts/README.md:38-60` | Minor |
| A-8 | ADR-0014 has a wrong REQ traceability number (it claims REQ-NF-13, but it is actually the three OTel signals); it is self-annotated and registered as D8, unadjudicated | `0014:6,72`; `plan.md:352` | Minor |
| A-9 | The M5 empirical evidence of ADR-0009 / 0010 is based on simulated counts, and ADR-0010's Evidence section does not disclose this | `0010:57-62` vs `plan.md:226-228` (already disclosed at the plan level) | Minor |

**Paper-only ADRs** (written down but not reflected in code/artifacts): ADR-0005's traces / logs / call-trace channel / `cps`; ADR-0008's cross-site warm standby, Sentinel, and PG streaming replication; ADR-0020's entire feature gating (0020:59 admits "暂无实现证据"); ADR-0010's in-cluster actuator (the ADR allows an ops script, but no artifact has ever been produced).

---

## 4. Design (HLD / LLD)

**The link of the document chain that is broken most thoroughly.** HLD / LLD are marked `As of: 2026-10-02`, M5 work happened on 2026-10-04, and the two documents **were never updated for M5**.

| # | Phenomenon | Evidence | Severity |
|---|---|---|---|
| D-1 | HLD §7 still says "**Redis and PostgreSQL are external to the chart**", directly contradicting the `stateStores` delivered in ADR-0026 / §4.6 | `hld.md:135` | **Blocker (document chain)** |
| D-2 | HLD §7 still says "**A real Kubernetes rolling upgrade and scale-down have not been run**", while §4.5 already claims it passed on kind and was signed off | `hld.md:139` vs `plan.md:284-293` | **Blocker (document chain)** |
| D-3 | LLD §1 still says of `deploy/helm` "no Helm lint/template/render proof…real cluster rollout/scale-down and alert firing also remain unverified"; LLD §7 likewise says "Live Kubernetes rolling-upgrade/scale-down … unverified" | `lld.md:34,124` | **Blocker (document chain)** |
| D-4 | `stateStores` appears **zero times** in HLD / LLD (a repo-wide docs search hits only plan, the ADR README, 0013, 0026, the architecture doc, reviews, and the acceptance runbook) | grep `stateStores` | Major |
| D-5 | The M5 additions — `downscale_config.py`, the `ActiveCallSource` simulated-count seam, the health/metrics endpoints, and the ingress template — are recorded in neither HLD nor LLD; LLD still says "executable injects `active_calls=lambda: 0`" | `lld.md:23` | Major |
| D-6 | HLD §6 / LLD §6 honestly state that "alert rules are configuration artifacts, not evidence of an alert backend firing", but that conclusion was never carried into the M5 closure decision | `lld.md:114`、`hld.md:113` | Minor (informational) |

Per AGENT.md §3.1, HLD/LLD are mandatory pre-coding artifacts; M5's deployment shape underwent an **architecture-level change** (state stores built into the chart), yet there is no HLD/LLD landing point at all.

---

## 5. Code

### 5.1 Alerts: 6 of the 8 rules are dead rules

| Rule | Referenced metric | Fact |
|---|---|---|
| `ASCallStateStoreUnavailable` (critical) | `as_state_store_available` | **does not exist in the code** |
| `ASConfigRollbackTriggered` (critical) | `as_config_rollbacks_total` | **does not exist in the code** |
| `ASTlsCertificateExpiring` | `as_tls_certificate_expiry_seconds` | **does not exist in the code** (REQ-NF-14 explicitly requires "证书 30 天内到期", which is actually unreachable) |
| `ASConfigDrift` | `as_config_version_in_sync` | **does not exist in the code** |
| `ASHighErrorRatio` | `as_sip_responses_total` | The name exists, but `record_response()` has **zero call sites** in production code |
| `ASTelemetryDropped` | `as_telemetry_dropped_total` | The name exists, but `record_telemetry_dropped()` has **zero call sites** |

Evidence: `platform/src/as_platform/telemetry/metrics.py:34-37` defines only 4 metrics; the four non-existent metric names are hit nowhere in the repo except in `deploy/alerts/` itself; the call sites of `record_response` / `record_rule_hit` / `record_telemetry_dropped` appear only in `platform/tests/test_metrics.py`; `__main__.py:94` only calls `set_active_calls`.

| # | Issue | Evidence | Severity |
|---|---|---|---|
| C-1 | The above 6 rules never fire, and `promtool check rules` reports no error (PromQL permits referencing a non-existent metric); there is no `promtool` execution point anywhere in the repo | `as-alerts.yaml:86,123,140,157,23-31,49`; neither the Makefile nor the tests have promtool | **Blocker** |
| C-2 | The denominator of `ASHighErrorRatio`, `clamp_min(sum(rate(...)), 1)`, is mathematically wrong: the unit of `rate()` is "per second", so during a low-traffic full outage the ratio is compressed to 0.01, which is exactly the non-firing case | `as-alerts.yaml:30` | Major |
| C-3 | The `> 0` threshold of `ASTelemetryDropped` is equivalent to "alert on a single occurrence" (combined with `for: 15m`), which does not match the "持续上升" semantics in the description | `as-alerts.yaml:49` | Major |
| C-4 | `ASActiveCallsSurge` fires on any non-zero value against a zero baseline; `sum()` erases the `use_case` dimension | `as-alerts.yaml:104` | Minor |
| C-5 | None of the 8 rules has a `runbook` / `runbook_url`; there are no `absent()`-style rules, so a metric that never appears will not alert | the full text of `as-alerts.yaml` | Minor |

### 5.2 Platform code: the simulated seam has entered the production path

| # | Issue | Evidence | Severity |
|---|---|---|---|
| C-6 | **The scale-down guard is "dead configuration"**: `load_downscale_guard_config()` reads the config in and does nothing but `logging.info`; `guard.enabled` / `protect_when_active_calls_above` have no consumer anywhere in the repo; apart from tests, `plan_scale_down` is called only manually in the kind script. Helm does deliver `AS_DOWNSCALE_GUARD_*` (`configmap.yaml:69-70`), creating the illusion of "configured but not in effect" | `__main__.py:119-124`; `downscale_config.py:40,46`; `plan.md:227` (it only proves "read", not "in effect") | **Blocker** |
| C-7 | **OTLP export is an empty shell**: even with `OTEL_EXPORTER_OTLP_ENDPOINT` configured, it only creates `BoundedQueueSink(capacity=256)` without passing an exporter → `NoOpExporter`, and data is dropped on enqueue; `export_failure_count` stays 0 forever and ops has no way to notice | `__main__.py:147-150,169`; `telemetry/__init__.py:77-86,129` | Major |
| C-8 | **The simulated-count seam has entered a production class**: `ActiveCallSource.__init__` unconditionally reads `AS_M5_SIMULATED_ACTIVE_CALLS`, and `count()` merges the fake count into the real return value; that env var is rendered by Helm as an official field (`simulatedActiveCalls`) | `runtime/active_calls.py:22-29,49,68-76`; `deploy/helm/templates/deployment.yaml:99-102` | Major |
| C-9 | `record_response` / `record_rule_hit` / `record_telemetry_dropped` have zero production call sites, so the metrics never increment | grep the whole repo for `*.py` | Major |
| C-10 | A parse failure of `AS_DOWNSCALE_GUARD_*` raises `ValueError`, but the load point is **outside** the `try` block (the `try` starts at `:179`) → a config error crashes the process directly instead of returning exit code 2; and there is no test for the failure path | `downscale_config.py:31,45`; `__main__.py:119` vs `:187-189` | Major |
| C-11 | `PostgresVersionStore` runtime wiring has **zero tests**: the entire `test_runtime.py` never mentions `version_store` / `PostgresVersionStore`; the derived table name `f"{config_schema}_config_versions"` is not pinned by any assertion | `services/config-service/src/as_config_service/runtime.py:278-280`; `services/config-service/tests/test_runtime.py` | Major |
| C-12 | The 4 new M5 files have no `# See ADR-00NN` (a hard requirement of AGENT.md §5 / REQ-G-3) | `runtime/active_calls.py`、`runtime/health.py`、`ops/downscale_config.py`、`__main__.py` | Minor |

### 5.3 Helm: the production profile is broken out of the box

| # | Issue | Evidence | Severity |
|---|---|---|---|
| H-1 | **`stateStores.enabled=true` + `bootstrapDevCredentials=false` → Postgres cannot start.** The else branch of `secret.yaml` does not write `POSTGRES_SUPERUSER_PASSWORD` / `CONFIG_DB_OWNER_PASSWORD`, while `state-postgres.yaml` references them via a non-optional `secretKeyRef` → `CreateContainerConfigError`. **This is exactly the combination in `values-onprem.example.yaml`** | `secret.yaml:30-40` vs `state-postgres.yaml:58-72` vs `values-onprem.example.yaml:8-12` | **Blocker** |
| H-2 | **`values-onprem.example.yaml` cannot pass `helm template` as-is**: `configService.enabled=true` while `secretName: ""` → the template `fail`s outright; the install command on lines 2-3 of the README must fail, and `chart-check` never renders with that profile | `values-onprem.example.yaml:31-35`; `config-service-deployment.yaml:4-6`; `chart-check.sh` only uses `--set` | **Blocker** |
| H-3 | `tls.enabled=true` + `secretName=""` (**the default**) → the volume mount is skipped, but the ConfigMap unconditionally emits `SIP_TLS_ENABLED: "true"`, i.e. fail-open | `deployment.yaml:138` vs `configmap.yaml:33-39`; `values.yaml:211-217` | Major |
| H-4 | `sip.peerAllowlist` defaults to the empty string and the chart side does not fail closed (ADR-0016's core control degrades into "relying on the process's own restraint") | `values.yaml:148`; `NOTES.txt:27-30` | Major |
| H-5 | A plaintext password enters the values; `state-migrate-job.yaml` puts the owner password in as a **plaintext env value**, readable with `kubectl get job -o yaml` | `values.yaml:160-165`; `state-migrate-job.yaml:16,67-68` | Major |
| H-6 | `secretKeyRef: optional: true` + empty `postgres.host` / `database` → renders `postgresql://:@:5432/`; the Pod starts normally and only fails at runtime; the DSN is not URL-encoded | `deployment.yaml:69-89`; `secret.yaml:16-40`; `values.yaml:200-207` | Major |
| H-7 | A `REDIS_URL` containing `@` is **silently dropped**, with no message at all | `configmap.yaml:43` | Major |
| H-8 | The NetworkPolicy has only `policyTypes: [Ingress]` (no Egress), and its source is any Pod bearing the `app.kubernetes.io/part-of: 3rdparty-as` label → any Pod with the same label can connect straight to 5432/6379 | `state-networkpolicy.yaml:18-24` | Major |
| H-9 | `postgres.port` is configurable, but `5432` is hardcoded in three places: the config-service Secret, the migrate Job, and the NetworkPolicy | `values.yaml:202` vs the three places | Major |
| H-10 | `minAvailable: 0` is silently not rendered because of a falsy check; there is no validation of `minAvailable >= replicas`, which can deadlock a node drain | `pdb.yaml:11`; `deployment.yaml:29` | Minor |
| H-11 | No `resources` → BestEffort QoS; no startupProbe on AS; config-service uses a `tcpSocket` probe and has neither preStop nor a PDB | `values.yaml:103,107,128`; `config-service-deployment.yaml:78-91` | Minor |

### 5.4 kind evidence scripts: 5 instances of fake verification

| # | Fake verification | Evidence |
|---|---|---|
| K-1 | `m5-ingress-evidence.sh` **only echoes** the three status codes: a non-3xx HTTP only emits `WARN` without exiting, the HTTPS / port-forward codes are never asserted, and the trailing `echo "recorded"` → all three codes can be 000 and it still exits 0 | `:104-127` |
| K-2 | The HPA guard in `chart-check.sh` only greps the `minReplicas` string and **does not check the helm exit code**; meanwhile the normally rendered stdout of `hpa.yaml:43` naturally contains `minReplicas` → delete the guard and the test still PASSes | `:50-57` vs `hpa.yaml:21-22,43` |
| K-3 | `m5-7.2d-evidence.sh` item-2 PASSes unconditionally (the else branch prints PASS directly); item-3 prints PASS even with an empty secret | `:55-69` |
| K-4 | Any bootstrap-admin failure (wrong password / unreachable DSN / command missing) is swallowed into "already complete or skipped" | `:37-42` |
| K-5 | `m5-verify.sh` with no kind cluster → `exit 0`; with no config-service Pod → WARN skips the assertion and it still prints `m5-verify: OK` | `:16-19,29-45` |
| K-6 | `m5-ingress-evidence.sh:30` pulls an unpinned, unchecksummed ingress-nginx manifest from GitHub `main` → the evidence is not reproducible and there is supply-chain risk | `:30` |

**Key characterization**: the input to all ISSU / scale-down evidence is the injected `AS_M5_SIMULATED_ACTIVE_CALLS=3`. A real SIP call has never driven `as_active_calls` (`increment` / `decrement` have no production call sites anywhere in the repo). This is self-confirming forensics of the form "fabricate a count → observe the fake count drop → assert it passed".

---

## 6. Testing and gates

### 6.1 Core problem: the gate will not go red because of M5's problems

| Fact | Evidence |
|---|---|
| `make gate` = `lint type test-unit`, **it does not include chart-check** | `Makefile:62` |
| ② integration has no PG service and no `AS_PG_TEST_DSN` → 11 of 13 files `pytest.skip`, so in practice only 1-2 run; the "142 passed" figure comes from a local compose PG and cannot be produced without a PG environment | AGENT.md §9 |
| `make gate-strict` / the AST scan **do not exist at all**, yet AGENT.md:176、ADR-0015、prd.md:507 all describe them as existing capabilities → REQ-G-3 has nowhere to run | the Makefile has no such target; the repo has no AST scan script |
| `.PHONY` misses 4 m5 targets | `Makefile:6` |

**Conclusion**: each of the three M5 closure-evidence items (`make gate` / `chart-check` / `test-integration-compose`) is individually real and can genuinely fail, but **together they do not mean "M5 passed the gate"** —— no layer of automated gating covers M5's deliverables at all. Whether `make gate` is green is **technically unrelated** to whether M5 is complete.

### 6.2 Actual state of the test layers

| Layer | marker | File count | Status |
|---|---|---|---|
| ① unit | `unit` | 42 | Really runs, really goes red (incl. 3 guards) |
| ① contract | `contract` | 5 | Really runs |
| ② integration | `integration` | 13 | 11 skip without a PG environment; locally requires a compose PG |
| ③ e2e | `e2e` | **0** | No test whatsoever to date |
| ④ performance | `performance` | **0** | 0 test files under `testbed/load/` |

The pytest configuration is healthy: no `conftest.py`, no `deselect`, no `xfail`, no `-k` / `-m not` filtering; the "deselected" in the report is the natural inverse selection of `-m "unit or contract"`.

### 6.3 Test quality

Positive: no `assert True` was found, no "call without asserting" was found, and no mocking-away of the logic under test; the purity probes in `test_downscale_guard.py:138-163` and the real socket + condition variable in `test_telemetry_export_integration.py` are of high quality.

| # | Issue | Evidence | Severity |
|---|---|---|---|
| T-1 | **The feature switch has only parsing-level tests, with no behavior tests for the on / off states.** `AS_DOWNSCALE_GUARD_ENABLED` has been introduced, but no test proves that "behavior differs when disabled" (in fact it does not differ; see C-6); the default state / canary strategy / removal conditions required by ADR-0020 appear neither in the code nor in the comments | `test_downscale_config.py:12-25` (only 4 assertions in the whole file); AGENT.md:109,151,287 | **Blocker** |
| T-2 | `test_downscale_config.py` has no invalid-input failure paths at all (the `ValueError` of `_parse_bool`, the `ValueError` for a non-integer threshold) | `downscale_config.py:31,45` | Major |
| T-3 | `test_health_server.py` only does `assert "as_active_calls" in body`, without validating TYPE / labels / values; the 404 branch is untested; 4 kinds of assertion are crammed into a single test, so the first failure masks the rest | `:42-52` | Minor |
| T-4 | `test_active_calls_source.py:22-35` as a whole is vouching for the legitimacy of the production simulation seam | `:22-35` | Minor |
| T-5 | Test comments generally cite only the ADR / test-plan and never REQ numbers (compare `version_store.py:40`, which has `REQ-NF-10`) | `test_downscale_guard.py`、`test_metrics.py`、`test_shell.py` | Minor |

---

## 7. Recommended minimum fix set (ordered by cost-effectiveness)

1. **Alerts**: delete or implement the 4 rules that correspond to non-existent metrics; wire real call sites into `record_response` / `record_rule_hit`; fix the `clamp_min` math error and the `> 0` threshold; run `promtool check rules` once in an environment that has `promtool`.
2. **Scale-down guard**: make `guard.enabled` / `protect_when_active_calls_above` genuinely take part in the decision (or delete the config items and update the docs accordingly), and add behavior tests for both the on and off states plus invalid-input tests.
3. **Helm**: fix the missing keys in the else branch of `secret.yaml` (H-1); make `values-onprem.example.yaml` renderable and add it to the chart-check matrix (H-2); `fail` when `tls.secretName` is empty (H-3); `fail` when `peerAllowlist` is empty (H-4).
4. **Fake verification**: fix the five spots K-1 ~ K-5 (the core is "an assertion must be able to fail" + "check the exit code"), and pin the ingress-nginx manifest (K-6).
5. **Gates**: fold `chart-check` into `make gate` (delivering the behavior already claimed in `plan.md:260`); start a compose PG and set `AS_PG_TEST_DSN` before running integration in bulk; add a guard to e2e / performance meaning "if that layer has cases, it must block"; add `gate-strict` + the AST scan, or else change the wording in AGENT.md / ADR-0015 / the PRD to "not yet implemented".
6. **Document chain**: add M5 chapters to HLD / LLD (`stateStores`, the downscale configuration, the simulation seam, health/metrics, ingress), and remove stale statements such as "PG/Redis 在 chart 外" "真实集群未跑"; add an Amendment to ADR-0008 addressing the SPoF conflict with ADR-0026; update the sippy premise facts in §6.2/§6.3/§8 of `system-architecture.md` per ADR-0019; add a REQ origin for 7.2d or explicitly register it as a sourceless gate-closure condition.
7. **Reviewable evidence**: un-ignore `artifacts/m5/` in `.gitignore` or move it into the repo at `docs/acceptance/artifacts/`, otherwise every "PASS" is a restatement about files that do not exist.

---

## 8. Sign-off

| Item | Record |
|---|---|
| Review conclusion | **Fail (Not approved)** |
| Recommended disposition | Revoke / downgrade the 2026-10-04 M5 engineering-closure sign-off; fix per §7 and re-review |
| Reviewer | AI agent (assigned by the maintainer), 2026-10-05 |
| Maintainer confirmation | **Awaiting sign-off** (this field must be filled in by the maintainer; this record does not constitute REQ-level acceptance, nor does it replace the M5 closure adjudication) |
| Evidence not accepted | All `m5-*` review records under `docs/reviews/` (judged untrustworthy by the maintainer) |
