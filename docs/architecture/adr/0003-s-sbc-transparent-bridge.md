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

# ADR-0003: Single ISC access semantics — the S-SBC is a transparent bridge

- **Status**: accepted
- **Date**: 2026-09-28
- **Decides**: §0 decision 10 — IMS position: out-of-network deployment, iFC-trigger, S-SBC transparent bridge → single ISC semantics
- **Responds to REQ**: REQ-F-1, REQ-F-2, REQ-F-3, REQ-F-5, REQ-NF-5

---

## Context

This product is positioned as a **productized third-party IMS Application Server**,
single-tenant on-premises, deployed outside the operator's IMS network
(`AGENT.md` §1). Its trigger path is: S-CSCF triggers the AS per iFC
(initial Filter Criteria, 3GPP TS 24.229), and the message is forwarded out by
the operator's S-SBC (Session-SBC).

The key cognitive correction of architecture document §1.1 is as follows:

- **From the S-CSCF side**: the third-party AS is treated as an **in-network
  AS**. The S-CSCF is completely unaware — it sends the ISC (IMS Service
  Centralization and Continuity) trigger message per iFC, and all headers such as
  the message's Request-URI, Route set, and P-Asserted-Identity look to the
  S-CSCF exactly as if they had been sent to an in-network AS.
- **From the AS side**: the SIP trunk message coming from the S-SBC "is" the one
  sent by the S-CSCF. The AS does not need to recognize "this message came from
  the S-SBC, or it came directly from the S-CSCF" — the two paths are semantically
  equivalent. The S-SBC assumes transparent bridging and topology hiding; it does
  not introduce a second business semantics.

The POC's `s_sbc_mock` simulator already modeled this behavior: forward `:15060`,
return `:15061`, pass the message through verbatim; the message headers received on
the AS side are consistent with those sent directly by the S-CSCF.

The architectural implication of this cognitive correction is: **the AS only needs
to implement one access semantics.** There is no need to write two adaptation
layers, one for the trunk (out-of-network) and one for direct S-CSCF (in-network)
— the two scenarios are the same ISC trigger as seen by the AS.

## Decision

The AS **implements only ISC semantics** (triggered by S-CSCF per iFC); it does
not implement "special out-of-network adaptation". The trunk is only a bearer
layer, not a second business semantics.

`testbed/simulators/` must contain an S-SBC simulator whose baseline behavior is
transparent bridging — it presents "the AS is in-network" to the upstream
(simulated S-CSCF) and "I am the S-CSCF" to the downstream (the AS). All
production access paths must be verified against this simulator as the behavioral
baseline.

## Consequences

### Positive

- **Implementing only one access semantics eliminates the extra complexity of a
  dual-mode adapter.** Supporting "in-network / out-of-network dual mode" would
  require writing two adaptation layers for every SIP message: one handling the
  ISC trigger coming directly from the S-CSCF, another adapting the trunked path
  (including possible number translation, port mapping, signaling-field
  adjustments, etc.). At POC scale this would increase signaling-handling code by
  50%+.
- **The AS needs no special handling for the S-SBC's correct bridging behavior.**
  The AS only recognizes the standard ISC message format; any non-standard
  behavior of the S-SBC belongs to boundary cases the testbed simulator must
  cover, not a special path the AS implementation must adapt to.

### Negative / accepted

- **Depends on the operator's S-SBC correctly performing transparent bridging.**
  If the S-SBC has non-standard behavior (e.g., rewriting certain headers, adding
  extra Routes, or mishandling in-dialog requests), the AS must adapt to those
  boundaries. Mitigation: the S-SBC simulator in `testbed/simulators` must first
  pass comparison against real-behavior captures provided by the S-SBC vendor
  before becoming the baseline; integration verification is done before production
  access.
- **The security boundary needs to be tightened further.** Since the AS side
  believes "the peer is the S-CSCF", the peer authenticity on the S-SBC link must
  be guaranteed by a two-fold TLS + allowlist (ADR-0016); otherwise anyone
  posing as the S-SBC could inject calls.

## Alternatives considered

| Option | Why not |
|---|---|
| In-network / out-of-network dual-mode adaptation | Would write one adaptation layer for each of the trunk and in-network access paths. At POC scale this adds 50%+ to signaling-handling code, and the maintenance cost and consistency risk of two logic sets are unacceptable |
| Bypass the S-SBC and talk directly to the S-CSCF | Not allowed by the operator network boundary design. The S-CSCF does not expose an out-of-network interface; the iFC-triggered ISC message must pass through the S-SBC's topology hiding |

## Evidence

- Architecture document §1.1 completed the IMS network-position analysis and the
  key cognitive correction, clarifying the S-SBC transparent bridge's two-way
  perspective.
- `AGENT.md` §1 defines the positioning explicitly: "triggered by the S-CSCF via
  the operator's S-SBC, which performs transparent bridging".
- The POC's `s_sbc_mock` already models transparent-bridge behavior, passing
  messages through verbatim without introducing business-semantics differences.

## Related

- [`../system-architecture.md`](../system-architecture.md) §1.1 key cognitive correction
- `testbed/simulators/` simulator design — S-SBC transparent-bridge behavioral baseline
- [ADR-0016](0016-in-boundary-security.md) in-boundary security: peer allowlist + end-to-end TLS
