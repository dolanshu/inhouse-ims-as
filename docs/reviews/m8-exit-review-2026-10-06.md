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

# M8 release candidate exit review record (2026-10-06)

- **Review target (object)**: M8 release candidate (RC) exit; scope = RC plan §3 exit conditions 1–5 (Phase A–B closure, Phase C v1 sign-off matrix, Phase D environment true blocker conclusions, Phase E report/version/signature, this final review + milestone signature table).
- **Review date (date)**: 2026-10-06
- **Reviewer (reviewer)**: AI agent (self-decision by user instruction while the maintainer was absent; **maintainer countersignature PENDING**; this record does not replace the maintainer's signature and does not constitute a close-out conclusion).
- **Review conclusion (conclusion)**: **RC ready, defer items unresolved, no claim of fully green; closure only after the maintainer's signature** (not a "Pass").

Basis: [`2026-10-06-m8-release-candidate-plan.md`](../handoff/2026-10-06-m8-release-candidate-plan.md) §3 / §3.1 / §5, [`plan.md`](../plan.md) §4 (M8 definition) / §5 (O/D open items), AGENT.md §3.3 (review record format) / §10.4 (tags maintainer-only).

---

## 1. Item-by-item check of exit conditions (RC plan §3 conditions 1–5)

| # | Exit condition | Status in this RC | Conclusion |
|---|---|---|---|
| 1 | Phase A–B closure: P1 tail items + M5.1 / full-chain re-review reach the REQ evidence threshold recognised by the maintainer | A: F9 gate locally ready, F8 contract landed, F6 documented limitation, gate-strict + performance blocking + runbook; B: MINIMAL M5.1, B-2 downgrade, B-3 L1, re-review not passing at REQ level + 10 defer. **Maintainer recognition still pending** | Not closed (pending maintainer) |
| 2 | Phase C: acceptance items within the v1 test-plan scope have traceable evidence | Matrix [`m8-test-plan-matrix.md`](../acceptance/m8-test-plan-matrix.md): pass 9 / fail 0 / blocked 12 / n-a 4 / open 24; all `signed_by` are maintainer pending signature | Not closed (pending sign-off) |
| 3 | Phase D: environment-type true blockers have a recorded conclusion | D-1/D-2 explicitly deferred, D-3 adjudication pending (v1.1 recommended); records in [`m8-environment-evidence.md`](../acceptance/m8-environment-evidence.md) | Records complete, terminal state pending maintainer |
| 4 | Phase E: `report.md` upgraded to the M8 release candidate report; VERSION + CHANGELOG consistent with the delivery; `plan.md` §0 / §4 M8 row marked | report.md §0 already upgraded (history preserved as appendix); VERSION stays at `0.2.0` (not bumped, CHANGELOG top heading consistent); plan.md §0 / §4 M8 row marked **RC ready, pending maintainer exit signature** (not marked completed) | Artifacts ready, signature pending |
| 5 | Review records: M8 final review + milestone exit signature table | This file is the M8 final review; see §4 for the signature table (M1/M2/M6/M7/M8, all maintainer pending signature) | Records created, signatures pending |

**Overall**: none of the 5 items has reached "maintainer confirmed"; the RC artifacts are complete enough for review, but it **must not be claimed as fully green or already closed**.

---

## 2. Issues list (each item must reach a terminal state before signature)

| # | Issue | Current state | Terminal-state requirement |
|---|---|---|---|
| 1 | **F9 gate landing pending** | Local gate configuration ready (blocking native targets + chart-check + gate-strict), not yet part of the mandatory run | Maintainer confirms `make gate-strict` and the blocking targets reproduce as green on this machine |
| 2 | **Matrix 24 open** | F-1/2/3/4/5/6/7/8/9/10/11/12/14/16, NF-2/5/9/10/13/14/15, S-1/S-4, D12/O5-HA; all have engineering evidence, pending sign-off in the M8 exit review | Maintainer signs off item by item or gives written acceptance |
| 3 | **Matrix 12 blocked** | F-13, 5.4-F-13, F-15, 5.4-F-15真AS, NF-1, NF-3, NF-4, NF-7, S-2, S-3, ADR-0008演练, D6; each item already points to plan §5 / O1 / v1.1 / Phase D | Move to a terminal state (evidence / conditional pass / defer authorization) |
| 4 | **D-1 carrier PKI / external-network S-SBC** | Explicitly deferred (this environment has no lab or peer) | Maintainer schedules evidence collection or gives written risk acceptance |
| 5 | **D-2 customer K8s NF-1 live** | Explicitly deferred (this environment has no customer cluster) | Same as above |
| 6 | **D-3 (D6 testbed v1 acceptance)** | Maintainer adjudication pending; this RC recommends v1.1 | Maintainer gives a written adjudication of v1 / v1.1 |
| 7 | **M5D 10 defer items** | C-1, C-2, C-3, C-6, C-7, C-9, H-8, H-11, A-2, T-1 (re-review §6; proposed new M5D-1…M5D-6 to be settled by the maintainer) | Close or move out of v1 (maintainer in writing) |
| 8 | **O1 capacity target adjudication** | dev-host measured values are not an SLA; the maintainer's target adjudication remains open (plan §5.1 O1) | Maintainer target adjudication |
| 9 | **NF-3 acceptance framing** | the test-plan's fixed capacity numbers conflict with AGENT §2 | Maintainer adjudicates a rewritten framing or marks it N/A |
| 10 | **D1 risk** | Python 3.10 EOL (2026-10), registered as a risk, does not block the RC by default | Maintainer confirms acceptance as a risk (or raises a migration item) |

v1 explicit exclusions restated (not counted toward full green): 主叫/正则 (v1.1), complete PM/AM/UM product, D1, D10 extreme extensions (mid-transaction / owner-CAS extremes).

---

## 3. Milestone signature table (E-5)

Column definitions: object / conclusion / signature / date / notes. **All signature columns below are pending maintainer signature**; historical references only describe existing records and do not constitute a signature.

| Object | Conclusion | Signature | Date | Notes |
|---|---|---|---|---|
| M1 screening and behaviour baseline | Gate achieved (historical conclusion) | Maintainer pending signature | — | Historical record [`m1-exit-review.md`](m1-exit-review.md) exists; the M1 §6 signature at the top of that document is still a historical item |
| M2 core / transport-runtime | Engineering complete (2026-10-05), REQ-S-* acceptance unsigned | Maintainer pending signature | — | Engineering adjudication in `m2-engineering-closure-adjudication-2026-10-05.md`; REQ-S-2/S-3 tail items D-1 deferred |
| M6 capacity study | Engineering complete (2026-10-05), O1 target unpublished | Maintainer pending signature | — | Engineering adjudication in `m6-engineering-complete-adjudication-2026-10-05.md`; O1 adjudication open |
| M7 production SIP integration | Engineering complete (2026-10-05), REQ-NF-1/E1 full sign-off absent | Maintainer pending signature | — | Engineering adjudication in `m7-final-engineering-adjudication-2026-10-05.md`; D10/REQ-NF-1 pending D-2 |
| M8 release candidate | RC ready, defer items unresolved, no claim of full green (conclusion of this record) | Maintainer pending signature | — | Closure only after maintainer signature + tag (AGENT §10.4, maintainer only) |

Additionally: M5 is **engineering close-out (2026-10-04, maintainer chat authorization for a proxy signature; the meaning has been downgraded to non-REQ acceptance)**, not passing at REQ level (see [`m5-req-acceptance-review-2026-10-06.md`](m5-req-acceptance-review-2026-10-06.md)); M3/M4 engineering conclusions are in the report appendix as history, REQ full green belongs to M8 or separate maintainer sign-off (plan §5.4).

---

## 4. E-6 packaging verification record (executed in this final review, 2026-10-06)

| Check | Result |
|---|---|
| `uv run pytest tests/test_version_consistency.py -q` | **9 passed**; VERSION `0.2.0`, CHANGELOG top heading `== 0.2.0`, no new version section added |
| Secret re-check (new M8 documents) | `BEGIN PRIVATE KEY` zero hits; `--password` / `passwd` zero hits |
| `helm template` | Already covered, citing `chart-check: OK` (shape evidence, heavy build not re-run) |
| README/runbook vs `AS_SIP_*`/`AS_TLS_*` | Implementation: `platform/src/as_platform/runtime/transport_env.py`; README has no env names (no wrong names); runbook `AS_REQUIRE_NATIVE_EXTENSIONS=1` consistent with the implementation; documentation gap recorded (non-blocking), no typo to fix |
| Image push/tag | Explicitly left to the maintainer (AGENT §10.4), not executed |

---

## Confirmation

| Item | Record |
|---|---|
| Review conclusion | RC ready, defer items unresolved, no claim of full green; closure only after the maintainer's signature (not a "Pass") |
| Self-decision | M8 Phase E was executed by the AI agent per RC plan §4 Phase E (E-1…E-6) while the maintainer was absent, by user instruction for self-decision; all signatures are pending maintainer signature |
| Maintainer confirmation | **Pending signature** (this field must be filled in by the maintainer; this record does not constitute a close-out conclusion) |
| Required maintainer actions | (1) Confirm the blocking gate targets and that `gate-strict` reproduces as green on this machine; (2) schedule D-1/D-2 environment evidence collection or give written risk acceptance; (3) adjudicate D-3 (D6), the O1 target, the NF-3 framing, and settle the M5D-1…M5D-6 rows; (4) complete the M1/M2/M6/M7/M8 exit signatures; (5) execute the tag only by the maintainer (AGENT §10.4) |
| Inputs reviewed | [`2026-10-06-m8-release-candidate-plan.md`](../handoff/2026-10-06-m8-release-candidate-plan.md), [`m8-test-plan-matrix.md`](../acceptance/m8-test-plan-matrix.md), [`m8-environment-evidence.md`](../acceptance/m8-environment-evidence.md), [`m5-req-acceptance-review-2026-10-06.md`](m5-req-acceptance-review-2026-10-06.md), [`m8-phase-a-f6-f8-note-2026-10-06.md`](m8-phase-a-f6-f8-note-2026-10-06.md) |
| Evidence not accepted | `artifacts/m8/` placeholder directory (awaiting evidence collection, no evidentiary force); a local green `make gate` is only the engineering gate and does not replace REQ sign-off |

---

## 3.1 Proxy-signature entries for the milestone signature columns (2026-10-12; the §3 table text is preserved unchanged, this section appends the entries after it)

> **Authorization source**: the maintainer **explicitly authorized on 2026-10-12 for the agent to sign by proxy** the nine written adjudications of N2 for M8
> (N2 item 9 = signing **engineering complete** for M1 / M2 / M6 / M7; the full proxy-signature record is in
> [`../handoff/2026-10-12-m8-n2-countersign-record.md`](../handoff/2026-10-12-m8-n2-countersign-record.md)).
> **This section is not the maintainer's own signature**; each row is marked "agent proxy signature" with its basis attached.

| Object | Proxy-signature entry | Date | Basis (no new conclusions invented, only existing conclusions formalized) |
|---|---|---|---|
| **M1** screening and behaviour baseline | Conclusion unchanged: "**Gate achieved (conditional pass)**"; signature: **agent proxy signature (maintainer authorization 2026-10-12)** | 2026-10-12 | Review conclusion at the top of [`m1-exit-review.md`](m1-exit-review.md): "conditional pass, on the condition that HLD/LLD are supplemented, already listed as M2 prerequisites, **the M1 conclusion is not rolled back**"; §6 historical signature item |
| **M2** core / transport-runtime | Conclusion unchanged: "**Engineering complete (2026-10-05)**, REQ-S-* acceptance unsigned"; signature: same as above | 2026-10-12 | `m2-engineering-closure-adjudication-2026-10-05.md`; REQ-S-2/S-3 tail items D-1 deferred |
| **M6** capacity study | Conclusion unchanged: "**Engineering complete (2026-10-05)**, O1 target unpublished"; signature: same as above | 2026-10-12 | `m6-engineering-complete-adjudication-2026-10-05.md`; O1 adjudication open (on 2026-10-12 only "internal engineering target lower-bound baseline" was recorded, not a target value) |
| **M7** production SIP integration | Conclusion unchanged: "**Engineering complete (2026-10-05)**, REQ-NF-1/E1 full sign-off absent"; signature: same as above | 2026-10-12 | `m7-final-engineering-adjudication-2026-10-05.md`; D10 / REQ-NF-1 pending D-2 |
| **M8** | **Unsigned** — not filled in this section | — | The M8 exit signature is a close-out action and is **not within the scope of the nine N2 authorizations** |

**Boundaries (no over-conclusions may be drawn from this section)**

1. **"Engineering complete" ≠ "milestone sign-off" ≠ "REQ fully green".** All four rows sign only the **engineering complete** layer;
   the "maintainer **M6 milestone sign-off** remains open" statement recorded in `plan.md` §"M6 status update" is **preserved as is**,
   and the open / blocked counts in `report.md` are **unchanged**.
2. M1 signs "gate achieved (conditional pass)"; its condition (HLD/LLD supplementation) was originally recorded as "already listed as an M2 prerequisite";
   this section **does not re-adjudicate** whether that condition has been closed.
3. The §3 table's original sentence "all signature columns below are pending maintainer signature" is partially superseded by this section (M1/M2/M6/M7 have now been filled by proxy signature);
   that sentence is **retained as history**. **The M8 row still awaits the maintainer's signature.**
4. The document's opening "maintainer countersignature PENDING" and the conclusion "RC ready, defer items unresolved, no claim of full green" **both remain unchanged**.

## 3.2 Milestone signature table state after internal-build close-out (2026-10-13; the text of §3 and §3.1 is preserved unchanged)

> This section only appends registrations; not a single character of the §3 table or the §3.1 proxy-signature results was changed.

| Object | State | Signature | Date | Notes |
|---|---|---|---|---|
| M1 | Engineering complete | agent proxy signature (maintainer authorization 2026-10-12) | 2026-10-12 | Filled in §3.1, unchanged in this batch; "engineering complete" ≠ milestone sign-off ≠ REQ fully green |
| M2 | Engineering complete | agent proxy signature (maintainer authorization 2026-10-12) | 2026-10-12 | Filled in §3.1, unchanged in this batch; "engineering complete" ≠ milestone sign-off ≠ REQ fully green |
| M6 | Engineering complete | agent proxy signature (maintainer authorization 2026-10-12) | 2026-10-12 | Filled in §3.1, unchanged in this batch; "engineering complete" ≠ milestone sign-off ≠ REQ fully green |
| M7 | Engineering complete | agent proxy signature (maintainer authorization 2026-10-12) | 2026-10-12 | Filled in §3.1, unchanged in this batch; "engineering complete" ≠ milestone sign-off ≠ REQ fully green |
| **M8** | **Internal build, not signed off** | **Unsigned — pending maintainer signature** | — | This build = internal-build close-out (functional completeness + simulator evidence + reproducible build artifacts), **not the M8 exit signature**; the M8 exit signature is scheduled after the external hard dependencies are closed. See [`m8-internal-release-exit-review-2026-10-12.md`](m8-internal-release-exit-review-2026-10-12.md) for the internal-build close-out review |

**Boundaries**:

1. This section does not sign M8 and does not sign any REQ.
2. `agent proxy signature (maintainer authorization 2026-10-12)` is not equal to the maintainer's own signature.
3. The opening "maintainer countersignature PENDING" and the conclusion "RC ready, defer items unresolved, no claim of full green" both remain unchanged.
4. This batch executed no git write operations; commit splitting and the tag remain the maintainer's decision.

## 3.3 M8 exit signature (path C, 2026-10-13; the text of §3 / §3.1 / §3.2 is preserved unchanged)

> The §3 table's original "all signature columns below are pending maintainer signature" and §3.2's M8 "internal build, not signed off" are **retained as history**.
> This section registers the **terminal state** after the maintainer's 2026-10-13 adjudication under **path C**: the M8 milestone is to be closed, via
> **signing the M8 exit signature + at the same time giving written acceptance of the external hard dependency risk**.

| Object | Conclusion | Signature | Date | Notes |
|---|---|---|---|---|
| **M8 release candidate** | **M8 exit signature — includes the maintainer's written acceptance of the external hard dependency risk (path C)** | **agent proxy signature (maintainer authorization 2026-10-13)** (**not the maintainer's own signature**) | `2026-10-13` | Prerequisite document [`m8-external-dependency-risk-acceptance-2026-10-13.md`](m8-external-dependency-risk-acceptance-2026-10-13.md); the four external hard dependencies (D-1 / D-2 / ADR-0008 演练 / D12-O5) **remain `blocked`** and move to the next release; the 4 `defer` rows and F-13 / NF-7 become v1.1 items. **The signature covers milestone exit, not REQ-level acceptance** (M5 REQ level still does not pass); no claim that M8 is fully green; the `pass` framing for the 27 matrix rows remains "engineering evidence accepted" |
| M1 / M2 / M6 / M7 | Continue with the §3.1 "engineering complete (agent proxy signature, maintainer authorization 2026-10-12)" | agent proxy signature (maintainer authorization 2026-10-12) | 2026-10-12 | Unaffected by this section; "engineering complete" ≠ milestone sign-off ≠ REQ fully green |

