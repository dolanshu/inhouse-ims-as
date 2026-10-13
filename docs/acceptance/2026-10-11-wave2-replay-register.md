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

# Wave 2 Replay Differential Case Register (the In-Repo Carrier of A4-3's "Separate Issue")

> **Landed date: 2026-10-11. Status: landed, pending maintainer review.**
>
> **This file is the in-repo carrier of the "separate issue" referred to in the A4-3 adjudication; this project has no external issue tracking, and in-repo documents are the tracking system.**
> 2026-10-11 maintainer adjudication: the "deferred to a separate issue" mentioned in G2 / A4-3 takes the **in-repo registration doc** (i.e., this file) as the carrier,
> and no external issue will be created separately. The adjudication source see §1.
>
> **Current status: the carrier has been created, the cases are not implemented, to be started after the A4 e2e batch's Wave 1 lands.**
>
> **This file does not sign off REQ-F-1**: REQ-F-1's (14-message B2BUA full replay) full-text status is **still open**; this file is only a tracking carrier,
> not an implementation, not acceptance evidence. This file likewise does not sign off REQ-F-2 / REQ-F-4, does not sign off any milestone, and does not constitute external acceptance pass.

---

## 1. Background and Adjudication Source

Wave 2 (14-message per-message replay differential comparison) was explicitly deferred in the e2e wave plan, then recorded by the 2026-10-10 adjudication as
"deferred to a separate issue, not created this iteration"; on 2026-10-11 the maintainer adjudicated this in-repo file as the carrier of that issue.

| Source | Location (line-by-line verified 2026-10-11) | Key points of the original text |
|---|---|---|
| e2e wave plan | [`2026-10-09-e2e-test-plan.md`](2026-10-09-e2e-test-plan.md) "Wave 2 — REQ-F-1 Shape (still no console)" section (`:66-74`) | Wave 2 work definition and completion criteria (see §3 excerpt) |
| Same as above | Same file, Wave 1 section's "**Explicitly not doing (Wave 1): 14-message per-message header differential comparison, console, kind, capacity numbers.**" (`:64`) | The 14-message per-message differential comparison is not part of Wave 1 |
| 2026-10-10 adjudication | [`../handoff/2026-10-10-unfinished-assessment-and-next-plan.md`](../handoff/2026-10-10-unfinished-assessment-and-next-plan.md) §0-A.6 adjudication record table **G2 / A4-3** row (`:56`) | "Wave 2's 14 replay cases are deferred to a separate issue; this iteration only registers them as a gap; this task **does not create an issue**." |
| Decision record transcription | [`../plan.md`](../plan.md) §0 "product decision record" table G2 / A4-3 row (`:39`) | "Wave 2 replay cases deferred to a separate issue; this iteration records them as a gap" |
| Carrier adjudication | Maintainer's 2026-10-11 adjudication (registered in [`../handoff/2026-10-11-open-adjudication-register.md`](../handoff/2026-10-11-open-adjudication-register.md) §2 P5 item, 2026-10-11 closing-round appended paragraph) | Use an in-repo doc in place of an external issue; this file is that carrier |

---

## 2. Case List: 14 Baseline Messages

