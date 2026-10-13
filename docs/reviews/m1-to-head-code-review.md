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

# M1 to HEAD code review record

> Review target: `d63cfb70b5b917a6575af1d271b3bef2efd600a1` to `cbbd2eccc4025367147fa1c6eb64c01dc80d1371` (`git diff d63cfb7...HEAD`; 48 commits, 203 changed files)
> Review date: 2026-09-30
> Reviewer: AI agent
> Specification basis: `docs/plan.md`
> Review conclusion: **pending adjudication** — this record retains findings on both the Standards and Spec axes and renders no pass/fail verdict.

## Standards

| # | Severity | Finding and evidence |
|---|---|---|
| 1 | [blocking] | Chinese code comments, logs and error messages in `testbed/simulators/resip-probe/resip_probe.cxx` violate the committed `AGENT.md` §5 "language of artifacts: English" requirement. Evidence: lines 1, 428, 467 of the file. |
| 2 | [blocking] | `ProbeInviteHandler::onConnected` performs the blocking call `std::this_thread::sleep_for(std::chrono::milliseconds(200))`, violating the `AGENT.md` §5 requirement that blocking operations must not be performed in SIP callbacks. Evidence: `testbed/simulators/resip-probe/resip_probe.cxx:250`. |
| 3 | [suggestion, judgement call: Duplicated Code] | Duplicated `max` selection logic for the longest-prefix candidate: `apps/anti-fraud/src/as_anti_fraud/decision.py:90` and `apps/translation/src/as_translation/decision.py:96` both use `return max(candidates, key=lambda candidate: candidate[0])[1]`. |
| 4 | [suggestion, judgement call: Duplicated Code] | Duplicated import, `ImportError` guidance and `SystemExit` logic in `_load_bindings`: `testbed/probe/e1_baseline_probe.py:267` and `testbed/probe/tls_hot_rotation_probe.py:144`. |

Tool-enforced checks such as formatting, lint and typing are not reported again.

## Spec

| # | Severity | Finding and evidence |
|---|---|---|
| 1 | [important] | M5 requires "no call loss during scale-down" (`docs/plan.md:120`), but the scale-down protection only yields a verdict and is not wired into the execution path: the guard lives at `platform/src/as_platform/ops/downscale_guard.py:19,91`; the HPA targets the Deployment directly, see `deploy/helm/templates/hpa.yaml:38,40`; `plan_scale_down` has no usage point outside the runtime guard module. |
| 2 | [important] | M5 requires "no call loss during rolling upgrade" (`docs/plan.md:120`), but the process entry point injects `active_calls=lambda: 0`, decoupling the drain-completion verdict from real in-flight calls. Evidence: `platform/src/as_platform/__main__.py:78`. |
| 3 | [praise] | The plan transparently records that M5 is still in progress and states that real-cluster rolling upgrade and scale-down verification are not yet complete. Evidence: `docs/plan.md:120`. |
| 4 | Scope check | No behaviourally meaningful scope creep was found. |

## Current status and confirmation sign-off

| Item | Status |
|---|---|
| Finding adjudication | pending adjudication |
| Fixes | not applied |
| Maintainer sign-off | pending |
| Out of review scope | Setup changes to `AGENT.md` and `docs/agents/` in the current working tree are outside the scope of this review |

## Per-axis summary

| Review axis | Record summary |
|---|---|
| Standards | 4 items: 2 × [blocking], 2 × [suggestion] (both are judgement calls). |
| Spec | 4 items: 2 × [important], 1 × [praise], 1 scope check (no behaviourally meaningful scope creep found). |
| Most severe Standards finding | The most severe issues on this axis are the two [blocking] findings on the SIP probe: non-English comments, logs and error text, plus the blocking sleep inside a SIP callback. |
| Most severe Spec finding | The most severe issue on this axis is that the M5 call-preservation acceptance is unmet/incomplete: the scale-down protection is not wired into the execution path, and the runtime drain counter is hard-coded to zero. |

None of the findings above have been adjudicated, no fixes have been applied, and maintainer sign-off is pending.
