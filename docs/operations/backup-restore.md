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

# Backup and Restore Plan (Backup & Restore) — In-house IMS Application Server

> **Deliverable ownership**: [`../product-packaging-plan.md`](../product-packaging-plan.md) §1 second batch **2.5 Backup and restore plan + drill record**. Per §3.2 of that plan, this deliverable is **class B**: **depends on a real cluster environment, M8 real-cluster evidence currently shelved (7.2d still blocked)**, and **M8 exit sign-off is still shelved** (review **G-P1-10**). This document provides the **plan and record template**, **not** a drilled conclusion.
>
> **⚠️ The chart does not ship a backup Job.** The chart only provides a **one-time schema migration Job** (`stateStores.migrateJob`), which is **not a backup**. Backup scheduling is borne by the **customer's backup tooling** (Velero, cron Job, or out-of-cluster WAL archiving in HA scenarios).
>
> **⚠️ The built-in Redis / PostgreSQL is single replica, not HA.** The Redis HA topology values are already adjudicated (**O5 / D3, G7**: primary/replica + Sentinel, following the ADR-0008 topology, not Redis Cluster; the chart still renders single replica, with no evidence of measured failover behavior; RPO / RTO values are still not adjudicated); production PG HA is **owned by the customer** (Patroni, cloud RDS, or switch to external `postgres.host` and set `stateStores.enabled=false`). ADR-0008 defines the **redundancy wording** (in-site N+1 zero single point of failure, cross-site 1+1 warm standby, not active-active); the **HA topology is jointly decided by the customer and ADR-0008**.
> - **2026-10-10 addition (G7 / D3, synced; the original text above is preserved unchanged)**: **the values of O5 and D3 are already adjudicated** — the baseline is **in-site N+1 + cross-site 1+1 warm standby**, with Redis choosing **primary/replica + Sentinel** (ADR-0008), not Redis Cluster. **Boundaries must not be overstated**: **no rack / AZ-level fault tolerance is promised**, and **RPO / RTO values are still not adjudicated** (see the status block below). This row's "single replica is not HA" describes the **current chart's actual form**; **that fact does not change because of the adjudication** — the adjudication gives the target topology, not the deployed topology. Landing see `../plan.md` §0 decision records G7 / B3 + D3 row and [`../handoff/2026-10-11-open-adjudication-register.md`](../handoff/2026-10-11-open-adjudication-register.md) §7.
>
> **⚠️ This document contains no capacity numbers**: no CPS / CAPS / BHCA / concurrency / throughput / latency / percentage capacity, and it does not cite M6 dev-host numbers (O1 undecided, `AGENT.md` §2). This document also contains no duration commitment for backup windows.
>
> **⚠️ RPO / RTO must be recorded jointly with the customer; this document does not unilaterally give values.** The **retention period** and **storage selection** values for call traces are already adjudicated (**O4 / D5, G6**: default 10 days, deployment-configurable; in-cluster PostgreSQL) — **not yet implemented** (trace storage / query / deletion capabilities do not currently exist); **this document writes no retention days**.
> - **2026-10-10 addition (G6, synced; the original text above is preserved unchanged)**: **O4 value adjudicated** (default 10 days, deployment-configurable), **D5 selection adjudicated** (in-cluster PostgreSQL), so the "pending item" wording in the previous sentence is outdated. **But "this document writes no retention days" remains in effect, with the reason changed to**: trace storage / query / deletion **is not implemented this round**; writing down days would be stating a non-existent behavior. **RPO / RTO are still not given unilaterally by this document** — this item was **not** adjudicated together with G6 / G7.
>
> **Cross-links**: [`runbook-l1.md`](runbook-l1.md) §3.5 (backup and restore daily commands), [`runbook-l2.md`](runbook-l2.md) §6 (database and migration troubleshooting), [`rollback-playbook.md`](rollback-playbook.md) §4 (stateful component maintenance windows), [`../product/responsibility-matrix.md`](../product/responsibility-matrix.md) §2 row ⑪ / §5.1 (backup and restore RACI, window cooperation), [`../acceptance/m5-state-stores-runbook.md`](../acceptance/m5-state-stores-runbook.md) (original document, **not deleted, not moved, not rewritten**).
>
> **Status note**: the outdated "not created" annotations in upstream documents were cleaned up uniformly on 2026-10-10; the blocked states described in this document (**real cluster environment / drill records**) **still hold**.
>
> **B6 review status**: this document has been reviewed under B6 with a review record left — [`../reviews/product-packaging-review-checklist-2026-10-12.md`](../reviews/product-packaging-review-checklist-2026-10-12.md) §6 (2026-10-12 first review) and §7 (2026-10-12 closure re-review); **the conclusion awaits maintainer confirmation** and must not serve as a basis for external delivery or acceptance before confirmation (`AGENT.md` §3.3).

