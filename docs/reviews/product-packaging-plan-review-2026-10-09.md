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

# Review Record for `docs/product-packaging-plan.md`

> Review target: `/home/shudong/project/3rdparty-as/docs/product-packaging-plan.md`
> Review date: 2026-10-09
> Reviewer: AI agent (the primary agent dispatched an Explore subagent to complete the document review; this writing subagent wrote it to disk)
> Review scope: the full text of the product packaging plan (§0 current-state inventory, §1 four batches of deliverables, §2 document structure, §3 execution order, §4 confirmed decisions)
> Review conclusion: the plan requires substantial revision before it can serve as the baseline for the internal go-live review

## Current Status

- **The maintainer completed adjudication of all 24 gaps (8 P0 / 10 P1 / 6 P2) on 2026-10-09; `docs/product-packaging-plan.md` has been revised per the adjudications (2026-10-09).**
- Adjudication result: **22 "accepted", 2 "partially accepted"** (G-P0-6, G-P2-6).
- **The independent re-check is complete**: the independent re-check agent verified item by item against the full text of the revised `docs/product-packaging-plan.md`, the fix plans of all 24 gaps have all landed correctly, and the Adjudication table written back is consistent with the adjudications.
- **All 24 gaps have been verified as closed (8 P0 + 10 P1 + 6 P2), all P0 closed**; the plan can serve as the baseline for the internal go-live review.
- Current milestone: the M7.1 engineering gate was closed (2026-10-07), the M8 release candidate artifacts are ready but the exit sign-off is still shelved (`docs/plan.md` §0).
- All leftover actions have been closed (2026-10-09):
  - **G-P0-6 target scenario, G-P2-6 product naming and repo rename**: a new "product decision record" subsection has been added to §0 of `docs/plan.md`, containing 2 decision rows (target scenario, provisional documentation name for the product), sourced from the maintainer's 2026-10-09 confirmation; the git repo name has been changed to `inhouse-ims-as` (only the git repo name and remote URL), while the chart name, image name and OTel service name remain `3rdparty-as`; the linkage surface is extremely small and no new ADR is needed.
  - **G-P1-9 (§3.5 version lifecycle / EOL)**: REQ-NF-16 (`docs/requirements/prd.md` L459-470) and ADR-0027 (`docs/architecture/adr/0027-version-lifecycle-and-eol.md`) have been added and registered in the ADR registry.
  - The **class-B deliverables** (NE Datasheet capacity values, PDPO retention period, performance benchmark report, real-cluster drill) are still shelved by the M8 exit sign-off and blocked by the unadjudicated O1/O4/D5.

---

## Review Target and Scope

| Item | Content |
|---|---|
| Target file | `docs/product-packaging-plan.md` |
| Baseline documents | `AGENT.md`, `docs/plan.md`, `docs/acceptance/test-plan.md`, `docs/acceptance/report.md`, the ADR registry and ADR-0013/0014/0017/0018/0019 etc. |
| Review scope | The full text §0–§4, focusing on consistency with the current milestone, the undecided items, the non-goals and the ADRs |

---

## Executive summary

`docs/product-packaging-plan.md` attempts to organize the existing outputs and gaps of the engineering milestones into a productization packaging roadmap oriented at the internal go-live review, but the current version deviates significantly from the actual project status:

1. **Over-claiming completed items**: Console, the capacity harness, the layered test system, Health/Draining etc. are marked as "existing", but the corresponding REQ acceptance, real-cluster validation or e2e coverage has not passed.
2. **Violating hard rules**: at §0.1 #9, §1.3, §1.4 #4.1 etc., the dev-host harness or the undecided O1 is written as a capacity/performance figure that may be published externally, violating `AGENT.md` §2 "no capacity figures may be published before the M6 measurement".
3. **Beyond the project scope**: §2.1/§2.2 contain a Diameter Sh interface panel and alert, conflicting with `AGENT.md` §2 "no Diameter Sh" and ADR-0017.
4. **Technical factual error**: §2.4 "iFC canary + one-click rollback" wrongly places the iFC trigger responsibility on the AS side; iFC actually resides in S-CSCF/HSS, and the AS only implements the business logic after the ISC trigger.
5. **Insufficient decision basis**: many "confirmed decisions" in §4 remain only at the level of discussion records and have not formed a formal decision landing point in `docs/plan.md`, an ADR or a review record.
6. **Unrealistic schedule**: §3 gives a total schedule of 3–4 weeks, without considering the shelved M8 sign-off, the undecided items O1/O4/D5 and the acceptance matrix with 12 blocked / 24 open.

In summary, this plan requires substantial revision before it can serve as the baseline for the internal go-live review.

---

## 1. Item-by-Item Assessment of the Existing Assets in §0.1

