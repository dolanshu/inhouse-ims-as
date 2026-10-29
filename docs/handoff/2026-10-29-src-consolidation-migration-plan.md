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

# src/ Consolidation Migration Plan (R2612 E3 — survey only, nothing moved)

> **Status: migration checklist produced for maintainer approval. Per R2612_Struct_Plan.md §6 Q6=B
> and §7 E3, this document is the first step of the `src/` consolidation decision; the actual
> directory moves are NOT executed in this batch.** Execution requires explicit maintainer
> approval of this checklist. No directory was moved, no code was changed, and no git write
> operation (`commit` / `push` / `tag` / branch) was performed to produce this document.
>
> Evidence collection: 2026-10-29, branch `R2612`, from direct inspection of tracked files
> (`git grep` over the index) and line-level reads of every file cited below. The working tree
> at survey time also contains the uncommitted E1/E2 batch changes described in
> R2612_Struct_Plan.md §7.

## 0. Decision being executed

The maintainer ruled (R2612_Struct_Plan.md §6, 2026-10-29):

> Q6=B — introduce a root `src/` that consolidates the product source tree
> (PostgreSQL-style "product vs. support" visual split), producing a migration checklist
> first; the checklist is executed only after maintainer approval.

Scope: move the three product source directories one level down. Everything else stays.

## 1. Old → new path mapping (complete)

| Old path (repo root) | New path | Moves? | Notes |
|---|---|---|---|
| `platform/` | `src/platform/` | yes | kernel: `src/as_platform`, `native/`, `tests/` move as one unit |
| `apps/` | `src/apps/` | yes | `translation/`, `anti-fraud/`, `README.md` (E2) |
| `services/` | `src/services/` | yes | `config-service/`, `console/`, `README.md` |
| `testbed/` | `testbed/` | **no** | stays at root (contracts, simulators, load, probe, sim-platform) |
| `tests/` | `tests/` | **no** | cross-cutting guards stay at root |
| `deploy/` | `deploy/` | **no** | helm / docker / compose / kind / alerts |
| `docs/` | `docs/` | **no** | |
| `scripts/` | `scripts/` | **no** | |
| `tools/` | `tools/` | **no** | bin/ untracked, bootstrap, env-probe, VERSIONS |

Workspace members before/after (8 members, count unchanged):

| Member path today | Member path after |
|---|---|
| `platform` | `src/platform` |
| `apps/translation` | `src/apps/translation` |
| `apps/anti-fraud` | `src/apps/anti-fraud` |
| `services/config-service` | `src/services/config-service` |
| `services/console` | `src/services/console` |
| `testbed/simulators` | `testbed/simulators` (unchanged) |
| `testbed/load` | `testbed/load` (unchanged) |
| `testbed/probe` | `testbed/probe` (unchanged) |

Import roots (`as_platform`, `as_translation`, `as_anti_fraud`, `as_config_service`,
`as_console`, `as_simulators`, `as_load`, `as_probe`) are distribution/package names —
**none of them change**. Every member keeps its internal `src/<package>` hatch layout;
`[tool.uv.sources]` entries are name-based (`workspace = true`), not path-based, so member
`pyproject.toml` files need **no** changes.

## 2. Reference inventory

The pattern used for the sweep is `(^|[^-._a-zA-Z0-9/"])(platform|apps|services)/` plus
manual reads of every executable reference. Total across the tracked tree: **≈1270
occurrences in ≈150 files**. The split below separates what must be synchronized from what
must be preserved as history.

### 2.1 uv workspace and toolchain (root `pyproject.toml`)

Every key that needs editing, with exact line references:

