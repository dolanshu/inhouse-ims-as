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

# M5 downscale and draining operations runbook

> Criterion implementation: `platform/src/as_platform/ops/downscale_guard.py` (ADR-0010)  
> Execution semantics: ISSU = draining (ADR-0009)  
> Plan: `docs/plan.md` §4.4.4 M5-2d / M5-3b

## 1. Prerequisites

- Each Pod can query **`as_active_calls`** (`GET :8080/metrics` or telemetry export).
- `AS_DOWNSCALE_GUARD_ENABLED` / `AS_DOWNSCALE_GUARD_PROTECT_ABOVE` injected via Helm ConfigMap (default enabled + threshold 0).
- HPA **may be disabled** (no thresholds before O1/M6); downscale can be manual or a cluster autoscaler proposing replica counts.

## 2. Input: `plan_scale_down`

Collect for each instance:

| Field | Source |
|-------|--------|
| `instance_id` | `POD_NAME` / `pod` label |
| `active_calls` | Prometheus `as_active_calls{pod="..."}` or `/metrics` |
| `draining` | Pod already went through cordon + delete flow and readiness is already 503 |

Call:

```python
from as_platform.ops.downscale_guard import InstanceLoad, plan_scale_down

plan = plan_scale_down(
    (
        InstanceLoad("as-translation-abc", active_calls=0, draining=False),
        InstanceLoad("as-translation-def", active_calls=3, draining=False),
    ),
    desired_replicas=1,
    protect_above=0,  # matches AS_DOWNSCALE_GUARD_PROTECT_ABOVE
)
```

- `plan.allowed` is `False`: not enough zero-call instances to delete → **do not delete the Pod**, or initiate draining on the high-load instance first.
- `plan.candidates`: list of instance IDs safe to delete first (still must go through draining, no SIGKILL).

## 3. Recommended order (manual downscale)

1. **Compute** `plan_scale_down` (or a wrapper ops script).
2. For each Pod in **removable**: before `kubectl delete pod` confirm `active_calls==0`; Kubernetes deletion triggers `preStop sleep` + SIGTERM.
3. For Pods **still carrying calls**: do not delete; wait for natural end, or end calls at the business layer; readiness after `request_terminate` becomes **503**, Endpoint should shed traffic.
4. If `blocked`: only shrink the `removable` subset, or wait.

## 4. M5 test hooks

- Set `AS_M5_SIMULATED_ACTIVE_CALLS=N` (test/evidence only): simulates N in-flight calls; after SIGTERM decrements by 1 per second, used by the kind evidence script to verify draining and the criterion.

## 5. Evidence paths

- **§217①② + H10**: `bash deploy/kind/m5-issu-scale-evidence.sh` (or `make m5-issu-scale-evidence`) → `artifacts/m5/<date>/issu-scale-evidence.log`
- Full bundle: `deploy/kind/m5-cluster-evidence.sh` (includes rollout + ISSU/scale)
- Cluster experiment logs: `artifacts/m5/<date>/cluster-evidence.log`