| # | Asset | What the Plan Claims | Accuracy | Evidence and Notes |
|---|---|---|---|---|
| 1 | Product version number | ✅ Existing | Accurate | The `VERSION` file + the `tests/test_version_consistency.py` guard; ADR-0018 accepted. |
| 2 | Helm Chart | ✅ Existing | Basically accurate | `deploy/helm/` exists and `make chart-check` passes; but config-service 7.2d and real-cluster HTTPS are still not accepted (`docs/plan.md` §5.4). |
| 3 | Prometheus metrics + alert skeleton | ✅ Existing | Basically accurate | `deploy/alerts/as-alerts.yaml` exists; but the alert-to-action cross-reference table, the OTLP exporter wiring and the capacity-class alerts are still deferred (`report.md` §0.4). |
| 4 | Health / Readiness / Draining | ✅ Existing | Partly accurate | The mechanism and the unit tests have been delivered (`platform/tests/test_health_server.py`, ADR-0009); but real-cluster ISSU / downscale-without-call-drop has not been fully accepted; the M5 engineering gate closing ≠ REQ acceptance. |
| 5 | Layered test system | ✅ Existing | Inaccurate | The `e2e` marker is 0 (`test-plan.md` L19); the performance layer is only an accept-all harness, not a business adjudication path. |
| 6 | Architecture docs + ADR system | ✅ Existing | Accurate | `docs/architecture/adr/README.md` registers 26 ADRs; some are still drafts (ADR-0023/0025). |
| 7 | Console | ✅ Existing | Inaccurate | M4b only completed an engineering slice (callee + prefix, approval flow, fleet distribution start); REQ-S-4, F-13, F-15 real AS, 7.2d ingress etc. are still open (`plan.md` §4.3, §5.4). |
| 8 | Some Runbooks | ✅ Existing (scattered) | Partly accurate | The runbooks are actually concentrated in `docs/acceptance/` (`m5-downscale-runbook.md`, `m5-state-stores-runbook.md`, `m4b-8-runbook.md` etc.), and are not as scattered as "scattered across each milestone's deliverables" suggests. |
| 9 | Capacity measurement harness | ✅ Existing | Inaccurate | M6 only completed the dev-host O1 official batch (`m6-o1-measurement-report-2026-10-05.md`), explicitly marked "not an external O1/SLA"; `AGENT.md` §2 prohibits publishing capacity figures before the M6 measurement. |
| 10 | Pluggable business engine architecture | ✅ Existing | Accurate | `apps/translation/` and `apps/anti-fraud/` are independent processes, conforming to ADR-0002. |

---

## 2. Item-by-Item Assessment of the Main Gaps in §0.2

| # | Gap Item | Plan Status | Assessment | Key Issue |
|---|---|---|---|---|
| 1 | 3GPP conformance matrix | ❌ Missing | Reasonable | No dispute, but Sh/CDR must be marked N/A (out of scope). |
| 2 | Network element datasheet (NE Datasheet) | ❌ Missing | Needs revision | It does not note that capacity figures are blocked by O1; CAPS/BHCA/concurrency values must not be written before O1 is adjudicated. |
| 3 | Fault demarcation handbook | ❌ Missing | Reasonable | No dispute. |
| 4 | One-pager product positioning + large architecture diagram | ❌ Missing | Reasonable | No dispute. |
| 5 | Grafana dashboard templates | ❌ Missing | Basically reasonable | But the dashboard content must not include a Diameter Sh panel. |
| 6 | Preflight environment validation script | ❌ Missing | Reasonable | No dispute. |
| 7 | Offline installation package | ❌ Missing | Needs revision | The scope should be limited to image sync + helm package scripts, rather than a general offline installer; ADR-0017 explicitly states that Helm is the only production form. |
| 8 | Responsibility boundary matrix (RACI) | ❌ Missing | Reasonable | No dispute. |
| 9 | SLA / version lifecycle / EOL policy | ❌ Missing | Needs revision | ADR-0018 only covers the semantics of release/component version numbers; lifecycle/EOL is a new decision and requires a new requirement + ADR. |
| 10 | Security compliance evidence (PDPO etc.) | ❌ Missing | Needs revision | It does not mention that O4 (call trace retention period) and D5 (trace storage selection) are still undecided, so retention days must not be made up. |
| 11 | Multi-service platform capability-opening / plugin mechanism document | ❌ Missing | Reasonable | It is suggested to mark it as v1.1 or on demand, to avoid scope expansion in the current milestone. |

---

## 3. Batch Review (§1)

### Batch 1: Review entry tickets

- **1.1 Product one-pager + naming**: the target scenario "internal go-live review" remains only at the discussion level and has not been landed as a formal decision in `docs/plan.md` or an ADR (see G-P0-6).
- **1.2 3GPP conformance matrix**: marking Sh/CDR as N/A is correct, but it must simultaneously make clear that E1/E4/E5 are still not accepted (`plan.md` §5.1 O2/O3).
- **1.3 Network element datasheet (NE Datasheet)**: the O1 adjudication must be awaited before writing the capacity model; currently writing CAPS/BHCA/concurrent sessions violates `AGENT.md` §2 (see G-P0-3).
- **1.4 Fault demarcation handbook**: reasonable, but it must be aligned with the RACI, the packet-capture responsible party and the S-CSCF/HSS side logs.
- **1.5 README rewrite**: reasonable, but the product name and target scenario decisions must be clarified first.

