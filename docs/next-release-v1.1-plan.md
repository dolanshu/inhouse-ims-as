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

# Project Plan for the Next Release (the v1.1 batch)

> Written to disk: 2026-10-13. **Nature: a registry carrier — not an execution plan, not a schedule.**
> This document signs off no REQ / milestone, changes no matrix status word, changes no count in
> `docs/acceptance/report.md`, and performs no git write operation.

---

## 0. Positioning and framing

This document **consolidates into a single carrier** the leftover items of the current version (the M8 internal release), which were scattered across several documents, so that they can be taken up in one go when the next release batch is scheduled.

- **This document is the single tracking carrier for the next release batch (referred to here as v1.1)**; the current project (the M8 internal release) closed on 2026-10-13 (`plan.md` §0 decision-record row of 2026-10-13, "M8 exit signature (path C)", and [`reviews/m8-external-dependency-risk-acceptance-2026-10-13.md`](reviews/m8-external-dependency-risk-acceptance-2026-10-13.md)), and the disposition of all of its leftover items is closed out here.
- **"v1.1" is a batch code name, not a release version number** — it follows the existing usage in the Lane D table of [`handoff/2026-10-10-unfinished-assessment-and-next-plan.md`](handoff/2026-10-10-unfinished-assessment-and-next-plan.md) (that table states explicitly: "'v1.1' means **the next batch** per this table's existing usage, **not a formal release version definition**"). The release version number is taken only from the root `VERSION` (currently `0.2.0`, not bumped, not tagged).
- **The "version naming" row in [`plan.md`](plan.md) §0 remains the authoritative framing**: "**There is no v1 / v1.1 definition**……to define one, it must be written in this document and confirmed by the maintainer". This document **follows the existing usage** and **does not** make a release version definition on behalf of `plan.md`.
- **Follow-on framing** (identical in framing to §12.2 of [`handoff/2026-10-10-unfinished-assessment-and-next-plan.md`](handoff/2026-10-10-unfinished-assessment-and-next-plan.md) and the added paragraph in §3 X1 of [`handoff/2026-10-11-open-adjudication-register.md`](handoff/2026-10-11-open-adjudication-register.md)): in any status review, report, handoff, or new-session opening, anything involving this version's leftover items shall **only write a "see §X of this document" pointer** — no item-by-item expansion, no separate reminders, and no further listing under "maintainer actions pending".
- **Deferred ≠ cancelled**. The restart condition for both the external hard-dependency class and the adjudicated-not-to-do class is uniformly: **a separate maintainer adjudication + the external resource being in place**; it must not be advanced incidentally as part of local work (verbatim from after table A in §1.1 of [`handoff/2026-10-12-m8-scope-revision-internal-release-plan.md`](handoff/2026-10-12-m8-scope-revision-internal-release-plan.md)).
- This document signs off no REQ / milestone, constitutes no external commitment, and produces no capacity or SLA figures.

---

## 1. Sources and consolidation notes

| Existing list | Path | Corresponding section here |
|---|---|---|
| M8 external hard-dependency risk acceptance §1 (the four external hard dependencies) | [`reviews/m8-external-dependency-risk-acceptance-2026-10-13.md`](reviews/m8-external-dependency-risk-acceptance-2026-10-13.md) §1 | §2 |
| M8 external hard-dependency risk acceptance §2 (the five v1.1 project-initiation items) | same §2 | §3 (rows 1–5) |
| M8 scope re-division §1.1 table A "moved out to the next release" | [`handoff/2026-10-12-m8-scope-revision-internal-release-plan.md`](handoff/2026-10-12-m8-scope-revision-internal-release-plan.md) §1.1 | §2 |
| M8 scope re-division §5 list handed over to the next release | same §5 | §2, §4-6 |
| Unfinished-items assessment §12 "adjudicated-not-to-do registry" | [`handoff/2026-10-10-unfinished-assessment-and-next-plan.md`](handoff/2026-10-10-unfinished-assessment-and-next-plan.md) §12 | §6 |
| Undecided-item registry in `plan.md` §5 (§5.1 / §5.2 / §5.2-bis / §5.3 / §5.4) | [`plan.md`](plan.md) §5 | §4 |
| B2 / B3 deferred-item registry (including the four start conditions in §4 and the deferral in §5) | [`handoff/2026-10-12-b2-b3-deferred-items.md`](handoff/2026-10-12-b2-b3-deferred-items.md) §0–§5 | §4 (rows 1–3), §7-4 |
| The "maintainer items pending" sections of the M8 batch completion handoffs | [`handoff/2026-10-12-m8-batch3-complete-handoff.md`](handoff/2026-10-12-m8-batch3-complete-handoff.md) §6, [`…-batch4…`](handoff/2026-10-12-m8-batch4-complete-handoff.md) §5, [`…-batch5…`](handoff/2026-10-12-m8-batch5-complete-handoff.md) §6, [`…-batch6…`](handoff/2026-10-12-m8-batch6-complete-handoff.md) §5 | §5, §7 |
| M8 batch 1 handoff (no "maintainer items pending" section; the uncommitted changes are recorded in §2.3) | [`handoff/2026-10-12-m8-batch1-complete-handoff.md`](handoff/2026-10-12-m8-batch1-complete-handoff.md) §2.3 | §5-6 |

