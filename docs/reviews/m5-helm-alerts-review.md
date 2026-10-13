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

# M5 Helm Template and Alert Rule Review Record

> Review target: `deploy/helm/` (values contract and templates)、`deploy/alerts/`
> Review date: 2026-09-28
> Reviewer: AI agent (checked against ADR-0002 / 0009 / 0013 / 0016, AGENT.md §2 and plan.md §6, REQ-NF-13 / NF-14 / NF-9)
> Review verdict: **conditional pass** —— the Helm rendering validation is done, and the PostgreSQL wiring plus the real-database closure loop (H11) are also done; the remaining gaps are ops wiring and capacity-class alerting (H10 / H12)

## Review findings

| # | Finding | Verdict |
|---|---|---|
| H1 | No absolute CPS or concurrent-session value appears anywhere in the repo; all HPA thresholds and replica min/max are `null` and annotated "待 M6 实测（O1）" | Accept: conforms to AGENT.md §2/§6 "publish no capacity numbers before M6" |
| H2 | `hpa.yaml` triple guard + `required`: with autoscaling enabled but no thresholds filled in, the **install fails outright** instead of falling back to guessed values | Accept: an install failure is preferable to shipping a capacity number of unknown origin |
| H3 | `pdb.yaml` has no capacity defaults; an empty `minAvailable` means nothing is rendered | Accept: same principle as H2 |
| H4 | Alerts use only ratios / relative quantities / state quantities (`ASActiveCallsSurge` uses "当前 > 1.3 × 30 分钟均值"), and every description explicitly states "不是容量数字" | Accept: REQ-NF-14's "surge" is implemented as a purely relative quantity, so no capacity commitment sneaks in |
| H5 | draining is expressed by `preStop` plus an extended `terminationGracePeriodSeconds` | Accept: the draining semantics of ADR-0009 |
| H6 | The comment on `sessionAffinity: ClientIP` states that it is only one of two safety nets (the other half is the application-layer Redis session table), and that it is insufficient when the S-SBC reuses the source port | Accept: avoids treating affinity as a correctness guarantee |
| H7 | Credentials are placeholders plus an `as.3rdparty/credentials: placeholder-replace-before-install` annotation; TLS is not placed in a Secret template and only references the customer PKI Secret mount (hot rotation without restart) | Accept: AGENT.md §13 forbids committing secrets; ADR-0016 certificate hot rotation |
| H8 | One Deployment / Service per use case, iterating `useCases` with `range`; `enabled: false` is skipped; when `replicaCount` is empty, `replicas: 1` is rendered followed immediately by the comment "这是渲染兜底，不是容量结论" | Accept: ADR-0002 one process per use case; the fallback value is explicitly de-capacity-ized |

## Gaps (do not block this delivery, but block M5 completion)

| # | Gap | Disposition |
|---|---|---|
| H9 | ~~`helm template` rendering validation not performed (no helm binary in the environment)~~ **Validation completed on 2026-09-28.** History: at review time the environment had no helm binary, so only plain YAML parsing + a static template-balance self-check were done. Current state: with helm v3.16.2, `helm lint deploy/helm` (0 failed) and `helm template as deploy/helm` (exit 0) both pass; the very first render exposed two left-trim sites in `_helpers.tpl` (the `{{- include ... }}` inside `as.labels` and `as.useCaseLabels` swallowed the preceding newline, labels got concatenated and YAML parsing failed repo-wide in that template); these were changed to `{{ include ... }}` without left trim; the negative case `--set autoscaling.enabled=true` fails as expected and prints the `required` message | **Validation completed, no longer a gap**; see the M5 section of `docs/acceptance/report.md` for evidence |
| H10 | Scale-down guard controller has landed; kind ops-wiring evidence: `m5-plan-scale-down-from-metrics.sh` + `m5-issu-scale-evidence.sh` (2026-10-04) | **kind evidenced** |
| H11 | PostgreSQL-based `VersionStore` wiring (carried over from M4) and its integration cases | **Completed (2026-09-28).** `services/config-service/src/as_config_service/postgres_store.py` is implemented: versions are **immutable append-only** (no UPDATE / no DELETE; rollback writes back the previous version's content instead of mutating history); table names go through a whitelist (identifiers never enter SQL via string concatenation, guarding against injection and wrong-table access); `psycopg` is a **lazy import** (the module can be imported and unit tests run without the driver installed). The 9 integration cases (`services/config-service/tests/test_postgres_store_integration.py`) **really connect to a PostgreSQL 16 container on `127.0.0.1:55432` and pass**, covering the governance closure loop: approve → persist → distribute → automatic rollback → fetch back the previous version; `pytest -m integration` reports **12 passed** repo-wide (9 PG + 3 telemetry export) |
| H12 | Capacity-class alerting (CPS / concurrency) and HPA thresholds | Blocked by O1 / M6; the `as.capacity` group is added separately after M6 |
| H13 | ISSU/draining + `plan_scale_down` path on kind `as-m5` (`artifacts/m5/*/issu-scale-evidence.log`) | **executed on kind (2026-10-04)** |

## Confirmed sign-off

| Item | Value |
|---|---|
| Review verdict | **M5-a/b engineering Accept** (adjudicated 2026-10-04); H10/H13 evidenced on kind; H12 → M6 |
| Reviewer | AI agent, 2026-09-28; updated 2026-10-04 |
| Maintainer sign-off | **Approved 2026-10-04** (authorized by chat, signed on behalf; see [m5-closure-adjudication-2026-10-04.md](m5-closure-adjudication-2026-10-04.md)) |
| M5 index | [m5-task-register-2026-10-04.md](m5-task-register-2026-10-04.md); evidence pointer [`m5-evidence-summary.md`](../acceptance/m5-evidence-summary.md) |
