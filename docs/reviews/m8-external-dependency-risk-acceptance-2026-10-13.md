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

**This document is the maintainer's 2026-10-13 written risk-acceptance adjudication (the premise document of path C), not evidence of verified pass.**

# M8 External Hard Dependency Written Risk Acceptance (Path C, 2026-10-13)

- **Adjudication item**: M8 exit sign-off —— **path C: sign the M8 exit sign-off + accept the external hard dependency risk in writing**
- **Adjudication date**: 2026-10-13
- **Adjudicator**: **maintainer (own signature —— to be filled in)**
- **Signature fill-in (2026-10-13)**: **agent countersignature (maintainer authorized on 2026-10-13)** —— authorization source: the maintainer's 2026-10-13 instruction "**authorized countersignature**". **Not the maintainer's own signature.**
- **Basis**:
  1. [`../acceptance/report.md`](../acceptance/report.md) §0.9 item 1, the **existing clause**, verbatim: "schedule carrier PKI lab and external-network S-SBC joint debugging (D-1), customer K8s live baseline (D-2), and file desensitized evidence per env-evidence §0; **or accept the risk in writing in the overall review**". This document exercises the "or" branch of that clause.
  2. The maintainer's 2026-10-13 instruction "**C**" —— the M8 milestone is to be closed, via the path of signing the exit sign-off + at the same time accepting the external hard dependency risk in writing.
- **Execution environment**: `dev-win03ib7niepf0`
- **Nature**: this document is a **precondition document for the signature**, not evidence; it does not replace any acceptance row, and does not change the status word of any matrix row.

---

## 1. Item-by-Item Acceptance List (Four External Hard Dependencies)

| # | Dependency | What Is Missing | Why This Release's Evidence Cannot Substitute | Restart Condition | Destination |
|---|---|---|---|---|---|
| 1 | **D-1** Carrier PKI + external-network S-SBC (touches matrix **S-2 / S-3**) | Missing a **carrier PKI lab** and an **external-network S-SBC peer** | TLS in this release uses a **test CA** (self-signed certificate chain), which **is not equivalent to a carrier-issued chain**; the M7.1 simulated transparent bridge is not a carrier S-SBC; the test CA does not sign REQ-S-2 / REQ-S-3 | **Separate maintainer adjudication + external resources in place** (carrier lab and external-network peer available); **deferred ≠ cancelled** | Next release list |
| 2 | **D-2** Customer K8s (touches **NF-1 live kill / restart / BYE**) | Missing a **customer cluster** | **A kind-owned cluster is not customer K8s**: network policies, storage classes, node behavior and real operational actions (live kill / restart / in-dialog BYE) are all non-equivalent; kind evidence only reaches the engineering and integration layers | **Separate maintainer adjudication + external resources in place** (customer cluster and a cooperation window available); **deferred ≠ cancelled** | Next release list |
| 3 | **ADR-0008** Cross-site switchover drill | Requires **two customer / production sites** to perform a site-level switchover | **A single lab cluster does not count**: a single cluster has no site boundary, no cross-site clock and network partition conditions, so the drill conclusion is not transferable | **Separate maintainer adjudication + external resources in place** (dual-site environment available); **deferred ≠ cancelled** | Next release list |
| 4 | **D12 / O5** Production Redis and PostgreSQL HA | Missing a **production-grade HA deployment** (Sentinel / Cluster, streaming replication, PITR) | **kind bundled state is not production HA**: it does not cover Sentinel failover, PostgreSQL streaming replication or PITR recovery drills; the backup-restore drill has only been verified on bundled PG | **Separate maintainer adjudication + external resources in place** (production HA environment available); **deferred ≠ cancelled** | Next release list |

**Uniform restart-condition basis**: **separate maintainer adjudication + external resources in place**; **deferred ≠ cancelled**. All four items roll over into the **next release list**; this release does not open an item, does not implement it, and does not accept it.

> **Destination pointer (appended 2026-10-13; the table above and this paragraph are preserved unchanged)**: the landing point of the "next release list" referred to in this paragraph is
> **§2** (external hard dependency category) of [`../next-release-v1.1-plan.md`](../next-release-v1.1-plan.md) —— the four items in this table are rows 1–4 of that section
> (D-1 / S-2 / S-3, D-2 / NF-1 live, ADR-0008 cross-site switchover drill, D12 / O5),
> packaging 2.4 traffic diversion / iFC coordination and 2.5 backup-restore are rows 5–6 of that section, X1 capture wiring is row 7 of that section, and **all seven are itemized inside the §2 table**;
> the wording follows the original text of §1 of this document. Any subsequent status inventory, reporting, handoff or new-session opening that touches the leftover items of this table shall **cite only this pointer**,
> and shall not expand them item by item, remind them separately, or list them again under "required maintainer actions".

---

## 2. v1.1 Item-Opening Confirmation (confirmed by the maintainer on 2026-10-13)

The following items were confirmed by the maintainer on 2026-10-13 to be opened as items of the **next release (v1.1)**; **this release does not open them and does not implement them**. On start they shall uniformly follow the **requirement → ADR → design → review** process (the same pattern as the existing FM / call trace).