> Batch 2 "SIP parity" **left no completion handoff document** (there is no `m8-batch2` file under `docs/handoff/`); this document does not write one on its behalf.

---

## 2. External hard-dependency class (restart = maintainer adjudication + external resource in place)

The wording follows verbatim §1 of [`reviews/m8-external-dependency-risk-acceptance-2026-10-13.md`](reviews/m8-external-dependency-risk-acceptance-2026-10-13.md) and §1.1 table A / §5 of [`handoff/2026-10-12-m8-scope-revision-internal-release-plan.md`](handoff/2026-10-12-m8-scope-revision-internal-release-plan.md).

| Existing ID / item | Blocker (what is missing) | Why this version's evidence cannot substitute | What is needed to restart | Source pointer |
|---|---|---|---|---|
| **D-1 / S-2 / S-3** (carrier PKI + external-network S-SBC) | Missing a **carrier PKI lab** and an **external-network S-SBC peer** | This version's TLS uses a **test CA** (a self-signed chain), which is **not the same as a carrier-issued chain**; the M7.1 simulated transparent bridge is not a carrier S-SBC; a test CA does not satisfy REQ-S-2 / REQ-S-3 | A carrier PKI lab + an external-network S-SBC joint-debugging window | `reviews/m8-external-dependency-risk-acceptance-2026-10-13.md` §1 item 1; `handoff/2026-10-12-m8-scope-revision-internal-release-plan.md` §1.1 row 1 / §5 row 1 |
| **D-2 / NF-1 live** (kill / restart / in-dialog BYE, customer K8s) | Missing a **customer cluster** | **A kind cluster of our own is not the customer's K8s**: network policies, storage classes, node behaviour, and real operations actions are all non-equivalent; kind evidence reaches only the engineering and integration layers | A customer K8s cluster | same §1 item 2; `handoff/…m8-scope-revision…` §1.1 row 2 / §5 row 2 |
| **ADR-0008** cross-site switchover drill | Requires **two customer / production sites** to perform a site-level switchover | **A single lab cluster does not count**: a single cluster has no site boundary, no cross-site clock or network-partition conditions, and the drill conclusion is not transferable | A dual-site (customer / production) environment | same §1 item 3; `handoff/…m8-scope-revision…` §1.1 row 3 / §5 row 3 |
| **D12 / O5-HA** (production Redis / PostgreSQL HA) | Missing a **production-grade HA deployment** (Sentinel / Cluster, streaming replication, PITR) | **kind bundled state is not production HA**: it does not cover Sentinel failover, PostgreSQL streaming replication, or a PITR restore drill; the backup-restore drill has only been verified on bundled PG | The customer's production topology | same §1 item 4; `handoff/…m8-scope-revision…` §1.1 row 4 / §5 row 4 |
| **Packaging 2.4 traffic diversion / iFC coordination** | Requires a coordination window on the S-CSCF / HSS side plus a real cluster | The real-cluster drill has not been done; responsibility for iFC triggering sits on the S-CSCF / HSS side | A real cluster + an in-network coordination window | `handoff/2026-10-12-m8-scope-revision-internal-release-plan.md` §1.1 row 5 / §5 row 5 |
| **Packaging 2.5 backup restore** (customer real-cluster version) | The customer real-cluster drill has not been done (**the kind engineering-drill version was done in this release**, see item 3 of §6 in that document) | kind bundled state is not production backup restore; PITR / object storage / cross-site are not verified | A customer real cluster | same §1.1 row 6 / §5 row 6 |
| **X1 scrape wiring** (annotation vs ServiceMonitor / PodMonitor) | Awaiting the carrier's monitoring-integration standard as input (G3 / A5 remain undecided; the chart is not changed at present) | Passing `promtool` syntax validation does not mean the scrape wiring is closed (P4 is syntax, X1 is wiring — they are different) | The carrier's monitoring-integration standard | same §1.1 row 7 / §5 row 7; `handoff/2026-10-11-open-adjudication-register.md` §3 X1 "adjudication written to disk (added 2026-10-12)" |

These seven items **keep their original status words** in the matrix (`blocked` / `open`); this document does not rewrite them and does not pre-emptively move them to a terminal state (verbatim from after §1.1 in [`handoff/2026-10-12-m8-scope-revision-internal-release-plan.md`](handoff/2026-10-12-m8-scope-revision-internal-release-plan.md)).

---

## 3. The v1.1 project-initiation class (goes through the requirement → ADR → design → review new-feature flow)

Rows 1–5 follow verbatim the table in §2 of [`reviews/m8-external-dependency-risk-acceptance-2026-10-13.md`](reviews/m8-external-dependency-risk-acceptance-2026-10-13.md).

