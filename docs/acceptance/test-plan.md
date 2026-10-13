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

# Acceptance Test Plan — 3rdparty-as

**Version**: v0.3 (acceptance criteria + automation boundary)
**Date**: 2026-09-28 (body); **2026-10-09** added the real-stack / e2e boundary
**Status**: most REQ checkboxes are still open. See the automation-layering section below; **the end-to-end (e2e) suite has not landed**, plan in [`2026-10-09-e2e-test-plan.md`](2026-10-09-e2e-test-plan.md). **2026-10-12 correction (e2e position)**: e2e is no longer zero cases — see automation-layering table ③ and the 2026-10-12 addendum in the REQ-F-1 section below; the previous sentence is retained unchanged.
**B6 review status**: this document has a review record from the B6 review — [`../reviews/product-packaging-review-checklist-2026-10-12.md`](../reviews/product-packaging-review-checklist-2026-10-12.md) §6 (first review 2026-10-12) and §7 (closed-loop re-review 2026-10-12); **the conclusion awaits maintainer confirmation** and until then must not be used as a basis for external delivery or acceptance (`AGENT.md` §3.3).

**M4b-8 BLOCKED matrix (2026-10-03)**: the maintainer ruling is in [`reviews/m4-req-calling-regex-lossless-adjudication-2026-10-03.md`](../reviews/m4-req-calling-regex-lossless-adjudication-2026-10-03.md). After **M4 engineering closed** (2026-10-04), the items below are **supplementary testing / deferred**, and do not block §4.3: see [`plan.md`](../plan.md) **§5.4** (F-13, F-15 real AS, caller/regex in v1.1, REQ all green). Evidence already collected on dev HTTPS: **callee + prefix** CRUD → approval, fleet, distribution start, etc. ([`m4b-8-runbook.md`](m4b-8-runbook.md)). **Step 3 (F-13)**: BLOCKED → **§5.4**. **7.2d**: **M5**.

> This document is extracted from the acceptance-criteria part of PRD v0.2 (prd.md).
> The concrete test cases (steps, assertions, data preparation) are to be added during the M2 design phase.
> **Note on protocol section numbers**: as in the PRD, the RFC 3261 section numbers here follow the original RFC 3261 as published by the IETF in 2002.

## Automation layering (2026-10-09)

| Layer | pytest marker | Current state |
|----|-------------|------|
| ① | `unit or contract` | `make gate`. The vast majority do not go through `_resip_runtime`. E1 runs the real stack when the `.so` exists; **S1/S4** use the `accept_all_invites` harness (bypassing `decide()`); **S2/S3** go through `decide()`. |
| ② | `integration` | The real-stack subset: TCP/TLS, two-leg FORWARD, SDP, `test_product_path` (simulated chain + `demo_rules`, **no** accept-all). Gate layer ② running all of `integration` **does not build** the native; the native path is covered separately by `make m2-platform-resip-build` + `AS_REQUIRE_NATIVE_EXTENSIONS=1 make gate`. |
| ③ | `e2e` | **8 stable passes** (Wave 1's five cases in `testbed/e2e/test_sip_first_edition.py` + Wave 2's three cases in `testbed/e2e/test_s1_replay_contract.py`; **fails rather than skips** when the native extension is missing). REQ-F-1 = **automated subset covered / full text still open**; see the 2026-10-12 addendum in the REQ-F-1 section below. |
| Capacity | `performance` / `as_load` | The peer of the M6 product-runtime load test is `load_uas_runtime.py` (an **accept-all harness**), not the business decision path. |

`accept_all_invites` is **not** ims-sim and is **not** the production path: on the real stack it is fixed at 100/180/200 and is used for stack / SDP probes. The 14 B2BUA messages of REQ-F-1 are **not** signed off by the harness.

---

## §1.1 Core call signalling path (REQ-F-1 to REQ-F-5)

### REQ-F-1 acceptance criteria

**Real-stack automation boundary (2026-10-09)**: the `accept_all_invites` harness covers the inbound visible prefixes **100 → 180 → 200 (with SDP)** on the product `_resip_runtime` (`test_e1_contract_resip_runtime.py`, `test_e1_contract_resip_runtime_full.py`). This is not the 14-message full text below. The outbound INVITE, the independent Call-ID, byte-identical SDP pass-through, Route consumption, and ACK/BYE remain in integration (`test_m7_forward_two_leg_integration.py`, `test_req_f4_sdp_identity_integration.py`, `test_resip_two_leg_integration.py`) and are **not** merged into `make gate`. Full real-stack replay of S5–S11 is likewise deferred. The path across a simulated S-SBC **without** accept-all is in `test_product_path.py` (`integration`). **The pytest `e2e` marker is still empty**; the completion plan is in [`2026-10-09-e2e-test-plan.md`](2026-10-09-e2e-test-plan.md). This does not count as sign-off of the full text of REQ-F-1.

