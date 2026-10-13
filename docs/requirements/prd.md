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

# Product Requirements Document (PRD) — 3rdparty-as

**Version**: v0.2 (reviewed)
**Date**: 2026-09-28
**Status**: reviewed — all 24 Gaps of prd-v0.1-review have been adjudicated as accepted and the corresponding changes are all on disk

> **Acceptance-criteria status**: the concrete test cases are in acceptance/test-plan.md. The current test-plan is a placeholder; test cases will be added during the M2 kernel implementation phase.
> **Note on protocol section numbers**: the RFC 3261 section numbers here follow the original RFC 3261 as published by the IETF in 2002.

> This document is the single requirement standard for the product.
> Requirement numbering scheme: REQ-F-* (functional) / REQ-NF-* (non-functional) / REQ-G-* (governance) / REQ-S-* (security).
> Signalling protocol basis: RFC 3261 (SIP), 3GPP TS 24.229 (IMS).
> Acceptance criteria are in ../acceptance/test-plan.md.

---

## 0. Product overview

**What this product is.** 3rdparty-as is a third-party Application Server deployed **outside** the operator's IMS (IP Multimedia Subsystem) core network. When the operator's S-CSCF network element decides via iFC (initial Filter Criteria, the trigger-rule table defined in 3GPP TS 24.229) that a call needs third-party involvement, SIP signalling (RFC 3261) reaches us through the operator's S-SBC (the border session controller, which carries the **transparent bridging** responsibility). We execute the business-logic decision — number translation, anti-fraud interception, intelligent routing, and so on — and return the result through the S-SBC to the operator side. From the operator's S-CSCF point of view we are simply an "in-network AS"; the S-SBC hides the fact that we are "out-of-network".

**Who uses it and what problem it solves.** There are two kinds of audience: ① **the operator's business configuration staff** — they configure number-range matching rules and policies (which ranges need translation, which ranges trigger anti-fraud) and approve change records through the console we provide; ② **the business users** — third parties such as translation service providers, anti-fraud providers and intelligent routing platforms that need to embed business logic into the call path and do not want to deploy and maintain a SIP signalling stack themselves. The operator's value: with our AS they can flexibly onboard third-party business without modifying their own IMS core network configuration. The business side's value: with the business decision interface we provide, they need not care about SIP protocol details.

**What it does not do (non-goals, condensed).** No media (it does not touch RTP, does not transcode, does not handle DTMF, does not anchor media streams), no CDR (billing call detail records), no lawful intercept, no Diameter Sh interface, single tenant, configuration management does not go through GitOps (operator O&M staff should not have to learn Git just to change a number range). If media handling — playback, recording, transcoding — is needed in future, it is performed by the MRF (Media Resource Function) inside the operator's network once triggered; we only deliver the decision.

**The following non-goals have been formalised as REQ-NF-*/REQ-S-*, traceable and acceptance-testable**: no media (REQ-NF-6), no CDR (REQ-NF-7), no lawful intercept (REQ-NF-8), security baseline (REQ-S-*).

---

## 1. User stories and scenarios

### Actor 1: the operator's business configuration staff (console user)

#### US-1: configure number-range matching rules

**As a** operator business configuration staff member, **I want** to configure "number range → business type" matching rules on the console, **so that** when the S-CSCF triggers us via iFC, we can route the call to the corresponding business (translation / anti-fraud / intelligent routing) according to the rule.

**Scenario narrative**: a regional operator has launched a translation service, and all calls in the number range `+86755*` must trigger the translation AS. The configuration staff add a rule on the console: `match: +86755* → action: route translation`. The rule draft is submitted → it enters the approval queue → after approval the rule takes effect.

**Corresponding REQ**: REQ-F-1 (a basic call can get through), REQ-F-6 (no match → 404), REQ-F-12 (rule CRUD), REQ-F-14 (approval flow)

#### US-2: configure a block policy (anti-fraud)

**As a** operator business configuration staff member, **I want** to configure a "number range → block" policy on the console, **so that** known fraud ranges (such as `+86168*`) can be rejected immediately and the S-CSCF does not have to try other ASs.

**Scenario narrative**: the anti-fraud centre has supplied a batch of fraud number prefixes. The configuration staff add a rule: `match: +86168* → action: decline 603` (on the **callee** target number). When the callee number hits that prefix we return 603 Decline directly (consistent with the "target number" in REQ-F-7).

**Corresponding REQ**: REQ-F-7

#### US-3: query a call trace (complaint tracing)

**As a** operator business configuration staff member, **I want** to be able to query the complete SIP message trace of a call by Call-ID on the console, **so that** when a user complains "why was my call rejected", the cause can be traced quickly.

