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

# ADR-0010 Review Record

> Review target: `docs/architecture/adr/0010-autoscaling-hpa-downscale-guard.md` (newly created on 2026-09-28, Status: draft)
> Review date: 2026-09-28
> Reviewer: AI agent (cross-checked against the AGENT.md red lines and non-goals, PRD REQs, and the ADRs already on record)
> Review conclusion: **Pass** — moved to accepted; 2 known gaps in total, none of them blocking

## Review Method

| Dimension | Method |
|---|---|
| Consistency with red lines | Clause-by-clause comparison against the original text of `AGENT.md` §2 (non-goal: publish no capacity numbers before the M6 measurements), §5 (the decision module is a pure function), §7 (write the ADR together with the change) |
| Consistency with requirements | Checked PRD v0.2 REQ-NF-1 (a process restart does not lose sessions), REQ-NF-3 (horizontally scalable: safe scale-down is possible), REQ-NF-4 (ISSU does not drop calls) |
| Consistency with existing ADRs | Whether it conflicts with ADR-0002 (stateless + Redis session table + affinity as double insurance), ADR-0007 (runtime state in Redis), ADR-0009 (draining, skeleton) |
| Structural completeness | Whether it has Context / Decision / Consequences / Alternatives / Evidence / Related, and whether the section structure matches ADR-0002 |
| Implementation consistency | Whether the criteria are faithfully implemented in `platform/src/as_platform/ops/downscale_guard.py` and locked down by `unit`-level test cases |

## Findings and Adjudication

| # | Finding | Adjudication |
|---|---|---|
| 1 | **Threshold discipline**: the ADR gives no target utilization, no target `active_calls`, no replica upper or lower bounds and no timeout value; everything points at `deploy/helm/values.yaml` to be filled in by M6; the `required` guard in `hpa.yaml` ("measure it in M6 (O1), do not guess") has been implemented as corroboration, not a verbal promise | Accept, as L1 evidence of red-line compliance; the distinction between "a threshold is a capacity conclusion, a guard threshold is a safety criterion" holds, and the two concepts are not conflated |
| 2 | **The controller only produces a verdict, it does not operate K8s**: the implementation is a pure function (`plan_scale_down` / `may_remove`), with no socket, no clock and no global state; separating the verdict from the execution lets the scale-down guard be covered by unit tests in an environment without a cluster | Accept; consistent with AGENT.md §5 "the decision module is a pure function", and the decoupling argument that peels "may we scale down" out of "should we scale down" holds |
| 3 | **Coordination with draining**: once a candidate is selected, its removal must go through draining (stop new calls first → wait for the count to reach zero → then delete), and instances already draining are not selected as candidates again, avoiding a repeated dispatch of the same removal | Accept; consistent with the draining semantics of ADR-0009. ADR-0009 is still a skeleton, so this ADR has downgraded it to plain text in Related, producing no dead links and not overstepping by adjudicating on its behalf |
| 4 | **The guard threshold is a safety criterion, not a capacity number**: default 0 (non-zero means protection is on), and it is explicit that "the justification for adjusting it must be accepting the risk of dropping calls, not a capacity conclusion" | Accept; `protect_above < 0` is clamped to 0 (illegal input must not loosen protection), test cases lock this down, failure in the safe direction is conservative, and there is no opening in the opposite direction |
| 5 | **Implementation and tests landed together**: `platform/src/as_platform/ops/downscale_guard.py` and `platform/tests/test_downscale_guard.py` were delivered in the same batch; 10 `unit` test cases cover letting all-zero calls through, giving partial candidates when partially blocked, not re-selecting draining instances, reproducible ordering, illegal thresholds not loosening protection, and purity (asserting no socket / clock calls after monkeypatching) | Accept; complies with AGENT.md §7 "write the ADR together with the change it authorizes", so it is not an after-the-fact record; the design that yields a usable subset of candidates when blocked means operations does not have to wait idle |
| 6 | Structural completeness: the sections align with ADR-0002 (header four fields → Context → Decision → Consequences → Alternatives → Evidence → Related), and all five Alternatives give a "Why not", so they are not perfunctory | Accept; the negative part of Consequences is non-empty and states the reason for acceptance and the resolution point |
| 7 | Two known gaps: ① scale-down may be blocked for a long time, and the timeout and override policy are undefined operational parameters; ② the controller needs a per-instance `active_calls` metric, which is finer-grained than an aggregate metric, and the metric-side extension has not been done | Accept as **known gaps**, neither blocking; ① is written into the negative part of Consequences and marked to go into `values.yaml`, ② belongs to M5 operations wiring and metric extension work and is outside the adjudication scope of this ADR |

## Adjudication Summary

| Category | Count | Disposition |
|---|---|---|
| Accepted with no changes needed | 5 (findings 1, 2, 3, 4, 6) | — |
| Accepted as known gaps | 2 (finding 5 has no gap; the two gaps in finding 7) | Finding 7 ① goes into `deploy/helm/values.yaml` as an operational parameter; ② is resolved together with the M5 per-instance metric extension |
| Changes required | 0 | — |

## Sign-off

| Item | Value |
|---|---|
| Review conclusion | Pass |
| State transition | ADR-0010 `draft` → `accepted`; registry synchronized (the 0010 line in `docs/architecture/adr/README.md` skeleton → accepted ✓) |
| Reviewer | AI agent, 2026-09-28 |
| Maintainer sign-off | To be filled in |
