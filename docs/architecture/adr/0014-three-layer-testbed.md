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

# ADR-0014: Three-layer testbed; capacity load testing uses real sockets only; the testbed is not a v1 deliverable

- **Status**: accepted
- **Date**: 2026-09-30
- **Decides**: §0 ledger entry 16 — test platform: testbed three layers; v1 is not a deliverable
- **Responds to REQ**: [REQ-NF-15](../../requirements/req-nf-15-testbed-performance.md) (2026-10-05, closes D8; the original REQ-NF-13 mis-pointing is noted in the Evidence history remark)

---

## Context

In the delivery environment, the S-CSCF, S-SBC, and HSS are **the operator's network elements**, not part of our deliverables (`AGENT.md` §1). Locally we do not have them; we can only simulate. If the iFC trigger chain and the S-SBC's transparent bridging behavior cannot be simulated, integration tests have nowhere to run — this is not "insufficient testing" but "having nothing to test".

Capacity measurement has a more specific historical lesson. The POC's `CapacityDriver` **directly drove callbacks**, bypassing the socket and event loop: what it measured was the business logic's execution time, not the system's capacity. Architecture doc §11.4 lists it as the first key point: if the capacity baseline is not comparable, there is no way to judge "whether CPS hits the wall", and thus no way to adjudicate whether a stronger stack is needed. In other words, **a figure measuring the wrong thing is more harmful than no figure** — it will be used as a basis.

The positioning of `testbed/` is simultaneously determined by a hard boundary: the layering diagram in `AGENT.md` §4 reads `testbed/ ──may use──▶ platform/ R&D asset, never a runtime dependency`, and "the kernel must never import applications, services, or testbed", enforced by `platform/tests/test_library_independence.py`. The testbed may **use** the kernel; the kernel must never **depend on** the testbed; the direction is one-way.

The last constraint comes from the delivery scope: architecture doc §11.4 key point 4 records "⏳ **v1 does not treat the testbed as a deliverable**, only as an R&D asset; customer acceptance testing capability is left to v1.1". Whether customer acceptance testing must be supported in v1 is **open item D6** (`docs/plan.md` §5.2, responsibility milestone M8); the current position is to defer it to v1.1.

## Decision

- **`testbed/` has three layers, each answering a different question:**
  - **contracts** — declarative contracts and baselines (the decision case set `decision/cases.json`, the SIP message baseline `sip-baseline/`). Answers "are the decisions correct, and are the implementations consistent" ([ADR-0012](0012-cross-implementation-parity.md)).
  - **simulators** — simulated peers and probes (simulated S-SBC / IMS network elements, stack-selection probes `testbed/probe/`). Answers "can AS work against something that behaves like the operator's peer".
  - **load** — real-socket load testing. Answers "where exactly the capacity boundary lies".
