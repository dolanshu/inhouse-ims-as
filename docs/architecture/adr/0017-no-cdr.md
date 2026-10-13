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

# ADR-0017: No CDR — replaced by call trail

- **Status**: accepted
- **Date**: 2026-09-30
- **Decides**: §0 ledger item 4 — users and scenarios: no CDR, replaced by a Call-ID-based call trail
- **Responds to REQ**: REQ-NF-7, REQ-NF-13

---

## Context

`AGENT.md` §2 lists "no CDR" as a non-goal: **"No CDR. No collection, no delivery, no archival, no rating. Replace it with a Call-ID-based call trail, for complaint tracing and anti-fraud evidence (ADR-0017)."** The four verbs (collection, delivery, archival, rating) cover the full lifecycle of a call detail record, while "replace it with a call trail" simultaneously rules out a misunderstanding: no CDR does not mean no evidence retained.

A CDR is not a single feature but an entire system. For one call to become a usable record, it must go through collection (pulling events from network elements), delivery (reliably reaching the billing domain — no loss, no duplication), archival (stored by retention period, queryable), rating (computing money by tariff), and inter-carrier settlement (reconciling and apportioning with other carriers). Of these five stages, the last two already go beyond "recording what happened" and straight into money. The carrier in-network system is an existing, audit- and reconciliation-validated capability; for an out-of-network third-party AS to rebuild it, the problem is not the workload but two points: **overstepping** (the billing domain is not our function — ADR-0016 already wrote "no billing" into the security boundary: do not reserve any collection point for it), and **reconciliation risk** (two records from the same source inevitably must answer "which one is authoritative," and every extra fact source adds a class of unreconcilable disputes whose cost far exceeds the convenience it brings). Architecture doc §7 writes this as an explicit deletion: "**Explicitly not done**: CDR collection, CDR delivery channel, CDR archival storage — no billing out-of-network"; the module list's "messaging module" (originally CDR delivery) is marked for deletion directly.

But what this non-goal blocks is only the CDR form, not the need it carries. Complaint tracing and anti-fraud evidence genuinely need to answer "what happened on this call": a user complains that a number range was rejected (PRD US-3 scenario: an operator enters a Call-ID in the console and sees INVITE → 603 Decline and the effective blocking policy); anti-fraud handling needs to explain "why this call was judged fraudulent." The queryers for this need are ops, customer service, and compliance staff; the query key is Call-ID and the query result is "every SIP message of this call." It must be satisfied — just not in the form of a call detail record.

There is also an easily-confused distinction that ADR-0005 has already separated: **a call trail and a trace are not the same thing.** A trace is **troubleshooting telemetry** — answering "on which legs, which network elements did this call spend how long, where did it fail," queried by R&D and SRE, with a short retention and tunable sampling. A call trail is a **business query channel**, queried by ops and customer service, with retention and query shape defined by business and compliance. The two must not substitute for each other, nor share the same storage and query entry: making the trace backend bear complaint forensics would force troubleshooting telemetry to carry business-level retention and compliance requirements; conversely making the call trail depend on the trace backend would subject the integrity and retention the evidence needs to the sampling rate.

## Decision

