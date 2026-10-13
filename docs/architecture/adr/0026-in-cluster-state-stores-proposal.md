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

# ADR-0026 (Proposal): In-Cluster Governance PostgreSQL and Runtime Redis — Clarifying "External" Semantics and Deployment Boundary

- **Status**: accepted
- **Date**: 2026-10-04
- **Maintainer sign-off**: 2026-10-04 —— delivery form selected is **single chart fully merged** (see Option **E** below); **not** using dual release (original Option A)
- **Decides**: §0 / D12 —— standard on-prem deploys AS workloads + dedicated PostgreSQL + Redis **in the same namespace**; **forbids** carrier IMS PG; **does not change** the ADR-0007 logical split; **partially revises** ADR-0013's "chart does not deploy PG/Redis" to "by default the same chart **optionally renders** in-cluster state (`stateStores.enabled`)"
- **Responds to REQ**: REQ-NF-1, REQ-NF-2, REQ-NF-9, REQ-NF-10; related to REQ-S-4 control-plane data landing

---

## Context

The maintainer questioned the phrasing in existing ADRs that "PostgreSQL / Redis are external dependencies." The motivation was **security and deliverability**, not a rejection of the ADR-0007 data-plane split itself.

**The AS governance PostgreSQL is not the carrier IMS core-network PostgreSQL.** The IMS side (S-CSCF, HSS, UDR, etc.) has its own configuration and subscription data stores; a third-party AS's governance state is a **product-instance-specific** rule version store, change orders, approval, and audit (ADR-0006). The two differ in trust domain, change path, backup, and compliance ownership. Pointing the AS configuration governance database "at" the same PostgreSQL that carrier IMS operations already manages typically means cross-team permissions, cross-segment access, and incident-domain coupling — under an off-net deployment premise this is hard to justify as a boundary and conflicts with the single-tenant "one customer, one complete system" delivery narrative.

**Carrier constraint (maintainer input)**: in the target deployment environment, the **carrier IMS PostgreSQL is not exposed to the AS** (no DSN, no network path, no shared instance). Therefore "have the customer fill in an existing PG address," if understood as "reuse IMS PG," is **not feasible** for such customers; the AS still needs an **independent** governance database, physically provided either by the customer's infrastructure team or co-located in the **same Kubernetes cluster and namespace** as the AS workloads.

**The actual meaning of "external" in ADR-0013** is the delivery-artifact boundary, not "must be outside the K8s cluster":

- The Helm chart **does not render or lifecycle-manage** the PostgreSQL and Redis StatefulSets / Operators / backup Jobs;
- Connection information is injected into the AS, `config-service`, and other Pods through `postgres.*`, `redis.*` (or Sentinel addresses) in `values.yaml`;
- M5 engineering evidence uses a **compose-spawned PG** (`deploy/kind/m5-lib.sh`) to satisfy kind acceptance, which also shows that "database role" and "whether the chart packages the database" are two different things.

The current chart and docs bind "customer or implementer fills in `postgres.host` / Redis topology" together with "chart does not deploy stateful components," which is easily read as "production PG/Redis must be outside the cluster." The maintainer wants: deploy a dedicated PG + Redis **in-cluster but still within the AS trust boundary**, and tighten east-west access with NetworkPolicy, rather than exposing state storage outside the cluster or relying on the IMS core database.

**Redis remains outside the Pod and outside the process** (ADR-0002): whether Redis runs behind an in-cluster Service or an out-of-cluster VIP, the AS process does not embed session state; this proposal only discusses Redis **network placement and delivery responsibility**, and does not overturn the `StateStore` / Sentinel (O5, D3) direction.

The open items **O5** (disaster-recovery tier) and **D3** (Sentinel wiring and split-brain idempotence) still constrain Redis topology; this proposal does not adjudicate them, but requires that any "in-cluster Redis" option be able to connect to the later conclusions of O5/D3.

## Decision

### Accepted (logic and boundary)

1. **ADR-0007 unchanged**: governance state → PostgreSQL, runtime state → Redis.
2. **The AS governance database and the IMS core database must be separate**; the carrier IMS PG **must not** serve as the AS DSN.
3. **Standard delivery**: PG + Redis live in the **same Kubernetes namespace** as translation / anti-fraud / config-service (single-tenant "one system").
4. **Helm delivery form (maintainer ruling)**: **Option E — single chart, single release, fully merged** (`deploy/helm/` renders the application and optional in-cluster state in one place). **Rejects Option A (dual chart / dual release)**: the maintainer judged the ISSU isolation benefit insufficient to offset the operational and version-matrix complexity of a dual release.