The baseline artifacts are already in-repo: [`../../testbed/contracts/sip-baseline/S1-basic-call/`](../../testbed/contracts/sip-baseline/S1-basic-call/)
(scenario S1 basic call, sippy baseline, capture date 2026-09-28; sequence description see that directory's `README.md`).
The file names in the table below are transcribed verbatim from that directory (2026-10-11 Glob verified, 14 `.txt` files in total, plus `README.md`), sorted `01 → 14`;
the direction (`in` = inbound leg entering the AS, `out` = outgoing leg sent by the AS), the peer (`trunk` / `core`), and the message type can all be read directly from the file names,
and this table does not fabricate internal details of the message files.

| # | File name (verbatim) | Direction | Peer | Message type | Position in the sequence (per that directory's README) |
|---|---|---|---|---|---|
| 01 | `01-in-invite-trunk.txt` | Inbound leg (trunk→AS) | trunk | INVITE | Call start |
| 02 | `02-out-100-trunk.txt` | Outgoing leg (AS→trunk) | trunk | 100 Trying | Provisional response to the inbound leg's INVITE |
| 03 | `03-out-invite-core.txt` | Outgoing leg (AS→core) | core | INVITE | B2BUA leg flip (new Call-ID) |
| 04 | `04-in-100-core.txt` | Inbound leg (core→AS) | core | 100 Trying | Provisional response to the outgoing leg's INVITE |
| 05 | `05-in-180-core.txt` | Inbound leg (core→AS) | core | 180 Ringing | Called party ringing |
| 06 | `06-out-180-trunk.txt` | Outgoing leg (AS→trunk) | trunk | 180 Ringing | Ringing returned to the caller |
| 07 | `07-in-200-core.txt` | Inbound leg (core→AS) | core | 200 OK | Called party answers |
| 08 | `08-out-ack-core.txt` | Outgoing leg (AS→core) | core | ACK | Confirms the outgoing leg's answer |
| 09 | `09-out-200-trunk.txt` | Outgoing leg (AS→trunk) | trunk | 200 OK | Answer returned to the caller |
| 10 | `10-in-ack-trunk.txt` | Inbound leg (trunk→AS) | trunk | ACK | Call establishment complete |
| 11 | `11-in-bye-core.txt` | Inbound leg (core→AS) | core | BYE | Release initiation (the core side hangs up first) |
| 12 | `12-out-200-core.txt` | Outgoing leg (AS→core) | core | 200 OK | BYE response (core side) |
| 13 | `13-out-bye-trunk.txt` | Outgoing leg (AS→trunk) | trunk | BYE | Release leg flip to the trunk |
| 14 | `14-in-200-trunk.txt` | Inbound leg (trunk→AS) | trunk | 200 OK | Release complete (terminal state) |

Additionally: the same directory's `README.md` is the scenario and sequence description, not counted in the 14 messages.

---

## 3. Differential Work Definition

The work definition comes entirely from [`2026-10-09-e2e-test-plan.md`](2026-10-09-e2e-test-plan.md) Wave 2 section (`:66-74`),
this section only summarizes and references, **without rewriting its conclusions**:

1. **Topology prerequisite**: on the Wave 1 topology, for **one** T1 (translation call established) call, collect the inbound / outgoing legs' key messages
   (method + final response code sequence), and perform a **normalized** comparison against the `S1-basic-call` baseline (`:70`).
2. **Two-leg Call-ID**: assert **C_in ≠ C_out** (REQ-F-2 subset) (`:71`).
3. **SDP byte-for-byte**: the SDP offer is **byte-identical** between the inbound and outgoing legs (REQ-F-4); **if the implementation cost is unacceptable, list a separate follow-up** (`:72`).
4. **Completion criteria (key points of the original text)**: `test-plan.md`'s REQ-F-1 tick may only change to
   "**automated subset covered / full text still open**" and link to the specific case name; **do not tick the full text before the 14 messages have been differentially compared** (`:74`).

The Wave 1 section explicitly states "**Explicitly not doing (Wave 1): 14-message per-message header differential comparison**" (`:64`), i.e., this batch of cases is not within Wave 1's scope.

---

## 4. Related Requirements and Current Status

| Related item | Relationship | Current status wording |
|---|---|---|
| **REQ-F-1** | The 14-message B2BUA full replay is the body of this batch of cases | **Full text still open, not signed off by this file.** The existing wording see [`../product/compliance-matrix.md`](../product/compliance-matrix.md): `:79` "14-message full replay not signed off", `:117` "14-message full text not signed off", `:234` S1 row "Partial (14-message full text not signed off)", `:266` "REQ-F-1's 14-message B2BUA **not** signed off by harness" (verified by search 2026-10-11) |
| **REQ-F-2** | Wave 2's differential assertion C_in ≠ C_out is a subset of REQ-F-2 (two legs with independent Call-IDs) | Covered when the Wave 2 cases are implemented; this file does not change its sign-off status |
| **REQ-F-4** | SDP offer byte-identical between the inbound / outgoing legs | The e2e plan allows listing it as a **separate follow-up** when the cost is unacceptable; this file does not prejudge the choice |
| Baseline artifacts | [`../../testbed/contracts/sip-baseline/S1-basic-call/`](../../testbed/contracts/sip-baseline/S1-basic-call/) 14 message files + README | Already in-repo, traceable (§2 list) |

**Current e2e landing status (verified by search 2026-10-11):**

- `pytest.mark.e2e` has **0 hits** across the repo's `.py` files — even Wave 1 has not yet landed;
  consistent with [`2026-10-09-e2e-test-plan.md`](2026-10-09-e2e-test-plan.md)'s opening "`pytest -m e2e` currently has **0** tests" (`:4`).
- **Start prerequisite**: ① the A4 e2e batch's **Wave 1 lands first** (`testbed/e2e/test_sip_first_edition.py`,
  adjudication see 2026-10-10 handoff §0-A.6 G2 / A4-1 row `:54`); ② run in an environment **with the required native extension**
  (G2 / A4-2: **fail** not skip when native is missing, `:55`).

