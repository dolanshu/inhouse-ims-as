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

# ADR-0023 Redis Call State Checkpoint Review Record

- **Review target**: [ADR-0023](../architecture/adr/0023-redis-call-state-checkpoint.md) and its REQ / source trace
- **Date**: 2026-10-01
- **Reviewer**: GitHub Copilot (writing subagent; technical review)
- **Conclusion**: **conditional technical pass; formal maintainer review and sign-off pending**

## Conclusion and Scope

ADR-0023 accurately records the direction explicitly chosen by the user this time: a Redis checkpoint of the necessary application-layer state, rather than serializing the full `SipStack` / DUM objects. That direction comes from the user's decision, not from an independent AI choice. The ADR status is still `proposed` and the registry status is `draft`; the conditional technical pass in this record does not mean the ADR was accepted, that implementation is complete, or that REQ-NF-1 / D10 was accepted.

This record reviews only the technical boundaries and provenance traceability of ADR-0023; it does not modify code, tests, the PRD or the test plan. Formal maintainer review, architecture acceptance and sign-off are still pending.

## REQ and Evidence Traceability

| Requirement / boundary | Traceability conclusion |
|---|---|
| REQ-NF-1 | The original wording "in-progress calls must not be dropped" remains a hard requirement. The current executable baseline of D10 in [`test-plan.md`](../acceptance/test-plan.md) is the established dialog after ACK completion; an upstream BYE newly arriving after a restart must be routed to the peer, and Redis must hold the complete dialog record. The D10 review record shows a fresh DUM UAS returning 481 for BYE, so the current baseline fails and a pass must not be claimed. |
| REQ-NF-2 | One separate process/failure domain per use case stays unchanged; the Redis checkpoint is an out-of-process data direction and does not merge the two apps. |
| REQ-NF-4 | The checkpoint direction can support the later ISSU state design, but ADR-0023 itself does not prove that rolling upgrade, owner takeover or acceptance of in-flight calls is complete. |
| REQ-F-1 / F-2 / F-5 / F-8 / F-9 / F-11 | Call establishment, the two B2BUA legs, routing information, CANCEL/BYE, in-dialog routing and races remain product SIP behaviour constraints; this ADR only specifies the direction of persisting that state at the designated recovery points, and does not change normal call semantics. |
| REQ-NF-6 | This checkpoint is signaling/dialog/controller data; it does not include RTP, media anchoring or media recovery, and follows the ADR-0004 boundary. |

Requirement semantics are governed by the [product PRD](../requirements/prd.md), and the precise D10 acceptance is governed by the [acceptance test plan](../acceptance/test-plan.md).

File-by-file verification result: the translation [`README.md`](../../apps/translation/README.md) describes future externalization of session state via StateStore; but [`decision.py`](../../apps/translation/src/as_translation/decision.py) is a pure decision function, the [unit tests](../../apps/translation/tests/test_decision.py) verify pure-function behaviour, and [contract replay](../../apps/translation/tests/test_contract_replay.py) only replays decision data — there is currently no translation-specific per-call checkpoint payload or StateStore write. The anti-fraud [`README.md`](../../apps/anti-fraud/README.md) describes the rate-window / reputation externalization direction; the actual [`decision.py`](../../apps/anti-fraud/src/as_anti_fraud/decision.py) receives a read-only `Mapping[str, int]` counters object and only reads it, the [unit tests](../../apps/anti-fraud/tests/test_decision.py) assert the counters are unchanged, and [contract replay](../../apps/anti-fraud/tests/test_contract_replay.py) injects counters from case data. Counters are independent aggregate state, not fields of each dialog; existing app source/tests have no StateStore read/write wiring.

The shared kernel [`as_platform/__init__.py`](../../platform/src/as_platform/__init__.py) only describes/exports the seam; [`state/__init__.py`](../../platform/src/as_platform/state/__init__.py) exports the protocol and implementations; [`store.py`](../../platform/src/as_platform/state/store.py), [`redis_store.py`](../../platform/src/as_platform/state/redis_store.py), [`in_memory.py`](../../platform/src/as_platform/state/in_memory.py) and the [contract tests](../../platform/tests/test_state_store_contract.py) prove that the current store is a generic key-value/TTL seam, and the contract has no two-leg atomic commit, owner fencing or durable commit acknowledgement.

## Conditional Items and Open Risks

| Item | Review opinion / handling in the ADR |
|---|---|
| D10 and UAS rehydrate | The current baseline still fails: a fresh DUM UAS returns 481 for a same-dialog BYE. A recovery adapter must be implemented and BYE routing plus the complete Redis record verified before D10 can be lifted. The narrow UAC `DialogSetId` re-INVITE probe is not complete recovery evidence. |
| early / in-flight phase | Pre-inbound-INVITE checkpoint, outbound INVITE pending/early/provisional, final 2xx waiting for ACK, and pending in-dialog transaction at crash time are all outside the current D10 acceptance and are not guaranteed by this ADR. If the product requires these phases, the requirement and test plan must be extended separately; REQ-NF-1 must not be silently narrowed. |
| Two-leg consistency and fencing | Both legs must be saved/restored as one logical checkpoint, using a monotonic generation/revision, and the old owner that has already been taken over must be fenced off; a half-restored pair must not be allowed to serve calls. The physical Redis representation can be decided later. |
| Durability and callback ordering | Dependent SIP side effects must occur after the durable acknowledgement. SIP callbacks must not block waiting for Redis; without an ack that respects the durability boundary, an asynchronous write must not be called committed, and side effects that depend on that commit must not be executed. The Redis failure model/RPO and error paths are still to be designed and accepted. |
| S-CSCF header extension | Only selected values that will in future pass peer authentication and allowlist validation are permitted, placed in a namespaced/versioned extension; size, retention period and classification must be constrained. Arbitrary SIP messages/all headers must not be stored; duplicate values/ordering are retained only per the approved contract. Do not specify or invent the headers currently in use; for the security boundary see [ADR-0016](../architecture/adr/0016-in-boundary-security.md). |
| ADR-0002 and the requirement boundary | [ADR-0002](../architecture/adr/0002-per-usecase-process-state-redis.md) stays accepted/unchanged; the conflict between the "all session state externalized" wording and the fact that the default DUM UAS/transaction runtime cannot be restored from the currently externalized records remains open. ADR-0023 does not supersede ADR-0002, nor does it modify the PRD/test plan. |

Detailed recovery evidence is governed by the [existing D10 review](d10-state-recovery-gap-review-2026-09-30.md) and the [call state recovery options comparison](../architecture/call-state-recovery-options.md). No new D10 SIP probe was run here; what is reported in this document are the probe records already present in the repository plus the current source-code inspection.

## Sign-off

| Item | Value |
|---|---|
| Technical conclusion | Conditional pass; limited to the direction and boundary completeness of the ADR draft |
| ADR status | `proposed`; registry `draft` |
| D10 / REQ-NF-1 | Fail / unresolved; continues to block |
| Maintainer formal review | Pending |
| Maintainer decision and sign-off | To be filled in |