**Scenario narrative**: a user complains that calls to the number range `+861681234` were rejected. The configuration staff enter the Call-ID on the console and see: INVITE → 603 Decline, corresponding to a configured block policy taking effect.

**Corresponding REQ**: REQ-F-13 (trace query), REQ-NF-7 (no CDR → replaced by the call trace)

#### US-4: approve configuration change records

**As a** operator operations lead, **I want** configuration changes to have to pass an approval flow, **so that** nobody accidentally changes a rule wrongly and causes an outage across all business.

**Scenario narrative**: the configuration staff submit a change record "add the +86755* translation rule". The system enters the approval queue, the operations lead sees the approval request on the console → approves → the change takes effect, recording the approver and the approval time.

**Corresponding REQ**: REQ-F-14 (approval flow), REQ-NF-10

---

### Actor 2: the S-CSCF (the inter-system trigger)

#### US-5: transparently trigger the third-party AS via the S-SBC

**As an** S-CSCF network element, **I want** to transparently forward SIP signalling to the third-party AS via the S-SBC according to iFC, **so that** the operator can flexibly onboard third-party business without modifying its own IMS core network configuration.

**Scenario narrative**: a caller dials `+867551234567`. The S-CSCF checks by iFC: this range must trigger an AS. The S-CSCF sends the INVITE to the S-SBC, the S-SBC performs transparent bridging (the S-CSCF cannot see "out-of-network"), and the message reaches our AS. We execute the business logic and return the result.

**Corresponding REQ**: REQ-F-1, REQ-F-2, REQ-F-3, REQ-NF-5

#### US-6: clean up the trigger chain on receiving 404

**As an** S-CSCF network element, **I want** that when the AS I triggered returns 404 Not Found, I know that "this number range is not within that AS's business scope", **so that** I can remove that AS from the iFC chain and go on to try the next AS or connect directly to the peer.

**Scenario narrative**: a caller dials `+869991234` (matching no number-range rule). The S-CSCF triggers us by iFC. We return 404 Not Found. The S-CSCF cleans up the trigger chain and transfers the call directly to the peer.

**Corresponding REQ**: REQ-F-6

#### US-7: terminate retries on receiving 603 Decline

**As an** S-CSCF network element, **I want** that when the AS I triggered returns 603 Decline, I know that "this AS explicitly rejects this call, stop trying other ASs", **so that** network element resources are not wasted on meaningless retries.

**Scenario narrative**: a caller dials `+861681234` (hits the block policy). The S-CSCF triggers us. We immediately return 603 Decline. The S-CSCF terminates the iFC chain and the call ends at us.

**Corresponding REQ**: REQ-F-7

---

### Actor 3: the AS itself / the operations team (the "user" of system constraints)

#### US-8: calls are not interrupted when the process restarts

**As the** AS system, **I want** calls in progress not to be interrupted when the process restarts or fails, **so that** users cannot perceive that we are under maintenance.

**Scenario narrative**: a call has progressed to the 180 Ringing stage. Operations restarts the AS process. The call is not interrupted, the normal signalling flow continues, and finally 200 OK → BYE completes normally. The latency commitment is to be frozen after M6 measurements.

**Corresponding REQ**: REQ-NF-1

#### US-9: old and new versions run side by side during a version upgrade

**As the** operations team, **I want** that when upgrading the AS version, new requests are routed to the new-version process while existing calls finish on the old-version process, **so that** there is no call interruption during the upgrade.

**Scenario narrative**: version v1.2.0 → v1.3.0. During the upgrade, once the new version is ready, newly arriving requests must be routed to the new-version process; existing calls continue to complete on the old-version process; with no new requests arriving, everything reaches zero after 2 hours and the old-version process is decommissioned.

**Corresponding REQ**: REQ-NF-4

---

### Actor 4: the business side (translation / anti-fraud / intelligent routing providers)

#### US-10: query number translation results

**As a** translation service provider, **I want** to be able to query which translation rule matched a call here and what the translated number is, **so that** I can reconcile against my own translation business system.

**Scenario narrative**: a translation service provider has a +86755* rule translating to +852755*. An INVITE to +867551234567 is translated to +8527551234567. The translation service provider queries this trace through the interface by Call-ID.

**Corresponding REQ**: REQ-F-13 (trace query), REQ-F-16 (translation processing flow)

#### US-11: query anti-fraud interception reports

**As a** anti-fraud service provider, **I want** to be able to query which block policy a call intercepted by 603 Decline matched, **so that** I can generate an anti-fraud report and report it to the operator or the regulator.

**Scenario narrative**: an INVITE to +861681234 was rejected with 603 Decline. The anti-fraud service provider finds it matched R-BLOCK-90 (a fraud number range) and generates an interception report.

