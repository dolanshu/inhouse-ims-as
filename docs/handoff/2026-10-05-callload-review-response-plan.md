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

# callload branch review — assessment of findings and remediation plan (2026-10-05)

> **Basis**: [`docs/reviews/callload-m2-m6-m7-demo-branch-review-2026-10-05.md`](../reviews/callload-m2-m6-m7-demo-branch-review-2026-10-05.md) (hereinafter **the review**).  
> **Scope**: engineering and acceptance facts; **excludes** version control operations (the maintainer handles the branch/merge themselves, see AGENT.md §11).  
> **Goal**: before maintainer sign-off, settle "does the review hold → what to do → what counts as closed".

---

## 1. Assessment of the review's conclusions

| Review conclusion | Assessment |
|----------|------|
| **The engineering slice holds, `make gate` is green** | **Agree**. The decision layer, M6 methodology, demo boundary wording, checkpoint CAS and the other positive items are consistent with the source code. |
| **Merging into trunk / demoing to a customer directly in the current form is not approved** | **Agree (conditional)**. The root cause is not "the documentation was never written" but that **the product runtime is still wired in loopback lab form** (F1+F7), and that **the recovery/checkpoint evidence chain diverges from the REQ statement** (F2–F4, F3). |
| **1 blocker + 10 major** | **The order of magnitude is reasonable**; F11 should be downgraded to **maintainer engineering hygiene** and must not be a P0 in the agent fix queue (see §3). |

**Statements that are disagreed with, or that need narrowing**:

| Review item | Adjustment |
|----------|------|
| **F10 "04afc5a not merged into trunk"** | In substance this is **the M5 full-chain conclusion not being reconciled with the story C demo wording on callload**, not "a git merge must happen first". Disposition = **content reconciliation**: story C only demos artifacts recognized by M5.1/full chain, or is explicitly labeled as an L1/mechanism demo. |
| **F11 commit granularity** | Of reference value to **future** maintainer merges; **not** a blocker for callload functional fixes; the agent **does not** rewrite history. |
| **"All 18 items are pending change"** | Should be split into **P0 product deployability**, **P1 M8 evidence authenticity**, and **P2 hygiene and demo repeatability**; P2 does not block an "internal technical demo (loopback)". |

---

## 2. Per-category assessment of the findings (whether adopted)

### 2.1 Adopted as P0 (must be done before a customer demo can be "non-loopback" / before the product process is configurable)

| ID | Review claim | Assessment | Disposition direction |
|----|----------|------|----------|
| **F1** | Listening address / Contact / SDP hardcode `127.0.0.1` | **Holds** (verified in multiple places in `runtime_module.cxx`) | Thread `AS_SIP_BIND_ADDRESS` / `AS_SIP_ADVERTISED_ADDRESS` (or the equivalent) through the C++ config and Contact/SDP; add a non-loopback bind integration test |
| **F7** | `SipStackService.from_env` does not read TLS/peer/bind settings | **Holds** (same root cause as F1) | Load certificate paths, peer allowlist, and fingerprints from the env/Helm contract; when TLS is enabled and the config is invalid → **fail to start** (fail-closed) |
| **F10 (content side)** | Demo story C contradicts the M5 full-chain "does not pass" | **Holds** | Update `pre-m8-demo-review-plan.md` and the wording/scope in `story-c.sh`; full-chain/M5.1 unclosed items **must not** be presented to a customer as "accepted operational capability" |

### 2.2 Adopted as P1 (hard M8 / REQ gate; can be done after the "internal loopback demo")

