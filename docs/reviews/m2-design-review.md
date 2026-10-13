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

# M2 Design Review Record (HLD / LLD)

> Review object: `docs/architecture/hld.md`, `docs/architecture/lld.md` (created 2026-09-28)
> Review date: 2026-09-28
> Reviewer: AI agent (cross-checked against the implementation, test-plan §5, AGENT.md §5, and accepted ADR-0002/0003/0005/0007/0016/0019)
> Review verdict: **conditional pass** — 3 signature drifts were corrected back into the LLD per "code is authoritative"; 3 gaps are carried into later milestones

## Review method

| Dimension | Method |
|---|---|
| Consistency with requirements | Item by item against `docs/acceptance/test-plan.md` §5 (M2 kernel acceptance) |
| Consistency with ADRs | ADR-0002 / 0003 / 0005 / 0007 / 0016 / 0019 / 0020 |
| Consistency with the implementation | Item by item against the landed code under `platform/src/as_platform/` (signature drifts found) |
| Consistency with coding conventions | `AGENT.md` §5 (pure functions, type annotations, forbidden module names, ADR annotations) |

## Findings and adjudication

| # | Finding | Adjudication | Status |
|---|---|---|---|
| D1 | The LLD §5 gating signature `is_enabled(source, name, scope)` is inconsistent with the implementation `is_enabled(name, scope, source)`; a single `value()` on `ToggleSource` cannot express the two-level source "deployment-level / runtime-state" | Correct the LLD back per **code is authoritative**: two methods `deployment_value` / `runtime_override` | Modified |
| D2 | LLD §4 `build_key(..., id)` uses the builtin name `id`, triggering ruff A002; the implementation uses `entity_id` | Correct the LLD back per code is authoritative | Modified |
| D3 | LLD §6 writes the telemetry drop counter as `dropped`, while the implementation exposes `dropped_count` / `export_failure_count` | Correct the LLD back per code is authoritative | Modified |
| D4 | HLD §7.3 adjudicates "M2 only lands the gating seam and introduces no new toggle"; the implementation is consistent (no new toggle was introduced) | Accepted; avoids toggle debt | Confirmed |
| D5 | LLD §2 defines `CallState`, which M2a did not implement (StateStore is a generic key-value store) | Accepted as a gap: CallState is landed by the use-case layer in M3, while the kernel only provides storage primitives | Pending M3 |
| D6 | The HLD §3 module view includes the SIP adapter and TLS transport (M2b), which the code does not implement | Accepted: consistent with the M2a / M2b split in HLD §1.2 | Pending M2b |
| D7 | The HLD §8 REQ/ADR traceability table covers 17 REQs, but REQ-S-4 (console authentication) falls in M4 | Accepted; ownership already declared in the HLD §1.3 non-goals and ADR-0016 | Pending M4 |
| D8 | ADR-0020, the basis of the gating implementation, is still draft | Accepted as a **dependency gap**: does not block M2a (seam only), but the ADR-0020 review must be completed before the M4 control plane lands | Pending review |

## Adjudication summary

| Category | Count | Disposition |
|---|---|---|
| Signature drifts (docs corrected back per code is authoritative) | 3 (D1-D3) | LLD updated |
| Confirmed consistent | 1 (D4) | — |
| Accepted as gaps | 4 (D5-D8) | Routed respectively to M3 / M2b / M4 / ADR review |

## Confirmation sign-off

| Item | Value |
|---|---|
| Review verdict | Conditional pass |
| Status transition | hld.md / lld.md: `draft` → `reviewed` |
| Reviewer | AI agent, 2026-09-28 |
| Maintainer signature | To be filled in |
