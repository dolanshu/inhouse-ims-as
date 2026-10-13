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

# Architecture entry

> **This document is the entry point and priority statement for
> `docs/architecture/`; it does exactly four things**: a document map with
> priorities, a delivery boundary, an evidence-grading scheme, and currently known
> open items. **This document resolves no open item.**
> Landed date 2026-10-11, **status: landed, pending maintainer review**.

## 1. Document map and priorities

**Normative documents = [`hld.md`](./hld.md) / [`lld.md`](./lld.md).**

| Document | Status |
|---|---|
| [`hld.md`](./hld.md) | **Normative document** (high-level design) |
| [`lld.md`](./lld.md) | **Normative document** (low-level design) |
| [`adr/`](./adr/) | Decision records; the entry point is the registry at [`adr/README.md`](./adr/README.md). ADRs record **why** a decision was made; they do not replace HLD / LLD |
| [`system-architecture.md`](./system-architecture.md) | **Reference and background material**, no normative force |
| [`reSIProcate.md`](./reSIProcate.md) | **Reference and background material** (SIP-stack selection background) |
| [`resiprocate-dum-b2bua.md`](./resiprocate-dum-b2bua.md) | **Reference and background material** (DUM protocol-mechanism background) |
| [`call-state-recovery-options.md`](./call-state-recovery-options.md) | **Reference and background material** (call-state recovery options comparison, same topic as ADR-0023) |
| [`capacity-estimate.md`](./capacity-estimate.md) | **Reference and background material** (capacity-estimation method, **containing no externally-committed numbers**) |

**Conflict-resolution rule (unambiguous):**

> **If any of the above "reference and background material" conflicts with HLD /
> LLD, HLD / LLD always win.**
> When reference material conflicts with an ADR: the ADR explains the decision
> rationale, but **the implementation criterion follows HLD / LLD**;
> when all three disagree, it is an **open item** to be escalated per §4 — **the
> reader must not pick one unilaterally**.

**Same-source overlap note:** `reSIProcate.md` / `resiprocate-dum-b2bua.md` / ADR-0019·0022 share a source;
`system-architecture.md` and `hld.md` are comparable in size and both are full-architecture
narratives; `call-state-recovery-options.md` and ADR-0023 are the same topic. Duplication is
not three sources of truth — **normative force lives only in HLD / LLD**.

## 2. Delivery boundary

The decision line ([`../handoff/2026-10-11-open-adjudication-register.md`](../handoff/2026-10-11-open-adjudication-register.md) §7.1):

> **Will this asset reach the customer? Yes → deliverable product; no, we use it
> only ourselves → scaffolding.**
> Second criterion for the gray zone: **will the customer file a ticket with us
> about it? Yes → deliverable product; never → scaffolding.**
> **Scaffolding produces instrument readings; the deliverable product is the
> quality-inspection report.**

| Category | Asset | Constraint |
|---|---|---|
| **Deliverable product** | `deploy/helm/` (chart + values + templates), container images, `deploy/alerts/` alert rules, `docs/product/`, `docs/operations/`, `docs/delivery/` | Enters the delivery package; accountable to the customer |
| **Scaffolding** | all `deploy/kind/` scripts, `testbed/` simulation and load-test assets, `docs/plan.md`, `docs/handoff/`, ADR | **Must not be used in customer production**; does not enter the delivery package |

**Landing and index:** [`../delivery/install-guide.md`](../delivery/install-guide.md) §2 delivery checklist,
and that file's `:19` (kind self-signed cert "is only a precedent, **not a deliverable**"),
`:91` (kind / lab install
**"must not be used in customer production"**). **That is the existing landing of
the decision line; this document only ratifies an existing fact, not a new
decision.**

**Production form:** Helm-only; no Operator, no second installer (ADR-0013;
[`../delivery/install-guide.md`](../delivery/install-guide.md) `:5` already declares this hard boundary).

## 3. Evidence grading

**Three classes; any citation must use the triplet `(conclusion, evidence file,
date)`** — bare sentences like "chart-check passed" with no subject are not
allowed; see [`docs/environments.md`](../environments.md) (the document forbids anonymous "this machine").