| Key | Lines today | Change |
|---|---|---|
| `[tool.uv.workspace].members` | 33–42 | 5 of 8 entries get `src/` prefix (`"platform"` → `"src/platform"`, `"apps/translation"` → `"src/apps/translation"`, `"apps/anti-fraud"` → `"src/apps/anti-fraud"`, `"services/config-service"` → `"src/services/config-service"`, `"services/console"` → `"src/services/console"`); 3 `testbed/*` entries stay |
| `[tool.pytest.ini_options].testpaths` | 59 | `["tests", "platform", "apps", "services", "testbed"]` → `["tests", "src/platform", "src/apps", "src/services", "testbed"]` |
| `[tool.ruff].src` | 77–86 | 5 product entries get `src/` prefix (`platform/src` → `src/platform/src`, etc.); 3 `testbed/*` entries stay |
| `[tool.ruff].extend-exclude` | 87–93 | **no product entries — unchanged** (`testbed/simulators/resip-probe/research` stays) |
| `[tool.mypy].files` | 131–140 | 5 product entries get `src/` prefix; 3 `testbed/*` entries stay |
| `[tool.mypy].mypy_path` | 141 | colon-joined 8 roots; 5 segments change (`platform/src:…` → `src/platform/src:…`) |

`uv.lock`: contains **16 editable-source path references** (lines 60–155 of `uv.lock`,
e.g. `source = { editable = "apps/anti-fraud" }`, `editable = "platform"`, and the
`requires-dist` cross-references). Regeneration: run `uv lock` (or `uv sync`) immediately
after the manifest edit — see §3 step 3 and the risk in §5.

### 2.2 Gate tests (`tests/`, kernel-side guard, moved tests)

`tests/test_workspace_layout.py` — **no code change needed.** It reads member paths from
the root manifest and joins them onto `REPOSITORY_ROOT` (L32, `parents[1]`; `tests/` stays
at root, depth unchanged). `packages[0].startswith("src/")` (L93) checks member-internal
layout and is unaffected.

`tests/test_layer_boundaries.py` — **must change.** Classification is by member-path
prefix:

- L113: `if member_path == "platform": return "kernel"` → must match `src/platform`;
- L115–117: `first = member_path.split("/", 1)[0]` and `first in {"apps", "services", "testbed"}` → after the move `apps`/`services` members have first segment `src`, so the set and the matching logic must distinguish `src/apps/…`, `src/services/…` (product) from `testbed/…` (unchanged);
- Prose/assertion text that names the prefixes and must be updated for accuracy: L21–24, L35–37, L46, L52–53, L198, L213, L220, L224, L242, L245, L248, L293, L331, L336–342, L356–359 (e.g. the fix hint at L357–359 "place it under platform/, apps/*, services/* or testbed/*").

`platform/tests/test_library_independence.py` (moves to `src/platform/tests/…`) — **must
change, 3 spots**: L37 `REPOSITORY_ROOT = …parents[2]` → `parents[3]` (depth grows by one);
L38 `KERNEL_SOURCE = REPOSITORY_ROOT / "platform" / "src" / "as_platform"` → insert
`"src"` segment; L102 `if member == "platform": continue` → `== "src/platform"`.
`FORBIDDEN_ROOTS` (L43–53) is import-root-based — unchanged.

Repo-root depth fixes inside moved tests (`parents[2]` → `parents[3]`):

| File (new location under `src/`) | Line | What it resolves |
|---|---|---|
| `platform/tests/test_req_s3_overlap_integration.py` | 33 | `testbed/simulators/resip-probe/gen-cert.sh` |
| `platform/tests/test_resip_runtime_tls_integration.py` | 35 | same `gen-cert.sh` |
| `platform/tests/test_resip_runtime_tls_policy_integration.py` | 34 | same `gen-cert.sh` |
| `platform/tests/test_m2_native_probe_smoke.py` | 32 | `_REPO_ROOT` |
| `platform/tests/test_m5_verify_strict.py` | 26 | `repo`, used for `deploy/kind/scripts/m5-lib.sh` + `cwd` |
| `platform/tests/test_e1_contract_resip_runtime_full.py` | 35 | `_BASELINE_ROOT` → `testbed/contracts/sip-baseline` |
| `platform/tests/test_sip_message.py` | 418 | **fallback only**; primary walk-up (L414–417, "pyproject.toml + testbed/" sentinel) is path-agnostic and keeps working — update the fallback depth for correctness |
| `apps/translation/tests/test_contract_replay.py` | 61 | **fallback only**; same walk-up pattern at L57–60 (`_CASES_PATH` at L64 resolves from the walk-up result) |
| `apps/anti-fraud/tests/test_contract_replay.py` | 62 | **fallback only**; same |

