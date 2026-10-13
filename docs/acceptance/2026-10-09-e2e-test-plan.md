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

# E2E Test Plan (Draft, Pending Maintainer Review)

**Date**: 2026-10-09  
**Status**: plan, **not implemented**. `pytest -m e2e` currently has **0** tests.  

> **Status correction (added 2026-10-11; the original text of the previous line is preserved unchanged)**: **Wave 1 has landed.**
> Created `testbed/e2e/test_sip_first_edition.py` (A4-1 adjudication: a separate new file, without touching
> `testbed/simulators/tests/test_product_path.py`'s `integration` marker);
> `uv run pytest -m e2e -q` went from **0** tests to **5**, all green 3 times consecutively
> (`(verified, docs/acceptance/artifacts/m5/2026-10-11/PASS-e2e-2026-10-11.txt, 2026-10-11)`).
> **Wave 2 and beyond are still not implemented** (14-message header differential comparison, control plane, and kind are all out of this round's scope).
> Execution record: [`../handoff/2026-10-11-w0-native-and-e2e-execution-record.md`](../handoff/2026-10-11-w0-native-and-e2e-execution-record.md) §7.
> **No REQ has been signed off yet**, see §8 of this document.
>
> **Further correction (added 2026-10-12; the original text of the previous paragraph and this section is preserved unchanged): Wave 2 has also landed.**
> On 2026-10-12 the maintainer authorized starting the A4 next batch (Wave 2's start prerequisite "start after Wave 1 completes" was met on 2026-10-11).
> Created `testbed/e2e/test_s1_replay_contract.py` (3 tests): **normalized** sequence differential comparison of the inbound and outgoing legs,
> **C_in ≠ C_out** (REQ-F-2 subset), and **byte-identical SDP offer** (REQ-F-4, included this round, no separate follow-up).
> `uv run pytest -m e2e -q` → **8 passed** (Wave 1's 5 + Wave 2's 3);
> without native, **8 failed / 0 skipped**.
> **Still open**: the **per-message header differential comparison** of the 14 messages — Wave 2's definition itself is the normalized skeleton differential comparison, which does not include this subset;
> `test-plan.md` REQ-F-1's `- [ ]` **not a single item is ticked**, with the status "automated subset covered / full text still open".
> Execution record [`../handoff/2026-10-12-o1-and-native-reproducibility.md`](../handoff/2026-10-12-o1-and-native-reproducibility.md) §5;
> write-back see [`../acceptance/2026-10-11-wave2-replay-register.md`](2026-10-11-wave2-replay-register.md) §6.
**Related**: [`test-plan.md`](test-plan.md) automation layering; [`../handoff/2026-10-09-sip-native-testing-plan.md`](../handoff/2026-10-09-sip-native-testing-plan.md) (harness / native gating); [`../handoff/pre-m8-demo-review-plan.md`](../handoff/pre-m8-demo-review-plan.md) (kind `as-m71`).

---

## 1. Definition (e2e in this repo)

**E2E** = one automation that simultaneously satisfies:

1. The **product SIP stack** is `_resip_runtime` (reSIProcate), not pure Python packet assembly, nor log parsing only.  
2. **The decision goes through the production seam**: `decide()` / activated rules or an equivalent `RuleSet` + outgoing leg hook; **`accept_all_invites` (and `early_cancel_harness`) is prohibited** as the default mode of the AS under test.  
3. **The path crosses the network element boundary**: at least "call source → (simulated or real) S-CSCF/S-SBC → AS → peer UAS", and asserts the **terminal state** (result code, outgoing leg user number when necessary, BYE not hanging).  
4. Marked **`@pytest.mark.e2e`**, collected by `make test-e2e` / gate layer ③; separated from `unit` / `contract` / `integration`, to avoid lengthening `make gate`.

**Not e2e:**

| Existing thing | Why it does not count |
|----------|------------|
| E1 S1 `accept_all_invites` | Harness: real stack but bypasses `decide()`, covering only 100/180/200 |
| E1 S2/S3 single socket | Real stack + `decide()`, but no simulated S-SBC, no complete 14 messages, no console |
| M6 `as_load` → `load_uas_runtime` | The peer is an accept-all UAS, testing capacity not business |
| `test_derived_baseline.py` | Asserts against the contract **file**, not against the product process |
| kind demo scripts | Evidence layer; steps can be **reused**, but do not count as this plan being "landed" before being promoted to pytest e2e |

---

## 2. Current State Anchors (reuse during implementation, do not reinvent the wheel)

| Anchor | Path | Already proven |
|------|------|--------|
| Local simulated chain + real stack + rules | `testbed/simulators/tests/test_product_path.py` | T1/T4/T5/F1/F2 result codes, translated user number, BYE; UDP/TCP/TLS; **integration**, short-duration `as_load` |
| Two legs / SDP | `platform/tests/test_m7_forward_two_leg_integration.py`, `test_req_f4_sdp_identity_integration.py` | FORWARD and SDP identity; no complete S-CSCF chain |
| Contract messages | `testbed/contracts/sip-baseline/S1-basic-call/` etc. | The 14 **shapes** of REQ-F-1; not yet replayed in full against the product stack |
| On-site demo | `scripts/demo-review/story-*.sh`, kind `as-m71` | Customer path; console in compose, signaling in kind |

**Gaps:** no `e2e` marker; gate layer ③ has no cases and does not block; REQ-F-1 tick still open.

---

## 3. Scope (suggested waves, to be cut down at review)

### Wave 0 — Make the gates clear (docs + marker conventions)

- This file + `test-plan.md` layering table (already written).  
- `pyproject.toml`'s `e2e` marker description aligned with the implementation.  
- Gates: until **at least one** e2e is stable, keep layer ③ non-blocking **or** change it to blocking but run only Wave 1's smoke (either/or, see §6).

### Wave 1 — Signaling e2e (no console)

Promote or split out `@pytest.mark.e2e` from `test_product_path`:

| ID | Scenario | Assertion (minimal) | Prohibited |
|----|------|----------------|------|
| E2E-SIP-1 | UDP: T1 translation call established | 200; outgoing leg user contains the translation result; BYE count and pending sessions are 0 | `accept_all_invites` |
| E2E-SIP-2 | UDP: T4 no match | 404; no outgoing leg or no BYE business leg (consistent with the existing `test_product_path`) | harness |
| E2E-SIP-3 | UDP: F2 blocked | 603 | harness |
| E2E-SIP-4 | One each for TCP and TLS (parameterizable, aligned with the existing 4 combinations or 1 each first) | Same T1 subset | Test CA, no claim of REQ-S-2/S-3 sign-off |

**Completion criteria:** `AS_REQUIRE_NATIVE_EXTENSIONS=1 uv run pytest -m e2e -q` green on a machine that has run `make m2-platform-resip-build`; without `.so` it **fails** (consistent with the native-contract strategy), not skips.

**Explicitly not doing (Wave 1):** 14-message per-message header differential comparison, console, kind, capacity numbers.

### Wave 2 — REQ-F-1 Shape (still no console)

On the Wave 1 topology, for **one** T1:

- Collect the inbound/outgoing legs' key messages (method + final response code sequence, or **normalized** comparison against `S1-basic-call`).  
- Assert **C_in ≠ C_out** (REQ-F-2 subset).  
- SDP offer byte-for-byte between the inbound and outgoing legs (REQ-F-4) if the implementation cost is acceptable; otherwise list a separate follow-up.

**Completion criteria:** `test-plan.md` REQ-F-1 tick changes to "automated subset covered / full text still open" and links to this case name; **do not** tick the full text before the 14 messages have been differentially compared.

### Wave 3 — Control Plane + Signaling (optional, heavy)

- compose or test client: rule change → activate bundle → **restart or hot reload policy per the repo's actual capability** → re-run E2E-SIP-1.  
- Align with demo story A; **do not** put manual browser steps into the first-version gate.

### Wave 4 — kind `as-m71` (pre-release evidence, default optional gate)

- Reuse `kind-up.sh` + `publish-m71-bundle.sh` + test pages or `as_load` to hit the **product Deployment** (not `load_uas_runtime`).  
- Marked `e2e` + `kind` (needs a new marker or env `AS_E2E_KIND=1`), **run manually on demand**, not on every PR, unless the maintainer requires it.

**Explicitly excluded:**

- M6 capacity / O1 report (`performance`).  
- `accept_all` harness as the AS under test.  
- Real operator S-SBC / customer PKI (M8 environment evidence, see `m8-environment-evidence.md`).

---

## 4. Boundary with Harness / Call Load (written into the case docstring)

| Process under test | Allowed |
|----------|------|
| The AS in E2E | `ResipRuntimeListener` or the product process shell, **`accept_all_invites=False`**, rules from `demo_rules()` or a bundle |
| Load generator | `as_load` is fine (it is a client); **the peer UAS uses `PeerUas` / a simulated called party**, not `load_uas_runtime.py` |
| Simulated S-CSCF/S-SBC | `as_simulators` or kind `ims-sim`; labeled "non-operator" |

---

## 5. Suggested File Layout (at implementation)

```text
testbed/simulators/tests/test_product_path.py   # can keep integration; or change to e2e
testbed/e2e/test_sip_first_edition.py           # Wave 1 new file (recommended, to avoid integration semantics confusion)
```

Gates (after Wave 1 lands):

- job `e2e`: `needs: [native-contract]` or brings its own `m2-platform-resip-build`;  
- `AS_REQUIRE_NATIVE_EXTENSIONS=1 uv run pytest -m e2e -q`;  
- remove `continue-on-error` **only if** Wave 1 is stable on `ubuntu-latest` (OpenSSL 3 and local cache paths need verification at implementation).

---

## 6. Decisions Pending Your Review

1. Should Wave 1 **directly change** `test_product_path`'s marker to `e2e` (fewer files) or **create a new file copying the assertions** (integration still gives developers a fast local run)?  
2. Without native, should e2e **fail** or **skip**? (Recommendation: consistent with `native-contract`: **fail**.)  
3. Is Wave 2's 14-message differential comparison **mandatory in this iteration** or **a separate issue**?  
4. Should kind e2e **never** enter PR required checks?

---

## 7. Acceptance (of the plan itself)

- [ ] The maintainer confirms the §1 definitions and the four decisions in §6  
- [ ] Wave 1 cases enter `master` and gate layer ③ behaves consistently with the decisions  
- [ ] `test-plan.md` REQ-F-1 tick status is consistent with whether Wave 2 is done (do not tick the full text if not done)

---

## 8. Current Handling of the Three Acceptance Boxes (added 2026-10-11; §7 original text preserved unchanged)

> The three boxes above are preserved **verbatim** per the history-keeping convention; this section only **appends** the current handling for cross-checking.

| §7 box | Handling (2026-10-11) |
|---|---|
| ① The maintainer confirms the §1 definitions and the four decisions in §6 | ✅ **Confirmed** — the four decisions are the **G2 / A4-1…A4-4** of `docs/handoff/2026-10-10-unfinished-assessment-and-next-plan.md` §0-A.6, adjudicated and landed on 2026-10-10; this round implements per them (A4-1 new file, A4-2 fail when native is missing, A4-3 Wave 2 deferred to an in-repo carrier, A4-4 registers the policy direction only, **no configuration change**) |
| ② Wave 1 cases enter `master` and gate layer ③ behaves consistently with the decisions | ⚠️ **Half done** — the cases have landed and passed stably on this machine; **entering `master` needs a maintainer commit** (this round made no git write operations). Of "gate layer ③ behaves consistently with the decisions", **the locally verifiable part is consistent**: fail not skip when native is missing (measured 5 failed / 0 skipped). **The gate configuration change for kind e2e entering PR required was not made** — the A4-4 adjudication explicitly states "does not constitute authorization for any configuration change" |
| ③ `test-plan.md` REQ-F-1 tick status is consistent with whether Wave 2 is done | ❌ **Not done** — Wave 2's 14-message differential comparison is not implemented, with the carrier being [`2026-10-11-wave2-replay-register.md`](2026-10-11-wave2-replay-register.md). **REQ-F-1's 14-message full text is still open; not ticked and not signed off this round** |

**Update to the §8 table's box ③ (added 2026-10-12; the original text of the table above is preserved unchanged)**:

| §7 box | Updated handling (2026-10-12) |
|---|---|
| ③ `test-plan.md` REQ-F-1 tick status is consistent with whether Wave 2 is done | **Landed per the completion criteria** — Wave 2 is implemented (`testbed/e2e/test_s1_replay_contract.py`, 3 tests), and the status changed to "**automated subset covered / full text still open**" and linked to the case name (`test-plan.md` REQ-F-1 section). **The 14-message per-message header differential comparison is still open, and not a single `- [ ]` in `test-plan.md` is ticked** — consistent with the completion criteria "do not tick the full text before the 14 messages have been differentially compared" |

**This round's boundary (to avoid over-inferring from "Wave 1 has landed")**:

- The 4 landed cases (E2E-SIP-1…4) cover **terminal result codes + outgoing leg translation result + BYE not hanging**,
  and **do not include** the 14-message per-message header differential comparison, **do not include** the control plane, **do not include** kind, and **do not include** any capacity numbers.
- The S-CSCF / S-SBC in the tested path are all **simulated** (`as_simulators`), and TLS uses a **test CA**;
  per this document's §3 "explicitly excluded" clause, **REQ-S-2 / REQ-S-3 are not signed off**.
- The real stack being green is **engineering gate layer** evidence; `docs/acceptance/report.md` §0.5's open 24 / blocked 12 **are unchanged**.
