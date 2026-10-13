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

# Review Record (round 2) — ADR-0019: Production SIP Protocol Stack Selection

- **Review target**: [`docs/architecture/adr/0019-sip-stack-selection.md`](../architecture/adr/0019-sip-stack-selection.md) (Draft; working-tree version, not committed)
- **Review date**: 2026-09-28
- **Reviewer**: AI agent (independent round 2 re-review; **not the final sign-off**, the final sign-off is done by the maintainer)
- **Relationship to round 1**: the round 1 gap review is in [`adr-0019-review.md`](adr-0019-review.md). This round is an independent re-review that both confirms its content and additionally records the items missed in round 1. Both rounds coexist and neither replaces the other.
- **Review scope**:
  - The full ADR-0019 draft (§1–§8)
  - Upstream consistency: `AGENT.md`, `docs/plan.md` §5, `docs/architecture/system-architecture.md` (§0 decision 8, §4.2, §6.2, §10, §12), `docs/architecture/capacity-estimate.md`, `docs/SIP_stack_selection.md`, `docs/architecture/adr/README.md`
  - Fact checking: the actual members of the `docs/architecture/adr/` directory, `platform/pyproject.toml`, the actual contents of `testbed/contracts/`, the git working-tree status
- **Review conclusion**: **conditional pass (Draft → revise before entering probe parity)**. Until all 6 P0 items in §2 section A are closed, ADR §6 step 2 must not be started. The final Accepted state requires probe parity plus the completed deep evaluation, followed by the maintainer's sign-off.
- **Current status addendum (later update)**: the above conditions have been met — the 15 gaps in this file and the subsequent remediation items are all closed; see `## Current Status` below; the original review conclusion is retained as history.

---

## Current Status

> This section is a later update reflecting the current state on disk in the working tree; the original review conclusion above is retained as history.

- **One-line conclusion**: the gaps of both rounds are all closed; at the document level ADR-0019 meets the conditions to enter probe (the final Accepted still requires probe parity + deep evaluation + maintainer sign-off).
- **Gap statistics**: round 1 13/13 closed; round 2 15/15 closed (P0 6/6, P1 5/5, P2 4/4).
- **Gates**: `make gate` green — `ruff format --check` / `ruff check` / `mypy` clean, pytest unit+contract 44 passed; the integration layer is expected to be `44 deselected` at the M0 stage per `AGENT.md` §9 (pytest exit code 5).
- **Sign-off status**: the maintainer sign-off line in `## 7. Sign-off` is still empty — this is a maintainer action, and this file does not sign on its behalf.
- **Unclosed items**: none. The two cross-file fixes are done and verified:
  - `docs/architecture/adr/README.md` L35: the "§0" column of the 0019 registry row has been corrected from "维护者裁决" to decision number `8` (consistent with the style of the other rows in that column).
  - `docs/architecture/system-architecture.md` L528: the "（open，不裁决）" in the §10.3 candidate section has been changed to "（选型进行中；决于 ADR-0019，本文件不裁决）".

---

## 1. Overall Assessment

The skeleton of the draft is right; there are three key correct points:

- **Capacity is not used as a reason to switch stacks** (§1.1) — consistent with `capacity-estimate.md` §5.1, avoiding a wrong attribution.
- **E1 (behavioral equivalence) is set as a gating item** (§4) — failing it means elimination.
- **Consequences is not empty** (§7) — the five accepted costs K1–K5 are listed, complying with the ADR discipline.

Three structural deficiencies:

1. **The thing being overturned does not exist**: the ADR-0011 being overturned has no physical file.
2. **The gate scenarios are not this product's scenarios**: S1–S7 are generic B2BUA scenarios, not AS scenarios triggered by ISC.
3. **No collateral consequences registered**: `system-architecture.md` §4.2 / §6.2 and ADR-0005 / 0009 / 0010 are all built on the sippy blocking model; after the stack switch the premise changes and the draft does not mention it.

---

## 2. Gap List

The prefix `G2-` means round 2. It coexists with the `G-P0-*` / `G-P1-*` / `G-P2-*` in the existing `adr-0019-review.md`; overlaps are noted.

### A. Must Fix (P0, blocks starting probe parity)