**Member-internal relative computations — verified unchanged** (the directory moves as a
unit, so `parents[N]` relative to the member root stays correct):

- `platform/tests/test_d10_process_restart_integration.py` L46, L154 — `parents[1]` = the platform member dir (`…/"src"/"as_platform"/…`, `PYTHONPATH = <member>/src`);
- `platform/src/as_platform/sip/resip_runtime.py` L53, `resip_recovery.py` L28, `resip_two_leg.py` L25 — `parents[3]` = platform member dir → `native/<ext>/build` defaults;
- `services/config-service/src/as_config_service/api.py` L2040 — `parents[3]` = the `services/` parent → `console/web` assets (resolves to `src/services/console/web` after the move; still correct);
- every member's `pyproject.toml` hatch `packages = ["src/<package>"]` — member-internal.

**testbed-side depth computations — verified unchanged** (testbed/ does not move):
`testbed/probe/src/as_probe/e1_baseline_probe.py` L67 and `tls_hot_rotation_probe.py` L61
(`parents[4]`); probe downstream uses at L68–69 / L62 point only into `testbed/`
(`testbed/contracts/sip-baseline`, `testbed/probe/out`);
`testbed/simulators/resip-probe/scripts/m2-native.sh` L22 (`PROBE_ROOT/../../..`);
`testbed/load/scripts/m6-*.sh` (5 scripts, `SCRIPT_DIR/../../..`);
`testbed/simulators/resip-probe/d10-recovery/run.sh` L17 and `orchestrate.py` L34;
`testbed/simulators/tests/test_network_policy.py` L23 (`parents[2]` → sim-platform chart);
`testbed/simulators/tests/test_derived_baseline.py` L81; `testbed/load/tests/*`
(`parents[3]`/`parents[4]`, incl. `test_harness.py` L1208).

### 2.3 Build and deploy

| File | Lines | Change |
|---|---|---|
| `.dockerignore` | 15 | `platform/native/*/build` → `src/platform/native/*/build` |
| `deploy/docker/Dockerfile` | 74–76 | `COPY platform/native/{resip_runtime,resip_two_leg,resip_recovery}` ×3 → `src/platform/…` |
| `deploy/docker/Dockerfile` | 134–138 | `COPY <member>/pyproject.toml <member>/README.md <member>/` for the 5 product members → `src/…` (L139–140 copy `testbed/simulators` + `testbed/load` — stay) |
| `deploy/docker/Dockerfile` | 144 | `COPY platform/src platform/src` → `src/platform/src` |
| `deploy/docker/config-service.Dockerfile` | 10–14 | same 5 product-member pyproject COPY lines → `src/…` |
| `deploy/docker/config-service.Dockerfile` | 20–23 | `COPY platform/src`, `COPY services/config-service/src`, `COPY services/console/src`, `COPY services/console/web` → `src/…` |
| `deploy/compose/compose.yml` | 42–44, 86–88, 103–105 | **no change** — build `context: ../..` (repo root) and `dockerfile: deploy/docker/config-service.Dockerfile` are unaffected; the Dockerfile edits above carry the change. Local images built from these Dockerfiles must be rebuilt after the move |
| `deploy/compose/README.md` | 80 | `uv run --directory services/config-service as-config-migrate` → `src/services/config-service` |
| `deploy/compose/scripts/m4b-8-browser-evidence.sh` | 31 | `uv run --directory "${REPO}/services/config-service" …` → `…/src/services/config-service` |
| `deploy/helm/**` | — | **no filesystem path references.** Only false positives: `apiVersion: apps/v1` (5 template files) and the `services.configService.*` helm-value key namespace (`chart-check.sh` L76–153, `values-product-as.yaml` L53 is testbed-side). Chart stays untouched |
| `Makefile` | 131 | `m71-sim`: `pytest platform/tests/test_udp_retransmission_contract.py …` → `src/platform/tests/…` (other explicit pytest paths in the target are `testbed/*` — stay) |
| `testbed/sim-platform/Dockerfile` | 26–30 | `COPY platform platform`, `COPY apps/translation apps/translation`, `apps/anti-fraud`, `services/config-service`, `services/console` → `src/…` (testbed COPY lines stay) |
| `testbed/sim-platform/Dockerfile.product` | 34–38 | same 5 COPY lines → `src/…` |
| `testbed/sim-platform/kind-up.sh` | 89 | `cp "$ROOT"/platform/native/resip_runtime/build/_resip_runtime*.so …` → `src/platform/native/…` |
| `platform/native/*` CMakeLists | — | **no repo-root-relative paths** — source/build dirs arrive via `cmake -S/-B` and `-DRESIP_HOME/-DRESIP_BUILD` passed by callers; no edit needed |