| # | Item | Content |
|---|---|---|
| 1 | **F-5** | **Record-Route** on the trunk side of product AS forwarding |
| 2 | **F-8** | **Real-stack cross-check of the three CANCEL branches** + native C++→Python JSON callback |
| 3 | **F-9** | **in-dialog re-INVITE / UPDATE** |
| 4 | **F-11** | **CANCEL before any downstream response** |
| 5 | **F-13 / 5.4-F-13 / NF-7 Call Trace** | Query the SIP message trace by Call-ID + retention-period cleanup; **adjudicated as a major missed item** (a regression of POC baseline capability; product-grade implementation has so far been zero) |

Items 1–4 in the table above are the 4 `defer` rows in the matrix; item 5 is a major missed item. **Not a single status word** of these 4 `defer` rows in the matrix, nor of the rows related to F-13 / 5.4-F-13 / NF-7, is changed (this document does not touch the matrix file).

> **Destination pointer (appended 2026-10-13; the table above and this paragraph are preserved unchanged)**: the five items in the table above have been merged into
> **rows 1–5 of §3** of [`../next-release-v1.1-plan.md`](../next-release-v1.1-plan.md) (the numbering, content and "why it is not implemented in this release"
> follow the original text of this table), and that document's §3 **adds same-origin deferred features**: §3-6 REQ-F-12 caller ID / regex rules (four-dimension UI),
> §3-7 Lane D 4.2 long-run stability report and 4.3 API version compatibility policy, §3-8 zero-call-loss rolling upgrade enhancement feature, §3-9 FM (Fault Management).
> The start process is uniformly requirement → ADR → design → review; subsequent inventories cite only this pointer and do not restate this table's contents item by item.

---

## 3. Boundaries (no over-conclusions may be derived from this document)

1. **Risk acceptance ≠ verified pass ≠ these rows becoming final.** What this document accepts is the fact that "evidence cannot be obtained in this release", not that "it has already been verified as qualified".
2. **These rows in the matrix keep their original status words** (`blocked` / `defer`). This document is only a **precondition document for the signature**, not a status-change instruction; the matrix file has not been modified.
3. **No restriction is lifted**, and **no authorization is given to incidentally advance** the evidence-gathering or implementation of these dependencies on this machine; any advancement requires a separate maintainer adjudication and authorization.
4. **No external capacity or SLA commitment is produced.** The external commitment value for O1 is still left blank; the internal engineering target (loopback CPS 1280) is internal-only.
5. **This document signs off no REQ**, and does not constitute any REQ-level acceptance conclusion; **M5 REQ-level is still a fail**.
6. **The signature covers milestone exit, not REQ-level acceptance.** The M8 exit sign-off being valid does not mean M8 is all green, does not mean a release has been made, and does not mean the acceptance items in the closing conclusion have been met.
7. **The internal version positioning is unchanged**: `VERSION` remains `0.2.0`, is not bumped, not tagged, and the chart is not synced with the internal build. The tag is performed by the maintainer only (`AGENT.md` §10.4).
8. This document performed no git write operations (no add / commit / tag / push / branch / stash).

---

## 4. Signature Block

| Item | Record |
|---|---|
| Adjudication item | M8 exit sign-off —— path C (sign-off + written acceptance of the external hard dependency risk) |
| Adjudication date | 2026-10-13 |
| **Adjudicator (signature)** | **agent countersignature (maintainer authorized on 2026-10-13)** (**not the maintainer's own signature**) |
| Effective condition | **This block takes effect after it is filled in and signed by the maintainer themselves**; before it is filled in, this document is in the adjudicated-but-not-yet-effective state. **(Satisfied on 2026-10-13** —— this block has been filled in by an agent countersignature, on the basis of the maintainer's same-day "authorized countersignature" instruction; **countersignature ≠ own signature**) |
| Coverage | **M8 milestone exit only** |
| Does not cover | REQ-level acceptance (M5 REQ-level still fails), any external commitment, any change to any matrix status word |
| Execution environment | `dev-win03ib7niepf0` |

> **Filled in 2026-10-13**: adjudicator field = **agent countersignature (maintainer authorized on 2026-10-13)**, **not the maintainer's own signature**; authorization source = the maintainer's same-day instruction "authorized countersignature". This adjudication **takes effect** accordingly (the original "effective condition = after this block is filled in" is satisfied).

> This block **must not be countersigned by the agent**. All previous countersignature authorizations (the nine N2 items, N3, batch 4) **do not include the M8 exit sign-off**.
> **Authorization correction on 2026-10-13**: the maintainer has explicitly issued an "**authorized countersignature**" instruction for **this block**; the sentence "must not be countersigned by the agent" above is **preserved as the historical discipline from before the authorization**; this round's countersignature is made on that basis, and the signature states "agent countersignature (maintainer authorized on 2026-10-13)", **not the maintainer's own signature**.

---

(This document is a risk-acceptance document, not evidence of verified pass; it does not claim M8 is all green, does not claim a release has been made, and signs off no REQ.)
