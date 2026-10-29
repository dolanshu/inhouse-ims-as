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

# ADR register

The architecture decision records for `3rdparty-as`. The design they record is
[`../system-architecture.md`](../system-architecture.md); the table below maps each confirmed decision in that document's §0 ledger
to the ADR that carries its context, consequences, and accepted gaps.

**Status legend** —— `skeleton`: decision confirmed but the ADR is not yet written; `draft`: written, not reviewed;
`accepted`: reviewed and binding; `superseded-in-part`: some premises overturned by a newer ADR, framework still valid.

ADRs are written **together with** the change they authorize, never retroactively or in a final bulk catch-up. A decision without an ADR is a decision that must be re-argued.

> **Note (2026-10-29)**: the product source layout now lives under `src/` (`platform/`, `apps/`, `services/` moved one level down to `src/platform/`, `src/apps/`, `src/services/`); ADR body directory references predate this move and are preserved verbatim as accepted records.

## Register

| ADR | Decision | §0 | Status |
|---|---|---|---|
| [0000](0000-adr-template.md) | The template used by every ADR below | — | accepted |
| [0001](0001-monorepo-uv-workspace.md) | Single monorepo + uv workspace; POC and `as_platform` merged in | 3 | accepted ✓ |
| [0002](0002-per-usecase-process-state-redis.md) | Runtime model: one process per use case, state externalized to Redis | 2 | accepted ✓ |
| [0003](0003-s-sbc-transparent-bridge.md) | Single ISC ingress semantics —— S-SBC is a transparent bridge, not a second business semantic | 10 | accepted ✓ |
| [0004](0004-media-seam.md) | Do not do media; keep a media seam and write down its trigger conditions | 11 | accepted ✓ |
| [0005](0005-observability-otel.md) | OTel three signals, backend-neutral, export must never block the call path; call traces keep an independent query channel | 12 | accepted ✓ |
| [0006](0006-config-governance.md) | Configuration governance: PostgreSQL version store + change-order state machine, not GitOps | 13 | accepted ✓ |
| [0007](0007-data-plane-split.md) | Data-plane split: Redis for runtime state, PostgreSQL for governance state | 14 | accepted ✓ |
| [0008](0008-redundancy.md) | Redundancy: intra-site N+1 no single point; cross-site 1+1 warm standby, not active-active | 7 | accepted ✓ |
| [0009](0009-issu-draining.md) | ISSU is draining, not in-flight state migration | §6.2 | accepted ✓ |
| [0010](0010-autoscaling-hpa-downscale-guard.md) | Scaling: custom-metric HPA + scale-down guard controller | 15 | accepted ✓ |
| 0011 | ~~SIP stack: dual stack, `sippy` for production, `go-b2bua` pilot~~ **stack premise overturned by ADR-0019**: sippy exits production stack; dual-stack parallel framework still valid | 8 | superseded-in-part |
| [0012](0012-cross-implementation-parity.md) | Language-neutral contracts + cross-implementation parity testing as the promotion gate | 9 | accepted ✓ |
| [0013](0013-helm-only-production.md) | Helm is the only production form; compose is development-only | 6 | accepted ✓ |
| [0014](0014-three-layer-testbed.md) | Three-layer testbed; real-socket load testing; not a v1 deliverable (**REQ:** [REQ-NF-15](../../requirements/req-nf-15-testbed-performance.md)) | 16 | accepted ✓ |
| [0015](0015-engineering-discipline.md) | Engineering model: layered TDD, ADR institutionalization, four-layer test gates | 17 | accepted ✓ |
| [0016](0016-in-boundary-security.md) | In-boundary security: peer allowlist, end-to-end TLS, console authentication, full audit. No LI, no billing | 18 | accepted ✓ |
| [0017](0017-no-cdr.md) | No CDR: not collected, not delivered, not archived —— replaced by call traces | 4 | accepted ✓ |
| [0018](0018-release-versioning.md) | One product release version, independent component interface versions | §11.3 | accepted ✓ |
| [0019](0019-sip-stack-selection.md) | Production SIP stack selection (overturns 0011's stack premise; reSIProcate selected; go-b2bua / libre as alternatives; rsipstack rejected because Rust is outside the team's tech stack) | 8 | **accepted** |
| [0020](0020-feature-capability-gating.md) | Feature capability gating: layered (deployment-wide master switch + fine-grained runtime override), reuses the configuration-governance change path | 19 | accepted ✓ |
| [0021](0021-runtime-override-granularity.md) | Runtime-override decision granularity and schema: number prefix + stable-hash percentage, idempotent decision (adjudicates open item D7) | — | accepted ✓ |
| [0022](0022-resiprocate-b2bua-control.md) | Product `CallController` over reSIProcate DUM protocol mechanism; language bridge and state recovery remain blockers | 8 | **accepted** (2026-10-05 amendment; D10/REQ-NF-1 still open) |
| [0023](0023-redis-call-state-checkpoint.md) | Call-recovery direction: application-layer necessary-state checkpoint to Redis; does not serialize full DUM / `SipStack` (D10 still not passed) | 2 | proposed |
| [0024](0024-console-password-sessions.md) | Console roles + password authentication and revocable sessions; M4b-6a/6b engineering slices; 2026-10-03 maintainer sign-off accepted | 18 | accepted ✓ |
| [0025](0025-managed-rule-runtime-bundle.md) | Management-plane `ManagedRule` → internal API `ConfigBundle`/`RuleDTO` lossless compile contract (v1: called + prefix subset) | 13 | draft |
| [0026](0026-in-cluster-state-stores-proposal.md) | In-cluster dedicated PG/Redis (not IMS); single-chart merged delivery; partially revises ADR-0013 state rendering | 14 / D12 | accepted ✓ |
| [0027](0027-version-lifecycle-and-eol.md) | Version lifecycle and EOL policy: minor-version support ≥ 12 months, EOL 6-month advance notice, no LTS defined | — | accepted ✓ |