Makefile targets audited in full: the only product-path reference is `m71-sim` (L131);
`gate`, `gate-native`, `m2-*` targets reach product code through
`testbed/simulators/resip-probe/scripts/m2-native.sh` (path unchanged) and env vars; all
other targets reference `deploy/`, `testbed/`, `scripts/` only.

`testbed/simulators/resip-probe/scripts/m2-native.sh` — script location and `REPO_ROOT`
computation (L22) unchanged, but **6 product path references must change**: L28–30
(`${REPO_ROOT}/platform/native/<ext>/build` defaults for `AS_RESIP_RUNTIME_BUILD` /
`AS_RESIP_TWO_LEG_BUILD` / `AS_RESIP_RECOVERY_BUILD`), L220 / L252 / L284
(`cmake -S "${REPO_ROOT}/platform/native/<ext>"`), L378 and L393
(`pytest platform/tests/test_resip_runtime_{tcp,tls}_integration.py` node ids).

### 2.4 Other code references

`scripts/check_adr_annotations.py` — **two layers of impact, the most easily missed file:**

- L101–108 `_scan_roots()`: hardcodes `root / "platform" / "src"` and iterates
  `("apps", "services")` with `root / member` + `base.glob("*/src")` → must become
  `root / "src" / "platform" / "src"` and `root / "src" / member`;
- L64–93 `GRANDFATHERED`: **26 allowlist keys** of the form
  `"platform/src/as_platform/…:name"` (12) and
  `"services/config-service/src/as_config_service/…:name"` (14) — keys are
  `path.relative_to(root)`, so all must be rewritten to `src/…` prefixes, otherwise the
  scan reports stale-key warnings plus false violations and `make gate-strict` fails.

Demo/harness scripts (pytest node ids and build-dir defaults):

| File | Line(s) | Reference |
|---|---|---|
| `scripts/d10-req-nf1-harness.sh` | 19 | `pytest platform/tests/test_d10_req_nf1_harness_integration.py` |
| `scripts/demo-review/story-a.sh` | 68, 78 | `services/config-service/tests/…` node id; `pytest services/config-service/tests/test_runtime_bundle.py` |
| `scripts/demo-review/story-b.sh` | 45, 50 | `pytest platform/tests/test_e1_contract_resip_runtime_full.py::…`; `pytest apps/anti-fraud/tests/test_decision.py` |
| `scripts/demo-review/story-c.sh` | 97, 113 | `pytest platform/tests/test_health_server.py platform/tests/test_metrics.py`; `pytest platform/tests/test_downscale_guard.py` |
| `scripts/demo-review/story-d.sh` | 66 | `pytest platform/tests/test_d10_req_nf1_redis_integration.py` |
| `scripts/demo-review/lib.sh` | 68 | `${REPO_ROOT}/platform/native/resip_runtime/build` default for `AS_RESIP_RUNTIME_BUILD` |

