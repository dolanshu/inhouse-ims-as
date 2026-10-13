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

# ADR-0006: Configuration governance — PostgreSQL version store + change-order state machine, not GitOps

- **Status**: accepted
- **Date**: 2026-09-28
- **Decides**: §0 ledger entry 13 — configuration governance: PostgreSQL version store + change-order state machine, not GitOps
- **Responds to REQ**: REQ-NF-10, REQ-F-12, REQ-F-14, REQ-G-1

---

## Context

On the subject of configuration changes, two constraints squeeze the design space from opposite directions.

The first comes from the delivery form. `AGENT.md` §2 lists "configuration does not go through GitOps" directly as a non-goal, with an unambiguous reason: **"Operator operations staff cannot be required to learn Git just to change a number range; versions are stored as rows in PostgreSQL, hidden behind the change-order state machine (ADR-0006). Change path: console / internal API submits a change order → approval → service writes to PostgreSQL → canary distribution. It is not operations directly UPDATE-ing the database, nor managing configuration with a git repository."** This non-goal is not a judgment on Git as a tool itself, but a judgment about the users: changing number ranges is the daily work of operator operations staff, and making the premise of that task "knows Git, can open a PR" stakes the product's usability on customer-side personnel skills, which is unacceptable in on-prem delivery.

The second comes from the risk of the change itself. Configuration is not static text; it is the input to decision behavior: one wrong number-range rule causes all calls to be misjudged or all rejected. Configuration changes must therefore be versionable, traceable, canary-deployable, and rollback-able (REQ-NF-10 verbatim: "Configuration changes must go through an approval process. Changes must be versionable, traceable, releasable via canary, and rollback-able. Operations staff are not required to learn Git to change configuration."). This is not "nice to have" — it is what the operator will ask about item by item at acceptance: who, when, under which change order, changed what into what.

Together these two eliminate two extremes. One end is a git repository: versioning, diff, and rollback semantics all come ready-made, but it directly conflicts with the §2 non-goal — gaining version semantics at the price of an entire toolchain that operations staff should not be required to master. The other end is operations directly UPDATE-ing the database: no version, no approval, no audit; when something is changed wrongly, you neither know what was changed nor can you go back. The usable range lies between the two — version semantics must be built in-house, but the change entry point must take the form operations staff already use (console / internal API).

There is also a cross-cutting constraint: ADR-0020 has already decided that feature switches **reuse** the same governance pipeline rather than opening a separate channel. This means the pipeline must accommodate two classes of configuration from the start — rules (declarative data, the criteria themselves) and switches (capability on/off) — with completely identical versioning, approval, canary, and rollback semantics for both. The pipeline is not designed for rules with switches tacked on; it is the common channel for both.

Ownership has already been decided by ADR-0007: governance state lands in PostgreSQL, runtime state in Redis. This ADR does not re-argue the storage selection; it only defines the form of governance state in PG and how changes flow through it.

## Decision

- **PostgreSQL version store: each configuration is an immutable version row.** New versions are **appended**; old versions are never overwritten, UPDATE-ed, or deleted. Each row carries a version number, configuration content, submitter, and submission time; historical versions are permanently readable, and both diff and rollback are computed over version rows, without depending on any additional source of truth. A rule's "currently effective version" is a marker on the version store, not the result of some row being rewritten.
- **Change-order state machine: `draft → submitted → approved → distributing → applied`, with side paths `rejected` and `rolled_back`.** The change order is the **only** write path for configuration; the creation of any version row must be traceable to a change order that has already completed the state machine. **The approver and approval time must be persisted** (REQ-F-14) — approval is not a verbal step in a process, but a record with an owner and a timestamp; a new version is written only after approval passes, and unapproved versions do not exist.
- **Canary distribution: notify AS instances to load the new version in batches, with a health check per batch.** Distribution is neither "effective once written" nor a single broadcast to all replicas: advance batch by batch, and after each batch loads, check instance health before advancing to the next batch. On distribution anomalies or health-check failures, **automatically roll back to the previous version**, and the rollback action itself is likewise audited. Audit records for the whole flow (submission, approval, distribution, rollback) land in PG.
- **Version reporting: AS instances report the version they have applied.** The kernel already has the contract model — `ConfigBundle` in `platform/src/as_platform/api/contract.py` (the configuration version delivered to use-case processes, containing `version` and `rules`) and `AppliedVersionReport` (returned by the instance after loading, containing `case`, `version`, `applied_at`). With reporting, "the version the control plane believes is effective" and "the version actually effective at runtime" can be aligned, rather than inferred from write-to-store time. This is also the basis for judging old/new version rule compatibility during ISSU.
- **The console does not write to the store directly.** All configuration changes go through change orders, with no bypass — the console is the submission entry point for change orders, not a write entry point for the version store. This is also the precondition for REQ-S-4 (console authentication and audit) to hold: if the change order is bypassed to reach the database directly, a segment is missing from the audit chain, and authentication has nothing to attach to.
- **Feature switches are a class of configuration version, going through the same pipeline** (ADR-0020). Switches do not open a new channel, do not create a new version store, do not create a new approval chain: like rules, they are versioned configuration undergoing the same change order → approval → write PG → canary distribution → rollback.

## Consequences

### Positive

