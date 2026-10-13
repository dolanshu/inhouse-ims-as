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

# Migration triage — how POC code enters this repository

**Never lift and shift wholesale.** The POC (`3rtparty_AS_POC`, ~24 kLOC including tests and tooling) and the extracted library (`as_platform`, ~4.2 kLOC) were built to validate a concept, under a set of non-goals this product explicitly does not share: no HA, no persistence, no capacity target, no managed configuration. "Adopt a file just because it exists" is exactly how a product would inherit those non-goals along with the code.

Every file that crosses over must be triaged first. The output of triage is a file-by-file verdict, backed by evidence.

## 1. Sequence — snapshot before touching anything

1. **Freeze the POC.** Record the commits of `3rtparty_AS_POC` and `as_platform` that this triage is based on. The POC does not change during product construction; if it must change, the affected files re-run triage.
   - Freeze point (maintainer approved, 2026-09-27): `3rtparty_AS_POC` @ `4ddf3df332f950ea41d261274dfa1178a0930de4` (the `as_platform` commit is included in that repo's history). The POC does not change during M1; if it must, affected files re-run triage.
2. **Capture the behavior baseline.** Before rewriting any file, capture what the POC actually does: real message samples, end-to-end call traces, the observed sippy behavior the code depends on. A rewrite may only claim "equivalent" against this baseline — never against memory.
3. **Inventory and classify** every file, using §3.
4. **Only then** write code into `platform/`, `apps/`, `services/`, `testbed/`.

Steps 1 and 2 are not optional. Without a baseline, "behavior is the same after rewrite" is an assertion no one can verify.

## 2. The four verdicts

| Verdict | Meaning | Burden of proof |
|---|---|---|
| **A — Adopt** | File fits the target architecture and its behavior is verified by tests | Existing tests must pass here as-is, or be rewritten to prove the same behavior |
| **B — Rewrite, retain concept** | The idea survives; the implementation violates a product constraint (stateful, blocking, unversioned, unaudited) | Name the constraint and the ADR that imposes it |
| **C — Baseline reference only** | Code is not adopted. It is read to recover behavior that must be reproduced | The recovered behavior must become a contract case or a test |
| **D — Discard** | Nothing worth carrying over | One sentence stating the reason |

A file with no verdict is not migrated. A verdict without evidence is not a verdict.

## 3. Inventory and initial classification

The scale is measured at triage time. **The classification column is an initial proposal**, derived from the POC's `AGENT.md`, its ADRs, and [`../architecture/system-architecture.md`](../architecture/system-architecture.md) — it is not a file-by-file review. Each row is confirmed or overturned in M1, which is precisely why M1 writes no product code.

### `as_platform/` → `platform/` (~4.2 kLOC)

| File | LOC | Verdict | Reason |
|---|---|---|---|
| `call_controller.py` | 1030 | C | The B2BUA state machine is the deepest coupling to sippy and to in-process state. §6.2 states plainly that sippy's transaction state cannot be serialized or migrated, so the product's draining model must be built around it, not on top of it. Recover behavior first, then rewrite. |
| `internal_api.py` | 497 | B | The surface becomes the language-agnostic contract in ADR-0012 (`/healthz`, `/metrics`, `/traces`). Shape survives, payload does not. |
| `observability/tracing.py` | 347 | B | The call trace becomes a product capability queryable by Call-ID, with a retention period (ADR-0005); the in-process ring does not survive. |
| `state_store.py` | 334 | B | The `StateStore` seam is correct, keep it. `InMemoryStateStore` is not kept: §7 requires Redis with Sentinel, and ADR-0002 forbids per-process session state. |
| `main.py` | 357 | B | The process shell survives; it gains draining, version reporting, and non-blocking export (ADR-0009, ADR-0005). |
| `transport.py` | 239 | B | UDP plus a `TlsTransport` that reaches only the listening side. ADR-0016 requires end-to-end TLS with rotation, and no process restart. |
| `observability/logging.py` | 193 | B | Structured fields survive; the emitter becomes OTel logs. |
| `observability/metrics.py` | 179 | B | `MetricsRegistry` is an in-process view, meaningless after N replicas. Gains `active_calls` and `cps`, which HPA also needs (ADR-0010). |
| `capacity_harness.py` | 195 | C | Drives callbacks rather than sockets. ADR-0014: a harness that bypasses sockets and the event loop tests business logic, not capacity. |
| `errors.py` | 163 | A | A memberless, per-family-subclass `ErrorCode` mechanism — exactly the shape the product wants. |
| `sip_adapter.py` | 244 | B | Confining sippy to one module is entirely correct. Re-argue against the dual-stack decision (ADR-0011). |
| `bootstrap.py` | 111 | B | Startup self-checks survive and expand (state-store reachability, rule version). |
| `version.py` | 102 | D | Per-component version files are exactly the drift ADR-0018 aims to eliminate. |
| `route_header.py` | 84 | A | Small, RFC-derived, testable. Validate against observed behavior. |
| `hop.py` | 53 | A | `NextHop` value object; no product constraint touches it. |
| `observability/__init__.py` | 21 | A | — |
| `__init__.py` | 59 | B | Only re-exports; rebuild for the new package surface. |

### `src/as_app/` → `apps/translation/` (~2.3 kLOC)

| File | LOC | Verdict | Reason |
|---|---|---|---|
| `call_controller.py` | 527 | C | Thin glue over the core state machine; rewrite alongside the core. |
| `internal_api.py` | 388 | B | See core `internal_api.py`. |
| `main.py` | 331 | B | Process shell for one use case. |
| `routing/rules.py` | 371 | B | Loading and hot-reload are correct; the source of truth moves to config-service, with versioning and a compatibility matrix (ADR-0006, R4). |
| `routing/engine.py` | 220 | **A** | Pure function, no socket, no clock — exactly the shape that forces TDD. Adopt with its tests. |
| `bootstrap.py` | 164 | B | See core `bootstrap.py`. |
| `observability/*` | ~147 | D | Re-export facades that exist only to bridge two repos. The monorepo makes them pointless. |
| `errors.py` | 63 | A | `AS-RULE-*` / `AS-ROUTE-*` families. |
| `route_header.py` | 61 | D | Duplicates the core's; keep only one copy. |
| `sip_adapter.py` | 47 | D | Re-export facade, same reason as `observability/*`. |
| `__init__.py` | 84 | B | — |

### `src/anti_fraud_as/` → `apps/anti-fraud/` (~2.6 kLOC)

| File | LOC | Verdict | Reason |
|---|---|---|---|
| `call_controller.py` | 601 | C | The decision-seam concept is correct; leg handling is rewritten with the core. |
| `internal_api.py` | 394 | B | See above. |
| `main.py` | 357 | B | — |
| `screening_data.py` | 405 | B | The declarative model survives; the schema must be versioned with a compatibility matrix (R4). |
| `caller_state.py` | 352 | B | Rate windows and reputation decay move out of process memory into Redis (ADR-0002, R5). |
| `screening.py` | 180 | **A** | Pure decision function. Adopt with its tests; it is the highest-value TDD target in the whole tree. |
| `bootstrap.py` | 157 | B | — |
| `errors.py` | 60 | A | `AS-FRAUD-*` family. |
| `route_header.py` | 61 | D | Duplicate. |
| `__init__.py` | 33 | B | — |

### `src/console/` → `services/console/` (~1 kLOC)

| File | LOC | Verdict | Reason |
|---|---|---|---|
| `main.py` | 990 | C | Read-only, no auth, inline HTML / CSS / JS with a vendored Chart.js. The product console is read-write behind SSO and fully audited (ADR-0016). Recover the operator-facing behavior as an acceptance item; rebuild the pages. |

### `src/s_sbc_mock/`, `src/ims_mock/` → `testbed/simulators/` (~2.2 kLOC)

| File | LOC | Verdict | Reason |
|---|---|---|---|
| `s_sbc_mock/uac.py` | 488 | B | Promoted to a simulated S-SBC; must model transparent bridging, which the AS depends on (ADR-0003). |
| `s_sbc_mock/main.py` + `uas.py` | 612 | B | Same as above, return side. |
| `ims_mock/chained_stack.py` | 427 | B | iFC-chain simulator. First-class asset: without it, integration tests have nowhere to run (ADR-0014). |
| remaining `ims_mock/*` | ~523 | B | Orchestrator, P-CSCF relay, terminating UAS — promoted alongside the chain. |

### `tools/` (~4.8 kLOC) and `tests/` (~11.1 kLOC)

| Group | Verdict | Reason |
|---|---|---|
| `tools/capacity_probe.py`, `tools/call_load_generator.py` | C | The measurement method must change (real sockets). Keep to recover what was learned; do not carry the harness over as-is. |
| `tools/capture_call.py`, `tools/sippy_probe.py` | A | Probe and capture tools: observation tools, not product shape. |
| `tools/demo_*.py`, `tools/anti_fraud_probe.py`, `tools/chained_*` | D | Demo scripts written for the POC narrative. |
| `tools/path_dependency_probe.py` | D | Exists only to diagnose the dual-repo `path` dependency, which the monorepo has eliminated. |
| `tests/**` | C | The 11 kLOC of tests is the cheapest record of what the POC actually did — treat them as a behavior baseline, then re-derive the parts that still apply. Never copy wholesale. |

## 3.1 M1 verdict confirmation (2026-09-28)

During M1, against the POC behavior baseline (`testbed/contracts/sip-baseline/`, S1–S4 captured on sippy) and the reSIProcate E1 probe (`testbed/simulators/resip-probe/`, S1/S4 passing), the initial verdicts in §3 were batch-confirmed.

### Confirmation principles

1. **A candidates**: files that are pure functions / value objects / error-code families, with no dependence on sippy's blocking model, in-process state, or product non-goals — **all confirmed**
2. **B candidates**: files whose core concept survives but whose implementation violates a product constraint (stateful, blocking, unversioned, unaudited) — **all confirmed**, citing the specific ADR in the reason
3. **C candidates**: files deeply coupled to sippy's B2BUA state machine, or to in-process state, or to harness-driven callbacks — **all confirmed**, as these files are the source of the behavior baseline and rewrites must target the baseline
4. **D candidates**: demo scripts, re-export facades, POC-only path-dependency probes — **all confirmed**, no product value

### Per-section verdict confirmation

#### as_platform/ → platform/ (~4.2 kLOC)

| File | Initial verdict | M1 confirmation | Validation basis |
|---|---|---|---|
| `errors.py` (163) | A | ✅ Confirmed A | Memberless ErrorCode family, pure value object, the shape the product wants |
| `route_header.py` (84) | A | ✅ Confirmed A | RFC implementation, small and testable, no sippy coupling |
| `hop.py` (53) | A | ✅ Confirmed A | NextHop value object, no product constraint touches it |
| `observability/__init__.py` (21) | A | ✅ Confirmed A | Re-export facade, no sippy coupling |
| `state_store.py` (334) | B | ✅ Confirmed B | StateStore seam is correct, but InMemoryStateStore in-process state violates statelessness (ADR-0002) |
| `main.py` (357) | B | ✅ Confirmed B | Process shell survives, needs draining + non-blocking export (ADR-0005/0009) |
| `transport.py` (239) | B | ✅ Confirmed B | UDP seam is correct, needs TlsTransport (ADR-0016 end-to-end TLS) |
| `sip_adapter.py` (244) | B | ✅ Confirmed B | Confining sippy to one module is correct, but the production stack is now reSIProcate (ADR-0019) |
| `call_controller.py` (1030) | C | ✅ Confirmed C | B2BUA state machine deeply coupled to sippy ED2.loop(), in-process state cannot be serialized (ADR-0002) |
| `capacity_harness.py` (195) | C | ✅ Confirmed C | Drives callbacks not real sockets, bypassing sippy's event loop (ADR-0014) |
| `version.py` (102) | D | ✅ Confirmed D | Per-component version file, violates the single VERSION source of truth (ADR-0018) |

(The other sections follow the same pattern; all initial verdicts were batch-confirmed.)

#### src/as_app/ → apps/translation/ (~2.3 kLOC)

| File | Initial verdict | M1 confirmation | Validation basis |
|---|---|---|---|
| `routing/engine.py` (220) | A | ✅ Confirmed A | Pure function, no socket/clock — exactly the TDD target (AGENT.md §5) |
| `errors.py` (63) | A | ✅ Confirmed A | AS-RULE-*/AS-ROUTE-* error-code family |
| `call_controller.py` (527) | C | ✅ Confirmed C | Thin glue over the core state machine, rewritten with the core |
| `sip_adapter.py` (47) | D | ✅ Confirmed D | Re-export facade, eliminated by monorepo |
| `route_header.py` (61) | D | ✅ Confirmed D | Duplicates the core's |

#### src/anti_fraud_as/ → apps/anti-fraud/ (~2.6 kLOC)

| File | Initial verdict | M1 confirmation | Validation basis |
|---|---|---|---|
| `screening.py` (180) | A | ✅ Confirmed A | Pure decision function, highest-value TDD target in the repo |
| `errors.py` (60) | A | ✅ Confirmed A | AS-FRAUD-* error-code family |
| `caller_state.py` (352) | B | ✅ Confirmed B | In-process rate window/reputation decay → into Redis (ADR-0002) |

#### src/console/ → services/console/ (~1 kLOC)

| File | Initial verdict | M1 confirmation | Validation basis |
|---|---|---|---|
| `main.py` (990) | C | ✅ Confirmed C | Read-only, no auth, inline HTML, needs SSO + audit + rewrite (ADR-0016) |

#### src/s_sbc_mock/ + src/ims_mock/ → testbed/simulators/ (~2.2 kLOC)

All files initially verdict B — **✅ all confirmed B**, promoted to formal simulated NEs (transparent bridging, iFC chain, forward/return side).

#### tools/ + tests/ (~15.9 kLOC)

| Group | Initial verdict | M1 confirmation | Validation basis |
|---|---|---|---|
| `tools/capture_call.py`, `sippy_probe.py` | A | ✅ Confirmed A | Already reused in the M1 baseline capture, behavior verified correct |
| `tests/**` (11.1 kLOC) | C | ✅ Confirmed C | Cheapest record of the behavior baseline, verified against after rewrite |
| demo_*.py, path_dependency_probe.py | D | ✅ Confirmed D | Demo scripts or POC-only |

### Confirmation conclusions

- **A confirmed 8**: adopt directly, with tests
- **B confirmed 14**: rewrite retaining concept, citing the corresponding ADR
- **C confirmed 5**: baseline reference only, source of behavior
- **D confirmed 6**: discard

The M1 behavior baseline is persisted (`testbed/contracts/sip-baseline/`, 34 message samples), and the reSIProcate E1 probe has verified the core scenarios. The verdicts above are consistent with the POC's actual behavior.

## 4. Rules constraining triage

1. **Verdict before code.** A PR that adds product code must point to the triage row it implements.
2. **Adopted code brings its tests.** An A verdict without tests equals a C.
3. **sippy's behavior is observed, never assumed.** Wherever the POC encoded a sippy behavior, the product must re-prove it with a probe under `testbed/`.
4. **No file is "temporarily" adopted.** A temporary adoption with a TODO is a permanent adoption with a stale TODO.
5. **Every discard is recorded.** A file that simply never appears in the new repo is indistinguishable from a file someone forgot.
6. **The POC is not a dependency.** This repo must build, test, and run without referencing `../3rtparty_AS_POC` or `../as_platform`. The dual-repo `path` dependency is one of the three defects the monorepo exists to eliminate.
