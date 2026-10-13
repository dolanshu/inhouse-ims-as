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

# ADR-0012: Language-agnostic contract + cross-implementation parity as the promotion gate

- **Status**: accepted
- **Date**: 2026-09-30
- **Decides**: §0 ledger entry 9 — cross-implementation boundary: language-agnostic contract + an implementation may only be promoted after passing cross-implementation parity
- **Responds to REQ**: REQ-G-2

---

## Context

This project has an explicit isomorphic translation route: port a certain use-case image to Go (`docs/plan.md` M7), and `AGENT.md` §10 points out explicitly that "porting the Go image is the highest-value AI task in this project — isomorphic translation + parity harness". The risk of porting lies not in being unable to write it, but in **writing it but not equivalently**: an implementation that runs, passes its own tests, yet diverges from the original on number-range matching priority or rate-window boundaries is a worse outcome than "not porting at all" — it hides the differences into production.

Therefore "equivalence" cannot be a verbal statement, nor **self-certification from within the implementation**. It can only be adjudicated by a criterion **independent of any implementation language**. If the contract is written in Python (for example as a pytest fixture), then the Go implementation is forever chasing Python, not chasing the requirement; once the Python side is itself wrong, both implementations will be wrong together and prove each other correct.

This judgment becomes stronger, not weaker, after the stack selection. ADR-0019's K7 records: after the production stack selects reSIProcate, if the final stack is Go/C/C++, the `platform/` Python kernel degrades into seam definitions and the test harness, and **ADR-0012's "cross-implementation parity" semantics change from "Python vs Go same use case" to "new-stack implementation vs `testbed/` baseline"**. That is, the baseline (not the current implementation of some language) is the anchor.

The reason decision semantics can be declared entirely as data is that they are pure functions to begin with: `AGENT.md` §5 stipulates that "decision modules are pure functions. Modules producing decisions cannot have sockets, cannot have clocks, cannot have global state". No clock means `received_at` can be passed in as data; no global state means the rate window's counters can be injected by the caller; no socket means decisions are protocol-independent. Together these three make "given this number and this configuration, what is the decision" writable as a language-agnostic case set.

## Decision

- **The contract exists in a declarative, language-agnostic form, landing in `testbed/contracts/`; it is data, not a fixture in some language.** The contract answers the requirements question, not "how Python does it now".
- **Every implementation must replay it, case for case, field for field.** The decision contract set `testbed/contracts/decision/cases.json` is replayed by each use case: `apps/translation` takes cases whose `applies_to` contains `translation` or `both`, `apps/anti-fraud` takes `anti-fraud` or `both`; `both` is shared kernel semantics, and every implementation must be field-for-field identical.
- **A missing or empty contract must fail loudly, not skip silently.** A contract that has not been replayed is a contract that has not been enforced.
- **An implementation may only be promoted after passing cross-implementation parity.** M7's Go image is gated by M6: it is promoted only when its output is output-for-output identical to the Python implementation (`docs/plan.md` §4 M7 row).
- **Parity semantics per ADR-0019's K7: new-stack implementation vs `testbed/` baseline, not "Python vs Go same use case".** The baseline is the anchor; the current implementation of some language is not.
- **A contract change equals a requirements change.** Adding or modifying a contract case is an interface change: it needs an ADR, and every implementation's gate must be re-run (REQ-G-2's documentation chain). **An implementation that cannot express a case has found a real difference between the implementations; it is not a reason to weaken the case.**
- **The decision contract and the SIP baseline have a clear division of labor and do not substitute for each other**: `testbed/contracts/sip-baseline/` captures **line bytes** (constraining the SIP adapter layer), while `decision/cases.json` writes **expected decisions** (constraining decisions, protocol-independent). An implementation that changes the SIP stack still has to answer the latter case by case.

## Consequences

### Positive

