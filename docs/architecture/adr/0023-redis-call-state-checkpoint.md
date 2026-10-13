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

# ADR-0023: Redis application-layer call-state checkpoint (necessary state)

- **Status**: proposed
- **Date**: 2026-10-01
- **Decides**: Records the implementation direction for decision §0 decision 2: checkpoint the minimal application-layer call state needed for recovery in Redis; do not serialize the entire `SipStack` / DUM objects
- **Responds to REQ**: REQ-NF-1, REQ-NF-2, REQ-NF-4; related REQ-F-1, REQ-F-2, REQ-F-5, REQ-F-8, REQ-F-9, REQ-F-11; boundary REQ-NF-6

## Context

The production SIP stack direction remains reSIProcate C++; product decision and application logic remain Python. DUM holds active SIP dialog, session, and transaction runtime. Writing the product's selected business/dialog fields into Redis does not equal serializing or recovering those native runtime objects.

REQ-NF-1 remains a hard requirement, originally requiring that an in-progress call not be dropped on process restart or failure. The current [`test-plan.md`](../../acceptance/test-plan.md) defines a fairly precise executable baseline for it: after an established dialog completes its ACK exchange, kill/restart the AS, then send a same-dialog BYE from upstream; the new process must route the BYE to the peer, and a complete dialog record must exist in Redis. That baseline only covers established dialogs whose ACK has completed and new BYEs arriving after restart; it does not cover INVITE, CANCEL, final responses, or 2xx/ACK transactions still in flight at crash time. REQ-NF-1's broad wording may exceed the precise acceptance scope of the current test plan; this ADR does not modify or narrow that requirement.

Existing D10 evidence shows: the cross-process UAC `DialogSetId` narrow path can rebuild the UAC dialog set and initiate a same-dialog re-INVITE, but does not restore the old `InviteSession` or transaction runtime; a fresh DUM returns 481 when it receives a same-dialog BYE for an already-established UAS dialog. D10 acceptance therefore still fails; UAS rehydrate and the product `CallController` two-leg recovery remain unresolved. See [D10 review](../../reviews/d10-state-recovery-gap-review-2026-09-30.md) and [recovery options comparison](../call-state-recovery-options.md).

ADR-0002 remains accepted and this ADR does not modify it. Its architectural wording "all session state externalized" cannot prove that the default DUM UAS dialog or `SipStack` transaction runtime can be rebuilt from externalized data; the conflict between this architectural goal and the current recovery capability remains unresolved and cannot be claimed as REQ-NF-1 satisfied via this ADR.

The current [`StateStore`](../../../platform/src/as_platform/state/store.py) provides only generic primitives such as `get`, `set`, `delete`, `expire`; [`RedisStateStore`](../../../platform/src/as_platform/state/redis_store.py) and its contract tests provide no two-leg atomic checkpoint, owner fencing, or durable-commit semantics. The existing decision code of both apps also writes no call state: the translation decision is a pure function; anti-fraud's pure function receives read-only rate-window counter inputs. Their specific evidence is in this ADR's Evidence and [recovery options comparison](../call-state-recovery-options.md).

This decision handles SIP signaling / dialog / controller data, not RTP or media state. Media remains excluded by REQ-NF-6 and [ADR-0004](0004-media-seam.md).

## Decision

