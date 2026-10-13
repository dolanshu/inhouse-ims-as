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

# M2a Kernel Code Review Record

> Review object: `platform/src/as_platform/` (decision / state / gating / telemetry / shell / api) and the six new test files under `platform/tests/`
> Review date: 2026-09-28
> Reviewer: AI agent (actually ran the gate + structure guards + reverse-dependency checks)
> Review verdict: **pass** — gate fully green; 6 implementation decisions confirmed, 4 gaps carried forward

## Gate evidence (actually run locally on 2026-09-28)

| Item | Result |
|---|---|
| `uv run ruff format --check .` | 95 files already formatted |
| `uv run ruff check .` | All checks passed! |
| `uv run mypy` | Success: no issues found in 19 source files |
| `uv run pytest -m "unit or contract" -q` | **114 passed**, 0 skipped |
| Structure guards (`platform/tests/test_library_independence.py` + `tests/`) | 56 passed |
| Kernel reverse dependencies (grep `as_platform` → apps/services/testbed) | None |

## Review findings

| # | Finding | Adjudication |
|---|---|---|
| C1 | The TDD order was really followed: the six test files were landed first and run red (collection error: module does not exist), then the implementation was driven to green | Accepted (AGENT.md §6 mandates TDD at the decision layer) |
| C2 | `decide()` purity: `received_at` is injected by the caller; there is no socket / clock / global state inside the module | Accepted (AGENT.md §5) |
| C3 | Conflict adjudication uses the sort key `(action_rank, len(prefix))` in descending order (BLOCK=2 > TRANSLATE=1 > FORWARD=0) | Accepted: consistent with test-plan §5.1 use case 7; the side effect "a shorter block overrides a longer translate" has a dedicated test |
| C4 | `RedisStateStore.get()` narrows `bytes \| str \| None` → `bytes \| None` with `isinstance`, without `# type: ignore` | Accepted: genuine type narrowing, compliant with mypy strict |
| C5 | After the redis dependency `redis>=5.0` (locks at 8.1.0), the 9 Redis contract use cases went from skipped to **genuinely executed** (105+9 → 114 passed) | Accepted: the contract is replayed against both implementations, consistent with test-plan §5.2 |
| C6 | The namespace defaults to `as` (rather than the LLD draft's `as:default`), producing keys `as:{case}:{kind}:{id}` | Accepted: the verifiable key format is authoritative (ADR-0007, test-plan §5.2 use case 6) |
| C7 | The rule-layer `Action` (forward/translate/block) and the decision-layer `DecisionAction` (including decline/not_found) are split into two enums | Accepted: rules express "configured intent", decisions express "protocol result", and `decide()` translates between them |
| C8 | When a rule does not specify it, the `FORWARD` target falls back to the normalized called number | Accepted: aligned with LLD §3 |
| C9 | `ShellConfig` gains `poll_interval_seconds` (additive only), and draining advances via an injected clock | Accepted: makes draining deterministically testable |
| C10 | No module names such as `util` / `helper` / `misc` / `common` / `tools` are seen under `platform/src/as_platform/` | Accepted (AGENT.md §5) |

## Gaps (non-blocking for M2a)

| # | Gap | Destination |
|---|---|---|
| C11 | TLS transport and SIP adapter are not implemented (binding reSIProcate) | M2b |
| C12 | `CallState` is not landed (StateStore only provides generic primitives) | M3 |
| C13 | No `integration` / `e2e` layer use cases; these two layers remain non-blocking | Become blocking when M2b / M3 introduce them |
| C14 | ADR-0020 (gating) is still draft; the gating seam is based on it | Review must complete before the M4 control plane |

## Confirmation sign-off

| Item | Value |
|---|---|
| Review verdict | Pass |
| Gate | Fully green (114 passed / 0 skipped) |
| Reviewer | AI agent, 2026-09-28 |
| Maintainer signature | To be filled in |