**Corresponding REQ**: REQ-F-13 (trace query), REQ-F-7 (603 Decline)

---

### Missing user stories + POC baseline

> The business description exists (§2 functional requirements) but user stories (§1) and POC baseline samples are missing. To be completed during the M2 probe phase.

| Use case to be added | Corresponding REQ | Reason |
|---|---|---|
| CANCEL flow user story | REQ-F-8 | The POC baseline already exists; the complete narrative can be added in the M2 design phase |
| in-dialog request routing | REQ-F-9 | Missing from the POC baseline |
| Non-2xx response branches | REQ-F-10 | The POC ReturnUas only returns 200 OK |
| CANCEL race | REQ-F-11 | The POC has no explicit race test |

---

## 2. Functional requirements (REQ-F-*)

**Signalling protocol basis**: RFC 3261 (SIP), 3GPP TS 24.229 (IMS session control).

Grouped by functional domain. Each item is marked **P0 / P1**:
- **P0 = the product does not exist without this function** (with no call-handling capability it does not deserve to be called an AS)
- **P1 = important but not core** (the product can run without it but is incomplete)

### 2.1 Core call signalling path (P0)

**This group defines the minimal closed loop of "accepting the operator's calls, executing business logic, and returning a result".**

---

#### REQ-F-1: an operator-triggered basic call, with the signalling sequence following RFC 3261 correctly

**Business description.** When the operator's S-CSCF triggers us by iFC (3GPP TS 24.229) to execute business logic, SIP signalling (RFC 3261) arrives via transparent bridging through the S-SBC. We handle the call as a B2BUA (RFC 3261 §6 Definitions + §12 Dialogs) — receiving the INVITE, executing the business decision (translation / anti-fraud / routing), and returning the result. The normal signalling sequence follows the RFC 3261 basic call flow: INVITE → 100 Trying → 180 Ringing → 200 OK → ACK → BYE → 200 OK.

**Acceptance criteria.** (Acceptance criteria are in ../acceptance/test-plan.md §1.1-REQ-F-1)

---

#### REQ-F-2: B2BUA dialog separation, with different Call-IDs on the two sides

**Business description.** As a B2BUA (RFC 3261 §6 Definitions (the B2BUA definition) and §12 Dialogs (a B2BUA maintains independent dialog state on each side)), we split one call into two independent dialogs. Each dialog has its own Call-ID (RFC 3261 §8.1.1 Call-ID header) — the Call-IDs of the two legs must differ, because the Call-ID identifies the uniqueness of a dialog (RFC 3261 §12.1 specifies that a B2BUA maintains independent dialog state on each side). The Request-URI (RFC 3261 §8.1.1.1 Request-URI + §19.1 generic URI format) is rewritten when traversing the B2BUA, ensuring that the routing of each leg is correct.

**Acceptance criteria.** (Acceptance criteria are in ../acceptance/test-plan.md §1.1-REQ-F-2)

---

#### REQ-F-3: Request-URI rewriting follows RFC 3261

**Business description.** The Request-URI (RFC 3261 §8.1.1.1 Request-URI + §19.1 generic URI format) carried by the upstream leg's INVITE is the operator-side routing address (for example `sip:+86123456789@s-cscf.operator.com`), and on the downstream leg it must be rewritten to the peer route we have selected internally (for example `sip:+86123456789@return-uas:5060`). The reverse direction is the same: a downstream-leg BYE must be rewritten back to the upstream leg's Request-URI. The rewriting rules come from the configured routing policy.

**Acceptance criteria.** (Acceptance criteria are in ../acceptance/test-plan.md §1.1-REQ-F-3)

---

#### REQ-F-4: complete SDP pass-through (we do not touch media)

**Business description.** The SDP offer (RFC 3261 §13.2.1 SDP offer/answer negotiation flow + RFC 3264 (SDP Offer/Answer Model), describing "I am ready to send voice, with which codec and which port") carried by the upstream INVITE must be passed through unchanged to the downstream peer; the SDP answer carried by the downstream 200 OK must likewise be passed back upstream unchanged. We do not do media anchoring at the application-server layer (that is, we do not "intercept" the voice stream, do not handle RTP ourselves, do not trigger DTMF). We keep an extension interface definition (enabled only when a playback / recording / transcoding / DTMF requirement appears), with an empty-shell production implementation. If media anchoring for playback / recording / transcoding is needed in future, it is performed by the MRF inside the operator's network, and we only tell the operator side over signalling that it should find the MRF.

**Acceptance criteria.** (Acceptance criteria are in ../acceptance/test-plan.md §1.1-REQ-F-4)

---

