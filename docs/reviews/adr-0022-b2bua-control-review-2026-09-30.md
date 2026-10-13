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

# ADR-0022 Technical Review Record

- **Date**: 2026-09-30
- **Reviewer**: GitHub Copilot (AI agent)
- **Conclusion**: conditional technical pass (limited to the responsibility split; D10 fail / unresolved); formal maintainer review and sign-off still pending

## Review Scope and Evidence

Reviewed ADR-0022 with respect to the responsibility split between reSIProcate DUM and the product `CallController`, requirement traceability, evidence boundaries and unresolved gates, and reviewed the user-supplied [`resiprocate-dum-b2bua.md`](../architecture/resiprocate-dum-b2bua.md). Cross-checked the DUM API/state behaviour of reSIProcate 1.14.0 (commit `632e215c2ca9aee5416bfe1808851ea6fa380044`), `BUILD_PYTHON` semantics, the E1 import failure record, the native S1/S4 local self-loop smoke, and the native TLS S1 failure record.

## Findings

- DUM is confined to protocol session/dialog/transaction mechanics; cross-leg semantic mapping and Python decision invocation belong to the product `CallController`, and DUM is not described as a complete product B2BUA.
- Transaction retransmission and timers are not re-implemented, and the non-blocking callback requirement is made explicit.
- The Python/C++ integration approach was not pre-selected; native S1/S4 are recorded only as smoke and do not masquerade as product E1 or requirement acceptance.
- The gap between ADR-0002's externalized-state wording and the REQ-NF-1 hard requirement, on the one hand, and DUM live protocol-object recovery capability, together with the unverified E5 state, is explicitly preserved.
- The user-supplied design notes preserve the responsibility-layering insight, but their examples are not a reliable API contract; the corrected 1.14.0 source facts that must be made explicit are as follows:
	- The two `onNewSession` overloads are `(ClientInviteSessionHandle, OfferAnswerType, const SipMessage&)` and `(ServerInviteSessionHandle, OfferAnswerType, const SipMessage&)`, not the two-argument forms used in the examples; `onProvisional`/`onFailure` are client-session callbacks, `onConnected` has both a client and a generic/server overload, `onTerminated` takes a reason and an optional associated message; there is no `InviteSessionHandler::onCancel`.
	- `makeInviteSession(...)` returns a to-be-sent `shared_ptr<SipMessage>`; the session handle is supplied by the subsequent DUM callback.
	- `ServerInviteSession` has no `cancel()`; on an initial UAS INVITE CANCEL, DUM answers the CANCEL with 200 and the INVITE with 487, and notifies termination with `RemoteCancel`. The controller remains responsible for the opposite UAC leg and for cleanup/race coordination.
	- `InviteSession::end()` is a BYE; `end()` in the client early state also takes the BYE path in this version. The exact cancellation API awaits the adapter spike and race tests and shall not be settled from pseudo-code. DUM has RFC session-timer support, so protocol timers should not be uniformly called application-managed.
	- The two legs are correlated with internal logical call keys/session handles; they cannot be unified into a Call-ID (REQ-F-2).
- At initial review, REQ-F-4 SDP body byte identity still had no on-the-wire evidence; the limited-sample comparison of D11 on 2026-10-01 has passed, but extraction/cloning of `Contents` and the unmodified callback still cannot prove wire identity on the product path. The full adapter, more boundary inputs and the review are unfinished, so REQ-F-4 acceptance remains pending.
- The D9 isolation probes added on 2026-10-01 substantially advanced native bridge feasibility: primitive CPython callback, a real DUM→Python `decide()`→404 (exception becomes 500) and one two-leg 486 branch were all measured. But this is not the product adapter/API; forking, the final-response race and full E1 are still unimplemented/unaccepted. Evidence: `/tmp/as-resip-python-bridge-spike/RESULTS.md`, `/tmp/as-resip-dum-python-slice/RESULTS.md`, `/tmp/as-resip-dum-two-leg-spike/RESULTS.md`.
- The limited native DUM on-wire samples of D11 now pass: the 143/233-byte offer, the 230-byte S1 offer and a distinct 238-byte answer all maintain byte identity between the two legs under test. The earlier S1 230-byte answer happened to be identical to the offer and is not counted as distinct-answer proof on its own. The full adapter, more boundary inputs and the review are still missing, so REQ-F-4 must not be marked as passed. Evidence: `/tmp/as-resip-dum-sdp-spike/RESULTS.md`, `/tmp/as-resip-dum-sdp-roundtrip/RESULTS.md`, `/tmp/as-resip-dum-final-probes/logs/probe-a-final.log`.
- The D10 restart evidence does not support a pass: the UAC `DialogSetId` hook can reconstruct re-INVITE across two processes, but the same-dialog BYE of the default DUM UAS returns 481 in a fresh process; there is no recovery of old transactions or product cross-leg mapping, and no public UAS rehydrate API was found. This result does not prove that a custom extension is impossible. Evidence: `/tmp/as-resip-dum-process-restart/RESULTS.md`, `/tmp/as-resip-dum-uas-restart/RESULTS.md`.
- The single early-CANCEL isolation branch passes, but it does not cover the final-response race or forking: `/tmp/as-resip-dum-final-probes/logs/probe-b-final-isolated.log`. All these spikes live in `/tmp` and are not product acceptance.

## Adjudication

The technical responsibility direction is consistent with the original production stack direction: the reSIProcate C++ selected by ADR-0019 stays unchanged; D9 now has strong feasibility evidence, but the product adapter/API and full E1 are not yet in place. The byte comparison of the limited D11 samples passes, while product REQ-F-4 acceptance is still pending. The D10 conclusion is **fail / unresolved**: the restart test of the same-dialog BYE of the default DUM UAS returns 481 and REQ-NF-1 is unproven; the maintainer must decide between custom UAS recovery/extension plus transaction-behaviour proof, or starting a formal ADR/design review. This conditional technical conclusion does not mean REQ-NF-1 is satisfied, and does not constitute maintainer approval, ADR acceptance, authorization to start coding, a K2 release or release acceptance.

**Maintainer formal review / sign-off: pending**
