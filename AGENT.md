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

# AGENT.md — 3rdparty-as

> Rules of engagement between humans and AI agents.
> Read this file before writing any code. If any rule here conflicts with a request, this file prevails, and raise the conflict with the maintainer.

## Agent skills

### Issue tracker

Issues and specs live in GitHub Issues; use the `gh` CLI. See `docs/agents/issue-tracker.md`.

### Triage labels

Use the canonical triage labels mapped in `docs/agents/triage-labels.md`.

### Domain docs

This is a single-context repo. Read the relevant domain docs and ADRs under `docs/architecture/adr/`; see `docs/agents/domain.md`.

## 1. Positioning and scope

A **productized third-party IMS Application Server (application server)**: single-tenant, on-premises, deployed outside the operator's IMS network, triggered by the S-CSCF through the operator's S-SBC, which does transparent bridging.

It **is not a POC**. The POC (`../3rtparty_AS_POC`) exists to validate concepts under a different set of goals; this repository is the product itself.

**We implement only the external AS.** The S-CSCF, S-SBC, and HSS are the operator's; here they appear only as simulators under `testbed/`.

For positioning details, architecture diagrams, and the 19 confirmed decisions, see [`docs/architecture/system-architecture.md`](docs/architecture/system-architecture.md). For milestones, open items, and current status, see [`docs/plan.md`](docs/plan.md).

## 2. Non-goals

Explicitly out of scope. Each is the result of a decision, not an oversight:

- **No media.** No RTP, no transcoding, no DTMF, no MRF, no media anchoring. Keep a seam and document the trigger conditions (ADR-0004).
- **No CDR.** No collection, delivery, archiving, or rating. Replace it with a Call-ID-based call trace, for complaint tracing and anti-fraud evidence (ADR-0017).
- **No lawful interception (LI).** IRIs belong to in-network network elements; having a third-party AS intervene would introduce cross-jurisdiction exposure (ADR-0016).
- **No Diameter Sh.** Data comes from our own data plane.
- **No multi-tenant.** Single-tenant, on-premises. Rationale:

  | Dimension | Single-tenant | Multi-tenant |
  |---|---|---|
  | Deployment | One independent instance per customer, on-prem delivery | Shared instance, logical isolation |
  | Isolation | Natural physical isolation, independent fault domains | Needs tenant-level namespaces + access control |
  | Ops | Upgrade windows negotiated per customer, no mutual impact | One change affects all tenants |
  | Compliance | Data does not leave the customer machine room, clear audit boundary | Cross-tenant data-leak risk needs extra proof |

  The operator's delivery form is itself one system per customer; multi-tenant brings no benefit in this scenario.
- **No GitOps for config.** We cannot require operator ops staff to learn Git just to change a number range; the version is stored as a row in PostgreSQL, behind a change-order state machine (ADR-0006).
  Change path: console / internal API submits a change order → approval → service writes to PostgreSQL → canary distribution.
  Not ops directly `UPDATE`-ing the database, nor managing config with a git repo.
- **No Operator (CRD).** Use Helm + standard Deployment / ConfigMap / Secret (ADR-0013).
- **No capacity numbers published before M6 measurement.** Before measuring on a real-socket load test, publish no CPS or concurrency number.

## 3. Engineering phases and the documentation chain

Every behavioral change must traverse the entire documentation chain. The Requirement is the **single standard** for design, coding, testing, and acceptance. A change missing any link is incomplete.

```text
Requirement
   ↓
Architecture Decision (ADR)
   ↓
High-Level Design (HLD) + Low-Level Design (LLD)
   ↓
Interface contracts and message samples
   ↓
Code + tests
   ↓
Acceptance items and Review Record
```

### 3.1 Phase definitions

| Phase | Output | Owner | Condition to enter next phase |
|---|---|---|---|
| **Requirement** | REQ-F-*/REQ-NF-* entries in `docs/requirements/` | Maintainer / Product | Review passed, with review record |
| **ADR** | `docs/architecture/adr/00NN-*.md` | Maintainer / Architecture | Review passed, with review record |
| **HLD/LLD** | `docs/architecture/hld.md`, `docs/architecture/lld.md` (including feature enablement design) | Maintainer / Architecture | Review passed, with review record |
| **Interface Contract** | Use cases, message samples in `testbed/contracts/` | Maintainer / Dev | Consistent with ADR, with review record |
| **Code + Test** | Implementation code + corresponding tests | Dev / AI agent | `make gate` green, PR references ADR and requirement |
| **Acceptance** | Evidence in `docs/acceptance/report.md` | Maintainer | Acceptance items pass one by one, with review record |