---

## 1. Data Classification and Backup Targets

| Data | Store | Loss consequence | Backup necessity | Current state |
|---|---|---|---|---|
| **Governance state**: rule versions, change orders, approval records, audit (schema `as_config` / `console_audit`, table `console_audit`), console users | **PostgreSQL** (chart built-in single-replica StatefulSet, or customer external PG) | **Broken audit chain**: change orders and approvers become untraceable, rule version history is lost, and the append-only semantics of the audit table are broken — such events must **also notify OP-SEC** | **Must back up** | Commands see §2; **scheduling is borne by the customer's backup tooling**; PG HA topology is decided by the customer + ADR-0008 |
| **Runtime state**: session / dialog state, anti-fraud rate windows | **Redis** (chart built-in single replica) | **In-flight call failure and counter loss** — loss ≈ call failure (ADR-0007); the AS side **cannot proactively remove in-flight calls**, so the recovery path is especially dependent on the peer not removing them | Backup strategy is **jointly decided by the customer and the maintainer** (ADR-0007 positions Redis as a backup-able item, but **does not mandate it**) | The chart's single Redis **is not HA**; the Sentinel topology values are already adjudicated **O5 / D3 (G7)** (primary/replica + Sentinel, ADR-0008, not Redis Cluster; the chart still renders single replica, with no evidence of measured failover behavior); the availability probe only produces `as_state_store_available` when `REDIS_URL` is non-empty <br>**2026-10-10 addition (G7 / D3)**: the Sentinel topology **values are adjudicated** (primary/replica + Sentinel, ADR-0008), not Redis Cluster; but the chart is still single replica, **not yet implemented**. |
| **Call traces** (complaint tracing and anti-fraud evidence by Call-ID) | **in-cluster PostgreSQL** (D5 adjudicated, G6; not yet implemented) | Trace evidence for complaint tracing / anti-fraud evidence is unavailable (no storage implementation currently) | **To be determined after implementation lands** (no trace storage to back up currently) | **Retention period O4 adjudicated (G6)** (default 10 days, deployment-configurable), **storage selection D5 adjudicated (G6)** (in-cluster PostgreSQL); **not yet implemented**: trace storage / query / deletion is not implemented this round, so this document **writes no retention days** (reason: nothing to write) and **no storage scheme** <br>**2026-10-10 addition (G6, synced; the original text in the same row is preserved unchanged)**: both **values are adjudicated** — O4 = default 10 days and deployment-configurable; D5 = **in-cluster PostgreSQL** (no longer either-or). **Not yet implemented**: trace storage / query / deletion is not implemented this round, so this row's "pending adjudication" has **substantively** turned into "**pending implementation**", and this document still writes no retention days. |
| **Certificates and credentials** | Customer PKI / k8s Secret | No impact as long as secrets are not lost | **Not in the backup script** | `tls.secretName` points to the customer Secret (`tls.crt` / `tls.key` / `ca.crt`); `AS_CONFIG_DSN` and the audit HMAC key go through Secret. **Backup scripts must not export Secret contents**; on restore, the customer re-issues them per their PKI process |