#### REQ-F-5: correct handling of Route / Record-Route headers, following RFC 3261

**Business description.** The value of a Route header addressed to us must be consumed (RFC 3261 §20.34 Route header + §16.4, the proxy rule class for consuming a Route addressed to this hop, as an analogue; a B2BUA has no direct MUST, but the behaviour should still be sensible). Routing information that needs to be carried over (the subsequent hop specified on the operator side) is explicitly generated by our routing policy, not copied mindlessly from the upstream Route header. If the downstream leg's peer returns a response carrying Record-Route (RFC 3261 §20.35 Record-Route header + §12.1.2, the reverse derivation of the Route Set from Record-Route), we must correctly handle Record-Route in the upstream leg's response, so that subsequent in-dialog requests are sent back along the path recorded in Record-Route.

**Acceptance criteria.** (Acceptance criteria are in ../acceptance/test-plan.md §1.1-REQ-F-5)

---

### 2.2 Routing and policy decisions (P0)

**This group is the reason we exist.** If we did nothing but "unconditionally forward" every call we received, the S-CSCF could just connect to the peer directly — we are triggered because we must make **decisions**: match a rule, choose a route, or reject.

---

#### REQ-F-6: return 404 Not Found when no rule matches

**Business description.** When the operator's S-CSCF triggers us through the S-SBC but the target number's range hits none of the configured business rules, we return 404 Not Found (RFC 3261 §21.4.5) — telling upstream "this range is not within our business scope". We return 404 rather than 403 Forbidden, because 403 means "I refuse to process", whereas 404 means "I do not exist (for this number range)". On the operator side the semantics are "clean up this trigger chain and transfer calls for this range to another AS or connect directly to the peer". The match target defaults to the target number (the callee direction); longest prefix first; no match → 404.

**Acceptance criteria.** (Acceptance criteria are in ../acceptance/test-plan.md §1.2-REQ-F-6)

---

#### REQ-F-7: return 603 Decline when a "block" policy is hit

**Business description.** When the target number hits a configured "block" policy (for example the anti-fraud range `+86168*`), we immediately return 603 Decline (RFC 3261 §21.6.2) — telling upstream "I reject this call, you need not try other ASs". In RFC 3261, 603 Decline explicitly means "declined by the user", and after receiving it the S-CSCF cleans up the trigger in the iFC chain and does not retry other ASs. The match target defaults to the target number; longest prefix first; on conflict, block rule > translation rule > default routing.

**Acceptance criteria.** (Acceptance criteria are in ../acceptance/test-plan.md §1.2-REQ-F-7)

---

### 2.3 Call lifecycle (P1)

**This group covers the various branch cases after the basic call.**

---

#### REQ-F-8: caller gives up — the CANCEL and BYE two-branch flows are correct

**Business description.** CANCEL and BYE are two different cancellation paths (RFC 3261 §9 vs §15): CANCEL is used when the INVITE has not yet produced a final response, BYE is used after the dialog has been established.

Branch ① — the outbound INVITE has no final response yet (early cancel): receiving CANCEL on the upstream leg → we return 200 OK to the CANCEL → we send CANCEL downstream → the peer (Return UAS) returns 487 Request Terminated to the INVITE → we pass the 487 through upstream → we send ACK upstream. The whole flow is "cancel the in-progress call and clean up the dialog" (RFC 3261 §9.2).

Branch ② — the outbound INVITE has already received 200 OK (cancel after the dialog is established): receiving CANCEL on the upstream leg → we return 200 OK to the CANCEL → but the outbound dialog is already established, so CANCEL has no effect (RFC 3261 §9 explicitly states that CANCEL has no effect on a request that has already produced a final response) → we must tear the dialog down with BYE: send BYE downstream → the peer returns 200 OK to the BYE → pass BYE through upstream → upstream returns 200 OK to the BYE → we pass it through to downstream.

**Acceptance criteria.** (Acceptance criteria are in ../acceptance/test-plan.md §1.3-REQ-F-8)

---

#### REQ-F-9: in-dialog request routing

**Business description.** After the dialog is established (the 200 OK → ACK exchange completes, RFC 3261 §17), subsequent in-dialog requests (re-INVITE, UPDATE, INFO, BYE) must be correctly routed to **the already-established active dialog** — they must not create a new dialog and must not be routed to the wrong peer. Dialog matching is based on Call-ID + local/remote tag (RFC 3261 §12 Dialogs); the Route header indicates the subsequent forwarding path.

**Acceptance criteria.** (Acceptance criteria are in ../acceptance/test-plan.md §1.3-REQ-F-9)

---

#### REQ-F-10: non-2xx response branches (486 / 480 / 408)