### Deployment options (historical comparison; **E is the only standard path**)

| Option | Summary | Ruling |
|---|---|---|
| **A. Companion release `as-state`** | Second chart + second release | **Not adopted** |
| **B. Optional subchart** | Same release, `dependencies` pulls upstream chart | **Not adopted on its own**; when E is implemented, if it reuses the upstream chart it may serve as an **implementation means** of E (still one release) |
| **C. Customer platform capability** | `stateStores.enabled=false`, only fill in external endpoint | **Retained** (customers with existing managed PG/Redis) |
| **D. Bare StatefulSet example** | Non-formal delivery | **Lab/kind aid only**, not the sole production story |
| **E. Single chart fully merged (accepted)** | One `helm upgrade` installs the in-namespace application + (when enabled by default) PG + Redis; Service DNS / Secret flow through the chart's `fullname`; behavior equals C when `stateStores.enabled=false` | **Standard on-prem** |

### Option E — implementation constraints (vs ISSU / scaling / traffic)

**Runtime is independent of chart count** (see maintainer review): HPA / draining / `as_active_calls` only act on the AS Deployment; traffic does not drive PG horizontal scaling; Redis topology still follows **O5 / D3**.

**ISSU discipline for the merged chart** (compensating for giving up the dual release boundary):

| Discipline | Requirement |
|---|---|
| **Resource labels** | state and app use different `app.kubernetes.io/component` (e.g. `state-postgres`, `state-redis`, `as-*`), facilitating `kubectl` / policy filtering |
| **Upgrade defaults** | For application ISSU: when `helm upgrade` only changes `image.*` / AS values, it **must not** trigger unnecessary changes to the PG/Redis StatefulSets (templates use stable names; PVC retention documented) |
| **Runbook chapters** | Within the same chart, still separate the **"application rollout / ISSU"** chapter from the **"state maintenance window (PG patch, Redis Sentinel)"** chapter, to avoid an upgrade silently changing the database without review |
| **Customer external store** | `stateStores.enabled=false` + `postgres.host` / `redis.*` point to the customer Service (Option C); does not render in-cluster state |

### Security: NetworkPolicy (Option E / C in-cluster endpoints)

When adopting in-cluster PG/Redis, the proposal requires at minimum:

- **Ingress**: only traffic from the AS use-case Deployments, `config-service`, `console` (and approved migration Jobs) to PG (5432) and Redis (6379 / Sentinel port) is allowed; by default deny other Pods in the same namespace and cross-namespace access.
- **Egress**: the state-store Pods **do not need** access to the SIP segment or the public internet; egress from AS application Pods remains governed by ADR-0016 (S-SBC direction), separate from the PG/Redis policy.
- **Credentials**: continue to have the customer or implementer inject `postgres.secretName` / Redis auth Secret; writing real DSNs into Git is forbidden (existing ADR-0013 constraint).

The main security gain of in-cluster placement is: **state ports are not exposed outside the cluster**, and the state plane is isolated from the IMS core data plane at both the instance and NetworkPolicy level — easier to justify in a delivery review than "relying on an unknown out-of-cluster PG topology."

### Implementation order (engineering after accepted)

1. [x] **values contract**: `stateStores.*` (default `enabled: false` to hold the AS-only gate; kind `M5_BUNDLED_STATE=1`).
2. [x] **templates**: `state-postgres.yaml`, `state-redis.yaml`, `state-networkpolicy.yaml`, `state-config-runtime-secret.yaml`; `chart-check` bundled matrix.
3. [x] **kind (M5 §4.6 / D12, not M2)**: `m5-helm-install.sh` / `m5-ingress-evidence.sh` bundled profile.
4. [x] **production (engineering artifacts)**: `values-onprem.example.yaml`, `state-migrate-job.yaml`, [`m5-state-stores-runbook.md`](../acceptance/m5-state-stores-runbook.md) HA/PITR + migrate Job; customer HA operations and D3 Sentinel replacing single-instance Redis remain **O5/D3**.
5. [x] **docs**: `system-architecture.md`, ADR-0013 Amendment (§4.6).

### Revision of ADR-0013 (accepted consequence)