1. Record the already-clearly-chosen **implementation direction**: use Redis to persist the application-layer necessary call state needed for recovery. This choice is a direction, not a claim that this ADR is accepted, the code is implemented, or D10 has passed.
2. The logical unit of a checkpoint is one call's complete controller state plus the necessary signaling/dialog data of its two B2BUA legs. Exact fields, serialization schema, migration strategy, and lifecycle must be frozen in later HLD/LLD from real SIP replay; the checkpoint does not include DUM pointers, complete `InviteSession` objects, SipStack transactions, timers, or any SIP message.
3. The two legs must be committed and recovered as one logically consistent checkpoint. The checkpoint carries a schema version, a monotonically increasing generation/revision, and owner-fencing information. After takeover, the old owner's fence is invalidated; no old process may continue to produce SIP side effects after the new owner takes over. The recovery side may only see one complete and committed two-leg revision; it must not serve a call with a half-leg state.
4. A single Redis value, or a verified Redis atomic script/transaction, are both optional physical representations later; the specific representation is a subordinate implementation detail, but two-legs-all-or-nothing, revision check, and fencing are hard constraints. The current generic `StateStore` contract itself does not satisfy these constraints.
5. Any SIP side effect that depends on a checkpoint must first have a durable-commit acknowledgement for the corresponding revision. A SIP callback must not block waiting for Redis: the write completes outside the callback, and the state machine may only continue with a non-blocking continuation after receiving an acknowledgement that satisfies the defined durability boundary. Merely enqueuing, writing to a client buffer, or issuing an async command does not mean the checkpoint is committed; without a durable acknowledgement, do not claim committed, nor execute a side effect that depends on that commit. Durability configuration, failure policy, and acceptable data-loss window must be defined by later design and acceptance.
6. The checkpoint reserves a namespaced, versioned extension payload for future AS-specific business data; the current translation payload is empty, and anti-fraud rate-window counters are not placed in per-dialog checkpoints. If, in future, signaled context/header values provided via the S-CSCF need to be retained, only selected values that have passed peer authentication and allowlist validation may be stored; size, retention, and data classification must be constrained. Arbitrary complete SIP messages or all headers must not be stored. Duplicate-header values and order are retained only when an approved header contract explicitly requires it. This ADR specifies no header names and claims no current app consumes such headers; the trust and privacy boundary follows [ADR-0016](0016-in-boundary-security.md).

The commitment boundary for the current restart phase is as follows:

| Phase at crash | Current commitment and boundary |
|---|---|
| Idle | No active call needs recovery; this ADR makes no call-continuity commitment for the idle state. |
| Inbound INVITE, before durable checkpoint / decision | Rebuilding a call from uncommitted input is unsupported; lossless recovery is not promised. |
| Outbound INVITE pending, early, or provisional | Recovering pending transactions, branches, retransmissions, or timers is unsupported; not part of the current D10 test-plan gate. |
| Final 2xx sent, waiting for ACK | Recovering that transaction/ACK handling is unsupported; not part of the current D10 test-plan gate. |
| Established dialog after ACK completed | **The current D10 baseline that must pass**: the goal is to recover from a complete Redis two-leg record and route a new upstream same-dialog BYE arriving after restart to the peer. Success is not yet promised: fresh DUM returns 481 to a UAS BYE, so a working recovery adapter must first exist and pass the current acceptance. |
| In-dialog request / transaction pending at crash | Recovering requests/response transactions left unfinished before the crash is not guaranteed. The current baseline sends one new BYE only after the process restarts; it does not represent verified pending-BYE, UPDATE, or re-INVITE recovery. |
| Terminal cleanup | A terminated call is not re-served as an active call; the interaction of terminal markers, idempotent cleanup, TTL, and owner fence still must be implemented and tested. |

INVITE/CANCEL/final-response/2xx-ACK and other in-flight transactions at crash time are not part of the current executable D10 acceptance, nor are they promised for recovery in this ADR. If the product requires these phases, the requirement and test plan must be separately reviewed and expanded; REQ-NF-1's broad wording remains unchanged.

## Consequences

### Positive

- While keeping the reSIProcate C++ and Python product-logic boundary, it selects the Redis direction consistent with ADR-0002, and does not misinterpret "stateless process" as serializing the entire SIP stack.
- It separates the call checkpoint from anti-fraud rate-window aggregate state and PostgreSQL governance state, avoiding copying non-call-level counters into every call record.
- It leaves a bounded extension point for future governance-permitted AS-specific data and selected signaling context.

### Negative / accepted

