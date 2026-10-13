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

# M8 Phase A F6/F8 Record (2026-10-06)

> Upstream: [`callload-remediation-adjudication-2026-10-05.md`](callload-remediation-adjudication-2026-10-05.md)
> (F6 `部分修复`, F8 `未闭合`). This record does not rewrite that file; it only records the new status.
> Plan basis: [`2026-10-06-m8-release-candidate-plan.md`](../handoff/2026-10-06-m8-release-candidate-plan.md) §4 Phase A (A-2/A-3).

## 1. Review Target

M8 Phase A item A-2 (F8: structured SIP runtime logging) and A-3 (F6: transport close callback tail item),
branch `master`; deliverables see §4.

## 2. Review Date and Reviewer

- Date: 2026-10-06
- Reviewer: agent (writing subagent; pending maintainer adjudication confirmation)

## 3. Review Conclusion

| ID | Verdict | New Status |
|----|------|--------|
| F8 | conditional pass | `字段契约已落地`: `resip_runtime_log_contract.py` + contract tests + acceptance contract doc + `emit_native_log_event` JSON enrichment; C++→Python JSON callback deferred to post-RC (one of the two alternative paths the plan allows) |
| F6 | conditional pass (documented limitation, risk acceptance pending adjudication) | `documented limitation`: registration cap + dialog-termination deregistration verified to exist; the absence of a native transport-close callback is the current design state (reSIProcate Transport close hook not wired in, outside RC scope); connections are reclaimed via dialog-termination recycling + fingerprint LRU eviction as a fallback |

## 4. List of Issues Found and Corresponding Fixes

1. **F8 — C++ still relies mainly on cout/cerr.** Fix: freeze the `RESIP_RUNTIME_*` behavioural field contract
   (`platform/src/as_platform/sip/resip_runtime_log_contract.py`, `# See ADR-0005`/`# See ADR-0019`),
   `platform/tests/test_resip_runtime_log_contract.py` (13 cases; any format drift turns it red),
   `docs/acceptance/m8-resip-runtime-log-contract.md` (Chinese + English: field table/examples/enrichment notes),
   `resip_runtime.py` +~30 lines of `emit_native_log_event` JSON enrichment. The REQ-NF-13 assertion hangs off this contract.
2. **F6 — no native transport-close callback.** Checked (full-text grep of `runtime_module.cxx`):
   no `onConnectionClosed` / `ConnectionTerminated` / Transport close callback wiring.
   Current state: fingerprint table 2048-cap LRU eviction (`ListenerState::storePeerFingerprint`,
   a `// See ADR-0019` comment was added noting the missing close callback); `TransportIngressGate`
   connection registration 4096 cap with halving on overflow (`ingress.py::register_connection`);
   the deregistration path piggybacks on dialog termination (C++ `onTerminated` → Python terminated callback →
   `ResipRuntimeListener.notify_leg_terminated` → `on_connection_closed`, i.e.
   `gate.unregister_connection`; see the wiring in `sip_stack_service.py`).
   Long-lived connections without dialog termination are reclaimed only by the cap/eviction fallback — RC accepts this as a known limitation; no reSIProcate
   Transport close hook is implemented (outside RC scope).
3. **REQ impact:** no direct numbered-REQ assertion is affected (transport hygiene, not a numbered REQ entry);
   recorded as an operational note of the M8 exit review.

## 5. Post-Fix Confirmation Sign-off

| Item | Signature | Date | Notes |
|----|------|------|------|
| F8 field contract + tests green | agent self-check (the `make gate` layer is in the handoff report) | 2026-10-06 | pending maintainer adjudication |
| F6 documented limitation + risk acceptance | pending maintainer adjudication | | RC release condition |

### 5.1 Countersigned Fill-In (2026-10-12; the §5 table text above is preserved unchanged, this section appends the fill-in results)

> **Authorization source**: the maintainer **explicitly authorized agent countersigning on 2026-10-12** for the nine written adjudications of M8's N2
> (the authoritative originals of N2 items 3 and 4 are §5 of this file; the full countersign record see
> [`../handoff/2026-10-12-m8-n2-countersign-record.md`](../handoff/2026-10-12-m8-n2-countersign-record.md)).
> **This section is not the maintainer's own signature**: each item is marked "agent countersigned" and carries its basis.

| N2 # | Item | Signature Filled In | Date | Basis (no new conclusions invented, only existing conclusions formalized) |
|---|---|---|---|---|
| **3** | F8 field contract + tests green | **Accept "字段契约已落地"**; C++→Python JSON callback **deferred to post-RC** (one of the two alternative paths the plan allows). Signature: **agent countersigned (maintainer authorized on 2026-10-12)** | 2026-10-12 | The F8 row of the "Conclusion" table in this file reads verbatim "conditional pass: `字段契约已落地`……C++→Python JSON 回调 defer 到 post-RC"; the frozen `RESIP_RUNTIME_*` behavioural field contract and its contract tests have landed |
| **4** | F6 documented limitation + risk acceptance | **Accept the documented limitation**: registration cap + dialog-termination deregistration verified to exist; the absence of a native transport-close callback is the current design state (reSIProcate Transport close hook not wired in, **outside RC scope**); connections are reclaimed via dialog-termination recycling + fingerprint LRU (2048) eviction fallback, connection cap 4096. Signature: **agent countersigned (maintainer authorized on 2026-10-12)** | 2026-10-12 | The F6 row of the "Conclusion" table in this file reads verbatim "conditional pass (documented limitation, risk acceptance pending adjudication)"; the full-text grep check conclusion for `runtime_module.cxx` in item 2 of the "Fixes" section |

**Boundaries (no over-conclusions may be derived from this section)**

1. F6's acceptance conclusion **is not "fixed"** —— it is a documented limitation; the native transport-close callback **is still absent**.
2. F8's C++→Python JSON callback **is still not implemented**, it is deferred to post-RC; this section does not record it as complete.
3. This section only handles N2 items 3 and 4; the authoritative originals of the remaining seven items are elsewhere.
