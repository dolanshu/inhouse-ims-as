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

# M3 Decision Module Review Record (translation / anti-fraud)

> Review object: `apps/translation/src/as_translation/decision.py` and its tests; `apps/anti-fraud/src/as_anti_fraud/decision.py` and its tests
> Review date: 2026-09-28
> Reviewer: AI agent (actually ran the gate + cross-checked AGENT.md §4/§5, ADR-0002/0016, baseline facts)
> Review verdict: **pass** — both modules are built on top of the kernel; 1 structural deviation is confirmed acceptable

## Gate evidence

| Item | Result |
|---|---|
| `uv run ruff format --check .` | 111 files already formatted |
| `uv run ruff check .` | All checks passed! |
| `uv run mypy` | Success: no issues found in 25 source files |
| `uv run pytest -m "unit or contract" -q` | 169 passed, 2 skipped |
| TDD | Both modules went red first (`ModuleNotFoundError`), then green |

## Review findings

| # | Finding | Adjudication |
|---|---|---|
| M1 | The verdicts of both modules use the kernel `decide()` as their only entry point, layering use-case semantics only on top of the kernel verdict | Accepted: the M2 gate claim "use cases can be built on top of it without touching sippy" is empirically substantiated, and matching/priority is not re-implemented |
| M2 | The translation assertion `+8613800138000 → 013800138000` comes from the already-captured baseline S1 and rule R-MOB-CM-40, not from invention | Accepted: it freezes a fact derived from the baseline into a use-case-layer assertion |
| M3 | anti-fraud uses an independent `RATE_LIMIT` reason, distinct from the kernel `MATCH_BLOCK`; and it explicitly does not rewrite the number (translation belongs to the translation use case) | Accepted: use-case responsibilities do not encroach on each other |
| M4 | The rate-window counter is injected by the caller (`Mapping[str, int]`); the module does not read the clock and opens no socket | Accepted: keeps the decision module a pure function (AGENT.md §5); window semantics are carried by StateStore (ADR-0002) |
| M5 | The over-limit determination uses `>=` rather than `>`, and this is explained in the docstring | Accepted: the boundary semantics are correct (using `>` would let one extra call through) |
| M6 | anti-fraud performs rate screening only after `FORWARD` / `TRANSLATE` | Accepted: calls already rejected by the kernel should not consume window budget, otherwise the window could be exhausted by abuse |
| M7 | Two members have same-named `test_decision.py`, causing a pytest collection conflict; the fix was to add `__init__.py` to `apps/anti-fraud/tests/` | Accepted: lowest cost without changing the root `pyproject.toml` import mode and without touching other members; **leftover**: it is recommended to later standardize on `importmode = "importlib"`, or use distinct test filenames inside each member |
| M8 | Neither imports across apps (no `as_translation` ↔ `as_anti_fraud`), and there is no `# type: ignore` / `# noqa` | Accepted (AGENT.md §4) |

## Gaps (non-blocking)

| # | Gap | Destination |
|---|---|---|
| M9 | How the counter is written to / read from StateStore (window sliding, TTL, split-brain idempotency) is not wired up yet | Later M3 work (the wiring layer), depends on the undecided D3 |
| M10 | Neither use case yet has a `contract`-layer replay (replaying the contract case set against both is an M3 gate) | M3 wrap-up |
| M11 | No `integration` / `e2e` layer use cases | The milestone with the first use case in that layer, which switches layers ②③ to blocking |

## Confirmation sign-off

| Item | Value |
|---|---|
| Review verdict | Pass |
| Gate | Fully green (169 passed / 2 skipped) |
| Reviewer | AI agent, 2026-09-28 |
| Maintainer signature | To be filled in |
