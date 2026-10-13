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

# M2 P2c resip runtime adjudication (2026-10-05)

> **Subject:** M2 handoff **P2c** — product-path reSIProcate listener → `TransportIngressGate` + `decide()`  
> **Prior review:** [`m2-p2c-resip-runtime-review-2026-10-05.md`](m2-p2c-resip-runtime-review-2026-10-05.md)  
> **Authority:** [`handoff/2026-10-04-m2.md`](../handoff/2026-10-04-m2.md) P2; [`m2-task-register-2026-10-05.md`](m2-task-register-2026-10-05.md)

## Adjudication

| Item | Verdict |
|------|---------|
| `platform/native/resip_runtime` + `ResipRuntimeListener` + integration test | **Accept** (engineering slice) |
| Full P2 TCP/TLS/mTLS on product transport | **Open** |
| P3 dual-cert overlap on product path | **Open** |
| Maintainer sign-off on P2c | **Pending** |
| M2 milestone closure | **Deny** — P2 remainder, P3–P4 incomplete |

## Rationale

P2c records the **authorized product binding shape**: native DUM ingress invokes Python at
`on_invite`, which enforces `TransportIngressGate` then pure `decide()` on
`SipRequestView` fields. It does not accept REQ-S or production trunk evidence.

## Limits

Native extension build is optional for `make gate`; integration evidence requires local
`make m2-platform-resip-build`.

## Sign-off

- Engineering adjudication recorded: 2026-10-05  
- Maintainer sign-off: **pending**
