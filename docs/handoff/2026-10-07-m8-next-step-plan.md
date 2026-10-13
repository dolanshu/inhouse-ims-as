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

# M8 next step (2026-10-07)

> **Status**: **still on hold (2026-10-07)**. M7.1 has closed on the engineering side. The remaining hold condition is that no real operator S-SBC / customer K8s testing is done before Close; see [`acceptance/m8-environment-evidence.md`](../acceptance/m8-environment-evidence.md). N2–N4 are not executed during the hold, and the M8 final-review confirmation column is not filled in. Before reopening, the published image carries SIP listening again.  
> **Upstream**: [`2026-10-06-m8-release-candidate-plan.md`](2026-10-06-m8-release-candidate-plan.md) (the master plan for phases A–E; not reopened here)  
> **Facts**: `master` / `origin/master` @ `20e3d07` (`M8 part 1`).

This document only schedules **landing existing artifacts** and **maintainer adjudications that do not depend on the lab**. The M8 exit signature, tagging, and on-site evidence collection are not part of this step.

---

## 1. Where we are now

| Already in `20e3d07` |
|---|
| F8 field contract + contract tests + `emit_native_log_event` JSON enrichment |
| F6: an ADR annotation at the fingerprint table eviction point (behaviour unchanged) |
| Minimal M5.1: Helm H-1…H-4 fail-closed, `chart-check` onprem and exit-code assertions, kind scripts K-1/K-2 |
| `make gate-strict`, `scripts/check_adr_annotations.py` |
| Sign-off matrix, environment evidence, M5 REQ re-adjudication, M8 exit review, Phase A F6/F8 record, `report.md` §0 |

---

## 2. Order

### N2 — Maintainer written adjudication (does not depend on the lab, does not close)

For each item, change the **authoritative source** and update the references along with it, so that one place being signed off does not leave the backlog still writing "not closed".

| # | Conclusion signed | Authoritative source | Must be synchronized |
|---|---|---|---|
| 1 | Authorization to enter M8, countersigned (already happened on 2026-10-06) | RC plan §10 "Approval to enter M8" | — |
| 2 | B-1 minimal M5.1; B-2 keep the 2026-10-04 engineering closure and downgrade it to non-REQ acceptance; B-3 Story C stays L1 | [`m5-req-acceptance-review-2026-10-06.md`](../reviews/m5-req-acceptance-review-2026-10-06.md) confirmation column | RC plan §10 "Phase B scope" |
| 3 | F8 accepts "the field contract has landed"; the C++ JSON callback stays after RC | [`m8-phase-a-f6-f8-note-2026-10-06.md`](../reviews/m8-phase-a-f6-f8-note-2026-10-06.md) §5 | the F8 row of [`callload-remediation-adjudication-2026-10-05.md`](../reviews/callload-remediation-adjudication-2026-10-05.md) (currently "not closed") |
| 4 | F6 **accepts the documented limitation** (a long-lived connection with no dialog termination relies only on the 2048-entry fingerprint LRU and the 4096 connection cap) | same §5 | the F6 row of the adjudication. The conclusion is not "fixed" |
| 5 | D6 testbed customer acceptance is pushed to **v1.1** | [`m8-environment-evidence.md`](../acceptance/m8-environment-evidence.md) D-3 | change `D6-testbed验收` in the matrix to n-a; RC plan §10 |
| 6 | NF-3 is marked **n-a** (a fixed capacity number conflicts with AGENT.md §2; the O1 target is still not published) | [`m8-test-plan-matrix.md`](../acceptance/m8-test-plan-matrix.md) | — |
| 7 | Confirm the four exclusions: calling/regex, PM/AM/UM, D1, D10 extreme expansion | the `signed_by` cells of the corresponding n-a rows in the matrix | write D1 in the note as an accepted risk, or raise a separate migration item |
| 8 | M5D-1…M5D-6 are **moved out of v1** | a new row in `plan.md` §5 (written by the maintainer) | the co-signature column of the M5 REQ re-adjudication. Without these 6 rows landing, M5 REQ stays "does not pass" |
| 9 | M1 / M2 / M6 / M7 sign **engineering complete** | M1: [`m1-exit-review.md`](../reviews/m1-exit-review.md) and the historical §6 of `report.md`; M2/M6/M7: their respective 2026-10-05 engineering adjudications | referenced by §3 of [`m8-exit-review-2026-10-06.md`](../reviews/m8-exit-review-2026-10-06.md); not serving as the authoritative source on their own |

After N2, M5 at the REQ level is still "does not pass", and M8 is still "RC ready, awaiting exit signature".

### N3 — Rows in the matrix whose evidence is already aligned

All of these can be done after N2. The signature note reads "engineering evidence accepted"; do not mark a whole test-plan row all-green.

- The 9 rows already marked pass: NF-6, NF-8, NF-11, NF-12, KERNEL-§5; G-1/G-2/G-3 note that each PR is still reviewed by the maintainer; G-4 notes that the local `make gate` is green and e2e is still non-blocking.
- The 7 signable rows among the open ones: F-1, F-2, F-3, F-6, F-7, F-12, F-14. The scope of F-12/F-14 is callee + prefix.

### N4 — Stop line

At the end of this step, the following items stay as they are:

- The M8 final-review confirmation column is not filled in; no tag is cut (AGENT.md §10.4).
- The M8 row in `plan.md` §4 stays "RC ready, awaiting maintainer exit signature".
- These 16 open rows are not changed to pass: F-4, F-5, F-8, F-9, F-10, F-11, F-16, NF-2, NF-5, NF-9, NF-10, NF-13, NF-14, NF-15, S-1, S-4, plus D12/O5-HA. F-5 is explicitly not signed as pass before Route/Record-Route re-collection.
- The 12 blocked items may only be written as defer or v1.1, not as pass: F-13, 5.4-F-13, F-15, 5.4-F-15 real AS, NF-1, NF-4, NF-7, S-2, S-3, ADR-0008 drill; if NF-3 and D6 have already been changed to n-a per N2, then remove them from this blocked list.
- D-1 (operator PKI / public-network S-SBC, matrix S-2/S-3) and D-2 (customer K8s NF-1 live) get no evidence collected in this step. These two are written as defer separately, which is still not enough to fill the M8 final-review confirmation column.

---

## 3. What happens only after this step

Even when D-1/D-2 are both closed, M8 still cannot be signed. The confirmation column is filled in only after every row below is already in a terminal state (pass / n-a / written defer or v1.1); as long as a defer remains, the conclusion is conditional pass, not all-green. The tag is executed by the maintainer only after that column is filled in (AGENT.md §10.4).

| Action afterwards | Rows it can close | Rows it cannot close |
|---|---|---|
| Schedule evidence collection, or accept D-1 / D-2 in writing | S-2, S-3, NF-1 | F-4, F-5, F-8, F-9, F-10, F-11, F-13, F-15, F-16, NF-2, NF-4, NF-5, NF-7, NF-9, NF-10, NF-13, NF-14, NF-15, S-1, S-4, D12/O5-HA, ADR-0008 |
| Supplement evidence for the remaining rows item by item, or write them as n-a / defer / v1.1 | the right-hand column above | — |

Until the rows in the right-hand column are written as terminal states, the M8 final-review confirmation column stays blank, and the M8 row in `plan.md` §4 stays "RC ready, awaiting maintainer exit signature".