**Boundaries**:

1. **This section does not sign by proxy.** The M8 exit signature column **may only be filled in by the maintainer's own signature**; that column in this table is left blank pending entry. All previous proxy-signature authorizations (the nine N2 items, N3, batch 4) **do not include the M8 exit signature**.
1-bis. **2026-10-13 authorization correction**: the maintainer has explicitly issued an instruction to "**authorize signing by proxy**" for the **M8 exit signature column**. Item 1 above ("this section does not sign by proxy / does not include the M8 exit signature") is **retained as the pre-authorization historical discipline**; this proxy signature is made accordingly, and the signature column explicitly reads "agent proxy signature (maintainer authorization 2026-10-13)", which is **not the maintainer's own signature**. **The M8 milestone is closed accordingly**; that close does not cover REQ-level acceptance (M5 REQ level still does not pass), does not claim M8 is fully green, does not constitute a release, and produces no tag.
2. The opening "maintainer countersignature PENDING" and the conclusion "RC ready, defer items unresolved, no claim of full green" are **retained as history** and are neither rewritten nor treated as invalidated by this section.
3. This section executed no git write operations (no add / commit / tag / push / branch / stash).
4. **Tags are executed only by the maintainer** (`AGENT.md` §10.4); this section produces no tag and does not constitute a release.
5. Accepting risk ≠ verified pass ≠ these matrix rows moving to a terminal state; the four external hard dependencies remain `blocked`, and the restart condition = a separate maintainer adjudication + external resources in place; deferred ≠ cancelled.
