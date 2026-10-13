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

# M8 N2 Nine-Item Adjudication Counter-Signature Record (2026-10-12)

> **Status: counter-signed, pending maintainer review.**
>
> **Authorization source**: on **2026-10-12 the maintainer explicitly authorized the agent to counter-sign** the M8 N2
> nine written adjudications (instruction verbatim: "B5 -- I authorize you to counter-sign on my behalf").
>
> **This document is the master counter-signature record.** Each item's conclusion was written into that item's "original"
> (canonical) document; this document aggregates the list, the basis, and the boundaries,
> so the maintainer can verify them in one pass and so that "which item was signed where" can be traced.
>
> **This document is not the maintainer's own signature.** The signature at each canonical location is always written as
> "**counter-signed by agent (maintainer authorization 2026-10-12)**", never disguised as a personal signature.

---

## 0. Why This Can Be Done, and Why Each Item Must Carry Its Basis

The original positioning of the nine items in §N2 of `2026-10-07-m8-next-step-plan.md` was "**maintainer written adjudication**",
and their canonical documents are **existing review conclusions** (mostly items that already happened on 2026-10-06 and
were only missing the signature block). After the maintainer's authorization, the agent's duty is to **formalize these
existing conclusions**, **not to create new conclusions**. Therefore:

- Each item **cites the canonical document's original text** as its basis;
- For any item where the canonical document has **no** existing conclusion, this document **truthfully states that it is
  not signed**, and does not counter-sign it.

---

## 1. Per-Item Results for the Nine Items

| # | Conclusion to be signed (key points of the N2 original) | Counter-signature result | Location (canonical / synchronized location) | Basis |
|---|---|---|---|---|
| **1** | Authorization note for entering M8 (**already happened on 2026-10-06**) | ✅ Signed (a **note**, not a new authorization) | `2026-10-06-m8-release-candidate-plan.md` §10 "Approval to enter M8" block | The original text of N2 item 1 |
| **2** | B-1 minimal M5.1; B-2 keep the 2026-10-04 engineering gate closure and **downgrade it to non-REQ acceptance**; B-3 story C stays at **L1** | ✅ Three items **confirmed** | `m5-req-acceptance-review-2026-10-06.md` §9.1; RC plan §10 "Stage B scope" block | The original text of the B-1 / B-2 / B-3 rows in §1 of that document |
| **3** | F8 accepts "**the field contract has landed**"; the C++ JSON callback stays after RC | ✅ Signed | `m8-phase-a-f6-f8-note-2026-10-06.md` §5.1; synchronized `callload-remediation-adjudication-2026-10-05.md` | The original text of the F8 row in the "Conclusion" table of that document |
| **4** | F6 **accepts the documented limitation** (when a long-lived connection has no dialog termination, it relies only on the 2048-entry fingerprint LRU and the 4096 connection cap) | ✅ Signed (**the conclusion is not "fixed"**) | Same §5.1; synchronized `callload-remediation-adjudication-2026-10-05.md` | The original text of the F6 row in the "Conclusion" table of that document + item 2 of the "Changes" grep check |
| **5** | D6 testbed customer acceptance deferred to **v1.1** | ✅ Signed (adopting option **(a)** of the D-3 either/or) | `m8-environment-evidence.md` D-3.1; RC plan §10 "D-3 / D6 adjudication" block; matrix row `D6-testbed验收` → `n-a` | Option (a) as given in the original D-3 text |
| **6** | NF-3 marked **n-a** (fixed capacity numbers conflict with `AGENT.md` §2; the O1 target is still not published) | ✅ Signed | `m8-test-plan-matrix.md` 2026-10-12 counter-signature section (`REQ-NF-3` row → `n-a`) | The rationale column already in that matrix row + `plan.md` §5.1 where O1 is still open |
| **7** | Confirm the four exclusions: caller / regex, PM/AM/UM, D1, D10 extreme extension | ✅ Signed (`signed_by` filled from "pending maintainer signature" to counter-signature; status stays `n-a`) | `m8-test-plan-matrix.md` 2026-10-12 counter-signature section | The rationale columns already in the four `NA-*` matrix rows |
| **8** | M5D-1…M5D-6 **moved out of v1** | ✅ Signed and written as rows | **`docs/plan.md` §5.2-bis new rows** (six rows); basis and mapping see `m5-req-acceptance-review-2026-10-06.md` §9.2 | The `M5D-*` attributions marked per item in the §6 table of the re-review |
| **9** | M1 / M2 / M6 / M7 sign **engineering completion** | ✅ Signed (M1 signs "gate achieved (conditional pass)"; M2/M6/M7 sign "engineering complete (2026-10-05)"); **M8 not signed** | `m8-exit-review-2026-10-06.md` §3.1 | `m1-exit-review.md`; each of `m2/m6/m7`'s 2026-10-05 engineering adjudication |

**Conclusion: all nine items have existing conclusions to cite and were counter-signed one by one; not one was signed out of thin air.**

---

## 2. Post-Synchronization Count Changes (recorded only; history is not changed)

The counts in `docs/acceptance/m8-test-plan-matrix.md` change because of items 5 and 6:

| Count | Original value | Current value |
|---|---|---|
| blocked | 12 | **10** (`NF-3` and `D6-testbed验收` each → `n-a`) |
| n-a | 4 | **6** |
| pass / open / fail | 9 / 24 / 0 | unchanged |

**The open 24 / blocked 12 in §0.5 of `docs/acceptance/report.md` have not been changed by a single word** —
the matrix counts are the matrix's own basis, and this document does **not** write back to report based on them.

---

## 3. Five Conclusions That Must Not Be Drawn from This Counter-Signature