### 3.2 Documentation requirements

- **Every phase must have documentation.** A decision without documentation is a decision that never happened.
- **Requirement is the single standard.** Design, code, tests, and acceptance must all trace to a specific REQ-* number.
- **All documents must be reviewed.** Review is not optional; each phase's output must pass review before entering the next phase.
- **A Review must have a separate review record.** Review opinions, modification records, and sign-off status are written to a separate file under `docs/reviews/` (e.g., `docs/reviews/adr-0019-review.md`). Oral or inline comments do not constitute a formal review record.
- **When overturning or modifying an upstream document, the entire chain must be updated synchronously.** Changing only code without changing requirement/design/acceptance is incomplete.

### 3.3 Review Record format

Each review record contains at least:

1. Review target (document / PR / commit range)
2. Review date and reviewer
3. Review conclusion: pass / conditional pass / fail
4. List of issues found and corresponding fixes
5. Confirmation sign-off after fixes

### 3.4 New Feature implementation flow

Corresponding to the §3 documentation chain, each new feature advances phase by phase:

1. **REQ** — the requirement entry enters `docs/requirements/`.
2. **ADR** — explicitly adjudicate **enablement** (whether to introduce a toggle, default state, canary, removal condition).
3. **HLD/LLD** — lands in the design doc: how toggles are layered, how they are judged, how to roll back.
4. **Contract** — the toggle only enables/disables a capability, **does not change the interface contract**; the off path uses the existing default.
5. **Code + Test** — both **on / off** states of the toggle must have tests (§6).
6. **Acceptance** — gather evidence by toggle state (§14).

**Rule**: each feature must explicitly adjudicate **whether to introduce a toggle**; if introduced, must state the **default state, canary strategy, and removal condition** (to prevent toggle debt). Mechanism in [ADR-0020](docs/architecture/adr/0020-feature-capability-gating.md) and [`docs/architecture/system-architecture.md`](docs/architecture/system-architecture.md) §5.3.

## 4. Layering

```text
apps/  ──uses──▶  platform/          one process per use case
services/ ─────────────────────────▶  PostgreSQL, AS internal API
testbed/ ──may use──▶ platform/       R&D asset, never a runtime dependency
```

**The core must never import apps, services, or testbed.** The repo boundary does not enforce this — in a monorepo any import resolves. It is enforced by [`platform/tests/test_library_independence.py`](platform/tests/test_library_independence.py) and [`tests/test_workspace_layout.py`](tests/test_workspace_layout.py).

An app must never import another app. A use case is one process, one fault domain, one canary unit.

**Internal dependency among services (added note 2026-10-11, pending maintainer review)**: the layering diagram above does not forbid dependencies between members of the services layer along the "internal API" direction. The only existing example: `services/config-service` (imports root `as_config_service`) depends on `services/console` (imports root `as_console`, using its session / auth internal API). That dependency is explicitly declared in `services/config-service/pyproject.toml` (the `as-console` in `[project].dependencies` and the workspace source in `[tool.uv.sources]`); `services/console/pyproject.toml`'s dependencies are empty, and console does not depend back on config-service, so no cycle is formed. Rule: such dependencies **must** be explicitly declared in the dependent party's `pyproject.toml`, and the declared internal dependency graph must be acyclic; "used but not declared" is machine-guarded by [`tests/test_layer_boundaries.py`](tests/test_layer_boundaries.py)'s `test_internal_imports_are_declared_dependencies`, and cycles by the same file's `test_internal_dependencies_do_not_form_a_cycle`; undeclared or cyclic is a violation. **This paragraph does not relax the app-mutual-exclusion rule above nor the testbed ban**: apps still must never import another app, and the product package still must never depend on testbed.

Directory structure and member list are in [`docs/plan.md`](docs/plan.md) §2.

## 5. Coding conventions

