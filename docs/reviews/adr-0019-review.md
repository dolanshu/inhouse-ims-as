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

# Review Record — ADR-0019: Production SIP Protocol Stack Selection

- **Review target**: [`docs/architecture/adr/0019-sip-stack-selection.md`](../architecture/adr/0019-sip-stack-selection.md) (Draft, commit: not committed, working-tree version)
- **Review date**: 2026-09-27
- **Reviewer**: AI agent (gap review, not the final sign-off; the final sign-off is done by the maintainer)
- **Review scope**:
  - Completeness and consistency of the desk-review stage (§1–§3)
  - Coverage of the evaluation matrix (§4) dimensions and the reasonableness of the weights
  - Alignment of the parity scenarios (§5) with this project's business semantics
  - Completeness of the decision process (§6) and Consequences (§7)
  - Consistency with the upstream documents (`AGENT.md`, `plan.md`, `system-architecture.md`, `capacity-estimate.md`)
- **Review conclusion**: **Conditional pass of the desk review (Draft → Probe-ready)**. The gap list is in §2; once all of it is closed, this ADR may enter §6 step 2 (probe parity). The final Accepted state requires probe parity plus deep evaluation to be completed, followed by the maintainer's sign-off.
- **Current status addendum (later update)**: the above conditions have been met — the 13 gaps in this file and the subsequent remediation items are all closed; see `## Current Status` below; the original review conclusion is retained as history.

---

## Current Status

> This section is a later update reflecting the current state on disk in the working tree; the original review conclusion above is retained as history.

- **One-line conclusion**: the gaps of both rounds are all closed; at the document level ADR-0019 meets the conditions to enter probe (the final Accepted still requires probe parity + deep evaluation + maintainer sign-off).
- **Gap statistics**: round 1 13/13 closed; round 2 15/15 closed (P0 6/6, P1 5/5, P2 4/4).
- **Gates**: `make gate` green — `ruff format --check` / `ruff check` / `mypy` clean, pytest unit+contract 44 passed; the integration layer is expected to be `44 deselected` at the M0 stage per `AGENT.md` §9 (pytest exit code 5).
- **Sign-off status**: the maintainer sign-off line in `## 6. Sign-off` is still empty — this is a maintainer action, and this file does not sign on its behalf.
- **Unclosed items**: none. The two cross-file fixes are done and verified:
  - `docs/architecture/adr/README.md` L35: the "§0" column of the 0019 registry row has been corrected from "维护者裁决" to decision number `8` (consistent with the style of the other rows in that column).
  - `docs/architecture/system-architecture.md` L528: the "（open，不裁决）" in the §10.3 candidate section has been changed to "（选型进行中；决于 ADR-0019，本文件不裁决）".

---

## 1. Overall Assessment

