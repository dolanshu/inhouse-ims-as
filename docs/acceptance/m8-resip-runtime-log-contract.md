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

# M8 field contract: reSIProcate runtime logs (F8 Phase A)

> REQ-NF-13 forensics mount point: JSON log `timestamp/level/trace_id/call_id/direction/method` + metrics/traces correlation (`test-plan.md` §2).
> Upstream adjudication: [`callload-remediation-adjudication-2026-10-05.md`](../reviews/callload-remediation-adjudication-2026-10-05.md) (F8 `not closed` → becomes `field contract landed` once this contract lands; the C++→Python JSON callback is deferred, see §5).

## 1. Background

The C++ binding (`platform/native/resip_runtime/runtime_module.cxx`) emits `RESIP_RUNTIME_*` behaviour primarily via `cout/cerr`,
and the Python side previously had no structured parsing. This contract freezes the existing `key=value` line format into an assertable field table,
so that REQ-NF-13 assertions have evidence to attach to (a full JSON callback is post-RC work, see §5).

## 2. Field contract table (event → fields → NF-13 mapping)

Parser: `platform/src/as_platform/sip/resip_runtime_log_contract.py`
(`parse_resip_runtime_log_line` / `is_resip_runtime_log_line` / `ResipRuntimeLogEvent.to_nf13_fields`);
tests: `platform/tests/test_resip_runtime_log_contract.py` (`contract` marker, 13 cases).

| event (C++ line location) | fields | NF-13 mapping (`to_nf13_fields`) |
|---|---|---|
| `RESIP_RUNTIME_LISTENING` (`runListener`, udp/tcp/tls three lines) | `address, advertised, udp_port/tcp_port/tls_port` | `level=info`, everything else `None` (no call context) |
| `RESIP_RUNTIME_UAC_INVITE_SENT` (`onNewSession` forwarding) | `outgoing_call_id, inbound_call_id, route_uri` | `call_id/trace_id=outgoing_call_id`, `direction=outbound`, `method=INVITE` |
| `RESIP_RUNTIME_UAC_NEW_SESSION` (`onNewSession` UAC) | `outgoing_call_id` | same as above (`outbound/INVITE`) |
| `RESIP_RUNTIME_UAC_FAILURE` (`onFailure`) | `outgoing_call_id, status` | same as above (`outbound/INVITE`, `level=info`: a downstream failure is a business event) |
| `RESIP_RUNTIME_UAS_FAILURE_MAPPED` (`onFailure` after mapping) | `outgoing_call_id, downstream_status, upstream_status` | same as above (`outbound/INVITE`) |
| `RESIP_RUNTIME_OUTBOUND_CANCEL_FORWARD` (`onTerminated` RemoteCancel) | `inbound_call_id` | `call_id/trace_id=inbound_call_id`, `direction=inbound`, `method=CANCEL` |
| `RESIP_RUNTIME_UAS_ANSWER_RELAYED` (`onAnswer` 200 relay) | `outgoing_call_id` | `outbound/INVITE` |
| `RESIP_RUNTIME_RELOAD_CERTIFICATES` (`runListener`) | `detail=invoked` (the only fixed literal without a `=`) | `level=info`, everything else `None` |
| `*_ERROR / *_CALLBACK_ERROR / *_CORRELATION_MISS / *_WORKER_ERROR` (each `cerr` site) | `message=<single word>` or the corresponding id field; **message lines containing spaces fail closed as format drift (returns `None`)** | `level=error`, `call_id/trace_id` taken from `outgoing_call_id/inbound_call_id` (if present) |

## 3. Example lines

```text
RESIP_RUNTIME_LISTENING address=127.0.0.1 advertised=127.0.0.1 udp_port=5060
RESIP_RUNTIME_UAC_INVITE_SENT outgoing_call_id=out-1@127.0.0.1 inbound_call_id=in-1@127.0.0.1 route_uri=sip:downstream@127.0.0.1:5070
RESIP_RUNTIME_UAC_NEW_SESSION outgoing_call_id=out-1@127.0.0.1
RESIP_RUNTIME_UAC_FAILURE outgoing_call_id=out-1@127.0.0.1 status=486
RESIP_RUNTIME_UAS_FAILURE_MAPPED outgoing_call_id=out-1@127.0.0.1 downstream_status=486 upstream_status=486
RESIP_RUNTIME_OUTBOUND_CANCEL_FORWARD inbound_call_id=in-1@127.0.0.1
RESIP_RUNTIME_UAS_ANSWER_RELAYED outgoing_call_id=out-1@127.0.0.1
```

## 4. JSON enrichment on the Python side

`platform/src/as_platform/sip/resip_runtime.py::emit_native_log_event` (~30 new lines):
parse one native line → fill in `timestamp` (`time.time()`, injectable) via `to_nf13_fields()`,
then `level/trace_id/call_id/direction/method` (`trace_id` can be overridden) → emitted as a
single `json.dumps` line through the `as_platform.sip.resip_runtime.native` logger.
The native line itself does not pass through Python logging, so enrichment happens on the **collection/forwarding side** (capturing the worker console and calling it line by line);
REQ-NF-13 assertions attach to this JSON output, and field stability is guarded by the contract tests (a C++ rename or key change turns them red).

## 5. Relationship to the F8 adjudication

- This contract closes Phase A's F8 requirement (the "C++→Python JSON callback **or** field contract + tests" choice takes the latter).
- The full C++→Python JSON callback (the native side calling the Python log callback directly, with `timestamp/level/trace_id`
  injected natively) is **deferred to post-RC**, to be done if maintainers ask; at that point this contract's event/field table becomes the starting schema for the callback payload.
