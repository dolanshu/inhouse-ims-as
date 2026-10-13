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

# ADR-0008: In-site N+1 zero single points of failure; cross-site 1+1 warm standby, not active-active

- **Status**: accepted
- **Date**: 2026-09-30
- **Decides**: §0 ledger entry 7 — Redundancy: in-site N+1 zero single points of failure + cross-site 1+1 warm standby
- **Responds to REQ**: REQ-NF-1, REQ-NF-3

---

## Context

The first question for a carrier-grade system is "can a single machine break". A system that stops service when one machine fails cannot enter the operator's machine room; this needs no argument — it is an entry condition.

What we deliver is **single-tenant on-premises** (REQ-NF-9): one independent instance per customer, deployed in the customer's own machine room. This means redundancy cannot be outsourced — no cloud vendor's availability-zone commitment covers for us; who bears each layer, and to what degree, must be written down before delivery.

The computing premise has already been solved by [ADR-0002](0002-per-usecase-process-state-redis.md): one process per use case, with session state, dialog state, and rate windows all externalized to Redis, and the process itself holding no session-level state that needs persistence. Therefore "multi-replica" is a natural corollary of ADR-0002, not a new burden introduced by this ADR: **when any single replica fails, there is no "the one and only copy of state" on it**. But ADR-0002 only solved the computing side; the state side (Redis, PostgreSQL) and the site side (cross-geography) remain blank, and this ADR fills exactly those two gaps.

On the cross-site side there is also a fact outside our control: **how traffic is shared between the two sites is decided by the operator's network elements (S-CSCF / S-SBC trunk priority) configuration, and is not within our delivery scope**. Architecture doc §6.1 records this as the first reason for not adopting active-active. The only thing we can decide is "in what state the standby site resides".

Another constraint comes from ADR-0002 itself: AS runtime state is in Redis. Once cross-site active-active is required, cross-site sharing or replication of runtime state (sessions, rate windows, reputation decay) becomes necessary, which would directly collide with ADR-0002's "Redis is the single source of truth" and with **open item O5** (disaster-recovery level N+1 or N+M). ADR-0002 has already listed O5 as its own known gap; this ADR does not overreach to decide it on O5's behalf.

## Decision

- **In-site: zero single points of failure.** Tolerates single-node failure (counted as N+1):
  - AS stateless multi-replica (one Deployment per use case, see ADR-0002);
  - `config-service` / `console` / observability aggregation multi-replica;
  - Redis raised to Sentinel (1 primary 2 replicas 3 sentinels);
  - PostgreSQL streaming replication + periodic backup + PITR;
  - stateful components (Redis, PG) are **all included** in the redundancy and backup checklist — a stateless computing side does not mean a stateless system.
- **Failure of any single in-site replica does not affect the business.** Replicas hold no unique state; in-flight calls' state survives in Redis; the remaining replicas continue carrying new traffic. This is the verifiable form of "zero single points of failure", not a slogan.
- **Cross-site: 1+1 warm standby, not active-active.** The standby site is **resident** with capacity ≥ the primary site, but **carries no normal traffic**; rules and configuration are synced to the standby site via `config-service`; failover relies on S-SBC-side trunk priority + automatic or manual scripts. Failover is an **operations action**, not real-time load sharing — the standby site's capacity is idle under normal conditions.
- **Why not active-active** — three reasons, none dispensable:
  1. How traffic is shared between the two sites is decided by operator network-element configuration, outside our control;
  2. active-active either shares session state across sites (replication latency + split-brain), or accepts losing in-flight calls at the moment of failure — and that SLA should be defined by the operator, not by us on its behalf;
  3. AS runtime state is in Redis (ADR-0002); replicating runtime state across sites would conflict with ADR-0002's single-source-of-truth premise and with open item O5. Warm standby's failover semantics are the simplest: **the standby site has no in-flight calls**, so failover requires no state migration and does not clash with the draining semantics of [ADR-0009](0009-issu-draining.md).