### Batch 2: Operability

- **2.1 Grafana dashboard templates**: including the "Diameter Sh interface" panel is out of scope (see G-P0-4).
- **2.2 Alert rule reinforcement**: the "Sh timeout" alert is likewise out of scope; it must be removed or changed to an explicit N/A.
- **2.3 L1/L2 Runbook**: reasonable; but it should collate the existing `docs/acceptance/*-runbook.md` rather than create new ones from scratch.
- **2.4 iFC canary + one-click rollback**: the iFC trigger belongs to S-CSCF/HSS, and the AS only implements the ISC business logic; this description is misleading (see G-P0-5, G-P1-10).
- **2.5 Backup-restore approach**: reasonable; but it depends on a real-cluster drill, and M8 7.2d is still blocked.

### Batch 3: Delivery form and compliance

- **3.1 Preflight script**: reasonable.
- **3.2 Offline installation package**: the scope should be narrowed to image sync + helm package scripts, conforming to the single-form constraint of ADR-0013 (see G-P1-7).
- **3.3 RACI**: reasonable.
- **3.4 PDPO compliance**: hardcoding retention days is not allowed; it must state that O4 is undecided and D5 is undecided (see G-P1-8).
- **3.5 Version lifecycle / EOL**: ADR-0018 only solves the version number; EOL / support period requires a new ADR / requirement (see G-P1-9).

### Batch 4: Icing on the cake

- **4.1 Performance benchmark report (official version)**: scheduling an official performance report before O1 is adjudicated violates `AGENT.md` §2 (see G-P0-8).
- **4.2 7×24 long-run stability test report**: it is suggested to make it on demand / v1.1; it should not be included by default in the current milestone.
- **4.3 API version compatibility policy**: it may be merged into the version lifecycle document, but it must be made clear that it depends on a new decision on top of ADR-0018.
- **4.4 Whitepaper**: reasonable, lowest priority.
- **4.5 Capability-opening mechanism document**: reasonable, suggested for v1.1 or on demand.

---

## 4. Document Structure Review (§2)

| Proposed Directory | Assessment | Notes |
|---|---|---|
| `docs/product/` | Accept | It does not conflict with the `operations/` planning at L26 of `docs/README.md`; a new directory is reasonable. |
| `docs/operations/` | Accept | Already planned at L26 of `docs/README.md`; but the directory does not exist yet (G-P2-1). |
| `docs/delivery/` | Basically accept | The boundary with `deploy/helm/README.md` needs clarification (G-P2-4). |
| `operations/grafana-dashboards/sh-interface.json` | Needs modification | The file name conflicts with the "no Sh" scope (G-P2-3). |
| `delivery/install-guide.md` | Needs modification | It overlaps in content with `deploy/helm/README.md`; it must be made clear that the former targets the delivery manifest while the latter targets Helm parameters (G-P2-4). |

---

## 5. Execution Order and Schedule Review (§3)

- The total schedule of **3–4 weeks** is unrealistic: the M8 sign-off is still shelved (`plan.md` §0), the undecided items O1/O4/D5 are not adjudicated, and the acceptance matrix with 12 blocked / 24 open has not converged (`report.md` §0.5).
- The iFC canary/rollback in step 4 "operations capability completion" depends on S-CSCF side configuration and a real-cluster drill, and cannot be completed in a fixed number of days (see G-P1-10).
- Step 7 "security compliance" requires O4/D5 to be adjudicated first, otherwise no actionable PDPO statement can be written (see G-P1-8).

Suggestion: first close the M8 exit sign-off and the O1/O4/D5 adjudications, then formulate an actionable packaging schedule.

---

## 6. Consistency Review of Confirmed Decisions (§4)

| Decision | What the Plan Claims | Actual State | Assessment |
|---|---|---|---|
| 4.1 Target scenario: internal go-live review | Confirmed | Only at the discussion level; `docs/plan.md` has no corresponding decision row, no ADR, no review record. | Pending adjudication (G-P0-6) |
| 4.2 Business positioning: multi-service platform | Confirmed | The `apps/` architecture supports it; it is repeatedly mentioned in the discussion. | Acceptable, but it is suggested to add an ADR / plan decision row. |
| 4.3 Naming: In-house IMS Application Server | Confirmed | Only at the naming discussion level; `docs/plan.md` and the ADR have no formal landing point. | Pending adjudication (G-P2-6) |
| 4.4 Pace of progress: full sequential rollout | Confirmed | M8 is still shelved and there is no upstream authorization to advance the packaging milestone; O1/O4/D5 are undecided. | Needs modification (G-P0-7) |

---

## 7. Missing Key Items

This plan does not sufficiently reflect the following items critical to the internal go-live review:

