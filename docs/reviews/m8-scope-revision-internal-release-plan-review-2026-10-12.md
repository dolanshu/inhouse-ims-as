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

# Review Record — M8 Scope Revision and Internal Release Wrap-Up Plan

- **Review target**: [`docs/handoff/2026-10-12-m8-scope-revision-internal-release-plan.md`](../handoff/2026-10-12-m8-scope-revision-internal-release-plan.md) (status: plan / uncommitted)
- **Review date**: 2026-10-12
- **Reviewer**: AI agent (TraeCode) —— review and gap listing only, **no signature**; the adjudications are the reviewer's recommendations, pending maintainer confirmation
- **Review scope**:
  - Consistency of the plan's factual statements about upstream documents (RC plan, 2026-10-10 inventory, 2026-10-09 SIP native plan, acceptance matrix `m8-test-plan-matrix.md`, `m8-environment-evidence.md`, `report.md`, `plan.md`, `deploy/docker/Dockerfile`, `environments.md`, `2026-10-12-o1-and-native-reproducibility.md`)
  - Internal consistency of the plan (§1 scope redivision / §2 six batches / §4 completion definition / §5 handover list / §6 adjudication items / §7 boundaries)
- **Review conclusion (historical, preserved)**: **conditional pass** —— the factual basis was verified to be basically accurate (see §3); 2 P1 and 2 P2 issues were found, none of which overturns the positioning of this plan (internal version / does not sign off M8), but they must be corrected before it can serve as an execution input.

---

## Current Status

> This section reflects the current on-disk reality; the original review conclusion above is preserved as history.

