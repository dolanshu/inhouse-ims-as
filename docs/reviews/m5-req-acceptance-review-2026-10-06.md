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

# M5 REQ-Level Acceptance Review Record (M8 Release Candidate, Phase B Minimum Set)

- **Review target (object)**: M5 milestone **REQ-level** acceptance (providing the basis for M8 test-plan checkmarks); scope = REQ-NF-3 / REQ-NF-4 / REQ-NF-9 / REQ-NF-13 / REQ-NF-14 + the 7.2d ingress/trusted-proxy gate-closure conditions. Inputs: [`m5-full-chain-review-2026-10-05.md`](m5-full-chain-review-2026-10-05.md) (conclusion: fail)、[`2026-10-06-m8-release-candidate-plan.md`](../handoff/2026-10-06-m8-release-candidate-plan.md) §4 Phase B.
- **Review date (date)**: 2026-10-06
- **Reviewer (reviewer)**: AI agent (per user instruction, self-decision while the maintainer was absent; **the maintainer's countersignature is still outstanding**; this record does not replace maintainer sign-off).
- **Review conclusion (conclusion)**: **conditional pass (engineering slice) / fail at the REQ level, 10 items deferred**. The M5 engineering slice (chart deployment shape, draining/scale-down mechanism wiring, kind deployment evidence) may be referenced by M8; M5 **fails at the REQ level** and must not be claimed as all-REQ-green; the 10 items in the table below are explicitly deferred, and all remaining full-chain Major/Minor items continue to be tracked per full-chain review §7 (see §5).

---

## 1. Phase B self-decision record (B-1 / B-2 / B-3, countersignature outstanding)

| ID | Self-decision | Rationale |
|----|--------|------|
| **B-1** | Execute only **MINIMAL M5.1**: Helm fail-open fixes (H-1…H-4) + chart-check onprem matrix + K-1/K-2 fail-closed hardening + HLD/LLD M5 delta + ADR-0008 amendment + REQ chain annotations. Full alerting/metrics wiring (C-1…C-5), OTLP exporter (C-7), scale-down guard parameterization (C-6), NetworkPolicy egress, resources/probes are all **DEFERRED until after the RC** | The RC must not claim M5 REQ green; the engineering-slice evidence is sufficient to substantiate the deployment shape, and full-chain remediation exceeds the RC window |
| **B-2** | **Uphold** the 2026-10-04 M5 engineering-gate sign-off (not revoked, history not rewritten), but explicitly **downgrade** its meaning to `engineering closure (not REQ acceptance)` | Avoid rewriting history; engineering closure and REQ acceptance are two different things, and this record is the first to write that sentence into a review conclusion |
| **B-3** | Story C stays at **L1 (F10)**: show only the chart/alerts **shape** + a kind digest; it must not be stated as "M5 full chain has been accepted" or "production alerting/scale-down has been closed" | Per the reconciliation paragraph of F10 in [`pre-m8-demo-review-plan.md`](../handoff/pre-m8-demo-review-plan.md); the wording is unchanged until the full-chain conclusion is flipped |

## 2. B-4 — Registering the 7.2d requirement-chain gap

- 7.2d (ingress/trusted-proxy) is one of M5's three gate-closure conditions, but in the PRD it has **no corresponding REQ source** (full-chain R-1: REQ-S-2 is SIP signaling TLS, REQ-S-4 only covers authentication and auditing; neither covers console HTTPS redirect / `X-Forwarded-Proto` trust / ingress proxy CIDR allowlist).
- This record registers it as a **sourceless gate condition**: `test-plan.md` §1.4 (M4b-7.2d preflight) is executed only as a pre-deployment check and **produces no REQ pass item**; adding a REQ or correcting via ADR is for the maintainer to adjudicate before M8 phase C.

## 3. B-5 — Scope statement

- Folding `chart-check` into `make gate` (blocking ① fast layer) was already completed in **Phase A**; this task does not touch the gate again.
- The landing point of B-5 in this task is **renderable onprem values**: non-empty placeholder secretName in `values-onprem.example.yaml` + the fail message in `config-service-deployment.yaml` pointing at the example file + a new onprem matrix in chart-check (H-2 verification).

## 4. B-6 — REQ traceability annotations

- Full-chain R-2: the 5 M5 acceptance/runbook documents and the M5 section of `report.md` have **REQ-\* reference count = 0**. This record restores that linkage; the M5 engineering slice traces back to: **REQ-NF-3** (horizontal scaling / draining / scale-down mechanism)、**REQ-NF-4** (ISSU draining semantics)、**REQ-NF-9** (single-tenant on-prem Helm delivery)、**REQ-NF-13** (metrics/health endpoint shape)、**REQ-NF-14** (alert rule set shape, shape only)、**7.2d** (sourceless gate condition, see B-4).
- Traceability stops at the "engineering slice" level and does not constitute a pass determination for the above REQs.

## 5. What this minimum set did / explicitly did not do

Done (this task's diff): H-1 (complete the keys in the `secret.yaml` else branch + `fail` for the stateStores production combination), H-2 (onprem example placeholder + chart-check onprem matrix), H-3 (`fail` when `tls.secretName` is empty), H-4 (`fail` when `peerAllowlist` is empty + `sip.allowEmptyAllowlistForTest` test escape hatch), K-1 (ingress/verify script WARN→FAIL), K-2 (HPA guard validates the helm exit code + onprem render assertion exit code), HLD/LLD `Amendment 2026-10-06`, an ADR-0008 SPoF-gap amendment, ADR-0013 amendment annotations.

Explicitly not done (still open; the full-chain §7 text governs): alert C-4/C-5 minor, simulated seam C-8, config crash path C-10, zero tests for the version store C-11, H-5/H-6/H-7/H-9/H-10, K-3…K-6, R-1…R-9 (including R-3 capacity-criteria mutual exclusion and R-6 evidence gitignore), plus the 10 formal deferrals in the table below.

## 6. Defer list (10 items; the constituents of the REQ-level fail)

| # | Full-chain ID | Content | Corresponding plan §5 / proposed new row |
|---|---------|------|--------------------------|
| 1 | C-1 | 6 dead alert rules (4 metrics do not exist + 2 zero call sites) | §5.3 PM/AM (alert lifecycle requirement to be added) + §4.4.3 (capacity-class alerting after M6); propose new `M5D-1` |
| 2 | C-2 | `clamp_min` math error (does not fire on a full outage at low traffic) | §5.1 O1 (thresholds must be measured at M6); propose new `M5D-1` |
| 3 | C-3 | The telemetry threshold `> 0` semantics do not match | §5.1 O1; propose new `M5D-1` |
| 4 | C-6 | Dead scale-down guard configuration (read in but only logged, not used in the decision) | ADR-0020/M7 actuation undecided; propose new `M5D-2` (guard parameterization + behavior tests for both on and off states) |
| 5 | C-7 | OTLP export is an empty shell (NoOp sink, dropped on enqueue) | §5.3 PM (OTel traces/logs not implemented); propose new `M5D-3` |
| 6 | C-9 | Metrics have zero production call sites (response/rule_hit/telemetry_dropped never increment) | M7 E1 (real call counting goes through the signaling path); propose new `M5D-1` |
| 7 | H-8 | NetworkPolicy has no Egress, and the source selector is too broad | §5.1 D12/O5 (HA/topology customer SLA); propose new `M5D-4` |
| 8 | H-11 | No resources (BestEffort), no startupProbe on AS, config-service tcpSocket probe | §5.1 O1/M6 (sizing depends on measurement); propose new `M5D-5` |
| 9 | A-2 | Cross-site switchover drill not performed (ADR-0008 assigned it to M5) | §5.1 O5 (DR level customer SLA); propose new `M5D-6` |
| 10 | T-1 | The feature switch has no behavior tests for the on and off states | ADR-0020 default state / canary strategy undecided; propose new `M5D-2` |

The finalization of the proposed plan §5 rows (`M5D-1`…`M5D-6`) is performed by the maintainer — this task does not modify `plan.md` (the maintainer owns plan editing); the table above is the proposed row content.

## 7. B-7 — Re-review statement

- This record is the **REQ-level re-review** of M5 (relative to the full-chain "fail" and the 2026-10-04 "engineering closure"): the conclusion is conditional pass (engineering slice) / fail at the REQ level.
- For M5 to flip to pass at the REQ level, the 10 items in the table above must be closed (or accepted in writing by the maintainer as risk / moved out of v1), and the maintainer must sign the countersignature field of this record; before that signature, any "all REQ green" statement is a violation.

---

## Confirmation

| Item | Record |
|---|------|
| Review conclusion | Conditional pass (engineering slice) / fail at the REQ level, 10 items deferred (§6) |
| Self-decisions | B-1 (minimal M5.1) / B-2 (uphold engineering closure and downgrade its meaning) / B-3 (story C stays at L1) — the maintainer's countersignature is still outstanding |
| Maintainer confirmation | **Awaiting sign-off** (this field must be filled in by the maintainer; this record does not constitute a REQ-level pass, nor does it revoke any existing closure record) |
| Input review | [`m5-full-chain-review-2026-10-05.md`](m5-full-chain-review-2026-10-05.md) (fail, remains in effect; this record is its Phase B re-review, not a refutation) |
| Evidence not accepted | All `m5-*` engineering-closure review records under `docs/reviews/` (following the full-chain evidence-exclusion statement) |

---

## 9. Proxy signature for N2 item 2 + finalization of the M5D rows (2026-10-12; §1 and §6 text preserved unchanged)

> **Authorization source**: on 2026-10-12 the maintainer **explicitly authorized the agent to sign on their behalf** for M8's nine written N2 adjudications
> (the canonical text of N2 item 2 is this very file; the overall proxy-signature record is
> [`../handoff/2026-10-12-m8-n2-countersign-record.md`](../handoff/2026-10-12-m8-n2-countersign-record.md)).
> **This section is not a maintainer's personal signature**; each item is marked "signed by the agent on behalf" with its basis attached.

### 9.1 Countersignature of B-1 / B-2 / B-3 (originally "the maintainer's countersignature is still outstanding")

| Self-decision | Proxy-signature conclusion | Basis |
|---|---|---|
| **B-1** Execute only **MINIMAL M5.1** (H-1…H-4 fixes + chart-check onprem matrix + K-1/K-2 fail-closed hardening + HLD/LLD delta + ADR-0008 amendment + REQ chain annotations); full alerting/metrics wiring (C-1…C-5), OTLP exporter (C-7), scale-down guard parameterization (C-6), NetworkPolicy egress, resources/probes are all **DEFERRED until after the RC** | **Confirmed**. Signature: **signed by the agent on behalf (maintainer authorization of 2026-10-12)** | The verbatim text of the §1 B-1 row in this file and its basis column (the RC must not claim M5 REQ green; the engineering-slice evidence suffices to substantiate the deployment shape) |
| **B-2** **Uphold** the 2026-10-04 M5 engineering-closure sign-off (not revoked, history not rewritten), with its meaning explicitly **downgraded** to "engineering closure (not REQ acceptance)" | **Confirmed**. Signature: same as above | The verbatim text of the §1 B-2 row in this file and its basis column |
| **B-3** Story C stays at **L1 (F10)**: show only the chart/alerts **shape** + a kind digest; it must not be stated as "M5 full chain has been accepted" or "production alerting/scale-down has been closed" | **Confirmed**. Signature: same as above | The verbatim text of the §1 B-3 row in this file and its basis column; the F10 reconciliation paragraph of `pre-m8-demo-review-plan.md` |

### 9.2 Finalization of the M5D-1…M5D-6 rows (N2 item 8)

§6 of this file states: "the finalization of the proposed `plan.md` §5 rows (`M5D-1`…`M5D-6`) is performed by the maintainer — this task does not modify `plan.md`".
**After the maintainer authorized the proxy signature on 2026-10-12, that finalization has been executed**: the six rows were written into §5 of `docs/plan.md`, with the mapping taken from the proposals in the §6 table:

| Row | Aggregated defer items | Content |
|---|---|---|
| `M5D-1` | C-1、C-2、C-3、C-9 | Alert rules and metric thresholds/call sites (`clamp_min` math error, telemetry threshold `> 0` semantics, zero production call sites for metrics, dead alert rules) |
| `M5D-2` | C-6、T-1 | Scale-down guard parameterization + behavior tests for the feature switch in both the on and off states |
| `M5D-3` | C-7 | OTLP export (currently a NoOp sink, dropped on enqueue) |
| `M5D-4` | H-8 | NetworkPolicy Egress and narrowing of the source selector |
| `M5D-5` | H-11 | resources requests/limits, AS startupProbe, config-service probe semantics |
| `M5D-6` | A-2 | Cross-site switchover drill (ADR-0008 assigned it to M5) |

All six rows are marked as **moved out of v1** (not included in v1 scope), and each carries its source defer items and the blocking O/D numbers.

**Boundary**: finalizing the M5D rows **does not equal** an M5 REQ pass —— per the N2 text, M5D-1…M5D-6 are merely **moved out of v1**;
the re-review conclusion (fail at the REQ level) is unchanged.