| # | Existing ID | Content | Why it is not implemented in this version | Start-up flow | Source pointer |
|---|---|---|---|---|---|
| 1 | **F-5** | **Record-Route** on the trunk leg of product-side AS forwarding | Not initiated and not implemented in this version (the matrix marks that behaviour `defer`) | requirement → ADR → design → review | `reviews/m8-external-dependency-risk-acceptance-2026-10-13.md` §2 item 1 |
| 2 | **F-8** | **Real-stack parity for the three CANCEL branches** + a native C++→Python JSON callback | same | same | same §2 item 2 |
| 3 | **F-9** | **in-dialog re-INVITE / UPDATE** | same | same | same §2 item 3 |
| 4 | **F-11** | **CANCEL preceding any downstream response** | same | same | same §2 item 4 |
| 5 | **F-13 / 5.4-F-13 / NF-7 call tracing** | Query SIP message traces by Call-ID plus retention-period cleanup; **adjudicated a major omission** (a regression against the POC baseline capability; there has been zero product-level implementation to date) | same; no trace store / API; O4 and D5 have been adjudicated but not implemented | same | same §2 item 5; the 2026-10-12 "F-13 / NF-7" row in the §0 decision record of `plan.md`; the "major omission ruling" paragraph after the §5.4 table of `plan.md` |
| 6 | **REQ-F-12 caller-ID / regex rules** (four-dimension UI) | The two capability dimensions: caller ID and regex | M4 live covers only called-party + prefix; the F-12 / F-14 sign-off scope is **limited to called-party + prefix**, and caller ID / regex remain `n-a` | same | the "caller ID / regex rules (REQ-F-12 four-dimension UI)" row of the §5.4 table in `plan.md` (planned attribution = v1.1); the last sentence of §4 of `handoff/2026-10-12-remaining-items-execution.md` |
| 7 | **Lane D 4.2** (7×24 long-stability report) and **4.3** (API version compatibility policy) | 4.2's production-readiness review needs stability evidence; 4.3 closes out the "candidate, undecided" placeholder in §7 of `version-lifecycle.md` | The attribution ruling is "v1.1" and it is not folded into this version's milestones; 4.3 is a new decision requiring a requirement + ADR + review record | same | the Lane D table and the "status (added later on 2026-10-12)" paragraph of `handoff/2026-10-10-unfinished-assessment-and-next-plan.md`; the 2026-10-12 "Lane D four items: attribution chosen from three options" row in the §0 decision record of `plan.md` |
| 8 | **Zero-call-loss rolling-upgrade enhancement feature** | Zero call loss during a rolling upgrade (candidate directions: process-level drain, S-SBC transparent bridge + StateStore, instance stickiness, maintenance-window definition, etc.) | REQ-NF-4 is signed pass in this version on the basis of "accepting the measured call loss" (**not "zero loss achieved"**); strict zero call loss is listed as a future release enhancement, and this version neither initiates it nor defines a requirement for it | same | the 2026-10-12 "REQ-NF-4 rolling upgrade signed pass on the basis of 'accepting measured call loss'" row in the §0 decision record of `plan.md`; B3-02 in `reviews/m8-batch3-kind-sim-evidence-review-2026-10-12.md` |
| 9 | **FM** (Fault Management) | Fault-management capability | Positioned as a **new feature for a future project / future batch**; at present it is not initiated, not implemented, has no requirement defined, and gets no demo or functional documentation | On future start-up it goes through the existing new-feature flow (requirement → ADR → design → review) | §2 P6 "current-state correction" and the P6 row of the §5 summary table in `handoff/2026-10-11-open-adjudication-register.md`; the 2026-10-11 P6 row in the §0 decision record of `plan.md` |
| 10 | **REQ-F-14 linkage: whitelist changes take effect after approval** (option ① of M8 batch 4 **D4-01**) | Bring "whitelist changes" into the change-order approval flow | D4-01 is **one of two options and remains undecided**: ① bring it under the change order (a v1.1 new feature; this version does not initiate it and the matrix row stays `defer`); ② amend the matrix row L86, "whitelist changes go through approval (F-14 linkage)", which conflicts with the code facts (if ② is chosen the row can move to pass on the strength of supplementary rejection-scenario test evidence). This row corresponds only to option ① | requirement → ADR → design → review | [`handoff/2026-10-12-m8-batch4-complete-handoff.md`](handoff/2026-10-12-m8-batch4-complete-handoff.md) §5 item 1 |

The start-up flow is always `requirement → ADR → HLD/LLD → contract → code+tests → acceptance items + review record` (`AGENT.md` §3).

---

## 4. The class "value adjudicated, implementation not landed" / awaiting a maintainer value