**Business description.** The downstream peer may return various non-2xx final responses: 486 Busy Here (line busy), 480 Temporarily Unavailable (temporarily unavailable), 408 Request Timeout (timeout). We must pass these responses through correctly back upstream (the "response pass-through" requirement of RFC 3261 §16.7), rather than "swallowing" or "rewriting" them in the middle. From the upstream perspective, "the downstream is busy" and "rejected" require different handling at the SIP protocol layer.

**Acceptance criteria.** (Acceptance criteria are in ../acceptance/test-plan.md §1.3-REQ-F-10)

---

#### REQ-F-11: the race between CANCEL and the final response

**Business description.** Referring to RFC 3261 §9.1, §9.2. CANCEL (RFC 3261 §9) and the downstream final response (200 OK or non-2xx) arriving almost simultaneously is a real race scenario. We must correctly handle both branches:

Branch ① — CANCEL arrives before the final response (the RFC-legal path): downstream has not yet returned a final response → we send CANCEL downstream → downstream returns 487 to the INVITE → we pass the 487 through upstream → we send ACK upstream.

Branch ② — the final response has already arrived (RFC §9 explicitly says "CANCEL has no effect on a request to which a UAS has already given a final response"): we have already received the downstream 200 OK or non-2xx final response → CANCEL has no effect on the outbound leg → we tear the dialog down with BYE (RFC §15): send BYE downstream → receive 200 OK → clean up the dialog.

**Acceptance criteria.** (Acceptance criteria are in ../acceptance/test-plan.md §1.3-REQ-F-11)

---

### 2.4 Console and configuration management (P1)

#### REQ-F-12: rule CRUD

**Business description.** Business configuration staff can create, read, update and delete number-range matching rules through the console. Each rule contains at least: match target (caller/callee), match mode (prefix/regex), target business type (translation / anti-fraud / routing / block / default), and enabled/disabled state.

**M4 scope note (2026-10-03 maintainer ruling)**: the **runtime matching axis** for routing/block/translation is consistent with REQ-F-6/F-7 and is **the callee (target number)** in all cases. M4 acceptance covers only console **callee + prefix** rule CRUD and distribution; **caller** matching and **regex** mode are marked **v1.1** and are out of scope for M4 acceptance. See [`reviews/m4-req-calling-regex-lossless-adjudication-2026-10-03.md`](../reviews/m4-req-calling-regex-lossless-adjudication-2026-10-03.md) for details.

**Acceptance criteria.** (Acceptance criteria are in ../acceptance/test-plan.md §1.4-REQ-F-12)

#### REQ-F-13: trace query

**Business description.** Both business configuration staff and the business side can query the complete message trace of a call by Call-ID (all SIP messages from INVITE → BYE, with inbound/outbound direction, timestamp, method, response code).

**Acceptance criteria.** (Acceptance criteria are in ../acceptance/test-plan.md §1.4-REQ-F-13)

#### REQ-F-14: approval flow

**Business description.** Configuration changes (rule create/update/delete, policy changes) must pass an approval flow: submit a change record → it enters the approval queue → the approver approves/rejects → after approval the rule takes effect. A rejection must carry a reason.

**Acceptance criteria.** (Acceptance criteria are in ../acceptance/test-plan.md §1.4-REQ-F-14)

#### REQ-F-15: canary distribution and rollback

**Business description.** New rule versions must be distributable in a canary fashion — notifying AS instances in batches to load the new rule version, with a health check per batch. If a problem is found during distribution it can be rolled back automatically to the previous version, and it can also be rolled back manually.

**Acceptance criteria.** (Acceptance criteria are in ../acceptance/test-plan.md §1.4-REQ-F-15)

---

### 2.5 Business decision chain (P1)

#### REQ-F-16: processing after a translation rule is hit

**Business description.** When the target number hits a configured translation rule (for example +86755* → +852755*), we must: ① extract the caller/callee number, ② perform number translation per the rule, ③ look up the next-hop route for the translated number, ④ send the downstream INVITE carrying the new Request-URI. The translation result, the version number of the rule that matched, and the routing target must be traceable (visible via the REQ-F-13 trace query).

**Acceptance criteria.** (Acceptance criteria are in ../acceptance/test-plan.md §1.5-REQ-F-16)

---

### 2.6 Known gaps

| Requirement | Gap description | Planned completion |
|---|---|---|
| REQ-F-9 | The POC has no ready-made capture, only indirect coverage via the chained topology | Add comparison scenarios to the testbed in the M2 probe phase |
| REQ-F-10 | The POC ReturnUas only returns 200 OK, with no busy branch | Add comparison scenarios to the testbed in the M2 probe phase |
| REQ-F-11 | The POC has no explicit race test | Add comparison scenarios to the testbed in the M2 probe phase |
| REQ-F-12 (extension) | Caller matching and regex mode: a long-term PRD capability; **M4 is callee+prefix only** | **v1.1** (accepted once the internal API / RuleSet and console capabilities are completed) |

