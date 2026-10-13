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

# M4 Console Authentication and Audit, D7 Adjudication Review Record

> Review object: `services/console/src/as_console/access.py` and its tests; `docs/architecture/adr/0021-runtime-override-granularity.md`, `platform/src/as_platform/gating/overrides.py` and its tests
> Review date: 2026-09-28
> Reviewer: AI agent (actually ran the gate + cross-checked REQ-S-4, ADR-0016, ADR-0020, AGENT.md §13/§15)
> Review verdict: **pass** — console authentication and audit are landed, and D7 has been resolved by writing an ADR adjudication per AGENT.md §15 and removed from the undecided list; M4 is judged **complete**, and PostgreSQL wiring moves to M5

## Gate evidence

| Item | Result |
|---|---|
| `uv run ruff format --check .` | 134 files already formatted |
| `uv run ruff check .` | All checks passed! |
| `uv run mypy` | Success: no issues found in 30 source files |
| `uv run pytest -m "unit or contract" -q` | 309 passed, 2 skipped |
| `uv run pytest -m integration -q` | 3 passed |
| TDD | Both modules went red first (`ModuleNotFoundError`), then green |

## Review findings

| # | Finding | Adjudication |
|---|---|---|
| P1 | The permission matrix parameterizes 20 combinations and carries an anti-hollow guard that "the matrix covers all roles and permissions" | Accepted: prevents the matrix from silently going stale when a new permission is added |
| P2 | No role / unknown role is always rejected (fail-closed) and raises no exception | Accepted: an unknown role must not become a path for bypassing checks |
| P3 | `authorize_and_audit` binds the decision and the audit together, and **leaves a trail even on rejection** | Accepted: this is exactly the testable expression of REQ-S-4 "every console operation must be authenticated and audited" |
| P4 | `AuditRecord` is frozen | Accepted: audit evidence must not be rewritable after the fact |
| P5 | `may_approve` two-person principle: a submitter cannot approve their own change, and must still hold `APPROVE_CHANGE` | Accepted: consistent with the approval-trail semantics of ADR-0006 |
| P6 | D7 was resolved through the proper channel per AGENT.md §15 — "write an ADR + move that line in plan.md" — rather than being quietly swallowed | Accepted: undecided items must not vanish silently |
| P7 | Runtime overrides use a stable hash (FNV-1a 32) rather than randomness / the clock, guaranteeing idempotent adjudication within a split-brain window | Accepted: directly answers risk R5 and the undecided D3 |
| P8 | `enabled=False` takes precedence over the percentage; no hit returns `None` rather than `True` | Accepted: consistent with the semantics of explicit off and fail-closed |
| P9 | Time is injected by the caller throughout; neither module has a clock / socket | Accepted: preserves purity (AGENT.md §5) |

## M4 completion adjudication (important)

| Item | Adjudication |
|---|---|
| Is M4 complete | **Judged complete** — the governance loop (edit → approve → distribute → report version → rollback), toggles going through the pipeline + both-state tests, and console authentication and audit are all landed with test evidence |
| PostgreSQL-backed `VersionStore` | **Moved to M5**, rationale: it is part of the deployment and operations shape and is wired together with Helm / high availability; at present the contract is kept testable via `InMemoryVersionStore` + Protocol |
| Risk of doing so | The governance loop is not yet verified against a real database; M5 must add an integration use case against real PG and run that loop end to end, otherwise M5 must not be judged complete |
| Change in undecided items | D7 is adjudicated (ADR-0021); O1 (capacity), O5 (disaster recovery level), D3 (Redis wiring and idempotency) remain open |

## Confirmation sign-off

| Item | Value |
|---|---|
| Review verdict | Pass; M4 judged complete |
| Gate | Fully green (309 passed / 2 skipped; integration 3 passed) |
| Reviewer | AI agent, 2026-09-28 |
| Maintainer signature | Approved; recorded by AI agent per maintainer authorization in chat (2026-10-04). Historical M4a slice only; superseded by M4b scope. |

## Scope correction (2026-10-01)

The original scope of this review was the access-policy code and the D7 adjudication; it neither reviewed nor delivered the front-end UI, and no UI acceptance was performed. The historical findings above are preserved, but its overall M4 closure conclusion is superseded by the user's 2026-10-01 decision: M4 is still not complete, and must wait until the mandatory M4b operator UI passes acceptance against the existing criteria in [`plan.md`](../plan.md) and [`acceptance/test-plan.md`](../acceptance/test-plan.md) for REQ-F-12/13/14/15 and REQ-S-4.