| # | Existing ID | Adjudicated value | What is still not landed | Blocking source | Source pointer |
|---|---|---|---|---|---|
| 1 | **B2 / O4 / D5** call-trace retention and storage | O4 = default retention **10 days**, configurable at deployment; D5 = **in-cluster PostgreSQL**; Redis continues to serve runtime checkpoints | The trace **storage / query / delete implementation has not landed**; the cleanup trigger point and the time-counting basis are "implementation details pending definition"; the fact recorded in `security-privacy.md` §4.1 that the chart has **no backup Job** is unchanged | The drafting of B2's requirement / ADR has been deferred as a whole (see §4-3); F-13 / NF-7 have also moved to v1.1 initiation (§3-5) | `handoff/2026-10-12-b2-b3-deferred-items.md` §0 table B2 row and §1 (deliverables and known prerequisite facts); the G6 row in the §0 decision record of `plan.md`; the D5 row in `plan.md` §5.2 |
| 2 | **B3 / O5 / D3** Redis HA and disaster recovery | O5 = **N+1 within a site + 1+1 warm standby across sites** (no rack / AZ-level fault-tolerance promise); D3 = **Redis primary/replica + Sentinel** (ADR-0008), Redis Cluster is not chosen | **The Sentinel implementation has not landed**; whether ADR-0008 covers the concrete Sentinel topology (how many Sentinels, quorum, relationship to K8s scheduling) is to be confirmed; **the RPO / RTO figures are still undecided** | Same as §4-3; RPO / RTO are external availability commitments and require a maintainer value (§7-4) | `handoff/2026-10-12-b2-b3-deferred-items.md` §0 table B3 row, §2 (deliverables and known prerequisite facts) and §5; the G7 row in the §0 decision record of `plan.md` |
| 3 | **The four start conditions of B2 / B3** | — (the conditions themselves, not values) | Confirm each one before the next start of work (the four conditions are retained verbatim, see below) | No start without confirmation | `handoff/2026-10-12-b2-b3-deferred-items.md` §4 |
| 4 | **M5D-1 … M5D-6** | — | All six rows are "moved out of v1" and **remain unimplemented**; M5D-1 / M5D-5 are blocked on the O1 value → cannot be scheduled; M5D-4 / M5D-6 are blocked on D12 / O5 (the O5 disaster-recovery baseline has been adjudicated but not implemented) → likewise cannot be scheduled | §5.1 **O1** / **D12 · O5** | the §5.2-bis table of `plan.md` and the "boundary" paragraph after it |
| 5 | **PM / AM / UM** product-management capability gaps | — | The requirement is pending: there is still no approved complete requirement / acceptance (PM lacks a PRD and acceptance criteria; AM lacks alert lifecycle management; UM lacks a complete account lifecycle, SSO / MFA, etc.) | Not merged into any batch until the requirement and acceptance criteria are approved | the §5.3 table of `plan.md` |
| 6 | **O1** externally committed value | **Internal engineering target = ≥ CPS 1280 with no failures under the loopback model** (internal only; must not be written into any external material) | **The externally committed value is still left unfilled**; the four downstream items — HPA thresholds / capacity-class alerts / the capacity value in ne-datasheet / the formal 4.1 report — all stay blocked | Missing a business adjudication-path measurement / a saturation-point observation / a multi-replica target environment (none of the three value-filling admission conditions in `ne-datasheet.md` §3 is satisfied) | the blocked-items paragraph of `plan.md` §5.1 and the added-correction paragraph of 2026-10-11; the 2026-10-12 "B1 / O1 value settled at one level" row in the §0 decision record of `plan.md`; `handoff/2026-10-12-m8-scope-revision-internal-release-plan.md` §0.6 and §5 row 8 |
| 7 | The 14 per-item header parity checks of **REQ-F-1** | — | The automated subset is covered but **the full text is still open**; not a single `- [ ]` in the REQ-F-1 section of `test-plan.md` **has been ticked** | The case implementation itself awaits the A4 e2e batch (to be started after Wave 1 lands); it is a v1.1 scheduling item | the "REQ-F-1 checkbox" row of `acceptance/2026-10-11-wave2-replay-register.md`; the 2026-10-11 P5 row in the §0 decision record of `plan.md` |
| 8 | **A3 Phase D** real-stack case implementation for S5–S11 + **S8** baseline re-capture | The schedule is finalized: **P1 S5 → P2 S7a → P3 S6 → P4 S10 → P5 S9 → P6 S11** | **The case-implementation batch has not landed**; starting it in batches requires maintainer authorization; **S8 is registered as a blocked item** — the baseline lacks the Route / Record-Route headers, so it is not scheduled until the M2 probe re-captures them; REQ-F-5 is not signed pass per the N4 stop line | S8 needs an M2 probe re-capture; the rest need authorization to start in batches | `handoff/2026-10-12-m8-scope-revision-internal-release-plan.md` §0.5; `handoff/2026-10-09-sip-native-testing-plan.md` §4-D; the 2026-10-12 "A3 Phase D schedule finalized" row in the §0 decision record of `plan.md` |
| 9 | **NF-15** HPA thresholds | Adjudicated: **fill `values-onprem.example.yaml`, keep the default `values.yaml` null** (noting "measured on kind, not an external commitment, must be re-measured in the target environment before go-live") | Missing a **measurement batch with per-pod CPU / memory utilization**; the 2026-10-12 saturation-point probe recorded no resource data and does not constitute that batch; the matrix NF-15 row stays `open` | The four G5 downstream items (HPA thresholds / capacity alerts / ne-datasheet / the 4.1 report) stay blocked | `handoff/2026-10-12-m8-scope-revision-internal-release-plan.md` §0.6 item 1 and §6 item 4; `handoff/2026-10-12-m8-batch5-complete-handoff.md` §6 item 5 |
| 10 | **REQ-F-15** full AS stack / **REQ-S-4** formally all-green / **PostgreSQL 16** | — | The three supplementary tests are still open (REQ-F-15 is not the testbed notify / health one; REQ-S-4 is separated from M4 engineering closure; PG 16 is a non-blocking follow-up with an evidence baseline of 12.22) | Related to the supplementary-test framing of §4.4.3 / after M7 integration; C5 has already registered REQ-F-13 / F-15 / S-4 / PG 16 together as "adjudicated not to do" (see §6) | the §5.4 supplementary-test table of `plan.md` (the REQ-F-15 row, the REQ-S-4 row, the PostgreSQL 16 row) |

