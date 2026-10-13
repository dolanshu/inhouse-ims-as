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

# ADR-0005: OTel three signals, backend-neutral, export must never block the call path

- **Status**: accepted
- **Date**: 2026-09-28
- **Decides**: §0 ledger entry 12 — OTel three signals, backend-neutral, export must never block the call path; call traces retain an independent query channel
- **Responds to REQ**: REQ-NF-13, REQ-NF-14

---

## Context

The call path is latency-sensitive. Any synchronous export placed on the call path adds its own cost directly to call setup latency — this is not speculation, but a direct consequence of the blocking model of `ED2.loop()`: `AGENT.md` §5 states explicitly "`ED2.loop()`, or an equivalent blocking event loop, is blocking. Never call blocking operations inside SIP callbacks — including telemetry export. Export runs on its own thread (ADR-0005)." Setting up one call crosses the SIP adapter, call controller, decision modules, and StateStore multiple times; any single network write (especially when the telemetry backend sits on the other side of the customer's machine room, across machine rooms, or across NAT) can amplify millisecond-level jitter into a second-level timeout. Telemetry exists to observe the system; it must never become the reason the system slows down.

The second constraint comes from the delivery form. The product is delivered on-prem into the customer's machine room, and telemetry backends are not uniform across customers: some already have Prometheus + Grafana, some have a vendor's own collection agent, some only have a log platform. Once the product binds to a particular backend in code, it takes the selection away from the customer, and it means every backend change requires a code change and a new release. The **semantics** of observability must be unified; the **backend** must be replaceable.

The third constraint is conceptual, and it is the one most easily confused: call traces and traces are not the same thing. A call trace is the sequence of SIP messages retrieved by Call-ID, used for complaint investigation and ticket forensics; it is a **business query channel** (REQ-NF-7 uses it to replace CDR, see ADR-0017), queried by operations and customer service, with its retention period and query form defined by the business. A trace is **troubleshooting telemetry**, used to answer "on which legs and which network elements did this call spend time, and at which step did it fail", queried by R&D and SRE, with short retention and adjustable sampling. The two can neither substitute for each other nor share the same storage and query entry point: making the trace backend carry complaint forensics would force troubleshooting telemetry to carry business-grade retention and compliance requirements; conversely, making call traces depend on the trace backend would subject business queries to the sampling rate.

`AGENT.md` §13 also gives a red line directly related to telemetry: payload logging is off by default and switchable. Payloads (SIP message bodies, SDP) may contain user identifiers and media addresses; enabled by default equals collecting private data by default.

## Decision

- **All three signals go through the OpenTelemetry SDK.** metrics covers operational metrics such as `active_calls`, `cps`, rule hit rate, and 4xx/5xx rates; traces produce one span chain per call, stringing together multi-leg and cross-network-element call segments; logs are structured JSON, correlated with traces via trace_id / span_id. The three signals share one set of semantic conventions (OTel semantic conventions) and do not each define their own field names.
- **Export never happens on the call path.** The call path only enqueues events into a **bounded queue** (enqueue, non-blocking); an independent background export thread takes events from the queue and exports them in batches. When the queue is full, new events are dropped and a `dropped` counter is incremented. The choice here is explicit: telemetry loss is acceptable; back-pressure on the call path is not.
- **Backend-neutral.** Code depends only on the OTel API and configuration, not on any concrete exporter implementation; the concrete exporter (OTLP / Prometheus / vendor agent) is decided by deployment configuration — changing backend is a configuration change, not a code change.
- **Payload logging is off by default and switchable** (`AGENT.md` §13). When enabled, it likewise goes through the bounded queue and never writes back to the call path.
- **Call traces go through an independent query channel**, not carried by the trace backend. It is organized by Call-ID and decoupled from the telemetry's sampling and retention policies.

## Consequences

### Positive

- **Zero back-pressure on the call path.** The telemetry cost on the call path degrades to a single in-memory enqueue; a slow, hung, or unreachable backend will not propagate into call setup latency.
- **Backends are replaceable.** The collection infrastructure already present in the customer's machine room can be integrated directly, without building a separate stack for the product and without changing product code.
- **Three signals connect troubleshooting.** metrics answers "is something abnormal", traces answers "which segment is abnormal", logs answers "what happened when it was abnormal"; the three correlate through trace context, giving a basis for locating issues across legs and network elements.

### Negative / accepted

- **Telemetry may be lost.** The bounded queue drops when full, and a long backend outage may lose a large amount of data. Accepted: telemetry is a means of observation, not a business fact; the cost of loss is far lower than back-pressuring the call path; and the `dropped` counter itself is a metric that explicitly exposes this loss, so nothing is silently lost.
- **The extra thread and queue introduce a new operational surface.** Queue length, export batch size, and export interval all become objects requiring tuning and monitoring; the background thread itself may also become a failure point (stuck, OOM). Accepted: its failure mode is "telemetry stops", not "calls fail".
- **The three signals introduce new dependencies and prerequisites.** The OTel SDK and its exporters enter the runtime dependency tree; at the same time REQ-NF-14 (alert rule set) takes this ADR's metric semantics as a prerequisite — alert rules cannot be written until metric names and labels are finalized. M5's alerting work therefore depends on this decision landing in M2.

## Alternatives considered

| Option | Why not |
|---|---|
| Synchronous export on the call path | Counts the telemetry export's network latency directly into call setup latency; backend jitter becomes call jitter, backend failure becomes call failure. Directly conflicts with the blocking-model red line in `AGENT.md` §5 |
| Self-built metric reporting | Reinventing the wheel: the semantic conventions, context propagation, sampling, and exporter ecosystem already provided by the SDK would all have to be implemented by hand; and a self-built implementation naturally binds to a particular backend, conflicting with the delivery form |
| metrics only, no traces | Cross-leg, cross-network-element fault localization becomes impossible: metrics can only answer "somewhere 4xx increased", not "where did this call get stuck". The localization needs of complaint cases cannot be met |

## Evidence

- `AGENT.md` §5: "`ED2.loop()`, or an equivalent blocking event loop, is blocking. Never call blocking operations inside SIP callbacks — including telemetry export. Export runs on its own thread (ADR-0005)."
- `AGENT.md` §13: "Payload logging is explicit and switchable; it is off by default in logs."
- PRD REQ-NF-13 (observability three signals), REQ-NF-14 (alert rule set), REQ-NF-7 (call trace query).
- Implementation evidence (bounded queue capacity and drop behavior, export thread independence and isolation verification) to be added after M2 lands.

## Related

- [ADR-0017](0017-no-cdr.md) No CDR — call traces take over its forensics role
- REQ-NF-7 Call traces: a business query channel, not telemetry
- REQ-NF-14 Alert rule set: takes this ADR's metric semantics as a prerequisite
- [`../system-architecture.md`](../system-architecture.md) §0 ledger entry 12
- `AGENT.md` §5 coding conventions, §13 security