1. **M8 status**: RC artifacts ready but the exit sign-off is shelved (`plan.md` §0, `report.md` §0).
2. **E1/E4/E5 not accepted**: reSIProcate production path behavior, TLS hot rotation and state externalization are still open (`plan.md` §5.1 O2/O3, ADR-0019 §7/§10).
3. **TLS/REQ-S-2/S-3 not accepted**: there is no lab evidence for carrier PKI or certificate rotation (`report.md` §0.6 D-1).
4. **e2e=0**: L19 of `test-plan.md` states explicitly that the e2e marker count is 0; the complete call + console has not landed.
5. **O1 capacity target unadjudicated**: both `AGENT.md` §2 and `plan.md` §5.1 O1 prohibit publishing capacity figures.
6. **O4 call trace retention period / D5 storage selection undecided**: this affects PDPO, security compliance and the backup-restore approach.
7. **REQ-S-4 / the overall M4b acceptance has not passed**: console security audit is still an engineering slice, not a REQ acceptance (`plan.md` §4.3, §5.4).
8. **testbed is not a v1 deliverable**: ADR-0014 explicitly states that v1 does not treat the testbed as a deliverable; the packaging plan should avoid treating the simulator IOT report as product evidence.

---

## Gap Register

### P0 gaps

#### G-P0-1 — Console is over-claimed

- **Location**: §0.1 #7 of `docs/product-packaging-plan.md`
- **Problem**: the Console is marked as "existing", but M4b is only an engineering slice; REQ-S-4, M4b-8, F-13, F-15 real AS, caller-ID/regex v1.1 and 7.2d ingress have all not passed acceptance.
- **Evidence**: §4.3 of `docs/plan.md` explicitly states that the M4 engineering gate closing does not include `test-plan` all-REQ green, F-13, F-15 real AS, caller-ID/regex v1.1, 7.2d ingress; the §5.4 supplementary test list is still open.
- **Suggestion**: change #7 to "partially existing (engineering slice)", and list the not-yet-accepted sub-items in the notes.

#### G-P0-2 — The capacity harness is misdescribed as "capacity measurement"

- **Location**: §0.1 #9 of `docs/product-packaging-plan.md`
- **Problem**: calling the M6 dev-host harness report "capacity measurement" violates `AGENT.md` §2 "no capacity figures may be published before the M6 measurement".
- **Evidence**: `AGENT.md` §2; `docs/plan.md` §5.1 O1 is still open; `m6-o1-measurement-report-2026-10-05.md` is explicitly marked "not an external O1/SLA".
- **Suggestion**: change it to "M6 capacity harness (dev-host internal measurement, not for external publication)".

#### G-P0-3 — The NE Datasheet plan writes capacity figures ahead of time

- **Location**: §1.3 of `docs/product-packaging-plan.md`
- **Problem**: the NE Datasheet is prepared to include figures such as CAPS/BHCA/concurrent sessions, but O1 is still unadjudicated.
- **Evidence**: `AGENT.md` §2; `docs/plan.md` §5.1 O1 (capacity targets: CPS, concurrent sessions and call-setup latency budget; the maintainer target adjudication is still open).
- **Suggestion**: the capacity chapter of the datasheet should be written as "blocked by O1, to be filled in after the M6 measurement and the maintainer's adjudication", with no concrete figures.

#### G-P0-4 — The Grafana panel includes the Diameter Sh interface

- **Location**: §2.1 / §2.2 of `docs/product-packaging-plan.md`
- **Problem**: the Grafana dashboard and alert rules include "Diameter Sh interface / Sh timeout", which is beyond the project scope.
- **Evidence**: `AGENT.md` §2 explicitly states "no Diameter Sh"; `ADR-0017` explicitly states no CDR/billing.
- **Suggestion**: remove the Sh panel and alert; mark Sh as N/A in the compliance matrix.

#### G-P0-5 — The scope of "iFC canary + one-click rollback" is wrong

- **Location**: §2.4 of `docs/product-packaging-plan.md`
- **Problem**: the iFC trigger logic belongs to S-CSCF/HSS and the AS only implements the business logic after the ISC trigger; the plan writes the iFC canary/rollback as an AS-side deliverable, which misleads the review.
- **Evidence**: iFC supports canary triggering by user group / number range / percentage (S-CSCF side, discussion record); the single ISC semantics of §1.1 of the architecture document.
- **Suggestion**: change it to "business canary / traffic-diversion approach after the ISC trigger + the coordination interface with the S-CSCF side's iFC canary", clarifying the AS-side boundary.

#### G-P0-6 — Insufficient decision basis for "target scenario: internal go-live review"

- **Location**: §4.1 of `docs/product-packaging-plan.md`
- **Problem**: this decision is marked "confirmed", but there is no corresponding decision row in `docs/plan.md`, no ADR and no review record.
- **Evidence**: there is relevant discussion in the discussion record; `docs/plan.md` has no decision landing point for it.
- **Suggestion**: the maintainer adjudicates: either add a formal decision row + review record to §1/§4 of `docs/plan.md`, or mark this item as a discussion opinion rather than a confirmed decision.

#### G-P0-7 — "Full sequential rollout" conflicts with the shelved M8

- **Location**: §4.4 of `docs/product-packaging-plan.md`
- **Problem**: it claims the pace of progress is "confirmed", but the M8 exit sign-off is still shelved, and O1/O4/D5 are undecided, so there is a lack of upstream authorization.
- **Evidence**: §0 of `docs/plan.md` "M8 is still shelved"; O1/O4/D5 in §5 are all open.
- **Suggestion**: change it to "the pace of progress is to be reconfirmed after the M8 sign-off and the O1/O4/D5 adjudications", or split it into "batch 1 first, the rest on demand".