- **① Do not collect CDR, do not deliver, do not archive, do not rate.** None of these four actions are performed, and no collection point is reserved for them (ADR-0016's principle: reserving a collection point equals reserving the possibility of being asked to enable it). No billing out-of-network, no exception channel.
- **② Replace it with a Call-ID-based call trail.** Every SIP message — inbound/outbound direction, timestamp, method, response code — is queryable via the console, for complaint tracing and anti-fraud evidence. The query key is Call-ID (`REQ-F-13` trail query). This is a **per-message record**, not an aggregate metric and not a sampled sample: the evidence requires "what exactly happened on this call."
- **③ A call trail is not a call detail record — this distinction must be declared explicitly in docs and code.** A trail has no delivery channel, does no rating, and does no inter-carrier settlement. The declaration's purpose is to prevent it from being treated as a billing data source downstream: once someone starts reconciling against it, it in fact becomes a second CDR, and it has not and does not intend to carry the delivery and settlement semantics of a record. Architecture doc §7's table already marks the "call trail" row "ops/evidence data, **not a record**"; this ADR requires that this marking hold at the code and interface level too.
- **④ Trail retention period is open item O4; until decided, no default value may be hard-coded.** The retention period is determined by **customer compliance requirements** (`docs/plan.md` §5.1 O4: call-trail retention period / M4 / customer compliance requirement). PRD REQ-NF-7 states "trail retention period pending — determined by customer compliance requirements, frozen at the M4 design stage. The cleanup task is already formalized as a feature, but the default value is undecided." **The mechanism (cleanup task exists, configurable) lands first; the value does not** — writing a default value would be answering a compliance question on the customer's behalf.
- **⑤ Trail and telemetry trace are separated (ADR-0005).** The trail is a business query channel, the trace is troubleshooting telemetry; the two do not share storage or sampling strategy. They are correlated by the same Call-ID / TraceID so troubleshooting can jump between them, but the query entry and retention policy are independent — the trail query capability must not depend on whether the customer has deployed a trace backend.

## Consequences

### Positive

- **Clear delivery boundary, no intrusion into the carrier billing domain.** No collection, no delivery, no rating means no "which record is authoritative" dispute. Billing remains the in-network existing capability's responsibility.
- **The complaint-tracing and anti-fraud-evidence needs are still met.** The per-message Call-ID trail answers exactly the questions those two scenarios ask (US-3: complain number range rejected → see INVITE → 603 Decline and effective policy). What is excluded is the record form, not the evidence itself.
- **No need to build a message-delivery pipeline for CDR.** The architecture doc module list's "messaging module" (CDR delivery) is deleted directly; an entire class of engineering problems — delivery reliability, deduplication, reconciliation — disappears.
- **Separating trail and trace makes each side's retention policy independent.** Troubleshooting telemetry can have short retention and sampling; evidence data is retained per compliance. They do not constrain each other.

### Negative / accepted

- **Cannot provide billing / reconciliation data — intentionally not done.** Any "while we're at it, emit a record" request must return to this ADR and §2 non-goals for re-adjudication, not add an export in the implementation. This is a capability gap, not a to-do: it is exactly the fulfillment of the "no overstepping" judgment.
- **Undecided retention brings storage and compliance uncertainty (open item O4).** Retention directly determines storage capacity and cleanup-task behavior; until customer compliance requirements are clear, capacity planning and cleanup strategy cannot be finalized. Accepted: mechanism first, value pending, is safer than writing a default that may violate customer compliance requirements. O4 belongs to M4.
- **Trail storage selection undecided (open item D5).** `docs/plan.md` §5.2 D5: whether call-trail storage uses PostgreSQL or a separate short-retention store — belongs to M4, related to O4. Before the retention period (O4) is set, storage selection lacks a key input, so this ADR does not adjudicate the selection.
- **The trail is a per-message full record, scaling with traffic.** Unlike a trace, which can be diluted by sampling, the evidence requires completeness, so trail data has no sampling as a reduction lever. The pressure on storage and cleanup must be jointly borne by the retention period (O4) and the selection (D5); while both are undecided this pressure is unquantifiable.

## Alternatives considered

| Option | Why not |
|---|---|
| Full CDR (collection + delivery + archival + rating) | Overstepping: the billing domain is not an out-of-network third-party AS's function (ADR-0016 no billing); rebuilding an existing carrier in-network capability; and introducing a second record fact source = reconciliation risk |
| Just write logs, no query channel | Complaint tracing needs a **structured Call-ID query**: ops and customer service want to enter a Call-ID and see the full message sequence of that call, not grep logs by time. Logs also lack their own retention and compliance semantics |
| Use trace as the trail | Sampling and short retention fail the evidence requirement: evidence needs "what exactly happened," sampling drops messages, short retention expires them. ADR-0005 already distinguishes the two, and trail query cannot depend on whether the customer deployed a trace backend |
| Record in CDR format but don't deliver ("just keep a record-shaped file") | Form is a promise: once the artifact looks like a record, downstream will use it as a record (reconciliation, settlement), yet it lacks delivery and settlement semantics. This is exactly why Decision ③ requires explicitly declaring "not a record" |

## Evidence

- `AGENT.md` §2 non-goals verbatim: "No CDR. No collection, no delivery, no archival, no rating. Replace it with a Call-ID-based call trail, for complaint tracing and anti-fraud evidence (ADR-0017)."
- PRD REQ-NF-7 (no CDR — replace with call trail) verbatim: "Do not collect billing records, do not deliver CDR, do not archive or rate CDR. Replace CDR with a **call trail** by Call-ID — every SIP message (in/out/timestamp/method/response code) is queryable via the console, for complaint tracing and anti-fraud evidence. A call trail is not a record: it has no delivery channel, does no rating, does no inter-carrier settlement. Trail retention period pending — determined by customer compliance requirements, frozen at the M4 design stage. The cleanup task is already formalized as a feature, but the default value is undecided."
- PRD REQ-NF-13 (OTel three-signal export) verbatim: "Export OpenTelemetry three signals: metrics (active_calls, cps, rule match rate, 4xx/5xx rate), traces (the complete span chain per call), logs (structured JSON logs). Metrics are consumable by Prometheus/Grafana." — the three signals are troubleshooting telemetry, on a separate channel from the trail (ADR-0005).
- PRD §1 non-goals condensed: "No CDR (billing record)"; same section notes "the following non-goals are formalized as REQ-NF-*/REQ-S-*: no media (REQ-NF-6), no CDR (REQ-NF-7)…". US-3 scenario: "an operator enters a Call-ID in the console and sees: INVITE → 603 Decline, with the corresponding configured blocking policy taking effect," corresponding to REQ-F-13 (trail query) and REQ-NF-7.
- Open items O4 (call-trail retention period / M4 / customer compliance requirement) and D5 (call-trail storage: PostgreSQL or a separate short-retention store / M4 / related to O4) — see `docs/plan.md` §5.1 and §5.2.
- Architecture doc §2 table: "call-trail record ① + ⑤ CDR replacement: queryable by Call-ID, for complaint tracing and anti-fraud evidence (not a record, no delivery channel, no rating)"; §7 storage table: "call trail / per-message record by Call-ID / short-term persistence (configurable retention) / ops-evidence data, **not a record**," with "**Explicitly not done**: CDR collection, CDR delivery channel, CDR archival storage — no billing out-of-network."
- ADR-0005 §Context already distinguishes trail from trace: "A call trail is the SIP message sequence queried by Call-ID, for complaint tracing and ticket forensics; it is a **business query channel** (REQ-NF-7 uses it to replace CDR, see ADR-0017)… a trace is **troubleshooting telemetry**… the two must not substitute for each other, nor share the same storage and query entry."
- Implementation evidence (trail storage and the `/api/v1/traces` query channel) lands at the M4 control-plane design stage, adjudicated together with O4 / D5.

## Related

- [ADR-0005](0005-observability-otel.md) three telemetry signals: trail is the business query channel, trace is troubleshooting telemetry, the two are separated
- [ADR-0016](0016-in-boundary-security.md) in-boundary security: no billing, no collection point reserved for it
- PRD REQ-NF-7 (no CDR — replace with call trail), REQ-F-13 (trail query)
- Open items O4 (call-trail retention period, M4), D5 (call-trail storage selection, M4) — see [`../../plan.md`](../../plan.md) §5
- [`../system-architecture.md`](../system-architecture.md) §2 module division and §7 data plane: call trail is not a record