- **One-line conclusion**: the factual baseline check passed; 1 P1 inconsistent with upstream was found (the A3 Phase D order), plus 1 P1 internal conflict in the plan (§4.2 vs §1.1/§5/§7.2), plus 2 P2. Not recommended as an execution input before correction.
- **Gap statistics**: P0 = 0; P1 = 2 (G-1, G-2); P2 = 2 (G-3, G-4). Among these, 3 are "to be modified" and 1 is "not a problem (closed)".
- **Gate**: N/A (documentation-only review, no code changes).
- **Signature status**: **unsigned** (signing is the maintainer's action).
- **Unclosed items**: G-1, G-2, G-3 to be modified; all destinations are **the plan document under review** (§0.5 / §2 dependency diagram / §2.2 / §4.2 / §5 / §1.1 Table A); trigger condition = after the maintainer confirms the adjudications, a writing subagent corrects the document under review and this record is back-filled with the re-check conclusion.

---

## 1. Overall Assessment

This plan has a clear positioning and strong boundary discipline (repeatedly stating "does not sign off any REQ / does not sign off any milestone, does not change matrix status, does not change report.md counts, does not perform git write operations"), consistent with the constraints of `AGENT.md` §3.2 and §11. Its factual basis was verified item by item to be **basically accurate**: the matrix's current counts, the open/blocked row sets, the N3 countersignature basis, the `report.md` §0.5 counts, the version basis in `plan.md` §0 and §5.2 / §5.4, the Dockerfile status quo, the four-layer restriction basis, the environment registration, and the numbering-basis table all agree with upstream (see §3 for details).

The main problems are concentrated in two places: the first is that §2's handling of the A3 Phase D ordering is **inconsistent with upstream §4-D yet is labeled "implemented per §4-D"** (G-1); the second is that §4's completion definition conflicts with §1.1/§5/§7.2 over the requirement for open restriction rows (D12/O5-HA) (G-2). Both belong to the "half-synchronized" class of problems —— the plan's own remaining sections are not synchronized with upstream, so readers get mutually contradictory conclusions from different sections.

---

## 2. Gap List (P0 / P1 / P2)

### G-1 (P1) The A3 Phase D execution order is inconsistent with upstream §4-D, and is mislabeled as "implemented per §4-D"

- **Location** (in the document under review): §0.5 (L64), §2 dependency order diagram (L123–133), §2.2 execution order table (L156–162).
- **Plan's wording**: the execution order is written as `P1 S5 → P6 S11 → P2 S7a → P3 S6 → P4 S10 → P5 S9`, and §2.2 claims that "the schedule was finalized in `2026-10-09-sip-native-testing-plan.md` §4-D, and this batch implements it that way" (L152).
- **Upstream reality** ([`docs/handoff/2026-10-09-sip-native-testing-plan.md`](../handoff/2026-10-09-sip-native-testing-plan.md) §4-D.2, L179–189): the priority is **P1 S5 → P2 S7a → P3 S6 → P4 S10 → P5 S9 → P6 S11**; §4-D.3 boundary 1 (L193) explicitly states that "implementation starts in waves per **P1→P6**".
- **Difference and risk**: the plan moves P6 (S11 CANCEL vs final response race) from **last** up to **2nd**; yet the reason §2.2 gives for S11 ("proving the two race branches deterministically is the most costly, the flaky risk is the greatest") is precisely the reason upstream §4-D.2 (L188) puts it **last** —— reason and position contradict each other, and it conflicts with the statement "implemented per §4-D".
- **Suggested fix**: either one —— (a) restore the original §4-D order; (b) if a reorder is truly intended, explicitly declare in §2.2 that "this batch adjusted the §4-D order" and state the reason for the adjustment, while deleting/correcting the wording "implemented per §4-D". All three places (§0.5, §2 dependency diagram, §2.2) must be synchronized in one pass.

### G-2 (P1) §4's completion definition conflicts with §1.1/§5/§7.2 over the requirement for open restriction rows (D12/O5-HA)

- **Location**: §4.2 (L246) vs §1.1 Table A (L96, L100), §5 (L260), §7.2 (L286).
- **Plan's wording**: §4.2 requires that "**all 17 open rows** (including NF-10, NF-13, NF-14, NF-15, etc.) move to a final state (pass / n-a / defer, reasons mandatory), and **no unexplained open may be left**".
- **Conflict**: `D12/O5-HA` currently has the status **open** (matrix L117), and belongs to the external hard dependency restriction rows; §1.1 Table A, §5 and §7.2 all require that it "**keep its original status word (open)**" and point to Table A. Therefore D12/O5-HA cannot both "move to a final state" and "stay open" —— the two requirements cannot hold at the same time.
- **Suggested fix**: explicitly exempt the open restriction rows in §4.2 (at least D12/O5-HA), or carve that row out separately from the "open rows must reach a final state" counting basis and note its destination.

### G-3 (P2) The "moved out to the next release" list is inconsistent between §1.1 Table A and §5

- **Location**: §1.1 Table A (L91–98) vs §5 handover list (L262).
- **Explanation**: §5 lists "packaging 2.5 backup-restore (customer real cluster version) | customer real cluster drill not done | customer real cluster", but §1.1 Table A (moved out to the next release) **does not list this item**, yet does list the similar external dependency "packaging 2.4 traffic diversion / iFC coordination". The two lists have inconsistent inclusion criteria for similar items.
- **Suggested fix**: add "packaging 2.5 backup-restore (customer real cluster version)" to §1.1 Table A; or note in §5 the reason why it is outside Table A's basis.

### G-4 (P2) The row attribution of §1.2 Table B and the §2.3 evidence table does not fully correspond —— recommended to be judged **not a problem**

- **Location**: §1.2 Table B (L107) vs the §2.3 evidence table (L172–179).
- **Explanation**: §1.2 Table B puts NF-13 / NF-14 / NF-15 into the broad category of "evidence rows obtainable via simulator / kind", but the §2.3 evidence table lists only NF-2/NF-4/NF-9/NF-5, F-15 and 5.4-F-15真AS, NF-10; NF-13/NF-14 are pointed by the §2.3 tail note (L181) to the "sign-off and review" batch, and NF-15 belongs to the §2.5 batch.
- **Judgment**: **not a problem** (closed once the reason is given) —— the row attribution is actually complete and nothing is missing; the §2.3 tail note and §2.5 separately state the destinations; only readability could be optimized further.
- **Optional suggestion**: add a cross-reference in §2.3 so readers do not mistake NF-13/NF-14/NF-15 for omissions.

---

## 3. Consistency Check (against upstream documents)

| The Plan's Statement | Upstream Source | Conclusion |
|---|---|---|
| Matrix counts pass 16 / open 17 / blocked 10 / n-a 6 / fail 0 | [`m8-test-plan-matrix.md`](../acceptance/m8-test-plan-matrix.md) N2/N3 countersign section (L138–196) | True |
| The set of 17 open rows is exactly F-4/F-5/F-8/F-9/F-10/F-11/F-16/NF-2/NF-5/NF-9/NF-10/NF-13/NF-14/NF-15/S-1/S-4/D12/O5-HA | Same as above | True |
| The set of 10 blocked rows is exactly F-13/5.4-F-13/F-15/5.4-F-15真AS/NF-1/NF-4/NF-7/S-2/S-3/ADR-0008-演练 | Same as above | True |
| N3 countersign of 7 rows (F-1/F-2/F-3/F-6/F-7/F-12/F-14), with the basis "engineering evidence accepted", not REQ-level acceptance | Same as above (L170–196) | True |
| The `report.md` §0.5 counts are still open 24 / blocked 12 (pass 9 / n-a 4) | [`report.md`](../acceptance/report.md) §0.5 (L44–52) | True |
| `plan.md` §0 has no v1 / v1.1 definition; the product version number only refers to root `VERSION` (currently 0.2.0) | [`plan.md`](../plan.md) §0 (L11–18), `VERSION` | True |
| `plan.md` §5.2 contains D1~D12 (including D5 in-cluster PostgreSQL, D12 in-cluster PG/Redis HA) | [`plan.md`](../plan.md) §5.2 (L488–495) | True |
| The Dockerfile is still the M5 process shell (`ENTRYPOINT ["python", "-m", "as_platform"]`; `EXPOSE 5060/udp 5061/tcp` are port declarations only) | [`deploy/docker/Dockerfile`](../../deploy/docker/Dockerfile) (L23–40) | True |
| The release image gap is "filled before reopening M8"; the M8 row says "RC artifacts ready, exit sign-off still shelved" | [`plan.md`](../plan.md) (L11–18, L192–204), [`pre-m8-demo-review-plan.md`](../handoff/pre-m8-demo-review-plan.md) (L144), [`2026-10-07-m8-next-step-plan.md`](../handoff/2026-10-07-m8-next-step-plan.md) (L2–8) | True |
| `plan.md` §5.4: REQ-S-4 formally going all-green belongs to M8 or is signed off separately by the maintainer | [`plan.md`](../plan.md) (L551–562) | True |
| Restrictions: D-1 touches S-2/S-3, D-2 touches NF-1, the ADR-0008 drill, D12/O5-HA; NF-2/NF-4/NF-9 use our own kind, NF-5 uses the M7.1 transparent bridge (no Kamailio) | [`m8-environment-evidence.md`](../acceptance/m8-environment-evidence.md) (L26–38, L39–55, L69–85) | True |
| Environment registration `dev-win03ib7niepf0` (WIN-03IB7NIEPF0), kind 0.24.0, kubectl 1.31.4, clusters as-m5 / as-m71 | [`environments.md`](../environments.md) (L37–49), [`m71-sim-platform-evidence.md`](../acceptance/m71-sim-platform-evidence.md) (L10–17) | True |
| The o1 document §2 `deploy/compose` is the PG/Redis integration dependency; §4 20→1280 CPS all successful, saturation point not reached, resource data not recorded | [`2026-10-12-o1-and-native-reproducibility.md`](../handoff/2026-10-12-o1-and-native-reproducibility.md) (L48–67, L137–175) | True |
| Numbering-basis table: RC plan A-1~A-7 / B-1~B-7 / D-1~D-3 / E-1~E-6; the 2026-10-10 inventory A2~A6 (Lane A) / B1~B6 (Lane B) | [`2026-10-06-m8-release-candidate-plan.md`](../handoff/2026-10-06-m8-release-candidate-plan.md) §4; [`2026-10-10-unfinished-assessment-and-next-plan.md`](../handoff/2026-10-10-unfinished-assessment-and-next-plan.md) Lane A/B | True |
| The 7 referenced handoff files and the N2 countersign record all exist | `docs/handoff/` | True |
| "A3 Phase D implemented per §4-D" (execution order) | [`2026-10-09-sip-native-testing-plan.md`](../handoff/2026-10-09-sip-native-testing-plan.md) §4-D | **Does not match —— see G-1** |

---

## Adjudication (adjudication record)

> The adjudications are **the reviewer's recommendations** and may only be executed after maintainer confirmation; signing is the maintainer's action.

| ID | Source | Issue Summary | Adjudication | Fix Plan | Status | Verification Method | Notes |
|---|---|---|---|---|---|---|---|
| G-1 | Reviewer (consistency check) | The A3 Phase D order in §0.5/§2/§2.2 does not match upstream §4-D, yet is labeled "implemented per §4-D" | Accepted (recommendation) | Restore the original §4-D order; or explicitly declare the order adjustment and its reason and delete the "implemented per §4-D" wording; synchronize all three places | To be modified | Document update | Pending maintainer confirmation |
| G-2 | Reviewer (internal consistency) | §4.2's "all 17 open rows move to a final state" conflicts with §1.1/§5/§7.2's "keep open" for D12/O5-HA | Accepted (recommendation) | Exempt the restriction open rows in §4.2, or carve them out of the "open must reach a final state" basis | To be modified | Document update | Pending maintainer confirmation |
| G-3 | Reviewer (internal consistency) | §1.1 Table A does not include "packaging 2.5 backup-restore (customer real cluster version)" from §5 | Accepted (recommendation) | Add it to Table A, or note in §5 the reason why it is outside Table A's basis | To be modified | Document update | Pending maintainer confirmation |
| G-4 | Reviewer (readability) | The row attribution of §1.2 Table B and the §2.3 evidence table does not fully correspond | Rejected | No change needed; optional: add a cross-reference in §2.3 | Closed | Already explained in the document | Not a problem: the §2.3 tail note and §2.5 separately state the destinations of NF-13/NF-14/NF-15 |

> Re-check round 1 determines that all three of G-1 / G-2 / G-3 are genuinely closed (see the "AI Re-check Conclusion" section below); the status column update is pending maintainer confirmation.

---

## AI Re-check Conclusion (Verification)

This round is the **first review**, and no post-correction re-check has been performed yet. After G-1 / G-2 / G-3 are dispositioned, an **independent re-check agent** must return to the body text of the document under review and prove each item clause by clause (the table's self-report must not be taken on trust), determine "genuinely closed / superficially closed / not closed", check whether new inconsistencies were introduced, and then back-fill this section.

### Re-check round 1 (2026-10-12)

**Re-checker**: independent re-check agent (m8-verifier). Re-check method: return to the body of the plan under review and read the current text (accepting no paraphrase), and compare clause by clause against upstream [`2026-10-09-sip-native-testing-plan.md`](../handoff/2026-10-09-sip-native-testing-plan.md) §4-D.2 / §4-D.3 and [`m8-test-plan-matrix.md`](../acceptance/m8-test-plan-matrix.md) L117.

**Clause-by-clause verification results**:

| ID | Judgment | Evidence (current text of the plan under review, line number + excerpt) |
|---|---|---|
| G-1 | **Genuinely closed** | All three places now follow the original upstream §4-D.2 order (P1 S5 → P2 S7a → P3 S6 → P4 S10 → P5 S9 → P6 S11): the §0.5 schedule paragraph (L64) "P1 S5 two-leg normalization cross-check → P2 S7a SDP corpus → P3 S6 rule priority → P4 S10 non-2xx → P5 S9 in-dialog → P6 S11 CANCEL race"; the §2 dependency order diagram (L126) "S8 pre-emptive re-capture → P1 S5 → P2 S7a → P3 S6 → P4 S10 → P5 S9 → P6 S11"; rows 1–6 of the §2.2 execution order table (L157–163) are in turn P1 S5 / P2 S7a / P3 S6 / P4 S10 / P5 S9 / P6 S11, and row 0 is the S8 baseline re-capture (consistent with the upstream §4-D.2 blocking row "after re-capture completes, it is recommended to insert after P3"). The "this batch implements it that way" above the §2.2 table (L153) is now true; the scenario column and the notes column correspond row by row to the upstream P1–P6 "why this position" (e.g. the P6 row L163 "proving deterministically is the most costly, the flaky risk is the greatest" is consistent with the reason for putting it last upstream), with no mis-ordering. |
| G-2 | **Genuinely closed** | Item 2 of §4 (L247) now explicitly exempts: "among the 17 open rows, the external hard dependency restriction row D12/O5-HA keeps open per §1.1 Table A and points to Table A (not required to reach a final state), and the remaining 16 rows all reach a final state……among the 10 blocked rows……restriction rows (S-2 / S-3 / NF-1 / ADR-0008-演练 / D12/O5-HA) keep their original status words and point to Table A". It no longer conflicts with §1.1 Table A (L96 collection row + L101 "keep the original status words (blocked / open)"), §5 (L261) or §7.2 (L287); the upstream basis for D12/O5-HA, open + restriction (matrix L117 "cannot be signed as pass \| open"), also matches. |
| G-3 | **Genuinely closed** | §1.1 Table A (L98) now includes "packaging 2.5 backup-restore (customer real cluster version) \| customer real cluster drill not done; kind bundled state is not production backup-restore \| customer real cluster", consistent with the same item in §5 (L263). |
| G-4 | **Closed (not a problem)** | The original judgment is maintained; the optional cross-reference has been added —— the §2.3 tail note (L182) now contains "(NF-15 is not absent from the table above by design: it belongs to the §2.5 "performance and capacity" batch; the destinations of NF-13 / NF-14 are given in the previous sentence of this paragraph.)". |

**Newly introduced issue check**:

- During the re-check it was found that the §2.3 boundary paragraph states "the live capture of NF-13 / NF-14 and the real trigger involve X1, and the final state is handled with reasons in the 'sign-off and review' batch" twice (the original sentence + the newly added parenthetical sentence). A correction has been executed: the parenthetical sentence was reduced to the minimal form that only keeps the cross-reference (the NF-15 destination + pointing NF-13/NF-14 back to the previous sentence); after the correction, the destinations of the three rows NF-13 / NF-14 / NF-15 in that paragraph are each stated only once, with no omission and no duplication.
- Post-correction re-inspection: no new inconsistency was found —— this correction touches no ordering, counting basis or status-word wording, and only deletes a duplication.

**Boundary statement**: this re-check only covers whether the corrections landed, **does not sign off any REQ / milestone**, and does not constitute maintainer confirmation; the Adjudication table status column update is pending maintainer confirmation.

---

## Signature

- **Signature status**: **unsigned**.
- **Authorization basis**: none. This review was performed by an AI agent, which only produced a gap list and recommended adjudications; the adjudications and the signature must be made by the maintainer (`AGENT.md` §3.2, §3.3; `.trae/rules/review-adjudication.md`).

---

(This record is review round 1; the target under review is a **plan**, and this record signs off no REQ, signs off no milestone, and changes no matrix row status.)
