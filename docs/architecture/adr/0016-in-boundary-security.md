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

# ADR-0016: In-boundary security — peer allowlist, end-to-end TLS, certificate hot rotation

- **Status**: accepted
- **Date**: 2026-09-28
- **Decides**: §0 ledger item 18 — in-boundary security: peer allowlist, end-to-end TLS, certificate hot rotation, console authentication (console part belongs to M4)
- **Responds to REQ**: REQ-S-1, REQ-S-2, REQ-S-3 (REQ-S-4 console authentication & audit belongs to M4; this ADR records the assignment)

---

## Context

We are deployed **outside** the carrier network (`AGENT.md` §1): the S-CSCF triggers us via the S-SBC; we are not a network element and are not inside the carrier's trusted network. This means the assumption "network location itself provides protection" does not hold — we cannot claim "anything that can reach us is an in-network device," because from our perspective the caller is a peer located on the public Internet or the customer's premises side.

`AGENT.md` §13 is blunt: "The trunk is untrusted. Peers must be validated against an allowlist and terminate TLS end-to-end with the S-SBC — anyone who can impersonate the S-SBC can inject calls (ADR-0016)." The implication of this red line is concrete: as long as someone can impersonate the S-SBC, they can inject arbitrary calls into our AS, thereby triggering arbitrary decision logic, consuming capacity, or even using our AS to place calls to real callees. So ingress validation is not a hardening item but a precondition for correctness.

The good news is that there is only one ingress. The difference between in-network and out-of-network (topology, addressing, SIP header handling) is absorbed by the S-SBC transparent bridge — ADR-0003 already established "single ISC ingress semantics; the S-SBC is a transparent bridge, not a second business semantic." Because there is only one ingress semantic, there is only one place that must be held: **the S-SBC-facing ingress**. This converges the security boundary from "several places each needing separate hardening" into "one place that can be fully described and fully audited."

The same section also gives two constraints directly relevant to implementation. First, certificate rotation: "Certificate rotation is a configuration hot update. Never restart the process, never drop in-flight calls." Under carrier traffic, a process restart dropping in-flight calls is unacceptable, yet certificate lifecycles are far shorter than process lifecycles — the two must be decoupled by hot update. Second, payloads: "Payload logging is explicit and toggleable; it is off by default in logs." And "every console operation must be authenticated and audited."

## Decision

- **Terminate TLS end-to-end toward the S-SBC direction, preferring mTLS (mutual certificate validation).** The transport termination point is the SIP adapter / transport layer; **the decision module is unaware of TLS** (`AGENT.md` §5 requires the decision module to be a pure function with no sockets). TLS handshake and certificate validation belong to transport; the decision logic only sees SIP messages already validated as coming from a trusted peer.
- **Validate the peer allowlist at ingress.** Validation is by source address and/or certificate identity (under mTLS, certificate identity takes precedence); on failure, drop and record a security event (not merely an ordinary log line). Allowlist and certificate are both configuration, so they follow ADR-0006's change pipeline — they carry the same change risk as rules and should not have a lower-tier change path.
- **Certificate hot rotation.** Certificate and allowlist are updated via hot loading: the process does not restart, in-flight calls are unaffected, and new connections use the new certificate. In implementation this reuses the configuration hot-update seam and follows the same path as ADR-0006's canary distribution — swapping a certificate and swapping a rule are the same class of operation and should not have two mechanisms.
- **Payload logging is off by default and toggleable** (`AGENT.md` §13). Enabling it is an explicit, auditable operation, never on by default for troubleshooting convenience.
- **No lawful interception (LI) and no billing.** The former is not this product's function; the latter is explicitly excluded by ADR-0017 and architecture doc §2 non-goals. This ADR does not reserve any collection point for them — reserving a collection point equals reserving the possibility of being asked to enable it.
- **REQ-S-4 (console authentication & audit) lands in the M4 control plane.** This ADR only records its assignment and hard-codes the constraint: **every console operation must be authenticated and audited**.

## Consequences

### Positive

- **Only one ingress, provable boundary.** We can draw the customer a boundary diagram with a single ingress, and audit "what can get in" item by item. This is the only defensible security argument available under an out-of-network deployment.
- **Certificate rotation does not affect in-flight calls.** Once certificate lifecycle is decoupled from process lifecycle, short-lived certificates (and emergency revocation) no longer need coordination with traffic windows.

### Negative / accepted

- **mTLS and certificate lifecycle management are new operational burdens.** Issuance, distribution, expiry monitoring, and revocation all need processes and owners; under on-prem delivery this process must also run at the customer side. Accepted: this is the inherent cost of out-of-network deployment; the alternative (relying on network isolation) is not provable.
- **A misconfigured allowlist causes legit peers to be rejected.** Omitting an allowlist entry when adding an S-SBC node or changing an address shows up as a full call rejection — the failure is explicit and total. Mitigated by canary distribution and rollback (ADR-0006): allowlist changes are the same tier as rule changes, canary-able and rollback-able.
- **TLS termination adds handshake overhead.** Each new connection incurs one handshake cost. Accepted: this is a one-time cost and connections are reusable; it is not on the critical decision path of every call.

## Alternatives considered

| Option | Why not |
|---|---|
| Rely on network-layer isolation | We are deployed out-of-network; isolation cannot be proven to the customer: we cannot argue "only trusted devices can reach us," so we cannot satisfy REQ-S-1's provability requirement |
| IP allowlist only, no TLS | Source addresses are spoofable (and under out-of-network deployment address ownership is not under our control), failing §13's red line "terminate TLS end-to-end with the S-SBC" |
| TLS but no allowlist | Any client holding a valid certificate can inject calls: TLS only proves "the peer has a certificate in our trust chain," not "the peer is the one we expect." mTLS + allowlist are both required |

## Evidence

- `AGENT.md` §13 verbatim: "The trunk is untrusted. Peers must be validated against an allowlist and terminate TLS end-to-end with the S-SBC — anyone who can impersonate the S-SBC can inject calls (ADR-0016)."
- `AGENT.md` §13: "Certificate rotation is a configuration hot update. Never restart the process, never drop in-flight calls." "Payload logging is explicit and toggleable; it is off by default in logs." "Every console operation must be authenticated and audited."
- PRD REQ-S-1, REQ-S-2, REQ-S-3, REQ-S-4.
- [ADR-0003](0003-s-sbc-transparent-bridge.md) establishes the S-SBC as a transparent bridge, so there is only one ingress semantic and only one ingress.

## Related

- [ADR-0003](0003-s-sbc-transparent-bridge.md) single ISC ingress semantic — S-SBC is a transparent bridge
- [ADR-0006](0006-config-governance.md) configuration governance: allowlist and certificate follow the same change pipeline
- ADR-0017 (skeleton, not yet implemented) no CDR, no billing
- `AGENT.md` §13 security, §5 decision module is a pure function
- REQ-S-4 (console authentication & audit) — belongs to M4 control plane
