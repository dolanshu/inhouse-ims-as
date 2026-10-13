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

# M8 Scope Revision and Internal-Version Wrap-up Plan (2026-10-12)

> **Status: this document is a plan, not an execution record.**
>
> - **Signs off nothing**: this document signs off no REQ, signs off no milestone, changes no `status` of any row in the sign-off matrix, and changes no count in `report.md`. Every "complete" / "final state" wording here refers to an **engineering target within this plan's scope**, not to an acceptance conclusion.
> - **Pending review**: after this document is written it is **pending maintainer review**; passing review **does not equal** execution authorization — the start of each batch still requires item-by-item approval from the maintainer (see §6).
> - **Triggering premise (maintainer instruction 2026-10-12)**: items that must depend on the carrier / customer environment are **moved to the next release**; **the premise of this version = functionality must be complete, evidence may use simulators**.
> - **Upstream pointers**: [`2026-10-06-m8-release-candidate-plan.md`](2026-10-06-m8-release-candidate-plan.md) (RC plan, the master plan of stages A–E), [`2026-10-07-m8-next-step-plan.md`](2026-10-07-m8-next-step-plan.md) (N2/N3/N4), [`../acceptance/m8-environment-evidence.md`](../acceptance/m8-environment-evidence.md) (the restriction basis), [`../acceptance/m8-test-plan-matrix.md`](../acceptance/m8-test-plan-matrix.md) (the sign-off matrix), [`2026-10-10-unfinished-assessment-and-next-plan.md`](2026-10-10-unfinished-assessment-and-next-plan.md) (the inventory of unfinished items).
> - **Numbering basis statement**: this document reuses the repository's existing numbering and **invents no new numbering**. The repository contains two similarly shaped and easily confused sets of numbering; this document always writes them per the existing usage below, and this table is authoritative for reading:
>
> | As written here | Meaning | Source |
> |---|---|---|
> | `A-1`~`A-7` (with hyphen) | RC plan **Stage A** tasks (A-1 F9 native gate … A-7 native consistency runbook) | RC plan §4 Stage A |
> | `A2`~`A6` (without hyphen) | 2026-10-10 inventory **Lane A** items (A2 real-stack build normalization … A6 version basis) | [`2026-10-10-unfinished-assessment-and-next-plan.md`](2026-10-10-unfinished-assessment-and-next-plan.md) §4 |
> | `B-1`~`B-7` (with hyphen) | RC plan **Stage B** tasks | RC plan §4 Stage B |
> | `B1`~`B6` (without hyphen) | The 2026-10-10 inventory's **maintainer adjudication items** (B1 O1 capacity target … B6 packaging document review) | same §0-A.2 / §4 Lane B |
> | `D-1`~`D-3` (with hyphen) | RC plan **Stage D** environment evidence items (D-1 carrier PKI / D-2 customer K8s / D-3 D6 testbed) | RC plan §4 Stage D; [`../acceptance/m8-environment-evidence.md`](../acceptance/m8-environment-evidence.md) |
> | `D1`~`D12` (without hyphen) | Undecided items in §5.2 of `plan.md` (D1 Python 3.10 EOL … D12 in-cluster PG/Redis HA) | [`../plan.md`](../plan.md) §5.2 |
> | `E-1`~`E-6` (with hyphen) | RC plan **Stage E** (report, version, signature) tasks | RC plan §4 Stage E |
> | `S5`~`S11` (`S7a`/`S8`) | A3 Phase D real-stack differential-check scenarios | [`2026-10-09-sip-native-testing-plan.md`](2026-10-09-sip-native-testing-plan.md) §4-D |
> | `S-1`~`S-4` (with hyphen) | Abbreviations for the matrix security rows `REQ-S-1`~`REQ-S-4` | [`../acceptance/m8-test-plan-matrix.md`](../acceptance/m8-test-plan-matrix.md) §3 |
> | `F-4`/`NF-2`/`5.4-F-13` and the like | Abbreviations for matrix row IDs (the `REQ-` prefix is omitted; backfill rows keep the `5.4-` prefix) | same |
>
> The six work batches all use **descriptive names** ("Release and Packaging", "SIP Differential Testing", "kind/sim Evidence", "Sign-off and Review", "Performance and Capacity", "Documentation and Reports"), with **no separately invented batch numbering**.

---

## 0. Factual Baseline (2026-10-12, the current state transcribed; this document rewrites no canonical document)

> This section is the factual foundation for the sections that follow. All entries are quoted from existing in-repo documents; this document **only transcribes, it does not rewrite and does not sign off**.

### 0.1 Current State of the Sign-off Matrix

The counts registered in the N2 / N3 counter-signature section of [`../acceptance/m8-test-plan-matrix.md`](../acceptance/m8-test-plan-matrix.md) on 2026-10-12 are authoritative: **pass 16 / open 17 / blocked 10 / n-a 6 / fail 0**.

