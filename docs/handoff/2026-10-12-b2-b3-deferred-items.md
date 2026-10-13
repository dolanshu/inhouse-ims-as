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

# B2 / B3 Deferred Items Register (requirement + ADR drafting, implemented next phase)

> **Landed: 2026-10-12. Status: registered, not drafted, not implemented.**
>
> **Maintainer decision 2026-10-12**: drafting the requirement and ADR for B2 / B3 **is major work and is not done this round**;
> it is **kept as a separate item to be done later**; **feature implementation goes into the next phase and is not done now**.
>
> **This file is the in-repo tracking carrier for these two items** (this project has no external issue tracker; in-repo documents are the tracking system ——
> consistent with the adjudication stance taken for A4-3 "separate issue", which uses
> [`../acceptance/2026-10-11-wave2-replay-register.md`](../acceptance/2026-10-11-wave2-replay-register.md) as its carrier).
>
> **This file signs off no REQ, starts no implementation, and constitutes no external commitment.**

---

## 0. First, What State B2 / B3 Are Actually In

These two items are often misread as "not yet adjudicated". **They are not** — **the values have long since been adjudicated**; what is missing is **engineering implementation**:

| Item | Adjudicated value | Adjudication source | Current status |
|---|---|---|---|
| **B2** | O4 = default retention **10 days**, deployment-configurable; D5 = **in-cluster PostgreSQL**; Redis continues to serve runtime checkpoint | §0-A.6 **G6 / B2 + D5** (adjudicated 2026-10-10, synced to `plan.md` §5 on 2026-10-11) | **value adjudicated**; trace storage / query / delete **not implemented** |
| **B3** | O5 = **in-site N+1 + cross-site 1+1 warm standby**; D3 = **Redis primary/replica + Sentinel** (ADR-0008) | §0-A.6 **G7 / B3 + D3** (adjudicated 2026-10-10) | **value adjudicated**, Sentinel **not implemented**; **RPO / RTO numbers still not adjudicated** |

**Therefore the content of this item is "turn the adjudicated values into implementable engineering", not "adjudicate once more".**

---

## 1. Item B2 · Call Trace Retention and Storage

### 1.1 What Must Be Delivered

| # | Deliverable | Explanation |
|---|---|---|
| 1 | **requirement** | requirement entries for the three capabilities of trace storage / query / delete; including retention-period semantics (**cleanup trigger point** and **time-origin definition** — explicitly marked at adjudication time as "implementation detail to be defined") |
| 2 | **ADR** | D5 has been settled as in-cluster PostgreSQL, but the deployment shape of "in-cluster" (StatefulSet? reuse the PG in the existing `deploy/compose`, or start a new one inside the chart?), the backup strategy, and the relationship to ADR-0026 (D12 in-cluster PG/Redis) all need an ADR to settle |
| 3 | Implementation (**next phase**) | storage / query / delete + cleanup trigger |

### 1.2 Known Preconditions (needed when drafting)

- The "pending D5 adjudication" wording in `docs/product/security-privacy.md` §2 / §3.1 and `docs/operations/backup-restore.md` §1
  was synced on 2026-10-11, as an addendum, to "value adjudicated, implementation not landed" (register §2 P3).
- The fact recorded in `security-privacy.md` §4.1 that the "**chart has no backup Job**" is **unchanged** — the backup/restore solution therefore remains unclosed.
  This point must be addressed when drafting the ADR, otherwise the ADR will conflict with repo facts.
- The adjudication original text states "**implementation not landed**" and that it "must not be marked as resolved".

### 1.3 Blocked Downstream Items (unblocked once drafting completes)

- The PDPO retention period and storage scheme in `docs/product/security-privacy.md` (currently unable to state "the system cleans up after 10 days")
- `docs/product/ne-datasheet.md` if it contains related wording
- Any packaging deliverable description that depends on "traces are queryable"

---

## 2. Item B3 · Redis HA and Disaster Recovery

### 2.1 What Must Be Delivered

| # | Deliverable | Explanation |
|---|---|---|
| 1 | **requirement** | disaster recovery capability requirement; including **RPO / RTO numbers** — **the adjudication explicitly did not settle these values**, and they must be added during the requirement phase, otherwise acceptance is impossible |
| 2 | **ADR** | D3 has chosen Redis primary/replica + Sentinel (ADR-0008), but whether ADR-0008 covers the **concrete Sentinel topology** (how many Sentinels, quorum, relationship to K8s scheduling) must be confirmed; if insufficient, a new ADR or a revision is needed |
| 3 | Implementation (**next phase**) | Sentinel deployment and failover verification |

