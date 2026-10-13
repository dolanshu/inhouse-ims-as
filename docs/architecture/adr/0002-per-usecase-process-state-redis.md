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

# ADR-0002: One process per use case + externalized state in Redis

- **Status**: accepted
- **Date**: 2026-09-28
- **Decides**: §0 decision 2 — runtime model: one process per use case + externalized state in Redis; stateless multi-replica AS
- **Responds to REQ**: REQ-NF-1, REQ-NF-2, REQ-NF-3, REQ-NF-4, REQ-NF-9

---

## Context

The POC, before the product's SIP stack was selected, used `sippy`, whose core
model is the blocking `ED2.loop()` — one process runs one event loop and can
naturally carry only one use case's SIP transactions and dialog state. This hard
constraint did not surface problems during the POC, but at productization it led
to three consequences:

1. **The process boundary is the failure-domain boundary.** Under sippy's
   blocking model, if one process crashes it affects only the use case it was
   carrying, not the others. This boundary is also the independent canary unit
   and the independent scale unit.
2. **The POC used `InMemoryStateStore`.** All sessions are lost on process
   restart. Architecture document §4.1 is explicit: unusable in production —
   on-prem operator delivery requires horizontally scaled multi-replica, and a
   single node cannot carry the full traffic load.
3. **`AGENT.md` §4 layering rule is already established: one use case, one
   process, one failure domain, one canary unit.** Each package under `apps/`
   corresponds to one independent business use case; `services/` is the control
   plane (rule governance, console); `platform/` is the kernel; `testbed/` is an
   R&D asset.

`as_platform/state_store.py` already has the `StateStore` seam interface, with an
access point reserved for `RedisStateStore`. This seam is the foundation of
externalized state.

## Decision

- **One use case = one process = one K8s Deployment.** `apps/translation`,
  `apps/anti-fraud` are independent processes; they do not share an event loop or
  process memory. `services/config-service`, `services/console` are control-plane
  processes, deployed independently from the signaling-plane processes.
- **Session state, dialog state, and caller_state (rate window, reputation
  decay) are all externalized to Redis.** The process itself holds no session-level
  state that needs persistence; restarting the process does not affect in-flight
  calls (all state survives in Redis).
- The StateStore seam is the core interface of this model, defined by
  `platform/state_store.py`; `RedisStateStore` is the production implementation.

## Consequences

### Positive

- **Stateless process → horizontally scalable**: K8s HPA can scale each use case's
  Deployment independently based on custom metrics (`active_calls`, `cps`), with
  no state migration to consider.
- **Stateless process → restartable at any time**: ISSU (In-Service Upgrade) needs
  only draining (drain traffic, wait for in-flight calls to reach zero), no state
  migration. ADR-0009 establishes this draining semantics.
- **Process boundary = failure-domain boundary**: a crash in one use-case process
  does not affect other use cases; multi-replica fault tolerance holds naturally.

### Negative / accepted

- **Redis + Sentinel becomes a hard dependency.** Redis is the sole holder of
  state, so its availability is directly equivalent to the availability of the
  AS's session state. The Sentinel topology (1 master + 2 replicas + 3 sentinels)
  must be designed before M2 (open items O5, D3). Within the Redis Sentinel
  switchover window, the anti-fraud rate window may double-count (risk R5) — the
  decision must remain idempotent-acceptable.
- **Affinity needs a two-layer safety net.** sippy is a blocking event loop; the
  LB-layer `sessionAffinity: ClientIP` cannot guarantee that dialog requests land
  on the same replica when the S-SBC reuses the source port. An application-layer
  Redis session table is needed as a backstop (architecture §4.1 risk R1).
- **Graceful shutdown draining needs a preStop hook + extended
  terminationGracePeriodSeconds.** Under sippy's blocking model, the process
  cannot exit immediately when `SIGTERM` arrives — it must first finish processing
  in-flight calls. The specific grace window and forced-release policy are defined
  by the hard ceiling on call duration.

## Alternatives considered

| Option | Why not |
|---|---|
| Multiple use cases in one process | In-process routing breaks failure-domain isolation; sippy's blocking model cannot handle multiple signaling paths (one blocking event loop is one thread) |
| Database-stored state (PostgreSQL) | PostgreSQL is not designed for high-concurrency session read/write. Every INVITE needs several session/rate/reputation records read and written, with unacceptable latency; and PostgreSQL's transaction semantics impose a hard constraint on call latency |
| In-process state + inter-process sync | Sync itself has consistency problems and high complexity; mirroring session state across multiple processes, handling race conditions, and stacking sync latency yield negative returns |

## Evidence

- `AGENT.md` §4 layering rule states the kernel is the platform, apps are use
  cases, services are the control plane, and one app must never import another app.
- `as_platform/state_store.py` already has the `StateStore` seam interface, with
  the `RedisStateStore` access point reserved.
- Architecture document §4.1 process and replica model establishes the four core
  points: process boundary, statelessness premise, two-layer affinity safety net,
  and graceful-shutdown draining.

## Related

- [`../system-architecture.md`](../system-architecture.md) §4.1 process and replica model
- [ADR-0010](0010-autoscaling-hpa-downscale-guard.md) scale HPA + downscale guard
- [ADR-0009](0009-issu-draining.md) ISSU is draining, not state migration
- Open items O5 (DR tier N+1 vs N+M), D3 (Redis wiring)