- **Still holds**: the only production form is Helm; no AS-specific Operator (CRD); compose is development only.
- **Revised**: "chart does not deploy Redis / PostgreSQL" becomes —— **by default on-prem, the same chart renders it when `stateStores.enabled=true`**; when the customer uses an external store, `enabled=false` and the chart only consumes the endpoint.

## Consequences

### Positive

- **Eliminates IMS PG misinterpretation**, avoiding the undeliverable assumption of "fill in a carrier core database address."
- **The security narrative can draw a boundary diagram**: both the SIP ingress (ADR-0016) and the state plane (PG/Redis) are within the customer namespace, and NetworkPolicy is auditable.
- **Preserves the ADR-0007 / 0002 logical model**; only moves the network and operational ownership of state storage, without introducing cross-store transactions.

### Negative / accepted

- **Expanded operations surface**: backup, upgrade, capacity, and HA of in-cluster PG/Redis must have a clear owner; ADR-0013 currently pushes this to "customer or implementer," and after the companion release the product side needs a matching runbook, otherwise the problem is merely moved from "outside cluster" to "inside cluster."
- **ISSU discipline cost of the merged chart**: must rely on labels, runbooks, and template stability to avoid "upgrading the app incidentally upgrades the database"; the maintainer accepts this in exchange for single-release simplicity.
- **O5 / D3 unresolved**: in-cluster Redis does not automatically solve Sentinel and split-brain; D3 remains a hard item.
- **Coexists with literal "external PostgreSQL" in some M5 docs**: this ADR must clarify that "external = chart does not deploy," to avoid the evidence chain being misread as rejecting in-cluster PG.

## Alternatives considered

| Option | Why not (as the sole path) |
|---|---|
| Reuse carrier IMS PostgreSQL | Unavailable under the maintainer constraint; conflicts with trust domain and ADR-0006 governance ownership |
| Insist on "must be outside K8s cluster" PG/Redis | Cannot meet the security goal of "state ports only reachable in-cluster"; inconsistent with the single-namespace complete-system narrative |
| Write a dedicated CRD Operator for AS to manage PG/Redis | `AGENT.md` §2 non-goal: no Operator; consistent with ADR-0013 rejection |
| Pull session state into the process / make PostgreSQL the runtime | Rejected by ADR-0002 / 0007; out of scope of this proposal |
| Option A dual release | Maintainer rejected 2026-10-04: complexity exceeds benefit |
| Option E single-chart merge + NetworkPolicy | **accepted** |

## Evidence

- [ADR-0013](0013-helm-only-production.md) original decision: "Redis / PostgreSQL are external dependencies (**chart does not deploy them**)"; `deploy/helm/README.md` table entry `postgres.host` —— "customer-specific, **external store** (ADR-0007)" —— consistent with the chart not rendering database objects, but it did not define "external = outside the cluster."
- [ADR-0007](0007-data-plane-split.md) governance/runtime split; independent of deployment topology.
- [ADR-0006](0006-config-governance.md) governance-state form: PostgreSQL version store + change orders; instance belongs to the AS product.
- `docs/plan.md` §4.4.4 **M5-1d**: kind uses compose PostgreSQL, **not** a chart-built database.
- `deploy/helm/values.yaml` comment block: single-tenant on-prem "one namespace holds one complete system (its own Redis / PostgreSQL / AS Pod group)" —— consistent with "in-cluster own PG/Redis," inconsistent with "IMS-shared PG."
- Maintainer input (2026-10-04): carrier IMS PG not exposed to AS; requires PG/Redis inside K8s to satisfy the security boundary.

## Related

- [ADR-0013](0013-helm-only-production.md) Helm as the only production form —— the main object of "external" semantics clarification
- [ADR-0007](0007-data-plane-split.md) data-plane split —— **logic** unchanged
- [ADR-0002](0002-per-usecase-process-state-redis.md) state externalized to Redis —— outside the process, can be in-cluster
- [ADR-0006](0006-config-governance.md) AS governance-state PostgreSQL
- [ADR-0008](0008-redundancy.md) redundancy and backup checklist for stateful components
- [ADR-0016](0016-in-boundary-security.md) SIP ingress security —— complementary to the state-plane NetworkPolicy
- [ADR-0023](0023-redis-call-state-checkpoint.md) Redis checkpoint direction —— independent of PG placement
- `docs/plan.md` §5.2 **D12** —— tracks this proposal
- Open items O5, D3
