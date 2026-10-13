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

# ADR-0020 — Feature capability gating and switches

- **Status**: accepted
- **Date**: 2026-09-28
- **Decides**: §0 ledger item 19 — layered feature gating (deployment-level master switch + runtime fine-grained override)
- **Responds to REQ**: REQ-G-1

## Context

- The delivery form is **single-tenant, one system per customer**, deployed outside the carrier network (AGENT.md §2). Therefore the problem a "switch" solves is **not** feature isolation between tenants, but the **start/stop / canary / rollback** of one system at the customer site.
- The product is delivered on a **unified release version** (ADR-0018), so an upgrade-window cost and risk are unacceptable. We need a mechanism to start/stop a capability, canary it by scope, and quickly roll back if necessary — without rebuilding or doing a full upgrade.
- Configuration governance already has a decision ([ADR-0006](0006-config-governance.md)): PostgreSQL version store + change-order state machine + canary distribution, rather than GitOps. Feature switches should **reuse** this pipeline, not introduce a second delivery form.
- **License gating is a non-goal**: this cycle does no License-key validation and no authorization tiering.

## Decision

Adopt **layered gating**, with the two tiers each owning a distinct responsibility:

| Tier | Granularity | Activation | Storage | Relation to change pipeline |
|---|---|---|---|---|
| ① Deployment-level master switch | Entire deployment | Hot-loaded via the config change pipeline, no restart | A class of versioned config in the PG version store | Goes change-order → approval → write PG → canary distribution → rollback |
| ② Runtime fine-grained override | number range / call / user / percentage | Hot evaluation (evaluated at decision time) | State externalized (Redis), eventually consistent | Override values are also governed by the pipeline; evaluation results must be idempotent |

- **A feature switch is a class of versioned config in the [ADR-0006](0006-config-governance.md) change pipeline**, following the same path as rules (change-order → approval → write PG → canary distribution → rollback); no new channel is opened.
- **A switch only toggles capability on/off; it does not change the interface contract.** When off, it takes the **existing default path**; it does not add a new "off-state" external behavior branch.
- Tier ② evaluation must **stay idempotent under the Redis split-brain window** (related risk R5, open item D3): repeated evaluation of the same decision yields the same result, with no inconsistent pass or repeated flip caused by read jitter within the window.
- **Every feature must be explicitly adjudicated in its ADR / HLD**:
  1. whether a switch is needed;
  2. default state (**default off**);
  3. canary strategy;
  4. **removal condition** (guard against "switch debt") — a switch is temporary scaffolding, not a permanent shape.

## Consequences

### Positive

- Capabilities can be independently started/stopped, canaried, and rolled back, without a full upgrade or rebuild of the system.
- Reuses the [ADR-0006](0006-config-governance.md) existing configuration governance, adding no new delivery form (no GitOps, no second version store, no second approval chain).
- **Default off + canary + removal condition** bounds the blast radius of "a new capability going live" to a controllable range.

### Negative / accepted

- The new runtime dimension brings **multi-replica consistency** and **split-brain idempotency** burden (related risk R5, open item D3).
- The two-tier gating increases HLD / LLD / test cost — **both the on and off states must be covered**.
- **Switch debt**: switches tend to only grow, never be removed, so each switch must state its removal condition, otherwise long-term maintenance cost keeps accumulating.
- **M0 (current milestone) does not land implementation**, only the architecture seam and rules; the evaluation granularity and config schema for runtime overrides are not yet determined (open item D7).

## Alternatives considered

| Option | Why not |
|---|---|
| No switch (full upgrade only) | Every capability start/stop requires a full upgrade; the upgrade-window cost and risk are unacceptable |
| License-key gating | Non-goal this cycle; introduces an authorization system and compliance surface, out of scope |
| Deployment-level static switch only | Cannot canary by number range / call / user / percentage; granularity insufficient |
| Runtime switch only | Lacks the deployment-level master breaker; cannot converge in one step on failure, slow rollback |

## Evidence

- No implementation evidence yet — **M0 does not land implementation**, only the architecture seam and rules. To be filled when **M2 kernel seam / M4 control plane** lands.

## Related

- [`../system-architecture.md`](../system-architecture.md) §5.3 and §0 decision 19
- [ADR-0006](0006-config-governance.md) (configuration governance: PostgreSQL version store + change-order state machine)
- Risk R5 (Redis becomes a new SPoF)
- Open item D3 (decision idempotency under Redis split-brain window), open item D7 (runtime-override evaluation granularity and config schema)
- Non-goal: **no multi-tenancy** (AGENT.md §2)
