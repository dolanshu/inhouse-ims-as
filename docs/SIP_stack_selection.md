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

# Open-Source SIP Protocol Stack Selection Comparison (against sippy)

> ⚠️ **Status update (2026-09-27)**: the conclusion of this document's "Judgment for the SIP AS POC" section is
> **"do not replace sippy", and that conclusion has been overturned by a maintainer ruling** — production SIP stack selection is reopened in full,
> sippy exits the production stack and is retained only as a POC behavioural baseline reference.
> The formal decision is in [`architecture/adr/0019-sip-stack-selection.md`](architecture/adr/0019-sip-stack-selection.md) (draft).
> This document's candidate list, licence red lines and layering perspective remain the **evaluation inputs** for ADR-0019 and stay valid;
> for capacity magnitudes see [`architecture/capacity-estimate.md`](architecture/capacity-estimate.md) (conclusion: capacity is not a differentiator).
> This document was written in the POC phase (`../3rtparty_AS_POC`); the original text is retained rather than rewritten.

## Baseline: what sippy is

**sippy** (Sippy Labs / sobomax, BSD-2-Clause) is a pure-Python RFC3261 stack + Back-to-Back User Agent (B2BUA).

- Unlike a SIP proxy, where the proxy maintains only **transaction state**, sippy maintains **full call state** and takes part in every call request. Therefore it can do things a proxy cannot — precise billing, prepaid charging and deduction, failover routing, and so on.
- Unlike a PBX such as Asterisk, sippy **does no media relay or processing at all**, and therefore introduces no extra packet loss, latency or jitter into the media path.
- Stated performance: 5,000–10,000 concurrent sessions on a single host; 150–400 call setups/teardowns per second.
- Ecosystem: supports an RFC7118-compatible secure websocket (wss) interface for WebRTC; can work with **sippy RTPProxy** for media relay; supports Cisco-compatible RADIUS AAA; can be combined with OpenSIPS / SER into a complete softswitch.
- There is also the official Go port **`go-b2bua`**.
- Licence: BSD-2-Clause (the `b2bua` repository) / BSD (the `sippy` package on PyPI is marked BSD).

> ⚠️ Commonly confused, and excluded: **SIPp** is a SIP traffic generator / load-testing tool (XML scenario scripts, simulating UAC/UAS), **not a protocol stack**; it is not the same kind of thing as sippy.

---

## Layered perspective: bare stack / server platform / application framework

Separating these three layers first decides the direction far better than a plain list of names:

1. **Pure signalling stack**: a library; you write the business logic yourself (sippy sits in this layer)
2. **Server platform**: a finished service, expressing routing and business through configuration or scripts
3. **Application framework layer**: a programming framework above the stack, the fastest route to something working

---

## I. Pure signalling stacks (directly comparable to sippy)

| Stack | Language / licence | Core characteristics | Best fit |
|---|---|---|---|
| **PJSIP** (pjproject) | C / GPLv2 or commercial dual licence | Signalling + **media** full stack (PJMEDIA codecs, PJNATH STUN/TURN/ICE); footprint < 200KB; cross-platform to an extreme degree; official SWIG bindings for Python / Java / C# | UAs that need media capability, embedded terminals; the most complete documentation and examples |
| **Sofia-SIP** | C / LGPL | From Nokia Research Center, event-driven, a single `nua` API; **the foundation of both FreeSWITCH and Flexisip** | Where RFC3261 rigour, pure signalling and lightness are wanted; downside: you must understand SIP before you can use `nua` well, so the barrier is higher than with DUM |
| **reSIProcate** | C++ / Vovida (BSD-like) | Three-layer API (low-level / DUM / recon); ships with the **repro** proxy + registrar + web management; used by CounterPath commercial products and Sipwise NGCP | Server-side, commercially friendly licensing; note that its TCP/TLS transport implementation is a relative weak point |
| **Belle-SIP** | C / GPLv3 or commercial | The signalling layer of Linphone; adopts the RFC6026 updated transaction state machine; **fully asynchronous transport layer** (UDP/TCP/TLS + DNS SRV/AAAA); complete dual-stack IPv6; the `refresher` object provides network-outage recovery and automatic refresh | Modern C projects, mobile; the repository has been merged into `linphone-sdk` |
| **libre + baresip** | C / **BSD-3-Clause** | creytiv lineage, asynchronous I/O, low memory footprint; a full modular set covering SIP/SDP/RTP/SRTP/STUN-TURN-ICE/WebSocket | Where you want to avoid GPL but still need industrial-grade quality; still releasing frequently in 2025 (libre 4.3.0 / baresip 4.2+) |
| **oSIP + eXosip2** | C / GPL(eXosip) + LGPL(oSIP) | One of the earliest open-source stacks, a few hundred KB, an extremely minimal API | Learning / experimentation, tiny embedded targets; GPL is a commercial obstacle and activity is now low |
| **rsipstack** | **Rust / MIT** | Strict four-layer architecture (transport / transaction / dialog / app); tokio async; UDP/TCP/TLS/WebSocket; built-in digest auth (MD5/SHA-256/SHA-512) and registration refresh | New projects writing an SBC / proxy / registrar in Rust |
| **Doubango** | C / GPLv3 | The only IMS stack implemented per **3GPP TS 24.229** (IMS-AKA, SigComp, IPsec, ENUM, SMS over IP) | ⚠️ **Development stopped around 2016**; the original vendor moved to AI vision, so it is not recommended for new projects |

