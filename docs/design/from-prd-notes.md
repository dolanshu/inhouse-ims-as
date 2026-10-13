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

# Technical notes stripped from PRD v0.1

> This file collects all 27 "technical note" sections stripped during the rewrite of `docs/requirements/prd.md` v0.1. These are design hints, not part of the requirements document, but are retained as source material for the M2 design phase.
>
> **Carry-over principle**: carry the original text only, do not modify content. Each item is prefixed with its original location.

---

## REQ-F-* functional requirements

### REQ-F-1

> Stripped from PRD v0.1, original location REQ-F-1 "Technical note" section

The B2BUA pattern splits a call into two independent SIP legs — upstream (to the S-SBC) and downstream (to the peer) — with our business logic in between. This is the B2BUA behavior defined in RFC 3261 §12, not something we invented.

---

### REQ-F-2

> Stripped from PRD v0.1, original location REQ-F-2 "Technical note" section

Different Call-IDs on the two legs and Request-URI rewriting are direct protocol corollaries of the B2BUA pattern, not behaviors we invented.

---

### REQ-F-3

> Stripped from PRD v0.1, original location REQ-F-3 "Technical note" section

Request-URI rewriting happens in the B2BUA state machine's `call_controller` layer; the rewrite rules come from the configured routing policy.

---

### REQ-F-4

> Stripped from PRD v0.1, original location REQ-F-4 "Technical note" section

The media seam retains the interface definition but does not implement production logic; the SDP body is passed through byte-for-byte at the Transport seam.

---

### REQ-F-5

> Stripped from PRD v0.1, original location REQ-F-5 "Technical note" section

Route/Record-Route is the "hop history" of the SIP dialog chain; the production stack (reSIProcate) has built-in handling for this.

---

### REQ-F-6

> Stripped from PRD v0.1, original location REQ-F-6 "Technical note" section

Rule matching executes inside the `decide()` decision function; the match table comes from the rule version delivered by config-service. "No match" is one of the decision function's return cases.

---

### REQ-F-7

> Stripped from PRD v0.1, original location REQ-F-7 "Technical note" section

The "block" policy is another return case of `decide()`, whose return value carries a "reject" verdict; the decision itself is a pure function, independent of the SIP stack.

---

### REQ-F-8

> Stripped from PRD v0.1, original location REQ-F-8 "Technical note" section

CANCEL drives the B2BUA state machine from the Early state into the Terminating state, with the internal `DialogState` marked canceling.

---

### REQ-F-9

> Stripped from PRD v0.1, original location REQ-F-9 "Technical note" section

The POC has chained-topology coverage, but capture_call.py does not run that scenario, so the POC baseline is missing. The production stack reSIProcate has a built-in dialog-matching mechanism, but we must ensure correct routing still holds after dialog state is externalized.

---

### REQ-F-10

> Stripped from PRD v0.1, original location REQ-F-10 "Technical note" section

The POC's ReturnUas only returns 200 OK, so the baseline is missing. The production implementation must branch on non-2xx at the `call_controller` layer and must not hardcode "downstream always succeeds".

---

### REQ-F-11

> Stripped from PRD v0.1, original location REQ-F-11 "Technical note" section

The POC has no explicit race test, so the baseline is missing. The production implementation must maintain a `canceling` state in `DialogState`, set when CANCEL arrives, after which any final response received is handled as "already canceled".

---

## REQ-NF-* non-functional requirements

### REQ-NF-1

> Stripped from PRD v0.1, original location REQ-NF-1 "Technical note" section

The InMemoryStateStore used by the POC loses sessions on restart. The production implementation must use the StateStore seam + Redis externalization, storing session state in Redis (Sentinel redundancy), with process memory used only as a cache.

---

### REQ-NF-2

> Stripped from PRD v0.1, original location REQ-NF-2 "Technical note" section

sippy ships a blocking ED2.loop(), naturally one process per use case. Process boundary = fault-domain boundary = independent canary / scale boundary.

---

### REQ-NF-3

> Stripped from PRD v0.1, original location REQ-NF-3 "Technical note" section

A stateless process (REQ-NF-1) is a hard prerequisite for horizontal scaling. The Redis session table provides affinity fallback, and the LB layer adds `sessionAffinity: ClientIP` as a second safeguard.

---

### REQ-NF-5

> Stripped from PRD v0.1, original location REQ-NF-5 "Technical note" section

This is a direct corollary of the "single ISC semantic" in the §0 product overview. The S-SBC is an operator-side NE, not part of our deliverables; the testbed must include an S-SBC simulator to validate this understanding.

---

### REQ-NF-9

> Stripped from PRD v0.1, original location REQ-NF-9 "Technical note" section

Single-tenant means the Helm chart produces one complete system, with one K8s namespace per customer.

---

### REQ-NF-4

> Stripped from PRD v0.1, original location REQ-NF-4 "Technical note" section

Premise: the production stack's (reSIProcate) SIP transaction/dialog state lives in process memory and cannot be "seamlessly handed over to a new version" — so ISSU can only use draining, not zero-traffic switchover.

---

### REQ-NF-6

> Stripped from PRD v0.1, original location REQ-NF-6 "Technical note" section

The media seam defines the interface only, and does not implement production logic.

---

### REQ-NF-7

> Stripped from PRD v0.1, original location REQ-NF-7 "Technical note" section

The call trace is both an operations signal (to the OTel trace backend) and a product capability (via the AS's own `/api/v1/traces` query channel); the two channels are correlated by the same Call-ID/TraceID.

---

### REQ-NF-8

> Stripped from PRD v0.1, original location REQ-NF-8 "Technical note" section

No LI / IRI / Intercept-related implementation in production code.

---

### REQ-NF-10

> Stripped from PRD v0.1, original location REQ-NF-10 "Technical note" section

Not operations directly UPDATING the database, and not managing configuration with a git repo. Schema versioning + compatibility matrix is a hard prerequisite for ISSU (REQ-NF-4).

---

### REQ-NF-11

> Stripped from PRD v0.1, original location REQ-NF-11 "Technical note" section

Guarded by `tests/test_version_consistency.py`; the gate blocks any commit where VERSION and pyproject drift.

---

### REQ-NF-12

> Stripped from PRD v0.1, original location REQ-NF-12 "Technical note" section

This is the realization of the architecture decision ledger.

---

## REQ-G-* governance requirements

### REQ-G-1

> Stripped from PRD v0.1, original location REQ-G-1 "Technical note" section

Two layers of gating: a deployment-level master switch (PG version store) + runtime fine-grained overrides (Redis, at number-range / call / user / percentage granularity).

---

### REQ-G-2

> Stripped from PRD v0.1, original location REQ-G-2 "Technical note" section

The document chain is defined in AGENT.md §3. The PR checklist must include an "upstream docs updated" item; the review record must tag the corresponding REQ-*.

---

### REQ-G-3

> Stripped from PRD v0.1, original location REQ-G-3 "Technical note" section

Enforced by an AST-scan guard (the scan script under the `tests/` directory) — new code that "violates ADR annotation discipline" is blocked by `make gate-strict`.

---

### REQ-G-4

> Stripped from PRD v0.1, original location REQ-G-4 "Technical note" section

The local gate runs the same four layers (fast → integration → e2e → performance). During M0, the integration/e2e/performance layers have no tests and are not blocking; the milestone that first introduces a test for a layer must simultaneously make that layer blocking.
