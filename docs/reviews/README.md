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

# Review records index

This directory holds the review records produced across M0–M8: design reviews, engineering slice reviews, adjudications, execution records and acceptance reviews. Per `AGENT.md` §3.2 / §3.3 (see also `.trae/rules/review-adjudication.md`), every review record ends with an `## Adjudication` adjudication table with the columns **ID / 来源 / 问题摘要 / 裁决 / 修改方案 / 状态 / 验证方式 / 备注**.

Entries are sorted by the date in the filename (ascending); records without a date in the filename (the earliest M0–M4 material) are listed first, alphabetically. Topic lines are taken from each record's first heading.

| Date | File | Topic |
|---|---|---|
| — | [`adr-0004-0009-0017-review.md`](./adr-0004-0009-0017-review.md) | Review Record — ADR-0004 / ADR-0009 / ADR-0017 (joint review of three skeleton backfills) |
| — | [`adr-0005-0007-0016-review.md`](./adr-0005-0007-0016-review.md) | ADR-0005 / 0007 / 0016 Review Record |
| — | [`adr-0006-review.md`](./adr-0006-review.md) | ADR-0006 Review Record |
| — | [`adr-0008-0012-0013-0014-0015-review.md`](./adr-0008-0012-0013-0014-0015-review.md) | ADR-0008 / 0012 / 0013 / 0014 / 0015 Review Record |
| — | [`adr-0010-review.md`](./adr-0010-review.md) | ADR-0010 Review Record |
| — | [`adr-0019-review-round2.md`](./adr-0019-review-round2.md) | Review Record (round 2) — ADR-0019: Production SIP Protocol Stack Selection |
| — | [`adr-0019-review.md`](./adr-0019-review.md) | Review Record — ADR-0019: Production SIP Protocol Stack Selection |
| — | [`adr-0020-review.md`](./adr-0020-review.md) | ADR-0020 Review Record (Feature Capability Gating and Toggles) |
| — | [`adr-m1-draft-review.md`](./adr-m1-draft-review.md) | ADR-0001/0002/0003/0018 M1 Draft Review Record |
| — | [`m0-skeleton-gap-review.md`](./m0-skeleton-gap-review.md) | M0 skeleton review — Gap Register |
| — | [`m1-exit-review.md`](./m1-exit-review.md) | M1 exit review record (Milestone Exit Review) |
| — | [`m1-to-head-code-review.md`](./m1-to-head-code-review.md) | M1 to HEAD code review record |
| — | [`m2-design-review.md`](./m2-design-review.md) | M2 Design Review Record (HLD / LLD) |
| — | [`m2a-kernel-review.md`](./m2a-kernel-review.md) | M2a Kernel Code Review Record |
| — | [`m2b-seam-review.md`](./m2b-seam-review.md) | M2b Boundary Seam Review Record |
| — | [`m3-decision-modules-review.md`](./m3-decision-modules-review.md) | M3 Decision Module Review Record (translation / anti-fraud) |
| — | [`m3-gate-review.md`](./m3-gate-review.md) | M3 Gate Review Record |
| — | [`m4-config-kernel-review.md`](./m4-config-kernel-review.md) | M4 Configuration Governance Kernel Review Record |
| — | [`m4-console-access-review.md`](./m4-console-access-review.md) | M4 Console Authentication and Audit, D7 Adjudication Review Record |
| — | [`m5-helm-alerts-review.md`](./m5-helm-alerts-review.md) | M5 Helm Template and Alert Rule Review Record |
| — | [`prd-v0.1-review.md`](./prd-v0.1-review.md) | PRD v0.1 Review Record |
| — | [`requirements-m1-review.md`](./requirements-m1-review.md) | Requirement List Review Record |
| 2026-09-30 | [`adr-0022-b2bua-control-review-2026-09-30.md`](./adr-0022-b2bua-control-review-2026-09-30.md) | ADR-0022 Technical Review Record |
| 2026-09-30 | [`d10-state-recovery-gap-review-2026-09-30.md`](./d10-state-recovery-gap-review-2026-09-30.md) | D10 state recovery design gap review record |
| 2026-09-30 | [`hld-lld-design-review-2026-09-30.md`](./hld-lld-design-review-2026-09-30.md) | Product-level HLD / LLD design review record |
| 2026-10-01 | [`adr-0023-redis-call-state-checkpoint-review-2026-10-01.md`](./adr-0023-redis-call-state-checkpoint-review-2026-10-01.md) | ADR-0023 Redis Call State Checkpoint Review Record |
| 2026-10-01 | [`m4b-1-console-ui-review-2026-10-01.md`](./m4b-1-console-ui-review-2026-10-01.md) | M4b-1 Console UI Engineering Preview Review |
| 2026-10-01 | [`m4b-3-change-order-journal-review-2026-10-01.md`](./m4b-3-change-order-journal-review-2026-10-01.md) | M4b-3 Change-Order Journal Review |
| 2026-10-01 | [`m4b-4-managed-rule-store-review-2026-10-01.md`](./m4b-4-managed-rule-store-review-2026-10-01.md) | M4b-4 ManagedRule Store Review |
| 2026-10-01 | [`m4b-5-1-read-api-review-2026-10-01.md`](./m4b-5-1-read-api-review-2026-10-01.md) | M4b-5-1 Read-Only API Engineering Review |
| 2026-10-01 | [`m4b-5-2b-write-api-review-2026-10-01.md`](./m4b-5-2b-write-api-review-2026-10-01.md) | M4b-5-2b ChangeOrder Journal Write API Engineering Review |
| 2026-10-01 | [`m4b-5-2c-applied-transaction-review-2026-10-01.md`](./m4b-5-2c-applied-transaction-review-2026-10-01.md) | M4b-5-2c APPLIED Transaction Coordination Engineering Review |
| 2026-10-02 | [`adr-0024-console-password-sessions-review-2026-10-02.md`](./adr-0024-console-password-sessions-review-2026-10-02.md) | ADR-0024 Console Password Sessions Design Review |
| 2026-10-02 | [`m4b-5-2d1-distribution-journal-review-2026-10-02.md`](./m4b-5-2d1-distribution-journal-review-2026-10-02.md) | M4b-5-2d1 Distribution Journal Review |
| 2026-10-02 | [`m4b-5-2d2-distribution-api-review-2026-10-02.md`](./m4b-5-2d2-distribution-api-review-2026-10-02.md) | M4b-5-2d2 Distribution API Review |
| 2026-10-02 | [`m4b-6a-auth-session-review-2026-10-02.md`](./m4b-6a-auth-session-review-2026-10-02.md) | M4b-6a Console Auth and Session Review |
| 2026-10-02 | [`m4b-6b-audit-integration-review-2026-10-02.md`](./m4b-6b-audit-integration-review-2026-10-02.md) | M4b-6b Audit API/Store Integration Review |
| 2026-10-03 | [`m4-closure-adjudication-2026-10-03.md`](./m4-closure-adjudication-2026-10-03.md) | M4 Closure Criteria Adjudication (Maintainer Grill Session) |
| 2026-10-03 | [`m4-req-calling-regex-lossless-adjudication-2026-10-03.md`](./m4-req-calling-regex-lossless-adjudication-2026-10-03.md) | M4 REQ: Rule match axis & console scope (Maintainer adjudication) |
| 2026-10-03 | [`m6-harness-current-review-2026-10-03.md`](./m6-harness-current-review-2026-10-03.md) | M6 Load Harness Current Work-in-Progress Review |
| 2026-10-03 | [`m6-harness-wip-review-2026-10-03.md`](./m6-harness-wip-review-2026-10-03.md) | M6 Load Harness Work-in-Progress Review |
| 2026-10-03 | [`m6-kickoff-review-2026-10-03.md`](./m6-kickoff-review-2026-10-03.md) | M6 Documentation-Only Kickoff Review |
| 2026-10-04 | [`m2-adapter-boundary-adjudication-2026-10-04.md`](./m2-adapter-boundary-adjudication-2026-10-04.md) | M2 adapter boundary adjudication (2026-10-04) |
| 2026-10-04 | [`m2-handoff-review-2026-10-04.md`](./m2-handoff-review-2026-10-04.md) | M2 Handoff Document Review |
| 2026-10-04 | [`m2-m6-session-progress-2026-10-04.md`](./m2-m6-session-progress-2026-10-04.md) | M2→M6 session progress and blockers (2026-10-04) |
| 2026-10-04 | [`m2-native-probe-review-2026-10-04.md`](./m2-native-probe-review-2026-10-04.md) | M2 Native Probe Review |
| 2026-10-04 | [`m2-p0-native-repro-review-2026-10-04.md`](./m2-p0-native-repro-review-2026-10-04.md) | M2 P0 native repro review (2026-10-04) |
| 2026-10-04 | [`m2-transport-native-probe-review-2026-10-04.md`](./m2-transport-native-probe-review-2026-10-04.md) | M2 Transport and Native Probe Review |
| 2026-10-04 | [`m5-0a-gate-review-2026-10-04.md`](./m5-0a-gate-review-2026-10-04.md) | M5-0a review (2026-10-04) |
| 2026-10-04 | [`m5-0b-integration-compose-review-2026-10-04.md`](./m5-0b-integration-compose-review-2026-10-04.md) | M5-0b review (2026-10-04) |
| 2026-10-04 | [`m5-0c-chart-check-review-2026-10-04.md`](./m5-0c-chart-check-review-2026-10-04.md) | M5-0c review (2026-10-04) |
| 2026-10-04 | [`m5-1a-images-review-2026-10-04.md`](./m5-1a-images-review-2026-10-04.md) | M5-1a review (2026-10-04) |
| 2026-10-04 | [`m5-1b-kind-helm-review-2026-10-04.md`](./m5-1b-kind-helm-review-2026-10-04.md) | M5-1b review (2026-10-04) |
| 2026-10-04 | [`m5-1c-ingress-template-review-2026-10-04.md`](./m5-1c-ingress-template-review-2026-10-04.md) | M5-1c review (2026-10-04) |
| 2026-10-04 | [`m5-1d-config-pg-review-2026-10-04.md`](./m5-1d-config-pg-review-2026-10-04.md) | M5-1d review (2026-10-04) |
| 2026-10-04 | [`m5-217-issu-scale-review-2026-10-04.md`](./m5-217-issu-scale-review-2026-10-04.md) | M5-217 review (2026-10-04) |
| 2026-10-04 | [`m5-2a-metrics-runtime-review-2026-10-04.md`](./m5-2a-metrics-runtime-review-2026-10-04.md) | M5-2a review (2026-10-04) |
| 2026-10-04 | [`m5-2b-readiness-review-2026-10-04.md`](./m5-2b-readiness-review-2026-10-04.md) | M5-2b review (2026-10-04) |
| 2026-10-04 | [`m5-2c-downscale-config-review-2026-10-04.md`](./m5-2c-downscale-config-review-2026-10-04.md) | M5-2c review (2026-10-04) |
| 2026-10-04 | [`m5-2d-downscale-runbook-review-2026-10-04.md`](./m5-2d-downscale-runbook-review-2026-10-04.md) | M5-2d review (2026-10-04) |
| 2026-10-04 | [`m5-3a-rollout-review-2026-10-04.md`](./m5-3a-rollout-review-2026-10-04.md) | M5-3a review (2026-10-04) |
| 2026-10-04 | [`m5-3b-scale-guard-review-2026-10-04.md`](./m5-3b-scale-guard-review-2026-10-04.md) | M5-3b review (2026-10-04) |
| 2026-10-04 | [`m5-3c-closure-docs-review-2026-10-04.md`](./m5-3c-closure-docs-review-2026-10-04.md) | M5-3c review (2026-10-04) |
| 2026-10-04 | [`m5-7.2d-ingress-closure-review-2026-10-04.md`](./m5-7.2d-ingress-closure-review-2026-10-04.md) | M5-7.2d review (2026-10-04) |
| 2026-10-04 | [`m5-a-helm-chart-review-2026-10-04.md`](./m5-a-helm-chart-review-2026-10-04.md) | M5-a review (2026-10-04) |
| 2026-10-04 | [`m5-b-alerts-review-2026-10-04.md`](./m5-b-alerts-review-2026-10-04.md) | M5-b review (2026-10-04) |
| 2026-10-04 | [`m5-c-downscale-guard-review-2026-10-04.md`](./m5-c-downscale-guard-review-2026-10-04.md) | M5-c review (2026-10-04) |
| 2026-10-04 | [`m5-closure-adjudication-2026-10-04.md`](./m5-closure-adjudication-2026-10-04.md) | M5 closure adjudication (2026-10-04) |
| 2026-10-04 | [`m5-d-metrics-contract-review-2026-10-04.md`](./m5-d-metrics-contract-review-2026-10-04.md) | M5-d review (2026-10-04) |
| 2026-10-04 | [`m5-d12-adr-0026-review-2026-10-04.md`](./m5-d12-adr-0026-review-2026-10-04.md) | M5-D12-adr review (2026-10-04) |
| 2026-10-04 | [`m5-d12-helm-state-review-2026-10-04.md`](./m5-d12-helm-state-review-2026-10-04.md) | M5-D12-helm review (2026-10-04) |
| 2026-10-04 | [`m5-d12-kind-bundled-review-2026-10-04.md`](./m5-d12-kind-bundled-review-2026-10-04.md) | M5-D12-kind review (2026-10-04) |
| 2026-10-04 | [`m5-d12-production-profile-review-2026-10-04.md`](./m5-d12-production-profile-review-2026-10-04.md) | M5-D12-prod review (2026-10-04) |
| 2026-10-04 | [`m5-e-version-store-review-2026-10-04.md`](./m5-e-version-store-review-2026-10-04.md) | M5-e review (2026-10-04) |
| 2026-10-04 | [`m5-f-container-draining-review-2026-10-04.md`](./m5-f-container-draining-review-2026-10-04.md) | M5-f review (2026-10-04) |
| 2026-10-04 | [`m5-h10-ops-wiring-review-2026-10-04.md`](./m5-h10-ops-wiring-review-2026-10-04.md) | M5-H10 review (2026-10-04) |
| 2026-10-04 | [`m5-task-register-2026-10-04.md`](./m5-task-register-2026-10-04.md) | M5 Task Register and Review Index (2026-10-04) |
| 2026-10-04 | [`m6-micro-measure-adjudication-2026-10-04.md`](./m6-micro-measure-adjudication-2026-10-04.md) | M6 micro-measure adjudication (2026-10-04) |
| 2026-10-04 | [`m6-resip-probe-smoke-review-2026-10-04.md`](./m6-resip-probe-smoke-review-2026-10-04.md) | M6 resip_probe external UAS smoke review (2026-10-04) |
| 2026-10-05 | [`adr-0022-acceptance-adjudication-2026-10-05.md`](./adr-0022-acceptance-adjudication-2026-10-05.md) | ADR-0022 acceptance adjudication (2026-10-05) |
| 2026-10-05 | [`adr-0022-acceptance-review-2026-10-05.md`](./adr-0022-acceptance-review-2026-10-05.md) | ADR-0022 acceptance review — B2BUA control layer (2026-10-05) |
| 2026-10-05 | [`callload-m2-m6-m7-demo-branch-review-2026-10-05.md`](./callload-m2-m6-m7-demo-branch-review-2026-10-05.md) | callload Branch Review Record — M2 Second Half / M6 / M7 / Pre-M8 Demo |
| 2026-10-05 | [`callload-remediation-adjudication-2026-10-05.md`](./callload-remediation-adjudication-2026-10-05.md) | callload Review Remediation — Adjudication Record (2026-10-05) |
| 2026-10-05 | [`cross-milestone-final-adjudication-2026-10-05.md`](./cross-milestone-final-adjudication-2026-10-05.md) | Cross-milestone final engineering adjudication (2026-10-05) |
| 2026-10-05 | [`cross-milestone-final-review-2026-10-05.md`](./cross-milestone-final-review-2026-10-05.md) | Cross-milestone final engineering review (2026-10-05) |
| 2026-10-05 | [`d10-redis-restart-adjudication-2026-10-05.md`](./d10-redis-restart-adjudication-2026-10-05.md) | D10 Redis + process restart adjudication (2026-10-05) |
| 2026-10-05 | [`d10-redis-restart-review-2026-10-05.md`](./d10-redis-restart-review-2026-10-05.md) | D10 Redis + process restart review (2026-10-05) |
| 2026-10-05 | [`d10-req-nf1-harness-adjudication-2026-10-05.md`](./d10-req-nf1-harness-adjudication-2026-10-05.md) | D10 REQ-NF-1 harness adjudication (2026-10-05) |
| 2026-10-05 | [`d10-req-nf1-harness-review-2026-10-05.md`](./d10-req-nf1-harness-review-2026-10-05.md) | D10 REQ-NF-1 engineering harness review (2026-10-05) |
| 2026-10-05 | [`d8-req-nf-15-adjudication-2026-10-05.md`](./d8-req-nf-15-adjudication-2026-10-05.md) | D8 REQ-NF-15 adjudication (2026-10-05) |
| 2026-10-05 | [`d8-req-nf-15-review-2026-10-05.md`](./d8-req-nf-15-review-2026-10-05.md) | D8 REQ-NF-15 testbed / performance traceability review (2026-10-05) |
| 2026-10-05 | [`m2-d3-sentinel-adjudication-2026-10-05.md`](./m2-d3-sentinel-adjudication-2026-10-05.md) | M2 D3 Redis Sentinel adjudication (2026-10-05) |
| 2026-10-05 | [`m2-d3-sentinel-review-2026-10-05.md`](./m2-d3-sentinel-review-2026-10-05.md) | M2 D3 Redis Sentinel review (2026-10-05) |
| 2026-10-05 | [`m2-engineering-closure-adjudication-2026-10-05.md`](./m2-engineering-closure-adjudication-2026-10-05.md) | M2 engineering closure adjudication — stack binding slice (2026-10-05) |
| 2026-10-05 | [`m2-milestone-engineering-complete-adjudication-2026-10-05.md`](./m2-milestone-engineering-complete-adjudication-2026-10-05.md) | M2 milestone engineering complete adjudication (2026-10-05) |
| 2026-10-05 | [`m2-p0-adjudication-2026-10-05.md`](./m2-p0-adjudication-2026-10-05.md) | M2 P0 adjudication (2026-10-05) |
| 2026-10-05 | [`m2-p2-ingress-adjudication-2026-10-05.md`](./m2-p2-ingress-adjudication-2026-10-05.md) | M2 P2 ingress adjudication (2026-10-05) |
| 2026-10-05 | [`m2-p2-ingress-runtime-review-2026-10-05.md`](./m2-p2-ingress-runtime-review-2026-10-05.md) | M2 P2 ingress runtime review (2026-10-05) |
| 2026-10-05 | [`m2-p2b-tcp-transport-review-2026-10-05.md`](./m2-p2b-tcp-transport-review-2026-10-05.md) | M2 P2b TCP transport review (2026-10-05) |
| 2026-10-05 | [`m2-p2c-resip-runtime-adjudication-2026-10-05.md`](./m2-p2c-resip-runtime-adjudication-2026-10-05.md) | M2 P2c resip runtime adjudication (2026-10-05) |
| 2026-10-05 | [`m2-p2c-resip-runtime-review-2026-10-05.md`](./m2-p2c-resip-runtime-review-2026-10-05.md) | M2 P2c resip runtime review (2026-10-05) |
| 2026-10-05 | [`m2-p2d-second-pass-review-2026-10-05.md`](./m2-p2d-second-pass-review-2026-10-05.md) | M2 P2d second-pass review (2026-10-05) |
| 2026-10-05 | [`m2-p2d-tls-runtime-adjudication-2026-10-05.md`](./m2-p2d-tls-runtime-adjudication-2026-10-05.md) | M2 P2d TLS runtime adjudication (2026-10-05) |
| 2026-10-05 | [`m2-p2d-tls-runtime-review-2026-10-05.md`](./m2-p2d-tls-runtime-review-2026-10-05.md) | M2 P2d TLS runtime review (2026-10-05) |
| 2026-10-05 | [`m2-p3-tls-rotation-adjudication-2026-10-05.md`](./m2-p3-tls-rotation-adjudication-2026-10-05.md) | M2 P3 TLS overlap adjudication (2026-10-05) |
| 2026-10-05 | [`m2-p3-tls-rotation-review-2026-10-05.md`](./m2-p3-tls-rotation-review-2026-10-05.md) | M2 P3 TLS overlap review (2026-10-05) |
| 2026-10-05 | [`m2-req-s3-adjudication-2026-10-05.md`](./m2-req-s3-adjudication-2026-10-05.md) | M2 REQ-S-3 product overlap adjudication (2026-10-05) |
| 2026-10-05 | [`m2-req-s3-review-2026-10-05.md`](./m2-req-s3-review-2026-10-05.md) | M2 REQ-S-3 product overlap integration review (2026-10-05) |
| 2026-10-05 | [`m2-task-register-2026-10-05.md`](./m2-task-register-2026-10-05.md) | M2 task register (2026-10-05) |
| 2026-10-05 | [`m2-tcp-product-review-2026-10-05.md`](./m2-tcp-product-review-2026-10-05.md) | M2 product TCP transport review (2026-10-05) |
| 2026-10-05 | [`m5-full-chain-review-2026-10-05.md`](./m5-full-chain-review-2026-10-05.md) | M5 Full-Chain Review Record — Requirement / ADR / Design / Code / Testing |
| 2026-10-05 | [`m5.1-closure-adjudication-2026-10-05.md`](./m5.1-closure-adjudication-2026-10-05.md) | M5.1 Engineering Adjudication — 2026-10-05 |
| 2026-10-05 | [`m5.1-cur-implementation-review-2026-10-05.md`](./m5.1-cur-implementation-review-2026-10-05.md) | M5.1 `cur` Implementation Review — 2026-10-05 |
| 2026-10-05 | [`m6-engineering-complete-adjudication-2026-10-05.md`](./m6-engineering-complete-adjudication-2026-10-05.md) | M6 engineering complete adjudication (2026-10-05) |
| 2026-10-05 | [`m6-o1-formal-review-2026-10-05.md`](./m6-o1-formal-review-2026-10-05.md) | M6 O1 formal measurement review (2026-10-05) |
| 2026-10-05 | [`m6-product-60s-review-2026-10-05.md`](./m6-product-60s-review-2026-10-05.md) | M6 product runtime 60s measure review (2026-10-05) |
| 2026-10-05 | [`m6-product-runtime-adjudication-2026-10-05.md`](./m6-product-runtime-adjudication-2026-10-05.md) | M6 product ResipRuntimeListener adjudication (2026-10-05) |
| 2026-10-05 | [`m6-product-runtime-micro-review-2026-10-05.md`](./m6-product-runtime-micro-review-2026-10-05.md) | M6 product runtime micro-measure review (2026-10-05) |
| 2026-10-05 | [`m6-product-runtime-smoke-review-2026-10-05.md`](./m6-product-runtime-smoke-review-2026-10-05.md) | M6 product ResipRuntimeListener smoke review (2026-10-05) |
| 2026-10-05 | [`m7-1-recovery-tu-adjudication-2026-10-05.md`](./m7-1-recovery-tu-adjudication-2026-10-05.md) | M7.1 RecoveryTU product native tree adjudication (2026-10-05) |
| 2026-10-05 | [`m7-1-recovery-tu-review-2026-10-05.md`](./m7-1-recovery-tu-review-2026-10-05.md) | M7.1 RecoveryTU product native tree review (2026-10-05) |
| 2026-10-05 | [`m7-2-recovery-coordinator-adjudication-2026-10-05.md`](./m7-2-recovery-coordinator-adjudication-2026-10-05.md) | M7.2 non-blocking Redis continuation adjudication (2026-10-05) |
| 2026-10-05 | [`m7-2-recovery-coordinator-review-2026-10-05.md`](./m7-2-recovery-coordinator-review-2026-10-05.md) | M7.2 non-blocking Redis continuation review (2026-10-05) |
| 2026-10-05 | [`m7-3-call-controller-recovery-adjudication-2026-10-05.md`](./m7-3-call-controller-recovery-adjudication-2026-10-05.md) | M7.3 CallController restore adjudication (2026-10-05) |
| 2026-10-05 | [`m7-3-call-controller-recovery-review-2026-10-05.md`](./m7-3-call-controller-recovery-review-2026-10-05.md) | M7.3 CallController restore review (2026-10-05) |
| 2026-10-05 | [`m7-4-checkpoint-commit-adjudication-2026-10-05.md`](./m7-4-checkpoint-commit-adjudication-2026-10-05.md) | M7.4 owner/fencing/commit adjudication (2026-10-05) |
| 2026-10-05 | [`m7-4-checkpoint-commit-review-2026-10-05.md`](./m7-4-checkpoint-commit-review-2026-10-05.md) | M7.4 owner/fencing/commit review (2026-10-05) |
| 2026-10-05 | [`m7-5-checkpoint-lifecycle-adjudication-2026-10-05.md`](./m7-5-checkpoint-lifecycle-adjudication-2026-10-05.md) | M7.5 TTL renewal and terminal cleanup adjudication (2026-10-05) |
| 2026-10-05 | [`m7-5-checkpoint-lifecycle-review-2026-10-05.md`](./m7-5-checkpoint-lifecycle-review-2026-10-05.md) | M7.5 TTL renewal and terminal cleanup review (2026-10-05) |
| 2026-10-05 | [`m7-6-d10-product-integration-adjudication-2026-10-05.md`](./m7-6-d10-product-integration-adjudication-2026-10-05.md) | M7.6 D10 product integration test adjudication (2026-10-05) |
| 2026-10-05 | [`m7-6-d10-product-integration-review-2026-10-05.md`](./m7-6-d10-product-integration-review-2026-10-05.md) | M7.6 D10 product integration test review (2026-10-05) |
| 2026-10-05 | [`m7-d10-product-adjudication-2026-10-05.md`](./m7-d10-product-adjudication-2026-10-05.md) | M7 D10 product path adjudication (2026-10-05) |
| 2026-10-05 | [`m7-d10-second-pass-review-2026-10-05.md`](./m7-d10-second-pass-review-2026-10-05.md) | M7.1–M7.6 D10 product slices — second-pass review (2026-10-05) |
| 2026-10-05 | [`m7-d10-status-2026-10-05.md`](./m7-d10-status-2026-10-05.md) | M7 D10 honesty status — recovery vs product (2026-10-05) |
| 2026-10-05 | [`m7-d10-third-pass-review-2026-10-05.md`](./m7-d10-third-pass-review-2026-10-05.md) | M7/D10 third-pass review (2026-10-05) |
| 2026-10-05 | [`m7-e1-contract-review-2026-10-05.md`](./m7-e1-contract-review-2026-10-05.md) | M7 E1 contract smoke — second-pass review (2026-10-05) |
| 2026-10-05 | [`m7-engineering-closure-adjudication-2026-10-05.md`](./m7-engineering-closure-adjudication-2026-10-05.md) | M7 engineering closure adjudication — control layer slice (2026-10-05) |
| 2026-10-05 | [`m7-engineering-slice-adjudication-2026-10-05.md`](./m7-engineering-slice-adjudication-2026-10-05.md) | M7 engineering slice adjudication (2026-10-05) |
| 2026-10-05 | [`m7-engineering-slice-review-2026-10-05.md`](./m7-engineering-slice-review-2026-10-05.md) | M7 engineering slice review (2026-10-05) |
| 2026-10-05 | [`m7-final-engineering-adjudication-2026-10-05.md`](./m7-final-engineering-adjudication-2026-10-05.md) | M7 final engineering adjudication (2026-10-05) |
| 2026-10-05 | [`m7-m7-tail-engineering-review-2026-10-05.md`](./m7-m7-tail-engineering-review-2026-10-05.md) | M7 tail engineering slice review (2026-10-05) |
| 2026-10-05 | [`m7-milestone-engineering-closure-adjudication-2026-10-05.md`](./m7-milestone-engineering-closure-adjudication-2026-10-05.md) | M7 milestone engineering closure adjudication (2026-10-05) |
| 2026-10-05 | [`m7-milestone-engineering-complete-adjudication-2026-10-05.md`](./m7-milestone-engineering-complete-adjudication-2026-10-05.md) | M7 milestone engineering complete adjudication (2026-10-05) |
| 2026-10-05 | [`m7-process-shell-recovery-adjudication-2026-10-05.md`](./m7-process-shell-recovery-adjudication-2026-10-05.md) | M7 process shell + recovery adjudication (2026-10-05) |
| 2026-10-05 | [`m7-process-shell-recovery-review-2026-10-05.md`](./m7-process-shell-recovery-review-2026-10-05.md) | M7 process shell + recovery wiring review (2026-10-05) |
| 2026-10-06 | [`m5-req-acceptance-review-2026-10-06.md`](./m5-req-acceptance-review-2026-10-06.md) | M5 REQ-Level Acceptance Review Record (M8 Release Candidate, Phase B Minimum Set) |
| 2026-10-06 | [`m8-exit-review-2026-10-06.md`](./m8-exit-review-2026-10-06.md) | M8 release candidate exit review record (2026-10-06) |
| 2026-10-06 | [`m8-phase-a-f6-f8-note-2026-10-06.md`](./m8-phase-a-f6-f8-note-2026-10-06.md) | M8 Phase A F6/F8 Record (2026-10-06) |
| 2026-10-09 | [`product-packaging-plan-review-2026-10-09.md`](./product-packaging-plan-review-2026-10-09.md) | Review Record for `docs/product-packaging-plan.md` |
| 2026-10-10 | [`product-packaging-execution-record-2026-10-10.md`](./product-packaging-execution-record-2026-10-10.md) | Productization Packaging Execution Record (2026-10-10) |
| 2026-10-10 | [`unfinished-assessment-2026-10-10-review-of-review-evaluation.md`](./unfinished-assessment-2026-10-10-review-of-review-evaluation.md) | Review Record: Evaluation of the Review Comments on `unfinished-assessment-2026-10-10-review.md` |
| 2026-10-10 | [`unfinished-assessment-2026-10-10-review-of-review.md`](./unfinished-assessment-2026-10-10-review-of-review.md) | Review Comments on the Review Record (review of review, 2026-10-10) |
| 2026-10-10 | [`unfinished-assessment-2026-10-10-review.md`](./unfinished-assessment-2026-10-10-review.md) | Review Record: Unfinished-Item Assessment and Next Plan (2026-10-10) |
| 2026-10-12 | [`m8-batch1-release-packaging-review-2026-10-12.md`](./m8-batch1-release-packaging-review-2026-10-12.md) | Review Record — M8 internal build batch 1: release and packaging |
| 2026-10-12 | [`m8-batch3-kind-sim-evidence-review-2026-10-12.md`](./m8-batch3-kind-sim-evidence-review-2026-10-12.md) | M8 batch 3 "kind/sim evidence" review record (2026-10-12) |
| 2026-10-12 | [`m8-batch4-signoff-review-2026-10-12.md`](./m8-batch4-signoff-review-2026-10-12.md) | Review Record — M8 internal build batch 4: sign-off and review |
| 2026-10-12 | [`m8-batch5-performance-capacity-review-2026-10-12.md`](./m8-batch5-performance-capacity-review-2026-10-12.md) | M8 batch 5 "Performance and capacity (kind)" review record (2026-10-12) |
| 2026-10-12 | [`m8-batch6-docs-report-review-2026-10-12.md`](./m8-batch6-docs-report-review-2026-10-12.md) | Review Record — M8 internal build batch 6: documentation and report |
| 2026-10-12 | [`m8-internal-release-exit-review-2026-10-12.md`](./m8-internal-release-exit-review-2026-10-12.md) | M8 Internal Release Wrap-Up Review Record (2026-10-12) |
| 2026-10-12 | [`m8-scope-revision-internal-release-plan-review-2026-10-12.md`](./m8-scope-revision-internal-release-plan-review-2026-10-12.md) | Review Record — M8 Scope Revision and Internal Release Wrap-Up Plan |
| 2026-10-12 | [`product-packaging-review-checklist-2026-10-12.md`](./product-packaging-review-checklist-2026-10-12.md) | Productization Packaging 16 Documents · Review Item Checklist (B6) |
| 2026-10-13 | [`m8-external-dependency-risk-acceptance-2026-10-13.md`](./m8-external-dependency-risk-acceptance-2026-10-13.md) | M8 External Hard Dependency Written Risk Acceptance (Path C, 2026-10-13) |