- **Language of artifacts: English.** Identifiers, comments, logs, error strings, commit messages, and code-adjacent docs are all English. Human-facing documentation in this repo is in Chinese; that is the only exception.
- **All public functions must have type annotations; `mypy` strict mode must be clean.**
- **The decision module is a pure function.** The module that produces decisions must have no socket, no clock, no global state. This is precisely why TDD is cheap there.
- **SIP stack interaction is confined to the SIP adapter and call controller.** Keep the glue layer thin.
- **`ED2.loop()` or equivalent blocking event loop is blocking.** Never call a blocking operation inside a SIP callback — including telemetry export. Export runs on its own thread (ADR-0005).
- **Every line of non-obvious code points to its ADR**: `# See ADR-00NN`. A reviewer must be able to walk from code to rationale in one step.
- **No `util`, `helper`, `misc`, `common`, `tools` module names in `src/`.**
- **SIP stack behavior is observed, not assumed.** When in doubt, write a probe under `testbed/` and run it. Never invent a header, status code, or API out of thin air.

## 6. Test strategy

Tests must align with requirements. Each test should trace to at least one REQ-* or contract case.

| Layer | Marker | Method |
|---|---|---|
| Decision logic | `unit` | **mandatory TDD**, red - green - refactor. The payoff of TDD is here. |
| Contract | `contract` | Declarative cases, in `testbed/contracts/`, replayed against **every** implementation |
| Protocol / access | `integration` | Contract tests + simulated peers; no strict TDD — high cost, low payoff |
| Full flow | `e2e` | Full call + error branches, including console |
| Capacity | `performance` | Real socket only. Never measure via driven callbacks — that tests business logic, not the system (ADR-0014) |

**The on/off states of a feature toggle must be covered in the corresponding test layer** (mechanism in [ADR-0020](docs/architecture/adr/0020-feature-capability-gating.md)).

Test ports must be configurable to avoid port conflicts during parallel runs.

## 7. ADR

Every architecture decision leaves a record in `docs/architecture/adr/`. The registry maps confirmed decisions to ADR numbers; see [`docs/architecture/adr/README.md`](docs/architecture/adr/README.md).

- Write the ADR **together with** the change it authorizes — not back-filled, not batch-filled.
- The ADR must state the gaps it accepts. An empty consequences section means analysis is unfinished.
- Overturning a decision means adding a new ADR, **and** updating [`docs/architecture/system-architecture.md`](docs/architecture/system-architecture.md) in the same change.
- POC ADRs 0001…0016 are **not** imported. They describe a different system. They may be cited as background, but not treated as binding.

## 8. Versions and dependencies

- **`./VERSION`** is the single source of the product release version. One number per delivery, because the operator receives a system.
- **`<member>/pyproject.toml`** carries that component's own interface version.
- **No member may own a `VERSION` file.** One number with two homes is exactly the drift this repo kills (ADR-0018). Guarded by [`tests/test_version_consistency.py`](tests/test_version_consistency.py).
- **The SIP protocol stack is decided by ADR-0019.** Until ADR-0019 is accepted, `platform/` binds to no specific SIP stack. The `sippy==2.4.2` used by the POC is only a reference tool in `testbed/` for capturing behavior baselines, and does not enter production dependencies.
- Every dependency goes through `uv`; commit `uv.lock` and verify lock-file consistency.

## 9. Gates

`make gate` = `ruff format --check` → `ruff check` → `mypy` → pytest (unit/contract layers). Four fixed steps; AST scanning is **not** in the gate.

**AST scanning ownership**: AST scanning (checks whether non-obvious code is annotated with its ADR, corresponding to REQ-G-3) runs **outside** `make gate` (ADR-0015). Trigger it with the `make gate-strict` target (`make gate` four steps + AST scanning). `make gate` itself stays the four fixed steps, keeping fast feedback.

Local also has four layers, each an independent target: ① fast (`make test-unit`, `unit or contract`) → ② integration (`make test-integration`) → ③ e2e (`make test-e2e`) → ④ performance (`make test-perf`, not in the commit gate). AST scanning is not part of these four layers; trigger it separately per the line above.

Nothing may be committed while the local gate is red. **The local gate's conclusion covers only what it actually ran**: never present a local re-run as stronger verification than it is.