| Bucket | Rows (matrix row IDs) |
|---|---|
| open 17 | F-4, F-5, F-8, F-9, F-10, F-11, F-16, NF-2, NF-5, NF-9, NF-10, NF-13, NF-14, NF-15, S-1, S-4, D12/O5-HA |
| blocked 10 | F-13, 5.4-F-13, F-15, 5.4-F-15真AS, NF-1, NF-4, NF-7, S-2, S-3, ADR-0008-演练 |

The 7 rows counter-signed under N3 (F-1/F-2/F-3/F-6/F-7/F-12/F-14) all use the signature basis "**engineering evidence accepted**", not REQ-level acceptance; M5 still fails at the REQ level and M8 is still "RC-ready, pending exit sign-off".

### 0.2 External Hard Dependencies (restriction)

Per [`../acceptance/m8-environment-evidence.md`](../acceptance/m8-environment-evidence.md): since **2026-10-07**, no real carrier S-SBC / customer K8s testing is done before Close; the following items stay `blocked` or `open` and **cannot be signed pass**:

| External hard dependency | Matrix rows it affects | What is missing |
|---|---|---|
| D-1 (carrier PKI + external-network S-SBC) | S-2, S-3 | A carrier PKI lab and an external-network S-SBC peer |
| D-2 (customer K8s) | NF-1 (live kill/restart/BYE) | A customer K8s cluster |
| ADR-0008 cross-site switchover drill | ADR-0008-演练 | Two customer / production sites (a single lab cluster does not count) |
| D12 / O5 production Redis and PostgreSQL HA | D12/O5-HA | Sentinel / streaming replication / PITR on the customer production topology (kind bundled state does not satisfy this item) |

### 0.3 Rows That Do Not Require a Customer Cluster

In the "the same restriction" section of the same document: **REQ-NF-2, REQ-NF-4, REQ-NF-9** ask for **our own kind / lab cluster** and do not require a customer cluster; the simulated S-SBC of **REQ-NF-5** was already built in M7.1 as a **transparent bridge** (no Kamailio, not a carrier S-SBC). These four rows are the main targets of the premise "evidence may use simulators".

### 0.4 Current State of the Release Image

`deploy/docker/Dockerfile` is still the **M5 process shell with no SIP listening** (`ENTRYPOINT ["python", "-m", "as_platform"]`; `EXPOSE 5060/udp 5061/tcp` is only a port declaration). Several documents explicitly state that this gap must be **filled before reopening M8** (the header of [`2026-10-07-m8-next-step-plan.md`](2026-10-07-m8-next-step-plan.md), §0 of [`../plan.md`](../plan.md), the release image row of [`pre-m8-demo-review-plan.md`](pre-m8-demo-review-plan.md)).

### 0.5 A3 Phase D Scheduling (finalized, 2026-10-12)

[`2026-10-09-sip-native-testing-plan.md`](2026-10-09-sip-native-testing-plan.md) §4-D: **P1 S5 two-leg normalized differential check → P2 S7a SDP corpus → P3 S6 rule priority → P4 S10 non-2xx → P5 S9 in-dialog → P6 S11 CANCEL race** (S11 is placed last because deterministic proof is the most expensive and the flaky risk is the greatest, consistent with the upstream rationale); **S8 is registered as a blocker** — the baseline lacks Route / Record-Route headers, so it is **not scheduled until the M2 probe capture is added**, and REQ-F-5 is not signed pass per the N4 stop line. **The scheduling is finalized, but the batch of test case implementations has not landed; starting them in batches requires maintainer authorization.**

### 0.6 Performance and Capacity

- **The HPA thresholds of NF-15 are still blocked**: a measurement batch with **per-pod CPU / memory utilization** is missing; the 2026-10-12 saturation probe (20 → 1280 CPS all successful, saturation point not reached) **recorded no resource data** and therefore does not constitute that batch (basis: §4 of [`2026-10-12-o1-and-native-reproducibility.md`](2026-10-12-o1-and-native-reproducibility.md)).
- **O1**: the internal engineering target (**CPS 1280 with no failures under the loopback model**) has been fixed and is **internal only**; **the external committed value is still not filled in** (G5 / B1; the three fill-in admission conditions in §3 of `ne-datasheet.md` are all unmet). The four downstream items — HPA thresholds, capacity-class alerts, Datasheet capacity values, and the 4.1 formal report — stay blocked.

### 0.7 F-13 / NF-7 (call traces)

There is no trace store / API; **O4** (10 days by default, configurable per deployment) and **D5** (in-cluster PostgreSQL) have been **adjudicated but not implemented** (the 2026-10-10 G6 adjudication plus [`2026-10-12-b2-b3-deferred-items.md`](2026-10-12-b2-b3-deferred-items.md) deferred them wholesale). The trace linkage part of F-16 depends on F-13. **Adjudicated on 2026-10-12: a major omission, deferred to v1.1 as a feature (requirement → ADR → design → review), not implemented in this version; F-16 is signed only for the non-trace part.**