### 4.3 The four start conditions of B2 / B3 (retained verbatim from §4 of `handoff/2026-10-12-b2-b3-deferred-items.md`)

- [ ] Maintainer authorization to start the requirement drafting
- [ ] The **B3 RPO / RTO figures** have a value (otherwise the requirement has nowhere to put the acceptance criteria)
- [ ] Confirm the relationship between B2's PG deployment form and ADR-0026 (amendment or a new ADR)
- [ ] Confirm whether B2 / B3 are to be **merged** into a single "state and persistence" requirement + ADR, or kept separate

### 4.4 M5D-1 … M5D-6 (`plan.md` §5.2-bis)

| Row | Aggregated defer items | Content | Blocking source | Status |
|---|---|---|---|---|
| **M5D-1** | C-1, C-2, C-3, C-9 | Alert rules and metric thresholds / call sites: 6 dead alert rules (4 metrics that do not exist + 2 with zero call sites), a `clamp_min` arithmetic error, a telemetry threshold `> 0` whose semantics do not match, metrics with zero production call sites | §5.1 **O1** (thresholds must be measured in M6) ＋ §5.3 PM/AM ＋ M7 E1 | **Moved out of v1** |
| **M5D-2** | C-6, T-1 | Scale-down guard parameter control (currently read in and only logged, not used in the decision) ＋ behaviour tests for the feature switch in both on / off states | ADR-0020 / M7 actuation undecided; the ADR-0020 default state / canary strategy undecided | **Moved out of v1** |
| **M5D-3** | C-7 | OTLP export (currently a NoOp sink that drops on enqueue) | §5.3 PM (OTel traces / logs not landed) | **Moved out of v1** |
| **M5D-4** | H-8 | NetworkPolicy has no Egress and its source labels are too broad | §5.1 **D12 / O5** (HA topology and customer SLA) | **Moved out of v1** |
| **M5D-5** | H-11 | No resources (BestEffort), no startupProbe for AS, the semantics of the config-service tcpSocket probe | §5.1 **O1** / M6 (sizing is downstream of measurement) | **Moved out of v1** |
| **M5D-6** | A-2 | The cross-site switchover drill has not been done (ADR-0008 assigns it to M5) | §5.1 **O5** (the disaster-recovery level is a customer SLA) | **Moved out of v1** |

**Inclusion note (§8-14)**: the formal migration of Lane B4 (Python 3.10 EOL / D1) has **no number and no carrier** — the 3.12 validation spike has been **fully rolled back** (all 7 `requires-python` pins + `uv.lock` restored, `git diff` → 0 changes, rebuilt back to cpython-310), while the formal migration has still not been done and requires requirement → ADR → review. This gap has the same root as **D1** (Python 3.10 EOL); this table does not add a separate row for it and tracks it together with D1 (the "spike measurement conclusion (2026-10-12)" and "the formal migration has still not been done" entries of Lane B4 in [`handoff/2026-10-10-unfinished-assessment-and-next-plan.md`](handoff/2026-10-10-unfinished-assessment-and-next-plan.md); the D1 row in `plan.md` §5.2).

---

## 5. Documentation and repository hygiene class (no external dependencies; can be closed out together when v1.1 is scheduled)