#### G-P0-8 — The batch 4 performance benchmark report still violates the capacity-figure prohibition

- **Location**: §1.4 #4.1 of `docs/product-packaging-plan.md`
- **Problem**: batch 4 still plans to "produce an official report based on D10 / the M6 capacity harness"; publishing a performance benchmark report before O1 is adjudicated violates a hard rule.
- **Evidence**: `AGENT.md` §2; `docs/plan.md` §5.1 O1; `ADR-0014` explicitly states that no capacity figures are published before M6.
- **Suggestion**: change it to "after the O1 adjudication, produce an internal-review-version performance report based on the M6 measurement"; at the current stage keep only the test methodology description, with no throughput/concurrency/latency values.

### P1 gaps

#### G-P1-1 — Health/Draining has only mechanism verification, lacking real-cluster evidence

- **Location**: §0.1 #4 of `docs/product-packaging-plan.md`
- **Problem**: ISSU/Draining was only verified on kind with a simulated `active_calls`; real-cluster rolling upgrade / downscale without dropping calls has not been fully accepted.
- **Evidence**: the M5 container image section of `docs/acceptance/report.md`; §4 of `m5-downscale-runbook.md` explicitly uses `AS_M5_SIMULATED_ACTIVE_CALLS`; the M5 engineering gate closing ≠ REQ acceptance.
- **Suggestion**: add "the mechanism has been delivered; call-drop-free behaviour under real SIP load is pending acceptance in M7/M8" to the notes.

#### G-P1-2 — The layered test system is over-claimed

- **Location**: §0.1 #5 of `docs/product-packaging-plan.md`
- **Problem**: e2e=0 and performance is only an accept-all harness; this is not a complete layered test system.
- **Evidence**: L19-20 of `docs/acceptance/test-plan.md`; the automation layering table of `test-plan.md`.
- **Suggestion**: change it to "the three-layer testbed skeleton has been established; e2e has not landed, and performance is only an accept-all harness (not a business path)".

#### G-P1-3 — The NE Datasheet gap does not note the O1 block

- **Location**: §0.2 #2 of `docs/product-packaging-plan.md`
- **Problem**: the gap table does not state that capacity figures cannot be written for now because O1 is undecided.
- **Evidence**: `docs/plan.md` §5.1 O1; `AGENT.md` §2.
- **Suggestion**: add "the capacity chapter is blocked by O1" to the impact scope of #2.

#### G-P1-4 — The SLA/EOL gap does not distinguish the scope of ADR-0018

- **Location**: §0.2 #9 of `docs/product-packaging-plan.md`
- **Problem**: the gap table does not state that ADR-0018 only covers version-number semantics, and that lifecycle/EOL is a new decision.
- **Evidence**: the Decision/Consequences of `ADR-0018` explicitly only resolves release/component version numbers and does not touch the support period/EOL.
- **Suggestion**: add "a new requirement + ADR is required, beyond the scope of ADR-0018" to the notes of #9.

#### G-P1-5 — The security/privacy gap omits O4/D5

- **Location**: §0.2 #10 of `docs/product-packaging-plan.md`
- **Problem**: it does not mention that the call trace retention period O4 and the storage selection D5 are still undecided, making an actionable PDPO statement impossible.
- **Evidence**: `docs/plan.md` §5.1 O4, §5.2 D5; `ADR-0017` Decision ④.
- **Suggestion**: change the status of #10 to "blocked by O4/D5", and list it as a prerequisite as critical as PDPO itself.

#### G-P1-6 — The 3GPP matrix does not note E1/E4/E5 and the sippy reference

- **Location**: §1.2 of `docs/product-packaging-plan.md`
- **Problem**: the conformance matrix does not state that production-stack E1/E4/E5 are still open, and that sippy is only a testbed baseline reference.
- **Evidence**: §7/§10 of `ADR-0019`; `docs/plan.md` §5.1 O2/O3.
- **Suggestion**: add an "E1/E4/E5 pending acceptance in M8" note to the matrix, and make clear in the scope description that sippy is only a testbed baseline.

#### G-P1-7 — The air-gapped package scope is too broad

- **Location**: §3.2 of `docs/product-packaging-plan.md`
- **Problem**: the "offline installation package" description leans towards a general offline installer, which may deviate from the Helm-only production form.
- **Evidence**: `ADR-0013`; `AGENT.md` §2 single-tenant on-prem.
- **Suggestion**: make it explicit as "image sync script + `helm package` + dependent image manifest + offline load script", producing no second installation form.

#### G-P1-8 — PDPO does not state that O4 is undecided

- **Location**: §3.4 of `docs/product-packaging-plan.md`
- **Problem**: the PDPO compliance is prepared to include a "retention period", but O4 is unadjudicated and days must not be hardcoded.
- **Evidence**: `docs/plan.md` §5.1 O4; `ADR-0017` Decision ④.
- **Suggestion**: change it to "the retention period is filled in after the O4 adjudication; currently only the retention scope, deletion mechanism and data-residency principle are described".

