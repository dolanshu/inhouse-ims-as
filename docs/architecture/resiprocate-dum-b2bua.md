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

# reSIProcate DUM Layer Capabilities and B2BUA Control-Layer Interface Design

> Applicable scenario: external third-party AS, SIP trunking, number translation, rule engine, 404/603/CANCEL, SDP pass-through.

> **Source-verification note (2026-09-30)**: This document is an exploratory architecture-design note, not an API contract. The C++ snippets below are uncompiled and unverified; several callback signatures and operations do not match reSIProcate 1.14.0 and must not be implemented from them. The only selected direction is reSIProcate (ADR-0019); the stack comparisons, implementation suggestions, and risk ratings here are background material and do not constitute a new product decision. At the layering level, SipStack owns transport and transaction processing/transaction timers; DUM uses SipStack as a TransactionUser/UA layer and manages dialog, InviteSession, and session-level behavior; the product controller owns cross-leg semantics and business control.

### reSIProcate 1.14.0 source-verification corrections

Verified version: tag `1.14.0`, commit `632e215c2ca9aee5416bfe1808851ea6fa380044`.

| Assumption/example in this document | Source-verification result |
|---|---|
| `onNewSession` uses a two-argument signature | Two overloads respectively receive `(ClientInviteSessionHandle, OfferAnswerType, const SipMessage&)` and `(ServerInviteSessionHandle, OfferAnswerType, const SipMessage&)`. `onProvisional` and `onFailure` are client-session callbacks; `onConnected` has a client-specific overload and a generic/server overload; `onTerminated` receives a handle, a reason, and an optional related message. There is no `InviteSessionHandler::onCancel` virtual. |
| `makeInviteSession(...)` returns `ClientInviteSessionHandle` | It returns the `shared_ptr<SipMessage>` to be sent; the session handle is obtained later via the DUM callback. |
| UAS CANCEL handled by `ServerInviteSession::cancel()`, application overrides `onCancel` | `ServerInviteSession` has no `cancel()`. When an initial UAS INVITE receives CANCEL, DUM's leg path returns 200 to CANCEL and 487 to INVITE, and notifies via `onTerminated(... RemoteCancel ...)`. The product controller must still coordinate the opposite UAC leg and cleanup/race. |
| `InviteSession::end()` or early-state `ClientInviteSession::end()` means CANCEL | `InviteSession::end()` means BYE; in this version `ClientInviteSession::end()` in early state also takes the BYE path. `ClientInviteSession::cancel()` exists; `DialogUsageManager::end(DialogSetId)` dispatches by DialogSet state. The specific cancel-API choice must be decided by the adapter spike and CANCEL/final-response race tests. |
| All session timers / retries managed by the application | DUM source includes RFC session-timer support; SipStack owns transaction processing, retransmission, and transaction timers, and DUM owns its session-level timer behavior. Product policy and other retries are kept separate from protocol timers. |
| Using `Contents` or leaving callbacks unchanged guarantees SDP bytes pass through unchanged | The default session-handler path extracts SDP via `Helper::getSdp`; the generic offer-answer pattern clones `Contents`. These source facts do not prove product-line REQ-F-4 SDP byte identity. It must be verified by a native adapter and wire-capture tests; the current conclusion is open. |
| Two legs may use a shared Call-ID or the original Call-ID as the correlation identifier | REQ-F-2 requires the two legs' Call-IDs to be independent. The controller should build correlation via an internal logical call key / session handles, not merging the two legs' Call-IDs. |

The verification above is based on the specified upstream source and does not mean the product adapter is implemented or has passed protocol acceptance.

### Process-restart probe supplement (2026-10-01; exploratory, non-normative)

`/tmp/as-resip-dum-process-restart/RESULTS.md` only proves a UAC `DialogSetId` rebuild hook: after Phase A process exits, Phase B's fresh SipStack+DUM manually restores To-tag, Route, remote target, and increments CSeq, sends a re-INVITE under the same Call-ID/tags, and receives 200/ACK. It does not restore the old `InviteSession`, transaction, or active media/call state.

Conversely, `/tmp/as-resip-dum-uas-restart/RESULTS.md` proves the default DUM UAS recovery path fails: after the old process establishes the dialog and completes 200/ACK then exits, a fresh DUM receives a well-formed same-dialog BYE and returns 481. In the source, a request with To-tag must be looked up in DUM's private dialog-set map; if the mapping is missing it returns 481; no public UAS DialogSet/session rehydrate API was found. This probe does not prove a custom DUM extension is impossible, but REQ-NF-1 is still not proven satisfied. This document remains non-normative reference and selects no recovery API or architectural workaround.

