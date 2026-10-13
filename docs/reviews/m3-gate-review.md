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

# M3 Gate Review Record

> Review object: M3 — applications (decision modules and contract replay). Scope covers the decision modules and tests of `apps/translation` and `apps/anti-fraud`, plus the `testbed/contracts/decision/` contract case set
> Review date: 2026-09-28
> Reviewer: AI agent (actually ran the gate + cross-checked plan.md §4 M3 gate, AGENT.md §4/§5/§6)
> Review verdict: **pass** — the M3 gate is met, and M3 is judged complete

## Gate checklist

| Gate item | Status | Evidence |
|---|---|---|
| Decision modules of `apps/translation` and `apps/anti-fraud` | Met | `as_translation/decision.py` (132 lines) and `as_anti_fraud/decision.py` (158 lines), both built on top of the kernel `decide()` |
| Decision modules follow TDD first | Met | Both modules went red first (`ModuleNotFoundError`), then green; translation 10 cases, anti-fraud 14 cases (marker `unit`) |
| The contract case set replays green against both | Met | 14 cases in `testbed/contracts/decision/cases.json`; `apps/translation/tests/test_contract_replay.py` and `apps/anti-fraud/tests/test_contract_replay.py` each replay them, marker `contract`, 21 cases passing in total (19 parameterized replays + 2 anti-false-green guards) |

## Gate evidence

| Item | Result |
|---|---|
| `uv run ruff format --check .` | 116 files already formatted |
| `uv run ruff check .` | All checks passed! |
| `uv run mypy` | Success: no issues found in 25 source files |
| `uv run pytest -m "unit or contract" -q` | 190 passed, 2 skipped |
| `uv run pytest -m contract -q` | 49 passed, 2 skipped |
| `uv run pytest -m integration -q` | 3 passed |

## Review findings

| # | Finding | Adjudication |
|---|---|---|
| G1 | The contract case set is declarative JSON plus README, independent of implementation language; cases carry `applies_to` to distinguish the two apps | Accepted: consistent with AGENT.md §6 "contracts = declarative cases, replayed against every implementation" |
| G2 | The baseline translation fact (`+8613800138000` → `013800138000`) is tagged `translation` only, not `both` | Accepted: under the same input translation rewrites the target while anti-fraud explicitly does not rewrite (target is null), so the semantics are inherently mutually exclusive; shared semantics are already expressed with `both` (block precedence, no match, longest prefix, separator carries no semantics) |
| G3 | Each of the two replay tests carries a guard asserting "this test hits at least some contract cases", preventing an empty green caused by a filter mismatch | Accepted: it guards against silent false green |
| G4 | Contract expected values are hand-computed from the kernel winning rule `(action_rank, prefix_length)` and only then verified by the replay; the data was not changed in order to pass | Accepted |
| G5 | In the same period the first `integration` layer use case was introduced (telemetry export over a real socket), and layer ② was switched to blocking | Accepted: AGENT.md §9 requires the milestone that first introduces that layer to switch it to blocking in the same step; layers ③ e2e and ④ performance still have no use cases and keep their previous status |

## Leftovers (non-blocking for M3)

| # | Leftover | Destination |
|---|---|---|
| G6 | The rate-window counter is still not wired to StateStore (sliding window, TTL, split-brain idempotency) | Later M3 work / depends on the undecided D3 |
| G7 | The `e2e` layer still has zero use cases | The milestone with the first e2e use case, which switches layer ③ to blocking |
| G8 | The test directory structure under the two members is asymmetric (`apps/anti-fraud/tests/` has `__init__.py`, translation does not), stemming from the collection conflict of same-named `test_decision.py` | Recommended future standardization: set `importmode = "importlib"` in the root pyproject, or use non-colliding filenames inside each member |

## Confirmation sign-off

| Item | Value |
|---|---|
| Review verdict | Pass, M3 judged complete |
| Gate | Met (190 passed / 2 skipped; contract 49 passed; integration 3 passed) |
| Reviewer | AI agent, 2026-09-28 |
| Maintainer signature | To be filled in |