### 2.2 Known Preconditions (needed when drafting)

- The **client wiring** for D3 was resolved on 2026-10-05 (`m2-d3-sentinel-adjudication-2026-10-05.md`);
  the only thing currently undecided is the **HA topology**.
- The adjudication explicitly says "**no rack / AZ-level fault tolerance is promised**" — the requirement must not be written as rack-level disaster recovery.
- The RPO / RTO and HA sections of `docs/operations/backup-restore.md` were synced on 2026-10-11 to "value adjudicated, implementation not landed".
- The `plan.md` §5.2 D3 row and §5.1 O5 row both carry inline notes; those are authoritative when drafting.

### 2.3 Blocked Downstream Items

- The RPO / RTO numbers in `docs/operations/backup-restore.md` (currently empty)
- `docs/product/security-privacy.md` §4.1
- Any availability commitment in external material

---

## 3. Why This Is Not Done This Round (recorded faithfully)

1. **It is requirement-level work**: per `AGENT.md` §3, it must go through requirement → ADR → HLD/LLD → contract → code + tests → acceptance items + review record.
   The **drafting** of the requirement and ADR itself requires first reading all relevant primary documents (ADR-0008, ADR-0026, the M2 D3 adjudication, the two downstream documents),
   which cannot be completed by a single instruction.
2. **B2 and B3 are entangled**: trace storage selects in-cluster PostgreSQL, while the high-availability shape of PG is in turn related to D12 (ADR-0026)
   and to B3's disaster recovery baseline (cross-site 1+1 warm standby). Drafting them separately would produce two mutually conflicting ADRs.
3. **The maintainer has been explicit**: this round only records the items; the feature is implemented next phase.

---

## 4. Start Conditions (confirm before kicking off next time)

- [ ] The maintainer authorizes starting the requirement drafting
- [ ] The **B3 RPO / RTO numbers** have values (otherwise the requirement has nowhere to put acceptance criteria)
- [ ] Confirm the PG deployment shape for B2 and its relationship to ADR-0026 (revision or a new ADR)
- [ ] Confirm whether B2 / B3 should be **merged** into one "state and persistence" requirement + ADR, or kept separate

---

## 5. Deferred to the Next Release (added later on 2026-10-12)

> **Maintainer decision 2026-10-12**: drafting the requirement and ADR for B2 / B3 (**including the B3 RPO / RTO values**)
> is **deferred in its entirety to the next release**; not started this round, and **it will not be raised separately again**
> (same stance as §12 "adjudicated-but-not-done register area" of
> [`2026-10-10-unfinished-assessment-and-next-plan.md`](2026-10-10-unfinished-assessment-and-next-plan.md):
> subsequent status inventories only cite the pointer and never restate item by item).

- All content of §0–§4 of this document **remains in effect** as input when the next release starts;
- The four start conditions of §4 are **retained verbatim** — confirm each one before the next release starts work; no start without confirmation;
- **Adjudicating the RPO / RTO values is deferred as well** — it is an external availability commitment and must be valued by the maintainer, not adjudicated by the agent;
- **Restart timing**: set by the maintainer when scheduling the next release; at that point, **append** the restart record to this document without rewriting it.

> **Destination pointer (added 2026-10-13; the original text of section 5 above is retained unchanged)**: the deferred registrations in this document are uniformly consolidated in
> [`../next-release-v1.1-plan.md`](../next-release-v1.1-plan.md) — **B2** (O4 = default 10-day retention, deployment-configurable,
> D5 = in-cluster PostgreSQL; trace storage / query / delete not implemented) see **§4-1**; **B3** (O5 / D3 selects Redis primary/replica + Sentinel,
> not implemented) see **§4-2**; **the four start conditions of §4 of this document** are retained verbatim as **§4.3** of that document, no start without confirmation;
> the **RPO / RTO values** are an external availability commitment and must still be valued by the maintainer, registered as **§7-4** of that document.
> All content of §0–§4 of this document **remains in effect** as input when the next release starts; the restart record will be **appended** to the corresponding row of that document at that time, without rewriting this section.

---

**Landed: 2026-10-12. Status: registered, not drafted, not implemented.**
(Related: [`2026-10-10-unfinished-assessment-and-next-plan.md`](2026-10-10-unfinished-assessment-and-next-plan.md) §4 B2 / B3;
upstream adjudication: the G6 / G7 rows of the §0 decision record table in `docs/plan.md`.
This file signs off no REQ, starts no implementation, and constitutes no external commitment.)