---

## 1. What the DUM Layer Accomplishes

DUM (Dialog Usage Manager) is the **high-level UA/session API** provided by reSIProcate. `SipStack` owns transport, SIP transaction processing, transaction timers, and its process loop; DUM is a `TransactionUser`, constructed with and holding a `SipStack&`, and on top of it provides dialog, `InviteSession`, and session-level behavior. The product `CallController` then sits above DUM, handling cross-leg correlation and business control.

### 1.1 Dialog/Invite-Session State Machine

- Automatically maintains UAS and UAC **InviteSession** states (Calling / Proceeding / Connected / Terminated).
- Handles INVITE 1xx, 2xx, 3xx–6xx, ACK, BYE, CANCEL, re-INVITE, UPDATE, etc.
- Automatically generates from-tag, to-tag, branch, and incrementing CSeq.
- Manages early-dialog and confirmed-dialog route set and remote target.

### 1.2 Callbacks (Observer pattern)

DUM reports InviteSession lifecycle through event callbacks. The descriptions below state event roles, not copy-paste function signatures; the exact overloads and parameters follow the verified 1.14.0 source.

| Event | Meaning | Control-layer responsibility |
|------|---------|------|
| `onNewSession` | UAC or UAS session establishment/correlation to a DUM session event; the two roles have different overloads | Record leg identity and begin the corresponding routing or state processing |
| `onProvisional` | client/UAC leg receives a provisional response | Coordinate sending a provisional response to the other leg per business policy |
| `onConnected` (client/UAC) | client leg receives final 2xx; DUM processes ACK per its UAC protocol flow | Coordinate the other leg's success response; do not assume this event means the UAS has received ACK |
| `onConnected` (server/UAS) | server leg enters connected state after receiving ACK | Update call state per the actual ACK event |
| `onFailure` | client/UAC leg receives a non-2xx final response | Map the result and coordinate the server leg and other pending branches |
| `onTerminated` | session-termination event, carrying the termination reason and an optional related SIP message | Coordinate the other leg by reason (including `RemoteCancel`) and clean up state |
| `onReadyToSend`, `onRedirected`, offer-answer-related events | other events during send-before, redirect, or offer-answer lifecycle | Handle only when the adapter design and tests explicitly require; do not infer message bytes are unchanged from these |

`InviteSessionHandler` has no `onCancel` virtual. When an initial UAS INVITE receives CANCEL, DUM returns 200 to CANCEL and 487 to the original INVITE, and notifies the application via a termination event carrying the `RemoteCancel` reason; the product controller remains responsible for coordinating the opposite UAC leg and the race cleanup.

### 1.3 Transport and Message Send/Receive

- DUM relies on the underlying `SipStack` for transport (UDP/TCP/TLS), transaction processing, transaction retransmission/timers, and message send/receive; DUM uses these mechanisms to implement UA/dialog/session behavior.
- The control layer drives sessions and messages through DUM operations verified by the adapter; do not treat this document as a specific send-API contract.

### 1.4 Session Management

- Maintains an `InviteSessionHandle` collection, allowing lookup and iteration over active sessions.
- `InviteSession::end()` means ending an established session (BYE semantics) and must not be used as CANCEL; in the verified version, early-state `ClientInviteSession::end()` is also not CANCEL.
- CANCEL is a state-dependent operation against an INVITE transaction/session not yet complete. The specific DUM operation adopted must be proven by the D9 spike and adapter tests covering races.

### 1.5 Functions Not Provided (left to the upper control layer)

- **Two-leg correlation**: DUM does not know that ServerInviteSession and ClientInviteSession belong to the same B2BUA call.
- **Business routing**: number translation, rule matching, error-code mapping.
- **Protocol/product policy layering**: DUM handles the SIP protocol and session-timer behavior it supports; the application owns product retries, backoff, routing retries, and similar policies, and the two must not be conflated.
- **Multi-leg coordination**: CANCEL needs to cancel both legs simultaneously; re-INVITE needs to pass between the two legs.
- **State persistence**: DUM does not write call state to a database.

---

## 2. How the Control Layer Interfaces with DUM

The B2BUA control layer sits above DUM; its core task is to **receive DUM's callback events, execute business logic, then call DUM's API to send messages or modify dialogs**.

### 2.1 Architecture Layers