> **Hard constraint on recovery order**: governance state (PG) and runtime state (Redis) **are not isomorphic**. Redis loss ≈ in-flight call failure; PostgreSQL loss ≈ broken audit chain. **Restore PG first, then Redis, and finally re-verify the console** (§4).

---

## 2. Backup Strategy

### 2.1 PostgreSQL (governance state — the audit chain must be preserved)

**Command as written (copied verbatim from [`../acceptance/m5-state-stores-runbook.md`](../acceptance/m5-state-stores-runbook.md) §Backup & restore)**

```sh
kubectl -n <ns> exec as-3rdparty-as-postgres-0 -- \
  pg_dump -U postgres -d as_config -Fc -f /tmp/as_config.dump
kubectl -n <ns> cp as-3rdparty-as-postgres-0:/tmp/as_config.dump ./as_config.dump
```

**Prerequisites and expectations**: the governance PG is reachable; use a role with backup privileges; `kubectl cp` requires `pg_dump` inside the Pod (the official PostgreSQL image has it). Expect `./as_config.dump` to land on disk and be **non-zero in size**.

**Scheduling**: **the chart does not ship a backup Job**. Scheduling is borne by the **customer's backup tooling** — Velero, cron Job, or **out-of-cluster WAL archiving** in HA scenarios. **RPO / RTO recorded jointly with the customer**; this document does not fill in values on their behalf (`AGENT.md` §2 and this document's status block).

**Alternative path in HA scenarios**: external `postgres.host` + `stateStores.enabled=false` (customer-managed PG), or customer-side Patroni / cloud RDS.

### 2.2 Redis (runtime state — strategy jointly decided by the customer)

- ADR-0007 positions Redis as the runtime store: **loss ≈ call failure**, so backup is an **option** rather than mandatory; but **RPO / RTO must still be recorded jointly with the customer**.
- If the customer chooses to back up: execute per their Redis persistence strategy (RDB / AOF) and customer backup tooling; **this document does not adjudicate on the customer's behalf**.
- ⚠️ **Brief runtime unavailability is expected within the Redis maintenance window** — in-flight call state is all in Redis. This is **known window behavior**, not a defect; handling see [`rollback-playbook.md`](rollback-playbook.md) §4.

### 2.3 Things Not in the Backup Scope

| Not backed up | Reason |
|---|---|
| **CDR / call records** | Not collected, not delivered, not archived (ADR-0017). Call traces **are not** call records |
| **Media / RTP** | No media (ADR-0004): no RTP, no transcoding, no DTMF, no MRF |
| **Secret contents** (private keys, `AS_CONFIG_DSN`, audit HMAC key) | Re-issued by the customer PKI / Secret management process; `AGENT.md` §11/ §13 prohibit committing secrets |
| **Diameter Sh side data** | No Sh (`AGENT.md` §2); no such data |
| **LI / IRI materials** | No LI (ADR-0016), **no collection point reserved for it** |

---

## 3. PostgreSQL HA / PITR Three Tiers

> Copied verbatim from [`../acceptance/m5-state-stores-runbook.md`](../acceptance/m5-state-stores-runbook.md) §PostgreSQL HA / PITR. The chart ships a **single-replica** StatefulSet; **production HA is owned by the customer**. The table below is an **engineering recommendation**, **not** an adjudication of customer topologies.

| Tier | Minimum expectation |
|---|---|
| **Lab / kind** | emptyDir or a single PVC; **backup optional** |
| **On-prem prod** | Record **RPO/RTO** (**recorded jointly with the customer**); use `pg_dump -Fc` (see §2.1) or WAL archiving to **out-of-cluster** storage; failover is borne by the customer's Postgres HA (Patroni, cloud RDS, etc.), **or** switch to external `postgres.host` and set `stateStores.enabled=false` |
| **Restore drill** | Restore the dump to a **new instance**; if the schema version changed, **re-run `as-config-migrate`**; point the runtime Secret to the new host (steps see §4) |