- **Capacity load testing uses real sockets only. Never measure by driving callbacks** — driving callbacks measures the business logic, not the system. Bytes must really go on the wire, and the socket, event loop, and protocol stack must all be in the measurement loop.
- **The testbed is an R&D asset, never a runtime dependency.** The kernel does not import testbed; production images do not carry the testbed.
- **The testbed is not a v1 deliverable.** Customer acceptance testing capability is deferred to v1.1 (open item D6's current position).
- **The load-testing tool may use SIPp (GPL)**: for internal testing only, **never distributed with the product**.

## Consequences

### Positive

- **Contracts and simulation make "equivalence" assertable.** Contracts are data, simulators are executable objects, and "equivalence" goes from a judgment to a repeatable assertion ([ADR-0012](0012-cross-implementation-parity.md)).
- **Simulated network elements are first-class assets.** With the iFC chain and S-SBC transparent bridging behavior simulatable, integration tests have somewhere to run; otherwise [ADR-0003](0003-s-sbc-transparent-bridge.md)'s single-ISC semantics could not be verified, only believed.
- **Real-socket load testing gives capacity meaning.** With the measurement loop including the socket and event loop, the measured figures can answer "has CPS hit the wall", and can serve as input to O1 and stack selection.
- **The three layers each do their job and do not impersonate each other.** The contracts layer is not used to impersonate integration verification, and the load layer is not used to impersonate functional correctness — the former misses protocol behavior, the latter misses system overhead.
- **One-way direction (testbed → platform) guarantees clean production images.** The runtime cannot depend in reverse on R&D assets.

### Negative / accepted

- **This ADR gives no capacity figures.** CPS, concurrent sessions, and setup latency all await M6 and open item O1 (`AGENT.md` §2: "no capacity figures are published before M6 measures them"). `testbed/load` was in a README-and-package-skeleton state when this ADR was accepted (2026-09-30); as of 2026-10-03, the maintainer has authorized continued M6 harness engineering, currently WIP, with loopback socket tests and one user-local SIPp 3.6.0 UAS interoperability smoke evidence, but still no reSIProcate/product-target measurements, and real target-stack capacity measurement has not yet begun.
- **The testbed has its own maintenance cost, and its failure mode is silent.** Simulators must evolve with real network-element behavior; once simulation and real network elements diverge, "simulation passed" becomes false evidence — it is still green, but what it proves is no longer true. This cost has no automated means of elimination; it can only be mitigated by periodically reviewing against real network-element behavior.
- **v1 does not open the testbed to customers, which means customer acceptance testing must use other means.** This is a **delivery boundary** and must be stated at the planning stage, not discovered at the acceptance stage. Whether to open it is decided by D6 (M8).
- **Some baselines have not yet been captured.** S5 / S6 / S7a / S8 were decided in M1 as "derived baselines" (assertions derived from `S1-basic-call`, not captured separately); S10 / S11 are README-only, awaiting M2 probe completion. These two decisions are recorded in `docs/plan.md` §3's M1 decision table; they do not block this ADR, but mean current baseline coverage is incomplete.
- **The probes currently produce no evidence.** The `testbed/probe/` E1 / E4 probes are **not executed** because this environment lacks reSIProcate's Python bindings (exit code 2, not skip); the E5 probe has not been written.

## Alternatives considered

| Option | Why not |
|---|---|
| Follow the POC's driven-callback harness for capacity measurement | Bypasses the socket and event loop, measuring business logic not the system; the capacity baseline is not comparable, cannot judge whether CPS hits the wall, nor adjudicate whether the stack suffices |
| Contracts layer only, no simulated peers | S-CSCF / S-SBC are the operator's network elements, not available locally; without simulation, integration tests have nowhere to run |
| Simulation only, no declarative contracts | Simulation verifies "can it run through", not "are the implementations equivalent"; cross-implementation porting loses its common anchor (ADR-0012) |
| Make the testbed a v1 deliverable (customers use it for acceptance) | Architecture doc §11.4 explicitly defers to v1.1; whether customer acceptance testing must be supported is open item D6 (M8), and this ADR does not decide D6 on its behalf |
| Let production code reuse the testbed's simulators / contract loader | Violates `AGENT.md` §4: the testbed is an R&D asset, never a runtime dependency; the direction can only be testbed → platform |
| Three-layer testbed + real-socket load testing + not a v1 deliverable (this decision) | Adopted |

## Evidence

- `testbed/README.md` three-layer table verbatim: "① Contracts / unit | `contracts/` + each package's `tests/` | the decision is correct, and every implementation is consistent"; "② Simulated integration | `simulators/` | AS can work against something that behaves like the operator's peer"; "③ Performance | `load/` | where exactly the capacity boundary lies". Same file's rules verbatim: **"Load testing must go through real sockets.** A harness that drives callbacks directly measures business logic, not capacity." "v1 does not deliver the testbed as a deliverable. **It is an R&D asset; customer acceptance testing capability is left to v1.1." "SIPp may be used here. It is GPL, for **internal use only, never distributed with the product**."
- `testbed/load/README.md` verbatim: **"Load testing goes through real sockets.** The POC's harness drives callbacks directly, bypassing the socket and event loop — it measures business logic, not the system. Figures from such a harness cannot answer "has CPS hit the wall", and therefore cannot decide whether Go is needed (ADR-0014)." Same file: "By stack: CPS, concurrent sessions, call setup latency — and the resource that saturates first. This is input to O1 and ADR-0011; it is not a marketing figure, and is not published before M6." Historical clarification: the above quotes reflect the README / stack-selection context when ADR-0014 was accepted on 2026-09-30; ADR-0019 has since selected reSIProcate, so the current M6 measurements serve O1 and operational capacity planning, and do not reopen stack selection without a new ADR.
- `AGENT.md` §4 layering diagram verbatim: `testbed/ ──may use──▶ platform/ R&D asset, never a runtime dependency`; it also records "**The kernel must never import applications, services, or testbed.** …… enforced by `platform/tests/test_library_independence.py`".
- `AGENT.md` §2 non-goal verbatim: "**No capacity figures are published before M6 measures them.** Before real-socket load testing measures it, no CPS or concurrency figure is published." §6 test strategy table: "Capacity | `performance` | real sockets only. Never measure by driving callbacks — that measures business logic, not the system (ADR-0014)".
- Architecture doc §11.4 "Test platform" key points verbatim: 1. "**Performance testing must be upgraded from "driving callbacks" to "real-socket load testing"**: the existing `CapacityDriver` calls callbacks directly, bypassing the socket and event loop, measuring business logic rather than system capacity. If the capacity baseline is not comparable, there is no way to judge "whether CPS hits the wall", and thus no way to adjudicate whether Go suffices." 2. "**Simulated network elements are first-class assets**……the iFC chain and S-SBC transparent bridging behavior must be simulatable, otherwise integration tests have nowhere to run." 4. "⏳ **v1 does not treat the testbed as a deliverable**, only as an R&D asset; customer acceptance testing capability is left to v1.1."
- Architecture doc §0 decision ledger entry 16 verbatim: "Test platform | testbed three layers; v1 is not a deliverable".
- `docs/plan.md` §2.1 directory structure verbatim: "`testbed/` ⑥ contracts/ (data) · simulators/ · load/".
- `docs/plan.md` §5.2 open item D6 verbatim: "must the testbed support customer acceptance testing in v1 | M8 | the architecture doc defers it to v1.1"; §5.1 O1 verbatim: "Capacity target: CPS, concurrent sessions, setup latency budget……**still an open item** …… M6's measurements, after the harness runs on real sockets"; §4 M6 row: "**Capacity research** | real-socket load-testing harness; measure CPS, concurrent sessions, setup latency — per stack | Not started | produces O1's answer; assume no target before this runs".
- `docs/plan.md` §3 M1 baseline decision table: S5 / S6 / S7a / S8 **accepted as "derived baselines"** (assertions derived from `S1-basic-call`, "re-capturing adds no information, only maintenance surface"); S10 / S11 **accepted as "M2 probe completion"** (consistent with PRD §2.4's known-gaps table). Derived assertions are already executable: `testbed/simulators/tests/test_derived_baseline.py` (marker `contract`).
- `testbed/probe/README.md` current status verbatim: "**Current status: neither probe has been executed.** This environment has no Python bindings for reSIProcate (build option `BUILD_PYTHON=ON` was not built)……fails loudly with exit code 2 and prints build guidance; never silently skips"; the E5 probe is "not yet written, listed as a follow-up item".
- **REQ position remark (history)**: when accepted on 2026-09-30, `Responds to REQ` was mistakenly written as REQ-NF-13. In PRD v0.2, REQ-NF-13 is OTel ([ADR-0005](0005-observability-otel.md)). **On 2026-10-05**, [REQ-NF-15](../../requirements/req-nf-15-testbed-performance.md) was added and plan D8 closed; retroactively, REQ-NF-15 governs.

## Related

- [ADR-0012](0012-cross-implementation-parity.md) Language-agnostic contract + cross-implementation parity — the consumer of the contracts layer
- [ADR-0019](0019-sip-stack-selection.md) Production SIP stack selection — `testbed/probe/` is its E1 / E4 evidence source
- [ADR-0003](0003-s-sbc-transparent-bridge.md) Single ISC access semantics — the behavior the simulation layer must simulate
- [ADR-0015](0015-engineering-discipline.md) Engineering discipline — the attribution layers of the three markers `contract` / `integration` / `performance`
- [`../system-architecture.md`](../system-architecture.md) §11.4 test platform, §12.1 open item O1, §12.2 risk R9
- Open items O1 (capacity target / M6) and D6 (whether the testbed supports customer acceptance testing / M8) — both **undecided**