- **Auditable, traceable.** Version rows carry submitter and time; change orders carry approver and approval time; distribution and rollback each leave records. After an incident, "who changed what into what, when, under what" can be reproduced verbatim, without stitching together logs.
- **Rollback-able, and rollback is cheap.** Rollback is not "changing the data back" but moving the effective marker back to the previous immutable version row; the previous version always exists intact, so there is no "rollback requires rebuilding history first" problem. Anomalies during distribution can also be rolled back automatically.
- **Canary-deployable.** Batches + health checks limit the blast radius of one bad change to the first batch, not all replicas.
- **Operations do not need to learn Git.** The change entry point is the console and internal API; versioning, approval, and rollback semantics are borne by the system, not shifted onto the user — this is the direct fulfillment of the §2 non-goal.
- **Switches and rules share one governance.** There is no second delivery form: no GitOps, no second version store, no second approval chain (ADR-0020's benefit comes directly from here).

### Negative / accepted

- **PostgreSQL becomes a single point of governance state.** Its availability is directly equivalent to "can configuration be changed". The failure degradation mode is describable (when PG is unavailable, configuration cannot be changed, but existing calls keep running because runtime state does not depend on PG — already established by ADR-0007), but this is not "no single point" — it is "this single point's cost is confined to the governance plane". **M5's high-availability design must cover it**; this ADR does not solve it.
- **The state machine and canary distribution are new complexity.** The change-order state machine, batch scheduling, health checks, automatic rollback, and version reporting are all things a git repository provides "for free" that must be implemented by hand here. Accepted: this complexity is exactly what buys "operations do not need to learn Git".
- **Canary granularity and configuration schema remain undecided.** Canary by number range, by call, by user, or by percentage (open item D7), as well as the schema form of the configuration itself, are not yet finalized. They must be settled before the control-plane detailed design — canary granularity determines the distribution unit and the rollback unit, and also the aggregation basis of `AppliedVersionReport`.
- **The retention period of audit data is undecided.** The value of the audit chain depends on how far back it can be reviewed, and that period has not yet been decided (the same retention-policy problem as open item O4 call-trace retention). An undecided retention period does not block the mechanism, but it affects PG capacity planning.

## Alternatives considered

| Option | Why not |
|---|---|
| GitOps (git repository manages configuration) | Directly conflicts with the `AGENT.md` §2 non-goal: operator operations staff cannot be required to learn Git just to change a number range; and the cost of self-hosting Git lies not in deployment but in operations (Gitea still needs HA/backup/upgrade/user system; GitLab CE is introducing a distributed system for one configuration version store) |
| Operations directly UPDATE the database | No version (once changed, you no longer know what was changed), no approval (approver not persisted), no audit (not traceable), not rollback-able (old value already overwritten). None of REQ-NF-10's four requirements is met |
| K8s ConfigMap + rolling update | No approval semantics and no version semantics: ConfigMap has only "the current value" and cannot answer "what was the previous version, who approved it"; and the rollback granularity is a deployment (one release) rather than configuration (one rule) — doing a rollback deployment to change one number range is unacceptable |
| Configuration-center products (Nacos / Apollo, etc.) | New external dependency and an entire independent operational surface (deployment, upgrade, backup, user system), conflicting with the single-tenant on-prem delivery form; and its built-in service discovery and configuration push semantics far exceed what is needed here |

## Evidence

- `AGENT.md` §2 non-goal verbatim: "Configuration does not go through GitOps. Operator operations staff cannot be required to learn Git just to change a number range; versions are stored as rows in PostgreSQL, hidden behind the change-order state machine (ADR-0006). Change path: console / internal API submits a change order → approval → service writes to PostgreSQL → canary distribution. It is not operations directly UPDATE-ing the database, nor managing configuration with a git repository."
- PRD REQ-NF-10 (configuration does not go through GitOps: versionable, traceable, canary-deployable, rollback-able), REQ-F-12 (rule CRUD), REQ-F-14 (approval process), REQ-G-1 (every feature must have enablement explicitly decided), REQ-S-4 (console authentication and audit).
- ADR-0007 has already decided governance state lands in PostgreSQL and runtime state in Redis; this ADR defines the form of governance state within the same mechanism, without re-arguing the selection.
- ADR-0020 has already decided feature switches reuse this change pipeline, without opening a new channel.
- Kernel contracts are in place: `ConfigBundle` in `platform/src/as_platform/api/contract.py` (`version` + `rules`, the configuration version delivered to use-case processes) and `AppliedVersionReport` (`case` + `version` + `applied_at`, returned by the instance after loading).
- Implementation evidence (version-row schema, state-machine migration implementation, batch distribution and health check, automatic rollback) to be added after M4 lands.

## Related

- [ADR-0007](0007-data-plane-split.md) Data-plane split: Redis holds runtime state, PostgreSQL holds governance state
- [ADR-0020](0020-feature-capability-gating.md) Feature capability gating: reuses this configuration-governance change pipeline
- REQ-S-4 Console authentication and audit — this ADR's "no bypass" is its precondition
- Open item D7 (canary granularity: number range / call / user / percentage, and configuration schema)
- Open item O4 (call-trace retention period) — the same retention-policy problem as audit retention
- [`../system-architecture.md`](../system-architecture.md) §5 control plane: rule governance and the change pipeline
