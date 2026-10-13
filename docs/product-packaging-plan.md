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

# In-house IMS Application Server Productization Packaging Plan

> This document is based on the discussion in `docs/discussion.md` about "how to package an in-house third-party IMS AS so that it looks like a commercial product", combined with this project's actual current situation, and sets out an actionable productization packaging roadmap.
>
> Applicable scenario (**current default direction**: confirmed by discussion, with the formal plan/ADR decision landing point still to be added, see §4.1): a carrier's in-house **In-house IMS Application Server** (**a provisional name used in this document**, first occurrence annotated with the 3GPP Third-Party AS role, hereafter in-house AS; naming status see §4.3), targeting xx carrier's internal go-live review. The repo name is proposed to become `inhouse-ims-as` (current default direction, formal decision landing point still to be added, see §4.3).

***

## 0. Current-state inventory and gaps

### 0.1 Assets already in hand

| # | Asset                            | Corresponding note                                          | Status       |
| - | ----------------------------- | --------------------------------------------- | -------- |
| 1 | Product version number (VERSION / semantic versioning)        | ADR-0018 has defined the release version policy                            | ✅ In place     |
| 2 | Helm Chart                    | ADR-0013 confirms Helm-only production deployment and the chart has been delivered; config-service 7.2d and real-cluster HTTPS are still not accepted          | ✅ In place     |
| 3 | Prometheus metrics + an alert skeleton          | The ADR-0005 observability scheme; the alert rules skeleton has been built; the alert-to-action matrix, the OTLP exporter wiring, and capacity-class alerts are still deferred                      | ✅ In place     |
| 4 | Health / Readiness / Draining | ISSU + Draining (ADR-0009) with a complete Pod lifecycle; the mechanism and unit tests have been delivered (including kind + simulated active_calls evidence); not dropping calls during a rolling upgrade / scale-down under real SIP load awaits M7/M8 acceptance | 🟡 Partially in place |
| 5 | Layered test system                        | The ADR-0014 three-layer testbed (unit / contract / integration); the unit/contract/integration skeleton has been established; the e2e marker count is 0 and has not landed; performance is only an accept-all harness, not a business adjudication path | 🟡 Partially in place |
| 6 | Architecture docs + the ADR system                 | HLD/LLD + 26 ADRs under `docs/architecture/`; some ADRs are still drafts (e.g. ADR-0023/0025)     | ✅ In place     |
| 7 | Console                  | Delivered in the M4 milestone, a configuration-management UI (engineering slice); unaccepted sub-items: REQ-S-4, M4b-8 production ingress, F-13 Live Call-ID trace, F-15 real-AS supplementary tests, caller ID / regex v1.1 | 🟡 Partially in place (engineering slice) |
| 8 | Some runbooks                    | The runbooks have been centralized in `docs/acceptance/` (m5-downscale, m5-state-stores, m4b-8, m8-native-consistency, etc.); the plan is to move / link them into `docs/operations/` | 🟡 Partially in place (centralized) |
| 9 | M6 capacity load-test harness (dev-host internal measurement) | dev-host internal measurement, callload tests; **not the external O1/SLA**; the maintainer adjudication on the O1 capacity target is still open; `AGENT.md` §2 forbids publishing capacity figures before a measured adjudication | 🟡 Partially in place |
| 10 | Pluggable business-engine architecture                 | One process per use case in the apps/ directory, naturally supporting the multi-business platform model                  | ✅ In place     |

### 0.2 Main gaps

| #  | Gap item                        | Scope of impact                        | Status   | Batch     |
| -- | -------------------------- | --------------------------- | ---- | ------ |
| 1  | 3GPP specification-conformity matrix               | The first gate of the network department review; without it, professionalism is questioned outright       | ❌ Missing | First batch   |
| 2  | Network-element dossier (NE Datasheet)         | Standard equipment for every legitimate network element in a live network; without it you are treated as a "project" rather than a "product"; the capacity chapter is blocked by O1 and no CAPS/BHCA/concurrency figures may appear before the adjudication    | ❌ Missing | First batch   |
| 3  | Fault demarcation manual                     | The biggest obstacle for an in-house network element is "when something breaks, you are the first suspect"; without a defined procedure you cannot prove your innocence | ❌ Missing | First batch   |
| 4  | One-page product positioning + an architecture overview diagram             | Needed for the review's first impression, for management reporting, and for external introductions        | ❌ Missing | First batch   |
| 5  | Grafana dashboard templates               | Only Prometheus metrics and alerts exist, with no visual dashboards | ❌ Missing | Second batch   |
| 6  | Preflight environment validation script           | One-click environment validation before deployment (K8s version, resources, dependent services)    | ❌ Missing | Third batch   |
| 7  | Offline installation package (air-gapped)          | Carrier machine rooms generally have no external network; without an offline package deployment is blocked        | ❌ Missing | Third batch   |
| 8  | Responsibility boundary matrix (RACI)               | Assigning accountability across multiple vendors; proactively offering the boundaries earns review points         | ❌ Missing | Third batch   |
| 9  | SLA / version lifecycle / EOL policy      | In-house work most often dies of version chaos; without this it looks unprofessional; ADR-0018 covers only the version-number semantics; lifecycle / EOL / support period are new decisions requiring a new requirement + ADR          | ❌ Missing | Third batch   |
| 10 | Security compliance evidence (PDPO / data residency / penetration testing) | Required by a Hong Kong carrier's internal controls and mandatory for passing review; blocked by the undecided O4 (call-trace retention period) / D5 (trace storage selection), so the retention period cannot be implemented              | ❌ Missing (blocked by O4/D5) | Third batch   |
| 11 | Capability-openness / plugin mechanism documentation for the multi-business platform | Where the long-term value of the platform positioning shows, guiding the onboarding process for new businesses; **v1.1 or on demand, not folded into the current milestone, to avoid scope creep**     | ❌ Missing (v1.1 / on demand) | Fourth batch   |