---

## II. Server platforms (not bare stacks, but usable as the foundation for an AS)

- **Kamailio** (C / GPLv2+): a routing engine. **KEMI allows routing logic to be written directly in Python / Lua / JS / Ruby** — one of the least-effort paths for an AS POC. v6.0.0 (2025-01) added five modules, including a multi-threaded UDP receive mode, port-range listening, a cmake build, and http2 client/server.
- **OpenSIPS** (C / GPL): split from the same lineage as Kamailio (a fork of SER/OpenSER in 2008) and went its own way. Its **native B2BUA module is more complete than Kamailio's**, suitable for billing, dynamic routing and IMS component scenarios; the current stable branch is 3.6.
- **FreeSWITCH**: B2BUA + full media stack (transcoding / IVR / conferencing / recording / WebRTC), with Sofia-SIP as its foundation.
- **Flexisip** (C++20, AGPLv3 or commercial licence): Belledonne's suite of proxy + presence + conference + B2BUA, built on a **forked Sofia-SIP** (with only a few maintenance patches applied).

> **Core distinction**: Kamailio / OpenSIPS are **proxies** — they never touch media and they are about CPS; FreeSWITCH / Asterisk are **B2BUAs** — they terminate calls and anchor media. When building an AS the usual shape is "the proxy in front absorbing registration and routing, the B2BUA behind doing the business".

---

## III. Application framework layer (the fastest route to a working AS skeleton)

- **drachtio** (MIT): **a C++ Sofia core (drachtio-server) plus a Node.js framework (drachtio-srf)**. Express-style middleware `srf.invite / register / options / subscribe`; a single `createB2BUA` directly establishes a paired UAS + UAC leg, with media handed to rtpengine. Still receiving active commits in 2026. The fastest path for rapidly validating AS logic in TypeScript.
- **JAIN-SIP** (NIST jsip, public domain): Java, the **JSR-32 reference implementation**, a Listener/Provider event model, ships with a TCK, and a parser that passes SIPPING torture tests. But NIST explicitly disclaims ongoing support, so its positioning is closer to experimental.
- **SIP.js / JsSIP**: browser-side, SIP over WebSocket + WebRTC, working with Kamailio / Asterisk / OverSIP.

---

## Judgment for the SIP AS POC

**sippy itself is already a very well-matched choice; replacing it is not recommended.** Reasons:

1. B2BUA semantics are naturally the shape of an AS — it has to maintain call state, rewrite SDP and insert business logic;
2. The BSD-2 licence is clean;
3. Python lets you spend your effort on business logic rather than protocol details;
4. At POC stage, not doing media relay is actually an advantage; when media is needed, attach sippy RTPProxy on demand.

### Three trigger points that would justify switching

| Trigger point | Recommended route |
|---|---|
| Concurrency / CPS hits a wall (sippy single-process 150–400 CPS) | Go straight to the official `go-b2bua` — same author, same design, lowest migration cost |
| Media capability is needed (playback, transcoding, recording, DTMF) | Do not wire up media yourself: sippy + RTPProxy, or a Kamailio / OpenSIPS + FreeSWITCH layering |
| IMS interoperability and compliance need to be validated | Use **SIPp** to load-test your own AS, and use Kamailio's IMS modules as a comparison reference |

### Commercial licence red lines

If this is to go commercial later, watch the copyleft constraints:

- Requires attention (GPL / AGPL or dual licensing; commercial use usually requires purchasing a licence): **PJSIP**, **Flexisip / Belle-SIP** (GPLv3 / AGPLv3), **Kamailio** (GPLv2+), **Sofia-SIP** (LGPL), **oSIP/eXosip** (GPL)
- Friendliest to closed source: **sippy (BSD-2)**, **libre / baresip (BSD-3)**, **reSIProcate**, **rsipstack (MIT)**, **drachtio (MIT)**

---

## Appendix: two decision variables still to be confirmed

1. Where the AS sits in the IMS architecture — an application server behind the S-CSCF, or a standalone fronted B2BUA?
2. Whether media needs to be handled at all?

These two answers directly determine which of the routes above should be taken.
