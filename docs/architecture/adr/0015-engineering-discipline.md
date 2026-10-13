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

# ADR-0015: Engineering discipline — layered TDD, ADR institutionalization, four-tier test gate

- **Status**: accepted
- **Date**: 2026-09-30
- **Decides**: §0 ledger item 17 — engineering discipline: layered TDD + ADR institutionalization + four-tier test gate
- **Responds to REQ**: REQ-G-3, REQ-G-4

---

## Context

This project's code falls into two categories with completely different testing cost structures. **Decision logic is pure functions**: `AGENT.md` §5 mandates that "modules producing decisions must have no sockets, no clock, no global state" — deterministic input, no IO, no time dependence, where TDD is cheapest and most effective. The **protocol / ingress layer**, by contrast, depends on real sockets, real stack behavior, and timing; writing strict red-green-refactor cycles for it is costly with low payoff — architecture doc §11.3 concludes "contract tests + simulation integration tests primarily, no strict TDD." A single unified test strategy across both categories inevitably over-requires one tier and under-requires the other.

A second fact dictates that discipline must be enforced by machine, not by conscience: **most of this project's code is produced by AI agents** (`AGENT.md` §10). The first hard rule of `AGENT.md` §10 is "AI-generated code passes the **exact same** gate. No lowering the bar just because it was generated." Human attention is a scarce resource that should focus on "is this decision correct," not "is this formatting correct"; formatting, types, and layering must be delegated to the gate.

A third fact is the half-life of decisions themselves. The ADR registry opens with: **"A decision without an ADR is a decision to be re-argued."** An unrecorded architectural decision does not disappear; it merely gets re-discussed the next time someone hits it — usually without the original constraint context. So "ADR institutionalization" is not paperwork; it amortizes the decision cost once and for all.

`AGENT.md` §6 already gives the layering and marker skeleton, `AGENT.md` §9 defines the gate, `docs/plan.md` §2.4 gives the four-tier gate table, and architecture doc §11.2 / §11.3 give the layering diagram and development-mode table. This ADR consolidates these already-scattered disciplines into one decision with consequences, and clarifies their boundaries (especially "what is outside the gate").

## Decision

- **① Layered testing and markers: `unit` / `contract` / `integration` / `e2e` / `performance`. The decision-logic layer mandates TDD (red-green-refactor); the protocol / ingress layer uses contract tests + simulation integration primarily, not strict TDD.** Layering is not a priority ordering but a different evidence type: unit proves the decision is correct, contract proves each implementation agrees, integration proves it works against a simulated peer, e2e proves the full flow including error branches, performance proves capacity boundaries.
- **② Every architectural decision must be recorded in an ADR; a decision without an ADR never happened.** The ADR is written **together with** the change it authorizes — not retrofitted, not batched. The ADR must state the gap it accepts (an empty Consequences section means the analysis is unfinished); overturning a decision means writing a new ADR and updating the architecture doc in the same change.
- **③ Four-tier test gate: ① fast → ② integration → ③ e2e → ④ performance.** Local `make gate` must be fully green to commit; `--no-verify` and its equivalents are forbidden (`AGENT.md` §11). The local gate's conclusion only covers what it actually ran (`AGENT.md` §9).
- **④ Non-obvious code must cite its ADR**: `# See ADR-00NN`, so a reviewer can step from code to rationale in one hop (REQ-G-3). The AST scan (checking this annotation) runs separately from the four `make gate` steps and can be triggered with `make gate-strict`.
- **The milestone that introduces the first use case for any tier must simultaneously make that tier blocking.** Otherwise the tier is decorative.

## Consequences

### Positive