### 0.3 Prerequisite dependencies and engineering-fact constraints

> The following 8 engineering facts are the constraining premise for all scheduling and all deliverable content in this plan, and correspond item by item with the review record (`docs/reviews/product-packaging-plan-review-2026-10-09.md` §7); no packaging document may contradict these facts.

1. **The M8 exit signature is on hold**: the M8 release candidate (RC) artifacts are ready, but the exit signature is still on hold (`docs/plan.md` §0).
2. **E1/E4/E5 are not accepted**: reSIProcate production-path behaviour (E1), TLS hot rotation (E4), and externalized state (E5) are still open, awaiting M8 acceptance (`docs/plan.md` §5.1 O2/O3, ADR-0019).
3. **No lab evidence for the carrier PKI / certificate hot rotation**: there is no laboratory evidence yet for TLS and REQ-S-2/S-3.
4. **e2e = 0**: the e2e marker count in `docs/acceptance/test-plan.md` is 0; the full call + console end-to-end path has not landed.
5. **The O1 capacity target is unadjudicated**: the maintainer's target adjudication is still open; `AGENT.md` §2 forbids publishing any CPS/CAPS/BHCA/concurrency/latency figure before a measured adjudication, and the M6 dev-host measurement is for internal reference only.
6. **O4 / D5 are undecided**: neither the call-trace retention period (O4) nor the trace storage selection (D5) has been adjudicated, so the PDPO retention period and storage scheme cannot be implemented.
7. **REQ-S-4 / M4b are not accepted as a whole**: console security audit is currently only an engineering slice, and M4 engineering closure does not equal REQ-level acceptance (`docs/plan.md` §4.3, §5.4).
8. **The testbed is not a v1 deliverable**: ADR-0014 is explicit that v1 does not treat the testbed as a deliverable; testbed simulation results (including the M7.1 simulation platform and callload) are R&D / demo assets and must not stand in as carrier IOT or live-network capacity evidence.

***

## 1. Packaging layers and priorities

Following the logic of "first get the entry ticket, then fill in operability, then do delivery, and finally add the finishing touches", the work is advanced in four batches. At present the first batch has priority and the rest are on demand; the pacing will be reconfirmed after the M8 exit signature and the O1/O4/D5 adjudications.

### First batch: the review entry ticket (highest priority)

> Goal: to make the network department's review meeting feel at first glance that "this is a product, not a POC". Based on the multi-business platform positioning, highlight the platform value and the avoidance of vendor lock-in.

| #   | Deliverable                | Key content                                                                                                                                                   | Corresponding discussion thread                               |
| --- | ------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------- |
| 1.1 | Product one-pager + naming (provisional document name)       | A one-sentence value proposition (multi-business platform + new businesses can go live without changing the IMS core + no lock-in to a core-network vendor), the target scenario (in-house AS / 3GPP Third-Party AS role, **the current default direction, not a formal decision landing point, see §4.1**), an architecture sketch, the key KPIs, three-step deployment; the product name is the **provisional document name** In-house IMS Application Server (see §4.3), and the repo name is proposed to become `inhouse-ims-as` | Layer 1 "narrative: from project to product"; the naming discussion (repo name proposed to become `inhouse-ims-as`) |
| 1.2 | 3GPP specification-conformity matrix       | List TS 24.229, TS 29.228/29.229 (Cx), GSMA IR.92/IR.94, RFC 3261/6733 item by item, honestly marked Fully / Partial / N-A / open + the corresponding Release; TS 29.328/29.329 (Sh) marked **N/A** with the reason retained (no Diameter Sh); TS 32.260/32.299 (charging) marked **N/A** with the reason retained (no CDR). **Note: the production-stack E1/E4/E5 (reSIProcate behaviour, TLS hot rotation, externalized state) still await M8 acceptance; sippy is only a testbed behavioural baseline reference and does not enter production dependencies** | Trust credential #1 specific to the AS network element; "this is looked at at first glance even in an internal review"                 |
| 1.3 | Network-element dossier (NE Datasheet) | Written along platform dimensions: **a capacity model (blocked by O1; before the adjudication only the model structure and measurement method are written, with no concrete CAPS/BHCA/concurrency figures)**, per-engine capacity references, KPI definitions and thresholds, the alert inventory, a dependency diagram, resource specifications, and deployment forms; the capacity figures are filled in after the M6 real-socket measurement and the maintainer adjudication | "Every legitimate network element in a live network has this one; if you have it, you are treated as a peer" |
| 1.4 | Fault demarcation manual             | The fault-attribution decision process across the four parties AS / S-CSCF / HSS / charging domain, the SIP/Diameter packet-capture alignment method, a "prove in 5 minutes that it is not your fault" checklist, and common fault playbooks; **aligned with the RACI, the interface packet-capture owners, and the S-CSCF/HSS side logs**                                                                         | Make-or-break #1 of the three, "can be demarcated"; the prerequisite document for the responsibility boundary matrix                      |
| 1.5 | README rewritten as the product entry point     | The front page changes from "how to use it" to "why it is worth it": platform value proposition → architecture overview → key KPIs → specification conformance → three-step deployment → document index                                                                                            | Layer 1 narrative; "a POC README explains how to use it, a product front page explains why it is worth it"         |