```
┌─────────────────────────────────────────────────────┐
│               Your B2BUA Controller                  │
│  - receive DUM callbacks                             │
│  - maintain two-leg mapping table (ServerLeg <-> ClientLeg) │
│  - invoke routing/engine for number translation/routing decision │
│  - handle error branches (404/603/CANCEL)            │
│  - generate telemetry events                         │
├─────────────────────────────────────────────────────┤
│                  DUM Layer                           │
│  - TransactionUser / UA layer                        │
│  - Dialog / InviteSession state machine              │
│  - session-level behavior and session timer          │
├─────────────────────────────────────────────────────┤
│                  SipStack                            │
│  - transport layer (UDP/TCP/TLS)                     │
│  - transaction layer                                 │
│  - security (TLS certificates)                       │
└─────────────────────────────────────────────────────┘
```

### 2.2 Core Interface Pattern: Event-Driven Lifecycle

The control layer consumes DUM lifecycle events and drives corresponding session operations through the adapter. The table below describes responsibility boundaries, not C++ interfaces or method signatures:

| Lifecycle stage/event | Control-layer responsibility | Constraint |
|------|------|------|
| New inbound UAS session | Allocate an internal logical call key, record the server-leg session identity, perform business routing | Do not use the SIP Call-ID as the sole cross-leg identity |
| Establish outbound UAC leg | Request the adapter to create and correlate the client-leg session identity per the verified flow | The creation flow and exact API remain to be decided by the D9 spike and adapter tests |
| provisional, connected, failure | Coordinate the other leg by the event's owning leg and its session identity | client/UAC and server/UAS connected-event semantics differ; do not merge them as "received 2xx" |
| terminated | Handle cancel, failure, or normal completion by termination reason and optional related message, and clean up the mapping | Cleanup must consider the other leg and branches still in a race |

The two legs correlate via an internal logical call key and their respective session identities. Under REQ-F-2, the two SIP legs' Call-IDs must remain independent; the mapping may record each Call-ID for diagnostics, but must not merge them or repurpose them as a shared Call-ID.

### 2.3 Control Layer's Key Lifecycle

1. **Receive inbound INVITE (UAS leg)**: DUM establishes/correlates the UAS session and reports the event. The control layer creates the internal logical call key, saves the server-leg session identity, and invokes routing decision; reject, provisional-response, and similar behaviors are performed through adapter-verified DUM operations.
2. **Establish outbound INVITE (UAC leg)**: the control layer requests the adapter to establish the UAC session per the routing result, saves its independent session identity, and correlates it to the same internal logical call key. The exact creation and send call remains to be verified by the D9 spike and adapter tests. The two SIP legs' Call-IDs remain distinct per REQ-F-2.
3. **Handle provisional and final responses**: a client/UAC provisional event may prompt the control layer to coordinate the UAS leg per policy. After the client/UAC receives the final 2xx, DUM processes ACK per the UAC protocol flow; the control layer then coordinates the UAS leg's success response. The UAS connected event occurs upon receiving ACK, so the two connected events are different lifecycle facts.
4. **Handle client/UAC non-2xx final response**: `onFailure` is a client-leg event. The control layer maps it per product rules to the UAS leg and coordinates any other not-yet-complete branches before cleaning up state.
5. **Handle CANCEL of an inbound initial UAS INVITE**: DUM returns 200 to CANCEL and 487 to the original INVITE, then notifies the control layer with the `RemoteCancel` termination reason; there is no `onCancel` virtual. The product controller coordinates the outbound UAC leg, fork/parallel-branch cleanup, and the CANCEL-vs-final-response race. The outbound early leg must use the state-appropriate DUM operation, and that choice must be proven by adapter tests; do not treat `end()` as CANCEL.
6. **Handle termination of an established session**: BYE/end semantics differ from CANCEL. The control layer coordinates both legs and cleans up the mapping per session state; the exact DUM operation follows the adapter verification result.
7. **Handle pre-send messages and SDP**: if the product genuinely needs to rewrite headers or offer-answer content, it must go through a verified adapter path. `Contents` parsing/cloning in a callback, or leaving content unchanged, does not prove REQ-F-4 SDP wire-byte identity; only real wire-capture verification can claim conformance.

### 2.4 Control-Layer Responsibility Boundary Summary

| Responsibility | Owner |
|------|------|
| Create/destroy dialog | DUM |
| Transport, SIP transaction processing, transaction retransmission and transaction timer | SipStack |
| Dialog / InviteSession semantics, session-level behavior, and DUM-supported session timer | DUM (using SipStack) |
| Adaptation of product messages/session commands and cross-leg business semantics | adapter / product controller; must not duplicate stack transaction/timer |
| Two-leg correlation | control layer (your own map) |
| Number translation, routing decision | control layer (invoke routing/engine) |
| Error-code mapping (404/603) | control layer |
| Two-leg CANCEL/BYE coordination and product-level race cleanup | control layer, using state-appropriate operations proven by adapter tests; `end()` is BYE semantics |
| Product retry/backoff policy | control layer; distinct from DUM's protocol/session timer |
| SDP/header pass-through and REQ-F-4 acceptance | control layer and adapter; must be wire-capture verified; do not claim SDP byte identity before verification |
| Telemetry logging | control layer |
| Rule hot-loading | control layer (separate thread, does not affect DUM callbacks) |