- **Unified quality gate.** `make gate` is the only gate for commits, always running the same checks in the same order (`ruff format --check` → `ruff check` → `mypy` → pytest unit+contract) — no second standard.
- **TDD investment lands where the payoff is highest.** Decision logic mandates TDD; the protocol layer is not forced, and the saved cost goes into contracts and simulation — which is where the protocol layer's real risk lies.
- **Decisions are traceable, code is attributable.** ADRs make "why it is this way" documented; `# See ADR-00NN` lets a reviewer step from one non-obvious line of code to that ADR instead of guessing.
- **AI-produced code meets the same standard as human code.** The gate is source-agnostic and only checks the artifact — which is the premise for AI assistance being used at scale in this project.
- **Layering keeps slow tests from blocking fast feedback.** The capacity tier runs on demand manually and is not in the commit gate.

### Negative / accepted

- **The four-tier gate only matters when each tier actually blocks.** The milestone introducing a tier's first use case must simultaneously make it blocking, otherwise the tier is merely decoration. Tier ③ e2e and tier ④ performance still have no use cases and do not block; tier ② integration became blocking with its first use case (`platform/tests/test_telemetry_export_integration.py`). **This is a discipline requiring continuous execution, not a one-time action.**
- **`make gate`'s four steps do not include the AST scan.** Therefore the "ADR annotation" rule is not enforced in the local fast gate, only in `make gate-strict` (REQ-G-3 explicitly assigns it here). Accepted: trade fast local feedback; the cost is that mis-annotations or omissions are not caught locally.
- **Layering markers rely on humans marking them correctly.** A test tagged in the wrong tier runs in the wrong gate tier (e.g., a slow integration test tagged `unit`), slowing the fast tier while letting the integration tier pass through empty. There is no automatic validation of markers.
- **The cost of ADR institutionalization is real.** Every decision requires a document with Consequences; skipping it to catch up on schedule is exactly the source of "decisions being re-argued." This batch of ADRs (0008 / 0012 / 0013 / 0014 / 0015) are themselves lagging products of this discipline — they already existed in architecture doc §0 ledger but lacked ADRs, an anti-pattern against `AGENT.md` §7 "no retrofitting, no batching," recorded here.
- **`--no-verify` being forbidden means a blocking gate must be fixed at the cause, not bypassed.** In emergency-fix scenarios this adds time cost. Accepted: a bypassed gate is no gate.

## Alternatives considered

| Option | Why not |
|---|---|
| Mandate TDD for all tiers | Protocol / ingress TDD is costly with low payoff (architecture doc §11.3); it displaces cost from the real high-risk area (contracts and simulation) |
| No TDD mandate for any tier (tests follow implementation) | Decision logic is pure functions where TDD is cheapest; abandoning it means abandoning quality where it is cheapest |
| Single tier (run everything once) | Slow tests block fast feedback; running capacity every commit kills merge throughput, and capacity conclusions are not a commit-gate concern anyway |
| Remote gate only, no local gate | Feedback cycle goes from minutes to "after push"; and committing ungreen locally turns the remote into a debugger |
| Decisions by word-of-mouth / PR description, no enforced ADR | A decision without an ADR gets re-argued (ADR registry opening); overturning a decision has no accountability or comparison point |
| Layered TDD + ADR institutionalization + four-tier test gate (this decision) | Adopted |

## Evidence