- **D10 remains blocked, REQ-NF-1 not met.** Current D10 acceptance cannot pass until a complete Redis dialog record exists and a same-dialog BYE after restart is routed to the peer; fresh DUM currently returns 481. The direction choice does not substitute for a recovery adapter, product CallController two-leg rebuild, or acceptance.
- UAS dialog rehydrate has no verified implementation. SipStack in-flight transaction and DUM session/timer recovery are likewise unresolved; this ADR does not promise to recover them.
- Two-leg atomic commit, durability/write-before-side-effect, generation and fencing, non-blocking durability continuation, and failure/cleanup policy all require new design and behavior tests. The existing `StateStore` contract alone cannot prove these semantics.
- The conflict between ADR-0002's "all session state externalized" wording and the default DUM UAS/transaction runtime's inability to be rebuilt from the current Redis record remains open. ADR-0002 remains accepted / unchanged; this ADR does not supersede it, nor silently narrow REQ-NF-1.
- Pending INVITE/CANCEL/final response/2xx-ACK recovery is beyond the current D10 test-plan; broader product guarantees need separate requirement/test-plan review.
- The failure model, acknowledgement semantics, and RPO of a Redis durable commit are not yet defined. If the configured Redis acknowledgement does not represent the required durability, the product must not treat it as a committed checkpoint.

## Alternatives considered

| Option | Why not |
|---|---|
| Keep state only in the current process | A process restart loses application state, failing REQ-NF-1's goal; ADR-0002 already excluded this runtime model. |
| Use PostgreSQL for necessary call state | This ADR explicitly chooses the Redis direction; PostgreSQL is only a future implementation reference, requiring separate review of ADR-0002's latency/runtime-storage constraints, and a transactional store would not rebuild DUM/UAS/transaction runtime either. |
| Serialize the entire reSIProcate `SipStack` / DUM objects | There is currently no such verifiable recovery contract; an object dump also does not automatically define timer, transport, owner-handoff, and version-compatibility semantics. This ADR does not set it as a goal. |
| Replace reSIProcate with another SIP product that supports persistence | The SIP stack choice is decided by ADR-0019. Replacement needs a separate architectural adjudication and product-semantics/deployment evaluation, not an implementation option of this ADR. |

## Evidence

- [`docs/acceptance/test-plan.md`](../../acceptance/test-plan.md) §2 REQ-NF-1: after ACK exchange completes, kill/restart, route upstream BYE to peer, complete dialog record exists in Redis.
- [D10 review](../../reviews/d10-state-recovery-gap-review-2026-09-30.md): records that the UAC `DialogSetId` narrow re-INVITE probe passed, fresh DUM UAS same-dialog BYE returns 481, and the Redis complete record and product controller mapping are not yet verified.
- [translation decision](../../../apps/translation/src/as_translation/decision.py) and [translation unit tests](../../../apps/translation/tests/test_decision.py): pure decision inputs/outputs, no app-owned per-call checkpoint or `StateStore` write.
- [anti-fraud decision](../../../apps/anti-fraud/src/as_anti_fraud/decision.py) and [anti-fraud unit tests](../../../apps/anti-fraud/tests/test_decision.py): `counters` is a read-only `Mapping[str, int]` input; tests assert the function does not modify counters; no app source/test wiring to `StateStore` was found.
- [`StateStore` protocol](../../../platform/src/as_platform/state/store.py), [`RedisStateStore`](../../../platform/src/as_platform/state/redis_store.py), and [store contract tests](../../../platform/tests/test_state_store_contract.py): existing API and contract cover generic key-value/TTL/idempotent single-key writes, not two-leg transactions, owner fencing, or durable acknowledgement.
- [ADR-0016](0016-in-boundary-security.md) establishes peer authentication, allowlist, and payload/privacy boundaries under out-of-network deployment; [ADR-0004](0004-media-seam.md) and REQ-NF-6 exclude media.

## Related

- [`../system-architecture.md`](../system-architecture.md) §0, §4.1, §7
- [ADR-0002](0002-per-usecase-process-state-redis.md): accepted per-use-case-one-process + Redis runtime direction; this ADR does not modify it
- [ADR-0019](0019-sip-stack-selection.md): reSIProcate production SIP stack
- [ADR-0022](0022-resiprocate-b2bua-control.md): proposed DUM/CallController boundary
- [ADR-0016](0016-in-boundary-security.md), [ADR-0004](0004-media-seam.md)
- [call-state recovery options comparison](../call-state-recovery-options.md)
- [D10 state recovery gap review](../../reviews/d10-state-recovery-gap-review-2026-09-30.md)