| ID | Review claim | Assessment | Disposition direction |
|----|----------|------|----------|
| **F2** | Recovery BYE Contact/route_set | **Holds** | Use the advertised address; BYE carries the checkpoint `route_set`; add a Record-Route recovery integration test |
| **F3** | UAC checkpoint placeholder tag/CSeq | **Holds** (hardcoded in `sip_stack_service.py`) | Native callbacks carry the real UAC dialog fields; the integration test asserts that the downstream accepts the BYE, not merely that it was logged |
| **F4** | Non-486 → 502, violating REQ-F-10 | **Holds** | Pass 408/480/486/503/504 etc. through in C++ and `call_controller`; change `test_outbound_non486_final_maps_to_502`; add contract coverage |
| **F9** | `make gate` does not build native → core tests skip | **Holds** | Add a **native build + required contract/integration** (**fail**, not skip, when the extension is missing); align the local `make gate` policy with plan (AGENT.md §9) |
| **F5** | Fingerprint cache is unbounded | **Holds** | Evict on connection close, or LRU/cap; long run or unit test |
| **F6** | Connection is registered but never unregistered | **Holds** | Transport close callback `unregister_connection`; correct the overlap semantics |
| **F8** | C++ cout/cerr | **Holds (before M8)** | Structured Python logging from the event callback, or a C++ field contract plus tests; may be scheduled at the end of P1 |

### 2.3 Adopted as P2 (does not block "engineering sign-off", does block "release candidate / external statements")

| ID | Assessment | Disposition |
|----|------|------|
| **F12** | Holds | Add a success-rate / exit-code policy to `as_load` |
| **F13** | Holds | demo script `--strict` + PASS/SKIP/FAIL summary written to the artifact |
| **F14** | Holds | `AS_M6_OUTPUT_ROOT` |
| **F15** | Holds | CHANGELOG/VERSION before M8 packaging (DoD) |
| **F16** | Holds | `CallController` recovery unit test |
| **F18** | Holds | Add S4 to the story, or drop the 487 promise from the demo plan |
| **F17** | Partially holds | Keep the vendor source; document the shelf life / rebuild procedure for the prebuilt bundle; whether to move it out of git is a maintainer decision |

### 2.4 Not included as execution items in this plan

| ID | Explanation |
|----|------|
| **F11** | Historical commit shape: **maintainer** merge norms; the agent is not assigned to "fix" it. |

---

## 3. Remediation plan (execution order)

### Stage 0 — Adjudication and framing (one maintainer decision, no code)

