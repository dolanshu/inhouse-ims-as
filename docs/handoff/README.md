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

# Handoff records index

This directory holds handoff records: the plans, execution records and completion handoffs passed between working sessions (session-to-session handover and migration-checklist records). Entries are sorted by the date in the filename (ascending); records without a date in the filename are listed first. Topic lines are taken from each record's first heading.

| Date | File | Topic |
|---|---|---|
| — | [`pre-m8-demo-review-plan.md`](./pre-m8-demo-review-plan.md) | Pre-M8 Product Demo / Review Plan |
| 2026-09-30 | [`2026-09-30.md`](./2026-09-30.md) | Handoff Record — 3rdparty-as |
| 2026-10-04 | [`2026-10-04-m2.md`](./2026-10-04-m2.md) | M2 Handoff: reSIProcate Native Stack and Transport |
| 2026-10-05 | [`2026-10-05-callload-review-response-plan.md`](./2026-10-05-callload-review-response-plan.md) | callload branch review — assessment of findings and remediation plan (2026-10-05) |
| 2026-10-05 | [`2026-10-05-m5.1-remediation-cur.md`](./2026-10-05-m5.1-remediation-cur.md) | Handoff — M5.1 on branch `cur` (2026-10-05) |
| 2026-10-05 | [`2026-10-05-m7-engineering-complete.md`](./2026-10-05-m7-engineering-complete.md) | Handoff — M7 engineering complete (2026-10-05) |
| 2026-10-05 | [`2026-10-05-milestones-engineering-complete.md`](./2026-10-05-milestones-engineering-complete.md) | Handoff — M2 / M6 / M7 engineering complete (2026-10-05) |
| 2026-10-06 | [`2026-10-06-callload-merge-to-master.md`](./2026-10-06-callload-merge-to-master.md) | callload → master merge preparation (2026-10-06) |
| 2026-10-06 | [`2026-10-06-m8-release-candidate-plan.md`](./2026-10-06-m8-release-candidate-plan.md) | M8 release candidate — execution plan (2026-10-06) |
| 2026-10-07 | [`2026-10-07-demo-on-m71-platform-plan.md`](./2026-10-07-demo-on-m71-platform-plan.md) | Demo wired to the M7.1 platform — preparation (2026-10-07) |
| 2026-10-07 | [`2026-10-07-m7.1-sim-platform-plan.md`](./2026-10-07-m7.1-sim-platform-plan.md) | M7.1 test simulation platform — plan (2026-10-07) |
| 2026-10-07 | [`2026-10-07-m8-next-step-plan.md`](./2026-10-07-m8-next-step-plan.md) | M8 next step (2026-10-07) |
| 2026-10-09 | [`2026-10-09-sip-native-testing-plan.md`](./2026-10-09-sip-native-testing-plan.md) | Handoff — SIP native testing gate completion plan (2026-10-09) |
| 2026-10-10 | [`2026-10-10-unfinished-assessment-and-next-plan.md`](./2026-10-10-unfinished-assessment-and-next-plan.md) | Unfinished-item assessment and next-step plan (2026-10-10) |
| 2026-10-11 | [`2026-10-11-local-infra-bootstrap-execution-record.md`](./2026-10-11-local-infra-bootstrap-execution-record.md) | Execution record: local installation of infra (helm / kubectl / kind / promtool) |
| 2026-10-11 | [`2026-10-11-local-infra-bootstrap-plan.md`](./2026-10-11-local-infra-bootstrap-plan.md) | Execution plan: local installation of infra (helm / kubectl / kind / promtool) |
| 2026-10-11 | [`2026-10-11-open-adjudication-register.md`](./2026-10-11-open-adjudication-register.md) | Open Adjudications and Leftover Issues Register (2026-10-11) |
| 2026-10-11 | [`2026-10-11-s1-document-structure-cleanup.md`](./2026-10-11-s1-document-structure-cleanup.md) | S1 · Document and Structural Consistency Cleanup (First Batch) |
| 2026-10-11 | [`2026-10-11-s1-execution-record.md`](./2026-10-11-s1-execution-record.md) | S1 · Document and Structural Consistency Cleanup — Execution Record |
| 2026-10-11 | [`2026-10-11-w0-native-and-e2e-execution-record.md`](./2026-10-11-w0-native-and-e2e-execution-record.md) | Execution Record: W0 Real-Stack Build Normalization + A3 Re-verification + A4 Wave 1 e2e Landing |
| 2026-10-12 | [`2026-10-12-a6-b-packaging-execution.md`](./2026-10-12-a6-b-packaging-execution.md) | Execution Record: A6 Execution Stance + B1–B6 (2026-10-12) |
| 2026-10-12 | [`2026-10-12-b2-b3-deferred-items.md`](./2026-10-12-b2-b3-deferred-items.md) | B2 / B3 Deferred Items Register (requirement + ADR drafting, implemented next phase) |
| 2026-10-12 | [`2026-10-12-m8-batch1-complete-handoff.md`](./2026-10-12-m8-batch1-complete-handoff.md) | M8 Internal Release Wrap-Up — Handoff (2026-10-12) |
| 2026-10-12 | [`2026-10-12-m8-batch3-complete-handoff.md`](./2026-10-12-m8-batch3-complete-handoff.md) | M8 Batch 3 "kind/sim Evidence" Completion Handoff (2026-10-12) |
| 2026-10-12 | [`2026-10-12-m8-batch3-prompt.md`](./2026-10-12-m8-batch3-prompt.md) | M8 Batch 3 "kind/sim Evidence" — New Session Prompt |
| 2026-10-12 | [`2026-10-12-m8-batch4-complete-handoff.md`](./2026-10-12-m8-batch4-complete-handoff.md) | M8 Batch 4 "Sign-off and Review" Completion Handoff (2026-10-12) |
| 2026-10-12 | [`2026-10-12-m8-batch4-prompt.md`](./2026-10-12-m8-batch4-prompt.md) | M8 Batch 4 "Sign-off and Review" — New Session Prompt |
| 2026-10-12 | [`2026-10-12-m8-batch5-complete-handoff.md`](./2026-10-12-m8-batch5-complete-handoff.md) | M8 Batch 5 "Performance and Capacity (kind)" Completion Handoff (2026-10-12) |
| 2026-10-12 | [`2026-10-12-m8-batch5-prompt.md`](./2026-10-12-m8-batch5-prompt.md) | M8 Batch 5 "Performance and Capacity (kind)" — New Session Prompt |
| 2026-10-12 | [`2026-10-12-m8-batch6-complete-handoff.md`](./2026-10-12-m8-batch6-complete-handoff.md) | M8 Batch 6 "Documentation and Reports" Completion Handoff (2026-10-12) |
| 2026-10-12 | [`2026-10-12-m8-batch6-prompt.md`](./2026-10-12-m8-batch6-prompt.md) | M8 Batch 6 "Documentation and Reports" — New Session Prompt |
| 2026-10-12 | [`2026-10-12-m8-n2-countersign-record.md`](./2026-10-12-m8-n2-countersign-record.md) | M8 N2 Nine-Item Adjudication Counter-Signature Record (2026-10-12) |
| 2026-10-12 | [`2026-10-12-m8-scope-revision-internal-release-plan.md`](./2026-10-12-m8-scope-revision-internal-release-plan.md) | M8 Scope Revision and Internal-Version Wrap-up Plan (2026-10-12) |
| 2026-10-12 | [`2026-10-12-o1-and-native-reproducibility.md`](./2026-10-12-o1-and-native-reproducibility.md) | Execution Record: Integration-Layer Completion + native Reproducibility + O1 Saturation Probe + A4 Wave 2 Landing |
| 2026-10-12 | [`2026-10-12-remaining-items-execution.md`](./2026-10-12-remaining-items-execution.md) | Execution Record: Four Wrap-up Items + Two Deferred Items (later on 2026-10-12) |
| 2026-10-29 | [`2026-10-29-src-consolidation-migration-plan.md`](./2026-10-29-src-consolidation-migration-plan.md) | src/ Consolidation Migration Plan (R2612 E3 — survey only, nothing moved) |
