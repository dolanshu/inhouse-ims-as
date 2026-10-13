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

# M5 Task Register and Review Index (2026-10-04)

> **Spec source**：[`plan.md`](../plan.md) §4.4 (§217 gate-closure conditions)、§4.5、§4.6；[`m5-closure-adjudication-2026-10-04.md`](m5-closure-adjudication-2026-10-04.md) item-by-item adjudication.  
> **Process**: each task gets its own review document → maintainer-level adjudication（**Accept / Fix / Deny**）。This is **not** equal to all REQs green or maintainer sign-off.

## Phase 0 — Baseline (§4.4.4)

| Task ID | Plan item | Evidence / artifact | Review |
|---------|-----------|-------------|--------|
| M5-0a | `make gate` all green | local gate；plan §4.4.4 | [m5-0a-gate-review-2026-10-04.md](m5-0a-gate-review-2026-10-04.md) |
| M5-0b | `test-integration-compose` | `make test-integration-compose` | [m5-0b-integration-compose-review-2026-10-04.md](m5-0b-integration-compose-review-2026-10-04.md) |
| M5-0c | `chart-check` | `deploy/helm/scripts/chart-check.sh` | [m5-0c-chart-check-review-2026-10-04.md](m5-0c-chart-check-review-2026-10-04.md) |

## Early delivery (§4.4.2)

| Task ID | Plan item | Review |
|---------|-----------|--------|
| M5-a | Helm chart skeleton (ADR-0013) | [m5-a-helm-chart-review-2026-10-04.md](m5-a-helm-chart-review-2026-10-04.md) (aligned with [m5-helm-alerts-review.md](m5-helm-alerts-review.md) H1–H9) |
| M5-b | Alert rules (REQ-NF-14) | [m5-b-alerts-review-2026-10-04.md](m5-b-alerts-review-2026-10-04.md) |
| M5-c | `plan_scale_down` (ADR-0010) | [m5-c-downscale-guard-review-2026-10-04.md](m5-c-downscale-guard-review-2026-10-04.md) |
| M5-d | `as_active_calls` contract (ADR-0005) | [m5-d-metrics-contract-review-2026-10-04.md](m5-d-metrics-contract-review-2026-10-04.md) |
| M5-e | PostgresVersionStore + integration | [m5-e-version-store-review-2026-10-04.md](m5-e-version-store-review-2026-10-04.md) |
| M5-f | Container image + SIGTERM draining smoke | [m5-f-container-draining-review-2026-10-04.md](m5-f-container-draining-review-2026-10-04.md) |

## Phase 1 — Deployment and 7.2d (§4.4.4 + M4b-7.2d)

| Task ID | Plan item | Review |
|---------|-----------|--------|
| M5-1a | Images `as-platform:m5` / `as-config-service:m5` | [m5-1a-images-review-2026-10-04.md](m5-1a-images-review-2026-10-04.md) |
| M5-1b | kind `as-m5` + Helm AS | [m5-1b-kind-helm-review-2026-10-04.md](m5-1b-kind-helm-review-2026-10-04.md) |
| M5-1c | Ingress template / object | [m5-1c-ingress-template-review-2026-10-04.md](m5-1c-ingress-template-review-2026-10-04.md) |
| M5-1d | config-service Ready + PG | [m5-1d-config-pg-review-2026-10-04.md](m5-1d-config-pg-review-2026-10-04.md) |
| M5-7.2d | §217③ runbook 1–6 + browser | [m5-7.2d-ingress-closure-review-2026-10-04.md](m5-7.2d-ingress-closure-review-2026-10-04.md) |

## Phase 2 — draining / scale-down (§4.4.4)

| Task ID | Plan item | Review |
|---------|-----------|--------|
| M5-2a | `/metrics` `as_active_calls` | [m5-2a-metrics-runtime-review-2026-10-04.md](m5-2a-metrics-runtime-review-2026-10-04.md) |
| M5-2b | `/health/ready` 503 draining | [m5-2b-readiness-review-2026-10-04.md](m5-2b-readiness-review-2026-10-04.md) |
| M5-2c | `AS_DOWNSCALE_GUARD_*` reads | [m5-2c-downscale-config-review-2026-10-04.md](m5-2c-downscale-config-review-2026-10-04.md) |
| M5-2d | downscale runbook | [m5-2d-downscale-runbook-review-2026-10-04.md](m5-2d-downscale-runbook-review-2026-10-04.md) |

## Phase 3 — Gate-closure evidence + §217①② (§4.4.4 / §217)

| Task ID | Plan item | Review |
|---------|-----------|--------|
| M5-3a | rollout restart | [m5-3a-rollout-review-2026-10-04.md](m5-3a-rollout-review-2026-10-04.md) |
| M5-3b | scale + `plan_scale_down` | [m5-3b-scale-guard-review-2026-10-04.md](m5-3b-scale-guard-review-2026-10-04.md) |
| M5-217 | §217①② ISSU + simulated `active_calls` | [m5-217-issu-scale-review-2026-10-04.md](m5-217-issu-scale-review-2026-10-04.md) |
| M5-H10 | Ops wiring (metrics → plan) | [m5-h10-ops-wiring-review-2026-10-04.md](m5-h10-ops-wiring-review-2026-10-04.md) |
| M5-3c | §4.5 docs + helm review annotations | [m5-3c-closure-docs-review-2026-10-04.md](m5-3c-closure-docs-review-2026-10-04.md) |

## §4.6 D12 / ADR-0026

| Task ID | Plan §4.6 checklist | Review |
|---------|---------------------|--------|
| M5-D12-adr | ADR-0026 accepted | [m5-d12-adr-0026-review-2026-10-04.md](m5-d12-adr-0026-review-2026-10-04.md) |
| M5-D12-helm | `stateStores` template + chart-check | [m5-d12-helm-state-review-2026-10-04.md](m5-d12-helm-state-review-2026-10-04.md) |
| M5-D12-kind | `M5_BUNDLED_STATE` kind | [m5-d12-kind-bundled-review-2026-10-04.md](m5-d12-kind-bundled-review-2026-10-04.md) |
| M5-D12-prod | on-prem + migrate Job + HA runbook | [m5-d12-production-profile-review-2026-10-04.md](m5-d12-production-profile-review-2026-10-04.md) |

## Explicitly out of scope for this register (§4.4.3, deferred)

HPA thresholds、capacity alerting (H12)、D3 Sentinel、M7 real SIP call-drop-free — **Deny inclusion into the M5 sign-off scope** (see the adjudication).