**Redis HA topology values are adjudicated (O5 / D3, G7: primary/replica + Sentinel, ADR-0008, not Redis Cluster); the chart's single Redis is still not HA (single-replica rendering, no evidence of measured failover behavior).**

> **2026-10-10 addition (G7 / D3, synced; the original text above is preserved unchanged)**: **the values of O5 / D3 are adjudicated** — in-site N+1 + cross-site 1+1 warm standby, Redis using primary/replica + Sentinel (ADR-0008), **not** Redis Cluster. The previous sentence "the chart's single Redis is not HA" **remains in effect**: the adjudication gives the target topology, **not yet implemented**, and **no rack / AZ-level fault tolerance is promised**. **RPO / RTO values are still not adjudicated**, and the value fields in §2.1 / §2.2 remain blank for the customer and maintainer to fill in.

---

## 4. Recovery Steps (Restore drill)

**Prerequisites**: a usable dump has been obtained per §2.1; the governance database is reachable; **the owner DSN is used only on trusted hosts or in a one-time Job, never in a runtime Pod / Deployment** (ADR-0006; L2 §6).

| Step | Action | Verification method |
|---|---|---|
| **1. Restore dump to a new instance** | Restore on the **new** instance (do not overwrite the original instance; keep the original as a rollback reference); the DSN host uses the **new hostname** | Dump restore is error-free; both schemas `as_config` and `console_audit` exist on the new instance |
| **2. Verify roles** | Three roles: `as_config_owner` (owner) / `as_config_web` (used by runtime Pods, **not owner**) / `as_config_runtime` (`NOLOGIN` least privilege, audit append-only related) | The `AS_CONFIG_DSN` in the runtime Secret uses **`as_config_web`**, **not** the owner; `AS_AUDIT_RESOURCE_HMAC_KEY_B64` exists |
| **3. Re-run migration when the schema version changed** | Run once per schema version (command as written below); **must run first when the database is empty** | `as-config-migrate` returns successfully; repeated executions are idempotent |
| **4. Point the runtime Secret to the new host** | Update the Secret to point to the new instance (Secret contents **not provided by this document**; go through the customer Secret management process) | After each instance restarts/hot-reloads, `printenv CONFIG_VERSION` has a value and **is consistent across replicas** |
| **5. Re-verify console login** | Log in to the console from a browser over **HTTPS** (same origin) | Login succeeds and the approval queue is visible; ⚠️ **do not save credentials**, do not file session cookie screenshots |
| **6. Re-verify audit queryability** | Export audit records | Output contains no password / token; the runtime role's INSERT/UPDATE/DELETE/TRUNCATE on the audit table is **rejected** (append-only, fail-closed) |
| **7. Re-verify the Redis side** | Per the recovery order in §1, Redis comes after PG | `as_state_store_available{use_case}` returns to `1`; ⚠️ when `REDIS_URL` is not configured the **series does not exist (not 0)** |

**Migration command as written (run once per schema version; copied verbatim from the original document)**

```sh
kubectl -n <ns> port-forward pod/as-3rdparty-as-postgres-0 15432:5432
export AS_CONFIG_OWNER_DSN="postgresql://as_config_owner:<password>@127.0.0.1:15432/as_config"
export AS_CONFIG_RUNTIME_ROLE=as_config_runtime
export AS_AUDIT_SCHEMA=console_audit
export AS_CONFIG_SCHEMA=as_config
uv run as-config-migrate
```

**Helm migrate Job (production / repeatable)** — Secret `as-config-migrate-owner`'s key `AS_CONFIG_OWNER_DSN` (owner login only):

