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

# ADR-0020 Review Record (Feature Capability Gating and Toggles)

> Review target: `docs/architecture/adr/0020-feature-capability-gating.md` (Status: draft → this review)
> Review date: 2026-09-28
> Reviewer: AI agent (cross-checked against AGENT.md §3.4 / §6, ADR-0006, and the already-implemented gating code)
> Review conclusion: **Pass** — moved to accepted; 1 undecided item (D7) listed as a known gap, non-blocking

## Review Method

| Dimension | Method |
|---|---|
| Consistency with red lines | AGENT.md §3.4 (every feature must adjudicate the toggle / default state / canary / removal condition), §6 (both states must be covered) |
| Consistency with existing ADRs | ADR-0006 (feature flags reuse the configuration governance pipeline), ADR-0007 (runtime overrides live in Redis) |
| Consistency with implementation | `platform/src/as_platform/gating/` (off by default, fail-closed, idempotent verdicts), `platform/src/as_platform/api/contract.py` (`ToggleDTO` entering `ConfigBundle`) |
| Structural completeness | Whether it has Context / Decision / Consequences / Alternatives / Evidence / Related |

## Findings and Adjudication

| # | Finding | Adjudication |
|---|---|---|
| T1 | The responsibilities of the two gating layers are clearly separated: ① the deployment-level master toggle (PG version store, hot reload) ② runtime fine-grained overrides (Redis, idempotent verdicts) | Accept: there is both a master switch that can converge in one action and canary granularity |
| T2 | It makes "off by default" and the "removal condition" explicit (to prevent toggle debt), and requires every feature to be adjudicated explicitly in the ADR / HLD | Accept: consistent with AGENT.md §3.4; `ToggleDTO.removal_condition` is implemented as **required** (no default value) |
| T3 | Toggles only enable and disable capabilities and do not change the interface contract; the off state goes through the existing default path | Accept: avoids an external behavior branch for the "off state" |
| T4 | Runtime verdicts must be idempotent in order to withstand the Redis split-brain window (risk R5 / undecided D3) | Accept: covered by the pure-function verdict of `is_enabled` and by tests for both states |
| T5 | Consistent with ADR-0006: a toggle travels the same change pipeline as a class of configuration version and does not open a separate channel | Accept: already implemented — `ConfigBundle.toggles` and `toggle_deployment()`, with a test covering "a toggle follows the change ticket through approval → distribution → rollback" |
| T6 | Undecided D7 (the verdict granularity and configuration schema for runtime overrides: number range / call / user / percentage) is still undefined | Accept as a **known gap**: must be decided before M4 completes, otherwise runtime overrides cannot be made configuration-driven |
| T7 | Runtime overrides currently have only a seam (`StaticToggleSource`); the Redis-side implementation has not been written | Accept as a **known gap**: to be completed in sync with the runtime storage wiring of ADR-0007 (around M5) |

## Adjudication Summary

| Category | Count | Disposition |
|---|---|---|
| Accepted with no changes needed | 5 (T1-T5) | — |
| Accepted as known gaps | 2 (T6, T7) | D7 to be decided before M4 completes; the Redis-side implementation is in sync with the ADR-0007 wiring |
| Changes required | 0 | — |

## Sign-off

| Item | Value |
|---|---|
| Review conclusion | Pass |
| State transition | `draft` → `accepted`; registry synchronized |
| Reviewer | AI agent, 2026-09-28 |
| Maintainer sign-off | To be filled in |