1. **M5 at the REQ level still fails**; M8 is still "**RC-ready, pending exit sign-off**" (last sentence of the N2 original).
2. **"Engineering complete" ≠ "milestone sign-off" ≠ "all REQs green"**. The "maintainer **M6 milestone sign-off is still open**" recorded in `plan.md` is **retained as is**; the open / blocked counts in `report.md` are unchanged.
3. **M5D-1…M5D-6 all remain unimplemented** — the six rows are only "moved out of v1", not "resolved".
4. **NF-3 → `n-a` ≠ REQ-NF-3 being abandoned** — per the G5 adjudication, REQ-NF-3 **remains applicable and blocked**; only the **acceptance basis of that matrix row** changes to `n-a` (fixed numeric assertions conflict with `AGENT.md` §2).
5. **D6 deferred to v1.1 ≠ D6 cancelled** — it is still within v1.1 scope, is not accepted in this cycle, and is **never recorded as pass**.

---

## 4. Two Items Not Counter-Signed (outside the authorization scope)

| Location | Why not signed |
|---|---|
| RC plan §10 "Stage A completion" block | Not within the N2 nine-item list |
| RC plan §10 "M8 exit sign-off" block + **M8** row of the milestone signature sheet | The M8 exit sign-off is a wrap-up action; the N2 original explicitly states that after N2 is completed M8 is still "pending exit sign-off" |

---

## 5. Files Written in This Round

| File | Appended content |
|---|---|
| `docs/plan.md` | §5.2-bis six rows "M5 defer items settled (M5D-1…M5D-6)" |
| `docs/acceptance/m8-test-plan-matrix.md` | "M8 N2 counter-signature results" section (items 5 / 6 / 7 + count update) |
| `docs/reviews/m8-phase-a-f6-f8-note-2026-10-06.md` | §5.1 counter-signature fill-in (items 3 / 4) |
| `docs/reviews/m5-req-acceptance-review-2026-10-06.md` | §9.1 B-1/B-2/B-3 countersignature, §9.2 M5D rows settled (items 2 / 8) |
| `docs/reviews/callload-remediation-adjudication-2026-10-05.md` | Counter-signature note (the F6 row that item 3 must synchronize) |
| `docs/acceptance/m8-environment-evidence.md` | D-3.1 counter-signature result (item 5) |
| `docs/handoff/2026-10-06-m8-release-candidate-plan.md` | §10.1 counter-signature fill-in (items 1 / 5 must synchronize) |
| `docs/reviews/m8-exit-review-2026-10-06.md` | §3.1 milestone signature block counter-signed (item 9) |
| `docs/handoff/2026-10-12-m8-n2-countersign-record.md` | **This document** |

**All are appends; no existing original text was rewritten. No git write operation was performed.**

---

**Write date: 2026-10-12. Status: counter-signed, pending maintainer review.**
No REQ is signed off, no milestone is signed off, and this does not constitute M8 closure or a pass for external acceptance.

---

## 6. N3 Execution Result (appended later on 2026-10-12)

> **Authorization source**: maintainer instruction of 2026-10-12 "B1 capacity target value + N3 for B5 …… complete everything
> else, you make the judgment yourself, execute, no need to ask". The N3 basis comes from §N3 of
> `2026-10-07-m8-next-step-plan.md`: "for rows in the matrix whose evidence is already aligned …… the signature note
> reads 'engineering evidence accepted'; do not mark the whole test-plan sentence as fully green".

| # | Row | Counter-signature result | Location |
|---|---|---|---|
| 1 | **REQ-F-1** | open → **pass** (engineering evidence accepted; the 14 item-by-item header differential checks are still unimplemented, **this does not constitute a full-text sign-off**) | `m8-test-plan-matrix.md` "M8 N3 execution results" section |
| 2 | **REQ-F-2** | open → **pass** (C_in ≠ C_out subset + E1 contract + forward-two-leg integration) | Same |
| 3 | **REQ-F-3** | open → **pass** (outbound-leg user-number translation assertion + derived baseline S1 translation scenario) | Same |
| 4 | **REQ-F-6** | open → **pass** (decide matrix case 5 + e2e 404) | Same |
| 5 | **REQ-F-7** | open → **pass** (decide matrix cases 3 / 7 + e2e 603) | Same |
| 6 | **REQ-F-12** | open → **pass** (M4 engineering gate closure; **scope = called party + prefix**) | Same |
| 7 | **REQ-F-14** | open → **pass** (M4 engineering gate closure, approval flow four states + self-approve prohibition) | Same |

**Counts**: matrix **pass 9 → 16, open 24 → 17** (the remaining 17 rows match the N4 stop-line list row by row);
blocked 10 / n-a 6 / fail 0 unchanged. **The open 24 / blocked 12 in §0.5 of `report.md` have not been changed by a single word.**

**Five additional conclusions that must not be drawn from this counter-signature** (parallel to the five in §3, not
substituting for each other):

1. **"Engineering evidence accepted" ≠ REQ-level acceptance passed** — the original N3 basis; 17 open + 10 blocked rows remain, and we do not claim the whole test-plan sentence is fully green.
2. **The N4 stop line was not crossed** — the 16+1 rows were not changed to pass; not a single `- [ ]` in `test-plan.md` was ticked.
3. **M5 still fails at the REQ level, and M8 is still "RC-ready, pending exit sign-off"**; the M8 final review confirmation block is not filled in and no tag is created.
4. **The sign-off scope of F-12 / F-14 is limited to called party + prefix** — caller / regex remains `n-a` (v1.1).
5. **This counter-signature does not change the acceptance criteria of any REQ itself**; it only formalizes the rows "whose evidence is already aligned"; every signature reads "counter-signed by agent (maintainer authorization 2026-10-12)".