| # | Problem | Location | Description | Suggested Fix |
|---|---|---|---|---|
| **G2-P0-1** | **The thing being overturned has no physical file** | Front page "Supersedes" line | Under `docs/architecture/adr/` there are actually only `0000-adr-template.md`, `0019-sip-stack-selection.md`, `README.md`. ADR-0011 is `skeleton` in the registry (the decision is confirmed, the ADR is unwritten). "Supersedes the premise in ADR-0011" points at a document that does not exist, so a reviewer cannot check the original text being overturned. Per `AGENT.md` §7, "a decision without an ADR is a decision that will be argued again" | Write a `0011` skeleton file and mark it `superseded-in-part`; or change the reference to "overturns the sippy premise of §0 decision 8 and §10 in `system-architecture.md` (ADR-0011 skeleton)" |
| **G2-P0-2** | **The production order of the parity baseline is deadlocked** | §5, §6 step 2 | §5 says the baseline "comes from the POC samples captured in M1 (POC freeze point 4ddf3df)", but M1 comes after the M0 sign-off, while the probe in §6 step 2 depends on that baseline — so the probe cannot start now. This is more serious than "the baseline points at an external repository": it is an ordering problem, not just a location problem | Add step 0 to §6: in M1, first run S1–S7 under `testbed/` with sippy to capture the baseline and write it to `testbed/contracts/`; the probe follows after that. State the milestone that produces the baseline and its owner. (Partially overlaps the existing G-P0-1; the ordering dimension is added here) |
| **G2-P0-3** | **The E1 gate scenarios are not this product's AS scenarios** | §5 S1–S7 | S1–S7 are generic B2BUA scenarios, missing the semantics most easily gotten wrong under the ISC trigger form (`AGENT.md` §1, ADR-0003): `Route` / `Record-Route` handling (after the S-CSCF inserts a route, the AS must preserve the in-dialog route), in-dialog requests (whether BYE / re-INVITE still traverse the AS), `P-Asserted-Identity` and trust-domain allowlist validation (`AGENT.md` §13), the terminating non-2xx branches (486 / 480 / 408), and the race between CANCEL and the final response. Choosing the wrong gate scenarios means the gate fails | Add at least S8–S11: Route/Record-Route handling, in-dialog request routing, the 486/480/408 branches, CANCEL race |
| **G2-P0-4** | **The primary reason R1 has no evidence anchor** | §2 R1 | "Upstream sippy has effectively stalled" is the engine of the entire stack-switch argument (R2–R4 all hang on it), yet the whole document has no repository URL, observation date, commit count for the last 12 months, or issue response status. `AGENT.md` §5 requires that "behavior is observed, not assumed"; the same applies to upstream activity | Attach an evidence table to each reason in §2 (source URL + capture date + observed value). The "460 commits / commits two months ago" in §10.1 of `system-architecture.md` is a snapshot taken at writing time and must be re-observed before it can be cited |
| **G2-P0-5** | **H4 / H5 do not distinguish "provided by the stack" from "built by us"; and H5 will also overturn downstream ADRs** | §3.1 H4/H5, §7 | The draft does not say whether these two hard constraints require native support from the stack or allow us to implement outside it. More importantly: "all state is in process memory, no serialization interface → ISSU can only drain" in §6.2 of `system-architecture.md` (ADR-0009), the "blocking model → custom-metric HPA + scale-down guard controller" in §4.2 (ADR-0010), and OTel "export must not enter the SIP callback" (ADR-0005, see `AGENT.md` §5) — **all three are built on the sippy blocking model**. After the stack switch the premise changes and Consequences does not register it at all | Rewrite H4/H5 as capability ownership statements (native to the stack / built by us); add "this ADR may also reopen ADR-0005 / 0009 / 0010" to §7, and list the re-review trigger conditions |
| **G2-P0-6** | **The evaluation matrix is not executable** | §4 | The weight column gives high/medium/low, but there is no scoring method or combination rule: how to adjudicate after scoring the three candidates on each dimension is not written. After the probe completes there will still be disputes — exactly what the ADR should have eliminated in advance | State the adjudication rule in §6 step 3, e.g. "among those passing E1, the one with the highest weighted total of E7 / E8 / E9 is selected; E10 is recorded only and is not a decision input" |

### B. To Be Completed During the Probe (P1)

| # | Problem | Location | Suggested Fix |
|---|---|---|---|
| **G2-P1-1** | **The candidate set misses the cheapest option**: H2 allows commit pinning + vendoring, so "vendoring sippy and maintaining it ourselves" is a legitimate candidate with a far lower cost than switching language, yet it appears neither in §3.2 nor as an explicit exclusion in §3.3 | §3.2 / §3.3 | State in §3.3 explicitly "we do not fork sippy" together with the reason (R3 maintainability and the R4 operational form are language-level, which a fork cannot solve). Otherwise the completeness of the selection does not hold |
| **G2-P1-2** | **Full parity probes contradict the K1 "fast path"**: writing one B2BUA probe for each of the three candidates (Go / C++ / C) is several weeks of work, yet K1 says the M0 sign-off is blocked and the fast path must be taken | §6 step 2 / §7.1 K1 | Give a time box and a degradation path: run only go-b2bua first (the closest in homology, the highest expected pass rate) and accept it first if it passes; leave C/C++ as an undecided item rather than a blocking one |
| **G2-P1-3** | **The candidate descriptions conflict with the hard constraints**: reSIProcate is noted as "the TCP/TLS transport layer is a known weak point" (which hits H4 directly) yet it is still in the candidate table; in `libre + baresip`, baresip carries a media module (which hits H3, conflicting with "no media") | §3.2 | For reSIProcate note "its retention is decided by the TLS probe"; tighten the candidates to `libre` (the SIP/SDP part), with baresip not entering the candidates |
| **G2-P1-4** | **The fate of `platform/` is not written**: `platform/pyproject.toml` is a Python kernel (`requires-python >=3.10,<3.11`), while `AGENT.md` §8 states that "before ADR-0019 is accepted, `platform/` must not bind to any specific SIP stack". After choosing the Go / C stack, is it retained as the seam definition or is it superseded? This determines the object of the "cross-implementation parity" in ADR-0012 (no longer Python vs Go on the same cases, but the new-stack implementation vs the testbed baseline) | §7 | Add an entry to §7: the role of the Python runtime after the stack switch (removed entirely / tests only / still hosting the rules engine), and synchronize the parity semantics of ADR-0012 |
| **G2-P1-5** | **The high weight of E9 constitutes a preset tilt toward Go**: go-b2bua naturally scores full marks on "homology with the POC baseline", which effectively gives it one vote before the selection | §4 E9 | State in §4 that this tilt is intentional, and that it must be weighed against E8 and must not alone constitute a reason for selection |

