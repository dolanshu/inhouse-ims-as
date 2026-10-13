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

# ADR-0019: Production SIP stack selection (overturning ADR-0011's stack premise)

- **Number**: ADR-0019
- **Status**: **Accepted** — reSIProcate selected
- **Date**: 2026-09-28
- **Accepted date**: 2026-09-28
- **Supersedes**: the "production stack = sippy" premise established by [ADR-0011](0011-sip-stack-dual-path.md) (ADR-0011's dual-stack parallel framework remains valid)
- **Related**: architecture decisions 8, O1, O2, O3, D1, D2; ADR-0011; [`capacity-estimate.md`](../capacity-estimate.md); [`docs/SIP_stack_selection.md`](../../SIP_stack_selection.md)
- **Responds to REQ**: implicitly responds to all REQ-F-* (the SIP stack is the infrastructure for all signaling features)

---

## 1. Background and problem

Architecture decision 8 and [ADR-0011](0011-sip-stack-dual-path.md) established "dual-stack parallel": sippy holds production, `go-b2bua` pilots.
The implicit premise of that decision was **sippy continuing as the production stack**.

The maintainer now explicitly overturns this premise: **sippy exits the production stack**.
What the production stack will use is not yet decided; candidates include `go-b2bua` (Go) and C/C++-family stacks.

Until this decision is complete, M2 (`platform/` kernel) cannot start — because the kernel's SIP adaptation layer
is stack-dependent, and writing it early would write code that must later be overturned. This ADR therefore **blocks M0 signoff**.

### 1.1 Why capacity cannot be the rationale

[`capacity-estimate.md`](../capacity-estimate.md) concludes: **capacity is not a differentiator among candidate stacks**.
The selection design target is ≥500 CPS / ≥20,000 concurrent dialogs; under a "multi-replica + stateless" architecture,
even sippy's nominal capacity (single-process 150–400 CPS) split across 4 replicas is sufficient.

So this ADR's decision basis is **not performance** but maintainability and supply-chain risk.
The capacity-estimate document independently owns the conclusion "capacity is not a differentiator"; this ADR merely cites it.

---

## 2. Decision basis (the real rationale)

| # | Rationale | Explanation |
|---|---|---|
| R1 | **Upstream activity / supply-chain risk** | sippy has a single maintainer, key issues long unclosed; the product is delivered on a 10-year lifecycle and cannot pin its production signaling plane on a dependency with no clear roadmap |
| R2 | **Runtime lifecycle** | sippy's validated Python 3.10 reaches EOL in 2026-10 (open item D1). Switching stacks can incidentally release the runtime lock |
| R3 | **Maintainability and troubleshooting ability** | Productization requires being able to read source, patch, and locate signaling issues on-site. The single-process GIL model and Python 2 lineage raise this cost |
| R4 | **Operational form** | A single-node static binary is superior to a multi-process Python runtime (carrier on-prem delivery, limited ops headcount) |

### 2.1 R1 evidence table

Capture date: 2026-09-28.

| Source | Repo URL | Commits in last 12 months | Open issues/PRs | Oldest open issue | Most recent release |
|---|---|---|---|---|---|
| sippy (Python) | <https://github.com/sippy/b2bua> | 50 | 28 | 2014-09-13 | v2.4.2 (2026-07-15) |
| go-b2bua | <https://github.com/sippy/go-b2bua> | 5 | 3 | 2023-09-06 | no release (latest commit 2026-06-05) |

> Note: the sippy main repo still has maintenance commits, but the core author is single, historical issues are heavily backlogged, and productization capabilities such as TLS hot rotation and state serialization have no upstream roadmap; go-b2bua has even lower activity. Under a 10-year lifecycle this constitutes a supply-chain risk rather than a short-term activity risk.

---

## 3. Candidate scope

Filtered from [`docs/SIP_stack_selection.md`](../../SIP_stack_selection.md) by hard constraints.

### 3.1 Hard constraints (eliminated if not met)

| Constraint | Meaning | Capability owner | Basis |
|---|---|---|---|
| **H1 License** | Closed-source commercial distribution needs no paid license | Stack-native | Product is a commercial delivery; GPL/AGPL/dual-license out |
| **H2 vendoring** | Can pin to a specific commit/tag and vendor into the repo | Stack-native / self-built | `AGENT.md` §8 dependency governance |
| **H3 pure signaling stack** | B2BUA semantics, maintains complete call state, no media | Stack-native | Architecture §2 non-goals, decision 4 |
| **H4 TLS + certificate hot rotation** | Supports SIP over TLS; certificate rotation does not restart the process or drop in-flight calls | Stack-native / self-built / combined; probe-verified | `AGENT.md` §13 |
| **H5 state externalizable** | Dialog/transaction state is serializable and recoverable, not forced to bind single-process memory | Stack-native / self-built / combined; design review or probe-verified | Architecture §2/§4, decision 2 |

> Capability-owner note: "stack-native" means the capability is provided by the stack itself; "self-built" means implemented by our team outside the stack; "combined" means the stack provides part of the mechanism and the team fills the rest.

### 3.2 Candidates entering evaluation

| Candidate | Language | License | Capability-owner note | Remarks |
|---|---|---|---|---|
| **go-b2bua** | Go | BSD-2-Clause | stack-native | Official port by the sippy author, **same lineage as the POC behavior baseline**; no release, requires commit pin + vendoring |
| **reSIProcate** | C++ | Vovida (BSD-like) | stack-native / self-built | In commercial use by Sipwise NGCP, CounterPath; the TCP/TLS transport layer is a known weak point, **kept or dropped per the TLS probe** |
| **libre** | C | BSD-3-Clause | stack-native / self-built | creytiv lineage, still frequently released in 2025 (libre 4.3.0); takes the SIP/SDP parts, **baresip carries a media module and is not a candidate** |

### 3.3 Explicitly excluded

| Excluded | Reason |
|---|---|
| PJSIP | GPLv2 / commercial dual-license (violates H1) |
| Belle-SIP / Flexisip | GPLv3 / AGPLv3 (violates H1) |
| Kamailio / OpenSIPS | GPL and proxy/server platforms, not bare stacks (violate H1, H3) |
| FreeSWITCH / Asterisk | Full media stacks, conflict with "no media" (violate H3) |
| Sofia-SIP | LGPL, commercial obstacle (H1 edge); and a pure stack but unfavorable license |
| **rsipstack** | MIT and a pure stack, but **Rust is not in the current team's tech stack**; learning and troubleshooting cost is a **veto**, not entering formal candidacy |
| oSIP / eXosip2 | GPL; low activity |
| Doubango | The only 3GPP TS 24.229 implementation, but reportedly stopped updating around 2016 (violates R1) |
| drachtio | MIT but is a server + Node.js framework, not a bare stack (H3 mismatch) |
| JAIN-SIP | NIST explicitly does not guarantee continued support (violates R1) |
| **sippy** | The premise of this ADR is to exclude it as the production stack; retained as a `testbed/` baseline reference |
| **fork / vendor sippy** | Vendoring does not release R3 (Python GIL / single-process model) or R4 (multi-process Python operational form); maintenance responsibility still falls on our team, and D1 cannot be resolved |

---

## 4. Evaluation matrix

| Dimension | Pass criterion | Weight |
|---|---|---|
| **E1 behavioral equivalence** | Real-socket replay reproduces the POC baseline (§5 scenarios) | **Threshold**, out if not met |
| **E2 license** | Closed-source commercial distribution needs no license | Hard constraint |
| **E3 vendoring** | Can commit pin + vendor | Hard constraint |
| **E4 TLS and hot rotation** | Supports SIP over TLS; certificate rotation does not restart or drop in-flight calls | Hard constraint |
| **E5 state externalizable** | State is serializable/recoverable, or the stack itself is stateless multi-replica | Hard constraint |
| **E6 build integration** | Can enter the monorepo build and gate (Go module / cmake / autotools) | Medium |
| **E7 upstream activity** | Commits in last 12 months; issues get responses | High |
| **E8 maintainability** | Weighted composite by §4.1 sub-items (code volume / build complexity / debugging toolchain / log and state export / community docs / skill match) | High |
| **E9 baseline lineage** | Degree of comparability with the POC (sippy) behavior — determines M1 baseline reuse value [^e9] | High |
| **E10 capacity reference** | Nominal capacity covers ≥500 CPS / ≥20,000 concurrent (incl. multi-replica) | **Low** (§1.1: not a differentiator) |
| **E11 language coupling** | The degree to which the stack's implementation language couples to the project's main language (Python) — determines whether the platform kernel must change language or introduce a cross-language FFI bridge | **High** |

[^e9]: E9's high weight is an intentional tilt reflecting M1 baseline reuse value, but E9 **must not alone constitute a selection rationale**; it must be weighed against dimensions like E8.

### 4.1 E8 (maintainability) scoring criteria

E8 is not a single-dimension score; it is split into the following sub-items; each scored 0–5 (5 best), weighted into the E8 composite.

| Sub-item | Scoring criteria | Weight |
|---|---|---|
| Code volume (LOC) | Fewer core-path LOC is better | Medium |
| Build complexity | Number of build-system kinds + external dependencies, fewer is better | Medium |
| Debugging toolchain | Whether it natively supports gdb / lldb / pprof etc. | High |
| Log and state export granularity | Whether there are readable logs and exportable / serializable state | High |
| Community documentation quality | Whether there are normative docs, examples, and maintenance guides | Medium |
| Team current skill match | Overlap with the team's current tech stack | High |

The E8 composite = the weighted sum of each sub-item's score. The "tiebreak by E8 team match" in §6 step 3 uses this table as the basis.

### 4.2 Candidate paper-evaluation table

Data capture date: **2026-09-28**. This table is a paper evaluation; **all dimensions involving runtime behavior (E1, E4, E5) require later probe replay verification**, and paper conclusions are not the final basis.

| Dimension | go-b2bua (Go) | reSIProcate (C++) | libre (C) |
|---|---|---|---|
| **E1 behavioral equivalence** | pending probe (threshold) | pending probe (threshold) | pending probe (threshold) |
| **E2 license** | ✅ pass (BSD-2-Clause) | ✅ pass (Vovida, BSD-like) | ✅ pass (BSD-3-Clause) |
| **E3 vendoring** | ✅ pass (Go module + commit pin) | ✅ pass (CMake + submodule / source vendor) | ✅ pass (CMake + submodule / source vendor) |
| **E4 TLS and hot rotation** | ⚠️ paper pass / pending probe | ⚠️ paper pass / pending probe | ⚠️ paper pass / pending probe |
| **E5 state externalizable** | ⚠️ paper pass / pending probe | ⚠️ paper pass / pending probe | ⚠️ paper pass / pending probe |
| **E6 build integration** | 5 | 3 | 4 |
| **E7 upstream activity** | 2 | 4 | 5 |
| **E8 maintainability (weighted composite)** | **3.4** | **3.0** | **2.7** |
| **E9 baseline lineage** | 5 | 1 | 1 |
| **E10 capacity reference** | 4 | 5 | 4 |
| **E11 language coupling** | 1 | 4 | 3 |

**Scoring notes**

**Hard-constraint dimensions (E2/E3/E4/E5)**

- **E2 license**: All three are BSD-family licenses; closed-source commercial distribution needs no paid license, satisfying H1.
  - go-b2bua: BSD-2-Clause, see [LICENSE](https://github.com/sippy/go-b2bua/blob/master/LICENSE).
  - reSIProcate: Vovida Software License v1.0 (OSI-certified, BSD-like), see [COPYING](https://github.com/resiprocate/resiprocate/blob/master/COPYING).
  - libre: BSD-3-Clause, see [LICENSE](https://github.com/baresip/re/blob/main/LICENSE).
- **E3 vendoring**: All three can pin to a specific commit and vendor into the repo, satisfying H2.
  - go-b2bua: Go module natively supports the `replace` directive pointing to a local vendor dir or specific commit.
  - reSIProcate / libre: CMake projects, integrable via `git submodule` or source copy + CMake `add_subdirectory`.
- **E4 TLS and hot rotation** (⚠️ paper judgment, pending probe verification):
  - go-b2bua: TLS is provided by Go stdlib `crypto/tls`, supports a `GetCertificate` callback for hot rotation; but the SIP over TLS transport-layer integration specifically needs probe verification.
  - reSIProcate: supports OpenSSL TLS transport (`TlsTransport`), but the TCP/TLS transport layer is a known weak point; the specific mechanism of certificate hot rotation (whether non-restart rotation is supported, whether in-flight calls are affected) needs probe verification.
  - libre: supports OpenSSL TLS transport (`tls` module); certificate hot rotation needs to be self-built at the application layer (the lower stack provides a TLS context management interface); probe verification of feasibility needed.
- **E5 state externalizable** (⚠️ paper judgment, pending probe verification):
  - go-b2bua: state is in-process, needs self-built serialization; ported by the sippy author, behavior model consistent with sippy, theoretically referenceable to sippy's serialization scheme, but specific complexity needs probe verification.
  - reSIProcate: the dum layer has dialog management (`DialogSet` / `Dialog`), and the stack itself has a stateful object model; whether complete serialization/deserialization (incl. transaction state) is supported needs probe verification.
  - libre: a lower stack; dialog state must be fully self-built in the upper application; high flexibility but large workload, needs probe verification of self-build cost.

**Normal dimensions (E6/E7/E9/E10)**

- **E6 build integration** (medium weight):
  - go-b2bua (5): Go module, single language, zero external system dependencies, `go build` produces a static binary, smoothest monorepo build integration.
  - reSIProcate (3): CMake build but with multiple sub-libraries (resip / dum / recon / rutil etc.), more external dependencies (OpenSSL, popt, c-ares etc.), build integration needs dependency-chain maintenance.
  - libre (4): CMake build, relatively clear structure; depends on base libraries like OpenSSL; needs to carve the SIP/SDP core out of the baresip ecosystem, slightly increasing integration cost.
- **E7 upstream activity** (high weight):
  - go-b2bua (2): ~5 commits in last 12 months, no release, 3 open issues, oldest issue 2023-09-06; low activity, high supply-chain risk. Source: [GitHub repo](https://github.com/sippy/go-b2bua).
  - reSIProcate (4): continuous commits in last 12 months, released 1.14.0 on 2026-06-18, issues get responses; commercial users like Sipwise NGCP, CounterPath; medium-to-high activity. Source: [GitHub repo](https://github.com/resiprocate/resiprocate).
  - libre (5): frequent releases, multiple 2025 releases (libre 4.x), still updating in 2026 (Fedora 45 has packaged 4.11.0); active baresip ecosystem, healthy community. Source: [GitHub repo](https://github.com/baresip/re).
- **E9 baseline lineage** (high weight):
  - go-b2bua (5): same author as sippy (POC baseline), highly consistent behavior model, maximum M1 baseline reuse value.
  - reSIProcate (1): independent implementation, no blood relation to sippy, behavior comparison must be built from scratch.
  - libre (1): independent implementation, a lower stack, dialog semantics must be self-built at the upper layer, largest behavior-model gap from sippy.
- **E10 capacity reference** (low weight, record only):
  - go-b2bua (4): Go's concurrency model natively supports high concurrency, single-process estimate of 500+ CPS feasible; specific numbers pending probe.
  - reSIProcate (5): C++ implementation, commercially validated at large-scale deployments, ample capacity.
  - libre (4): C implementation, excellent performance, but the upper layer must self-build dialog management, overall capacity depends on the upper-layer implementation.
- **E11 language coupling** (high weight):
  - go-b2bua (1): stack is Go, no cross-language binding. 70–80% of the platform signaling plane needs rewriting in Go, with Python relegated to the rule engine and control plane. The project goes from single-language (Python) to dual-language (Python + Go), maintaining two toolchains, two test frameworks, two debugging flows.
  - reSIProcate (4): stack is C++, **ships Python bindings** (build option `BUILD_PYTHON=ON`). The platform kernel can stay fully Python, with the SIP adaptation layer directly `import`ing the reSIProcate Python module, no hand-written FFI bridge needed. The language boundary is maintained upstream, debugging completable on the Python side.
  - libre (3): stack is C, has a C API. The platform kernel can stay fully Python, but the SIP adaptation layer needs a **hand-written `ctypes` bridge** — type conversion, memory management, and error propagation all must be maintained ourselves. One more hand-written FFI cost than reSIProcate, but still no language change needed.

**E8 maintainability (weighted composite)**

E8 is scored separately on the six sub-items of §4.1, weight conversion: high=1.0, medium=0.5; Σweight = 4.5.
Detailed calculation process in the table below (each sub-item 0–5):

| E8 sub-item | Weight | go-b2bua | reSIProcate | libre |
|---|---|---|---|---|
| Code volume (LOC) | Medium (0.5) | 4 | 2 | 4 |
| Build complexity | Medium (0.5) | 5 | 3 | 4 |
| Debugging toolchain | High (1.0) | 4 | 3 | 3 |
| Log and state export granularity | High (1.0) | 2 | 4 | 2 |
| Community documentation quality | Medium (0.5) | 2 | 4 | 2 |
| Team skill match | High (1.0) | 4 | 2 | 2 |
| **E8 composite** | — | **3.4** | **3.0** | **2.7** |

- **go-b2bua**: strength in team skill match (some Go), simple build, small code volume; weakness in log and state export (needs self-build) and community docs (only auto-generated API docs).
- **reSIProcate**: strength in log and state management (complete dum layer) and community docs (commercial-grade); weakness in large code volume (steep learning curve) and team skill match (limited C++ experience).
- **libre**: strength in lean code and clean build; weakness in log/state needing upper-layer self-build, few docs, low team skill match.

> **Paper-evaluation conclusion (not final)**: on the high-weight dimensions E7+E8+E9+E11 the composite ranking is reSIProcate (3.0) > go-b2bua (2.9) ≈ libre (2.9); go-b2bua and libre tie; per §6 step 3's tiebreak rule, the maintainer adjudicates by E8 team match. The gaps are small (0.1-level), and E4/E5 are both paper judgments, E1 unverified. The final ranking needs updating after probe replay.

---

## 5. Minimal replay scenarios (E1 threshold)

Each candidate writes a probe, runs real sockets, and verifies the following behaviors match the POC baseline.
The baseline is captured by M1 in `testbed/` using sippy for S1–S11 and persisted to `testbed/contracts/sip-baseline/`;
the probe requires that baseline to be persisted as an entry condition.

Replay only validates **externally observable message behavior**: method, response code, presence and semantics of key headers, message order;
it does not validate header order, the specific value of Via branch, or SDP `o=` timestamps (implementation details).

**Assertion-granularity table** (field-by-field classification, ensuring probes written by different people reach the same conclusion):

| Granularity | Meaning | Fields |
|---|---|---|
| **Strict equality** | Must match verbatim | Method (`INVITE` / `ACK` / `BYE` / `CANCEL` …), response code (`100` / `180` / `200` / `4xx` …), CSeq method name |
| **Existence only** | Only requires the header to exist, value not compared | whether `To` / `From` tag exists, whether `Contact` exists |
| **Pattern match** | Must match a given pattern, value itself not compared | Via branch starts with `z9hG4bK`; tag is random hex; `Call-ID` is a valid host form (`local-id@host`) |

> `Call-ID` necessarily differs on the two legs (stated in S5), so it is outside the three constraint classes above — judged separately by "the two sides' values must differ."

| # | Scenario | Assertion |
|---|---|---|
| S1 | Basic call | `INVITE → 100 Trying → 180 Ringing → 200 OK → ACK`, then `BYE → 200 OK` |
| S2 | No matching rule | Receive `INVITE` → return `404 Not Found` |
| S3 | Policy rejection | Receive `INVITE` → return `603 Decline` |
| S4 | Caller gives up | `INVITE` not connected, receive `CANCEL` → return `200 OK`, and send `CANCEL` to the callee side |
| S5 | Two-leg B2BUA | UAS leg terminated, UAC leg newly created, **Call-IDs differ** on the two sides |
| S6 | Request-URI / number rewrite | Forward by new URI after rewrite, other headers transparent per rule |
| S7a | SDP fully transparent mode | SDP byte-for-byte unchanged, no field modified, media not anchored |
| S7b | SDP rewrite-by-contract mode | Only rewrite specified fields per contract, other fields unchanged, media not anchored |
| S8 | Route / Record-Route handling | S-CSCF inserts path in `Record-Route` / `Route`; AS preserves that path in in-dialog requests, no loss or misordering of `Route` headers |
| S9 | in-dialog request routing | After dialog established, received `BYE` / `re-INVITE` / `UPDATE` still processed by AS and returned per the `Route` set |
| S10 | Non-2xx branch handling | When callee returns `486 Busy`, `480 Temporarily Unavailable`, `408 Request Timeout`, AS relays the corresponding final response to the caller and cleans up the corresponding leg |
| S11 | CANCEL and final-response race | After caller sends `CANCEL`, if callee simultaneously returns a final response (2xx or 6xx), AS produces no duplicate ACK/erroneous routing; converges per transaction semantics |

### 5.1 Follow-up scenario list (not E1 threshold, progressively completed in M2/M3)

re-INVITE (hold / resume), forking, retransmission timeout, REFER (call-transfer semantics), PRACK / UPDATE interleaving,
`P-Asserted-Identity` and trust-domain allowlist validation.

### 5.2 S12: TLS certificate hot rotation (E4 hard-constraint verification scenario, not E1 threshold)

S12 is not part of the S1–S11 E1 threshold set; it verifies §4 E4 and §3.1 H4. A candidate **must pass** this scenario before entering Accepted,
but it **does not block E1 probe startup**. Assertions (all must hold):

- During rotation, in-flight calls' `BYE` completes normally (`BYE → 200 OK`), call not interrupted;
- After rotation, new calls initiated use the **new certificate** to establish the TLS session;
- The entire rotation process **does not restart the process**;
- No call loss within the rotation window (no abnormal termination, no AS-self-triggered 5xx).

---

## 6. Decision process

0. **Baseline persistence** (precondition for entering probe): M1 phase first uses sippy in `testbed/` to capture S1–S11 baseline,
   persist to `testbed/contracts/sip-baseline/`. Owner: dev/AI agent; the maintainer confirms baseline coverage of S1–S11 before entering step 1.
1. **Paper review** (E2/E3/E4/E5/E7): first eliminate candidates failing hard constraints. Done; results in §3.
2. **Probe replay** (E1): Phase A runs only `go-b2bua` (2-week timebox). If E1 passes and E8 is acceptable,
   it can enter the Accepted flow. C/C++ candidates (reSIProcate / libre) are Phase B,
   started only if `go-b2bua` fails E1, or E8 team match is unacceptable.
   The E1 threshold scenarios are **S1–S11**; **S12 (TLS certificate hot rotation, see §5.2)** verifies the E4 hard constraint,
   does not block E1 probe startup, but a candidate **must pass** before entering Accepted.
3. **Deep evaluation and adjudication** (E6/E8/E9): for candidates passing the E1 threshold, adjudicate by the following rules:
   - E1 is an elimination threshold; those failing are out;
   - among passers, the one with the highest weighted total of E7 / E8 / E9 / E11 is selected; E8 is the §4.1 sub-item weighted composite;
   - E10 is record-only, not a decision input;
   - on a tie, the maintainer adjudicates by E8 team match;
   - **E6 verification method**: write a **minimal build job** that compiles the candidate stack and runs a minimal probe (S1 suffices);
     that job passing locally counts as E6 evidence. It is a **probe-phase deliverable**.
4. **Rollback trigger**: rollback to sippy, and mark this ADR Rejected, if and only if one of the following holds:
   - (a) all formal candidates fail the E1 threshold; or
   - (b) the E8 composite assessment (§4.1) shows maintenance cost higher than continuing to maintain sippy —
     the quantitative threshold is **required effort > existing sippy maintenance effort × 2**. Scope: base on the person-hours our team invested in sippy over the last 12 months (incl. defect fixes, upgrades, troubleshooting); convert via the same-period timesheet or estimate; scope confirmed by the maintainer at assessment.
5. **This ADR turns Accepted** (2026-09-28):
   - **Selected stack**: reSIProcate (C++, Vovida license, BSD-like)
   - **Version pin**: specific commit/tag determined in the M1 probe phase (current latest release is 1.14.0, 2026-06-18)
   - **Integration method**: CMake + `git submodule` vendoring; connect to the platform kernel via Python bindings (`BUILD_PYTHON=ON`)
   - **Accepted gaps**:
     1. E1 behavioral equivalence (S1–S11) not yet verified by real-socket probe — to be completed in M1; on failure, roll back to go-b2bua or sippy
     2. E4 TLS certificate hot rotation (S12) not yet verified — to be completed in M1
     3. E5 state externalizable / serialization capability not yet verified — to be completed in M1
     4. TCP/TLS transport layer is a known reSIProcate weak point; production needs focused attention — see K8
     5. C++ stack introduces C++ toolchain and debugging cost — team needs to add C++ / gdb capability
     6. platform kernel SIP adaptation layer not started before probe completes (K2)
   - **Historical status note (2026-10-04)**:
     1. The above "to be completed in M1" schedule was not completed as originally written (S12 unfinished when M1 closed).
     2. S12 (TLS certificate hot rotation) remains open.
     3. Subsequent native-probe SIGHUP/cert-swap evidence is testbed-only smoke, cannot alone close E4, nor be treated as REQ-S-3 acceptance.
     4. Current status and follow-up actions are per `docs/plan.md` and `docs/reviews/m2-native-probe-review-2026-10-04.md`.
6. **Synchronous update**: `docs/architecture/system-architecture.md` decision 8, the ADR registry, `docs/SIP_stack_selection.md` conclusion section, `platform/pyproject.toml`.

---

## 7. Current consequences

### 7.1 Accepted costs

| # | Cost | Mitigation |
|---|---|---|
| K1 | **M0 signoff blocked**. The repo stays at skeleton state until selection completes | This ADR takes the fast-evaluation track, not pursuing perfection |
| K2 | **`platform/pyproject.toml` currently has empty SIP dependencies**, cannot write any signaling code before M2 | First define language-agnostic seams (`Transport`, `StateStore`, `CallController` shells), not bound to any stack |
| K3 | **M1's captured POC baseline is based on sippy**; if a C/C++ stack is finally selected, the baseline's "equivalence" needs reinterpretation (not line-by-line comparison) | Baseline recorded as **externally observable message behavior** (S1–S11), not in sippy API form |
| K4 | If go-b2bua is selected, **no release**, requires commit pin + vendoring, and partial upstream maintenance responsibility falls on us | Run its upstream regression suite in this repo; pin recorded in `AGENT.md` §8 equivalent clause |
| K5 | Introducing Go or C/C++ **breaks the simplicity of "one interpreter"**; the monorepo needs a multi-language build chain (open item D2 becomes a hard constraint) | D2's ADR sets the structure before M2 |
| K6 | **May reopen ADR-0005 / 0009 / 0010**. All three are built on sippy's blocking model: ADR-0005 (OTel export must not block the call path), ADR-0009 (ISSU can only drain), ADR-0010 (custom metric HPA + scale-down protection controller) | After the stack is fixed, re-review item by item: if the new stack is non-blocking, ADR-0005/0010 premises change; if state is serializable, ADR-0009 can upgrade from draining to state migration |
| K7 | **After switching stacks, Python runtime's role needs repositioning** | If the final stack is Go/C/C++, `platform/`'s Python kernel degrades to seam definition and test harness; ADR-0012's "cross-implementation replay" semantics changes from "Python vs Go same use case" to "new-stack implementation vs `testbed/` baseline" |
| K8 | **reSIProcate TCP/TLS transport layer is a known weak point**; production needs focused monitoring of TLS connection stability and hot-rotation behavior | M1 probe phase focuses on S12; production deployment adds TLS connection metric alerts |

### 7.2 Unresolved

- Which stack selected: **reSIProcate** (accepted 2026-09-28)
- E1 / E4 / E5 probe verification **not yet complete**, registered as accepted gaps (see §6 step 5).
  M1 phase executes probes; if any hard constraint (E4/E5) or threshold (E1) fails, trigger rollback assessment.
- If it finally returns to sippy (assessed that switching stacks yields insufficient benefit), this ADR should be marked **Rejected** with reasons, not quietly discarded.
  In the rollback case, R2 (Python 3.10 EOL in 2026-10, open item D1) still holds; disposition is one of two paths:
  - Migrate the Python runtime to 3.11 / 3.12 and re-validate sippy; or
  - Register the EOL runtime as an accepted risk in the ADR.

---

## 8. Review record

The review record is separately persisted at [`docs/reviews/adr-0019-review.md`](../../reviews/adr-0019-review.md) and
[`docs/reviews/adr-0019-review-round2.md`](../../reviews/adr-0019-review-round2.md).
Per `AGENT.md` §3.2, this ADR must have that file before being Accepted.

---

## 9. Probe harness (2026-09-30)

The E1 / E4 probe harness is persisted in `testbed/probe/`:

| File | Role |
|---|---|
| `testbed/probe/e1_baseline_probe.py` | E1: replay `testbed/contracts/sip-baseline/` S1–S11 baseline on real sockets, comparing each message sent by the stack under test |
| `testbed/probe/tls_hot_rotation_probe.py` | E4 / S12: assert certificate hot rotation does not restart the process or drop in-flight calls |
| `testbed/probe/sequence_compare.py` | Pure-function comparator: method / response code, `Call-ID`, Request-URI `host:port`, body byte-for-byte; not comparing header order / `Via` branch / SDP `o=` timestamp |
| `testbed/probe/tests/test_sequence_compare.py` | Unit test of the comparison logic (marker `unit`) |
| `testbed/probe/README.md` | How to run, exit codes, expected behavior when bindings are missing, K2 constraints |

**Not executed currently.** This environment has no reSIProcate Python binding — the build option `BUILD_PYTHON=ON` is not built,
`import resip` fails (confirmed in this actual run). Both probes **lazily import** the binding module, and on missing binding fail loudly with **exit code 2**
and print build guidance (how to build with `BUILD_PYTHON=ON`, how to make it importable, how to re-run), **never silently skip** —
a skip is not evidence, and K2 must not be released without any evidence.

Therefore:

- **E1 (S1–S11) and E4 (TLS hot rotation) remain open accepted gaps in this ADR**; status does not change because the harness is persisted;
  only after running in an environment with the binding and backfilling results into `docs/acceptance/report.md` may §6 step 5's gap list be updated.
- The interface of the stack under test is expressed by a minimal Protocol (`StackUnderProbe.send(payload) -> bytes | None`,
  the four methods of `TlsStackUnderProbe`); **the adapter fitting reSIProcate's binding is not implemented this time**,
  provided by the binding side at real integration (optional entry `create_stack_under_probe(host, port)`).
- **The E5 (state externalizable / serialization) probe is not yet written**, listed as follow-up — E5 currently has no executable judgment at all.
- K2 still holds: before the probe passes, the platform's SIP adaptation layer does not start.

## 10. Evidence correction (2026-09-30)

The historical Accepted decision above selected reSIProcate and remains in force. A correction to its stated integration route is required: inspection of upstream reSIProcate 1.14.0, tag commit `632e215c2ca9aee5416bfe1808851ea6fa380044`, confirmed that `BUILD_PYTHON=ON` enables PyCXX-based rePro Python routing/plugin targets; it does **not** provide a general `resip`/DUM Python binding. The E1 harness's `import resip` therefore exited 2. This corrects the integration evidence, not the stack selection.

The proposed [ADR-0022](0022-resiprocate-b2bua-control.md) tracks the DUM/product `CallController` responsibility split and the unresolved integration and state-recovery design. E1, E4, and E5 remain open; K2 remains unreleased. Native DUM S1/S4 smoke is not product E1 acceptance, and native TLS S1 failed to establish a call (503 Certificate Validation Failure; timeout exit 124). No product acceptance or release conclusion follows from these observations.