> **Scheduling and coverage status update (added 2026-10-12; the text above is retained unchanged)**: ① **The e2e marker is no longer empty** — Wave 1 (5 cases) and Wave 2 (3 normalised skeleton comparison cases, including C_in ≠ C_out and byte-identical SDP) have landed; REQ-F-1's status is "automated subset covered / full text still open", and the 14-message per-header comparison is still not implemented (carrier [`2026-10-11-wave2-replay-register.md`](2026-10-11-wave2-replay-register.md)). ② **The S5–S11 schedule is finalised** (priority P1 S5 → P6 S11; S8 is registered as blocked because the baseline lacks Route / Record-Route headers, so it is not scheduled until those are collected), see [`../handoff/2026-10-09-sip-native-testing-plan.md`](../handoff/2026-10-09-sip-native-testing-plan.md) §4-D. **No REQ has been signed off.**

- [ ] Start the simulated S-SBC and the simulated peer (Return UAS)
- [ ] Send INVITE from the simulated S-CSCF (the target number hits a business rule)
- [ ] Assert in order that 14 messages are received: INVITE(upstream) → 100 Trying(downstream) → 100 Trying(upstream) → 180 Ringing(upstream) → 180 Ringing(downstream) → 200 OK(upstream) → 200 OK(downstream) → ACK(downstream) → ACK(upstream) → BYE(upstream) → 200 OK(downstream) → BYE(downstream) → 200 OK(upstream) → the 200 OK confirmation after BYE
- [ ] The message methods and response codes are strictly equal to the 14 in the POC baseline `testbed/contracts/sip-baseline/S1-basic-call/`
- [ ] The Via branch parameter matches the z9hG4bK pattern (reSIProcate produces different hex values; matching the pattern counts as a pass)
- [ ] Do not check the SDP `o=` timestamp, do not check header field ordering

> **REQ-F-1 automation coverage status (added 2026-10-12; all `- [ ]` checkboxes above are retained unchanged)**
>
> Per the completion criteria of Wave 2 in [`2026-10-09-e2e-test-plan.md`](2026-10-09-e2e-test-plan.md)
> ("the REQ-F-1 checkbox may only be changed to '**automated subset covered / full text still open**' and linked to concrete case names; **the full text must not be checked off while the 14 messages are not compared**"),
> the current status is:
>
> **Status = "automated subset covered / full text still open".**
>
> | Subset already covered by automation | Case |
> |---|---|
> | The **normalised** message sequence of both legs matches the `S1-basic-call` baseline skeleton (each leg is `INVITE → 200 → ACK → BYE → 200`, with 1xx provisional responses dropped under the "final response code sequence" definition) | `testbed/e2e/test_s1_replay_contract.py::test_e2e_s1_replay_both_legs_match_the_normalised_baseline` |
> | **C_in ≠ C_out** (independent Call-IDs for the two legs, a REQ-F-2 subset) | `testbed/e2e/test_s1_replay_contract.py::test_e2e_s1_replay_second_leg_starts_a_new_call_id` |
> | **The SDP offer is byte-identical across the inbound and outbound legs** (REQ-F-4) | `testbed/e2e/test_s1_replay_contract.py::test_e2e_s1_replay_sdp_offer_is_byte_identical_across_legs` |
>
> **Still open, so none of the checkboxes above has been touched**: the **per-message header comparison** of the 14 messages (including the 100/180 provisional response sequence, the Via branch pattern, Route consumption, etc.). Wave 2's definition is itself a **normalised** comparison of "method + **final** response code sequence" and does not include per-message headers; that subset is still tracked by [`../acceptance/2026-10-11-wave2-replay-register.md`](2026-10-11-wave2-replay-register.md).
>
> How to run: `uv run pytest -m e2e -q` (run `make m2-platform-resip-build` first; when the native is missing it **fails rather than skips**, A4-2).
> Execution record: [`../handoff/2026-10-12-o1-and-native-reproducibility.md`](../handoff/2026-10-12-o1-and-native-reproducibility.md).
> **This addendum does not sign off the full text of REQ-F-1.**

### REQ-F-2 acceptance criteria
- [ ] Complete the basic call of REQ-F-1
- [ ] Extract the Call-ID of the inbound (upstream) INVITE (recorded as C_in)
- [ ] Extract the Call-ID of the outbound (downstream) INVITE (recorded as C_out)
- [ ] Assert **C_in ≠ C_out** (the two legs are independent dialogs; RFC 3261 §12 B2BUA maintains independent dialog state on each side)
- [ ] Extract the Call-IDs of the inbound 200 OK / ACK / BYE and assert that **they all equal C_in** (within the same dialog the Call-ID must be identical, RFC 3261 §8.1.1.4)
- [ ] Extract the Call-IDs of the outbound 200 OK / ACK / BYE and assert that **they all equal C_out**

### REQ-F-3 acceptance criteria
- [ ] Complete the basic call of REQ-F-1
- [ ] Extract the Request-URI of the upstream INVITE
- [ ] Extract the Request-URI of the downstream INVITE
- [ ] Assert that the host/port parts differ (the routing address changes)
- [ ] Assert the user part: in a **non-translation scenario** it stays unchanged; in a **translation scenario** it changes according to the translation rule — baseline S1 is a translation scenario (`+8613800138000` → `013800138000`), so "the user part must be byte-identical" must not be used as the acceptance criterion for the translation business case