| # | Item | Current state | Suggested attribution | Source pointer |
|---|---|---|---|---|
| 1 | Five stale downstream statements — the `0.0.0-skeleton` and "O1 is unadjudicated" wording in `docs/delivery/airgap-package.md`, `docs/delivery/install-guide.md`, `docs/operations/rollback-playbook.md`, `docs/product/ne-datasheet.md`, and `docs/product/version-lifecycle.md` | Stale at the level of fact (the chart has been synced to `0.2.0` for the first time and the O1 internal engineering target value has been set), but the original text is retained per the history-preservation convention and has not been edited back in every place | The packaging-document owners should handle it in the next documentation sync batch following "**retain the original text + append an annotation**"; **awaiting a maintainer decision, not edited in this round** | the §5 table of `handoff/2026-10-12-remaining-items-execution.md` and its "recommended disposition (maintainer decision pending, out of scope for this round)" paragraph |
| 2 | Registration of the config-service integration test failure under PG 15.18 (`AmbiguousFunction`, a PG 14+ type change) | Honest `FAIL-` evidence has been recorded and **no product code was changed**; the standard environment is PG 12.22 so it is not blocking for now, but PG 12 has reached EOL and this is the same class as **D1** | **Whether to initiate a fix is pending a maintainer decision** | the ② item of the "four executions after authorization" row of 2026-10-12 in the §0 decision record of `plan.md`; lines 425–427 and line 999 of `handoff/2026-10-10-unfinished-assessment-and-next-plan.md` |
| 3 | Draft of the final wording for the M8 rows in `plan.md` §0 / §4 | The draft is in `docs/acceptance/m8-plan-m8-row-draft-2026-10-12.md`, is **not merged into `plan.md`**, and has no merge owner | To be merged after the maintainer confirms the wording (E-3 of batch 6 did not perform that merge) | `handoff/2026-10-12-m8-batch6-complete-handoff.md` §5 item 1 |
| 4 | Whether to introduce the `defer` status word | The batch 4 draft (7 pass / 10 defer) introduces `defer` as a **new** status word, which may only be used after maintainer confirmation (D4-03); on 2026-10-13 the proxy signature that finalized batch 4's terminal states has already applied that word to the terminal counts pass 27 / defer 4 / blocked 9 / n-a 9, noting "defer is a newly added status word in this round" | Whether to keep using it long-term **is pending maintainer confirmation** | the last sentence of §2 of `handoff/2026-10-12-m8-batch4-complete-handoff.md`, §5 item 3, and the "terminal counts" row of §7 |
| 5 | The NF-15 matrix row stays `open` | Batch 5 explicitly wrote "this batch does not touch it"; whether it is finalized in batch 4 is that batch's decision, and the handoff target did not endorse it | To be adjudicated together with the measurement batch in §4-9 | `handoff/2026-10-12-m8-batch5-complete-handoff.md` §6 item 5 and the "batch 5 judged pass" paragraph of §8 |
| 6 | Uncommitted working-tree changes and files with no owner (`.dockerignore`, `docs/intro.md`, the 4 uncommitted changed files recorded in §2.3 of batch 1, the per-batch prompt files, etc.; the tracking status is whatever the site shows) | **`git status` at the time is authoritative; this document does not freeze the list item by item** (the list changes with commit activity, and freezing it guarantees staleness); how commits are split is the maintainer's decision (`AGENT.md` §10.4) | Maintainer: commit splitting and tagging | `handoff/2026-10-12-m8-batch1-complete-handoff.md` §2.3; `handoff/2026-10-12-m8-batch3-complete-handoff.md` §6 item 3; `handoff/2026-10-12-m8-batch4-complete-handoff.md` §5 item 8; `handoff/2026-10-12-m8-batch5-complete-handoff.md` §6 item 3; `handoff/2026-10-12-m8-batch6-complete-handoff.md` §5 item 7 |
| 7 | Inconsistent counting framing in `docs/acceptance/report.md` §0.5 | The original §0.5 text (2026-10-06) reads open 24 / blocked 12 / pass 9 / n-a 4, which is inconsistent with the matrix terminal states pass 27 / defer 4 / blocked 9 / n-a 9; the added §0.10 "count sync and internal-release wrap-up declaration" already exists, and the §0.5 original text is retained as a historical value | Do not edit §0.5 back; readers should follow §0.10 | `acceptance/report.md` §0.5, §0.10 |
| 8 | **Terminal state of the performance-layer gate** (M8 batch 5 **B5-04**) | The one-of-two choice is **still undecided**: ① implement a `make gate` blocking layer; ② have the M8 final review accept the risk in writing. Path C on 2026-10-13 has already accepted the **external hard-dependency risk** in writing but **has not recorded a separate adjudication for this layer**, so this item cannot be treated as covered by path C | Awaiting separate maintainer confirmation; once confirmed, schedule it separately per the §9 start-up preconditions | [`handoff/2026-10-12-m8-batch5-complete-handoff.md`](handoff/2026-10-12-m8-batch5-complete-handoff.md) §6 items 1–2 |
| 9 | **config-service's single PG connection does not reconnect automatically after a restart** (M8 batch 3 **B3-04**; `500` → recovers after restart) | Whether to initiate a project is **undecided**; review record B3-04 is still marked "pending maintainer confirmation / pending adjudication" | The maintainer adjudicates line by line among the §7-class actions | [`handoff/2026-10-12-m8-batch3-complete-handoff.md`](handoff/2026-10-12-m8-batch3-complete-handoff.md) §6 items 2 and 4 |
| 10 | **OR → AND semantics for `authorize_peer` address / certificate allowlisting** (M8 batch 4 **D4-02**) | Currently **a matching address is allowed through without requiring the peer certificate**; whether to tighten it to AND is **undecided** (it is a security stance, and the agent must not adjudicate it) | Awaiting maintainer adjudication | [`handoff/2026-10-12-m8-batch4-complete-handoff.md`](handoff/2026-10-12-m8-batch4-complete-handoff.md) §5 item 2 |
| 11 | **Gap in the root `README.md` environment-variable table** | Currently **0/16** coverage; non-blocking, already registered in §0.7 of `docs/acceptance/report.md` | Handle together with the next documentation sync batch | [`handoff/2026-10-12-m8-batch6-complete-handoff.md`](handoff/2026-10-12-m8-batch6-complete-handoff.md) §5 item 5 |

---

## 6. Adjudicated not to do (record retained, ≠ closed)

The registry table is copied verbatim from §12.1 of [`handoff/2026-10-10-unfinished-assessment-and-next-plan.md`](handoff/2026-10-10-unfinished-assessment-and-next-plan.md):

| Item | Registry conclusion | Impact of not doing it (**stated only once**) |
|---|---|---|
| **C1** external portion | **Not to do** | The parts of E1 / E4 / E5 that need a carrier PKI or the customer's K8s stay open long-term (the local real-stack parts were completed with A2 / A3) |
| **C2** D-1 carrier PKI + external-network S-SBC | **Not to do** | REQ-S-2 / REQ-S-3 stay open long-term |
| **C3** D-2 customer K8s REQ-NF-1 live | **Not to do** | REQ-NF-1 live (kill / restart / BYE) stays open long-term |
| **C4** Packaging 2.4 traffic diversion / 2.5 backup-restore drill | **Not to do** | The drill records for the two items above are missing |
| **C5** REQ-F-13 / F-15 / S-4 / PostgreSQL 16 | **Not to do** | The four supplementary tests stay open long-term |
| **W3** | **Registered as not-to-do together with the C column** | Same as above |