These three do not block M1 (M1 focuses on the P0 core path and the P1 call-lifecycle backbone), but they do block M2's "complete protocol behaviour" verification. REQ-F-12 (extension) does not block M4 closure (see the REQ-F-12 M4 scope note).

---

## 3. Non-functional requirements (REQ-NF-*)

Non-functional requirements define "how the product must run", not "what functions the product must have". Each item is marked **P0 / P1**:
- **P0 = the cornerstone of the product architecture** (if it is not met, functional requirements are moot)
- **P1 = important but not an architectural cornerstone** (a defect is not fatal but operations will trip over it)

### 3.1 Core architectural constraints (P0)

---

#### REQ-NF-1: no session loss on process restart

**Business description.** On process restart or failure, calls in progress must not be cut — session state, dialog state and business processing state must be persisted outside the process.

**Acceptance criteria.** (Acceptance criteria are in ../acceptance/test-plan.md §2-REQ-NF-1)

---

#### REQ-NF-2: bounded per-process state

**Business description.** One business use case per process. A process crash affects only the use case it carries and does not spill over into the others.

**Acceptance criteria.** (Acceptance criteria are in ../acceptance/test-plan.md §2-REQ-NF-2)

---

#### REQ-NF-3: horizontally scalable

**Business description.** Supports horizontal scaling: processing instances can be added as business volume grows without affecting existing calls; and it can scale down safely as business volume shrinks.

**Acceptance criteria.** (Acceptance criteria are in ../acceptance/test-plan.md §2-REQ-NF-3)

---

#### REQ-NF-4: In-Service Upgrade (ISSU) support

**Business description.** During a version upgrade or configuration update, calls in progress must not be cut. New requests are routed to the new-version process while existing calls continue to complete.

**Acceptance criteria.** (Acceptance criteria are in ../acceptance/test-plan.md §2-REQ-NF-4)

---

#### REQ-NF-5: S-SBC transparent bridging — we cannot see the in-network/out-of-network distinction

**Business description.** From the perspective of our AS, a message coming from the S-SBC "is" a message from the S-CSCF. We do not need to implement two sets of logic, an "in-network AS adaptation layer" and an "out-of-network AS adaptation layer" — the S-SBC has done the transparent bridging, and we only need to implement **one** access semantics.

**Acceptance criteria.** (Acceptance criteria are in ../acceptance/test-plan.md §2-REQ-NF-5)

---

#### REQ-NF-9: single-tenant on-premises deployment

