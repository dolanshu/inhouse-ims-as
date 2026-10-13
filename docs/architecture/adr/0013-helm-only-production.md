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

# ADR-0013: Helm is the only production form

- **Status**: accepted
- **Date**: 2026-09-30
- **Decides**: §0 ledger entry 6 — deployment form: Kubernetes + Helm (compose only for the dev environment)
- **Responds to REQ**: REQ-NF-9

---

## Context

What we deliver is **single-tenant on-premises** (REQ-NF-9): one independent instance per customer, deployed in the customer's (the operator's) own machine room, with one namespace carrying one complete system — its own Redis, PostgreSQL, and AS Pod group. The people we face at delivery are the customer's operations staff, who will not read our source code and will only execute commands following an installation guide.

Under this delivery form, **the number of delivery forms itself is a variable that needs to be managed**. If `docker compose` could also go to production, then "which set is actually running in this customer's production" becomes a question that must be answered first every time troubleshooting happens; worse, semantics such as draining, session affinity, Secret mounting, probes, and certificate hot rotation would each evolve in the two forms, ending with neither being complete, and incidents only happen on the half where semantics are missing.

`AGENT.md` §2's non-goals have already closed the other path: **"No Operator (CRD). Use Helm + standard Deployment / ConfigMap / Secret (ADR-0013)."** The reason is that the benefit does not match: the Operator's automation capabilities (custom resources, automatic reconciliation, complex upgrade orchestration) in the scenario of "single-tenant on-prem, change frequency per customer-negotiated windows" buy benefits insufficient to offset its own learning, build, and maintenance costs.

There is also a special constraint that must be borne by the delivery form: **before open item O1 is answered by M6 measurements, this repository must not publish any capacity figures** (`AGENT.md` §2). This means the delivery form must not contain any "authoritative-looking" capacity defaults — a guessed HPA threshold is more dangerous than no HPA, because it silently throttles or over-scales. This constraint requires the chart to have the ability to **refuse rendering**, not merely "leave it empty".

## Decision

- **Production delivery is only the Helm chart (`deploy/helm/`).** One form, no alternatives.
- **`deploy/compose/` is only for the local development environment and must not be used in production.** It is not a "lightweight production"; it is a development launcher.
- **No Operator / CRD.** Use Helm + standard Deployment / ConfigMap / Secret (`AGENT.md` §2 non-goal).
- **Container images are built by `deploy/docker/Dockerfile`; the image is an input to the chart, not a second delivery form.** The image tag is injected via the chart's `image.repository` / `image.tag`, and consumed by Helm after being published to the customer's internal registry.
- **All capacity-type keys are left empty (null), and the template refuses to render rather than falling back to a guessed value.** Unfilled means installation fails (`required` guard + `fail`), rather than pretending it exists with a default value.
- **Customer-specific keys, addresses, and topology are never given values in the repository**: credential placeholders (empty strings), TLS via the customer PKI's Secret reference, Redis / PostgreSQL as external dependencies (the chart does not deploy them).

## Consequences

### Positive