| # | Class | Meaning | In-repo instance | Directory |
|---|---|---|---|---|
| **①** | **Deliverable product quality evidence** | Quality-check artifacts of the deliverable product (chart / image / alert rules / docs) | `PASS-chart-check-2026-10-05.txt`, `PASS-alert-check-2026-10-05.txt`, `PASS-gate-2026-10-05.txt` | `docs/acceptance/artifacts/m5/2026-10-05/` (index and easy-to-misread notes in that directory's [`README.md`](../acceptance/artifacts/m5/README.md)) |
| **②** | **Externally-binding basis** | **Basis for external commitments that we produce using internal scaffolding; not a customer acceptance item** — the customer does not sign that transcript. What the customer will press on is "can the chart install, does upgrade drop calls", not the kind scripts | kind-cluster transcripts such as 7.2d; "control-plane cluster deployment proof (incl. 7.2d)" in the M5 closure conditions | Artifacts scattered in `docs/acceptance/` and handoff records; produced by the scaffolding `deploy/kind/`. **Nature adjudication in register §7.3** |
| **③** | **Failure / fail-closed record** | File-name prefix `FAILCLOSED-`, **not a pass evidence**. Its value is in proving that "explicit failure when no cluster / prerequisites missing" behavior exists | `FAILCLOSED-m5-strict-context-2026-10-05.txt` (`M5_STRICT=1` and no `kind-as-m5`, **exit=1**) | `docs/acceptance/artifacts/m5/2026-10-05/` |

**Three hard rules:**

1. **The file name is the conclusion** — `docs/acceptance/artifacts/**` enforces the
   prefix `PASS-` / `FAILCLOSED-`, format `<conclusion>-<checked-item>-<date>.txt`.
2. **`Fail` / `ERROR` text inside this directory is normal semantics; do not judge
   the file as failed on that basis; always defer to the file-name prefix.**
   (Example: `[INFO] Fail: tls.enabled=true requires tls.secretName` inside
   `PASS-chart-check-2026-10-05.txt` is a chart-check **expected assertion** of a
   fail-closed render.)
3. **skip is not pass evidence** — `PASS-gate-2026-10-05.txt` contains 2 SKIPPED
   entries; citation must state the skip composition alongside.

Basis and approval record: register §7.4 (four-tier evidence mechanism). Regression
guard: `tests/test_evidence_discipline.py`.

## 4. Currently known open items

**This section only lists, does not resolve.** Each item links to the register;
**the reader must not pick one unilaterally before the maintainer resolves it**.

| Item | Status | Links to |
|---|---|---|
| ADR-0023 body and registry once drifted (registry said `draft` / body said `proposed`) | **Fixed** — body wins; registry changed to `proposed`, with basis and date note under [`adr/README.md`](./adr/README.md) below the registry | register §1 S1 table; note in adr/README.md |
| **G3 / A5** monitoring wiring (annotation vs ServiceMonitor / PodMonitor) | Pending operator monitoring-integration standard input, **chart not changed now** | register §3 X1 |
| **D3** HA topology | Redis **client wiring resolved 2026-10-05**; the only remaining open item is the HA topology (N+1 vs N+M, Sentinel vs Cluster, etc.) | register §2 P2 / `../plan.md` §0 decision table |
| **O5** DR tier | In-site N+1, cross-site 1+1 warm standby already decided (G7); **no rack/AZ-level fault-tolerance commitment**, RTO / RPO values not yet decided | register §2 P2 |
| **O4 / D5** values | Decided but **implementation not landed**: O4 default retains 10 days and is deployment-configurable, D5 selects in-cluster PostgreSQL; trace storage / query / deletion capability **not implemented this round**, downstream docs still stale | register §2 P2 / P3 |
| **P4** new alert-rule-group validation | The `as.runtime` / `as.platform` added 2026-10-10 **have not been validated by promtool yet** (needs promtool to run; not run this round). `deploy/alerts/` is a deliverable product; validation responsibility does not float just because the evidence comes from scaffolding | register §7.5 |
| **G9-b / G9-c** | Machine-capability definitions already have a home (`docs/environments.md`) but **not yet substituted-decided**; whether cluster-level verification must run on every machine / every PR is still undecided | register §1 G9 |
| **S1** five-tier document-system full-chain cleanup | **Unauthorized, not started** | register §4 S1 |

## 5. Related entries

| Document | What it is |
|---|---|
| [`../environments.md`](../environments.md) | Environment registry — referenced environments must use the names in the table |
| [`../acceptance/artifacts/m5/README.md`](../acceptance/artifacts/m5/README.md) | Evidence index + three easy-to-misread things |
| [`../handoff/2026-10-11-open-adjudication-register.md`](../handoff/2026-10-11-open-adjudication-register.md) | Adjudication and open-issue register (§7 = 2026-10-11 adjudication landing) |
| [`../README.md`](../README.md) | `docs/` master navigation |