### 0.8 Document Counts and Already-Deferred Items

- The §0.5 counts in `../acceptance/report.md` **are still open 24 / blocked 12** (pass 9 / n-a 4) and are **not synchronized** with the matrix after N2/N3 (pass 16 / open 17 / blocked 10 / n-a 6).
- **X1** capture wiring is already deferred (awaiting the carrier's monitoring-integration standard input; G3 stays undecided, the chart is not changed); **B2 / B3** are deferred wholesale to the next release; the **four Lane D items** have each been adjudicated to v1.1 / on demand (4.2 long-run report v1.1, 4.3 API version compatibility v1.1, 4.4 white paper on demand, 4.5 capability-opening mechanism on demand).

> **Destination pointer (appended 2026-10-13; the original text of item 2 above is retained unchanged)**: the destinations of the deferred items listed in this item are consolidated under
> [`../next-release-v1.1-plan.md`](../next-release-v1.1-plan.md) — **X1 capture wiring** see **§2** row 7 (inside the seven external hard dependencies table);
> **B2** see **§4-1** and **B3** see **§4-2**, with both of their four startup conditions retained as is in **§4.3** (must not start without confirmation), and B3's RPO / RTO values see **§7-4**;
> **Lane D 4.2 / 4.3** see **§3-7** (4.4 / 4.5 have been adjudicated as "on demand" and are not in the v1.1 initiation column).
> Subsequent status reviews, reports, handoffs, and new session openings that touch the leftover items in this item always **cite only that pointer**, do not itemize, and no longer list them as "actions for the maintainer".

### 0.9 Four-Layer Evidence Mechanism and Version Naming

- **Four-layer evidence mechanism** (adjudicated 2026-10-11): ① the filename is the conclusion (`docs/acceptance/artifacts/**` mandates the `PASS-` / `FAILCLOSED-` prefix); ② the environment must have a name (registered in [`../environments.md`](../environments.md); the anonymous "this machine" is forbidden); ③ the status triple `(conclusion, evidence file, date)`; ④ the guard test `tests/test_evidence_discipline.py`. The registered environment is `dev-win03ib7niepf0` (host `WIN-03IB7NIEPF0`).
- **Version naming**: §0 of [`../plan.md`](../plan.md) explicitly states there is **no v1 / v1.1 definition**; the product version number is determined **solely by the root `VERSION`** (currently `0.2.0`). The "v1 / v1.1" in other documents is not a release version definition.

---

## 1. Redrawing the Scope

### 1.1 Table A "Moved Out to the Next Release"

| Row / item | Blocker | What is needed to restart |
|---|---|---|
| S-2 / S-3 | External hard dependency D-1: no carrier PKI lab, no external-network S-SBC peer (restriction before Close since 2026-10-07) | A carrier PKI lab + an external-network S-SBC joint-debug window |
| NF-1 (live kill / restart / BYE) | External hard dependency D-2: no customer K8s cluster | A customer K8s cluster |
| ADR-0008-演练 | External hard dependency: cross-site switchover needs two customer / production sites; a single lab cluster does not count | A dual-site (customer / production) environment |
| D12/O5-HA (production Redis / PG HA) | External hard dependency: needs Sentinel / streaming replication / PITR on the customer production topology; kind bundled state does not satisfy this item | The customer production topology |
| Packaging 2.4 traffic diversion / iFC cooperation | Needs an S-CSCF / HSS-side cooperation window + a real cluster | A real cluster + an in-network cooperation window |
| Packaging 2.5 backup and restore (customer real-cluster version) | The customer real-cluster drill has not been done; kind bundled state is not production backup and restore | A customer real cluster |
| X1 capture wiring | Awaiting the carrier's monitoring-integration standard input (G3 / A5 stay undecided, the chart is not changed for now) | The carrier's monitoring-integration standard |

**"Deferred ≠ cancelled."** The restart conditions follow the basis in §0 of [`2026-10-10-unfinished-assessment-and-next-plan.md`](2026-10-10-unfinished-assessment-and-next-plan.md): **separate maintainer adjudication + the external resources being in place**; **it must not be pushed forward incidentally as part of local work**. These rows **keep their original status word** in the matrix (`blocked` / `open`); this document does not rewrite them and does not transition them to a final state early.

> **Destination pointer (appended 2026-10-13; the original text of Table A and of the basis paragraph above is retained unchanged)**: the seven rows of Table A together with the restart-condition basis in that paragraph are
> consolidated under [`../next-release-v1.1-plan.md`](../next-release-v1.1-plan.md) **§2** (the external hard dependency class) — rows 1–4 correspond to
> D-1 / S-2 / S-3, D-2 / NF-1 live, the ADR-0008 drill, and D12 / O5; rows 5–6 correspond to packaging 2.4 / 2.5, and row 7 corresponds to X1 capture wiring;
> that section's wording follows this table and the paragraph above. Also: the **O1 external committed value** see **§4-6** of the same document, and the v1.1 feature initiations see **§3**.
> Subsequent status reviews, reports, and handoffs that touch the leftover items of Table A always **cite only that pointer**; **this list no longer restates them one by one**.

### 1.2 Table B "Must Be Completed in This Version"

| Category | Content | Corresponding matrix rows / basis |
|---|---|---|
| **Functional engineering completion** within v1 scope | The SIP differential testing batch (A3 Phase D: S5 / S7a / S6 / S9 / S10 / S11 + the S8 prerequisite capture) | F-4, F-5, F-8, F-9, F-10, F-11, F-16 (see the "SIP Differential Testing" batch in §2) |
| Evidence rows obtainable via simulators / kind | Cluster-level and call-level evidence obtainable with kind / M7.1 sim | NF-2, NF-4, NF-5, NF-9, NF-10, NF-13, NF-14, NF-15; F-15 and 5.4-F-15真AS (kind + sim full stack) |
| Release actions (RC plan Stage E) | report.md, VERSION / CHANGELOG, plan.md write-back, the internal-version exit review document, the milestone signature sheet, the packaging re-check | E-1~E-6 (see the "Documentation and Reports" batch in §2) |

**F-13 / NF-7 have been adjudicated (2026-10-12, maintainer): judged a major omission, deferred to v1.1 as a feature, not implemented in this version** (see the adjudication result of item 1 in §6).

### 1.3 The Positioning of This Version (one sentence)

**This version = internal version: functionally complete + simulator evidence + reproducibly buildable release artifacts. This version is not the M8 exit sign-off** — the M8 exit sign-off is still scheduled after the external hard dependencies (Table A), and the final wording of the M8 row in §4 of `plan.md` is confirmed by the maintainer.

---

## 2. Work Breakdown of This Version (six batches, with dependency order noted)

**Dependency order**:

```text
批次 1「发布与打包」（最先，无依赖）
  ↓
批次 2「SIP 对拍」（S8 前置补采 → P1 S5 → P2 S7a → P3 S6 → P4 S10 → P5 S9 → P6 S11）
  ↓
批次 3「kind/sim 证据」（与批次 2 可部分并行；F-15 真 AS 依赖批次 1 的镜像）
  ↓
批次 4「签收与评审」（依赖批次 2/3/5 产出证据）
  ↓
批次 5「性能与容量（kind）」（可与批次 3 并行；向批次 4 供 NF-15 证据）
  ↓
批次 6「文档与报告」（最后，依赖前五个批次）
```

**Authorization (2026-10-12, maintainer)**: the **six batches in §2 are all authorized in one go** (batches 2 / 3 see item 5 in §6; batches 1 / 4 / 6 are authorized together this time; batch 5 by item 4 in §6). The agent proceeds by the dependency order above; each batch / each item leaves a separate review record; matrix rows keep their original status word; no REQ is signed; no git write operation is executed.

### 2.1 Batch "Release and Packaging" (first, no dependency)

| Item | Content | Basis |
|---|---|---|
| Dockerfile with SIP listening | The release image is currently the M5 process shell with no SIP listening (§0.4); this batch fills that in | The header of [`2026-10-07-m8-next-step-plan.md`](2026-10-07-m8-next-step-plan.md) "before reopening, put SIP listening into the release image again" |
| Reproducible image build + digest record | Reproduce the build and record the image digest | RC plan E-6 |
| Consistency of helm values-onprem / compose | The version and configuration of the three delivery states (chart onprem values / compose / image) are consistent | RC plan E-6, B-5 |
| Sanitization re-check | No secrets, no pcap, no password-bearing logs inside the artifacts | §0 sanitization red line of [`../acceptance/m8-environment-evidence.md`](../acceptance/m8-environment-evidence.md); RC plan E-6 |
| README / runbook consistent with the `AS_SIP_*` / `AS_TLS_*` implementation | The delivery documentation is aligned item by item with the actual environment variables in the code | RC plan E-6 |

**Boundaries**: image push / tag is executed only by the maintainer (RC plan E-6); this batch does not bump the root `VERSION` (the value awaits the adjudication of item 2 in §6).

### 2.2 Batch "SIP Differential Testing" (A3 Phase D landing)

**Prerequisite**: **S8** — use the M2 probe to capture the Route / Record-Route baseline (the baseline lacks these two headers, the root cause of the 2 existing skips); **S8 implementation is not scheduled before the capture is added**, and REQ-F-5 is not signed pass before the capture per the N4 stop line.

**Execution order** (scheduling finalized in [`2026-10-09-sip-native-testing-plan.md`](2026-10-09-sip-native-testing-plan.md) §4-D; this batch lands per that order):

| Order | Scenario | Matrix row advanced | Prerequisite / note |
|---|---|---|---|
| 0 | S8 baseline capture (M2 probe Route / Record-Route) | **F-5** (the capture is a prerequisite for signing F-5) | S8 is not scheduled without the capture; after the capture completes it is suggested to insert it after P3 |
| 1 | P1 S5 two-leg normalized sequence differential check | F-2 **was already counter-signed pass under N3 on 2026-10-12**; here it is a coverage extension (row status unchanged) | None (reuses the `testbed/e2e/` framework) |
| 2 | P2 S7a SDP pass-through corpus expansion (and a broader F-4 corpus) | **F-4** | Add SDP variants with media descriptions / multiple m-lines |
| 3 | P3 S6 multi-rule priority + no-match combination | F-3 **was already counter-signed pass under N3 on 2026-10-12**; here it is a coverage extension (row status unchanged) | Shares the simulation chain with S2 (404 already green) |
| 4 | P4 S10 non-2xx (486 / 480 / 408) pass-through | **F-10** | Depends on first extending the testbed peer UAS (it currently only returns 200) |
| 5 | P5 S9 in-dialog routing | **F-9** | Depends on the M7.3 context restoration engineering slice (already in place) |
| 6 | P6 S11 CANCEL and final response race | **F-11** | Deterministic proof of both race branches is the most expensive and the flaky risk is the greatest; closing out with a gap registration is permitted |

Other related items: **F-8** (the three CANCEL branches) advances together with the S4 cancel harness and the S11 differential check; the **trace linkage part of F-16** (the translation decision chain) **depends on F-13** — since F-13 has been adjudicated as deferred to v1.1, F-16 **is signed only for the non-trace part and the reason is stated**.

**Authorization premise (updated 2026-10-12)**: starting the **implementations of A3 Phase D in batches has been authorized by the maintainer in one go** (batch 2 includes the S8 baseline capture and all of P1–P6; P4 includes extending the testbed UAS with non-2xx branches); the agent advances in batches per the §4-D order and **leaves a separate review record for each batch landed**; **this plan does not counter-sign and does not presuppose that any row turns pass**.

### 2.3 Batch "kind/sim Evidence"

Rows satisfied by our own kind / lab cluster without requiring a customer cluster (§0.3) + evidence obtainable with simulators:

| Row | Evidence content | Environment |
|---|---|---|
| NF-2 | Killing translation does not affect anti-fraud (dual-Deployment isolation verified live) | kind |
| NF-4 | M7.1 sim call traffic + kind rolling update with zero loss (rolling verification with real SIP traffic, filling the gap of the currently blocked row) | sim + kind |
| NF-9 | Namespace fault isolation (Redis crash / AS crash does not affect the other namespace) | kind |
| NF-5 | Simulated-simulator swap consistency (using the M7.1 transparent bridge as the control) | sim |
| F-15 / 5.4-F-15真AS | Real AS full-stack distribution / health / automatic + manual rollback | kind + sim |
| NF-10 | Live canary distribution / rollback (evidenced together with F-15 real AS) | Same as F-15 real AS |
| 2.5 backup and restore (engineering drill) | kind bundled PG backup / restore / rebuild drill + runbook walkthrough + measured elapsed time record (RTO magnitude, not a commitment) | kind |

**Boundaries**: all of the above is **engineering / integration-layer evidence** and is not upgraded to carrier or customer acceptance (see §3); the live capture and real triggering of NF-13 / NF-14 involve X1 (capture wiring, already deferred), and their final state is handled by rationale in the "Sign-off and Review" batch. (NF-15's absence from this table is not an omission: it belongs to the §2.5 "Performance and Capacity" batch; the destination of NF-13 / NF-14 is in the preceding sentence of this paragraph.)

**Authorization (2026-10-12)**: this batch (including the 2.5 kind drill) has been authorized by the maintainer in one go; each batch landed leaves a separate review record.

### 2.4 Batch "Sign-off and Review"

| Row / item | Content |
|---|---|
| S-1 (whitelist) | Review the existing engineering evidence + backfill missing measurements; whitelist changes go through approval (linked with F-14) |
| S-4 (RBAC + tamper-proof audit) | Review + backfill missing measurements; **durable audit already has an engineering slice** (M4b-6b durable audit API / store: `PostgresAuditStore` + owner trigger blocking mutation / truncate), and this batch fills in what is missing for a formal all-green (`plan.md` §5.4: formal all-green for REQ-S-4 belongs to M8 or to a separate maintainer sign-off) |
| Row-by-row finalization of the matrix's 17 open rows | Each row gets one of **pass / n-a / defer**, and **must carry a rationale**; pass requires new evidence from this version (triple archived); rows depending on X1 or external environments (such as the live capture and real triggering of NF-13 / NF-14) transition to defer by rationale or are submitted to the maintainer for review |

**Boundaries**: the sign-off action still requires maintainer authorization / review; this document only lists the plan and does not counter-sign; "engineering evidence accepted" ≠ REQ-level acceptance passed ≠ milestone sign-off (the N3 basis continues).

### 2.5 Batch "Performance and Capacity (kind)"

| Item | Content | Boundary |
|---|---|---|
| NF-15 multi-replica measurement batch | Multi-replica measurement on kind, **recording per-pod CPU / memory utilization** | This is the prerequisite for filling in the HPA thresholds; the 2026-10-12 saturation probe recorded no resource data and cannot be reused as that batch |
| Filling in the HPA thresholds | After the kind measurement data is produced, fill `values-onprem.example.yaml`; the default `values.yaml` stays null | Already adjudicated (§6 item 4, 2026-10-12); the example states "measured on kind, not an external commitment, must be re-measured in the target environment before go-live"; the `hpa.yaml` guard is unchanged |
| Performance-layer gate (RC plan A-6) | Final state is one of two: implemented as a blocking layer, or written risk acceptance at the M8 final review | Do not implement on your own initiative, do not accept the risk on your own |
| O1 | The internal engineering target (loopback CPS 1280 with no failures) is fixed, internal only | **The external committed value is still not filled in** (G5 / B1; the three Datasheet fill-in admission conditions are unmet) |
| Capacity-class alerts | Still not added | The G5 adjudication sentence remains in effect; the `ne-datasheet.md` capacity values and the 4.1 formal report stay blocked |

**Boundaries**: this batch publishes no external capacity figure whatsoever (AGENT.md §2); internal engineering target values must not be written into any external material.

### 2.6 Batch "Documentation and Reports" (RC plan Stage E)

| ID | Task | Content |
|---|---|---|
| E-1 | Promote `report.md` to the M8 RC report | And synchronize the §0.5 counts with the matrix's current values **pass 16 / open 17 / blocked 10 / n-a 6 / fail 0** (currently open 24 / blocked 12, see §0.8) |
| E-2 | VERSION / CHANGELOG | **Already adjudicated: no bump** (§6 item 2, 2026-10-12) — VERSION stays `0.2.0`, and CHANGELOG appends an internal build entry inside the 0.2.0 section; the "version naming" row in §0 of `plan.md` remains in effect |
| E-3 | Write back the `plan.md` §0 / §4 M8 row | Write back per the actual wrap-up state of this version; the final wording of the M8 row is confirmed by the maintainer |
| E-4 | Internal-version exit review document (`docs/reviews/`) | **State explicitly that it is not the M8 exit sign-off** |
| E-5 | Milestone signature sheet | The "engineering completion" of M1 / M2 / M6 / M7 has already been counter-signed under maintainer authorization on 2026-10-12 (N2 item 9); **M8 is not signed** |
| E-6 | Packaging re-check | `test_version_consistency`; the image and Helm are reproducibly buildable; the re-check finds no secrets / no real packet captures; the README and runbook are consistent with the `AS_SIP_*` / `AS_TLS_*` implementation |

---

## 3. Evidence Environment Basis (grading of simulator evidence)

**Available environments** (all must be archived per the four-layer mechanism):

| Environment | Purpose | Registration / basis |
|---|---|---|
| Our own kind (`as-m5` / `as-m71`) | Cluster-level evidence (NF-2 / NF-4 / NF-9, F-15 real AS, NF-10, NF-15 multi-replica) | [`../environments.md`](../environments.md) (kind 0.24.0 / kubectl 1.31.4 already registered) |
| M7.1 simulated S-SBC (test CA, UDP / TCP / TLS, call load) | Call traffic differential check (NF-4), simulated-simulator swap consistency (NF-5) | [`../acceptance/m71-sim-platform-evidence.md`](../acceptance/m71-sim-platform-evidence.md) |
| `deploy/compose` | PostgreSQL / Redis dependencies (integration layer) | §2 of [`2026-10-12-o1-and-native-reproducibility.md`](2026-10-12-o1-and-native-reproducibility.md) |
| `dev-win03ib7niepf0` (host `WIN-03IB7NIEPF0`) | Gate / build / saturation probe | [`../environments.md`](../environments.md) |

**Explicitly "does not count"** (the downgrade basis for simulator evidence):

| What we have | Does not equal | Consequence |
|---|---|---|
| TLS calls on the test CA | The carrier PKI issuance chain | S-2 / S-3 still belong to Table A |
| kind bundled state | Production Redis / PG HA | D12/O5-HA still belongs to Table A |
| The M7.1 sim transparent bridge | A carrier S-SBC | The D-1 restriction is not lifted |
| The accept-all harness | The business decision path | The O1 external committed value is still not filled in (all three of the above plus real-cluster multi-replica measurement are missing) |

**Write-down discipline**: all evidence is written per the four-layer mechanism (§0.9) — the `PASS-` / `FAILCLOSED-` filename prefix, the environment name registered in `environments.md`, the status triple `(conclusion, evidence file, date)`, and the guard test `tests/test_evidence_discipline.py`. **Tool availability is never substituted for evidence, and a skip / not-run is never treated as green.**

---

## 4. Definition of Done for This Version (internal release gate-closure conditions)

Only if all of the following hold may it be called "internal version wrap-up complete":

1. **Batch completeness**: the exit criteria of the six batches in §2 are all satisfied, or equivalently satisfied after written adjustment by the maintainer.
2. **Matrix final state**: of the 17 open rows, the external-hard-dependency restriction row D12/O5-HA stays open per Table A in §1.1 and points to Table A (it is not required to reach a final state), and the other 16 rows all reach a final state (pass / n-a / defer, with a mandatory rationale); no unexplained open may be left. Of the 10 blocked rows, the rows for which this version can produce evidence (NF-4, F-15, 5.4-F-15真AS) have a final state; F-13 / 5.4-F-13 / NF-7 have been adjudicated as deferred to v1.1 as a feature and reach the final state n-a (see §6 item 1); the restriction rows (S-2 / S-3 / NF-1 / ADR-0008-演练 / D12/O5-HA) keep their original status word and point to Table A.
3. **RC report and version consistency**: the §0.5 counts in `report.md` match the matrix's current values; `VERSION` / `CHANGELOG` match the delivery artifacts (version number basis: no bump, see §6 item 2).
4. **List of non-claims**: **no claim that M8 is fully green, no claim that there is an M8 exit sign-off**; apart from the rows already counter-signed as "engineering evidence accepted", no claim is made that any REQ-level acceptance has passed.
5. **Tags only by the maintainer**: this plan executes no git write operation; the commit split, tags, and push are decided and executed by the maintainer (AGENT.md §10.4).

---

## 5. Handover List for the Next Release (inputs when M8 is reopened)

| Row / item | Blocker | What is needed to restart |
|---|---|---|
| S-2 / S-3 | D-1: no carrier PKI lab, no external-network S-SBC peer | A carrier PKI lab + an external-network S-SBC joint-debug window |
| NF-1 (live kill / restart / BYE) | D-2: no customer K8s cluster | A customer K8s cluster |
| ADR-0008-演练 | Needs two customer / production sites | A dual-site environment |
| D12/O5-HA | Needs Sentinel / streaming replication / PITR on the customer production topology | The customer production topology |
| Packaging 2.4 traffic diversion / iFC cooperation | Needs S-CSCF / HSS-side cooperation + a real cluster | A real cluster + an in-network cooperation window |
| Packaging 2.5 backup and restore (customer real-cluster version) | The customer real-cluster drill has not been done (the kind engineering drill version was done in this version, see §6 item 3) | A customer real cluster |
| X1 capture wiring | Awaiting the carrier's monitoring-integration standard input | The carrier's monitoring-integration standard |
| O1 external committed value | Missing measurement of the business decision path / saturation point observation / target-environment multi-replica (the three fill-in admission conditions in §3 of `ne-datasheet.md` are all unmet) | Real-cluster multi-replica + S-SBC path measurement |
| F-13 / 5.4-F-13 / NF-7 (call traces, a major omission) | Already adjudicated as deferred to v1.1 as a feature; no trace store / API; O4 and D5 adjudicated but not implemented | Go through the new feature process at v1.1 start (requirement → ADR → design → review) |

**The restart conditions follow the Table A basis in §1**: separate maintainer adjudication + the external resources being in place; deferred ≠ cancelled; it must not be pushed forward incidentally as part of local work. B2 / B3 (requirement + ADR drafting) and the four Lane D items have each been deferred, carried by [`2026-10-12-b2-b3-deferred-items.md`](2026-10-12-b2-b3-deferred-items.md) and by Lane D of [`2026-10-10-unfinished-assessment-and-next-plan.md`](2026-10-10-unfinished-assessment-and-next-plan.md); this list does not expand them again.

> **Destination pointer (appended 2026-10-13; the original text of the handover list and of that paragraph above is retained unchanged)**: this list has been merged into
> [`../next-release-v1.1-plan.md`](../next-release-v1.1-plan.md) — the seven external hard dependencies see **§2**;
> the F-13 / 5.4-F-13 / NF-7 call traces and the other v1.1 feature initiations see **§3**; the **O1 external committed value** see **§4-6**;
> B2 / B3 see **§4-1 / §4-2** (including the four startup conditions in §4.3).
> Any subsequent status review, report, handoff, and the organizing of "next release inputs" when M8 is reopened always **cite only that pointer**; **this list no longer restates them one by one**.

---

## 6. Items Pending Maintainer Adjudication (before starting work)

| # | Item to be adjudicated | Impact |
|---|---|---|
| 1 | **F-13 / NF-7 trace store** | **Adjudicated (2026-10-12, maintainer): judged a major omission, deferred to v1.1, going through the new process as a feature; not implemented in this version.** The trace linkage part of F-16 is signed only for the non-trace part |
| 2 | **The basis for the internal version number and the CHANGELOG entry** | **Adjudicated (2026-10-12, maintainer): no bump** — VERSION stays `0.2.0`; CHANGELOG appends an internal build entry inside the 0.2.0 section (marked internal, not a release); the image tag uses `as-platform:0.2.0-internal-<date>` for distinction; the chart is no longer synchronized; the "version naming" row in §0 of `plan.md` remains in effect |
| 3 | **2.5 backup and restore** | **Adjudicated (2026-10-12, maintainer): the complete kind engineering drill is included in this version** — a backup/restore/rebuild drill on kind bundled PG + a runbook walkthrough + a measured elapsed time record, landing `PASS-` / `FAILCLOSED-` evidence; it is stated explicitly that this does not equal the customer real-cluster version (the customer version is in the next release, see §5), and PITR / object storage / cross-site are not verified |
| 4 | **NF-15 HPA thresholds** | **Adjudicated (2026-10-12, maintainer): fill `values-onprem.example.yaml`, the default `values.yaml` stays null** — after the kind multi-replica + per-pod resource utilization batch produces data, write the `autoscaling` thresholds into the onprem example and note "measured on kind, not an external commitment, must be re-measured in the target environment before go-live"; the fail-closed null and the `hpa.yaml` guard stay as they are; ne-datasheet / capacity alerts / the 4.1 formal report stay blocked (the four G5 downstream items) |
| 5 | **Authorization to start batches 2 / 3** | **Authorized (2026-10-12, maintainer): batches 2 and 3 are authorized in one go** — batch 2 includes the S8 baseline capture and all of P1–P6 (P4 includes extending the testbed UAS with non-2xx branches); batch 3 includes the 2.5 kind drill; the agent advances in batches per the §4-D order and leaves a review record for each batch landed; matrix rows keep their original status word, and no REQ is signed |
| 6 | **Authorization to start batches 1 / 4 / 6 (and implicitly batch 5)** | **Authorized (2026-10-12, maintainer): authorized in one go** — thus all six batches in §2 are authorized; advance per the dependency order and leave a review record for each batch / item; matrix rows keep their original status word, no REQ is signed, and no git write operation is executed |

---

## 7. Boundaries (no excessive conclusions may be drawn from this plan)

1. **This document signs off no REQ / milestone, changes no row `status` in the matrix, and changes no count in `report.md`**; every "complete / final state" wording refers to an engineering target within this plan's scope.
2. **"Moved out to the next release" ≠ cancelled, ≠ resolved**; deferred items **keep their original status word** in the matrix (`blocked` / `open`) — the six-word discipline: deferred ≠ cancelled.
3. **Simulator evidence is engineering / integration-layer evidence and is not upgraded to carrier or customer acceptance**; test CA ≠ carrier PKI, kind bundled state ≠ production HA, sim transparent bridge ≠ carrier S-SBC, accept-all harness ≠ business decision path.
4. **Closing out this version ≠ the M8 exit sign-off**; the final wording of the M8 row in §4 of `plan.md` is confirmed by the maintainer, and the M8 final review confirmation block stays blank until the external hard dependencies are closed.
5. **This document has executed no git write operation** (no `add` / `commit` / `tag` / `push` / branch creation / remote change); the commit split is decided by the maintainer.
6. If this document is overturned by later evidence or by maintainer adjudication, **an appended line must state so** (date + the overturned item + the basis); it must not be silently replaced.

---

**Write date: 2026-10-12. Status: plan, pending maintainer review.**

(Upstream: [`2026-10-06-m8-release-candidate-plan.md`](2026-10-06-m8-release-candidate-plan.md), [`2026-10-07-m8-next-step-plan.md`](2026-10-07-m8-next-step-plan.md), [`../acceptance/m8-environment-evidence.md`](../acceptance/m8-environment-evidence.md), [`../acceptance/m8-test-plan-matrix.md`](../acceptance/m8-test-plan-matrix.md), [`2026-10-10-unfinished-assessment-and-next-plan.md`](2026-10-10-unfinished-assessment-and-next-plan.md).
This document signs off no REQ, signs off no milestone, changes no matrix row status, and constitutes no external commitment.)
