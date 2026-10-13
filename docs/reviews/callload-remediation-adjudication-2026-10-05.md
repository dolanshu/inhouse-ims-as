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

# callload Review Remediation — Adjudication Record (2026-10-05)

> Input: [`callload-m2-m6-m7-demo-branch-review-2026-10-05.md`](callload-m2-m6-m7-demo-branch-review-2026-10-05.md)  
> Plan: [`../handoff/2026-10-05-callload-review-response-plan.md`](../handoff/2026-10-05-callload-review-response-plan.md)  
> Verification: local `make gate` (964 passed, 2 skipped); native integration requires `make m2-platform-resip-build` + `make m2-platform-resip`.

| ID | Status | Evidence |
|----|------|------|
| F1 | Fixed | `bind_address`/`advertised_address` threaded through C++ + `transport_env.py` |
| F7 | Fixed | `AS_TLS_*` / `AS_PEER_*` + `SipStackService.from_env` |
| F10 | Fixed (content) | Story C talk track + the F10 reconciliation section of `pre-m8-demo-review-plan.md` |
| F9 | Partially fixed | `native_extensions.py` + local `make m2-platform-resip-build`; **the blocking target has not yet become a mandatory gate** |
| F4 | Fixed | `map_outbound_failure_to_inbound_status` + C++ `mapUpstreamFailureStatus` |
| F3 | Fixed (FORWARD path) | `buildUacLegDict` + `sip_stack_service` `uac_leg` |
| F2 | Fixed | recovery BYE Contact + `Route` replay |
| F5 | Fixed | fingerprint map 2048 cap eviction |
| F6 | Partially fixed | connection registration cap + dialog termination deregistration; no native transport close callback |
| F8 | Not closed | C++ still uses cout/cerr predominantly; a JSON callback or macro contract is needed before M8 |
| F11 | Maintainer | not brought into the agent queue |
| F12–F18 | Fixed | see each entry in CHANGELOG 0.2.0 |

**Still does not constitute**: M2/M6/M7 milestone exit, all-green REQ, formal customer NF-1 sign-off.

---

## Merged into master (2026-10-06)

| Item | Status |
|----|------|
| Engineering fixes (table above) | Recorded; F8 open, F6 partial |
| F9 blocking gate | **Not in effect** — the blocking targets (`m2-native-smoke` / `m2-platform-resip`) have not yet been brought into the mandatory gate set |
| Maintainer merge checklist | [`../handoff/2026-10-06-callload-merge-to-master.md`](../handoff/2026-10-06-callload-merge-to-master.md) |
| Merged into master @ SHA | **`139d299`** (2026-10-06; squash) |

---

## Countersign addendum (2026-10-12; one of the "must be synchronized" items of N2 item 3)

> **Authorization source**: on 2026-10-12 the maintainer **explicitly authorized the agent to countersign** the nine written adjudications of M8 N2.
> The "must be synchronized" column of N2 item 3 (F8) points to the **F6 row** of this file; this addendum formalizes the result.
> **This addendum is not a maintainer personal signature**; the master countersign record is at
> [`../handoff/2026-10-12-m8-n2-countersign-record.md`](../handoff/2026-10-12-m8-n2-countersign-record.md).

**Status update to the F6 row of the table above**: changed from "partially fixed" to **"partially fixed + documented limitation accepted"** (supplemented, not replaced).
Signature: **agent countersign (maintainer authorization dated 2026-10-12)**.

**Basis (no newly invented conclusion)**: the original text of N2 item 4 — F6 accepts the documented limitation
(a long-lived connection with no dialog termination relies only on the 2048-entry fingerprint LRU and the 4096 connection cap); the formalization record is at
[`m8-phase-a-f6-f8-note-2026-10-06.md`](m8-phase-a-f6-f8-note-2026-10-06.md) §5.1.

**Boundary**: **the conclusion is not "fixed"** — the native transport-close callback is **still absent**;
this addendum does not change the factual description in the F6 row of the table above, it only adds the signature fact that the risk has been accepted.