#### G-P1-9 — Version lifecycle / EOL does not state that a new ADR is required

- **Location**: §3.5 of `docs/product-packaging-plan.md`
- **Problem**: it does not state that this deliverable requires a new requirement + ADR, leaving the document chain incomplete.
- **Evidence**: the document chain requirement of `AGENT.md` §3.1.
- **Suggestion**: add the note "REQ-NF-XX and an ADR must be added first, then HLD/LLD/acceptance".

#### G-P1-10 — iFC canary / backup-restore do not acknowledge the S-CSCF dependency

- **Location**: §2.4 / §2.5 of `docs/product-packaging-plan.md`
- **Problem**: iFC canary and the backup-restore drill depend on S-CSCF side configuration and a real-cluster environment; the plan does not explain this sufficiently.
- **Evidence**: the discussion record (iFC canary depends on the S-CSCF side); M8 7.2d BLOCKED (`plan.md` §5.4).
- **Suggestion**: add a risk note about "depending on S-CSCF side coordination and the M8 real-cluster environment" to the relevant deliverables.

### P2 gaps

#### G-P2-1 — `docs/operations/` has not been created yet

- **Location**: §2 of `docs/product-packaging-plan.md`
- **Problem**: the plan adds `docs/operations/`, but that directory does not exist yet.
- **Evidence**: L26 of `docs/README.md` already plans `operations/`, but the actual directory has not been created.
- **Suggestion**: accept it as a known gap; when creating the directory, migrate/link the existing runbooks into it.

#### G-P2-2 — The description of the actual runbook location is inaccurate

- **Location**: §0.1 #8 of `docs/product-packaging-plan.md`
- **Problem**: "some runbooks are scattered across each milestone's deliverables" does not match reality; the runbooks are already concentrated in `docs/acceptance/`.
- **Evidence**: `docs/acceptance/m5-downscale-runbook.md`, `m5-state-stores-runbook.md`, `m4b-8-runbook.md`, `m8-native-consistency-runbook.md` etc.
- **Suggestion**: change it to "the runbooks are already concentrated in `docs/acceptance/`; the plan migrates/links them to `docs/operations/`".

#### G-P2-3 — The file name `sh-interface.json` conflicts

- **Location**: §2 of `docs/product-packaging-plan.md`
- **Problem**: `operations/grafana-dashboards/sh-interface.json` conflicts with the "no Diameter Sh" scope.
- **Evidence**: `AGENT.md` §2.
- **Suggestion**: delete that file entry or change it to a placeholder note explicitly marked N/A.

#### G-P2-4 — The boundary between `delivery/install-guide.md` and the Helm README is unclear

- **Location**: §2 of `docs/product-packaging-plan.md`
- **Problem**: `delivery/install-guide.md` overlaps in content with the existing `deploy/helm/README.md`, and the responsibility boundary is not explained.
- **Evidence**: `deploy/helm/README.md` already contains detailed installation, values descriptions and rendering guards.
- **Suggestion**: `delivery/install-guide.md` should focus on "delivery manifest + image sync + the helm install command list", while `deploy/helm/README.md` should focus on the Helm chart parameters and behaviour; the two documents should link to each other to avoid duplication.

#### G-P2-5 — The 3–4 week schedule ignores the shelved M8 and the undecided items

- **Location**: §3 of `docs/product-packaging-plan.md`
- **Problem**: the schedule does not consider the shelved M8 sign-off, the undecided O1/O4/D5, or the 12 blocked / 24 open acceptance items.
- **Evidence**: `docs/plan.md` §0, §5; `report.md` §0.5, §0.8.
- **Suggestion**: change it to "first close M8 and O1/O4/D5, then formulate an executable schedule", or give a multi-scenario estimate with blocking conditions.

#### G-P2-6 — Insufficient basis for the product name being "confirmed"

- **Location**: §4.3 of `docs/product-packaging-plan.md`
- **Problem**: the product name is marked "confirmed", but it appears only in the naming discussion, with no ADR / plan decision row.
- **Evidence**: the naming discussion record; `docs/plan.md` has no such decision row.
- **Suggestion**: the maintainer adjudicates: either add a formal decision landing point, or mark it as "suggested name" rather than confirmed.

---

## Adjudication

The quoted literals below are the exact original wording of `docs/product-packaging-plan.md` and are kept verbatim.