`tools/` — **clean.** `env-probe.sh`, `bootstrap-infra.sh`, `VERSIONS` contain no
`platform|apps|services` path references (bin/ is untracked by design).
`.gitignore` — clean (only `testbed/sim-platform/.image-native/`, which stays).
`.env.example` L4 — prose comment "所有 apps/ 进程" (1 wording sync).

### 2.5 Documentation references

Areas and volumes (occurrence counts from the sweep pattern; "lines" counts matching
lines):

**Live documents — synchronize paths/trees/diagrams:**

| Area | Files | Occurrences | Notes |
|---|---|---|---|
| `README.md` | 1 | ~11 lines | repo-tour tree L194–208 (`platform/`, `apps/`, `services/` rows), mermaid architecture diagram L56/L58/L59/L60/L62/L65 (subgraph labels + app nodes), L106 `platform/src/as_platform/telemetry/metrics.py`, L210 guard-test path, L214 layering table "Directory" column. Also L181 "8 members" — count stays 8, wording survives |
| `AGENT.md` | 1 | 6 | L131–136 layering diagram + guard-test links (`platform/tests/…`), L140 services-internal-dependency note (`services/config-service`, `services/console` paths). Testbed references (L40/93/154/163/186) unchanged |
| `CONTRIBUTING.md` | 1 | 1 | L58 `platform/tests/test_library_independence.py` link in the add-a-member steps (steps 3–5 describe root-pyproject edits — text stays valid) |
| `docs/architecture/` | 17 | 55 | `lld.md` 14 (incl. implementation-status table L29–47 with `apps/*/decision.py`, `services/config-service/src/…` file paths; test-layer tables L166–169), `hld.md` 2, `call-state-recovery-options.md` 2, ADRs 0001 (4), 0002 (3), 0012 (3), 0006/0009/0010/0014/0015/0019 (2 each), 0004/0021/0022/0024/0025 (1 each) — see the ADR ruling note below |
| `docs/product/` | 6 | 110 | compliance-matrix 30, ne-datasheet 10, security-privacy 10, responsibility-matrix 9, version-lifecycle 8, one-pager 2 |
| `docs/operations/` | 6 | 31 | runbook-l1 9, runbook-l2 8, grafana-dashboards/README 3, alert-response-matrix 2, rollback-playbook 2, fault-demarcation 1 |
| `docs/plan.md` | 1 | 9–11 | mostly inside dated milestone/progress rows (history — keep); L167 guards table and L183 progress line describe the current layout — sync candidates |
| `deploy/alerts/` | 2 | 4 | README L68/74/127 (`platform/src/as_platform/…` metric-authority paths), `as-alerts.yaml` L51 comment |
| `deploy/compose/README.md` | 1 | 1 | L80 (listed in §2.3) |
| Member READMEs | 7 | ~19 | `apps/README.md` L25/L43; `apps/translation/README.md` L15/L23/L55/L58 (incl. `uv run python apps/translation/translation_sip_main.py`); `apps/anti-fraud/README.md` L15; `services/config-service/README.md` L15/L42/L61/L74 (`uv run --directory services/config-service …` ×3); `services/console/README.md` L15/L23/L26/L36; `platform/native/README.md` L29/L37/L49/L55; `platform/src/as_platform/sip/README.md` L24/L48. Note: several member READMEs are still in Chinese — path edits only, no rewrite |
| In-code docstrings/tests prose | 6 | ~10 | `platform/tests/test_req_s1_whitelist_rejection.py` L17/L42/L176, `platform/tests/test_resip_runtime_log_contract.py` L16, `platform/src/as_platform/sip/resip_runtime_log_contract.py` (1), `services/config-service/tests/test_req_s4_rbac_api_matrix_integration.py` (3 lines), `test_req_s4_audit_immutability.py` (1), `apps/anti-fraud/tests/__init__.py` (1) — cite file paths in prose; update where they name moved paths |
| `testbed/contracts/decision/README.md` | 1 | 2 | references product paths |
| `testbed/probe/README.md` | 1 | 1 | references product paths |

