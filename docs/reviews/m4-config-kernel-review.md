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

# M4 Configuration Governance Kernel Review Record

> Review object: `services/config-service/src/as_config_service/` (`change_order.py`, `version_store.py`, `distributor.py`), the toggle-contract extension in `platform/src/as_platform/api/contract.py`, and their tests
> Review date: 2026-09-28
> Reviewer: AI agent (actually ran the gate + cross-checked ADR-0006, ADR-0020, AGENT.md §3.4/§5)
> Review verdict: **pass (phased)** — the governance logic loop is closed; PostgreSQL wiring and the console have not started, so M4 is not judged complete

## Gate evidence

| Item | Result |
|---|---|
| `uv run ruff format --check .` | 127 files already formatted |
| `uv run ruff check .` | All checks passed! |
| `uv run mypy` | Success: no issues found in 28 source files |
| `uv run pytest -m "unit or contract" -q` | 254 passed, 2 skipped |
| `uv run pytest -m integration -q` | 3 passed |
| TDD | All three modules went red first (`ModuleNotFoundError` / `ImportError`), then green |

## Review findings

| # | Finding | Adjudication |
|---|---|---|
| N1 | The change-order state machine is a pure function; illegal transitions raise `IllegalTransitionError` (including `DRAFT → APPLIED`), and approval must always record the approver and the time | Accepted: the state-machine semantics of REQ-F-14 and ADR-0006 are landed |
| N2 | The version store is immutable-append, and historical versions are read-only; the PG implementation leaves a seam unimplemented | Accepted: ADR-0006 / ADR-0007 require immutable version rows; PG wiring is listed as a remaining M4 item |
| N3 | Distribution rolls back immediately and stops advancing subsequent batches whenever "any instance is unhealthy" | Accepted: the blast radius is locked to the current batch, which is exactly the point of canarying |
| N4 | `rollback_target` is `version - 1`, and the first version returns `None` when there is no rollback target | Accepted: the boundary is explicit and has tests |
| N5 | Toggles enter `ConfigBundle`, belong to the same version as rules, and go through the same pipeline; `ToggleDTO.removal_condition` has **no default value** | Accepted: prevents toggle debt (ADR-0020 / AGENT.md §3.4); giving it no default is correct |
| N6 | `toggle_deployment` retains `False` and does not filter out "off" | Accepted: filtering would make "off" be misread as "not configured", and would also leave stale values behind on rollback |
| N7 | Both toggle states have tests (7 kernel contract cases + 7 pipeline cases) | Accepted: AGENT.md §6 requires covering both states |
| N8 | `ConfigBundle.toggles` carries a default, and neither existing construction styles nor existing config-service tests were affected (254 = 240 + 14, 2 skipped unchanged) | Accepted: backward compatibility is already verified by the gate |
| N9 | Two implementation deviations: the `now` of `InMemoryVersionStore.append` was relaxed to optional; `Distribution` has two extra default fields | Accepted: otherwise the injected clock and reason/now have nowhere to go; both are default parameters and do not break callers |

## Remaining (M4 not done)

| # | Remaining item | Explanation |
|---|---|---|
| N10 | PostgreSQL-backed `VersionStore` implementation | Requires real PG; recommended to introduce it together with integration-layer use cases (that layer has already been switched to blocking) |
| N11 | `services/console` (read/write, authentication, audit, REQ-S-4) | The other half of M4, not yet started |
| N12 | `ConfigVersion.change_id` currently permits `None` | The production write path must enforce non-null, borne by the PG implementation or an upper-layer service; pending adjudication |
| N13 | ADR-0020 is still draft | The basis of the toggle pipeline; it must be reviewed and promoted before M4 completion |

## Confirmation sign-off

| Item | Value |
|---|---|
| Review verdict | Pass (phased); M4 not judged complete |
| Gate | Fully green (254 passed / 2 skipped; integration 3 passed) |
| Reviewer | AI agent, 2026-09-28 |
| Maintainer signature | Approved; recorded by AI agent per maintainer authorization in chat (2026-10-04). Historical M4a slice only. |
