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

# ADR-0021: Evaluation granularity and config schema for runtime overrides

- **Status**: accepted
- **Date**: 2026-09-28
- **Decides**: Open item D7 — evaluation granularity and config schema for runtime overrides
- **Responds to REQ**: REQ-G-1, REQ-NF-10

---

## Context

[ADR-0020](0020-feature-capability-gating.md) splits feature gating into two tiers: ① deployment-level master switch, ② runtime fine-grained override. It decided "whether to layer," but left the **granularity** of tier ② as an open item — the original text's candidates were "number range / call / user / percentage," with no decision on whether to pick one, combine, or what the schema looks like. ADR-0020's review recorded this as a known gap that "must be adjudicated before M4 is complete."

Without fixed granularity, three things cannot land:

1. **The config schema cannot land.** The schema is a direct projection of granularity: if granularity is number range, the field is a prefix; if granularity is user, the field must be a user identifier. With the schema undecided, [ADR-0006](0006-config-governance.md)'s change-order template, console form, and version diff have no object.
2. **Idempotent evaluation cannot be guaranteed.** Tier ② of ADR-0020 has the hard requirement "repeated evaluation of the same decision yields the same result, with no inconsistent pass or repeated flip caused by read jitter within the window" (risk R5, open item D3). This requirement directly constrains "how percentage is computed": any percentage algorithm depending on the clock, random numbers, or stored state could change its answer on repeated evaluation within the Redis split-brain window — effectively leaving idempotency to luck.
3. **Audit has no foothold.** Carrier acceptance will ask "why did this call take the new path" (REQ-NF-10: traceability). With granularity undecided, we cannot answer "by which configuration."

There is also a product premise: this product is a **number-domain AS**, where user identifiers are unavailable — `AGENT.md` §2 explicitly states "no Diameter Sh; data comes from our own data plane." This directly rules out a class of designs that use the user as the criterion.

## Decision

The evaluation granularity for runtime overrides is fixed as: **number prefix (number range) as the first dimension, optionally overlaid with a stable-percentage call split by call**. No "by user," no "persistent per-call override."

**Schema.** One runtime-override entry has five fields:

| Field | Type | Meaning |
|---|---|---|
| `name` | string | The feature name this override entry belongs to |
| `prefix` | string | Number-range prefix, normalized form (isomorphic to `Rule.prefix`); empty string means the whole domain |
| `percent` | int | Integer 0–100, what proportion of calls within the matched prefix |
| `enabled` | bool | Whether enabled; explicit off takes priority over percentage |
| `removal_condition` | string | Removal condition: when to tear down this scaffolding (guard against switch debt, ADR-0020) |

**Matching.** Take override entries with matching `name` and matching prefix, **longest prefix wins** — consistent with the kernel `RuleSet.match` ordering, so ops need only one mental model. An override entry with `enabled` False returns `False`; explicit off takes priority over percentage. When no matching entry is found, return `None` (fail-closed, left to the deployment-level decision), not `True`; this is consistent with `gating.is_enabled` semantics.

**Percentage split must be idempotent.** Use a stable hash of Call-ID, not depending on the clock, random numbers, or stored state:

```text
h = FNV-1a 32-bit(call_id.encode("utf-8"))
hit ⟺ h % 100 < percent
```

Thus the same call lands in the same bucket in any replica, on any repeated evaluation — exactly the idempotency required by the Redis split-brain window (risk R5, open item D3).

**Boundaries.** `percent <= 0` never hits; `percent >= 100` always hits. Values outside 0–100 are clamped to these two boundaries, with no error or exception — no new failure mode is introduced into the evaluation path.

## Consequences

### Positive

