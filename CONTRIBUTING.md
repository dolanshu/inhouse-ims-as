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

# Contributing

## Before you start

Read in this order:

1. [`AGENT.md`](AGENT.md) — the rules. Binding on both humans and agents.
2. [`docs/README.md`](docs/README.md) — where the documentation lives.
3. [`docs/plan.md`](docs/plan.md) — which milestone is running, and which are still open.

## Environment

```bash
uv sync            # resolve and lock the whole workspace
make gate          # pre-commit gate, order per the gate table below, layer ①
```

- Python **3.10**, pinned by `.python-version`: this is the version sippy was validated against. Before changing it, read `docs/plan.md` D1.
- `uv` manages everything. Do not use pip inside the workspace.
- Commit `uv.lock` to the repository. If `uv sync` rewrites it, commit it together with the change that caused it.

## The gate

`make gate` has four fixed steps (AGENT.md §9): `ruff format --check` → `ruff check` → `mypy` → pytest (unit/contract layers). AST scanning is **not** inside `make gate`; `make gate-strict` = the four gate steps + AST scanning (`scripts/check_adr_annotations.py`, REQ-G-3, ADR-0015).

| Layer | Command | Blocking |
|---|---|---|
| ① fast | `make test-unit` + `chart-check` + `gate-strict` scan | Blocking |
| ② integration | `make test-integration` | Blocking |
| ③ e2e | `make test-e2e` | Non-blocking (0 cases; the milestone that introduces the first e2e case must make it blocking, ADR-0015) |
| ④ performance | `make test-perf` | Blocking once run (cases exist since M6) |

Nothing may be committed while the local gate is red. Never present a local re-run as external proof that the gate has passed.

## Adding a workspace member

1. Create `<dir>/pyproject.toml` with `[project]`, `[build-system]`, and
   `[tool.hatch.build.targets.wheel] packages = ["src/<package>"]`.
2. Create `src/<package>/__init__.py` stating the module's responsibility.
3. Add the directory to the root `pyproject.toml`'s `[tool.uv.workspace].members`.
4. Add its `src/` to `[tool.ruff].src`.
5. Add its `src/` to `[tool.mypy].files` and `mypy_path`.
6. If it is not the core, add its import root to `FORBIDDEN_ROOTS` in
   `src/platform/tests/test_library_independence.py`.

Steps 3–6 are asserted by guards in `tests/`; you cannot quietly skip them.

**Do not** add `[tool.pytest]`, `[tool.ruff]`, or `[tool.mypy]` tables to a member. Tool configuration has a single home: the workspace root.

## Commits

- Conventional Commits, in English, one logical change per commit:
  `feat` · `fix` · `docs` · `refactor` · `test` · `chore` · `build`.
- Do not skip hooks. If a hook blocks a commit, fix the cause.
- Never commit keys, certificates, or real traffic captures.
- Agents do not push, create branches, or create tags.

## Reviews

- PRs that adopted POC code must reference the corresponding triage line in [`docs/migration/triage.md`](docs/migration/triage.md).
- PRs carrying non-obvious design decisions must bring their ADR along.
- PRs containing AI-generated work must be labeled as such.

## Cross-platform note

The `mypy_path` in the root `pyproject.toml` uses the POSIX `:` separator. On Windows, use the `MYPYPATH` environment variable instead; this build targets Linux.