```sh
helm upgrade --install as deploy/helm -f deploy/helm/values-onprem.example.yaml ...
kubectl -n <ns> delete job/as-3rdparty-as-config-migrate --ignore-not-found
kubectl -n <ns> wait --for=condition=complete job/as-3rdparty-as-config-migrate --timeout=300s
```

⚠️ **Job reuse pitfall**: a same-named Job is not rebuilt → **must `delete job ... --ignore-not-found` first, then `wait`**, otherwise you will **wait on an already-completed old Job and misjudge success**.

---

## 5. Restore Drill Record Template

**Current state: ⚠️ No real-cluster drill record.** The table below is a template, **with no rows currently filled in**. M8 **7.2d blocked**, exit sign-off shelved (G-P1-10). ⚠️ **The elapsed-time column is filled in by the drill party; this document presets no values** (and gives no duration commitment).

| Field | Fill-in requirement |
|---|---|
| **Date** | Actual execution date of the drill (including time zone) |
| **Scope** | Governance state / runtime state / both; whether console re-verification is included |
| **Backup source** | Dump file identifier / WAL archive batch / backup tooling and schedule (**containing no credentials**) |
| **Restore target** | Host identifier of the new instance; **do not overwrite the original instance** |
| **Elapsed time** | **Filled in by the drill party**; this document presets nothing and commits to nothing |
| **Verification items** | Check all 7 steps of §4 item by item (including `CONFIG_VERSION` consistency, console HTTPS login, audit append-only rejection verification) |
| **Result** | Pass / conditional pass / fail; evidence path (`artifacts/<milestone>/<YYYY-MM-DD>/`, after redaction) |
| **Open issues** | Unclosed items, responsible party, who needs to adjudicate |

> **Record discipline**: drill records are evidence, and per `AGENT.md` §3.2 / §3.3 need a supporting independent review record to complete the documentation chain; records **do not constitute an acceptance conclusion**. kind / compose / `testbed/` simulation results **must not** serve as drill records (ADR-0014: the testbed is not a v1 deliverable).

---

## 6. Boundaries and Non-Goals

| Not doing | Reason |
|---|---|
| **CDR archiving / billing backup** | No CDR: not collected, not delivered, not archived, not priced (ADR-0017). Call traces **are not** call records |
| **Media backup** | No media: no RTP, no transcoding, no DTMF, no MRF, no media anchoring (ADR-0004) |
| **Diameter Sh side data backup** | No Sh — data comes from our own data plane (`AGENT.md` §2) |
| **LI / IRI retention** | No LI: IRI is an in-network network element function, ADR-0016 **reserves no collection point for it** |
| **Writing retention days in this document** | The call trace retention period **O4 is adjudicated (G6)** (default 10 days, deployment-configurable), and the storage selection **D5 is adjudicated (G6)** (in-cluster PostgreSQL); **not yet implemented** (nothing to write), so this document does not hard-code it <br>**2026-10-10 addition (G6)**: O4 / D5 **values are adjudicated** (10 days configurable / in-cluster PostgreSQL), but **not yet implemented**, so this prohibition **remains in effect**. |
| **Writing RPO / RTO values in this document** | **RPO / RTO values are still not adjudicated (G7 gave none)**; recorded jointly by the customer and the maintainer, this document gives no unilateral values <br>**2026-10-10 addition (G7)**: RPO / RTO **were not given values in this adjudication**, so this item is **preserved as-is, not deleted or modified**. |
| **Writing recovery duration commitments in this document** | This document gives only **steps and verification methods**; actual elapsed time is filled in by the drill party in §5 |
| **Shipping a backup Job / a second installation form** | The chart does not ship a backup Job; the only production form is Helm (ADR-0013) |

---

## 7. Undecided and Blocked

