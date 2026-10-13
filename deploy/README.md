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

# `deploy/`

| Directory | Role |
|---|---|
| `helm/` | **Production delivery form.** Kubernetes + Helm; one chart manages the whole system |
| `compose/` | Development environment only. Never used for delivery |

Helm is the only production form (ADR-0013). Compose exists so a developer can stand up AS + config-service + console + Redis + PostgreSQL on a laptop; it is not a deployment target and carries no HA semantics.

## What the chart must express

- `sessionAffinity: ClientIP` on the AS Service, plus the Redis session table as a second line of defense (ADR-0002).
- `preStop` draining, extended `terminationGracePeriodSeconds`, and a PodDisruptionBudget for ISSU (ADR-0009).
- Redis and PostgreSQL as external dependencies, not in-chart stateful workloads: the operator's redundancy requirements decide how they run.
- Certificates come from a Secret or the customer's PKI; rotation must never restart the AS pod (ADR-0016).

## Status

Placeholder. The chart lands with the deployment milestone; see `docs/plan.md` for the sequence.