### 2.5 Thread-Safety Notes

- The thread affinity of callback execution depends on the host and its event-loop integration; do not assume it necessarily runs on DUM's own thread or a fixed single-threaded EventLoop.
- Control-layer callbacks must be **non-blocking**, performing no long I/O (such as database queries, HTTP requests). If async processing is needed, follow the host event loop and the adapter's thread/handle-safety constraints, scheduling session operations back to the execution context permitted to perform them.
- If the routing engine is a pure, stateless function, it can be called within the callback; if it has caching/hot-loading, thread safety must be guaranteed per the host concurrency model (e.g. read-write lock or atomic pointer swap).

---

## 3. Comparison with sippy B2BUA

| Feature | sippy B2BUA | reSIProcate + self-built DUM |
|------|------------|------------------------|
| Out-of-the-box B2BUA | Yes (b2bua_simple) | No, control layer must be built |
| Two-leg correlation | Automatic | Manual |
| Callback model | Event-driven (similar) | Virtual-function callbacks |
| Error branches | Built-in | Self-implemented |
| TLS | Supported (needs compilation) | Native support |
| Community activity | Lower (personal project) | Higher (widely used in VoIP industry) |
| Learning curve | Low | Medium-high |

> Background comparison, not a product decision: team capability, POC speed, and migration suggestions do not change ADR-0019. Only reSIProcate is selected as the production-stack direction; sippy content does not constitute a candidate or migration authorization.

---

## 4. Risk Areas of a Self-Built B2BUA (reSIProcate DUM)

For the scenario (signaling-only, SDP/header pass-through, change Request-URI + number, rule engine, 404/603/CANCEL, Call-ID tracking), guard against these:

1. **Two-leg dialog correlation**: after the UAS leg receives INVITE, the control layer produces a UAC leg per the rules. Build the mapping with an internal logical call key and a per-leg session identity; keep the two ends' Call-IDs independent per REQ-F-2 and record each leg's tag, route-set, and similar info as needed, otherwise BYE/CANCEL/re-negotiation will hit the wrong leg.

2. **Early dialog and provisional**: 180 with no SDP, 180 with SDP, and 183 take different paths; if PRACK is required by the S-SBC/core (IMS often involves early-media/PRACK), DUM can support it but it must be handled in the control layer, otherwise you stall in early media.

3. **Retransmission/timers/transactions**: RFC3261 transaction processing, retransmission, and transaction timer belong to SipStack; DUM provides dialog/session behavior and its supported session timer. Bypassing SipStack to handle raw transactions yourself easily introduces errors.

4. **CANCEL/487/200 correlation**: an initial UAS CANCEL is handled by DUM returning 200 to CANCEL and 487 to INVITE, and reporting `RemoteCancel`. The controller must still coordinate the outbound UAC leg and fork, and handle the CANCEL-vs-final-response race; the outbound early-leg operation must be proven by state-applicability tests, and `end()` must not substitute for CANCEL.

5. **re-INVITE/UPDATE/hold/resume**: even with SDP pass-through, mid-session SDP changes and session-timer refresh must be forwarded bidirectionally without breaking the dialog route.

6. **The "pure pass-through" boundary of SDP pass-through**: RFC7092 classifies "change signaling only, not SDP" as signaling-only, and "change SDP" as SDP-modifying signaling-only. REQ-F-4 SDP wire-byte identity is currently unproven; `Contents` parse/clone or a no-op callback is insufficient to prove identity. Real wire capture is mandatory, and only after verification can conformance be claimed; if you normalize, filter codecs, or change IP, the corresponding SDP modification behavior must be separately verified.

7. **TLS long connections and concurrency**: the host and event-loop integration determine thread ownership and the concurrency model; B2BUA state must avoid races, and do not do blocking I/O in DUM callbacks.

8. **Testability**: put the pure-function routing engine outside; DUM callbacks only do "receive event → look up rule → modify message → send to peer," so unit tests don't depend on the network.

> Background risk rating, not a product decision: self-built thin control layer on DUM = medium; bare writing from SipStack = high; using DUM but stuffing all business into callbacks = medium-high (hard to test). Behavior and API still must be verified per source, adapter spike, and wire-level tests.