**Layering status note**: `make test` runs ① → ② → ③ in sequence. The `integration` layer already has tests; the `e2e` layer has no test files yet (the marker is declared in `pyproject.toml`), so `make test` will fail at ③ because pytest collects no tests. `make gate` runs only layer ①. The milestone that first introduces a test for a layer must confirm that layer is active in the corresponding target.

## 10. AI assistance and Subagent collaboration

1. AI-generated code goes through the **exact same** gate. No lower standard because it was generated.
2. PRs containing AI-generated work must be **labeled** so reviewers can weight them accordingly.
3. Porting the Go image is the highest-leverage AI task in this project — isomorphic translation + differential-harness. Exploit this leverage; but do not lower the standard.

### 10.1 Subagent mode (the sole authoritative description of dispatch)

- **Decide when taking the task, not when writing the file**: on receiving a task, first judge whether it will produce a file change (create / edit / delete). If yes — before doing anything else, dispatch a writing subagent; the main agent only plans and reviews.
- **The main agent does not write code or files.** The main agent plans, splits tasks, reviews subagent output, and reports to the maintainer.

**Identify the IDE first — the two IDEs have different dispatch mechanisms; using the wrong one silently degrades to read-only** (this repo's M0 already hit this pitfall):

| IDE | Read-only (explore / research / code search) | Writable (any file change) |
|---|---|---|
| **Trae** | `Agent` tool, `subagent_type = Explore` | `Agent` tool, `subagent_type = general-purpose` |
| **CodeBuddy** | `Task` tool, no `name` passed, `subagent_name = code-explorer` | `Task` tool, **pass `name`** (role label, e.g. `m0-writer`, i.e. team mode) + `mode = "acceptEdits"` |

> Basis: use whichever tool you have. In CodeBuddy there is **no** `general-purpose` / `Explore`; calling by name raises
> `Subagent "general-purpose" not found`; **do not fall back to the main agent writing files itself** — use its own team mode (pass `name`) instead.
> Conversely, in Trae the `Agent` tool + `subagent_type` is correct; do not copy CodeBuddy's approach.

Dispatching a writing subagent:

1. The `prompt` must be self-contained: goal, boundaries, verification commands, report format, and all hard constraints (e.g., "do not run git commit", "only this one file may be changed"). CodeBuddy additionally needs `name` and `mode = "acceptEdits"` (passing `name` auto-enables team mode and creates the team; no separate `team_create` needed).
2. After the subagent reports completion, the main agent uses `git status` / `git diff` to verify the actual changes against its self-report.
3. After confirming, close that writer, **then** start the next one.

- **Only one writing subagent per worktree at a time.** Git state is per-worktree; a second writer's changes land on the wrong branch or overwrite each other, and the failure is silent.
- **The spawn prompt must be self-contained**: appended messages are only read at the next turn boundary and **cannot interrupt a running turn** (§10.3).
- **When a writable subagent cannot be dispatched**: ① first confirm the current IDE and mode per the table above; ② if still unavailable, **stop and report to the maintainer**, who must explicitly approve the main agent writing directly. **Never decide on your own to write files.**
- **Trust but verify:** the main agent must use `git status` / `git diff` to verify the files a writing subagent actually changed, against its self-reported summary. A subagent's summary describes its intent, not necessarily what it actually did.
- **Main agent self-check**: before each turn ends, answer "did I write any file directly this turn?". If yes — stop immediately and report to the maintainer.

### 10.2 Context management

- **When context nears its limit, notify the maintainer immediately**; do not work silently until auto-compaction happens. Notification content: (1) a disk-state inventory of what has landed (verified with `git status`); (2) handoff decision suggestion (new conversation / catch up on disk first / stay in this conversation).
- **Any decision that "exists only in the conversation and cannot be recovered if lost" must be written to disk before opening a new conversation.** Write destinations: adjudications go to ADR / gap review, status to `docs/plan.md`, research conclusions to a dedicated `docs/` doc.
- Specific flow in the project skill `.trae/skills/context-handoff/`.

### 10.3 Task dispatch and synchronization

- Subagents are stateless: each call returns only the final result, intermediate steps invisible. The spawn prompt must be self-contained — goal, boundaries, verification commands, report format all written in.
- **All hard constraints must be in the spawn prompt** (e.g., "do not run git commit", "only this one file may be changed"), not relied upon in follow-up messages.
- When you need to ask or append instructions: if the subagent is still running use `SendMessage` (CodeBuddy) or an equivalent append mechanism; if completed, use the `resume` parameter (Trae) to continue its context. Do not spawn a new subagent just to ask a follow-up.
- A subagent must stop and report before making an expensive modification (adding a dependency, changing a schema, deleting code, committing).

### 10.4 Handover protocol

The **opening ceremony** of each milestone conversation:

1. Read `AGENT.md` (this file)
2. Read `docs/README.md`
3. Read the current milestone section in `docs/plan.md`
4. Read the acceptance items for that milestone in `docs/acceptance/m8-test-plan-matrix.md` (2026-10-11 correction: originally pointed to `docs/acceptance/criteria.md`, which never existed; the acceptance matrix now uses `m8-test-plan-matrix.md`)
5. Confirm the current branch (named or approved by the maintainer)
6. **First-task subagent judgment**: on receiving the maintainer's first task, first judge whether it involves a file change (create / edit / delete). Yes — dispatch a writing subagent immediately, then do other planning or discussion; No — enter read-only mode.

**Closing ceremony**:

1. Run the DoD, write results to `docs/acceptance/report.md`
2. Update `docs/plan.md` status and the next-milestone entry
3. Update `CHANGELOG.md` and `VERSION`
4. Do not write a tag: the tag is the maintainer's step

## 11. Git rules

- **Never push without the maintainer's explicit approval in that conversation.** Not push, not force-push, not tag.
- **Agents do not create branches.** Work on the branch designated by the maintainer. Each branch needs a clear purpose and end condition.
- **Nothing may enter `main` / `master` without per-instance, explicit approval.**
- **Conventional Commits**, in English, one logical change per commit: `feat` · `fix` · `docs` · `refactor` · `test` · `chore` · `build`.
- **Do not skip hooks.** `--no-verify` and its equivalents are forbidden. If a hook blocks a commit, fix the cause.
- **Never commit keys, certificates, or real traffic captures.**
- A behavioral change must traverse the whole documentation chain: requirement → ADR → design → interface contract → acceptance item → CHANGELOG.

## 12. Adopting code from the POC

**Never copy wholesale.** See [`docs/migration/triage.md`](docs/migration/triage.md).

- Each POC file must have an adjudication before writing product code — adopt / rewrite / baseline-reference / discard — and must have evidence.
- Adopted code comes **with its tests**.
- The POC's behavior baseline must be captured **before** any rewrite, so that "equivalence" is a checkable assertion.
- This repo must build, test, and run **without referencing** `../3rtparty_AS_POC` or `../as_platform`.

## 13. Security

- Do not commit any sensitive information: no keys, certificates, tokens, or real addresses.
- The trunk is untrusted. Peers must be validated against an allowlist and terminate TLS end-to-end with the S-SBC — anyone who can impersonate the S-SBC can inject calls (ADR-0016).
- Certificate rotation is a configuration hot-update. Never restart a process, never drop in-flight calls.
- Payload logging is explicit and toggleable; off by default in logs.
- Every console operation must be authenticated and audited.

## 14. Definition of done

- [ ] End-to-end pass against the simulated peer
- [ ] Added tests in the layer of the change; `make gate` green
- [ ] `ruff format`, `ruff check`, `mypy` clean
- [ ] Change carries an ADR; if the decision moved, `docs/architecture/system-architecture.md` is updated
- [ ] README and affected docs updated (new env var, port, command, directory)
- [ ] Has a CHANGELOG entry; if delivery content changed, the product version was bumped
- [ ] If POC code was adopted: referenced the corresponding triage line
- [ ] No key committed
- [ ] Documentation chain complete: requirement → ADR → HLD/LLD → contract/message samples → acceptance item → review record
- [ ] If a feature toggle was introduced: both on/off states have tests and acceptance evidence, and the removal condition is stated

## 15. Open items

The open-item list and risk register are held in [`docs/plan.md`](docs/plan.md) §5. Do not silently resolve an open item: if a piece of work forcibly forces out a decision, write an ADR and move that line in `plan.md`.

The largest of these, O1 (capacity target), has its own independent research milestone (M6). Do not assume any capacity number before it runs.