> Note: this assertion has actually been executed by the derived baseline test `testbed/simulators/tests/test_derived_baseline.py` over the 14 messages of `S1-basic-call`; after normalisation both sides point at the same callee (`13800138000`).

### REQ-F-4 acceptance criteria
- [ ] Complete the basic call of REQ-F-1
- [ ] Extract the SDP body (bytes) of the upstream INVITE
- [ ] Extract the SDP body (bytes) of the downstream INVITE
- [ ] Assert that the two are byte-identical
- [ ] Extract the SDP body of the upstream 200 OK and the SDP body of the downstream 200 OK, and likewise assert they are byte-identical

### REQ-F-5 acceptance criteria
- [ ] Complete the basic call of REQ-F-1, where the upstream INVITE carries one Route header (for example `Route: <sip:proxy.example.com:5060>`)
- [ ] Assert that we consumed the Route header addressed to us (the downstream INVITE no longer retains that Route value)
- [ ] Assert that the destination address of the downstream request is **the peer selected by our routing policy** (not the proxy that the operator-side Route points at)
- [ ] Construct a 200 OK returned by the downstream peer carrying Record-Route
- [ ] Assert that Record-Route is present in the upstream 200 OK and that its value matches the downstream Record-Route (RFC 3261 §12.1.2 Route Set reverse derivation)

---

## §1.2 Routing and policy decisions (REQ-F-6 to REQ-F-7)

### REQ-F-6 acceptance criteria
- [ ] Start the simulated environment, with the rule table containing only +86138* (not +86199*)
- [ ] Send INVITE to +861990000000 from the simulated S-CSCF
- [ ] Assert that we return 404 Not Found (RFC 3261 §21.4.5)
- [ ] Assert that no B2BUA dialog is created (i.e. no downstream INVITE is sent)
- [ ] Compare against the 4 messages of the POC baseline `testbed/contracts/sip-baseline/S2-no-match-404/`
- [ ] Assert that the match target is the target number (the callee direction)
- [ ] Assert longest-prefix-first matching

### REQ-F-7 acceptance criteria
- [ ] Start the simulated environment, with the rule table containing +86168* → R-BLOCK-90 (block policy)
- [ ] Send INVITE to +861681000000 from the simulated S-CSCF
- [ ] Assert that we return 603 Decline (RFC 3261 §21.6.2)
- [ ] Assert that no B2BUA dialog is created
- [ ] Compare against the 4 messages of the POC baseline `testbed/contracts/sip-baseline/S3-policy-reject-603/`
- [ ] Construct a priority conflict scenario that matches both "block" and "translation", and assert that the priority logic is correct (**block rule > translation rule > default routing**)
- [ ] Assert that the match target is the target number; longest prefix first

---

## §1.3 Call lifecycle (REQ-F-8 to REQ-F-11)

### REQ-F-8 acceptance criteria (two branches)

#### Scenario ①: CANCEL is sent **before** 180 Ringing (no early dialog)
- [ ] Start the simulated environment, with the downstream Return UAS not immediately returning 180 Ringing (or returning late enough that the upstream can send CANCEL first)
- [ ] Send INVITE from the simulated S-CSCF (hits a business rule)
- [ ] Before 180 Ringing and before any response from the peer arrives, send CANCEL from the simulated S-CSCF
- [ ] Assert that after receiving CANCEL we immediately return 200 OK (the acknowledgement of CANCEL)
- [ ] Assert that we send CANCEL downstream (not BYE — the outbound leg has no final response yet)
- [ ] Assert that downstream returns 487 Request Terminated (the INVITE transaction is terminated by CANCEL, RFC 3261 §9.2)
- [ ] Assert that we pass the 487 through to upstream
- [ ] Assert that we send ACK upstream
- [ ] Compare against the message sequence of the POC baseline `testbed/contracts/sip-baseline/S4-caller-cancel/`

#### Scenario ②: CANCEL is sent **after** 180 Ringing and **before** 200 OK (early dialog present)
- [ ] Start the simulated environment, with the downstream Return UAS returning 180 Ringing but delaying the 200 OK
- [ ] Send INVITE from the simulated S-CSCF (hits a business rule)
- [ ] After 180 Ringing and before 200 OK, send CANCEL from the simulated S-CSCF
- [ ] Assert that we return 200 OK to the CANCEL
- [ ] Assert that we send CANCEL downstream (against the INVITE transaction that has not yet produced a final response)
- [ ] Assert that the peer (Return UAS) returns 487 to the INVITE
- [ ] Assert that we pass the 487 through to upstream
- [ ] Assert that we send ACK upstream

#### Scenario ③: CANCEL is sent **after** 200 OK (dialog already established)
- [ ] Start the simulated environment, with the downstream Return UAS returning 200 OK normally
- [ ] Complete the basic call (REQ-F-1); once the dialog is established (200 OK + ACK completed)
- [ ] Upstream sends CANCEL
- [ ] Assert that CANCEL has no effect on an established dialog (RFC 3261 §9)
- [ ] Assert that we tear the dialog down with BYE: send BYE downstream → peer returns 200 OK → pass BYE through upstream until the dialog cleanup completes