> **Note (2026-10-11, status-drift correction)**: the table above originally recorded **0023** as `draft`, but
> [0023](0023-redis-call-state-checkpoint.md) states `Status: proposed` in its body —— the register and the body disagree.
> **The body is authoritative**; this correction changes only this one register entry to `proposed`, **without altering the ADR body or any other register entry**.
> 0025's `draft` matches its body, so it is left unchanged here.
> Basis: [`../../handoff/2026-10-11-open-adjudication-register.md`](../../handoff/2026-10-11-open-adjudication-register.md)
> §1 S1 table "register/body drift" row. **This note is on disk, pending maintainer review.**

> **Second full re-review (2026-10-11, S1 second batch)**: opened **0001–0027** individually (0000 template excluded) and checked the status lines against their bodies;
> conclusion: **25 English `- **Status**:` lines and the two Chinese-language status lines (0011 / 0019) all match the register above**
> (0023=proposed, 0025=draft, 0011=superseded-in-part, the rest accepted; 0024's trailing maintainer-sign-off note does not change its accepted value).
> **0011 ↔ 0019 are mutually traceable**: [0011](0011-sip-stack-dual-path.md) body line 4 states
> "superseded-in-part by ADR-0019", and [0019](0019-sip-stack-selection.md) body line 7 states
> "overturns the 'production stack = sippy' premise established by ADR-0011".
> **Link check**: resolved all Markdown links within `docs/**` pointing to `adr/00NN-*.md` by relative path (206 in total),
> **205 valid, no out-of-range reference to ADR-0028 or above**; found **1 pre-existing broken link**:
> [`../../acceptance/m5-engineering-closure-2026-10-04.md`](../../acceptance/m5-engineering-closure-2026-10-04.md)
> line 43 writes the link as `architecture/adr/0026-in-cluster-state-stores-proposal.md`,
> which from `docs/acceptance/` should resolve to `../architecture/adr/...` (missing the `../` prefix).
> That file is a 2026-10-04 historical closure document; under the history-preservation convention and outside this batch's authorized change path, **it is not fixed or altered here**,
> only registered for the maintainer to decide (fix: change the link to `../architecture/adr/0026-in-cluster-state-stores-proposal.md`).
> This re-review **did not alter any ADR body and did not alter the register table above**. **This note is on disk, pending maintainer review.**

## Rules

- **Numbers are append-only.** A superseded ADR keeps its number and is marked as superseded by a new ADR; numbers are never reused or reordered.
- **One ADR, one decision.** "Architecture" is not a decision.
- **An ADR must state what it accepts.** The gap it knowingly incurs is part of the record; an ADR without a consequences section is marketing.
- **Code points to its ADR.** A non-obvious line of code carries `# See ADR-00NN`, so a reviewer can walk from code to rationale in one step.
- **Overturning a decision** means writing a new ADR and, in the same change, updating
  [`../system-architecture.md`](../system-architecture.md).

## Relationship to POC ADRs

The POC shipped ADRs 0001 … 0016 in `3rtparty_AS_POC/docs/architecture/adr/`. They are **not** imported.
They record the decisions of a proof-of-concept —— a different system with different non-goals. When a POC decision survives into the product,
it must be re-argued here against the product constraints, with the POC text cited as background. Those that did not survive are simply absent; the migration triage
([`../../migration/triage.md`](../../migration/triage.md)) records the reasons.