- **"Not to do ≠ closed"** — these REQ are **still open** in `docs/acceptance/report.md`, and the open / blocked counts **do not change because of this section** (§12.2 item 2).
- If external evidence collection is restarted in future, re-schedule it **at that time** and **append** the restart record to **this section** rather than rewriting it (§12.2 item 4).
- Every later review cites only the pointer and does not restate item by item (§12.2 item 1).

---

## 7. Awaiting the maintainer's own signature / value (the agent must not sign on their behalf nor adjudicate)

| # | Item | Current status | Why the agent cannot complete it | Source pointer |
|---|---|---|---|---|
| 1 | **The maintainer's own signature in the M8 exit signature block** | The signature block = **signed on the maintainer's behalf by the agent (authorized by the maintainer on 2026-10-13)**, **not the maintainer's own signature**; the pre-authorization historical discipline "the agent must not sign this block on the maintainer's behalf" is retained as the pre-authorization original text | A proxy signature ≠ an own signature; the only possible source of validity for this block is the maintainer personally | `reviews/m8-external-dependency-risk-acceptance-2026-10-13.md` §4 signature block and the two entries filled in on 2026-10-13 after the table; item 1 of §0.11 of `acceptance/report.md` |
| 2 | **M1 exit signature** | The "maintainer signature" field = **to be filled in** (the reviewer field is the AI agent, 2026-09-28) | The signature field can only be filled in by the maintainer | the confirmation-signature table of § of `reviews/m1-exit-review.md`; the "M1 completion date" row of `plan.md` §0 |
| 3 | **M6 milestone sign-off** | **Still open** (M2 / M6 / M7 are "engineering complete", ≠ milestone sign-off) | Milestone sign-off is a maintainer action; "engineering complete" ≠ "milestone sign-off" ≠ "all REQ green" | the current-status row of `plan.md` §0 ("the maintainer's M6 milestone sign-off is still open") and the boundary paragraph of the 2026-10-12 N2 proxy-signature row |
| 4 | **The B3 RPO / RTO value** | **Still undecided** (the O5 / D3 topology values have been decided; the RPO / RTO figures are deliberately left blank) | It is an **external availability commitment** and requires a maintainer value; the agent must not adjudicate it | `handoff/2026-10-12-b2-b3-deferred-items.md` §2.1 item 1 and §5 item 3; the G7 row in the §0 decision record of `plan.md` |
| 5 | **The externally committed O1 value** | **Left unfilled** (the internal engineering target = CPS 1280 with no failures under the loopback model, internal only) | External capacity / SLA figures require maintainer adjudication; none of the three value-filling admission conditions in `ne-datasheet.md` §3 is satisfied | the blocked-items paragraph of `plan.md` §5.1; the 2026-10-12 "B1 / O1 value settled at one level" row in the §0 decision record of `plan.md` |
| 6 | **Authorization for the A4-4 gate configuration change** (whether e2e is brought back into `make test`, whether kind e2e enters PR required) | The adjudication states explicitly: **this is a configuration-change authorization; the A4-4 adjudication explicitly does not authorize it this time; changing it requires separate maintainer approval** | A configuration-change authorization can only be given by the maintainer; A4-4 only established the policy direction | row 2 of the §13.1 table of `handoff/2026-10-10-unfinished-assessment-and-next-plan.md`; the G2 / A4-4 row in the §0 decision record of `plan.md` |

---

## 8. Zero-orphan cross-check table

This table checks item by item the cases of "declared closed but the item has no owner"; **every item must have a landing point in this document**, leaving no unowned leftover.

