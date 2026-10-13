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

# M2 P3 TLS overlap adjudication (2026-10-05)

> **Subject:** M2 handoff **P3** (partial) — REQ-S-3 overlap policy on product ingress seam  
> **Prior review:** [`m2-p3-tls-rotation-review-2026-10-05.md`](m2-p3-tls-rotation-review-2026-10-05.md) (**Pass** for P3 slice only)  
> **Authority:** [`handoff/2026-10-04-m2.md`](../handoff/2026-10-04-m2.md) P3; [`m2-task-register-2026-10-05.md`](m2-task-register-2026-10-05.md)

## Adjudication

| Item | Verdict |
|------|---------|
| `TlsRotationState` + `TransportIngressGate.install_with_overlap` + unit tests | **Accept** |
| Native `reload_certificates` on overlap start (P2c UDP runtime) | **Accept** |
| Full REQ-S-3 acceptance (test-plan §3 all bullets) | **Open** |
| Active-call / dual-cert wire proof on product TLS transport | **Open** |
| Maintainer sign-off on P3 | **Pending** |
| M2 milestone closure | **Deny** — P3 partial; P2 TLS product path and P4 remain open |

## Rationale

The review recorded **Pass** for overlap **policy** and the reload **request path**. Accepting this
slice authorizes bindings to pass stable `connection_id` tokens, call `register_connection` at accept,
and use `install_with_overlap` when config service publishes new TLS material. It does **not** accept
REQ-S-3 or close M2.

## Limits

Not REQ acceptance, not operator PKI/S-SBC evidence, not deployment certification unless separately recorded.

## Sign-off

- Engineering adjudication recorded: 2026-10-05  
- Maintainer sign-off: **pending**
