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

# kind — M5 cluster evidence (dev / gate optional)

Create a [kind](https://kind.sigs.k8s.io/) cluster on local Docker, load the AS / config-service images, install the Helm chart, and collect **M5-3a/b** and **7.2d** evidence.

## Prerequisites

- Docker
- `kind`, `kubectl`, `helm` (prefer `PATH`; otherwise repo `.tools/m71-bin`; or `HELM_BIN`)
- Run from the repo root

**PostgreSQL (M5-1d)**: the production chart by default does **not** bundle PG (`stateStores.enabled=false`). **kind defaults** `M5_BUNDLED_STATE=1` (§4.6 / ADR-0026): same namespace `postgres-0` + `m5-config-migrate-kind.sh`. Optionally `M5_BUNDLED_STATE=0` + compose host `:55432` (the `m5-lib.sh` gateway DSN).

## One-shot evidence

```sh
./deploy/kind/scripts/m5-cluster-evidence.sh
```

Artifacts: `artifacts/m5/<UTC-date>/cluster-evidence.log` (plus ingress check summary).

## Verification (existing cluster)

```sh
make m5-kind-verify   # gate + chart-check + Pod metrics + config-service port-forward
M5_STRICT=1 make m5-kind-verify   # no kind cluster or non-zero assertion → exit 1 (M5.1-P1-1)
```

## Step by step

| Script | Purpose |
|------|------|
| `m5-kind-up.sh` | create cluster `as-m5` (if not exists) |
| `m5-images.sh` | `docker build` + `kind load` |
| `m5-helm-install.sh` | `helm upgrade --install` (AS two use cases, HPA off) |
| `m5-ingress-evidence.sh` | **M5-1d** compose PG + **M5-1c** ingress-nginx + config-service Ingress + in-cluster / port-forward checks |
| `m5-rollout-scale.sh` | rollout restart + **§217①②/H10** (calls `m5-issu-scale-evidence.sh`) |
| `m5-issu-scale-evidence.sh` | simulate `active_calls`, ISSU draining 503, `plan_scale_down` allow/deny |
| `m5-plan-scale-down-from-metrics.sh` | pull from Pod `/metrics` and execute `plan_scale_down` |
| `m5-7.2d-evidence.sh` | **7.2d closure** (`M5_7_2D_E2E_PASSWORD`); `make m5-7.2d-evidence` |
| `m5-config-migrate-kind.sh` | `as-config-migrate` on bundled PG |
| `m5-verify.sh` | local gate + kind smoke (`make m5-kind-verify`) |
| `m5-gen-certs.sh` | kind TLS (SAN includes `console.m5.test` + localhost) |
| `m5-lib.sh` | compose PG, host gateway IP, runtime DSN (sourced by other scripts) |

## Corporate HTTP proxy

If the shell sets `http_proxy`/`https_proxy`, **do not** use bare `curl http://127.0.0.1` to verify kind (the request goes to the corporate proxy → 403/000). The evidence scripts use:

- in-cluster `curl` → `ingress-nginx-controller` Service;
- or `NO_PROXY=127.0.0.1,localhost` + `kubectl port-forward`.

## ingress-nginx admission webhook

`m5-ingress-evidence.sh` `wait`s the admission-create Job; on timeout it prints **WARN** and records `admission_job_ok=0` (see log). Never silently delete the VWC in production; if the Job fails on kind dev, register the reason in the runbook before continuing.

## Host 80/443

By default `m5-kind-up.sh` does **not** map hostPort 80/443; reaching ingress directly from the host may fail. Verification uses **in-cluster curl** or **port-forward**. If you must test 80/443 from the host, rebuild the cluster with a kind config that has `extraPortMappings` (a separate change, not the M5 default).