- **The disaster-recovery level itself remains open item O5.** Whether specifically N+1 (node level) or N+M (rack / AZ level) is **not decided by this ADR**. This ADR only establishes a lower bound: **in-site must have zero single points of failure**. Architecture doc §6.1 currently records N+1 (single node), noting "if tolerance of an entire rack/AZ failure (N+M) is required, Redis needs to span AZs and Pods must be forcibly spread — please point out any needed changes". O5 is decided by customer SLA (`docs/plan.md` §5.1, affecting M5's Redis topology).

## Consequences

### Positive

- **In-site tolerates single-replica / single-node failure.** This is the combined result with ADR-0002: stateless processes + externalized state + multi-replica; the statement does not hold if any of the three is missing.
- **Stateless multi-replica makes scaling and upgrades meaningful.** HPA can scale each use case independently ([ADR-0010](0010-autoscaling-hpa-downscale-guard.md)), and ISSU only needs draining without state migration ([ADR-0009](0009-issu-draining.md)). Redundancy and these two are two uses of the same set of premises.
- **Warm standby's failover semantics are the simplest.** The standby site has no in-flight calls, failover requires no state movement, and there is no intermediate state like "both sites running half of the same call at once" that defies reasoning. Predictability matters more than throughput at an incident scene.
- **The redundancy checklist is part of the deliverable.** Redis and PG are explicitly included in the redundancy and backup checklist, avoiding the half-counted judgment of "AS is multi-replica, so the system is highly available".

### Negative / accepted

- **Cross-site failover is an operations action, and there is a failover window.** The window length is jointly determined by S-SBC / trunk-side configuration and our failover scripts, and is not under our unilateral control. It must be **drilled**, not just written in the plan; failover drills belong to M5 (operations milestone) and M8 (release-candidate acceptance runs). A failover process that has never been drilled is no failover process.
- **The warm-standby site's long-term idle cost.** An entire set of resident capacity carrying no traffic (AS replica groups, config-service, Redis, PG) is pure expense. Accepted: it is the price of site-level SLA, and it buys the simplest failover semantics.
- **Redis and PostgreSQL high-availability details are not decided within this ADR.** The Sentinel topology (1 primary 2 replicas 3 sentinels) is the form recorded in architecture doc §6.1, while Sentinel's wiring and how decisions remain idempotently acceptable within the split-brain window belong to open item D3; Redis becoming a new SPoF is risk R5 in the risk register. This ADR only requires "stateful components are included in the redundancy and backup checklist" and does not give topology parameters.
- **This ADR gives no cross-site RTO / RPO figures.** They cannot be given before O5 and customer SLA are decided; giving an undecided figure is more dangerous than giving none.
- **N+1 vs N+M is undecided, which means the current design may be reworked if the customer requires rack-level disaster recovery.** Accepted: this is the cost of O5, and not something this ADR can eliminate.

## Alternatives considered

| Option | Why not |
|---|---|
| In-site single replica + fast recovery | Single-point failure stops the business and fails the entry condition; REQ-NF-1 (ongoing calls must not break when a process restarts or fails) cannot be satisfied with a single replica |
| Cross-site active-active | Traffic sharing is decided by operator network-element configuration, outside our control; and it either shares session state across sites (replication latency + split-brain), or accepts losing in-flight calls at the moment of failure — that SLA should be defined by the operator. ADR-0002 puts runtime state in Redis; replicating runtime state across sites conflicts with the single-source-of-truth premise and with O5 |
| Cross-site cold standby (standby site not resident, started after failure) | Failover requires spinning up capacity first; RTO is uncontrollable and depends on standby resources being immediately available; operator machine rooms do not offer "scale on demand" elasticity |
| Cross-site warm standby 1+1 + in-site N+1 (this decision) | Adopted. In-site tolerates single-node failure; cross-site trades idle capacity for the simplest failover semantics (standby site has no in-flight calls, no state migration needed) |
| Three-site / multi-site disaster recovery | Not requested by the requiring party (operator SLA); increasing the site count before O5 is decided would only amplify the undecided surface |

## Evidence

- Architecture doc §6.1 "Redundancy" verbatim: **"In-site: zero single points of failure (N+1, tolerates single-node failure)"** — AS stateless multi-replica; config-service / console / observability aggregation multi-replica; Redis raised to Sentinel; PG streaming replication + periodic backup + PITR; stateful components (Redis, PG) all included in the redundancy and backup checklist. Same section, **"Cross-site: 1+1 warm standby"** — the standby site is resident but carries no traffic; rules/configuration synced via config-service; failover relies on S-SBC-side trunk priority + automatic/manual scripts.
- Architecture doc §6.1 verbatim on not adopting active-active: **"Not adopting active-active: how traffic is shared between the two sites is decided by operator network-element configuration, outside our control; and active-active either shares session state across sites (latency + split-brain), or accepts losing in-flight calls at the moment of failure — this SLA should be defined by the operator. Warm standby's failover semantics are the simplest: the standby site has no in-flight calls."**
- Architecture doc §6.1 N+M note: **"⚠️ If tolerance of an entire rack/AZ failure (N+M) is required, Redis needs to span AZs and Pods must be forcibly spread — currently recorded as N+1 (single node); please point out any needed changes."**
- Architecture doc §0 decision ledger entry 7 verbatim: "Redundancy | In-site N+1 zero single points of failure + cross-site 1+1 warm standby".
- `docs/plan.md` §5.1 open item O5 verbatim: "Disaster-recovery level: N+1 (node) or N+M (rack / AZ) | M5 Redis topology | Customer SLA"; architecture doc §12.1 O5 row: "Cross-site disaster-recovery level: N+1 (single node) or N+M (rack/AZ) | Whether Redis spans AZs, Pod spread policy | Customer SLA". Neither is decided.
- Architecture doc §12.2 risk register R5 verbatim: "**Redis becomes a new SPoF** | after statelessization | Sentinel + decisions remain idempotently acceptable under the split-brain window".
- [ADR-0002](0002-per-usecase-process-state-redis.md) Evidence / Consequences: process is stateless → horizontally scalable, restartable at any time; "Redis + Sentinel becomes a hard dependency……the Sentinel topology (1 primary + 2 replicas + 3 sentinels) must be fully designed before M2 (open items O5, D3)".
- PRD REQ-NF-1 (process restart does not lose sessions) verbatim: "When a process restarts or fails, ongoing calls must not break — session state, dialog state, and business processing state must be persisted outside the process."
- PRD REQ-NF-3 (horizontally scalable) verbatim: "Supports horizontal scaling: when traffic increases, processing instances can be added without affecting existing calls; when traffic decreases, capacity can be safely reduced."
- `docs/plan.md` §4 milestone table M5 (operations) and M8 (release candidate): M8's exit criteria are "evidence-backed acceptance runs, a complete documentation chain, and a unified product version" — failover drill evidence is attributed to these two.
- Implementation evidence (multi-replica live runs, Sentinel topology wiring) to be added after M5 / M8 land; this ADR establishes the form and the lower bound, and does not fabricate redundancy implementations that do not yet exist.

## Related

- [ADR-0002](0002-per-usecase-process-state-redis.md) One process per use case + state externalized to Redis — the computing-side premise for in-site zero single points of failure
- [ADR-0009](0009-issu-draining.md) ISSU is draining, not state migration — warm-standby failover needs no state migration, consistent with this
- [ADR-0010](0010-autoscaling-hpa-downscale-guard.md) Autoscaling HPA + downscale guard — shares the "stateless multi-replica" premise with redundancy
- [ADR-0007](0007-data-plane-split.md) Data-plane split — the redundancy and backup targets for Redis and PostgreSQL respectively
- [`../system-architecture.md`](../system-architecture.md) §6.1 Redundancy, §12.1 open item O5, §12.2 risk R5
- Open items O5 (N+1 vs N+M / M5 / customer SLA) and D3 (Redis wiring and split-brain window) — both **undecided**; this ADR does not decide them on their behalf

## Amendment 2026-10-06 (M5.1 minimal set; SPoF gap registration relative to ADR-0026)

- This ADR's requirement of "in-site zero single points of failure" (Redis Sentinel 1 primary 2 replicas 3 sentinels + PG streaming replication + backup + PITR) and the single-replica built-in state stores actually rendered by ADR-0026's standard path (PostgreSQL StatefulSet `replicas: 1`, Redis Deployment `replicas: 1`) **have a gap**: the built-in path is a single point, and production HA is declared as customer-owned per the runbook (see `docs/acceptance/m5-state-stores-runbook.md`).
- This Amendment only registers the gap and does not relax this ADR's in-site zero-single-point-of-failure requirement; the final form of production HA and its acceptance criteria are deferred to the **M8 exit review** (O5 customer SLA decision), at which point either customer-owned HA is accepted or Sentinel/streaming-replication implementation is added. The cross-site failover drill (A-2) is likewise deferred, see `docs/reviews/m5-req-acceptance-review-2026-10-06.md`. (REQ-NF-1, REQ-NF-3; ADR-0026; plan §5.1 O5/D12.)