**History — preserve verbatim, do not edit (保史):**

| Area | Files | Occurrences |
|---|---|---|
| `docs/acceptance/` | 42 | 588 (incl. the 2026-10-12 FAIL/PASS artifact dumps) |
| `docs/reviews/` | 69 | 192 |
| `docs/handoff/` (pre-existing records, incl. this file's siblings) | 20 | 135 |
| `CHANGELOG.md` | 1 | 14 |
| `R2612_Cont.md`, `R2612_Struct_Plan.md` | 2 | 5+ |
| `docs/migration/triage.md` | 1 | 6 — historical POC→monorepo triage; its `src/as_app/` etc. refer to the *old POC layout*. **Name-collision warning:** after this migration `src/` means the product root; do not "fix" these to avoid fabricating history (an optional one-line historical note can be added at maintainer discretion) |

**ADR ruling note.** ADR bodies are accepted design records; several (0001, 0002, 0014,
0015, 0019, …) embed directory trees / layering language that names `platform/`,
`apps/`, `services/`. Two defensible treatments: (a) ADR text is history — never edited;
add a short "2026-10-29: layout now under `src/`" addendum line per ADR or a single note
in `docs/architecture/adr/README.md`; (b) treat directory references as living baseline
and update them. **This choice belongs to the maintainer**; the default below assumes (a)
for ADR bodies + a note in the ADR README, with `lld.md`/`hld.md` synchronized as living
documents.

### 2.6 CI

**No CI configuration exists**: no `.github/` directory, no `.gitlab-ci.yml`, no
`.circleci/`. The gate is the local `make gate` / `make gate-strict` / `make chart-check`
chain. Nothing to update in this category; the only consequence is that verification is
entirely local (§3).

## 3. Step-by-step execution checklist (for approval)

Seven steps; `git mv` everywhere so file history is preserved. Every step ends with a
verification command and an expected result. Steps 2–6 each end in a green `make gate`
before proceeding.

**Step 1 — Pre-flight baseline.**
Action: confirm clean-enough tree state with the maintainer (E1/E2 batch output is
uncommitted), record baseline: `make gate` → expect 1181 passed / 0 failed (per E1
record), `git status --short > /tmp/e3-pre.txt`.
Verify: `make gate`; expected: green, and the diff against the recorded baseline after the
batch contains only intended changes.

**Step 2 — Move the three directories (`git mv`).**
Action:
`git mv platform src/platform && git mv apps src/apps && git mv services src/services`.
Immediately fix the repo-root depth computations inside the moved tree (§2.2 table:
6 direct `parents[2]`→`parents[3]`, 2 fallback depths in `test_sip_message.py` +
2×`test_contract_replay.py`, and the 3 spots in `src/platform/tests/test_library_independence.py`).
Do **not** touch member-internal `parents[N]` (verified correct in §2.2).
Verify: `git status --short | grep '^R' | wc -l` (renames dominate; no copy/re-add of
source files); `git diff -M --stat | tail -1` shows high similarity. `make gate` is
expected red until steps 3–4 land — run it to capture the failure inventory, not as a
blocker.

**Step 3 — Root manifest + `uv.lock` regeneration.**
Action: apply the six key edits in §2.1; run `uv lock` then `uv sync`.
Verify: `uv run python -c "import as_platform, as_translation, as_anti_fraud, as_config_service, as_console, as_simulators, as_load, as_probe"` (all 8 import); `git grep -c 'editable = "' uv.lock` shows the 16 entries now carry `src/…` (3 testbed unchanged);
`uv run pytest tests/test_workspace_layout.py -q` → green (member-exists, src-layout,
ruff-src agreement all derive from the manifest).
Expected: workspace resolves from the new member paths; lock and manifest agree (this
unblocks every `uv sync --frozen` consumer, §5).

**Step 4 — Gate tests + first full gate.**
Action: apply the `tests/test_layer_boundaries.py` changes (§2.2: `_classify_layer`
prefixes + assertion/docstring text).
Verify:
`uv run pytest tests/ -q` (all 5 guards green, incl. the four-layer classification and
acyclicity tests);
`uv run pytest src/platform/tests src/apps src/services -m "unit or contract" -q`
(product unit/contract green from the new roots);
then **`make gate`** → expected: fully green (lint + type + layer ①).
Expected: first complete gate over the `src/` layout.

**Step 5 — Build, deploy, and tooling references.**
Action: apply §2.3 + §2.4 edits: `.dockerignore`; both `deploy/docker/*.Dockerfile`; the
two `testbed/sim-platform/Dockerfile*`; `testbed/sim-platform/kind-up.sh`; `Makefile`
`m71-sim`; `testbed/simulators/resip-probe/scripts/m2-native.sh` (6 refs);
`scripts/check_adr_annotations.py` (`_scan_roots` + all 26 `GRANDFATHERED` keys);
`scripts/demo-review/*` + `scripts/d10-req-nf1-harness.sh`; `deploy/compose/README.md` +
`deploy/compose/scripts/m4b-8-browser-evidence.sh`.
Verify: `make gate-strict` (ADR annotation scan clean, zero stale-key warnings);
`uv run pytest src/platform/tests/test_m5_verify_strict.py -q`;
`uv run pytest src/platform/tests/test_req_s3_overlap_integration.py src/platform/tests/test_resip_runtime_tls_integration.py src/platform/tests/test_resip_runtime_tls_policy_integration.py -m integration -q` (gen-cert.sh resolution);
`bash testbed/simulators/resip-probe/scripts/m2-native.sh build-platform-resip` (native rebuild from the new source root — optional, needs the m2 cache);
image builds `docker build -f deploy/docker/Dockerfile .` and
`docker build -f deploy/docker/config-service.Dockerfile .` (optional, needs docker) or
`make chart-check` as the deploy-side smoke.
Expected: every consumer of the moved tree resolves the new paths; no stale grandfather
keys.

**Step 6 — Documentation sweep (live docs only).**
Action: apply §2.5 live-doc edits — `README.md` (tree, mermaid, guard links),
`AGENT.md`, `CONTRIBUTING.md`, `lld.md`/`hld.md`, `docs/product/` (6 files),
`docs/operations/` (6 files), `docs/plan.md` (layout-describing lines only), member
READMEs, in-code docstring paths, `testbed/contracts/decision/README.md`,
`testbed/probe/README.md`, `.env.example` L4; add the ADR note per the maintainer's
ruling. **No edits** to `docs/acceptance/`, `docs/reviews/`, historical `docs/handoff/`,
`CHANGELOG.md`, `docs/migration/triage.md`, `R2612_*`.
Verify: `git grep -n -E '(^|[^-._a-zA-Z0-9/"])(platform|apps|services)/(native|src|tests|translation|anti-fraud|config-service|console|pyproject|README)' -- README.md AGENT.md CONTRIBUTING.md docs/architecture docs/product docs/operations docs/plan.md '*/README.md'`
returns only intentional (historical/quoted) remnants, each reviewed one-by-one;
`make gate` stays green (evidence-discipline / requirements-registry guards string-check
docs — any expectation drift surfaces here and is fixed in this step).
Expected: live docs describe the `src/` layout; history untouched.

**Step 7 — Final verification and record.**
Action: run the full chain: `make gate` → `make gate-strict` → `make chart-check` →
`make alert-check`; optionally `make test-e2e` (marker-based collection unaffected by
testpaths rename) and `uv run pytest -m integration -q` (integration layer exercises the
depth-fixed tests and the m2-native path defaults). Update R2612_Struct_Plan.md §7 E3
status and append a CHANGELOG entry per maintainer instruction. Leave all committing to
the maintainer.
Expected: every command green; results recorded with the triple
(command, artifact, date) per AGENT.md evidence discipline.

## 4. Non-automatable items and risks

1. **`uv.lock` staleness vs. `uv sync --frozen` (highest risk).** `uv.lock` carries 16
   `editable = "<member path>"` entries. Three Dockerfiles (`deploy/docker/Dockerfile`
   L142/L145, `config-service.Dockerfile` L18/L24) and `testbed/sim-platform/Dockerfile*`
   run `uv sync --frozen`, which installs from the lock as-is; a lock that still points at
   `platform`/`apps/…` fails (or mis-resolves) the moment the directories move. The lock
   must be regenerated (step 3) **before** any image build. There is no CI to catch this —
   a broken lock surfaces only on the next local build.
2. **`parents[N]` depth fixes are silent if missed.** `parents[2]` after the move resolves
   to `src/` instead of the repo root. Some failures are loud
   (`test_library_independence.py` L83–85 asserts `KERNEL_SOURCE` exists), but e.g. the
   `gen-cert.sh` resolution tests fail only in the integration layer, and the two
   walk-up **fallbacks** (`test_sip_message.py` L418, `test_contract_replay.py`) are
   dead code while the walk-up works — nothing red unless integration/perf runs. Mitigation:
   step 7 runs integration explicitly.
3. **`GRANDFATHERED` key drift in `scripts/check_adr_annotations.py`.** 26 path-prefixed
   keys; if only `_scan_roots` is updated, `make gate-strict` reports 26 stale keys plus
   false violations for every moved file. Both halves must change in the same edit.
4. **C++ build caches.** `platform/native/*/build/` directories (gitignored, on disk) and
   `~repo/.cache/m2-resiprocate` hold absolute-path CMake caches. After the move the
   in-tree caches point at `…/platform/native/…` and can poison a rebuild; the m2-native
   defaults in `m2-native.sh` L28–30 change to `src/platform/native/…`, so old build dirs
   are simply orphaned. Mitigation: delete `src/platform/native/*/build` (stale artifacts)
   and, if oddities appear, `AS_RESIP_CACHE_ROOT` to a fresh cache before step 5's native
   rebuild. Stale developer-local `AS_RESIP_*_BUILD` env overrides may also still point at
   old paths — they override the fixed defaults.
5. **Docker/kind image staleness.** compose (`deploy/compose/compose.yml`) and
   sim-platform build from the repo-root context; previously built images contain the old
   layout. Rebuild before any compose/kind evidence run after the migration.
6. **Chart checksums / `.helmignore`:** none reference source paths (`deploy/helm/` has no
   source-tree references at all, §2.3) — no checksum comments to invalidate.
7. **Docs guards string-check documents.** `tests/test_evidence_discipline.py` and
   `tests/test_requirements_registry.py` assert on doc contents (this already bit the E1
   batch). The step-6 doc sweep must re-run `make gate` to catch expectation drift.
8. **Member README language.** Several member READMEs are still Chinese (E2 covered only
   some); path edits inside them must follow the 保史 convention — fix the path, do not
   rewrite surrounding text.
9. **`src/` name collision in history.** `docs/migration/triage.md` uses `src/…` for the
   old POC layout; search hits for `src/` will grow noisier after the migration. History
   is not edited; future authors must disambiguate by date.
10. **`uv sync` local venvs.** Existing `.venv` editable installs point at old paths;
    `uv sync` after step 3 re-links them. Any stale shell with `PYTHONPATH` into
    `<repo>/platform/src` must be restarted.

## 5. Declaration

- This checklist is **produced for maintainer approval**; it is the E3 deliverable of
  R2612_Struct_Plan.md §7 (Q6=B first step).
- **No directory was moved and no code, configuration, or documentation file was changed
  in this batch.** The only file created is this document.
- Execution of the checklist (§3) starts only after the maintainer approves it; all
  committing remains the maintainer's decision (AGENT.md §11 — no `commit` / `push` /
  `tag` from agents).