- `AGENT.md` §6 testing-strategy table verbatim (line by line): "Decision logic | `unit` | **mandatory TDD**, red-green-refactor. TDD pays off here." "Contract | `contract` | declarative use cases, placed in `testbed/contracts/`, replayed against **every** implementation." "Protocol / ingress | `integration` | contract tests + simulated peer; no strict TDD — costly, low payoff." "Full flow | `e2e` | full call + error branches, including console." "Capacity | `performance` | real sockets only. Never test by driving callbacks — that tests business logic, not the system (ADR-0014)."
- `AGENT.md` §9 gate verbatim: "`make gate` = `ruff format --check` → `ruff check` → `mypy` → pytest (unit/contract tiers). Four steps fixed; AST scan is **not** inside the gate." "**AST scan assignment**: the AST scan (checking whether non-obvious code cites an ADR, per REQ-G-3) runs **outside** `make gate` separately (ADR-0015). Trigger via the `make gate-strict` target (`make gate`'s four steps + AST scan)." "Local gate not green, nothing commits. **The local gate's conclusion only covers what it actually ran**: never present a local re-run's result as stronger verification than it is." "**The milestone introducing a tier's first test must simultaneously confirm that tier is active in the corresponding target.**"
- `Makefile` definitions: `gate: lint type test-unit`, where `lint` = `ruff format --check .` + `ruff check .`, `type` = `uv run mypy`, `test-unit` = `uv run pytest -m "unit or contract" -q`. File header comment: "3rdparty-as — the local gate." "`make gate` is tier ① — lint, type, then unit/contract tests, in that order."
- `docs/plan.md` §2.4 "Four-tier test gate (ADR-0015)" table: ① fast `unit or contract` (`make gate` / `make test`), ② integration (after ①), ③ e2e (after ②), ④ performance (on demand / manual). Same-section progress verbatim: "the `integration` tier's first use case has been introduced (`platform/tests/test_telemetry_export_integration.py`, real-socket verification that telemetry export does not block), tier ② has simultaneously become blocking; tier ③ e2e and tier ④ performance still have no use cases and do not block."
- Architecture doc §11.3 "Development mode (Q16 = A)" table verbatim: "**Business decision layer** (`routing/engine`, `screening`) | **mandatory TDD**, Red-Green-Refactor | pure functions, TDD highest payoff lowest cost." "**Protocol/ingress layer** | contract tests + simulation integration primarily | no strict TDD, high cost low payoff." "**Design decisions** | **ADR institutionalization** | every decision here lands an ADR." §11.2 four-tier gate diagram annotation ① "minutes-scale · must pass."
- Architecture doc §0 decision ledger item 17 verbatim: "Engineering discipline | layered TDD + ADR institutionalization + four-tier test gate."
- PRD REQ-G-3 (non-obvious code must cite its ADR) verbatim: "Non-obvious code (code you cannot understand why it is written that way without reading context) must carry a comment pointing to the corresponding architectural decision… must annotate `# See ADR-00NN` at the end of the code line. Reviewer steps from code to rationale, not guessing. The AST scan runs outside `make gate` separately…"
- PRD REQ-G-4 (`make gate` must be green to commit) verbatim: "`make gate` = `ruff format --check` → `ruff check` → `mypy` → pytest (unit/contract tiers). Local gate not green, nothing commits. `--no-verify` and its equivalents are forbidden."
- `AGENT.md` §11 Git rules verbatim: "**Do not skip hooks.** `--no-verify` and its equivalents are forbidden. If a hook blocks the commit, fix the cause." §10 rule 1: "AI-generated code passes the **exact same** gate. No lowering the bar just because it was generated."
- `docs/architecture/adr/README.md` rules verbatim: "Write the ADR **together with** the change it authorizes — no retrofitting, no final batch. A decision without an ADR is a decision to be re-argued." "**An ADR must state what it accepts.** … an ADR without a Consequences section is propaganda." "**Code points to its ADR.** A non-obvious line carries `# See ADR-00NN`."

## Related

- [ADR-0012](0012-cross-implementation-parity.md) language-agnostic contracts — the criterion source for the `contract` tier
- [ADR-0014](0014-three-layer-testbed.md) three-layer testbed — the carrier for the `integration` and `performance` tiers
- [`../system-architecture.md`](../system-architecture.md) §11.2 four-tier test gate, §11.3 development mode
- `AGENT.md` §6 testing strategy, §9 gate, §10 AI assistance, §11 Git rules (**repo red line; this ADR archives them, does not replace them**)
- PRD REQ-G-3 (ADR annotation), REQ-G-4 (`make gate` gate)
- Tier ③ e2e and tier ④ performance **still have no use cases** and do not block; the points at which they become blocking are M3 and M6 respectively