### REQ-F-9 acceptance criteria
- [ ] Start the simulated environment
- [ ] Complete one basic call (REQ-F-1) and establish a dialog
- [ ] After the dialog is established, send a re-INVITE from the simulated S-CSCF (carrying the correct Route header + the correct Call-ID + matching local/remote tags)
- [ ] Assert that we route the re-INVITE to the correct downstream peer (not creating a new dialog, not dropping it into a black hole)
- [ ] Test in-dialog routing of UPDATE and BYE the same way
- [ ] In the M2 phase, write the complete in-dialog comparison scenarios under `testbed/simulators/`

### REQ-F-10 acceptance criteria
- [ ] Start the simulated environment, with the downstream peer configured to return 486 Busy Here
- [ ] Send INVITE from the simulated S-CSCF
- [ ] Assert that after we send INVITE downstream we receive 486
- [ ] Assert that we forward 486 upstream (not rewriting it to 404 or 200 OK)
- [ ] Test the scenarios where downstream returns 480 and 408 the same way
- [ ] Verify that the dialog state is cleaned up correctly after a non-2xx is received

### REQ-F-11 acceptance criteria (two branches)

#### Scenario ①: CANCEL arrives before the final response (the RFC-legal path)
- [ ] Start the simulated environment, and use controllable delay or mock injection so that CANCEL arrives before the peer's final response
- [ ] Send INVITE from the simulated S-CSCF
- [ ] Inject CANCEL into the inbound leg (before the outbound leg's final response returns)
- [ ] Assert that the outbound leg's downstream returns 487 to the INVITE
- [ ] Assert that we pass the 487 through upstream and send ACK
- [ ] The dialog state ends as Terminated, with no dangling dialog

#### Scenario ②: The final response has already arrived (CANCEL has no effect on the outbound leg)
- [ ] Start the simulated environment, with the downstream Return UAS normally returning a 200 OK or a non-2xx final response
- [ ] Only after we have received the downstream final response does upstream send CANCEL
- [ ] Assert that CANCEL has no effect on the outbound leg (RFC 3261 §9)
- [ ] Assert that we tear the dialog down with BYE (if 200 OK) or clean up directly (if non-2xx)
- [ ] The dialog state ends as Terminated

---

## §1.4 Console and configuration management (REQ-F-12 to REQ-F-15)

### REQ-F-12 acceptance criteria
- [ ] The console UI exists: rule list, create, edit, delete buttons
- [ ] When creating a rule you can fill in: match target (**M4: callee**; caller is v1.1), match mode (**M4: prefix**; regex is v1.1), target business type (translation / anti-fraud / routing / block / default), and an enable/disable switch
- [ ] **M4**: after activation the rule is consistent with the callee prefix and target type/detail filled in on the console (consistent with the callee matching axis of REQ-F-6/F-7; see the M4 scope note in PRD REQ-F-12)
- [ ] After a rule is saved it enters the approval queue (linked with REQ-F-14)
- [ ] After approval the rule takes effect; disabled rules do not participate in matching
- [ ] Rule CRUD operations generate audit logs (REQ-S-4)

### REQ-F-13 acceptance criteria
- [ ] The console provides a Call-ID query entry point
- [ ] The query results display the complete SIP message trace: each message includes direction (inbound/outbound), timestamp, method, response code, Call-ID, From/To
- [ ] The trace query results show translation rule hit information (linked with REQ-F-16)
- [ ] The business side (Actor 4) can also query the same trace through the interface

### REQ-F-14 acceptance criteria
- [ ] After a rule create/update/delete is submitted, the status becomes "pending approval"
- [ ] The approver can see the pending items in the approval queue
- [ ] After approval the rule takes effect and the status becomes "in effect"
- [ ] A rejection must supply a rejection reason; the rule status becomes "rejected"
- [ ] The whole flow has audit logs (REQ-S-4)

### REQ-F-15 acceptance criteria
- [ ] Canary distribution can notify AS instances in batches (N instances per batch) to load the new rule version
- [ ] After each batch there is a health check (instance active_calls normal, no process restart)
- [ ] If a batch fails to distribute, it automatically rolls back to the previous version
- [ ] Operations can manually trigger a rollback
- [ ] The whole flow has audit logs

### M4b-8 browser acceptance procedure (subordinate to the REQs above; executed once the dependencies are ready)

This procedure is the execution steps for REQ-F-12/13/14/15 and REQ-S-4; it neither adds nor replaces their acceptance criteria. Before starting you must have: a same-origin HTTPS console/API serving; PostgreSQL, audit and auth configured; two different accounts with clearly separated permissions, operator and approver; a known Call-ID with expected SIP events; and test AS instances that can be operated on safely. What is currently missing is the configured HTTPS serving/proxy, lossless runtime rule mapping, the live trace source/API, the AS instance inventory, the notification transport and the health source; steps blocked by these backends are marked **BLOCKED** and must not be recorded as passed.

**M4 browser HTTPS (2026-10-03 closure ruling)**: M4/M4b-8 may be executed on same-origin HTTPS provided by **compose, a self-signed certificate or a local reverse proxy**, and redacted evidence may be collected; this does not replace the formal production/cluster preflight of 7.2d below. Formal **7.2d** ingress/trusted-proxy proof belongs to **M5** acceptance; see [`reviews/m4-closure-adjudication-2026-10-03.md`](../reviews/m4-closure-adjudication-2026-10-03.md) and `plan.md` §4.2.

**M4b-7.2d ingress/TLS preflight (BLOCKED)**: before starting any login/browser operation flow, complete and record the following checks against the real customer/test deployment:

- Keep the default ingress-nginx annotation prefix `nginx.ingress.kubernetes.io`; confirm that no custom prefix has invalidated the chart annotations.
- Inspect the external ingress-nginx controller configuration and confirm that `no-tls-redirect-locations` does not contain `/`, so it does not exempt the console/API routes from the HTTPS redirect.
- Confirm that the Ingress uses the customer TLS Secret configured for the actual hostname.
- Request HTTP `/` and `/internal/v1` from an external client and confirm the requests are redirected to HTTPS or rejected; in a real browser check the network/request evidence to confirm credentials were never submitted over HTTP.
- Verify that the forwarded scheme is trusted only when the request origin belongs to the explicitly configured ingress proxy IPs/CIDRs.

The redirect annotations fixed in the chart apply only to the chart's Ingress objects and cannot configure or prove the behaviour of an external controller. Until all the above real controller/deployment/browser evidence is available, this preflight and 7.2d remain **BLOCKED**; template rendering or route mocks cannot substitute.

1. Log into the browser as the operator, and create, edit, disable and delete a test rule item by item; submit each change as an approval request. After refreshing, confirm the live status matches the approval queue and that the page has no fixture fallback.
2. Handle the requests as a different approver: approve at least one valid change, reject at least one with a reason; verify that a rejection without a reason is rejected, that the creator/submitter cannot approve or reject their own order (try each and confirm the status did not change), and that another approver's approve/reject succeeds. Check the rule and request status after approval/rejection.
3. Query the live trace by the known Call-ID, and check the direction, timestamp, method, response code, Call-ID and From/To of every expected message, along with the applicable rule hit information.
4. Execute batched distribution against the test instances; verify per-batch instance notification, the loaded version, and the active_calls/process health results. Inject a health failure in one batch and verify the automatic rollback to the previous version; then perform and verify one manual rollback.
5. Per §3, verify the audit actor, time, action, resource, outcome and applicable before/after snapshots for every permitted, rejected and failed operation; confirm that password, verifier, session/CSRF token, cookie/request headers are redacted. Check the append-only triggers/constraints and runtime DB grants, and actually verify that explicit id INSERT, UPDATE, DELETE and TRUNCATE are all rejected; trigger failure paths such as audit unavailable/authorization/stale-revision, and confirm fail-closed behaviour and the corresponding audit records.

Record the result of each step along with the environment/version; save the redacted browser screenshots, HTTP requests/responses, console/network error logs, trace query results, distribution/health/rollback reports, the corresponding audit snapshots, plus the output verifying the database grants and the rejected writes. Passwords, tokens, cookies and other secrets must not be saved. When any real backend is missing, mark that step **BLOCKED: missing backend**; route mocks, fixtures or static page results must not be substituted for REQ acceptance.

---

## §1.5 Business decision chain (REQ-F-16)

### REQ-F-16 acceptance criteria
- [ ] Start the simulated environment and configure the translation rule +86755* → +852755*
- [ ] Send INVITE to +867551234567 from the simulated S-CSCF
- [ ] Assert that we extract the callee number +867551234567 and translate it per the rule to +8527551234567
- [ ] Assert that the Request-URI of the downstream INVITE is sip:+8527551234567@<routing target>
- [ ] Assert that the REQ-F-13 trace query shows: the pre-translation number, the post-translation number, the matched rule ID and version number, and the routing target

---

## §2 Non-functional requirements (REQ-NF-*)

### REQ-NF-1 acceptance criteria
- [ ] Start the simulated environment
- [ ] Place a basic call (REQ-F-1) and wait for the dialog to be established (the ACK exchange completes)
- [ ] Mid-call (while the dialog is in the active state), forcibly kill the process carrying that call
- [ ] After the process is brought back up by K8s it restarts automatically
- [ ] Send BYE from upstream (S-CSCF/S-SBC)
- [ ] Assert that the new process **after the restart can still route the BYE correctly to the peer** (showing that the dialog state was not lost)
- [ ] Dialog state verification: the dialog record for that Call-ID exists completely in Redis

### REQ-NF-2 acceptance criteria
- [ ] Directory structure: `apps/translation/` and `apps/anti-fraud/` are each independent (not two use cases running in one process)
- [ ] K8s Deployment: one Deployment per use case, with replica counts configured independently
- [ ] Kill the Pod carrying the translation use case and assert that the anti-fraud use case is unaffected (the anti-fraud Pod does not restart, load does not drop)

### REQ-NF-3 acceptance criteria
- [ ] Configure HPA: the translation Deployment scales on active_calls (threshold 500)
- [ ] Inject 1000 concurrent basic calls
- [ ] Assert that the translation Deployment's replica count scales from 3 to ≥ 5
- [ ] Stop injecting, wait 30 seconds, and assert that the replica count scales back below the threshold
- [ ] During scaling, already-established calls are not lost (verified together with REQ-NF-1)

### REQ-NF-4 acceptance criteria
- [ ] Start a rolling upgrade
- [ ] Inject basic calls during the upgrade
- [ ] New calls are routed to the new-version replicas (old-version replicas have been drained)
- [ ] Existing calls on old-version replicas complete normally (BYE → 200 OK)
- [ ] After active_calls on an old-version replica reaches zero, the Pod is deleted by K8s
- [ ] No calls are lost throughout the upgrade

### REQ-NF-5 acceptance criteria
- [ ] There is an S-SBC simulator in the testbed: it receives messages from the simulated S-CSCF and forwards them to our AS; it receives responses from our AS and sends them back to the simulated S-CSCF
- [ ] There is no "is_intranet" / "is_extranet" / "network_mode" style branch check anywhere in the AS code
- [ ] Swap in an S-SBC simulator with a different implementation (for example Kamailio) and assert that the AS-side behaviour is identical

### REQ-NF-6 acceptance criteria
- [ ] grep the production code: no RTP / G.711 / G.729 / DTMF / transcoding related implementation
- [ ] The seam files exist (interface definitions), and the production implementations are stubs / raise NotImplementedError / empty functions
- [ ] The seam comments state the "trigger conditions" and "under what circumstances an implementation is needed"

### REQ-NF-7 acceptance criteria
- [ ] The console can query the complete SIP message trace by Call-ID (all messages from INVITE to BYE, with inbound/outbound direction, timestamp, method, response code)
- [ ] The trace retention period is undecided — it suffices to verify that the cleanup job runs correctly; the concrete number of days is frozen at M4
- [ ] Cleanup job: PG runs it on a schedule and deletes expired trace rows; manually triggering the cleanup command executes it immediately
- [ ] grep the production code: no CDR / wholesale pricing / billing related implementation

### REQ-NF-8 acceptance criteria
- [ ] grep the production code: no lawful_intercept / IRI / intercept related implementation
- [ ] The architecture document §9.2 states explicitly that "LI is done inside the S-CSCF/SBC network and is not within our delivery boundary"

### REQ-NF-9 acceptance criteria
- [ ] The Helm chart can independently deploy one complete system into a specified namespace
- [ ] There is no sharing between namespaces (an independent Redis, an independent PG, an independent AS Pod group)
- [ ] A failure in one namespace (Redis dying, the AS process crashing) does not affect the other namespace

### REQ-NF-10 acceptance criteria
- [ ] The console can submit rule drafts, raise change records and trigger approval
- [ ] After approval, config-service writes a new (immutable) version into PG
- [ ] Canary distribution: notify AS instances in batches to load the new version, with a health check per batch
- [ ] On a distribution failure it automatically rolls back to the previous version
- [ ] The whole flow has audit logs written to PG
- [ ] grep the code: no git / github / gitlab related configuration loading logic

### REQ-NF-11 acceptance criteria
- [ ] A single `./VERSION` file exists at the repository root
- [ ] `grep -r "VERSION=" platform/ apps/ services/` returns nothing (no component owns a VERSION file)
- [ ] `tests/test_version_consistency.py` passes
- [ ] After modifying the root VERSION, the product version reported by all components changes in sync

### REQ-NF-12 acceptance criteria
- [ ] `pyproject.toml` contains the `[tool.uv.workspace]` configuration
- [ ] Running `uv sync` pulls all dependencies into alignment in one go
- [ ] After `git clone` of this repository, `make dev` starts the services directly with no extra `git clone` of other repositories

### REQ-NF-13 acceptance criteria
- [ ] After starting an AS instance, the active_calls, cps, rule match rate, 4xx rate and 5xx rate metrics can be collected on the Prometheus/Grafana side
- [ ] Every call has a complete trace span chain: inbound INVITE → business decision → outbound INVITE → BYE
- [ ] Each JSON log line contains trace_id, and can be correlated with metrics/traces
- [ ] The structured JSON log fields include: timestamp, level, trace_id, call_id, direction, method

### REQ-NF-14 acceptance criteria
- [ ] The Prometheus Alertmanager has preset alert rules:
  - active_calls spike > 30% (5-minute window)
  - 5xx rate > 1% (5-minute window)
  - process restart loop (> 3 times within 1min)
  - certificate expiring within 30 days
- [ ] Manually trigger any of the above conditions and assert that Alertmanager fires the alert correctly (the notification channel is undecided, frozen at M2)

### REQ-NF-15 acceptance criteria
- [ ] The PRD and [`req-nf-15-testbed-performance.md`](../requirements/req-nf-15-testbed-performance.md) exist, and ADR-0014's `responds to REQ` points at REQ-NF-15 (D8 traceability)
- [ ] The `testbed/load/` harness drives the system under test over real UDP sockets (the `as_load` integration test passes at gate layer `integration`)
- [ ] The capacity study evidence includes `summary.json` (with `c6_windows` 1s/100s) and a `resources.json` snapshot from the target side; it is forbidden to pass off the driver callback as a capacity measurement (ADR-0014)
- [ ] The M6 O1 internal measurement report records the formal dev-host batch and its limitations; the report figures are **not** to be used as an SLA or as externally marketed capacity
- [ ] Production-cluster multi-replica saturation point, HPA thresholds and the `performance` marker blocking the gate — stay open until **M8** or a separate maintainer ruling

---

## §3 Security requirements (REQ-S-*)

### REQ-S-1 acceptance criteria
- [ ] An allowlist configuration exists in config-service (IP:port or certificate fingerprint)
- [ ] From a peer outside the allowlist, send SIP messages to us and assert that the messages are dropped or that 403 is returned
- [ ] From a peer inside the allowlist, send messages and assert they are processed normally
- [ ] Allowlist changes must go through the approval flow (REQ-F-14)

### REQ-S-2 acceptance criteria
- [ ] All SIP signalling between AS and S-SBC goes over TLS (port 5061 or another encrypted port)
- [ ] Plaintext connections (TCP port 5060) are rejected (the handshake fails or the connection is closed)
- [ ] The TLS certificate chain is issued by the operator PKI and verification passes

### REQ-S-3 acceptance criteria
- [ ] During certificate rotation (the window where the old and new certificates coexist), calls in progress are unaffected
- [ ] New TLS connections during rotation use the new certificate
- [ ] After the old certificate expires, peer connections still holding the old certificate are correctly rejected (or the switchover was completed within the window)
- [ ] There is no process restart during rotation

### REQ-S-4 acceptance criteria
- [ ] Every console operation must verify the operator's authorisation; this explicitly includes write operations such as rule CRUD, approval and rollback
- [ ] Authorisation method: RBAC roles plus a password or client certificate
- [ ] All operations generate audit logs containing: the operator, timestamp, operation type, resource; changes must record the before and after values, and read or rejected attempts should record an empty snapshot where applicable; passwords, password verifiers, session/CSRF tokens and cookies/request headers must be redacted
- [ ] Audit logs are tamper-proof: the runtime API database role has SELECT on the audit table and column-level INSERT limited to non-id fields (actor, action, resource, outcome, occurred_at, before_json, after_json); it has no permission for table-level INSERT or for INSERT into the id column, with id assigned by a sequence; it has no UPDATE, DELETE or TRUNCATE permission. Tests verify the effective permissions and prove that explicit id INSERT and the above modification/truncate operations are rejected, and that append-only triggers/constraints prevent modification and truncation (the migration/owner role is handled separately)

---

## §4 Governance requirements (REQ-G-*)

### REQ-G-1 acceptance criteria
- [ ] The HLD section of each feature contains an "Enablement" subsection stating the default state, the canary strategy and the removal condition
- [ ] Both the on and off states of the feature switch have test coverage
- [ ] There is no case in the code where "the switch exists but no removal condition was written" (an AST scan guard)

### REQ-G-2 acceptance criteria
- [ ] The PR checklist includes "REQ-* / ADR / design document / contract cases / acceptance record updated"
- [ ] A review record can be traced back to at least one REQ-* number
- [ ] A code change can be traced back to a requirement (via an ADR or a direct reference)

### REQ-G-3 acceptance criteria
- [ ] The four steps of `make gate` (format/check/mypy/pytest) do not include the AST scan (the AST scan is triggered separately by `make gate-strict`)
- [ ] Deliberately write one line of architectural code without an annotation and assert that the AST scan blocks it (via `make gate-strict`)
- [ ] Scan coverage: all non-trivial architectural code has an ADR annotation

### REQ-G-4 acceptance criteria
- [ ] `make gate` exits with code 0
- [ ] When layer ① of `make test` fails, the subsequent layers are blocked
- [ ] The pre-commit hook runs the lint/format part of `make gate` before a local commit

---

## §5 M2 kernel acceptance (unit / contract layer)

> This section is the acceptance criteria for the M2 kernel (platform), corresponding to `docs/architecture/lld.md`.
> Layers and markers: `unit` = pure logic, no sockets; `contract` = language-agnostic contract cases, replayed for **every** implementation.
> Decision logic (`decide()`, rule matching) is **TDD-mandatory** per AGENT.md §6: red - green - refactor.

### 5.1 `decide()` decision matrix (marker: unit)

Rule set (test fixture):
| Prefix | action | Note |
|---|---|---|
| `+86755` | translate (target = `return-uas`) | Translation business |
| `+8675512` | translate (target = `return-uas`) | A longer prefix, used to verify longest-prefix-first |
| `+86138` | forward | Direct forwarding |
| `+86168` | block (603) | Anti-fraud block |

| # | Callee number | Expected action | Expected reason_code | Assertion focus |
|---|---|---|---|---|
| 1 | `+867550123456` | TRANSLATE | `MATCH_TRANSLATE` | Hits `+86755`, target is `return-uas` |
| 2 | `+8675512345678` | TRANSLATE | `MATCH_TRANSLATE` | Matches both `+86755` and `+8675512`; **assert that the longer prefix is hit** — `+8675512` (`matched_rule_id` can tell them apart) |
| 3 | `+861681000000` | DECLINE | `MATCH_BLOCK` | Returns 603 and **does not create the outbound leg** (REQ-F-7) |
| 4 | `+8613800000000` | FORWARD | `MATCH_FORWARD` | Direct forwarding |
| 5 | `+869990000000` | NOT_FOUND | `NO_MATCH` | Returns 404 and creates no outbound leg (REQ-F-6) |
| 6 | `867551234567` (no `+`) | TRANSLATE | `MATCH_TRANSLATE` | Matches after number normalisation; equivalent to case 1 |
| 7 | The number hits both block and translate (e.g. `+86168` block and `+8616` translate) | DECLINE | `MATCH_BLOCK` | **block takes priority over translate** (consistent with §1.2 REQ-F-7 acceptance) |

Note: the number in case 1 deliberately avoids `+8675512`, so that "hits `+86755`" and case 2's "hits the longer prefix" are two non-overlapping assertions.

General assertion: `decide()` is a pure function — the same input must always give the same output; no sockets, no clock reads, no global state (indirectly assertable via "the injected received_at does not participate in the decision" and "two consecutive calls give equal results").

### 5.2 StateStore contract (marker: contract)

The same set of cases is replayed against **both implementations**: `InMemoryStateStore` and `RedisStateStore` (the Redis cases skip in an environment with no Redis, but the contract itself must exist).

| # | Case | Assertion |
|---|---|---|
| 1 | `get` a non-existent key | Returns `None`, raises no exception |
| 2 | `get(k)` after `set(k, v, ttl)` | Returns bytes byte-identical to `v` |
| 3 | Write the same key with the same value twice | Consistent result, no exception (**idempotent**) |
| 4 | `set(ttl=1)`, inject a clock advance beyond the TTL | `get` returns `None`; the implementation **must not** read the system clock internally |
| 5 | `get(k)` after `delete(k)`; then `delete(k)` again | The first returns `None`, the second raises no exception |
| 6 | Key format | Of the form `as:{case}:{kind}:{id}` |
| 7 | Swap the write order | Consistent final value (idempotent semantics, surviving replay across a Redis split-brain window) |

### 5.3 The two states of feature gating (marker: unit)

| # | Case | Assertion |
|---|---|---|
| 1 | Unregistered toggle name | `is_enabled` returns `False` (**fail-closed**) |
| 2 | Deployment-level default state | Returns `False` (**off by default**) |
| 3 | Set to on at deployment level | Returns `True` |
| 4 | Runtime override on / off | The override value takes priority over the deployment level |
| 5 | Repeated evaluation within the same scope | Consistent result (**the decision is idempotent**) |
| 6 | The decision entry point does not depend on a real Redis | Done by injecting a `ToggleSource`; the test has no sockets |

Both states (on / off) must be covered (ADR-0020, REQ-G-1).

### 5.4 Telemetry must not block (marker: unit)

| # | Case | Assertion |
|---|---|---|
| 1 | The call path calls `emit()` | Produces no network IO at all (assert via a NoOp / fake exporter that the socket was never called) |
| 2 | Keep calling `emit()` after the queue is full | Raises no exception, does not block; the `dropped` counter increments |
| 3 | Default sink | Is `NoOpSink` (no error when no exporter is configured) |
| 4 | Export thread | Consumes the queue on an independent thread; the call path does not wait for the export to complete |

### 5.5 Process-shell draining (marker: unit)

| # | Case | Assertion |
|---|---|---|
| 1 | SIGTERM received when `active_calls == 0` | Stops accepting new requests and exits |
| 2 | SIGTERM received when `active_calls > 0` | **Does not exit**; new requests are rejected; exits once it reaches zero |
| 3 | Zero not reached before the timeout (a configurable upper bound) | Forced exit and logged; must never wait indefinitely |

### 5.6 Traceability to requirements / design

| This section | Corresponding REQ | Corresponding design |
|---|---|---|
| 5.1 | REQ-F-1, REQ-F-6, REQ-F-7 | `lld.md` §2, §3 |
| 5.2 | REQ-NF-1, REQ-NF-2 | `lld.md` §4 (ADR-0002, ADR-0007) |
| 5.3 | REQ-G-1 | `lld.md` §5 (ADR-0020) |
| 5.4 | REQ-NF-13 | `lld.md` §6 (ADR-0005) |
| 5.5 | REQ-NF-4 | `lld.md` §7 (ADR-0009) |