- **The contract is the only criterion for "equivalence".** It does not depend on the reviewer's memory, nor on "we looked at it once during the last port". Equivalence goes from a statement to a repeatable assertion.
- **The promotion gate is executable and automatable.** Adding an implementation does not require discussing "whether to run parity"; just run the same contract; the gate is at gate ①'s `contract` layer, not in the review meeting.
- **The contract decouples the "verdict" from the "protocol".** Changing stacks (`ADR-0019`) does not spill over into the adjudication of decision semantics, because the decision contract contains no SIP syntax.
- **The contract forces implementations to externalize uncertainty.** Clocks and counters must be injected by the caller, making decisions deterministically replayable in any language — the side effect is that decision logic is naturally testable.

### Negative / accepted

- **The contract's maintenance cost is three-way synchronization.** Adding one decision fact requires simultaneously touching the contract, each implementation's replay, and the requirements entry; missing one produces "the contract passed but the requirements did not keep up" or vice versa. Accepted: this three-way synchronization is exactly what REQ-G-2's documentation chain requires, not an extra burden.
- **Contract changes go through the requirements process, which is slower than changing code.** This is deliberate: the contract is an interface, and interface changes should be slow.
- **Cross-implementation parity has so far only produced evidence at the decision layer.** The SIP-side E1 parity probe `testbed/probe/e1_baseline_probe.py` **has not been executed** — this environment has no Python bindings for reSIProcate, and the probe **fails loudly with exit code 2 and prints build guidance when the bindings are missing; it never silently skips**. Therefore the gate "promote only after passing cross-implementation parity" is today only adjudicable at the decision contract layer; at the protocol layer it remains an open gap (ADR-0019's E1 / E4 / E5).
- **Currently only the Python side is replaying.** The replays of `apps/translation` and `apps/anti-fraud` prove that "two use cases agree on the same contract", not that "two languages agree on the same contract". The first true cross-implementation parity waits for M7.

## Alternatives considered

| Option | Why not |
|---|---|
| Contract written as a Python test (pytest fixture) | The contract is bound to the implementation language; the Go side must rewrite a set of assertions, and "equivalence" loses its common anchor. When the Python side itself errs, both implementations err together and prove each other correct |
| Manual packet-capture comparison as the equivalence criterion | Not reproducible, not automatable, and one-off: the next port has to redo it, and conclusions vary by person |
| Manual review against the requirements document to determine equivalence | Documents are not an executable criterion; "looks consistent" cannot distinguish boundary behaviors such as number-range priority |
| Each implementation writes its own tests, and all green means equivalent | Tests are written against each implementation itself; green only proves self-consistency, not agreement with the other implementation |
| Declarative language-agnostic contract + replay by every implementation (this decision) | Adopted. The contract is data, anchored to the requirements rather than some language; parity is a hard promotion gate |

## Evidence

- **The decision contract set has landed**: `testbed/contracts/decision/cases.json` is a 14-case JSON array, each case containing `case_id` / `description` / `applies_to` / `call_id` / `calling_number` / `called_number` / `received_at` / `rules` / `translations` (translation-specific) / `limits` and `counters` (anti-fraud-specific) / `expected`. By `applies_to` distribution: `both` 5 cases (`blocked-range-is-declined`, `no-rule-matches-is-not-found`, `longest-prefix-wins`, `block-outranks-translate`, `separators-carry-no-routing-meaning`), `translation` 3 cases (`translate-baseline-number`, `translate-without-a-translation-rule-falls-back`, `translation-prefers-the-longest-prefix`), `anti-fraud` 6 cases (`forward-under-the-limit-passes-through`, `forward-over-the-limit-is-declined`, `translate-under-the-limit-is-not-rewritten`, `blocked-range-outranks-the-rate-screen`, `rate-window-prefers-the-longest-prefix`, `an-ungoverned-number-is-not-screened`).
- **Each of the two use cases replays**: `apps/translation/tests/test_contract_replay.py` and `apps/anti-fraud/tests/test_contract_replay.py`, marker `contract`; `test_contract_case` compares four fields field for field — `action` / `target` / `reason_code` / `matched_rule_id` — and `test_the_contract_set_carries_cases_for_this_use_case` prevents vacuous passes caused by an empty filter match. On missing or empty files, `pytest.fail` fails loudly.
- `testbed/contracts/decision/README.md` verbatim: "This directory holds the **decision contract case set**: data, not code… without reference to Python, Go or any other host language. Every implementation has to reproduce the whole set, case for case (ADR-0012)." Same file: "A Go implementation that keeps its own SIP stack still has to answer every case here identically, and that is the entry ticket for the migration." Also: "A missing `cases.json` fails the replay loudly — a contract that is not replayed is not enforced." And the contract-change rule: "adding or changing a contract case is an interface change. It needs an ADR, and every implementation's gate has to be re-run. An implementation that cannot express a case has found a real difference between the stacks; it is not a reason to weaken the case."
- **The SIP message baseline has landed**: under `testbed/contracts/sip-baseline/`, `S1-basic-call` (14 messages), `S2-no-match-404`, `S3-policy-reject-603`, and `S4-caller-cancel` (12 messages) have message files; `S5-b2bua-two-legs`, `S6-request-uri-rewrite`, `S7a-sdp-pass-through`, `S8-route-record-route`, `S10-non-2xx-branch`, and `S11-cancel-race` are README-only (M1 decision: S5/S6/S7a/S8 become derived baselines with assertions derived from S1; S10/S11 await M2 probe completion, see `docs/plan.md` §3 M1 decision table).
- **The probe provides E1 parity but is currently not executed**: `testbed/probe/README.md` verbatim "**Current status: neither probe has been executed.** This environment has no Python bindings for reSIProcate (build option `BUILD_PYTHON=ON` was not built)……both probes **fail loudly with exit code 2 and print build guidance when the bindings are missing; they never silently skip**. E1 and E4 are therefore **still open acceptance gaps** in ADR-0019." The exit-code table records `2` = "Python bindings for the stack under test missing (or no usable stack handle factory) — the probe did not run; this is not a pass".
- [ADR-0019](0019-sip-stack-selection.md) §7.1 K7 verbatim: "**The Python runtime role needs repositioning after the stack change** …… if the final stack is Go/C/C++, the `platform/` Python kernel degrades into seam definitions and the test harness, and ADR-0012's "cross-implementation parity" semantics change from "Python vs Go same use case" to "new-stack implementation vs `testbed/` baseline"".
- `docs/plan.md` §4 milestone M7 verbatim: "Go migration | one use case's `go-b2bua` image, commit-pinned and vendored; cross-implementation parity | Not started | **Gated by M6.** Promoted only when output-for-output identical to the Python implementation (ADR-0012)".
- `AGENT.md` §6 test strategy table: "Contract | `contract` | declarative cases, placed in `testbed/contracts/`, replayed against **every** implementation".
- PRD REQ-G-2 (changes must run through the documentation chain) verbatim: "Any behavior change — large or small — must run through the entire documentation chain: requirement → ADR → design → contract → code → acceptance. Changing code only, without upstream documents, is incomplete."
- Architecture doc §0 decision ledger entry 9 verbatim: "Go-side boundary | image port + language-agnostic contract + cross-implementation contract-test parity".

## Related

- [ADR-0014](0014-three-layer-testbed.md) Three-layer testbed — the contracts layer is this ADR's carrier
- [ADR-0019](0019-sip-stack-selection.md) Production SIP stack selection — K7 redefines the comparison target of "parity"
- [ADR-0002](0002-per-usecase-process-state-redis.md) One process per use case — determines that replay is split by use case
- [ADR-0015](0015-engineering-discipline.md) Engineering discipline — the `contract` marker and the four-layer gates
- [`../system-architecture.md`](../system-architecture.md) §11.4 test platform, §10.3 image port + parity
- PRD REQ-G-2 (changes must run through the documentation chain)
- Milestone M7 (Go image + cross-implementation parity) **not started**, gated by M6 capacity research