- **One form; operations only need to learn Helm.** Installation, upgrade, rollback, and parameterization all have semantics in only one place; troubleshooting does not require first answering "which set is this".
- **Continuity semantics are implemented in only one place.** `preStop` draining and the extended termination grace period ([ADR-0009](0009-issu-draining.md)), `sessionAffinity: ClientIP` (one of [ADR-0002](0002-per-usecase-process-state-redis.md)'s belt-and-suspenders), TLS certificate mounting and hot rotation ([ADR-0016](0016-in-boundary-security.md)), audit and credential replacement — all defined once, only in the chart.
- **Capacity figures cannot leak out of the chart.** `autoscaling`'s thresholds and replica min/max are `null`, and `hpa.yaml` **does not render the resource** when thresholds are missing; when `autoscaling.enabled` is set but thresholds are unfilled, `minReplicas` / `maxReplicas` go through the `required` guard, installation **fails**, and an explicit message is given. PDB's `minAvailable` likewise does not render when `null` — an availability lower bound invented out of thin air is a decision nobody has made.
- **One Deployment per use case is isomorphic with ADR-0002.** `useCases` is the list being iterated; use cases with `enabled: false` render no objects; adding a use case requires no template-structure changes.

### Negative / accepted

- **The Operator's automation capabilities are given up.** No custom resources, no automatic reconciliation, no complex upgrade orchestration. Accepted: single-tenant on-prem, low change frequency, the Operator's costs exceed its automation benefits; and this is an `AGENT.md` §2 non-goal, not a trade-off of this ADR.
- **The customer environment must have Kubernetes.** Environments without K8s cannot be delivered; bare-metal deployment or "containers running directly" forms are currently not accepted. If such customers appear in the future, a new ADR is needed to overturn this decision, not improvising a set at delivery time.
- **The `helm` binary is an installation prerequisite; this repository does not deliver helm itself.** Air-gapped delivery scenarios need to bring it themselves; this belongs to the implementation manual.
- **Several values must be filled by the customer or the implementer at installation time, and empty-value semantics need to be correctly understood**: `redis.sentinel.masters` / `.addresses` (depends on undecided O5 and D3), `postgres.host` / `.database` (customer-specific external storage, [ADR-0007](0007-data-plane-split.md)), `tls.secretName` (customer PKI), `telemetry.otlpEndpoint` (empty = NoOp export, safe for the call path, [ADR-0005](0005-observability-otel.md)), `sip.peerAllowlist` (**empty must be treated as fail-closed**, [ADR-0016](0016-in-boundary-security.md)). An empty `peerAllowlist` is not a "configure it later" convenience; it is the enabled state of a security control.
- **The chart does not deploy Redis and PostgreSQL.** They are external dependencies, whose high availability and backup are borne by the customer or the implementer ([ADR-0008](0008-redundancy.md) requires stateful components to be included in the redundancy and backup checklist, but they are not within this chart's scope).

## Alternatives considered

| Option | Why not |
|---|---|
| compose can also go to production (dual form) | Semantics drift in the two forms: compose has no HPA, no PDB, no Secret governance, no draining terminationGracePeriod semantics; and "which set is running in production" must be reconfirmed every time |
| Helm + Operator (CRD) | Benefit does not match: single-tenant on-prem, low change frequency, the Operator's learning and maintenance costs exceed its automation benefits; `AGENT.md` §2 has listed it as a non-goal |
| Kustomize | No packaging and release version management; the same set of carrier-grade knobs cannot be centralized and made explicit as values, nor parameter-validated at installation time |
| Bare metal / systemd deployment | Directly conflicts with [ADR-0010](0010-autoscaling-hpa-downscale-guard.md)'s HPA and [ADR-0008](0008-redundancy.md)'s multi-replica zero single points of failure; scaling and draining of one-process-per-use-case both need an orchestration layer |
| Pure Helm + standard objects (this decision) | Adopted. One form, one set of semantics, missing thresholds means refusing to render |

## Evidence

- `AGENT.md` §2 non-goal verbatim: "**No Operator (CRD).** Use Helm + standard Deployment / ConfigMap / Secret (ADR-0013)."
- `deploy/helm/values.yaml` verbatim (M5 values contract comment block): "Single-tenant, on-prem: one namespace holds one complete system (its own Redis / PostgreSQL / AS Pod group). See REQ-NF-9. **Helm is the only production form; `deploy/compose/` is dev-only. See ADR-0013.**" Same file's capacity-rule comment: "no CPS or concurrency figure is published before M6 measures it. Every key below that would encode a capacity assumption is left null, and the template that consumes it does not render the resource at all rather than fall back to a guessed number."
- `deploy/helm/README.md` "Render guards" verbatim: `hpa.yaml` renders only when `autoscaling.enabled` **and** at least one target threshold is non-null, with `minReplicas` / `maxReplicas` then `required`; `pdb.yaml` renders only when `podDisruptionBudget.minAvailable` is non-null; `secret.yaml` renders only when `postgres.secretName` is empty. Same table: "`autoscaling.minReplicas` / `.maxReplicas` | `required` — install **fails** with an explicit message when autoscaling is enabled. There is no default, because a default would be a guessed capacity number".
- Guard code in `deploy/helm/templates/hpa.yaml`: `{{- $minReplicas := required "autoscaling.minReplicas is required when autoscaling.enabled=true. It is a capacity figure: measure it in M6 (O1), do not guess." $a.minReplicas }}` (same for `maxReplicas`), plus the `{{- fail ... }}` when all thresholds are empty. The file header comment states: entering this file with capacity figures as null is a **hard error, not a silent skip**, because "an HPA silently omitted because its thresholds were left empty looks identical to an HPA that was never intended".
- **Rendering verified (M5)**: `docs/acceptance/report.md` M5 section verbatim — "helm v3.16.2: `helm lint deploy/helm` 0 failed, `helm template as deploy/helm` exit 0; the first render exposed and fixed two left-trim-induced label concatenation issues in `_helpers.tpl`; the `--set autoscaling.enabled=true` (HPA thresholds unfilled) path failed as expected". With the current default values (`useCases` is `translation` and `anti-fraud`, both `enabled: true`, HPA thresholds and `podDisruptionBudget.minAvailable` are null, so `hpa.yaml` and `pdb.yaml` do not render), `serviceaccount.yaml` / `secret.yaml` / `configmap.yaml` each render 1, plus one Deployment + Service per use case for 4, totaling **7 objects**.
- **The image is an input to the chart, not a second form**: `deploy/docker/README.md` verbatim "The image is an input to the Helm chart; it is not a second production deployment form. Helm remains the only production deployment form under ADR-0013. The files under `deploy/compose/` are for local development only." The build command is `docker build -t as-platform:dev -f deploy/docker/Dockerfile .` (build context is the repository root).
- `docs/plan.md` §2.1 directory structure verbatim: "`deploy/` helm/ (production) · compose/ (dev only)"; §4 milestone M5 deliverables include the Helm chart.
- Architecture doc §0 decision ledger entry 6 verbatim: "Deployment form | Kubernetes + Helm (compose only for the dev environment)".
- PRD REQ-NF-9 (single-tenant on-premises deployment) verbatim: "Independent instance per customer, on-premises delivery (deployed inside the operator's machine room). No multi-tenancy……the operator's delivery form is itself one customer per system; multi-tenancy brings no benefit in this scenario and instead increases cross-tenant data leakage risk."
- `deploy/helm/README.md` "Keys left empty on purpose" table, O5 / D3 linkage verbatim: "`redis.sentinel.masters` / `.addresses` | topology depends on unresolved O5 (N+1 vs N+M) and D3 (Sentinel wiring, split-brain window)".

## Related

- [ADR-0002](0002-per-usecase-process-state-redis.md) One process per use case — `useCases` iteration and the session-affinity belt-and-suspenders
- [ADR-0009](0009-issu-draining.md) ISSU is draining — `preStop` + extended terminationGracePeriodSeconds
- [ADR-0010](0010-autoscaling-hpa-downscale-guard.md) Autoscaling HPA — the guard that consumes missing-threshold-refuses-to-render
- [ADR-0016](0016-in-boundary-security.md) In-boundary security — TLS Secret mounting hot rotation, empty `peerAllowlist` means fail-closed
- [ADR-0005](0005-observability-otel.md) OTel three signals — empty `otlpEndpoint` means NoOp export
- [ADR-0007](0007-data-plane-split.md) Data-plane split — governance PG / runtime Redis logic unchanged
- [ADR-0008](0008-redundancy.md) Redundancy — HA/backup responsibility per [ADR-0026](0026-in-cluster-state-stores-proposal.md) runbook
- [ADR-0026](0026-in-cluster-state-stores-proposal.md) (2026-10-04) — revises the below "the chart does not deploy PG/Redis": optional `stateStores.enabled` rendered by the same chart; IMS PG forbidden
- [`../system-architecture.md`](../system-architecture.md) §0 entry 6
- Open items O1 (capacity target / M6) and O5 / D3 (Redis topology and wiring) — all **undecided**; the chart's corresponding keys stay empty

## Amendment ([ADR-0026](0026-in-cluster-state-stores-proposal.md), 2026-10-04)

**Partially revises** this ADR's last Decision item and "the chart does not deploy Redis and PostgreSQL" in Consequences:

- **Still holds**: the only production form is `deploy/helm/`; no Operator; compose is dev-only; capacity keys refuse guessed rendering.
- **Revised**: standard on-prem can render dedicated PostgreSQL and Redis in the **same release, same namespace** via **`stateStores.enabled=true`** (see `values-onprem.example.yaml`); `bootstrapDevCredentials` is kind/dev only.
- **Still holds**: the operator's **IMS core database** must not serve as the AS governance DSN; when the customer brings managed PG/Redis, set `stateStores.enabled=false` and fill `postgres.host` / `redis.url`.
- **Backup / HA**: the chart does not replace the ADR-0008 checklist; see `docs/acceptance/m5-state-stores-runbook.md`.

- **Amendment 2026-10-06 (M5.1 minimal set)**: "the chart does not deploy PG/Redis" in the main Decision / Consequences has been replaced by this Amendment section (`stateStores.enabled=true` optional same-chart rendering); Helm as the only production form and capacity refusing guessed rendering remain unchanged.