| ID | Source | Issue Summary | Adjudication | Fix Plan | Status | Verification Method | Notes |
|---|---|---|---|---|---|---|---|
| G-P0-1 | §0.1 #7 | The Console is marked as "已有", but M4b is only an engineering slice and multiple REQ items such as REQ-S-4/M4b/REQ are not accepted | Accepted | Change #7 to "部分已有（工程切片）" and list the unaccepted sub-items | Verified | Document update + maintainer verification (product-packaging-plan.md 2026-10-09 revised version L21) | |
| G-P0-2 | §0.1 #9 | The M6 dev-host harness is described as "容量实测", violating the rule that no capacity figures be published before M6 | Accepted | Change it to "M6 容量 harness（dev-host 内部测量，非对外发布）" | Verified | Document update + maintainer verification (product-packaging-plan.md 2026-10-09 revised version L23) | |
| G-P0-3 | §1.3 | The NE Datasheet plans to write CAPS/BHCA/concurrency figures, but O1 is unadjudicated | Accepted | Write the capacity chapter as "受 O1 阻塞，待实测后填入" | Verified | Document update + maintainer verification (product-packaging-plan.md 2026-10-09 revised version L69) | Capacity values pending O1 adjudication (class-B deliverable) |
| G-P0-4 | §2.1/§2.2 | The Grafana/alerts contain a Diameter Sh panel and an Sh timeout alert, out of scope | Accepted | Remove the Sh panel and alert; mark Sh as N/A in the compliance matrix | Verified | Document update + maintainer verification (product-packaging-plan.md 2026-10-09 revised version L79-L80) | |
| G-P0-5 | §2.4 | "iFC 灰度 + 一键回退" wrongly puts the S-CSCF/HSS-side iFC responsibility on the AS | Accepted | Change it to "ISC 触发后业务灰度/摘流 + 与 S-CSCF 侧配合" | Verified | Document update + maintainer verification (product-packaging-plan.md 2026-10-09 revised version L82) | |
| G-P0-6 | §4.1 | "目标场景：内部上线评审" is marked confirmed, but has no plan/ADR/review record landing point | **Partially accepted** | The maintainer confirmed direction A (internal go-live review) on 2026-10-09, but that direction currently comes only from the discussion record; §4.1 of the plan document has been downgraded in wording to "当前默认方向（讨论确认，待补 plan/ADR 正式决策落点）" and is no longer written as a confirmed decision | Closed | Document update + plan decision row (docs/plan.md L21-28) | The formal decision landing point has been added: the §0 "product decision record" subsection of docs/plan.md |
| G-P0-7 | §4.4 | "顺序全量推进" is marked confirmed, but the M8 sign-off is shelved and O1/O4/D5 are undecided | Accepted | Change it to "待 M8 签字与 O1/O4/D5 裁决后确认推进节奏" | Verified | Document update + maintainer verification (product-packaging-plan.md 2026-10-09 revised version L220-L223) | The pace of progress has been changed into categories A and B; category B awaits the closure of the prerequisites |
| G-P0-8 | §1.4 #4.1 | The batch 4 official performance benchmark report still violates the capacity-figure prohibition | Accepted | Change it to "O1 裁决后整理内部评审版报告"; no figures at the current stage | Verified | Document update + maintainer verification (product-packaging-plan.md 2026-10-09 revised version L103) | The performance report awaits the O1 adjudication (class-B deliverable) |
| G-P1-1 | §0.1 #4 | Health/Draining has only mechanism + simulation verification and lacks real-cluster ISSU/downscale evidence | Accepted | Add the note "真实 SIP 负载下不掉呼叫待 M7/M8 验收" | Verified | Document update + maintainer verification (product-packaging-plan.md 2026-10-09 revised version L18) | |
| G-P1-2 | §0.1 #5 | The layered test system is over-claimed: e2e=0, performance only an accept-all harness | Accepted | Change it to "骨架已建立；e2e 未落地，performance 非业务路径" | Verified | Document update + maintainer verification (product-packaging-plan.md 2026-10-09 revised version L19) | |
| G-P1-3 | §0.2 #2 | The NE Datasheet gap does not note the O1 block | Accepted | Add "容量章节受 O1 阻塞" to the impact scope of #2 | Verified | Document update + maintainer verification (product-packaging-plan.md 2026-10-09 revised version L31) | Capacity values pending O1 adjudication |
| G-P1-4 | §0.2 #9 | The SLA/EOL gap does not distinguish that ADR-0018 only covers version numbers | Accepted | Add "需新增 requirement + ADR" to the notes of #9 | Verified | Document update + maintainer verification (product-packaging-plan.md 2026-10-09 revised version L38) | Same origin as G-P1-9, a new requirement + ADR is required |
| G-P1-5 | §0.2 #10 | The security/privacy gap omits O4/D5 | Accepted | Change the status of #10 to "受 O4/D5 阻塞" | Verified | Document update + maintainer verification (product-packaging-plan.md 2026-10-09 revised version L39) | Pending O4/D5 adjudication |
| G-P1-6 | §1.2 | The 3GPP matrix does not note that E1/E4/E5 are still open and that sippy is only a testbed baseline | Accepted | Add an E1/E4/E5 pending-acceptance note to the matrix and explain the status of the sippy reference | Verified | Document update + maintainer verification (product-packaging-plan.md 2026-10-09 revised version L68) | |
| G-P1-7 | §3.2 | The air-gapped package scope is too broad and may deviate from Helm-only | Accepted | Make it explicit as "镜像同步 + helm package + 离线加载脚本" | Verified | Document update + maintainer verification (product-packaging-plan.md 2026-10-09 revised version L92) | |
| G-P1-8 | §3.4 | The PDPO compliance does not state that O4 is undecided and retention days must not be hardcoded | Accepted | Write the retention period as "由 O4 裁决后填入" | Verified | Document update + maintainer verification (product-packaging-plan.md 2026-10-09 revised version L94) | Pending O4/D5 adjudication |
| G-P1-9 | §3.5 | Version lifecycle / EOL does not state that a new ADR/requirement is required | Accepted | Add the note "需先补 REQ + ADR" | Closed | Document update + REQ-NF-16 (prd.md L459-470) + ADR-0027 | REQ-NF-16 and ADR-0027 have been added, and the ADR registry has been updated |
| G-P1-10 | §2.4/§2.5 | iFC canary / backup-restore do not acknowledge the S-CSCF and real-cluster dependencies | Accepted | Add the dependency and risk notes | Verified | Document update + maintainer verification (product-packaging-plan.md 2026-10-09 revised version L82-L83) | The real-cluster drill awaits the M8 7.2d unlock, and 2.4 additionally requires S-CSCF/HSS side coordination |
| G-P2-1 | §2 | `docs/operations/` has not been created yet | Accepted | Create the directory and migrate/link the existing runbooks | Verified | Document update + maintainer verification (product-packaging-plan.md 2026-10-09 revised version L124) | §2 now notes that the directory has not been created and that existing runbooks are migrated/linked when it is |
| G-P2-2 | §0.1 #8 | The runbooks are actually concentrated in `docs/acceptance/`; the description is inaccurate | Accepted | Change it to "Runbook 已集中，计划迁到 operations/" | Verified | Document update + maintainer verification (product-packaging-plan.md 2026-10-09 revised version L22) | |
| G-P2-3 | §2 | The file name `sh-interface.json` conflicts with the no-Sh scope | Accepted | Delete it or change it to an N/A placeholder note | Verified | Document update + maintainer verification (product-packaging-plan.md 2026-10-09 revised version L125-L127) | The file entry has been deleted from the directory tree, keeping only the overview/sip-signaling dashboards |
| G-P2-4 | §2 | The boundary between `delivery/install-guide.md` and `deploy/helm/README.md` is unclear | Accepted | Clarify the responsibilities of the two documents and link them to each other | Verified | Document update + maintainer verification (product-packaging-plan.md 2026-10-09 revised version L136-L143) | |
| G-P2-5 | §3 | The 3–4 week schedule ignores the shelved M8 and O1/O4/D5 | Accepted | Change it to "先关闭 M8 与 O1/O4/D5，再定排期" | Verified | Document update + maintainer verification (product-packaging-plan.md 2026-10-09 revised version L148-L189) | It has been changed to categories A and B with blocking conditions and a multi-scenario schedule, without presupposing a total duration |
| G-P2-6 | §4.3 | The product name being "confirmed" rests only on discussion evidence | **Partially accepted** | The maintainer confirmed on 2026-10-09 that the documentation uses the provisional name In-house IMS Application Server and that the git repo name is changed to inhouse-ims-as (the chart/image/service names remain 3rdparty-as); §4.3 of the plan document has been changed to "文档暂用名 / 建议名称（待补正式决策落点）" and no longer states that the product name has been formally approved | Closed | Document update + plan decision row (docs/plan.md L21-28) | The formal naming decision landing point has been added: the §0 "product decision record" subsection of docs/plan.md |

