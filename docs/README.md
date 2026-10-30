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

# Documentation map

Read by reader role. Everything is plain text — Mermaid or ASCII diagrams, never rendered images that cannot be diffed.

> Three new reader-facing directories were added under `docs/`: **review** [`product/`](#for-reviewers-product-and-review-documents), **operations** [`operations/`](#operations-and-on-call), **delivery** [`delivery/`](#delivery-form). All three come from the same packaging plan: [`product-packaging-plan.md`](product-packaging-plan.md).

## Deciding what to build

| Document | What it is |
|---|---|
| [`architecture/README.md`](architecture/README.md) | **Architecture entry point.** The document map and priorities (**specification documents = `hld.md` / `lld.md`**), delivery boundaries, evidence grading, currently known open items |
| [`architecture/system-architecture.md`](architecture/system-architecture.md) | **Design baseline.** Every confirmed decision, its rationale, the open-items list and the risk register |
| [`architecture/adr/`](architecture/adr/) | Decision records; start with the registry in its README |
| [`requirements/`](requirements/) | Requirements documents (PRD, REQ-NF-15 testbed / performance research); start from its README |
| [`design/`](design/) | Design working notes, including the technical notes stripped from PRD v0.1; start from its README |
| [`SIP_stack_selection.md`](SIP_stack_selection.md) | Open-source SIP protocol stack selection comparison (against sippy) — the input behind ADR-0019 |
| [`plan.md`](plan.md) | Delivery plan: milestones, ordering, exit criteria |
| [`environments.md`](environments.md) | **Environment registry.** Register of long-lived facts: each machine's name, hostname, tools present/absent, evidence already produced. When citing an environment you must use the name in the table. **The data is generated on the spot by `tools/env-probe.sh` probing and is not maintained by hand** (see "Local environment and tooling") |
| [`product-packaging-plan.md`](product-packaging-plan.md) | **Product packaging plan.** Four batches of deliverables, the origin and execution order of the three new directories `product/`·`operations/`·`delivery/` |
| [`migration/triage.md`](migration/triage.md) | How POC code was triaged before anything was adopted |
| [`next-release-v1.1-plan.md`](next-release-v1.1-plan.md) | **The single tracking vehicle for the next release (the v1.1 batch).** Where the fate of every leftover item after this version (the M8 internal version) is closed out is consolidated here; all other documents keep only pointers |

## Building it

| Document | What it is |
|---|---|
| [`../AGENT.md`](../AGENT.md) | **Read this before writing code.** Collaboration rules, layering, TDD policy, gates, git rules |
| [`../CONTRIBUTING.md`](../CONTRIBUTING.md) | Environment setup, local gates, commit and review conventions |
| [`../README.md`](../README.md) | Positioning, repository tour, quick start |
| [`agents/`](agents/) | Agent-facing docs: domain docs, the GitHub issue tracker conventions, triage labels |

## For reviewers: product and review documents

| Document | What it is |
|---|---|
| [`product/one-pager.md`](product/one-pager.md) | **Product one-pager.** Value proposition, the big architecture picture, KPI definitions, three-step deployment |
| [`product/ne-datasheet.md`](product/ne-datasheet.md) | **Network element datasheet.** Interface inventory, KPIs and alarms, dependencies, resource specifications; capacity figures are blocked by O1 |
| [`product/compliance-matrix.md`](product/compliance-matrix.md) | 3GPP / GSMA / RFC specification conformance matrix (Sh and billing are marked N/A with the reason retained) |
| [`product/responsibility-matrix.md`](product/responsibility-matrix.md) | RACI responsibility boundary matrix: AS versus the S-CSCF / HSS / billing domain / network management / security domains |
| [`product/version-lifecycle.md`](product/version-lifecycle.md) | Version lifecycle and EOL policy (REQ-NF-16 / ADR-0027) |
| [`product/security-privacy.md`](product/security-privacy.md) | Security and privacy compliance (PDPO); retention period pending O4, storage selection pending D5 |
| [`reviews/README.md`](reviews/README.md) | **Review record index.** Every review record in this directory (162 files, dated M0→M8) with its topic; each record ends with an `## Adjudication` table (`AGENT.md` §3.2 / §3.3) |

## Operations and on-call

| Document | What it is |
|---|---|
| [`operations/README.md`](operations/README.md) | Operations volume overview: reader tiers, consolidation mapping, not-yet-delivered list |
| [`operations/runbook-l1.md`](operations/runbook-l1.md) | L1 operations runbook: daily inspection, first response to alarms, common operations (NOC) |
| [`operations/runbook-l2.md`](operations/runbook-l2.md) | L2 operations runbook: deep troubleshooting, signalling and log forensics (second line) |
| [`operations/fault-demarcation.md`](operations/fault-demarcation.md) | Fault demarcation runbook: four-way demarcation across AS / S-CSCF / HSS / billing domain |
| [`operations/rollback-playbook.md`](operations/rollback-playbook.md) | Traffic draining / rollback plus coordination on the iFC side |
| [`operations/backup-restore.md`](operations/backup-restore.md) | Backup and restore plan plus a drill record template (depends on a real cluster environment) |
| [`operations/alert-response-matrix.md`](operations/alert-response-matrix.md) | Alert-to-action table: severity, trigger conditions, handling actions, escalation path |
| [`operations/grafana-dashboards/README.md`](operations/grafana-dashboards/README.md) | Grafana dashboard templates (`overview.json` / `sip-signaling.json`) and their usability prerequisites |

> `docs/acceptance/*-runbook.md` are the historical originals and the audit traceability source, **never deleted, never moved, never rewritten**; `operations/` only provides the index + links + the operational body text aimed at on-call staff.

> **Review / execution record entry point**: the **execution record** for this round of product packaging (the three directories `product/`, `operations/`, `delivery/`) is in [`reviews/product-packaging-execution-record-2026-10-10.md`](reviews/product-packaging-execution-record-2026-10-10.md). ⚠️ That file is an **execution record, not a maintainer-signed review record** — the independent review record each volume requires (`AGENT.md` §3.3) is still awaiting maintainer review; the pre-packaging review comments are in [`reviews/product-packaging-plan-review-2026-10-09.md`](reviews/product-packaging-plan-review-2026-10-09.md).

## Delivery form

| Document | What it is |
|---|---|
| [`delivery/README.md`](delivery/README.md) | Delivery directory overview: the three-step delivery process, prerequisites, boundary against the authoritative documents |
| [`delivery/install-guide.md`](delivery/install-guide.md) | **Installation and deployment guide.** Delivery checklist, image acquisition and mirroring, `helm install` command sequence (Helm parameters are authoritative in [`../deploy/helm/README.md`](../deploy/helm/README.md)) |
| [`delivery/airgap-package.md`](delivery/airgap-package.md) | How to produce and use the air-gapped installation package: the networked side, the offline side, checksums and supply chain |
| [`delivery/preflight.sh`](delivery/preflight.sh) | Pre-deployment environment validation script: K8s / resources / dependent services / Helm / RBAC / chart render guards |

## Running it

| Document | What it is |
|---|---|
| `acceptance/` | Item-by-item acceptance criteria with evidence and the original historical runbooks — still where the historical evidence lives |
| [`../deploy/helm/README.md`](../deploy/helm/README.md) | **The single authority on Helm chart parameters and rendering behaviour** (delivery-form notes) |

## Local environment and tooling

> **Environment information is not maintained by hand.** The scripts below handle probing and installation, and the data rows of the registry in
> [`environments.md`](environments.md) come from their output. The project is deployed onto different computers, so **environmental differences are the
> norm** — do not infer project capability from any single machine's tool inventory, and do not change the documentation's position because "some machine lacks X".

| Script / document | What it is |
|---|---|
| [`../tools/env-probe.sh`](../tools/env-probe.sh) | **Environment probe (read-only).** Probes hostname / OS / architecture plus docker / uv / python3.10 / helm / kubectl / kind / promtool / make / git, distinguishing three states: "✅ present / ❌ missing / ⚠ installed but unusable". `--markdown` emits rows that can be pasted straight into the table in [`environments.md`](environments.md), `--json` is for machines. It installs nothing, changes no system state and needs no root, and still exits 0 when tools are missing |
| [`../tools/bootstrap-infra.sh`](../tools/bootstrap-infra.sh) | **infra tooling installation (no root, idempotent).** Unpacks helm / kubectl / kind / promtool into `tools/bin/`, with versions pinned in [`../tools/VERSIONS`](../tools/VERSIONS); supports `--dry-run`, `--only <tool>`, `--force`, and automatically invokes `env-probe.sh` to verify afterwards. **Any path that needs root reports an explicit error and never sneaks in a sudo** |
| [`handoff/README.md`](handoff/README.md) | **Handoff record index.** Every session handoff record in `handoff/` (38 files) with its topic |
| [`handoff/2026-10-11-local-infra-bootstrap-plan.md`](handoff/2026-10-11-local-infra-bootstrap-plan.md) | **The execution plan for filling in the four missing tools locally** (prerequisite checks, installation inventory, pinned versions, falsifiable verification steps, rollback, stop line). Executors should start from that document, not from this one |

## References

| Document | What it is |
|---|---|
| `glossary.md` | IMS / SIP glossary — **not yet created**; will land with the first code milestone |
| `specs/` | Normative references (RFC 3261, RFC 4566, RFC 8688, TS 24.229) and message samples — **not yet created** |