### Second batch: operability

> Goal: make the NOC / operations team willing to take it on, able to troubleshoot, and able to roll back. Corresponds to "operability" and "the three make-or-break items" in the discussion.

| #   | Deliverable                | Key content                                                                         | Corresponding discussion thread                   |
| --- | ------------------ | ---------------------------------------------------------------------------- | ---------------------------------- |
| 2.1 | Grafana dashboard templates       | An overview board (overall health / session count / throughput / latency P50/P95/P99), SIP/ISC signalling detail, resource usage (CPU / memory / connection pool), and an alert panel; **no Diameter Sh panels (Sh is out of scope)**; no capacity commitment figures appear on the panels | Layer 3 "operability"; "a monitoring wall is more persuasive than a hundred pages of documentation"      |
| 2.2 | Alert rule reinforcement + an alert-to-action matrix  | Fill in the alerts on the critical paths (SIP 5xx spikes, ISC timeouts, session leaks, Pod restarts, etc.); alert severity (P1/P2/P3), trigger conditions, handling actions, escalation paths; **no Sh-related alerts (Sh is out of scope)**; capacity-class alerts stay deferred pending the O1 adjudication        | Layer 3 operability; the matching L1 runbook            |
| 2.3 | L1 / L2 runbook volumes | L1: alert handling, daily inspection, common fault handling (for the NOC); L2: deep troubleshooting, signalling analysis, configuration changes (for the second line); **prefer consolidating / reorganizing the existing runbooks in `docs/acceptance/` (m5-downscale, m5-state-stores, m4b-8, m8-native-consistency, etc.) over building new ones from scratch**                          | Make-or-break #3 of the three, "can be handed over"; "separate L1/L2 runbook volumes"  |
| 2.4 | Post-ISC business canary / traffic-diversion plan + coordination with S-CSCF-side iFC canarying | **The iFC trigger logic belongs to S-CSCF/HSS, not to the AS side; the AS only implements the business decision after the ISC trigger.** What the AS side can do is business-rule canarying (number range / percentage, corresponding to ADR-0021) and traffic diversion / rollback (runtime override, one-click sub-second shutdown of the AS business logic and pass-through to the next stage); iFC triggering by number range / percentage requires coordination configuration on the S-CSCF/HSS side, and this deliverable only defines the coordination interface and process. ⚠️ Risk note: it depends on S-CSCF-side coordination and a real-cluster drill (M8 7.2d is still blocked) | Make-or-break #2 of the three, "can be rolled back"; "a rollback drill record is extremely persuasive at network review" |
| 2.5 | Backup-restore plan + drill records      | Backup strategy for state data (Redis / PG), recovery RTO/RPO, a backup verification script, and periodic drill records; **it depends on a real cluster environment, and the M8 real-cluster evidence is currently on hold**                                | Layer 3 operability; "backup restore plus drill records"              |

### Third batch: delivery form and compliance

> Goal: complete deliverables, pass compliance review, and be deployable in a production environment. Corresponds to "delivery form" and "quality and compliance evidence" in the discussion.