---

## 5. Non-Goals (this file's boundary)

- **This file does not implement any case**: it does not create new `testbed/e2e/` test files, does not write a differential harness, and does not modify any product / test code.
- **No supplementary packet captures**: the baseline is the existing 14 files in `S1-basic-call` in-repo; no new captures are added, and no real traffic is referenced.
- **No sign-off**: does not sign off REQ-F-1 / REQ-F-2 / REQ-F-4, does not sign off any milestone, and does not constitute external acceptance pass.
- **Does not schedule on the maintainer's behalf**: case implementation belongs to the A4 e2e batch, and the start order is subject to maintainer authorization.
- **Write-back convention at future implementation**: after a new `testbed/e2e/` test file implements the differential comparison, **append** a section to this file registering the result
  (implementation date, case file name, differential scope, whether SDP differential comparison is included or listed as a separate follow-up), and per the e2e plan's completion criteria
  change the REQ-F-1 tick to "automated subset covered / full text still open"; **must not** tick the full text before all 14 messages have been differentially compared.

---

## 6. Implementation Result Write-Back (added 2026-10-12; the original text of §1–§5 is preserved unchanged)

> This section is appended per §5's "write-back convention at future implementation". The start prerequisite has been met:
> ① Wave 1 landed on 2026-10-11; ② this machine already has the required native extension.

| Write-back item | Content |
|---|---|
| **Implementation date** | 2026-10-12 |
| **Case file** | `testbed/e2e/test_s1_replay_contract.py` (3 e2e cases; side by side with Wave 1's `test_sip_first_edition.py`, with no mutual imports) |
| **Differential scope** | **Normalized** sequence differential comparison — per the e2e plan's Wave 2 definition "method + **final** response code sequence", with 1xx provisional responses discarded; each of the inbound and outgoing legs asserts `INVITE → 200 → ACK → BYE → 200`; additionally includes **C_in ≠ C_out** (REQ-F-2 subset) |
| **SDP differential comparison** | **Included, no separate follow-up** — asserts the inbound leg INVITE's body and the outgoing leg INVITE's body are **byte-equal** (REQ-F-4) |
| **REQ-F-1 tick** | Changed per the completion criteria to "**automated subset covered / full text still open**" and linked to the above case name; not a single `- [ ]` in `test-plan.md`'s REQ-F-1 section is **ticked** (the 14-message per-message header differential comparison is still open); see [`../acceptance/test-plan.md`](../acceptance/test-plan.md) "REQ-F-1 automated coverage status (added 2026-10-12)" section |
| **Measured result** | `uv run pytest -m e2e -q` → **8 passed** (Wave 1's 5 + Wave 2's 3); Wave 2 alone passed **3 passed** 4 times consecutively; after temporarily moving away `_resip_runtime*.so`, **8 failed / 0 skipped** (A4-2 holds) |
| **Execution record** | [`../handoff/2026-10-12-o1-and-native-reproducibility.md`](../handoff/2026-10-12-o1-and-native-reproducibility.md) |

**Implementation approach and cost (recorded factually)**: to collect the two-leg message sequences, this case uses `monkeypatch` to wrap **within the test module**
`TransparentBridge._on_message` and `_forward_response`, two **private** methods (the observation points are the bridge hops on both sides of the AS:
`north` sees the inbound leg, `south` sees the outgoing leg). **Not a single byte of the product code and `as_simulators` was changed**, at the cost of this case depending on a private API,
and renaming internals of the bridge will invalidate this file.

**Still open (not closed by this section)**: the 14-message **per-message header differential comparison** — including the 100/180 provisional response sequence, Via branch patterns,
Route consumption, etc. Wave 2's definition itself is the normalized skeleton differential comparison, which does not include per-message headers.
**This section does not sign off REQ-F-1's full text, does not sign off REQ-F-2 / REQ-F-4, and does not sign off any milestone.**