| # | Phenomenon (source) | Landing point here |
|---|---|---|
| 1 | The "Maintainer's own signature — to be filled in" signature block in §4 of `reviews/m8-external-dependency-risk-acceptance-2026-10-13.md` | §7-1 |
| 2 | §0.11 of `docs/acceptance/report.md` / the separation of the M8 exit signature from the own signature | §7-1 |
| 3 | The §7.5 list of `handoff/2026-10-11-open-adjudication-register.md` omits P4 (listing only 7 items), which §6.1 adds back per the actual record | §5-7 (inconsistent registry framing; the original text is not edited back) |
| 4 | The G9-a / G10 / G11 statuses in the §5 summary table of the same document were not corrected, relying on §6.1 to cover them | §5-7 |
| 5 | Lane B6 of `handoff/2026-10-10-unfinished-assessment-and-next-plan.md` says "accept 16 / needs modification 0 / rejected 0" but the same sentence lists 6 unclosed items (chart `--apply`, `kubeVersion`, RPO / RTO, O1, X1, a real cluster) | §4 (the chart sync has been executed and `kubeVersion` has been written; RPO / RTO → §4-2; O1 → §4-6) and §2 (X1, a real cluster) |
| 6 | The same §12 C1–C5 and W3, "adjudicated not to do ≠ closed", and the absence of a restart carrier | §6 |
| 7 | M8 batch 1 completed but 4 documents have uncommitted changes with no owner | §5-6 |
| 8 | M8 batch 3: `.dockerignore`, `docs/intro.md` (untracked, origin unknown), and `batch5-prompt.md` repeatedly recorded as unowned leftovers | §5-6 |
| 9 | M8 batch 4: the `defer` status word in the 7 pass / 10 defer draft is unapproved, leaving 10 rows dangling | §5-4 |
| 10 | M8 batch 5: the NF-15 matrix row stays `open`; this batch explicitly does not take it and the handoff target did not endorse it | §5-5 / §4-9 |
| 11 | M8 batch 6: the draft wording for the M8 rows in `plan.md` §0 / §4 is not merged | §5-3 |
| 12 | §5 of `handoff/2026-10-12-remaining-items-execution.md`: five stale documents, and the recommended disposition has neither a carrier nor a schedule | §5-1 |
| 13 | After "moved out of v1" for M5D-1…M5D-6 in `plan.md` §5.2-bis there is no landing point | §4-4 |
| 14 | Lane B4 of `handoff/2026-10-10-unfinished-assessment-and-next-plan.md`: the Python 3.12 spike has been rolled back, and the formal migration has no number and no carrier | §4 (folded into the D1 row explanation, see the last paragraph of §4.4) |
| 15 | §4 of `handoff/2026-10-12-remaining-items-execution.md`: "F-12 / F-14 caller ID / regex still n-a, v1.1" has no registry carrier | §3-6 |
| 16 | `docs/reviews/product-packaging-plan-review-2026-10-09.md`: it claims all 24 gaps are closed, yet the remarks column still holds rows marked "pending O1 adjudication" and "pending O4/D5 adjudication" (G-P0-3, G-P0-8, G-P1-3 and G-P1-5, G-P1-8) | §4-6 (O1) / §4-1 (O4 / D5) |
| 17 | §0.8 of `handoff/2026-10-12-m8-scope-revision-internal-release-plan.md`: the counts in §0.5 of `report.md` are not synced | §5-7 |
| 18 | Items 1–2 of §6 of M8 batch 5 (performance-layer gate terminal state B5-04) previously had no landing point in this document | §5-8 |
| 19 | Items 2 and 4 of §6 of M8 batch 3 (B3-04 config-service PG reconnection) previously had no landing point in this document | §5-9 |
| 20 | Item 2 of §5 of M8 batch 4 (D4-02 `authorize_peer` OR / AND semantics) previously had no landing point in this document | §5-10 |
| 21 | Item 1 of §5 of M8 batch 4 (D4-01 whitelist-change approval) previously had no landing point in this document | §3-10 |
| 22 | Item 5 of §5 of M8 batch 6 (the gap in the root `README.md` environment-variable table) previously had no landing point in this document | §5-11 |

---

## 9. Start-up preconditions and stop lines

- **Start-up flow**: `requirement → ADR → HLD/LLD → contract → code+tests → acceptance items + review record` (`AGENT.md` §3); **each item requires explicit maintainer authorization before it starts**.
- **Stop lines**: items for which the external resource has not been obtained or the maintainer has not adjudicated **must not be started**; they **must not be advanced incidentally as part of local work** (following the framing after the §1.1 table in [`handoff/2026-10-12-m8-scope-revision-internal-release-plan.md`](handoff/2026-10-12-m8-scope-revision-internal-release-plan.md)).
- **Deferred ≠ cancelled**; the restart condition is uniformly "**a separate maintainer adjudication + the external resource being in place**".
- **This document is the carrier**: on restart, **append** a record to the corresponding row here and **do not rewrite existing rows** (identical framing to §6 and to §5 of `handoff/2026-10-12-b2-b3-deferred-items.md`).

---

## 10. Boundaries (no over-conclusions may be drawn from this document)

1. This document signs off no REQ / milestone, changes no matrix status word, and changes no count in `docs/acceptance/report.md`.
2. This document **is not a release version definition**; the root `VERSION` is still `0.2.0`, not bumped and not tagged; tags are executed only by the maintainer (`AGENT.md` §10.4).
3. Folding an item into this document **does not mean it is scheduled**, let alone started or implemented.
4. For the external hard dependencies in §2: **accepting the risk ≠ passing verification**; **restarting ≠ starting automatically**.
5. "Value adjudicated" in §4 **does not mean implemented** — O4 / D5 / O5 / D3 are all "value adjudicated, implementation not landed".
6. The internal engineering target (CPS 1280 with no failures under the loopback model) is **internal only** and must not be written into any external material; this document produces no external capacity / SLA figures.
7. **At the REQ level, M5 is still not passing**; the M8 signature covers milestone exit and does not cover REQ-level acceptance.
8. This document performs no git write operation (no add / commit / tag / push / branch creation / remote change).
9. If this document is overturned by later evidence or a maintainer adjudication, **an appended row must explain it** (date + the overturned item + the basis); silent replacement is not allowed.
10. Item 8 of §5 (the terminal state of the performance-layer gate) **must not be treated as covered by path C of 2026-10-13** — path C accepted the external hard-dependency risk, which is a different thing from this layer's one-of-two choice.

---

Written to disk: 2026-10-13. Status: registered, not scheduled, not started, not implemented.