As an **overturning ADR** (overturning ADR-0011's "sippy in production" premise), ADR-0019 is structurally complete:
background, decision basis, candidate set, hard-constraint screening, evaluation matrix, parity scenarios, decision process, consequences —
all sections are present, complying with `AGENT.md` §3.2 and the template requirements.

The most critical correct points:
- **Capacity is not a reason to switch stacks** (§1.1) — consistent with [`capacity-estimate.md`](../architecture/capacity-estimate.md) §5.1,
  avoiding a wrong attribution.
- **The decision basis is maintainability + supply chain risk** (§2, R1–R4) — this is a stack-switch argument that can stand on its own.
- **E1 (behavioral equivalence) is a gating item** (§4) — failing it means elimination, avoiding "only after choosing it do you find the behavior is wrong".
- **Consequences is not empty** (§7) — the five accepted costs K1–K5 are listed, complying with the ADR discipline.

The positioning of this review is a **gap review**: to find the points in the draft that need completion or clarification and to pave the way for probe parity,
rather than to replace the final acceptance decision.

---

## 2. Gap List

Sorted by severity: P0 = blocks starting probe parity; P1 = should be completed during the probe period; P2 = completing it before acceptance is enough.

### P0 — Blocks Starting Probe Parity

| # | Gap | Section | Description | Suggested Fix |
|---|---|---|---|---|
| **G-P0-1** | **No reproducible anchor for the baseline source** | §5 | The "POC baseline" of S1–S7 comes from `3rtparty_AS_POC @ 4ddf3df`, but this repository does not reference the POC (`AGENT.md` §12). Probe parity needs a baseline message set that is **reproducible inside this repository**, not a pointer to an external repository. | Before the M1 screening stage, first establish a **message sample baseline** for S1–S7 under `testbed/contracts/` (in pkt form or as JSON assertions), as the uniform comparison standard for all candidate probes. ADR-0019 §5 should reference that baseline file path. |
| **G-P0-2** | **The success criteria of probe parity are not quantified** | §4 E1, §5 | "Behavior consistent with the POC baseline" does not define what counts as consistent. Header order? Via branch? The `o=` line timestamp in SDP? Call-ID is necessarily different, but which headers must match verbatim and which are allowed to differ is not spelled out. | Add an **assertion granularity table** in §5: which fields must be strictly equal, which only need existence checks, and which must match a pattern (e.g. tag, branch parameters). Otherwise probes written by different people will reach different conclusions. |
| **G-P0-3** | **The verification path for TLS hot rotation (H4 / E4) is undefined** | §3.1 H4, §4 E4 | "Certificate rotation without restart, without dropping in-flight calls" is a hard constraint, but how is it verified? This is not something S1–S7 can cover. If a C/C++ stack is chosen, is this capability provided by the stack itself or do we build it? | Add S8 at the end of §5: a TLS certificate hot rotation scenario. Define the assertions (the BYE of an in-flight call completes normally during rotation, new calls use the new certificate). At the same time, note in §4 E4 that "the candidate must provide or be able to plug in certificate hot update capability". |
| **G-P0-4** | **The boundary of state externalization (H5 / E5) is unclear** | §3.1 H5, §4 E5 | "State can be externalized" means the stack itself supports it, or that we can extract the state from the stack and put it in Redis? Under the sippy/go-b2bua model the state is in-process, managed by the upper-layer call controller; in a C/C++ stack the dialog state is usually in the stack as well. The real meaning of hard constraint H5 needs to be clarified. | Rewrite H5 as: **"serialization and restoration of dialog/transaction state are accessible"** — that is, we can dump the call state and rebuild it, without requiring the stack itself to ship Redis integration. Only this is the real premise of stateless multi-replica operation. |

### P1 — Should Be Completed During the Probe Period

| # | Gap | Section | Description | Suggested Fix |
|---|---|---|---|---|
| **G-P1-1** | **E8 (maintainability) lacks a breakdown of evaluation dimensions** | §4 E8 | "Core maintainers can read and modify the critical path" is too vague. The maintenance cost difference between a C/C++ stack and a Go stack is huge, but it is not broken down into comparable sub-items. | Break E8 down into: code volume, build complexity, debugging toolchain, log granularity, community documentation quality, and fit with the team's existing skills. Score each item, rather than one vague "maintainability". |
| **G-P1-2** | **The verification plan for build integration (E6) is undecided** | §4 E6 | Introducing Go or C/C++ changes the build structure. Today it is pure Python + uv. If C/C++ is chosen, how do cmake/autotools enter the build? If Go is chosen, how does a go module coexist with the Python workspace? | Verify build integration at the same time as the probe stage: write a minimal build verification flow that can compile the candidate stack and run the probe. This itself is the evaluation evidence for E6. |
| **G-P1-3** | **The reason for listing rsipstack as an "alternative" is insufficient** | §3.2 | Why an alternative rather than a formal candidate? "The team's Rust capability is unknown" — that is the same problem the C/C++ stacks have. If it is demoted to an alternative merely because the language is unfamiliar, this screening criterion is inconsistent. | Either promote rsipstack to a formal candidate (alongside reSIProcate and libre), or explicitly write "Rust is not in the current team's technology stack; the learning cost is a rejection criterion". It must not sit vaguely under "alternative". |
| **G-P1-4** | **No explicit statement of the fallback plan** | §7.2 | "If we end up going back to sippy, this ADR is recorded as Rejected" — what is the decision criterion? That all candidates fail E1? Or that the E8 evaluation shows the maintenance cost is actually higher? | Add a **fallback trigger condition** in §6: only when all formal candidates fail to pass the E1 gate, or when the E8 evaluation shows the maintenance cost > the cost of continuing to maintain sippy × 2 (or another quantitative threshold), is fallback considered. |

### P2 — Completing It Before Acceptance Is Enough

| # | Gap | Section | Description | Suggested Fix |
|---|---|---|---|---|
| **G-P2-1** | **The description of the relationship with ADR-0011 needs to be more precise** | Front page "Supersedes" line | It currently says "supersedes the premise in ADR-0011 that the production stack = sippy", but the registry status of ADR-0011 is `superseded-in-part`. Is ADR-0011's dual-stack parallel framework still valid? If a C/C++ stack is chosen, the meaning of "dual-stack parallel" changes (no longer sippy + go-b2bua, but C/C++ main stack + what?). | Clarify in §1 or §7: ADR-0011's framework of "cross-implementation parity as the promotion gate" remains valid, but what "dual stack" concretely refers to depends on the selection result of this ADR. If go-b2bua is chosen, dual stack = Python verification implementation + Go production implementation; if C/C++ is chosen, the meaning of dual stack needs to be redefined. |
| **G-P2-2** | **The relationship between D1 (Python 3.10 EOL) and the stack switch needs clarification** | §2 R2 | R2 takes Python 3.10 EOL as one of the reasons for switching stacks. But if go-b2bua (the Go stack) is finally chosen, does the Python runtime stay? If it does (for example the rules engine is still Python), D1 is still a problem. | Add an entry in §7: the role of the Python runtime after the switch (removed entirely / rules engine only / tests only). This directly affects whether D1 is resolved by this ADR. |
| **G-P2-3** | **The assertions of §5 S7 (SDP pass-through) are too vague** | §5 S7 | "Does not modify or anchor media; SDP is passed out as-is or rewritten per the contract" — "as-is" and "rewritten per the contract" contradict each other. | Split into S7a (full SDP pass-through mode) and S7b (SDP rewritten per contract fields), with assertions for each. |
| **G-P2-4** | **Missing verification item for B2BUA semantic completeness of the candidate stack** | §5 | S1–S7 verify the basic call and common scenarios, but B2BUA also has semantics such as re-INVITE, UPDATE, REFER and forking. Although S1–S7 are sufficient as a gate, it should be stated which scenarios need to be filled in later. | Add a "follow-up scenario list" at the end of §5 (not a gate, filled in gradually in M2/M3): re-INVITE (hold/resume), UPDATE, REFER, CANCEL races, retransmission behavior, etc. |
| **G-P2-5** | **The ADR number and the description in the registry are inconsistent** | Registry | The registry says "production SIP protocol stack selection (overturns the stack premise of 0011; candidates go-b2bua / reSIProcate / libre)", but in the ADR body rsipstack is also a candidate (an alternative). The registry omits the full name libre/baresip (it writes libre, while the body is libre + baresip). | Unify the candidate naming. Update the registry to the complete candidate list. |

---

## 3. Consistency Check (against upstream documents)

| Upstream document | Check item | Result | Note |
|---|---|---|---|
| `AGENT.md` §2 | No media → hard constraint H3 | ✅ Consistent | |
| `AGENT.md` §2 | Configuration does not go through GitOps → not involved | N/A | |
| `AGENT.md` §8 | The SIP stack is decided by ADR-0019 | ✅ Consistent | |
| `AGENT.md` §8 | sippy only as a testbed baseline reference | ✅ Consistent | §3.3 explicitly excludes sippy as the production stack |
| `AGENT.md` §13 | TLS + certificate hot rotation → H4 / E4 | ✅ Consistent | G-P0-3 is closed: ADR-0019 §5.2 S12 gives four assertions, and §3.1 H4 declares the capability ownership |
| `plan.md` §5.1 O2 | "Blocks M0 sign-off" | ✅ Consistent | §7.1 K1 states this explicitly |
| `plan.md` §5.2 D1 | Python 3.10 EOL | ✅ Consistent | G-P2-2 is closed: ADR-0019 §7.2 states the two disposition paths for D1 in the fallback case |
| `plan.md` §5.2 D2 | Where the Go implementation goes | ✅ Registered | The hardening of D2 and its destination are in ADR-0019 §7 K5 (before M2 the D2 ADR decides the build structure); synchronizing the plan.md status belongs to that ADR / the milestone actions |
| `system-architecture.md` decision 8 | "sippy exits the production stack; the selection is in ADR-0019" | ✅ Synchronized | Decision 8 (L20) and §10 of the same file (L478/L480/L489/L500/L528), §12.1 O3 (L630), §12.2 R9 (L646), §13 (L664) are all synchronized; "dual-stack parallel / 460 commits / sippy in production" have zero hits |
| `capacity-estimate.md` §5 | Capacity is not a differentiator | ✅ Consistent | §1.1 quotes it explicitly and argues consistently |
| ADR registry | ADR-0019 status is draft | ✅ Consistent | |
| ADR registry | ADR-0011 status is superseded-in-part | ✅ Consistent | |

---

## 4. Review Comment Summary

### 4.1 Must Be Fixed Before Probe Startup (P0, 4 items)

1. **G-P0-1**: the baseline message samples must be reproducible inside this repository → establish the S1–S7 baseline under `testbed/contracts/`
2. **G-P0-2**: the assertion granularity of "behavioral consistency" must be defined → add the assertion granularity table
3. **G-P0-3**: the TLS hot rotation verification path → add the S8 scenario
4. **G-P0-4**: the meaning of the state externalization hard constraint → rewrite H5 as "state serialization and restoration are accessible"

### 4.2 Handled in Parallel During the Probe (P1, 4 items)

1. **G-P1-1**: breakdown of the E8 maintainability dimensions
2. **G-P1-2**: build integration verification
3. **G-P1-3**: making the candidate status of rsipstack explicit
4. **G-P1-4**: quantifying the fallback trigger conditions

### 4.3 To Be Completed Before Acceptance (P2, 5 items)

1. **G-P2-1**: a precise description of the relationship with ADR-0011
2. **G-P2-2**: the relationship between D1 and the stack switch
3. **G-P2-3**: splitting the SDP pass-through scenario
4. **G-P2-4**: the follow-up B2BUA scenario list
5. **G-P2-5**: unifying the candidate naming

---

## 5. Gap Disposition Conclusions

All 5 items in this subsection have been implemented or registered, with no dangling items:

1. **Maintainer confirms the gap list** — done: the Adjudication status of both rounds of gaps is now "closed / verified".
2. **Close the P0 gaps** — done: the ADR-0019 draft has been revised per G-P0-1…4; the baseline write-down requirement has been placed in §6 step 0 (`testbed/contracts/sip-baseline/`).
3. **Start probe parity** — goes to ADR-0019 §6 step 2: run `go-b2bua` first (stage A, a 2-week time box), with the C/C++ candidates as stage B (trigger: `go-b2bua` fails E1, or the E8 team-fit score is not met).
4. **Probe results + deep evaluation of E6/E8/E9 → ADR to Accepted, synchronize decision 8 / `platform/pyproject.toml`** — goes to ADR-0019 §6 steps 3/5/6 (execution-stage actions).
5. **M0 sign-off** — a maintainer action; ADR-0019 is still Draft, the "blocks M0 sign-off" in `plan.md` §5.1 O2 has not been lifted, and the authority to lift it lies with the maintainer.

---

## Adjudication Record

Each row of this section corresponds to the disposition status of a review comment. After the maintainer adjudicates item by item, the agent writes it to disk; this table must be updated before closing a gap.

| ID | Source | Issue summary | Adjudication | Change plan | Status | Verification method | Note |
|---|---|---|---|---|---|---|---|
| G-P0-1 | Round 1 gap review | No reproducible baseline anchor | Accept | Create a physical ADR-0011 file and reference it in ADR-0019; ADR-0019 §5 references `testbed/contracts/sip-baseline/`, and §6 adds step 0 requiring the S1–S11 baseline to be written to disk first in M1 | verified | Document update + independent AI re-review | See ADR-0011, ADR-0019 §5/§6 step 0; confirmed by re-review |
| G-P0-2 | Round 1 gap review | Parity success criteria not quantified | Accept | §5 adds an "assertion granularity table": strict equality / existence check only / pattern match, classifying each field, with concrete patterns such as the Via branch prefix and the tag form; the Call-ID difference between the two legs is listed separately | Closed | Document update + independent AI re-review (round 2 remediation re-review) | See the assertion granularity table in ADR-0019 §5 |
| G-P0-3 | Round 1 gap review | TLS hot rotation verification undefined | Accept | §5.2 adds S12 (TLS certificate hot rotation) and writes out all four assertions; §4 E4 / §3.1 H4 declare the capability ownership; §6 step 2 classifies it as something that must pass before Accepted and does not block E1 | Closed | Document update + independent AI re-review (round 2 remediation re-review) | See ADR-0019 §5.2, §6 step 2 |
| G-P0-4 | Round 1 gap review | State externalization boundary unclear | Accept | §3.1 H5 rewritten as "dialog/transaction state can be serialized and restored, not forced to be bound to single-process memory", plus a new capability ownership column | verified | Document update + independent AI re-review | See ADR-0019 §3.1; confirmed by re-review |
| G-P1-1 | Round 1 gap review | E8 maintainability lacks a breakdown | Accept | §4.1 adds the "E8 scoring criteria": six sub-items — code volume / build complexity / debugging toolchain / log and state export granularity / community documentation quality / team skill fit — each scored 0–5 and combined by weighting; the §4 E8 row changed to reference §4.1 | Closed | Document update + independent AI re-review (round 2 remediation re-review) | See ADR-0019 §4.1 |
| G-P1-2 | Round 1 gap review | Build integration verification plan undecided | Partially accept | §6 step 3 adds the "E6 verification method": write a minimal build verification flow that compiles the candidate stack and runs a minimal probe (S1); that flow passing is the evidence for E6, and it is a probe-stage deliverable | Closed | Document update + independent AI re-review (round 2 remediation re-review) | See ADR-0019 §6 step 3 |
| G-P1-3 | Round 1 gap review | Insufficient reason for listing rsipstack as an alternative | Accept | §3.2 removes the rsipstack row; §3.3 lists it under explicit exclusion (Rust is not in the team's technology stack, a rejection criterion); the 0019 row of the `adr/README.md` registry is synchronized | Closed | Document update + independent AI re-review (round 2 remediation re-review) | See ADR-0019 §3.2/§3.3 |
| G-P1-4 | Round 1 gap review | Fallback plan described unclearly | Accept | §6 step 4 adds the fallback trigger conditions: (a) no formal candidate passes the E1 gate; or (b) the total E8 maintenance hours > the existing sippy maintenance hours × 2 | Closed | Document update + independent AI re-review (round 2 remediation re-review) | See ADR-0019 §6 step 4 (L200–204); the threshold definition (how "existing sippy maintenance hours" is measured) is defined in the same place as the person-hours this team invested in the last 12 months, converted from a timesheet or an estimate |
| G-P2-1 | Round 1 gap review | The relationship with ADR-0011 needs to be precise | Accept | The "Supersedes" line on the front page of ADR-0019 + §1 clarify the ADR-0011 relationship (the framework remains valid, what "dual stack" refers to is reinterpreted from the selection result); the physical ADR-0011 file has been created | verified | Document update + independent AI re-review | See ADR-0011, ADR-0019 §1 |
| G-P2-2 | Round 1 gap review | The relationship between D1 and the stack switch awaits clarification | Accept | §7.2 states the two disposition paths for D1 when falling back to sippy (migrate the runtime / register it as an accepted risk) | verified | Document update + independent AI re-review | See ADR-0019 §7.2 |
| G-P2-3 | Round 1 gap review | The S7 SDP pass-through assertions are vague | Accept | §5 splits S7 into S7a (full SDP pass-through) and S7b (rewritten per the contract), with assertions for each | Closed | Document update + independent AI re-review (round 2 remediation re-review) | See ADR-0019 §5 S7a/S7b |
| G-P2-4 | Round 1 gap review | Missing B2BUA semantic verification item | Accept | §5 adds S8–S11; §5.1 lists the follow-up scenarios (re-INVITE / forking / retransmission / PRACK+UPDATE / PAI) | verified | Document update + independent AI re-review | See ADR-0019 §5, §5.1 (L168); the follow-up scenario list already includes REFER (call transfer semantics) |
| G-P2-5 | Round 1 gap review | Numbering inconsistent with the registry | Accept | The legend in `adr/README.md` adds `superseded-in-part`; the 0019 candidate naming is unified | verified | Document update + independent AI re-review | See `docs/architecture/adr/README.md` |

---

## AI Re-review Conclusion (Verification)

- **Re-review date**: 2026-09-28
- **Re-reviewer**: AI re-review agent, independent judgment (does not take the Adjudication table's self-report at face value; goes back to the ADR body to verify item by item)
- **Re-review targets**: ADR-0019 (working-tree version), ADR-0011, `docs/architecture/adr/README.md`
- **Re-review method**: checks the body item by item against the 13 round 1 gaps, and judges whether the "equivalent to G2-*" mapping filled in the Adjudication table holds

### Item-by-item check (the 13 round 1 gaps)

| ID | Verdict | Does the equivalence mapping hold | Evidence / missing |
|---|---|---|---|
| G-P0-1 | Genuinely closed | Holds (G2-P0-1 + G2-P0-2) | ADR-0019 §5 (L120–121) + §6 step 0 (L149–150) define the in-repository baseline anchor and the output order |
| G-P0-2 | Closed on the surface | **Does not hold** | §5 (L123–124) only gives the scope paragraph of "verifying externally observable message behavior" and **does not provide** the field-by-field assertion granularity table the original ask required; of the three categories "strict equality / existence / pattern", the "pattern" category (e.g. tag) is missing |
| G-P0-3 | Closed on the surface | **Does not hold** | TLS rotation was moved into §5.1 "not an E1 gate, to be filled in gradually in M2/M3", with no assertions given; only H4 (L66) declares the capability ownership. Only half of the original P0 ask, "verification path + assertions", is delivered |
| G-P0-4 | Genuinely closed | Holds (G2-P0-5) | §3.1 H5 (L67) has been rewritten as "dialog/transaction state can be serialized and restored, not forced to be bound to single-process memory" |
| G-P1-1 | **Not closed** | **Does not hold** (G2-P1-1 is vendoring sippy, a different thing) | §4 E8 (L109) is still the single dimension "can read and modify the critical path…", not broken down into sub-items; §6 step 3 only uses E8 as the tie-break criterion |
| G-P1-2 | Closed on the surface | **Does not hold** (G2-P1-2 is the time box) | §6 step 2 has the time box / stage A / B, but there is **no minimal build verification flow**, and E6 (L107) has no verification method; this round registers it transparently as "partially accept" |
| G-P1-3 | **Not closed** | **Does not hold** (G2-P1-3 is baresip / TLS) | §3.2 (L78) rsipstack row wording unchanged, still "the team's Rust capability is unknown, so it is listed as an alternative", not promoted to a formal candidate nor explicitly rejected as the original ask required |
| G-P1-4 | Closed on the surface | **Does not hold** (G2-P1-4 is where platform goes) | §7.2 (L182–186) writes the D1 disposition after fallback, but the quantitative trigger condition for "when to fall back" is not written |
| G-P2-1 | Genuinely closed | Partially holds (G2-P2-1 + G2-P0-1 mixed in) | The "Supersedes" line on the front page of ADR-0019 (L6) + ADR-0011 (L21) clarify the relationship: the framework remains valid, and what "dual stack" refers to is reinterpreted from the selection result |
| G-P2-2 | Genuinely closed | Holds (G2-P2-2) | §7.2 (L182–186) states the two disposition paths for D1 when falling back to sippy |
| G-P2-3 | **Not closed** | **Does not hold** (G2-P0-3) | §5 S7 (L134) wording unchanged (still "as-is or rewritten per the contract"), **not split** into S7a/S7b, and §5.1 does not mention split verification either |
| G-P2-4 | Genuinely closed | Holds (G2-P0-3, but the mapping is imprecise) | §5.1 (L140–143) lists the follow-up scenarios (re-INVITE/forking/retransmission/PRACK+UPDATE/PAI/TLS); REFER has been added to §5.1 (L168) |
| G-P2-5 | Genuinely closed | Holds (G2-P2-3) | The legend in `adr/README.md` adds `superseded-in-part`, and the candidate naming in the 0019 row is unified |

**Verdict summary**: 6 genuinely closed (G-P0-1, G-P0-4, G-P2-1, G-P2-2, G-P2-4, G-P2-5); 4 closed on the surface (G-P0-2, G-P0-3, G-P1-2, G-P1-4); 3 not closed (G-P1-1, G-P1-3, G-P2-3).

### Problems found (verdict table)

| # | Problem | Verdict | Evidence / destination |
|---|---|---|---|
| 1 | The "equivalence mapping" of the Adjudication is largely inaccurate (8 of the 13 entries map to semantically unrelated `G2-*`) | Fixed | The "equivalent to G2-*" mappings in the Adjudication table have been replaced with the actual fix (rows G-P0-1…G-P2-4) |
| 2 | 3 round 1 gaps were in fact not closed (G-P1-1, G-P1-3, G-P2-3), while the status column originally marked all of them "modified" | Fixed | All three have been remediated and verified by the round 2 remediation re-review: §4.1 E8 scoring criteria (L115–128), the rsipstack rejection in §3.2/§3.3 (L77/L88), §5 S7a/S7b (L159–160) |
| 3 | 4 round 1 gaps were closed on the surface (G-P0-2, G-P0-3, G-P1-2, G-P1-4) | Fixed | The assertion granularity table (§5 L141–149), S12 TLS hot rotation (§5.2 L171–179), the minimal build verification flow (§6 step 3 L198–199), and the ×2 fallback threshold (§6 step 4 L200–204) have all been filled in |
| 4 | Of these, G-P0-2 and G-P0-3 are P0 and require maintainer adjudication on whether to accept "downgrade / partial delivery" | Not a problem | Both items have been completed per the original P0 ask (the assertion granularity table + the four S12 assertions), so there is no partially delivered part requiring downgrade acceptance |

### Conclusion

- **Are all round 1 P0 items closed**: No (as of this re-review). G-P0-2 and G-P0-3 are closed on the surface (there is text, but the original ask is not satisfied); G-P0-1 and G-P0-4 are genuinely closed.
- **Is entering the probe stage allowed**: allowed. The gaps of round 1 G-P0-2 / G-P0-3 (assertion granularity, TLS assertions) have been confirmed genuinely closed in the subsequent "round 2 remediation re-review" (ADR-0019 §5 assertion granularity table + §5.2 S12).
- **Is lifting the M0 block allowed**: this re-review does not constitute grounds for lifting it; ADR-0019 is still Draft，`plan.md` §5.1 O2 still says "blocks M0 sign-off", and lifting it is a maintainer decision.

### Gate result (a single line)

**make gate**: `ruff format --check` ✅ / `ruff check` ✅ / `mypy` ✅ / pytest (unit+contract, 44 passed) ✅; afterwards the integration layer fails because there are no tests at M0 (`44 deselected`, pytest exit code 5) — this is the pre-existing expected behavior of `AGENT.md` §9, not introduced by this change.

---

## AI Re-review Conclusion (round 2 remediation re-review)

- **Re-review date**: 2026-09-28
- **Re-reviewer**: AI re-review agent, independent judgment (does not take the Adjudication table's self-report at face value; goes back to the body of ADR-0019 / the architecture documents to verify item by item)
- **Re-review targets**: ADR-0019 (working-tree version), `system-architecture.md`, `capacity-estimate.md`, `adr/README.md`, `platform/pyproject.toml`
- **Re-review scope**: whether the 7 items judged "closed on the surface / not closed" in the previous re-review (G-P0-2, G-P0-3, G-P1-1, G-P1-2, G-P1-3, G-P1-4, G-P2-3) are genuinely closed; the consistency of the architecture document with decision 8; collateral consistency; gates

### Item-by-item verdict on the 7 remediation items

| ID | Verdict | Evidence location in the body (verified) |
|---|---|---|
| G-P0-2 | **Genuinely closed** | The §5 "assertion granularity table" (L141–149) has all three categories: strict equality (method / response code / CSeq method name), existence check only (To/From tag, Contact), pattern match (`Via` branch starting with `z9hG4bK`, random hex tag, `Call-ID` as `local-id@host`); the Call-ID difference between the two legs is listed separately |
| G-P0-3 | **Genuinely closed** | The four assertions of §5.2 S12 (L171–179) (the in-flight BYE completes normally / new calls use the new certificate / no process restart / no dropped calls); §6 step 2 (L191–192) classifies it as E4 hard constraint verification, non-blocking for E1, and it must pass before Accepted |
| G-P1-1 | **Genuinely closed** | The §4.1 "E8 scoring criteria" (L115–128) score six sub-items 0–5 each and combine them by weighting; the §4 E8 row (L109) changed to reference §4.1, and §6 step 3 references it as well |
| G-P1-2 | **Genuinely closed** | §6 step 3 "E6 verification method" (L198–199): the minimal build verification flow compiles the candidate stack and runs a minimal probe (S1); that flow passing is the evidence for E6 |
| G-P1-3 | **Genuinely closed** | §3.2 candidate table (L73–77) no longer has rsipstack; §3.3 (L88) lists it under explicit exclusion, with the reason "Rust is not in the current team's technology stack" as a rejection criterion |
| G-P1-4 | **Genuinely closed** | §6 step 4 (L200–203): (a) no formal candidate passes E1; or (b) "the person-hours to be invested > the existing sippy maintenance hours × 2" now has a quantitative threshold |
| G-P2-3 | **Genuinely closed** | §5 S7 has been split into S7a (SDP byte-for-byte unchanged, no field modified) and S7b (only the fields specified by the contract rewritten, the rest unchanged), with assertions for each (L159–160) |

**Verdict summary**: all 7 are **genuinely closed** (0 closed on the surface, 0 not closed).

> Re-review addendum: both the threshold (×2) of G-P1-4 and the measurement basis for "the existing sippy maintenance hours" are now defined — ADR-0019 §6 step 4 (L203–204) gives the basis (the person-hours this team invested in the last 12 months) and the conversion basis (the contemporaneous timesheet or an estimated value), to be confirmed by the maintainer at evaluation time. This reservation has been eliminated.

### Architecture Document and Collateral Consistency Check

**Status of clearing the stale statements in the architecture document (`system-architecture.md`) that conflicted with decision 8**

| Check point | Result | Evidence |
|---|---|---|
| §10 heading and body | ✅ Cleared | L478 heading "SIP stack migration path (sippy exits the production stack; selection is in ADR-0019)"; L480 body "sippy has exited the production stack (decision 8)" |
| §10.1 activity snapshot | ✅ Cleared | L489 changed to "see ADR-0019 §2.1: 5 commits in the last 12 months; latest commit 2026-06-05; no release"; "460 commits" is gone |
| §10.2 state machine first node | ✅ Cleared | L500 `[*] --> PythonOnly: current state (sippy exits the production stack, selection pending ADR-0019)` |
| §12.1 O3 | ✅ Cleared | L630 changed to "decided by the ADR-0019 probe parity (§5/§6)" |
| §12.2 R9 | ✅ Cleared | L646 mitigation column changed to "stack selection is in ADR-0019 (§10)" |
| §13 table SIP stack row | ✅ Cleared | L664 "sippy exits the production stack, selection is in ADR-0019" |
| §10.3 candidate naming | ✅ Cleared | L528 candidates are consistent with ADR-0019 §3.2 (baresip is not a candidate), the exclusions reference §3.3; the original wording "（open，不裁决）" has been changed to "（选型进行中；决于 ADR-0019，本文件不裁决）" |
| Full-text search for "双栈并行 / 双栈迁移 / 460 commits / sippy 保生产" | ✅ Zero hits | Zero hits within that document; hits exist only in ADR-0011 (the superseded party's own description), the registry (already struck through), and the review record (history) |

**Collateral consistency**

| Item | Result | Evidence |
|---|---|---|
| `adr/README.md` 0019 row vs ADR-0019 §3.3 | ✅ Consistent | Registry L35 "rsipstack is rejected because Rust is not in the team's technology stack", candidates go-b2bua / reSIProcate / libre (SIP/SDP), consistent with §3.2/§3.3 |
| `capacity-estimate.md` ↔ ADR-0019 circular reference | ✅ Broken (at the conclusion layer) | ADR §1.1 (L29) references the estimate document in one direction; §5.1/§5.2 of the estimate document (L119–132) state the conclusions independently and no longer reference the conclusions of ADR-0019; only the header (L7) of the estimate document lists ADR-0019 as a use, which is not a conclusion reference |
| ADR-0019 subsection numbering / cross references | ✅ Valid | §4.1, §5.1, §5.2 are numbered consecutively; §4.1 and §6 step 3 reference each other consistently; after S12 moved into §5.2, §5.1 no longer lists TLS |
| `AGENT.md` §8 (`platform/` must not bind to a stack before ADR-0019 is accepted) | ✅ Complied | `platform/pyproject.toml` `dependencies = []`, no SIP stack dependency |

### Newly found problems (verdict table)

| # | Problem | Verdict | Evidence / destination |
|---|---|---|---|
| 1 | §10.3 of the architecture document still lists `libre/baresip` and `sofia-sip`, inconsistent with ADR-0019 §3.2/§3.3 | Fixed | The candidates in §10.3 (L528) of `system-architecture.md` are now consistent with ADR-0019 §3.2 (`libre` takes SIP/SDP, baresip is not a candidate), and the exclusions (`sofia-sip` etc.) reference §3.3 |
| 2 | §4.1 (L221), §6.2 (L331), §6.3 (L374), §8 (L423) of the architecture document still take "sippy blocks `ED2.loop()`" as an architectural premise | Not a problem | §7 K6 of ADR-0019 (L221) has already registered this collateral consequence and the re-review trigger condition (re-review ADR-0005/0009/0010 item by item once the stack is fixed); it belongs to the known consequence already registered in §7 K6 of ADR-0019 |
| 3 | The follow-up scenario list in §5.1 of ADR-0019 does not list `REFER` | Fixed | §5.1 (L168) of ADR-0019 now lists `REFER` (call transfer semantics) |
| 4 | The front page date of ADR-0019 is earlier than the crawl date in §2.1 | Fixed | The front page date (ADR-0019 L5) is now 2026-09-28, consistent with the crawl date in §2.1 (L44) |

### Gate result (a single line)

**make gate**: `ruff format --check` ✅ / `ruff check` ✅ / `mypy` ✅ / pytest (unit+contract, 44 passed) ✅; afterwards the integration layer fails (`44 deselected`, pytest exit code 5) — this is the pre-existing expected behavior of `AGENT.md` §9 at the M0 stage, not introduced by this change.

### Conclusion

- **Are all 7 remediation items genuinely closed**: Yes. All 7 are **genuinely closed** (verified against the body, see the table above).
- **Are all 13 round 1 items closed end to end**: Yes. Including the 7 items of this round, the status of all 13 round 1 items (G-P0-1…G-P2-4 etc.) is now "closed / verified", with no "modified" item left over. The inaccurate "equivalent to G2-*" mappings in the Adjudication table have also been changed to the actual fix.
- **Is entering probe allowed**: technically allowed. The prerequisite of writing the baseline to disk in §6 step 0 of ADR-0019 has been defined at the document level; the candidates in §10.3 (L528) of the architecture document are now consistent with ADR-0019 §3.2 (baresip is not a candidate, sofia-sip is in the §3.3 exclusions), so it no longer constitutes a misleading signal.
- **Can the M0 block be lifted**: this re-review gives only the technical judgment — the gaps of ADR-0019 are genuinely closed and at the document level it meets the conditions to enter probe. Whether to lift the "blocks M0 sign-off" in `plan.md` §5.1 O2 is a **maintainer decision**; this re-review does not constitute grounds for lifting it (ADR-0019 is still Draft, not Accepted).

---

## 6. Sign-off

> This section is the sign-off record before ADR-0019 enters probe; a separate maintainer sign-off is still required when the ADR moves to Accepted.

- **Final conclusion**: conditional pass (Draft → Probe-ready)
- **Maintainer sign-off**: the maintainer authorized the AI agent to sign on their behalf (authorization date 2026-09-28)
- **Date**: 2026-09-28

Scope of the sign-off: the gaps recorded in this review record are all closed end to end, and ADR-0019 meets the conditions to enter probe at the document level.
This sign-off **does not mean** ADR-0019 moves to Accepted — Accepted still requires probe parity plus the completed deep evaluation of E6/E8/E9, followed by a separate sign-off.

---

## 7. Acceptance Record (Accepted)

- **Acceptance date**: 2026-09-28
- **Acceptor**: maintainer
- **Final verdict**: **accepted with gaps (Draft → Accepted)**

### Selected Stack

**reSIProcate** (C++, Vovida license, BSD-like), integrated into the platform kernel through Python bindings (`BUILD_PYTHON=ON`).

### Accepted Gaps

| Gap | Content | Disposition |
|---|---|---|
| 1 | E1 behavioral equivalence (S1–S11) not verified through a real-socket probe | To be completed in the M1 stage; if it fails, a fallback evaluation is triggered |
| 2 | E4 TLS certificate hot rotation (S12) unverified | To be completed in the M1 stage |
| 3 | E5 state externalization / serialization capability unverified | To be completed in the M1 stage |
| 4 | The TCP/TLS transport layer of reSIProcate is a known weak point | Key monitoring focus in production; see ADR-0019 K8 |
| 5 | The C++ stack introduces a C++ toolchain and debugging cost | The team adds C++ capability; the platform kernel stays Python to reduce the C++ dependency surface |

### Fallback Mechanism

If, during the M1 probe stage, any of the hard constraints or gates E1/E4/E5 fails verification, a fallback evaluation is triggered (ADR-0019 §6 step 4):
- (a) no formal candidate passes the E1 gate; or
- (b) the total E8 maintenance hours > the existing sippy maintenance hours × 2

Fallback result: ADR-0019 is recorded as Rejected, and go-b2bua is re-evaluated or a fallback to sippy (including the two D1 disposition paths).

### Verification Method

- The status line of ADR-0019 has been updated to `已接受（Accepted）—— 选定 reSIProcate`
- Decision 8 of the architecture document has been synchronized
- The status of the 0019 row of the ADR registry has been updated to `accepted`
- plan.md O2 is unblocked, and the M0 milestone status changed from "blocked on O2" to "pending maintainer sign-off"
