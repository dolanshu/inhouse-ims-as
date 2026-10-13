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

# D10 state recovery design gap review record

- **Review target**: reSIProcate DUM / `SipStack` process-restart recovery path (D10, E5, REQ-NF-1)
- **Date**: 2026-10-01
- **Reviewer**: GitHub Copilot (AI agent)
- **Upstream version**: reSIProcate 1.14.0, commit `632e215c2ca9aee5416bfe1808851ea6fa380044`
- **Conclusion**: **not passed / unresolved; maintainer adjudication required**

## Scope and evidence

This record reviews two isolated two-process restart probes and the boundary of what they prove about the current acceptance of D10/REQ-NF-1. The current baseline follows [`test-plan.md`](../acceptance/test-plan.md): after the basic call completes the ACK exchange, kill/restart the AS, then have the upstream send an in-dialog BYE, verifying that the replacement routes the BYE to the peer and that Redis holds a complete dialog record. This test exercises SIP dialog/control-state continuity; it does not test RTP/media interruption or recovery; the replacement needs to handle a new BYE transaction and does not need to recover an already-completed INVITE transaction. The experiments used uv CPython 3.10.21; all build artifacts and logs are in `/tmp`, and no repository code was modified.

- **UAC DialogSet reconstruction hook**: `/tmp/as-resip-dum-process-restart/RESULTS.md`. Phase A establishes the dialog and then the process exits; Phase B creates a new SipStack+DUM, uses `makeInviteSession(..., DialogSetId, ...)`, manually restores the To-tag, Route, remote target and an incrementing CSeq, and sends an in-dialog re-INVITE under the same Call-ID/tags, receiving 200 and ACK. This result only proves that one UAC DialogSet reconstruction hook is feasible; it does not restore the old `InviteSession` or `SipStack` transactions, and it does not prove recovery of the product `CallController` mapping. The INVITE transaction of the current baseline is already complete after the ACK, so not restoring the old transaction does not constitute a failure of the current gate; the probe does not test RTP/media.
- **UAS same-dialog request**: `/tmp/as-resip-dum-uas-restart/RESULTS.md`. Phase A establishes the UAS dialog and exits after completing 200/ACK; the fresh DUM receives a well-formed same-dialog BYE and actually returns 481. In the corresponding source path, a request carrying a To-tag looks up the DUM private map by `DialogSetId`; when the old dialog set is missing, 481 is returned. No public UAS DialogSet/session rehydrate API was found. This BYE is precisely the request that the current D10 baseline requires the replacement to handle; the 481 makes the SIP dialog/control-state baseline fail. This probe did not verify the complete Redis record and did not test RTP/media.

The UAS probe shows that this restart path fails for the default DUM, but it does not prove that a custom DUM patch/extension is impossible. The 481 is failure evidence for the current established-dialog BYE acceptance, not evidence of media interruption. Neither probe restored the `SipStack` transaction runtime; the current baseline does not require restoring an INVITE transaction already completed by the ACK. Transaction recovery after a process crash during a pending INVITE/CANCEL/final-response/2xx-ACK has not been tested and is an optional extension outside the current scope. Two-leg mapping recovery of the product `CallController` is also unverified; merely storing the business context in Redis does not constitute evidence that these states are recoverable.

## Adjudication and pending decisions

D10 is **not passed / unresolved**, because in the current ACK-established-dialog baseline the replacement's fresh DUM returns 481 for the upstream same-dialog BYE and fails to complete the required BYE peer routing; the complete Redis dialog record was also not verified by the probe. The UAC hook cannot stand in for UAS dialog/session or product cross-leg state recovery. The INVITE/ACK transactions of the current baseline are already complete, so failure to restore the old transaction is not the reason for D10 failing; pending transaction recovery is merely an untested optional extension. REQ-NF-1 keeps its original text and hard acceptance properties; this record does not relax the requirement, does not accept an architectural workaround, and does not replace the reSIProcate stack already selected by ADR-0019. This conclusion concerns only SIP control-state recovery and does not involve RTP/media.

The maintainer must explicitly choose a follow-up path:

1. Design/implement a UAS/dialog and `CallController` recovery mechanism that can satisfy the current ACK-established-dialog BYE/Redis baseline, and verify BYE routing and the complete Redis dialog record per the test plan; or
2. Start a formal ADR/design review to assess the conflict between the existing product architecture and the current established-dialog baseline of REQ-NF-1, and the feasible architectural boundaries. If in-flight INVITE/CANCEL/final-response/2xx-ACK recovery at process crash is to be added, the requirement and test plan must be separately amended/extended and adjudicated by the maintainer; this document does not choose Redis, PostgreSQL or any other recovery store/design.

These two are pending-adjudication options, not accepted solutions. Until the maintainer decision is complete, D10, E5, REQ-NF-1 and the M7/M8 recovery acceptance all remain blocked.

## Sign-off

| Item | Value |
|---|---|
| Review conclusion | not passed / unresolved; maintainer adjudication pending |
| Maintainer decision | to be filled in: custom UAS recovery/extension + transaction proof, or a formal ADR/design review |
| Maintainer sign-off | to be filled in |