- **Evaluation can be done offline.** Evaluation depends only on config and `call_id`, reading no Redis, no clock, no random numbers, so it can be evaluated in-process or previewed offline in the console for the consequence of the same config.
- **Evaluation is idempotent.** Repeated evaluation of the same call yields the same result; the split-brain window will not flip one pass into a reject (the positive answer to risk R5 / open item D3).
- **Evaluation is auditable.** Tracing a call requires only two numbers: `call_id` and the `percent` of the matched prefix. "Why did this call take the new path" has a definite answer.
- **The config schema is isomorphic to rules** (both are "prefix + attribute"), so it reuses [ADR-0006](0006-config-governance.md)'s same governance pipeline: version row, change order, approval, canary distribution, rollback; rules and override entries share one set of semantics, and console and audit have only one model.

### Negative / accepted

- **Percentage split is powerless to "precisely specify one particular call."** This is intentional: to make a specified call take the new path, you must reverse-derive the Call-ID that lands in that bucket, rather than directly naming a call.
- **Different calls within the same prefix behave differently.** The first step in troubleshooting during the canary period is to see which bucket the `call_id` lands in; the intuition "this whole prefix is on" no longer holds, and ops' mental model needs one calibration.
- **The combination of `prefix` and `percent` requires ops understanding.** The behavior produced by multiplying the two fields must be previewed by the console (enter prefix + percentage, show hit/miss examples), otherwise configuration can only be guessed. Console preview is a delivery item of the M4 control plane, not optional.

## Alternatives considered

| Option | Why not |
|---|---|
| By user | This product is a number-domain AS; no Diameter Sh (`AGENT.md` §2 non-goal), so user identifiers are simply unavailable; introducing an Sh interface just to obtain an identifier means bringing in a whole network-element integration for one gating dimension |
| Persistent per-call override | State grows with call volume (one record per call), audit must leave a trace per call, and state in Redis means repeated evaluation within the split-brain window may read a different version — directly violating ADR-0020's idempotency requirement for tier ② (risk R5, open item D3); negative net benefit |
| By time window | Depends on the clock. The same decision evaluated in different replicas at different moments yields different results, breaking idempotency; and clock rollback would suddenly zero or suddenly fully enable the canary scope |
| Random-percentage | Repeated evaluation of the same decision yields different results, directly violating idempotency (risk R5, open item D3). A random number is a tool to "split once," not to "split the same way every time" |

## Evidence

- [ADR-0020](0020-feature-capability-gating.md) lists "evaluation granularity and config schema for runtime overrides" as a known gap (open item D7), and requires adjudication before the M4 control-plane design.
- Risk R5 (Redis becomes a new SPoF) and open item D3 (decision idempotency under Redis split-brain window) require tier ② evaluation to be idempotent, which directly determines that percentage must use a stable Call-ID hash rather than clock or random numbers.
- `AGENT.md` §2 non-goal "no Diameter Sh, data comes from our own data plane" — the by-user granularity is unavailable.
- Implementation evidence (landed in this change): `platform/src/as_platform/gating/overrides.py` provides `RuntimeOverride`, `fnv1a32`, `in_bucket`, `match_override`; `platform/tests/test_gating_overrides.py` (marker `unit`) covers percentage boundaries, repeated-evaluation idempotency, intra-prefix split, `enabled=False` priority, longest-prefix priority, `None` on no match, and hash regression lock-in and purity (no clock read, no socket opened).
- Isomorphism with kernel rules: `as_platform/decision/rules.py`'s `Rule` is already "prefix + attribute," and longest-prefix priority is the existing ordering (REQ-F-6).

## Related

- [ADR-0020](0020-feature-capability-gating.md) layered gating (this ADR adjudicates its tier ②)
- [ADR-0006](0006-config-governance.md) configuration governance: PostgreSQL version store + change-order state machine
- [ADR-0007](0007-data-plane-split.md) data-plane split: Redis stores runtime, PostgreSQL stores governance state
- Risk R5 (Redis becomes a new SPoF)
- Open item D3 (decision idempotency under Redis split-brain window)
- [`../system-architecture.md`](../system-architecture.md) §5.3 Feature enablement