### C. To Be Completed Before Acceptance (P2)

| # | Problem | Location | Suggested Fix |
|---|---|---|---|
| **G2-P2-1** | **§1.1 contains process-oriented wording**: "writing capacity into the decision reasons will be overturned by the reviewer" is not decision content; and it forms a circular reference with §5.1 of `capacity-estimate.md` (the two documents cite each other's conclusions) | §1.1 | Let the estimate document be solely responsible for "capacity is not a differentiator" and have the ADR only cite the conclusion; delete the reviewer-related wording |
| **G2-P2-2** | **D1 is not disposed of after the fallback**: §7.2 says "if we end up going back to sippy, this ADR is recorded as Rejected", but after the fallback R2 still holds (Python 3.10 goes EOL in 2026-10, undecided item D1) | §7.2 | State the disposition path for D1 in the fallback case (migrate the runtime / register it as an accepted risk) |
| **G2-P2-3** | **The registry status conflicts with the legend**: `0011` is marked `superseded-in-part`, but the registry legend only has skeleton / draft / accepted; the `0019` row's candidate description omits rsipstack and the full name libre | `adr/README.md` | Unify the status words and the candidate naming (consistent with the existing G-P2-5; confirmed here) |
| **G2-P2-4** | **Decision 8 of the architecture document is not synchronized**: §0 decision 8 of `system-architecture.md` is still "dual-stack parallel: sippy stays in production + go-b2bua as a pilot" | `system-architecture.md` | Per `AGENT.md` §7 "when overturning a decision, update the architecture document in the same change", write in "sippy exits the production stack, the selection is in ADR-0019" now, without waiting for the selection result |

---

## 3. Consistency Check (round 2 re-review)

| Upstream | Check item | Result | Note |
|---|---|---|---|
| `AGENT.md` §2 | No media → H3 | Consistent | G2-P1-3 is closed: the candidates are tightened to `libre` (SIP/SDP), baresip does not enter the candidates (§3.2 L77) |
| `AGENT.md` §8 | The SIP stack is decided by ADR-0019; `platform/` is not pre-bound | Consistent | G2-P1-4 is registered: §7 K7 of ADR-0019 (L222) states the fate of the Python kernel |
| `AGENT.md` §8 | sippy only as a testbed baseline reference | Consistent | §3.3 (L93) has excluded the production identity |
| `AGENT.md` §13 | TLS + certificate hot rotation → H4/E4 | Consistent | G2-P0-5 is closed: §3.1 H4/H5 added a capability ownership column (L66–67) |
| `AGENT.md` §7 | Overturning a decision requires a new ADR and synchronizing the architecture document | Consistent | G2-P2-4 has been fixed by synchronizing the architecture document (decision 8 L20 and §10/§12/§13); G2-P0-1 is fixed (the physical ADR-0011 file has been created) |
| `plan.md` §5.1 O2 | "Blocks M0 sign-off" | Consistent | §7.1 K1 of ADR-0019 (L216) |
| `plan.md` §5.2 D1 | Python 3.10 EOL | Consistent | G2-P2-2 is closed: §7.2 (L228–230) of ADR-0019 states the two D1 disposition paths in the fallback case |
| `plan.md` §5.2 D2 | Where the Go implementation goes | Registered | The hardening of D2 and its destination are in §7 K5 of ADR-0019 (L220): before M2 the D2 ADR decides the build structure |
| `system-architecture.md` §0 decision 8 | sippy exits the production stack | Synchronized | Decision 8 (L20) and §10/§12/§13 have been synchronized |
| `system-architecture.md` §6.2 / §4.2 | draining / HPA based on the sippy blocking model | Registered | G2-P0-5 is closed: §7 K6 of ADR-0019 (L221) registers this collateral consequence and the re-review trigger condition, including the collateral ADRs 0005/0009/0010 |
| `capacity-estimate.md` §5.1 | Capacity is not a differentiator | Consistent | G2-P2-1 is closed: §5.1/§5.2 of the capacity estimate (L119–132) are now stated independently and no longer cite ADR-0019 back |
| `testbed/contracts/` | Current state of the contract directory | README only | G2-P0-2 has defined the landing point: §5/§6 step 0 of ADR-0019 (L135/L185) requires M1 to write `testbed/contracts/sip-baseline/` to disk |
| `platform/pyproject.toml` | SIP dependencies are empty | Consistent | Consistent with the self-report in §7.1 K2 of ADR-0019 (L217) |
| git working tree | Commit status | ADR-0019, the capacity estimate and `docs/reviews/` are all uncommitted (`??`) | Per `AGENT.md` §11, a commit requires the maintainer's approval each time |

---

## 4. Re-review of the Round 1 Review Record

It is confirmed that G-P0-1～4, G-P1-1～4 and G-P2-1～5 in `adr-0019-review.md` basically hold. Four were judged too lightly or judged wrongly:

1. **§3 consistency check judged "decision 8 of the architecture document not synchronized" as deferrable** — this conflicts with `AGENT.md` §7; this round re-judges it as fix immediately (G2-P2-4, now fixed: decision 8 L20 and §10/§12/§13 have been synchronized).
2. **G-P0-1 only said the baseline "points at an external repository"** — the more serious problem is that the M1 baseline has not yet been produced, forming an ordering deadlock (G2-P0-2).
3. **It failed to catch that "the premises of downstream ADRs are collaterally changed"** (G2-P0-5) — ADR-0005 / 0009 / 0010 are all built on the sippy blocking model; this is the most expensive hidden consequence of this ADR.
4. **It failed to find that ADR-0011 has no physical file** (its G-P2-5 only mentions an inconsistency in the registry description).

The sign-off section §6 of that file is empty and the reviewer describes themselves as "AI agent (not the final sign-off)", so per `AGENT.md` §3.3 it counts only as a gap review and does not constitute the formal review record of the ADR.

---

## 5. Disposition Conclusions for the Items Pending Adjudication

All 3 items in this subsection have been handled, with no dangling items:

1. **The fast path** (run only `go-b2bua` first, accept it first if it passes) — **adopted**: written into §6 step 2 of ADR-0019, where stage A runs only `go-b2bua` (a 2-week time box) and the C/C++ candidates are stage B triggered by degradation.
2. **The fate of the `platform/` Python kernel** — **registered**: §7 K7 of ADR-0019 states that after the stack switch the Python kernel degrades into the seam definition and the test harness, and the parity semantics of ADR-0012 are synchronized.
3. **Whether to update decision 8 of the architecture document now** — **executed**: §0 decision 8 (L20) of `system-architecture.md` has been changed to "sippy exits the production stack, the selection is in ADR-0019", and the related wording in §10/§12/§13 of the same file has been synchronized.

## 6. Follow-up Execution Path (all registered, not gaps)

1. **Maintainer confirms this round's gap list** — done: the Adjudication status of both rounds of gaps is now "closed / verified".
2. **Close the 6 P0 items in §2 section A** — done: the 6 P0 items have been implemented in the body of ADR-0019 and verified by an independent re-review.
3. **M1 baseline capture → probe parity** — goes to §6 step 0 of ADR-0019: in M1 first capture S1–S11 with sippy and write them to `testbed/contracts/sip-baseline/`, with the baseline being written to disk as the entry condition for the probe (an execution-stage action).
4. **Probe results + deep evaluation of E6/E8/E9 → ADR to Accepted → synchronize decision 8 / the registry / `platform/pyproject.toml`** — goes to §6 steps 3/5/6 of ADR-0019 (an execution-stage action, trigger: the probe completes).

---

## Adjudication Record

Each row of this section corresponds to the disposition status of a review comment. After the maintainer adjudicates item by item, the agent writes it to disk; this table must be updated before closing a gap.

| ID | Source | Issue summary | Adjudication | Change plan | Status | Verification method | Note |
|---|---|---|---|---|---|---|---|
| G2-P0-1 | Round 2 independent re-review | The thing being overturned has no physical file | Accept | Create the ADR-0011 skeleton and mark it `superseded-in-part`; §1 of ADR-0019 and the "Supersedes" line on the front page reference that physical file | Closed | Document update + independent AI re-review | See `docs/architecture/adr/0011-sip-stack-dual-path.md`, ADR-0019 §1 |
| G2-P0-2 | Round 2 independent re-review | The production order of the baseline is deadlocked | Accept | §6 adds step 0: in M1 first run S1–S11 with sippy and write the captured baseline to `testbed/contracts/sip-baseline/`, with the probe using that as its entry condition | Closed | Document update + independent AI re-review | See ADR-0019 §5, §6 step 0 |
| G2-P0-3 | Round 2 independent re-review | E1 scenarios are not this product's AS scenarios | Accept | Add S8–S11: Route/Record-Route, in-dialog routing, the 486/480/408 branches, CANCEL race | Closed | Document update + independent AI re-review | See ADR-0019 §5 |
| G2-P0-4 | Round 2 independent re-review | R1 has no evidence anchor | Accept | §2 adds an R1 evidence table: source URL, capture date, commit count for the last 12 months, age of the oldest unclosed issue, most recent release | Closed | Document update + independent AI re-review | See ADR-0019 §2.1 |
| G2-P0-5 | Round 2 independent re-review | The capability ownership of H4/H5 is not differentiated | Accept | H4/H5 rewritten as capability ownership statements (native to the stack / built by us / combined); §7 adds K6: may also reopen ADR-0005/0009/0010 | Closed | Document update + independent AI re-review | See ADR-0019 §3.1, §7 K6 |
| G2-P0-6 | Round 2 independent re-review | The evaluation matrix is not executable | Accept | §6 step 3 states the adjudication rule: E1 is the elimination gate; the highest weighted total of E7/E8/E9 is selected; E10 is recorded only; ties are broken by the E8 team fit | Closed | Document update + independent AI re-review | See ADR-0019 §6 step 3 |
| G2-P1-1 | Round 2 independent re-review | The self-maintained sippy option is missing | Accept | §3.3 explicitly excludes forking/vendoring sippy and gives the reason (R3/R4/D1) | verified | Document update + independent AI re-review | See ADR-0019 §3.3 |
| G2-P1-2 | Round 2 independent re-review | Full parity probes contradict the fast path | Accept | §6 adds a time box: stage A runs only go-b2bua (2 weeks), and passing it allows entry into Accepted; C/C++ serves as stage B triggered by degradation | verified | Document update + independent AI re-review | See ADR-0019 §6 step 2 |
| G2-P1-3 | Round 2 independent re-review | The candidate descriptions conflict with the hard constraints | Accept | The reSIProcate note is changed to "its retention is decided by the TLS probe"; the candidates are tightened to `libre`; baresip explicitly does not enter the candidates | verified | Document update + independent AI re-review | See ADR-0019 §3.2 |
| G2-P1-4 | Round 2 independent re-review | The fate of platform is not written | Accept | §7 adds K7: the role of the Python runtime after the stack switch and the change in the parity semantics of ADR-0012 | verified | Document update + independent AI re-review | See ADR-0019 §7 K7 |
| G2-P1-5 | Round 2 independent re-review | The high weight of E9 presets a tilt toward Go | Accept | §4 E9 adds a footnote: the tilt is intentional, but must not alone constitute a reason for selection | verified | Document update + independent AI re-review | See the footnote in ADR-0019 §4 E9 |
| G2-P2-1 | Round 2 independent re-review | §1.1 contains process-oriented wording | Accept | Delete the reviewer-related wording; the capacity estimate document is solely responsible for the conclusion and the ADR only cites it | Closed | Document update + independent AI re-review (round 2 remediation re-review) | See ADR-0019 §1.1 (L22–29); §5.1/§5.2 (L119–132) of `capacity-estimate.md` have been changed to state independently that "capacity is not a differentiator" and no longer cite the conclusions of ADR-0019 |
| G2-P2-2 | Round 2 independent re-review | D1 is not disposed of after the fallback | Accept | §7.2 states the disposition path for D1 when falling back to sippy (migrate the runtime or register it as an accepted risk) | verified | Document update + independent AI re-review | See ADR-0019 §7.2 |
| G2-P2-3 | Round 2 independent re-review | The registry status conflicts with the legend | Accept | The legend in `adr/README.md` adds `superseded-in-part`; the 0019 candidate naming is unified | verified | Document update + independent AI re-review | See `docs/architecture/adr/README.md` |
| G2-P2-4 | Round 2 independent re-review | Architecture decision 8 not synchronized | Accept | §0 decision 8 of `system-architecture.md` is changed to "sippy exits the production stack, the selection is in ADR-0019" | Closed | Document update + independent AI re-review (round 2 remediation re-review) | See §0 (L20) of `docs/architecture/system-architecture.md`; this re-review confirms that the §10 heading/body (L478/L480), the §10.1 activity snapshot (L489), the §10.2 state machine first node (L500), §12.1 O3 (L630), §12.2 R9 (L646) and the §13 table (L664) of the same file are all synchronized; "双栈并行 / 460 commits / 保生产" have zero hits in that document; the §10.3 candidate naming (L528) is consistent with §3.2/§3.3 of ADR-0019 |

---

## AI Re-review Conclusion (Verification)

- **Re-review date**: 2026-09-28
- **Re-reviewer**: AI re-review agent, independent judgment (does not take the Adjudication table's self-report at face value; goes back to the ADR body to verify item by item)
- **Re-review targets**: ADR-0019 (working-tree version), ADR-0011, `docs/architecture/adr/README.md`, `docs/architecture/system-architecture.md` §0
- **Re-review method**: locate the corresponding content in the body for each gap, check whether the original ask is covered; check the consistency of numbering/references/registry/architecture document

### Item-by-item check (the 15 round 2 gaps)

| ID | Verdict | Evidence location in the body (verified) |
|---|---|---|
| G2-P0-1 | Genuinely closed | The physical ADR-0011 file exists (`adr/0011-sip-stack-dual-path.md`), and its status line is marked `superseded-in-part by ADR-0019`; the "Supersedes" line on the front page of ADR-0019 (L6) links that physical file; registry 0011 = superseded-in-part |
| G2-P0-2 | Genuinely closed | §6 step 0 (L149–150) requires M1 to first capture S1–S11 with sippy and write them to `testbed/contracts/sip-baseline/`; §5 (L120–121) explicitly states "the probe enters on the condition that this baseline has been written to disk" |
| G2-P0-3 | Genuinely closed | §5 S8 (Route/Record-Route), S9 (in-dialog routing), S10 (486/480/408 non-2xx), S11 (CANCEL race) — all four semantics are present (L135–138) |
| G2-P0-4 | Genuinely closed | The §2.1 R1 evidence table (L42–51) has all three elements: source URL, capture date (2026-09-28), observed value (commit count for the last 12 months / unclosed issues / oldest issue / most recent release) |
| G2-P0-5 | Genuinely closed | Both §3.1 H4 and H5 add a "capability ownership" column (native to the stack / built by us / combined, L66–67); §7 K6 (L176) lists the collateral ADRs 0005/0009/0010 and the re-review trigger conditions |
| G2-P0-6 | Genuinely closed | §6 step 3 (L155–159): E1 as the elimination gate, the highest weighted total of E7/E8/E9 selected, E10 recorded only and not a decision input, ties broken by E8 |
| G2-P1-1 | Genuinely closed | §3.3 (L94) explicitly excludes forking/vendoring sippy and gives the R3/R4/D1 reasons |
| G2-P1-2 | Genuinely closed | §6 step 2 (L152–154): stage A runs only go-b2bua (a 2-week time box) and passing it enters Accepted; C/C++ is stage B |
| G2-P1-3 | Genuinely closed | The reSIProcate note in §3.2 says "whether it is retained is decided by the TLS probe" (L76); libre takes SIP/SDP, baresip does not enter the candidates (L77) |
| G2-P1-4 | Genuinely closed | §7 K7 (L177) states that the Python kernel degrades into the seam / test harness and that the parity semantics of ADR-0012 change |
| G2-P1-5 | Genuinely closed | The footnote in §4 E9 (L113): the tilt is intentional, but must not alone constitute a reason for selection |
| G2-P2-1 | Genuinely closed | §1.1 (L22–29) drops the reviewer-oriented wording and is changed to "the capacity estimate document is independently responsible for the conclusion, this ADR only cites it" (one-way) |
| G2-P2-2 | Genuinely closed | §7.2 (L182–186) states the two D1 disposition paths when falling back to sippy |
| G2-P2-3 | Genuinely closed | The README legend adds `superseded-in-part`; the 0019 row registers the candidates rsipstack (alternative), libre (SIP/SDP) |
| G2-P2-4 | Genuinely closed | §0 decision 8 of `system-architecture.md` = "sippy exits the production stack, the selection is in ADR-0019" |

**Verdict summary**: all 15 round 2 gaps are **genuinely closed** (P0 6/6, P1 5/5, P2 4/4).

### Newly found problems (verdict table)

| # | Problem | Verdict | Evidence / destination |
|---|---|---|---|
| 1 | Decision 8 of the architecture document is inconsistent with §10/§12/§13 (decision 8 was changed but the stale wording was not cleared) | Fixed | The §10 heading (L478), §10.1 (L489), §10.2 (L500), §10.3 (L528), §12.1 O3 (L630), §12.2 R9 (L646) and §13 (L664) of `system-architecture.md` have been synchronized; "双栈并行 / 双栈迁移 / 460 commits / sippy 保生产" have zero hits in the whole document; the back-reference in ADR-0011 consequently holds |
| 2 | The §10.1 activity snapshot (460 commits) contradicts the observed value in §2.1 of ADR-0019 | Fixed | §10.1 (L489) of `system-architecture.md` changed to "see ADR-0019 §2.1: 5 commits in the last 12 months; latest commit 2026-06-05; no release" |
| 3 | ADR-0011 is marked `superseded-in-part` while ADR-0019 is not yet Accepted | Not a problem | The maintainer has changed decision 8, so this is intentional; the status line of ADR-0011 explicitly marks `superseded-in-part`, to be formally confirmed when ADR-0019 is Accepted |
| 4 | The document date of ADR-0019 is earlier than the capture date in §2.1 | Fixed | The front page date of ADR-0019 (L5) is now 2026-09-28, consistent with the capture date in §2.1 (L44) |
| 5 | The "§0" column of the 0019 registry row reads "维护者裁决", inconsistent with the style of the other rows | Fixed | The "§0" column at L35 of `docs/architecture/adr/README.md` is now the decision number `8`, consistent with the style of the other rows in that column |
| 6 | The circular reference between the capacity estimate and ADR-0019 is only made one-way | Fixed | §5.1/§5.2 (L119–132) of `capacity-estimate.md` state independently that "capacity is not a differentiator" and no longer cite the conclusions of ADR-0019; only the header (L7) of that file lists ADR-0019 as a use |

### Conclusion

- **Are all P0 items closed**: Yes. All 6 round 2 P0 items are **genuinely closed** (verified against the body), and the status column has been updated to "closed".
- **Is entering the probe stage allowed**: allowed. The precondition of §6 step 2 of ADR-0019 (the step 0 baseline written to disk) has been defined at the document level. Problems 1/2 above (the architecture document §10 conflicting with decision 8) have accordingly been fixed by synchronizing the architecture document (see rows 1/2 of "Newly found problems (verdict table)" in this file), and no longer constitute a misleading signal.
- **Is lifting the M0 block allowed**: this re-review does not constitute grounds for lifting it. ADR-0019 is still Draft and not Accepted, and §5.1 O2 of `plan.md` explicitly says "blocks M0 sign-off"; this re-review only confirms "its P0 gaps are genuinely closed and at the document level it meets the conditions to enter probe", and lifting the block is a maintainer decision.

### Gate result (a single line)

**make gate**: `ruff format --check` ✅ / `ruff check` ✅ / `mypy` ✅ / pytest (unit+contract, 44 passed) ✅; afterwards the integration layer fails because there are no tests at M0 (`44 deselected`, pytest exit code 5) — this is the pre-existing expected behavior of `AGENT.md` §9, not introduced by this change.

---

## AI Re-review Conclusion (round 2 remediation re-review)

- **Re-review date**: 2026-09-28
- **Re-reviewer**: AI re-review agent, independent judgment (does not take the Adjudication table's self-report at face value; goes back to the body of ADR-0019 / the architecture documents to verify item by item)
- **Re-review targets**: ADR-0019 (working-tree version), `system-architecture.md`, `capacity-estimate.md`, `adr/README.md`, `platform/pyproject.toml`
- **Re-review scope**: whether the 7 items judged "closed on the surface / not closed" in the previous re-review (G-P0-2, G-P0-3, G-P1-1, G-P1-2, G-P1-3, G-P1-4, G-P2-3) are genuinely closed; whether the two "modified" items in this table (G2-P2-1, G2-P2-4) are genuinely closed; the consistency of the architecture document with decision 8; collateral consistency; gates

### Item-by-item verdict on the 7 remediation items + 2 follow-up items

| ID | Verdict | Evidence location in the body (verified) |
|---|---|---|
| G-P0-2 | **Genuinely closed** | The §5 "assertion granularity table" (L141–149) has all three categories: strict equality (method / response code / CSeq method name), existence check only (To/From tag, Contact), pattern match (`Via` branch starting with `z9hG4bK`, random hex tag, `Call-ID` as `local-id@host`); the Call-ID difference between the two legs is listed separately |
| G-P0-3 | **Genuinely closed** | The four assertions of §5.2 S12 (L171–179) (the in-flight BYE completes normally / new calls use the new certificate / no process restart / no dropped calls); §6 step 2 (L191–192) classifies it as E4 hard constraint verification, non-blocking for E1, and it must pass before Accepted |
| G-P1-1 | **Genuinely closed** | The §4.1 "E8 scoring criteria" (L115–128) score six sub-items 0–5 each and combine them by weighting; the §4 E8 row (L109) changed to reference §4.1, and §6 step 3 references it as well |
| G-P1-2 | **Genuinely closed** | §6 step 3 "E6 verification method" (L198–199): the minimal build verification flow compiles the candidate stack and runs a minimal probe (S1); that flow passing is the evidence for E6 |
| G-P1-3 | **Genuinely closed** | §3.2 candidate table (L73–77) no longer has rsipstack; §3.3 (L88) lists it under explicit exclusion, with the reason "Rust is not in the current team's technology stack" as a rejection criterion |
| G-P1-4 | **Genuinely closed** | §6 step 4 (L200–203): (a) no formal candidate passes E1; or (b) "the person-hours to be invested > the existing sippy maintenance hours × 2" now has a quantitative threshold |
| G-P2-3 | **Genuinely closed** | §5 S7 has been split into S7a (SDP byte-for-byte unchanged, no field modified) and S7b (only the fields specified by the contract rewritten, the rest unchanged), with assertions for each (L159–160) |
| G2-P2-1 | **Genuinely closed** | §1.1 (L22–29) drops the reviewer-oriented wording and is changed to "the capacity estimate document is independently responsible for the conclusion, this ADR only cites it"; §5.1/§5.2 (L119–132) of `capacity-estimate.md` state independently and no longer cite the conclusions of ADR-0019, so the circular reference (at the conclusion layer) is broken |
| G2-P2-4 | **Genuinely closed** | §0 decision 8 (L20) of `system-architecture.md` = "sippy exits the production stack, the selection is in ADR-0019"; the §10 heading/body (L478/L480), §10.1 (L489), the §10.2 first node (L500), §10.3 (L528), §12.1 O3 (L630), §12.2 R9 (L646) and §13 (L664) are all synchronized; "双栈并行 / 460 commits / 保生产" have zero hits |

**Verdict summary**: the 7 round 1 remediation items plus the 2 round 2 follow-up items, 9 in total, are all **genuinely closed** (0 closed on the surface, 0 not closed).

> Re-review addendum: both the threshold (×2) of G-P1-4 and the measurement basis for "the existing sippy maintenance hours" are now defined — §6 step 4 (L203–204) of ADR-0019 gives the basis (the person-hours this team invested in the last 12 months) and the conversion basis (the contemporaneous timesheet or an estimated value), to be confirmed by the maintainer at evaluation time. This reservation has been eliminated.

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
| 4 | The front page date of ADR-0019 is earlier than the capture date in §2.1 | Fixed | The front page date (ADR-0019 L5) is now 2026-09-28, consistent with the capture date in §2.1 (L44) |

### Gate result (a single line)

**make gate**: `ruff format --check` ✅ / `ruff check` ✅ / `mypy` ✅ / pytest (unit+contract, 44 passed) ✅; afterwards the integration layer fails (`44 deselected`, pytest exit code 5) — this is the pre-existing expected behavior of `AGENT.md` §9 at the M0 stage, not introduced by this change.

### Conclusion

- **Are all 7 remediation items genuinely closed**: Yes. All 7 are **genuinely closed** (verified against the body, see the table above).
- **Are the 13 round 1 items closed end to end**: Yes. The Adjudication status of all 13 round 1 items and all 15 round 2 items is now "closed / verified", with no "modified" item left over; the inaccurate "equivalent to G2-*" mappings in the round 1 table have also been changed to the actual fix.
- **Is entering probe allowed**: technically allowed. The prerequisite of writing the baseline to disk in §6 step 0 of ADR-0019 has been defined at the document level; the candidates in §10.3 (L528) of the architecture document are now consistent with ADR-0019 §3.2 (baresip is not a candidate, sofia-sip is in the §3.3 exclusions), so it no longer constitutes a misleading signal.
- **Can the M0 block be lifted**: this re-review gives only the technical judgment — the gaps of ADR-0019 are genuinely closed and at the document level it meets the conditions to enter probe. Whether to lift the "blocks M0 sign-off" in `plan.md` §5.1 O2 is a **maintainer decision**; this re-review does not constitute grounds for lifting it (ADR-0019 is still Draft, not Accepted).

---

## 7. Sign-off

> This section is the sign-off record before ADR-0019 enters probe; a separate maintainer sign-off is still required when the ADR moves to Accepted.

- **Final conclusion**: conditional pass (Draft → Probe-ready)
- **Maintainer sign-off**: the maintainer authorized the AI agent to sign on their behalf (authorization date 2026-09-28)
- **Date**: 2026-09-28

Scope of the sign-off: the gaps recorded in this review record are all closed end to end, and ADR-0019 meets the conditions to enter probe at the document level.
This sign-off **does not mean** ADR-0019 moves to Accepted — Accepted still requires probe parity plus the completed deep evaluation of E6/E8/E9, followed by a separate sign-off.

---

## 8. Acceptance Record (Accepted)

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

If, during the M1 probe stage, any of the hard constraints or gates E1/E4/E5 fails verification, a fallback evaluation is triggered (§6 step 4 of ADR-0019):
- (a) no formal candidate passes the E1 gate; or
- (b) the total E8 maintenance hours > the existing sippy maintenance hours × 2

Fallback result: ADR-0019 is recorded as Rejected, and go-b2bua is re-evaluated or a fallback to sippy (including the two D1 disposition paths).

### Verification Method

- The status line of ADR-0019 has been updated to `已接受（Accepted）—— 选定 reSIProcate`
- Decision 8 of the architecture document has been synchronized
- The status of the 0019 row of the ADR registry has been updated to `accepted`
- plan.md O2 is unblocked, and the M0 milestone status changed from "blocked on O2" to "pending maintainer sign-off"
