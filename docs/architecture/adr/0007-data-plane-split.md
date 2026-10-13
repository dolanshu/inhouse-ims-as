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

# ADR-0007: Data-plane split — Redis holds runtime state, PostgreSQL holds governance state

- **Status**: accepted
- **Date**: 2026-09-28
- **Decides**: §0 ledger entry 14 — data-plane split: Redis holds runtime state, PostgreSQL holds governance state
- **Responds to REQ**: REQ-NF-1, REQ-NF-2, REQ-NF-10

---

## Context

The system contains two classes of state with completely different natures; their read/write patterns, persistence requirements, and failure costs are all opposite.

**Runtime state**: session state, dialog state, anti-fraud rate windows, reputation decay. Its characteristics are high-concurrency reads/writes (every hop of every call reads and writes many times), it must survive process restarts, and it can tolerate extremely small losses — the cost of losing one rate window is one inaccurate decision or one failed call, which can be absorbed by the operator network's own retries and fault tolerance.

**Governance state**: rule versions, change orders, approval records, audit logs. Its characteristics are low concurrency (configuration changes are far less frequent than calls), it must be persistent, and it must be auditable and rollback-able — "when, by whom, from what to what, under which change order" for a rule must be reproducible verbatim after an incident. ADR-0006 establishes it as a PostgreSQL version store + change-order state machine, not GitOps.

Putting them into the same store necessarily requires compromise on one side: using one database to carry both classes of data means either sacrificing latency and connection count for runtime state, or sacrificing audit and rollback capability for governance state. ADR-0002 has already rejected the direction of "using PostgreSQL to store session state" — each INVITE requires reading and writing multiple session, rate, and reputation records, and PostgreSQL is not designed for this kind of high-concurrency session read/write; the latency is unacceptable. This decision has in effect already pushed runtime state toward Redis; what this ADR must determine is the ownership of governance state, and how the boundary between the two stores is drawn.

Open item O5 (disaster-recovery level N+1 or N+M) and D3 (Redis wiring and idempotence under the split-brain window) directly affect the fault-tolerance design here; this ADR fixes the write semantics first, before they are finalized.

## Decision

- **Redis (+ Sentinel) holds runtime state.** Accessed via the `StateStore` seam established by ADR-0002 (production implementation `RedisStateStore`); all runtime-state keys **must carry a TTL**, with the key namespace unified as `as:{case}:{kind}:{id}`. TTL is a hard requirement: a runtime-state key without a TTL is de facto governance-state data, and a misuse.
- **PostgreSQL holds governance state.** Rule versions are **immutable rows** (new versions appended, old versions unchanged), change orders go through the state machine (draft → approval → canary → applied / rollback), and all changes leave a full audit trail. This is the same mechanism as ADR-0006; this ADR does not redefine it.
- **The two are not mutual failovers and do no cross-store transactions.** There is no "dual-write consistency" problem, because no piece of data needs to land in both places: a piece of data belongs either to runtime state or to governance state, determined by its nature, not by convenience. Therefore no distributed transactions, no CDC synchronization, and no compensation are needed.
- **Runtime-state writes must be idempotent.** Repeated writes for the same Call-ID must produce consistent results, to tolerate repeated execution under the Redis split-brain window (risk R5, open item D3). The idempotence requirement at the decision level is consistent with ADR-0002: within the split-brain window, rate windows may be double-counted, and idempotence is the only acceptable mitigation.
- **Backup strategies are separated.** PostgreSQL needs a backup and retention policy (governance state cannot be lost, and the audit chain cannot be erased by recovery); Redis is **not backed up** — its loss is equivalent to call failure, a cost that is acceptable, and backing it up would not reduce the magnitude of that cost.

## Consequences

### Positive

- **Each side gets the optimal selection.** Runtime state gets memory-level read/write latency and the TTL primitive; governance state gets transactions, immutable versions, and the audit chain; neither has to compromise for the other.
- **Clear failure domains.** Redis failure → new calls are affected (no state to write), but the governance plane remains operable (configuration can be changed, rolled back, and audited); PostgreSQL failure → configuration cannot be changed, but existing calls keep running (runtime state does not depend on PG). Both degradation modes are describable and drillable, without needing to make judgments at failure time.

### Negative / accepted

- **Two stores, two sets of operations and monitoring.** Capacity planning, backup, upgrade, and alerting all have to be done twice; the operational surface doubles. Accepted: this cost corresponds to the genuinely different requirements of the two data classes; merging the stores would only trade the cost for a bigger compromise.
- **Redis becomes a new SPoF (risk R5).** The sole holder of all runtime state; its availability is directly equivalent to session-state availability. Mitigated jointly by the Sentinel topology (1 primary + 2 replicas + 3 sentinels) and write idempotence — the former shortens the unavailability window, the latter guarantees repeated execution within the window does not change results. Completely eliminating the SPoF awaits the finalization of open item O5.
- **Governance state and runtime state exhibit version drift.** Rule versions advance in PG, but the versions actually loaded by each replica live in Redis or process memory, and the two are never instantaneously consistent. The mitigation is canary distribution and version reporting (ADR-0006), not strong consistency.

## Alternatives considered

| Option | Why not |
|---|---|
| All in Redis | Governance state is not auditable or rollback-able: Redis has no transactional versions or audit chain, and rule changes cannot answer "who changed what, when", nor return to the previous version after an incident |
| All in PostgreSQL | See ADR-0002: the high-concurrency read/write latency of sessions/rates/reputation is unacceptable, and the multiple reads/writes per INVITE would press the cost of transactional semantics directly onto the call path |
| Single store + partitioning | The availability and retention requirements of the two data classes conflict fundamentally: runtime state wants low latency and TTL auto-reclamation; governance state wants persistence and never auto-deletes. Same-store partitioning solves isolation, not the requirements conflict |

## Evidence

- ADR-0002 has already decided on state externalization and the `StateStore` seam, and explicitly rejected PostgreSQL for session state.
- [`../system-architecture.md`](../system-architecture.md) §4.1 process and replica model establishes the statelessization premise and the direction of state externalization.
- Open item O5 (disaster-recovery level N+1 vs N+M), D3 (Redis wiring and split-brain idempotence) — this ADR's fault-tolerance design depends on both being finalized.

## Related

- [ADR-0002](0002-per-usecase-process-state-redis.md) Runtime model and the `StateStore` seam
- [ADR-0006](0006-config-governance.md) Configuration governance: PostgreSQL version store + change-order state machine
- ADR-0009 (skeleton, not landed) ISSU is draining, not state migration
- [ADR-0010](0010-autoscaling-hpa-downscale-guard.md) Autoscaling HPA + downscale guard
- Risk R5 (Redis single point), open items O5 (disaster-recovery level), D3 (Redis wiring and split-brain idempotence)