| #   | Deliverable               | Key content                                                                          | Corresponding discussion thread                    |
| --- | ----------------- | ----------------------------------------------------------------------------- | ----------------------------------- |
| 3.1 | Preflight environment validation script  | One-click pre-deployment check: K8s version and API, node resources (CPU / memory / storage), dependent services (Redis / PG / network), Helm version, RBAC permissions         | Layer 4 "delivery form"; "can be brought up with one click, validated with one click"              |
| 3.2 | Offline installation package (air-gapped) | An image synchronization script (image save/load + a dependent-image manifest + checksums) + `helm package` + offline loading/installation scripts; **it must not produce a second installation form besides Helm (ADR-0013)**                          | Layer 4 delivery form; "air-gapped is the norm for domestic carriers"     |
| 3.3 | Responsibility boundary matrix (RACI)      | The division of responsibility between AS and the S-CSCF / HSS / charging domain / network management / security domains; a fault demarcation flowchart; the owners of interface packet captures; and a change-window coordination mechanism            | Trust credential #4 specific to the AS network element; "proactively offering the boundaries is what reviewers respond to most"      |
| 3.4 | Security compliance statement (PDPO)      | A Hong Kong PDPO (Personal Data (Privacy) Ordinance) compliance statement; **it describes only the data retention scope (MSISDN / IMPU / call traces), the deletion mechanism, and the data-residency principle (storage location, proof of no cross-border transfer); the concrete retention period is filled in after the O4 adjudication and the trace storage after the D5 adjudication, and no number of days is hard-coded at present**; a dependency vulnerability scan result and a penetration test plan are attached | Layer 5 "quality and compliance evidence"; Hong Kong localization, "PDPO rather than the MLPS"     |
| 3.5 | Version lifecycle and EOL policy    | A REQ-NF-XX and a corresponding ADR must be added first (outside ADR-0018's scope), and only then does the HLD/LLD/acceptance document chain follow; semantic versioning rules, release cadence, support periods, the EOL advance-notice period, upgrade paths and compatibility commitments, and the LTS / development-edition distinction                           | Layer 6 commercial packaging + item ① of the in-house six-piece set; "in-house work most often dies of version chaos" |

### Fourth batch: finishing touches (not urgent, advance on demand)

> Goal: upgrade the completeness of the product, supporting long-term platform evolution and fast onboarding of new businesses. Corresponds to "telecom-grade hard metrics" and "commercial packaging" in the discussion.

| #   | Deliverable           | Key content                                                           | Corresponding discussion thread                |
| --- | ------------- | -------------------------------------------------------------- | ------------------------------- |
| 4.1 | Performance benchmark report (internal review version)   | **After the O1 adjudication**, an internal-review report is compiled from the M6 real-socket measurement; at the current stage only the test methodology (environment, traffic model, metric definitions) is delivered, with no throughput/concurrency/latency figures at all | Layer 2 "telecom-grade hard metrics"; "a published performance benchmark report"       |
| 4.2 | 7×24 long-stability test report (on demand / v1.1)   | Continuous-run stability data, memory-leak detection, session-leak detection, abnormal-recovery statistics, cumulative throughput and success rate (all internal measurements); **on demand / v1.1, not part of the current milestone's default scope**                        | Layer 5 quality and compliance; "a 7×24 long-stability test report"        |
| 4.3 | API version compatibility policy    | Version-number rules for northbound/southbound interfaces, backward-compatibility commitments, deprecation policy, and an upgrade migration guide; **it depends on a new decision on top of ADR-0018 (advanced together with 3.5)**                                | Layer 5 quality and compliance; "an API version compatibility policy"         |
| 4.4 | Product whitepaper / architecture whitepaper | The complete product narrative, an in-depth analysis of the technical architecture, the design philosophy, a comparison with vendor solutions (TCO / flexibility / avoiding lock-in), and typical deployment scenarios              | Layer 1 narrative + Layer 6 commercial packaging; "whitepaper + architecture diagram" |
| 4.5 | Capability-openness mechanism documentation for the multi-business platform (v1.1 / on demand) | A business-engine SDK, plugin specifications, the new-business onboarding process, a development guide for the apps/ directory, and an explanation of the pluggable architecture design; **v1.1 / on demand, not folded into the current milestone**                          | Where the long-term value of the multi-business platform positioning shows            |

***

## 2. Proposed documentation structure changes

> Principle: **do not break the existing structure, only add**. The existing `architecture/`, `reviews/`, `handoff/`, and other directories stay as they are.

```
docs/
├── product/                    # 面向评审/交付的产品文档（新增）
│   ├── one-pager.md            # 产品一页纸（定位、价值、KPI、架构大图）
│   ├── ne-datasheet.md         # 网元档案（容量、KPI、告警、依赖）
│   ├── compliance-matrix.md    # 3GPP/GSMA/RFC 规范符合性矩阵
│   ├── responsibility-matrix.md # 责任边界矩阵（RACI）
│   ├── version-lifecycle.md    # 版本生命周期与 EOL 策略
│   └── security-privacy.md     # 安全与隐私合规（PDPO）
├── operations/                 # 运维文档（已落盘；已归集 docs/acceptance/ 现有 runbook 的索引与操作正文，原件保留不动）
│   ├── grafana-dashboards/     # Grafana 看板 JSON 模板（不含 Diameter Sh 看板，Sh 不在范围内）
│   │   ├── overview.json
│   │   └── sip-signaling.json
│   ├── runbook-l1.md           # L1 运维手册（NOC 日常）
│   ├── runbook-l2.md           # L2 运维手册（深度排障）
│   ├── fault-demarcation.md    # 故障定界手册
│   ├── backup-restore.md       # 备份恢复方案 + 演练记录模板
│   └── rollback-playbook.md    # 业务摘流 / 回退 + iFC 配合手册
└── delivery/                   # 交付相关（新增）
    ├── preflight.sh            # 部署前环境校验脚本
    ├── airgap-package.md       # 离线安装包制作与使用说明
    └── install-guide.md        # 安装部署指南（聚焦交付清单、镜像同步、helm install 命令序列；Helm 参数与行为仍以 `deploy/helm/README.md` 为权威，两文档互相链接、不重复）
```

### Notes

- **New** **`product/`**: centrally holds the product-level documents aimed at review / customers, separated from the engineering documents (architecture).
- **New** **`operations/`**: consolidates the existing runbooks in `docs/acceptance/` (m5-downscale, m5-state-stores, m4b-8, m8-native-consistency, etc.) together with operations documents such as alerts and rollback; when the directory was created the content was migrated or linked uniformly. That directory now exists, and the runbooks there use the approach of "consolidate + index + rewrite the operational body aimed at on-duty staff"; the **original runbooks under `docs/acceptance/` are left untouched**.
- **New** **`delivery/`**: the delivery-related content (installation scripts, offline package, deployment guide), so the delivery team can use it as soon as they receive it; `install-guide.md` only covers the delivery checklist, image synchronization, and the helm install command sequence, with `deploy/helm/README.md` remaining authoritative for Helm parameters and behaviour; the two documents link to each other and do not duplicate each other.
- The existing `README.md` is rewritten as the product entry page, linking to the three new directories above.

***

## 3. Execution order and scheduling (with blocking conditions)

> This section gives no unconditional total duration. Any schedule is conditional on the closure of the prerequisite dependencies; before the M8 exit signature and the O1/O4/D5 adjudications, no delivery date is committed for the full packaging scope.

### 3.1 Prerequisite dependencies

The following prerequisites must be confirmed before the packaging work starts or is expanded (for the engineering facts see §0.3):

- **The M8 exit signature is still on hold**: the RC artifacts are ready, but the acceptance exit has not been signed.
- **O1 (capacity target), O4 (call-trace retention period), and D5 (trace storage selection) are all unadjudicated**.
- **Acceptance items are not closed**: E1/E4/E5 (reSIProcate behaviour, TLS hot rotation, externalized state), REQ-S-2/S-3 (carrier PKI / certificate hot rotation), REQ-S-4, e2e marker = 0, and so on.

### 3.2 The deliverables split into two classes by blocking relationship

**Class A: no dependency on undecided items, can start immediately**

| Deliverable | Note |
| --- | --- |
| 1.1 One-pager / naming (provisional document name) | Written according to the current default direction and the provisional name; the formal decision landing point is still to be added (see §4.1, §4.3) |
| 1.2 Specification-conformity matrix | Honestly marked Fully / Partial / N-A / open; Sh and charging are marked N/A with the reason retained |
| 1.4 Fault demarcation manual | Aligned with the RACI, the interface packet-capture owners, and the S-CSCF/HSS side logs |
| 3.3 RACI responsibility boundary matrix | Division of responsibility across vendors, with no external blocker |
| 2.3 Runbook consolidation | Consolidate / reorganize the existing runbooks in `docs/acceptance/` rather than building new ones from scratch |
| 2.1 / 2.2 Dashboards and alerts | No capacity figures, no Diameter Sh panels and no Sh-related alerts |
| 3.1 Preflight script | Pre-deployment environment validation |
| 3.2 Offline package script | image save/load + a dependent-image manifest + checksums + `helm package` + the offline loading script |

**Class B: blocked by prerequisites, to be decided after scheduling**

| Deliverable | Blocking item |
| --- | --- |
| 1.3 The capacity chapter of the NE Datasheet | O1 (before the adjudication only the model structure and measurement method are written, with no figures) |
| 3.4 PDPO retention period | O4 / D5 (before the adjudication only the retention scope, deletion mechanism, and data-residency principle are written) |
| 4.1 Performance benchmark report | O1 (after the adjudication, compile the internal-review version from the M6 real-socket measurement) |
| 2.4 / 2.5 Real-cluster drills (iFC coordination, backup restore) | The M8 real-cluster environment (7.2d is still blocked), and 2.4 additionally needs S-CSCF/HSS-side coordination |
| 3.5 Version lifecycle / EOL | Requires a new requirement + ADR first (outside ADR-0018), then the design / acceptance document chain |

### 3.3 Multi-scenario scheduling

- **Scenario one (Class A only, the documentation and script packaging)**: not blocked by any undecided item; the first batch of entry tickets (1.1 / 1.2 / 1.4, etc.) and the parallelizable Class A script / consolidation work can be completed within **1–2 weeks**.
- **Scenario two (A + B in full)**: must be re-estimated **after the M8 exit signature and the O1/O4/D5 adjudications**, with **no preset total duration**; the timing of 2.4 / 2.5 additionally depends on the S-CSCF/HSS-side coordination window and the real-cluster schedule.

### 3.4 The boundary of testbed evidence

testbed simulation results (including the M7.1 simulation platform and callload) are R&D / demo assets; ADR-0014 is explicit that v1 does not treat the testbed as a deliverable, and they **must not stand in as carrier IOT or live-network capacity evidence in the packaging documents**. When citing M6 dev-host harness figures the "internal measurement / not external" qualifier must be attached, and before the O1 adjudication no capacity/performance metric may be promised on that basis.

***

## 4. Decisions and status

The current status is annotated for each of the following directions and names: some are confirmed only by discussion in `docs/discussion.md` and have not yet formed a formal decision landing point in `docs/plan.md` / an ADR; until the decision rows and review records are completed, they must not be described as "confirmed decisions" or as a formally approved product name.

### 4.1 Target scenario: internal go-live review (current default direction)

- **Direction**: A — xx carrier's internal go-live review (internal-review orientation). The maintainer confirmed this direction on 2026-10-09.
- **Status**: **the current default direction (confirmed by discussion, formal plan/ADR decision landing point still to be added)**. This direction currently comes only from the discussion in `docs/discussion.md` and has not yet formed a formal decision landing point in `docs/plan.md` / an ADR; a plan decision row + review record must be added later.
- **Impact**: the packaging focus falls on fault demarcation, rollback, RACI, and operations handover.

### 4.2 Business positioning: a multi-business platform

- **Current default direction**: option B — a multi-business platform (pluggable business engines; currently translation / anti-fraud, with colour ringback tone, voicemail, capability openness, etc. extensible in the future)
- **Status**: the apps/ architecture already supports it (one process per use case) and it was repeatedly confirmed in discussion; it is recommended to add an ADR / plan decision row
- **Rationale**: the apps/ architecture naturally supports one process per use case, and positioning as a platform has more long-term value than a single business
- **Impact**: the product narrative emphasizes "platform", "extensible", and "avoiding vendor lock-in"; the Datasheet is written along platform dimensions

### 4.3 Naming: In-house IMS Application Server (provisional document name / proposed name)

- **Provisional document name / proposed name (formal decision landing point still to be added)**: the product documents provisionally use **In-house IMS Application Server** (first occurrence annotated with the 3GPP Third-Party AS role, hereafter in-house AS). The maintainer confirmed on 2026-10-09 that the documents adopt this provisional name.
- **Repo name**: the git repo name is proposed to become `inhouse-ims-as` (confirmed by the maintainer on 2026-10-09; only the git repository name and the remote URL). The chart name, image name, and OTel service name stay `3rdparty-as` (an independent namespace, decoupled from the git repo name).
- **Status**: this name is **not a formally approved product name**; the formal naming decision still needs a plan/ADR landing point.
- **Impact**: only the git repository name changes (directory name + remote URL); component naming inside the repository such as the chart name, image name, and OTel service name is untouched; the impact surface is tiny (3 operations at the git layer) and no new ADR is needed. Until the formal decision landing point is completed, the product documents use the provisional name and annotate its status.

### 4.4 Scope and pacing

- **Class A (no dependency on undecided items) starts immediately**: complete the first batch of entry tickets first (see §3.2), without waiting for the M8 signature or the O1/O4/D5 adjudications.
- **Class B waits for the prerequisites to close**: after the M8 exit signature and the O1/O4/D5 adjudications, reconfirm the scope and schedule of the Class B deliverables (see §3.3 scenario two); no total duration is preset.

### 4.5 Added decision status (2026-10-10)

- **Formal framing of the target scenario**: xx carrier's internal production-readiness / release review (internal production-readiness/release review).
- **Framing of the product / document name**: `In-house IMS Application Server` is adopted as a descriptive product / document name, **not as a brand or trademark claim**.
- **Repository naming status**: the GitHub repository rename to `inhouse-ims-as` is recorded as reported complete by the maintainer; this task **does not** change this repository's local directory path or remote configuration.
- **The naming boundary stays unchanged**: the chart name, image name, and OTel service name continue to be `3rdparty-as`, and this addition does not change that boundary.
- **The O4/D5 decision landing point and its boundary**: the policy decisions for O4 (10-day default, configurable at deployment) and D5 (in-cluster PostgreSQL) are recorded in `docs/plan.md` §0, so the related "pending adjudication" wording in §4.4 is superseded at the level of the *decision*; but the trace storage / query / cleanup implementation, the evidence completion, and the remaining M8/O1 gates are still outstanding, and this addition **does not** constitute execution authorization.
- **Relationship to the existing text**: this section is an additional decision statement and **takes precedence over** the earlier wording in §4.1 / §4.3 and the status paragraph at the end of the document regarding "default direction / provisional name / repo name proposed to change"; the relevant old wording is retained as a historical audit chain and is neither deleted nor rewritten.
- **Governance boundary**: this addition creates no new ADR and does not constitute execution authorization, external acceptance, or REQ/milestone sign-off.

***

> This plan is a framework document with blocking conditions: among the directions and names listed in §4, the target scenario and the product name are currently confirmed only by discussion (the maintainer confirmed the direction / provisional name on 2026-10-09) and await a formal decision landing point; Class A deliverables can start immediately, while Class B deliverables are conditional on the closure of the prerequisite dependencies. The detailed templates and content of each deliverable can be refined further on the basis of the above directions.

---

## 5. Execution status (2026-10-10)

> This section is an **execution-status write-back**; it only appends and does not modify any existing content in §0–§4. The write-back details and verification evidence are in [`reviews/product-packaging-execution-record-2026-10-10.md`](reviews/product-packaging-execution-record-2026-10-10.md); the previous round of plan review is in [`reviews/product-packaging-plan-review-2026-10-09.md`](reviews/product-packaging-plan-review-2026-10-09.md).
>
> **Status framing**: "written to disk" in the table below = the file has been written and self-checked by the executor, **which does not equal accepted**. Maintainer review is **still pending** (the reviewer is still to be designated). **No commit was made in this round**.

| ID | Deliverable | Written-to path | Status | Blocking source |
|---|---|---|---|---|
| 1.1 | Product one-pager + naming (provisional document name) | `docs/product/one-pager.md` | Written to disk, awaiting maintainer review; 2026-10-12 B6 review: **needs modification**; 2026-10-12 closed-loop re-review: **accept (pending maintainer confirmation, see reviews/product-packaging-review-checklist-2026-10-12.md §7)** | — |
| 1.2 | 3GPP specification-conformity matrix | `docs/product/compliance-matrix.md` | Written to disk, awaiting maintainer review; 2026-10-12 B6 review: **needs modification**; 2026-10-12 closed-loop re-review: **accept (pending maintainer confirmation, see reviews/product-packaging-review-checklist-2026-10-12.md §7)** | — |
| 1.3 | Network-element dossier (NE Datasheet) | `docs/product/ne-datasheet.md` | Written to disk (§3 gives only the capacity **model structure and measurement methodology**, with no figures); 2026-10-12 B6 review: **needs modification**; 2026-10-12 closed-loop re-review: **accept (pending maintainer confirmation, see reviews/product-packaging-review-checklist-2026-10-12.md §7)** | **O1** (capacity value) |
| 1.4 | Fault demarcation manual | `docs/operations/fault-demarcation.md` | Written to disk, awaiting maintainer review; 2026-10-12 B6 review: **needs modification**; 2026-10-12 closed-loop re-review: **accept (pending maintainer confirmation, see reviews/product-packaging-review-checklist-2026-10-12.md §7)** | — |
| 1.5 | README rewritten as the product entry point | root `README.md`, `docs/README.md` | Written to disk, awaiting maintainer review | — |
| 2.1 | Grafana dashboard templates | `docs/operations/grafana-dashboards/{overview.json,sip-signaling.json,README.md}` | Written to disk; **no Sh panels / latency panels / capacity figures**; the scrape-wiring gap is explicitly marked as **not closed**; 2026-10-12 B6 review: dashboard JSON **accept**, dashboard README **needs modification**; 2026-10-12 closed-loop re-review: JSON and README **both accept (pending maintainer confirmation, see reviews/product-packaging-review-checklist-2026-10-12.md §7)** | Closing the wiring is chart work, not done |
| 2.2 | Alert rule reinforcement + an alert-to-action matrix | `docs/operations/alert-response-matrix.md`, `deploy/alerts/as-alerts.yaml`, `deploy/alerts/README.md` | Written to disk; two new groups `as.runtime` / `as.platform` with 5 rules in total were added, and **the original 5 `as.call-path` rules were not changed**; `promtool check rules` was **not executed** (the execution environment `dev-win03ib7niepf0` has no `promtool`, see [`environments.md`](environments.md)); 2026-10-12 B6 review: **needs modification**; 2026-10-12 closed-loop re-review: **accept (pending maintainer confirmation, see reviews/product-packaging-review-checklist-2026-10-12.md §7)** | Same as above (scrape wiring) |
| 2.3 | L1 / L2 runbook volumes | `docs/operations/{runbook-l1.md,runbook-l2.md,README.md}` | Written to disk; the originals in `docs/acceptance/` are **left untouched**, with only consolidation and indexing done; 2026-10-12 B6 review: **needs modification**; 2026-10-12 closed-loop re-review: **accept (pending maintainer confirmation, see reviews/product-packaging-review-checklist-2026-10-12.md §7)** | — |
| 2.4 | Traffic diversion / rollback + iFC coordination | `docs/operations/rollback-playbook.md` | Written to disk (the plan and the boundaries); **the real-cluster drill has not been done**; 2026-10-12 B6 review: **needs modification**; 2026-10-12 closed-loop re-review: **accept (pending maintainer confirmation, see reviews/product-packaging-review-checklist-2026-10-12.md §7)** | A real cluster (**M8 7.2d blocked**) + S-CSCF / HSS-side coordination |
| 2.5 | Backup-restore plan + drill records | `docs/operations/backup-restore.md` | Written to disk (the plan + a record **template**); **the drill records are empty**; no RPO / RTO figures are given; 2026-10-12 B6 review: **needs modification**; 2026-10-12 closed-loop re-review: **accept (pending maintainer confirmation, see reviews/product-packaging-review-checklist-2026-10-12.md §7)** | A real cluster; the customer-side HA is undecided (O5 / D3) |
| 3.1 | Preflight environment validation script | `docs/delivery/preflight.sh` | Written to disk; `bash -n` passes, and the `--dry-run` behaviour and exit code have been verified; 2026-10-12 B6 review: **needs modification**; 2026-10-12 closed-loop re-review: **accept (pending maintainer confirmation, see reviews/product-packaging-review-checklist-2026-10-12.md §7)** | The environment `dev-win03ib7niepf0` has no `kubectl` / `helm`, so validation against a real environment was not run |
| 3.2 | Offline installation package (air-gapped) | `docs/delivery/airgap-package.md`, `docs/delivery/scripts/{bundle-images.sh,load-images.sh,images.txt}` | Written to disk; the scope is limited to image save/load + a manifest + checksums + `helm package`, and it does not produce a second installation form; 2026-10-12 B6 review: **needs modification**; 2026-10-12 closed-loop re-review: **accept (pending maintainer confirmation, see reviews/product-packaging-review-checklist-2026-10-12.md §7)** | `helm package` was not actually tested (the environment `dev-win03ib7niepf0` has no `helm`) |
| 3.3 | Responsibility boundary matrix (RACI) | `docs/product/responsibility-matrix.md` | Written to disk, awaiting maintainer review; 2026-10-12 B6 review: **needs modification**; 2026-10-12 closed-loop re-review: **accept (pending maintainer confirmation, see reviews/product-packaging-review-checklist-2026-10-12.md §7)** | — |
| 3.4 | Security compliance statement (PDPO) | `docs/product/security-privacy.md` | Written to disk; **no retention day count is written**, only the retention scope / deletion mechanism / data-residency principle; 2026-10-12 B6 review: **needs modification**; 2026-10-12 closed-loop re-review: **accept (pending maintainer confirmation, see reviews/product-packaging-review-checklist-2026-10-12.md §7)** | **O4** (retention period), **D5** (storage selection) |
| 3.5 | Version lifecycle and EOL policy | `docs/product/version-lifecycle.md` | Written to disk; §3 **restates** the accepted decisions of ADR-0027 item by item and adds no new commitments; 2026-10-12 B6 review: **needs modification**; 2026-10-12 closed-loop re-review: **accept (pending maintainer confirmation, see reviews/product-packaging-review-checklist-2026-10-12.md §7)** | — |
| 4.1 | Performance benchmark report | §3 (the methodology chapter) of `docs/product/ne-datasheet.md` | **Only the methodology is delivered**, the formal report is not done; 2026-10-12 B6 review: **needs modification**; 2026-10-12 closed-loop re-review: **accept (pending maintainer confirmation, see reviews/product-packaging-review-checklist-2026-10-12.md §7)** | **O1** |
| 4.2 | 7×24 long-stability test report | — | **Not done, as planned**; **the attribution has been adjudicated (2026-10-12): v1.1** — delivered in the next batch, not folded into the current milestone | — |
| 4.3 | API version compatibility policy | §7 of `docs/product/version-lifecycle.md` | The pending points and their exit conditions are listed in the form "**candidate, undecided**"; no ADR. **The attribution has been adjudicated (2026-10-12): v1.1** — closed out with an ADR + a policy chapter in the next batch | Requires a maintainer decision + a new ADR + a review record |
| 4.4 | Product whitepaper / architecture whitepaper | — | **Not done, as planned**; **the attribution has been adjudicated (2026-10-12): on demand** — written only when there is an external narrative need | — |
| 4.5 | Capability-openness mechanism documentation for the multi-business platform | — | **Not done, as planned**; **the attribution has been adjudicated (2026-10-12): on demand** — written after the plugin mechanism lands, to avoid writing it out of thin air | — |

**Code-side change surface**: only `deploy/alerts/as-alerts.yaml` and `deploy/alerts/README.md` (new alert rule groups and their documentation); **no product code was changed**. **No git write operation was performed** (no `commit` / `add` / branch change / remote change / tag).

**Residual gaps (outside this round's change surface, recorded only)**: ① the alert scrape wiring is not closed (the chart has no `prometheus.io/scrape`, no ServiceMonitor / PodMonitor); ② `promtool check rules` was not run; ③ the `version` / `appVersion` in `Chart.yaml` are not in sync with the root `VERSION`; ④ the chart has no `kubeVersion` declaration (`preflight.sh` derives a lower bound from the API actually used by the template as a compensation).

**2026-10-12 B6 review write-back (appended, the original text of the rows above is unchanged)**: the review conclusions for the 16 documents have been recorded in
[`reviews/product-packaging-review-checklist-2026-10-12.md`](reviews/product-packaging-review-checklist-2026-10-12.md) §6 ——
**accept 0 / needs modification 16 / rejected 0**; among the accompanying assets the dashboard JSON and images.txt are accept and the rest need modification.
Five common gaps: ① the 2026-10-11 downstream sync (task E) covered only security-privacy and backup-restore, so the "undecided" and "e2e=0" wording for O4/O5/D3/D5 in the other 14 documents is
stale; ② 9+ occurrences of "e2e=0" across the whole batch (in reality 8 cases pass stably, REQ-F-1 = the automated subset is covered /
the full text is still open); ③ chart version consistency is missing (VERSION 0.2.0 vs Chart.yaml 0.0.0-skeleton, kubeVersion not written in),
which affects rollback-playbook L3 and the naming of delivery artifacts; ④ the delivery checklist does not include `deploy/alerts/` (of the four G9-a delivery products only three have landed);
⑤ functional defects in the accompanying scripts (bundle-images.sh:205 has the digest check inverted, load-images.sh --values does not match its name,
preflight.sh false-positives on Sentinel deployment). **This write-back signs off no REQ/milestone and authorizes no modification; the items needing modification are to be re-reviewed after closure.**
Also: residual gap item ② above (`promtool check rules` not run) was closed on 2026-10-11 —
(verified, docs/acceptance/artifacts/m5/2026-10-11/PASS-alert-check-full-2026-10-11.txt, 2026-10-11), 3 groups / 10 rules;
X1 scrape wiring still awaits external input.

**2026-10-12 closed-loop re-review write-back (appended, the original text of the rows above is unchanged)**: all 16 "needs modification" items of the B6 review checklist have been closed and re-reviewed, with the conclusions in [`reviews/product-packaging-review-checklist-2026-10-12.md`](reviews/product-packaging-review-checklist-2026-10-12.md) §7 —— **accept 16 / needs modification 0 / rejected 0 (pending maintainer confirmation)**; among the accompanying assets the dashboard README and the three delivery scripts moved from "needs modification" to accept, and the two dashboard JSON files and `images.txt` stay accept. Five common gaps: ①② (the task-E coverage gap, the e2e framing) are closed (the root cause, the marker table in `docs/acceptance/test-plan.md`, has been fixed and back-filled across the whole batch); ④ (the delivery checklist missing the alert rules) is closed per G9-a; ⑤ (functional defects in the accompanying scripts) is closed; ③ (chart version consistency) has been synced in the documentation wording throughout, while **the actual sync (the first `--apply` and writing `kubeVersion`) awaits a maintainer decision**. The items still unclosed are listed in §7.4 of the checklist. **This write-back signs off no REQ / milestone and does not constitute a basis for external delivery or acceptance.**

**Added later on 2026-10-12 (the original text of the rows above is unchanged)**:

1. **The chart's first sync has been executed** (responding to "the actual sync awaits a maintainer decision" above — on 2026-10-12 the maintainer ruled that the agent should judge the timing and the values): the `Chart.yaml` `version` / `appVersion` = `0.2.0` (the root `VERSION` is the single source), and `kubeVersion: ">=1.23.0-0"` has been written; `(verified, docs/acceptance/artifacts/m5/2026-10-12/PASS-chart-version-sync-2026-10-12.txt, 2026-10-12)`. Residual gap item ③ above is from now on **closed at the level of fact** (the original text of that row is retained as an audit chain).
2. **The attribution of the four Lane D items has been adjudicated** (on 2026-10-12 the maintainer authorized the agent to choose from three options): **4.2 → v1.1, 4.3 → v1.1, 4.4 → on demand, 4.5 → on demand**; these have been written into the status column of the four rows in the table above. Framing note: "v1.1" per this plan's existing usage means **the next batch**, not a formal release version definition (the "version naming" row of `docs/plan.md` §0 remains in effect).
3. **The X1 scrape wiring and B2 / B3 (including the RPO / RTO values) have been deferred to the next release per the maintainer's decision of 2026-10-12** — later reviews cite only the pointer and no longer list them separately (landing points: §3 X1 of `docs/handoff/2026-10-11-open-adjudication-register.md`, §5 of `docs/handoff/2026-10-12-b2-b3-deferred-items.md`).
4. This addition **signs off no REQ / milestone and does not constitute a basis for external delivery or acceptance**.