- [x] **D0-1** Confirm this plan's P0/P1/P2 split; confirm whether an "internal loopback demo" is allowed before P0 completes (recommended: **stories B/E + documentation only**, story A signaling bridge and full story C **deferred**).
- [x] **D0-2** Build a **demo reconciliation table** for the M5 full chain plus the `cur` M5.1 conclusion (if it exists): every delivered-capability claim in story C → cite the review/adjudication status (see the F10 section of [`pre-m8-demo-review-plan.md`](pre-m8-demo-review-plan.md)).
- [x] **D0-3** Record in `docs/plan.md` or a handoff: the **callload review F1–F18 tracking table** (this document's §4) is the single backlog; do not open a third line (merge checklist see [`2026-10-06-callload-merge-to-master.md`](2026-10-06-callload-merge-to-master.md)).

### Stage 1 — P0: leaving loopback (the product becomes configurable)

**Goal**: the process can bind a non-loopback address on a container/VM and load TLS/peer configuration; the demo wording is aligned with M5.

| Task | Deliverable | Verification |
|------|--------|------|
| **P0-1 F1+F7** | C++ transport config + Python `SipStackService`/env documentation; Contact/SDP use the advertised address | Integration test binding to non-`127.0.0.1`; after `make m2-platform-resip-build`, at least 1 E1 case passes in a non-loopback scenario |
| **P0-2 F10** | Update `pre-m8-demo-review-plan.md`, plus the comments and customer-facing blocks in `scripts/demo-review/story-c.sh` | Maintainer signs off on "story C scope" |
| **P0-3 review write-back** | This document + the §4 tracking table; F1/F7/F10 marked as "fixing/fixed" | Against the review's adjudication table |

**Stage 1 closure criteria**: the maintainer accepts "the product process has **configurable listening and TLS/peer seams**"; **do not** claim REQ-S-2/NF-9 acceptance.

### Stage 2 — P1: evidence and REQ alignment (hard items before M8)

| Task | Dependency | Verification |
|------|------|------|
| **P1-1 F9** | None | native build job green; the relevant tests **fail** when the extension is absent; the local docs clearly state the relationship between `make m2-platform-resip-build` and gate |
| **P1-2 F4** | native | contract test + modify the unit test that froze the incorrect behavior |
| **P1-3 F3+F2** | native + recovery | real checkpoint fields; recovery BYE integration test |
| **P1-4 F5+F6** | native | disconnect / rotation unit or integration tests |
| **P1-5 F8** | optional, parallel with P1-4 | log field contract test |

**Stage 2 closure criteria**: the P1 items in the review adjudication are changed to "fixed"; the related `test-plan` entries **may enter M8 execution** (still not automatically green).

### Stage 3 — P2: hygiene and demo repeatability

- Implement item by item per §2.3; **F15** aligned with the M8 packaging milestone.
- **F18**: add a `test_e1_s4_*` step to `story-b.sh` or `story-sip.sh`, or revise §5 of the demo plan.

### Stage 4 — re-review and merge preparation

- [x] Output: [`callload-remediation-adjudication-2026-10-05.md`](../reviews/callload-remediation-adjudication-2026-10-05.md) (the status column of the adjudication table).
- [x] Merge to `master` preparation: [`2026-10-06-callload-merge-to-master.md`](2026-10-06-callload-merge-to-master.md) (the maintainer executes the merge; **pending** working-tree commit + explicit approval).
- Input: the §4 tracking table is closed except for F8 / part of F6 / F11; residual risk see merge handoff §2.4.
- This **still does not** mean M2/M6/M7 milestone exit or an all-green REQ.

---

## 4. Tracking table (update the status column during execution)

| ID | Priority | Status | Owner | Verification command / evidence |
|----|--------|------|--------|-----------------|
| F1 | P0 | Fixed | agent | `transport_env` + `runtime_module.cxx` |
| F7 | P0 | Fixed | agent | `test_transport_env.py` |
| F10 | P0 | Fixed | agent | story-c + pre-m8 §story C |
| F9 | P1 | Partially fixed | agent | `native_extensions.py`; **the blocking native-build job is not in place yet** |
| F4 | P1 | Fixed | agent | `test_call_controller.py` |
| F3 | P1 | Fixed | agent | FORWARD `uac_leg` native callback |
| F2 | P1 | Fixed | agent | `recovery_module.cxx` |
| F5 | P1 | Fixed | agent | fingerprint cap |
| F6 | P1 | Partially fixed | agent | registration cap + deregistration on termination |
| F8 | P1 | Not closed | agent | REQ-NF-13 pending before M8 |
| F12–F18 | P2 | Fixed | agent | CHANGELOG 0.2.0 / demo / as_load / M6 root |
| F11 | — | Maintainer | maintainer | not tracked by the agent |

---

## 5. Relationship to branches/milestones (statement of fact, does not assign git operations)

- **callload** carries the second half of M2 / M6 / M7 / Pre-M8 Demo engineering; the review correctly points out the gap between it and the **loopback lab form**.
- **master / cur** carry a separate **M5 full chain / M5.1** line; demo **story C** requires cross-branch **content reconciliation**, rather than assuming "merging resolves it".
- The **M6/M7 engineering results** (harness, O1 report, E1 shape, FORWARD 486) are **retained** after the P0/P1 fixes; there is no need to roll everything back because of the review.
- **2026-10-06**: when the maintainer prepares to merge `callload` into `master`, follow [`2026-10-06-callload-merge-to-master.md`](2026-10-06-callload-merge-to-master.md); the merge **does not** change the milestone/REQ boundaries in §5.

---

## 6. Suggested opening moves for the next session

1. The maintainer confirms **Stage 0** (D0-1–D0-3).  
2. Implement **P0-1** (F1+F7) as a single line until the non-loopback integration test is green.  
3. In parallel, **P0-2** documentation (narrowing demo story C).  
4. Do **P1-1 F9** early, to stop later fixes from churning without a native gate.  