| Item | Blocking source | Impact on this document | Responsible party |
|---|---|---|---|
| **Real-cluster restore drill** | M8 **7.2d blocked**, exit sign-off shelved (G-P1-10) | §4 has only **steps and verification methods**, with **no executed drill**; §5 has **no filled-in records** | Maintainer + OP-NOC |
| **PG HA topology** | Owned by the customer (ADR-0008 / ADR-0026); the disaster recovery level **O5 value is adjudicated (G7)**: in-site N+1 + cross-site 1+1 warm standby; **not yet implemented**, with the standby site location and PG HA topology still owned by the customer | The "On-prem prod" tier in §3 is an **engineering recommendation**, not an adjudication of customer topology | OP-NET (customer SLA) + maintainer |
| **Redis HA (Sentinel)** | **O5 / D3 values are adjudicated (G7)**: in-site N+1 + cross-site 1+1 warm standby, Redis primary/replica + Sentinel (ADR-0008, not Redis Cluster); **not yet implemented** (the chart still renders single replica, with no evidence of measured failover behavior) | The loss impact of §1 runtime state can be judged, but the **recovery path** depends on customer-side topology landing and failover measured forensics | OP-NET + maintainer |
| **Call trace retention period (O4) and storage selection (D5)** | Customer compliance requirements | The trace row in §1 is registered per the G6 adjudicated wording (default 10 days, deployment-configurable; in-cluster PostgreSQL); because **not yet implemented**, this document still must not contain retention days | **OP-SEC** (A/R) + AS-Vendor |
| **ADR-0008 redundancy drill** | **blocked** in the matrix | The failover and recovery playbook for the cross-site **1+1 warm standby (not active-active)** is **not yet written**; the standby site has no in-flight calls | OP-NOC + OP-NET |
| **E5 / REQ-NF-1 (state externalization and recovery)** | REQ-NF-1 sign-off belongs to M8 (D-2 defer) | The call-level checkpoint recovery path has only **engineering slice evidence**; this document covers only the recovery of **PG / Redis, the two stores** | AS-Vendor |
| **M5D 10 deferrals** | M5 REQ-level non-pass constituents | Some control plane capabilities are still deferred, affecting the completeness of post-recovery re-verification | Maintainer |
| **RPO / RTO records** | Must be recorded jointly with the customer | The value fields in §2.1 / §2.2 are **filled in by the customer and the maintainer**, left blank in this document | AS-Vendor + OP-NOC |
| **This document's review status** | `AGENT.md` §3.3 requires an independent review record | A review record has been left under B6 review — [`../reviews/product-packaging-review-checklist-2026-10-12.md`](../reviews/product-packaging-review-checklist-2026-10-12.md) §6 (2026-10-12 first review) and §7 (2026-10-12 closure re-review); **the conclusion awaits maintainer confirmation** and must not serve as a basis for external delivery or acceptance before confirmation | Maintainer |

**Adjudication sync note for 2026-10-10 (added 2026-10-11; the original text of each row in the table above is preserved unchanged)**: the "undecided" wording in the **O5 / D3 / O4 / D5 four rows** of the table above is outdated — G7 adjudicates O5 (in-site N+1 + cross-site 1+1 warm standby) and D3 (Redis primary/replica + Sentinel), and G6 adjudicates O4 (default 10 days, deployment-configurable) and D5 (in-cluster PostgreSQL). **None of the four rows are thereby closed**: trace storage / query / deletion **is not implemented this round**; the chart is still single replica, **RPO / RTO values are not adjudicated**, and the standby site location and PG HA topology are **still owned by the customer**. The "responsible party" column in the table above and "this document must not contain retention days" **remain in effect**. Landing see `../plan.md` §0 decision records G6 / G7 rows and [`../handoff/2026-10-11-open-adjudication-register.md`](../handoff/2026-10-11-open-adjudication-register.md) §7. **This document does not constitute customer acceptance.**
**2026-10-12 addition**: the main cells related to O4 / D5 / O5 / D3 / RPO-RTO in the table above have been updated in place to the adjudicated wording (G6 / G7, not yet implemented; RPO / RTO still not adjudicated); this note remains as the audit chain.