---

## AI Re-check Conclusion (Verification)

- This review record has been re-checked against the full text of `docs/product-packaging-plan.md`, `AGENT.md`, `docs/plan.md`, `docs/acceptance/test-plan.md`, `docs/acceptance/report.md` and ADR-0013/0014/0017/0018/0019.
- All P0/P1/P2 gaps have been given an evidence source, a fix plan and an initial adjudication-table status.
- The maintainer completed all 24 adjudications on 2026-10-09 (22 accepted, G-P0-6 and G-P2-6 partially accepted), and `docs/product-packaging-plan.md` has been revised per the adjudications.
- **The independent re-check agent has verified item by item against the full text of the revised `docs/product-packaging-plan.md`, and the fix plans of all 24 gaps have landed correctly.**
- **§0.3's prerequisites fully cover all missing key items of review record §7.**
- **The Adjudication table written back is consistent with the adjudications.**
- **All 24 gaps have been closed (8 P0 + 10 P1 + 6 P2), all P0 closed, and the plan can serve as the baseline for the internal go-live review.**
- **All leftover actions have been closed**: G-P0-6/G-P2-6 have added formal decision rows to docs/plan.md; G-P1-9 has added REQ-NF-16 + ADR-0027.

---

## Signature

- **Reviewer**: AI agent (Explore + writing subagent)
- **Review date**: 2026-10-09
- **Maintainer adjudication date**: 2026-10-09
- **Independent re-check date**: 2026-10-09
- **Re-check conclusion**: all 24 gaps are closed (8 P0 + 10 P1 + 6 P2), all P0 closed, and the plan can serve as the baseline for the internal go-live review. All leftover actions have been closed (2026-10-09).