**Business description.** An independent instance per customer, delivered on-premises (deployed inside the operator's machine room). No multi-tenancy (no shared instance + logical isolation + tenant namespaces). The reason for choosing single tenancy: the operator's delivery form is itself one customer one system; multi-tenancy brings no benefit in this scenario and instead increases cross-tenant data leakage risk.

**Acceptance criteria.** (Acceptance criteria are in ../acceptance/test-plan.md §2-REQ-NF-9)

---

### 3.2 Scaling and governance (P1)

This group defines "how operations and the engineering team must cooperate in order to maintain this product long-term".

---

#### REQ-NF-6: no media

**Business description.** No RTP implementation, no transcoding, no DTMF handling, no media anchoring, no MRF deployment. We keep an extension interface definition (enabled only when a playback / recording / transcoding / DTMF requirement appears), with an empty-shell production implementation. The reason: an out-of-network third-party AS doing media relay creates a triangular route (media leaves the network and comes back, doubling bandwidth and increasing latency), and an out-of-network node handling user voice involves lawful intercept and privacy compliance. (Per ADR-0004, currently in skeleton state, completed in M2)

**Acceptance criteria.** (Acceptance criteria are in ../acceptance/test-plan.md §2-REQ-NF-6)

---

#### REQ-NF-7: no CDR — replaced by the call trace

**Business description.** No billing record collection, no CDR delivery, no CDR archiving and no wholesale rating. Instead of CDR, a Call-ID-keyed **call trace** is used — every SIP message (inbound/outbound, timestamp, method, response code) can be queried through the console, for complaint tracing and anti-fraud evidence. The call trace is not a billing record: it has no delivery channel, does no wholesale rating and does no inter-operator settlement. The trace retention period is undecided — determined by the customer's compliance requirements, frozen in the M4 design phase. The cleanup job has been formalised as a function, but its default value is undecided. (Per ADR-0017, currently in skeleton state, completed in M2)

**Acceptance criteria.** (Acceptance criteria are in ../acceptance/test-plan.md §2-REQ-NF-7)

---

#### REQ-NF-8: no lawful intercept (LI)

**Business description.** No lawful intercept implementation. IRI (Intercept Related Information) belongs to the responsibility of in-network network elements (S-CSCF, S-SBC); letting a third-party AS get involved introduces cross-jurisdiction exposure (the three elements — intercept instruction, intercept target data, intercept acknowledgement — are not in the same jurisdiction). We collect no media content, and signalling-layer IRI should be output by the in-network network elements themselves. (Per ADR-0016, currently in skeleton state, completed in M2)

**Acceptance criteria.** (Acceptance criteria are in ../acceptance/test-plan.md §2-REQ-NF-8)

---

#### REQ-NF-10: configuration does not go through GitOps

**Business description.** Configuration changes must pass an approval flow. Changes must be versionable, traceable, publishable in canary fashion and rollbackable. Operations staff are not required to learn Git in order to change configuration.

**Acceptance criteria.** (Acceptance criteria are in ../acceptance/test-plan.md §2-REQ-NF-10)

---

#### REQ-NF-11: single source of the version

**Business description.** The product has exactly one version number, and all components declare their own interface versions. It is not permitted for several components to each have different release versions.

**Acceptance criteria.** (Acceptance criteria are in ../acceptance/test-plan.md §2-REQ-NF-11)

---

#### REQ-NF-12: all components managed in one repository

**Business description.** All components live in one repository. Build and container build must not fail because of cross-repository dependencies.

**Acceptance criteria.** (Acceptance criteria are in ../acceptance/test-plan.md §2-REQ-NF-12)

---

#### REQ-NF-13: OTel three-signal export

**Business description.** Export the three OpenTelemetry signals: metrics (active_calls, cps, rule match rate, 4xx/5xx rate), traces (the complete span chain per call), logs (structured JSON logs). Metrics can be consumed by Prometheus/Grafana.

**Acceptance criteria.** (Acceptance criteria are in ../acceptance/test-plan.md §2-REQ-NF-13)

---

#### REQ-NF-14: alert rule set

**Business description.** Based on the metrics exported by REQ-NF-13, a preset alert rule set: active_calls spike > 30%, 5xx rate > 1%, process restart loop (> 3 times within 1min), certificate expiring within 30 days.

**Acceptance criteria.** (Acceptance criteria are in ../acceptance/test-plan.md §2-REQ-NF-14)

---

#### REQ-NF-15: three-layer testbed and real-socket capacity study

**Business description.** See the separate clause [`req-nf-15-testbed-performance.md`](req-nf-15-testbed-performance.md): the testbed is split into contracts / simulators / load layers; the capacity and O1 study permits only the real-socket load-testing path; the testbed is a research and development asset and is not a v1 deliverable. This REQ does not specify an external SLA or any marketing capacity claim.

**Acceptance criteria.** (Acceptance criteria are in ../acceptance/test-plan.md §2-REQ-NF-15)

---

#### REQ-NF-16: version lifecycle and EOL policy

**Business description.** Every formal release (GA) should define an explicit lifecycle:
- Support period: the minimum duration from GA to EOL (recommended ≥ 12 months)
- EOL advance notice period: at least 6 months
- Upgrade path: adjacent minor versions can be upgraded to directly; a migration guide must be provided across major versions
- LTS versions: LTS is not defined for now; if it is needed in future, a new ADR must be added
- Security patches: no security patches are provided after EOL

**Corresponding ADR**: ADR-0027

**Acceptance criteria.** (Acceptance criteria are in ../acceptance/test-plan.md §2-REQ-NF-16)

---

## 4. Security requirements (REQ-S-*) — newly added (overturns the requirements-m1-review Gap 3 ruling)

**Note**: the M1 phase adjudicated that "security requirements are implicitly covered by REQ-NF" (requirements-m1-review Gap 3); **that ruling is now overturned**. AGENT.md §13 explicitly says "the trunk is untrusted", so security semantics cannot be implicit and must be formalised into traceable, acceptance-testable REQ-S-* items.

#### REQ-S-1: peer allowlist validation

**Business description.** Only accept messages from peers inside the allowlist (S-SBC, authorised business parties). The allowlist is distributed via config-service and supports certificate fingerprint validation or IP:port allowlisting. Messages not on the allowlist are dropped directly or answered with 403.

**Acceptance criteria.** (Acceptance criteria are in ../acceptance/test-plan.md §3-REQ-S-1)

#### REQ-S-2: end-to-end TLS with the S-SBC

**Business description.** The signalling channel between us and the S-SBC must be encrypted (TLS). The TLS certificate is issued by the operator's PKI. Plaintext connections are rejected.

**Acceptance criteria.** (Acceptance criteria are in ../acceptance/test-plan.md §3-REQ-S-2)

#### REQ-S-3: certificate hot rotation

**Business description.** TLS certificates can be hot-rotated before their validity period expires — calls in progress are unaffected and new connections use the new certificate. During rotation the old and new certificates are both valid (a dual-certificate window).

**Acceptance criteria.** (Acceptance criteria are in ../acceptance/test-plan.md §3-REQ-S-3)

#### REQ-S-4: console operation authorisation and audit

**Business description.** All write operations on the console (rule CRUD, approval, rollback) must be authorised (RBAC, or a minimal role set + password/certificate), and all operations generate tamper-proof audit logs (operator, timestamp, operation type, before/after values). The audit log retention period = the compliance requirement (frozen at M4).

**Acceptance criteria.** (Acceptance criteria are in ../acceptance/test-plan.md §3-REQ-S-4)

---

## 5. Governance requirements (REQ-G-*)

**This group is marked P2 = engineering discipline constraints.** They do not affect the correctness of the product's functionality but do affect long-term maintainability. Not meeting them does not block functional acceptance but does block the local gate (make gate).

Governance requirements constrain development discipline and engineering methodology. All are **P2**.

---

#### REQ-G-1: every feature must have an explicit enablement ruling

**Business description.** Before every new feature enters HLD/LLD, three things must be explicitly adjudicated: ① whether to introduce a feature switch, ② the switch's default state (it must default to off), ③ the switch's removal condition (to prevent switch debt). A switch only enables/disables capability and **does not change the interface contract**; when off it follows the existing default path.

**Acceptance criteria.** (Acceptance criteria are in ../acceptance/test-plan.md §4-REQ-G-1)

---

#### REQ-G-2: changes must run through the whole document chain

**Business description.** Any behavioural change — however small — must run through the entire document chain: requirement → ADR → design → contract → code → acceptance. Changing code without changing the upstream documents is unfinished work. The requirement is the only standard, and every stage must be traceable to a concrete REQ-* number.

**Acceptance criteria.** (Acceptance criteria are in ../acceptance/test-plan.md §4-REQ-G-2)

---

#### REQ-G-3: non-obvious code must be annotated with the corresponding ADR

**Business description.** Non-obvious code (code whose reason for being written this way is not understandable without context) must carry a comment pointing at the corresponding architectural decision. Design decision points in the code, non-intuitive engineering trade-offs and architectural implementations backed by an ADR must be annotated at the end of the code line with `# See ADR-00NN`. A reviewer walks from the code to the reason in one step instead of guessing. The AST scan is an extra step outside `make gate` and is not part of the standard four make gate actions. The AST scan can be triggered via the `make gate-strict` target.

**Acceptance criteria.** (Acceptance criteria are in ../acceptance/test-plan.md §4-REQ-G-3)

---

#### REQ-G-4: make gate must be fully green before committing

**Business description.** `make gate` = `ruff format --check` → `ruff check` → `mypy` → pytest (the unit/contract layer). If the local gate is not green, nothing may be committed. `--no-verify` and its equivalents are forbidden.

**Acceptance criteria.** (Acceptance criteria are in ../acceptance/test-plan.md §4-REQ-G-4)

---

## 6. Version history

| Version | Date | Description | Author |
|---|---|---|---|
| v0.1 (draft) | 2026-09-28 | First version, rewritten from the architecture quick-reference table into a top-down PRD | AI agent |
| v0.1 (draft) | 2026-09-28 | Stripped out design content: removed all technical annotations, rewrote the business description without design language | AI agent (writing subagent) |
| v0.2 (reviewed) | 2026-09-28 | All 24 prd-v0.1-review Gaps addressed: A1-5 protocol hard errors (REQ-F-8/2/11/RFC sections/Route semantics), B1-7 coverage gaps (Actor 4, REQ-F-12-16, REQ-S-1-4, REQ-NF-13/14, trace retention period undecided), C1-12 consistency cleanup | AI agent (writing subagent) |

---

## 7. Note on making up for lost ground

This PRD was created **after** the existing ADRs (0001, 0002, 0003, 0011, 0018, 0019, 0020). In the ideal order of AGENT.md §3.1, the requirement should come **before** the ADR. **This round is making up for lost ground; the Context sections of existing ADRs are not retroactively modified**.

**The new decision flow from M2 onwards requires:** every new ADR must first have a requirement written (appended to this document), and only then have the ADR written. The ADR document header must carry a "this ADR responds to REQ-*" field. Existing ADRs do not retroactively get this field, but new ADRs from M2 onwards must comply.
