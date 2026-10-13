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

# M8 release candidate — execution plan (2026-10-06)

> **Status**: **in progress** (the maintainer authorized entry into M8 on 2026-10-06)  
> **Basis**: §4 of [`plan.md`](../plan.md) (M8 definition), [`2026-10-05-milestones-engineering-complete.md`](2026-10-05-milestones-engineering-complete.md), [`2026-10-05-callload-review-response-plan.md`](2026-10-05-callload-review-response-plan.md), [`test-plan.md`](../acceptance/test-plan.md), AGENT.md §3.1 / §14  
> **Single backlog (the tail items of the callload review)**: the tracking table in §4 of [`callload-remediation-adjudication-2026-10-05.md`](../reviews/callload-remediation-adjudication-2026-10-05.md) — this plan **does not duplicate** it by opening a third engineering line.

---

## 1. What M8 is / is not

| M8 **is** | M8 **is not** |
|-----------|---------------|
| A **REQ / test-plan** sign-off run backed by evidence | a new functional milestone (no default expansion of the PRD scope) |
| The closing stage for the **maintainer milestone exit** (M1/M2/M6/M7) and for **M8's own** sign-off | redoing the M2–M7 **engineering closure** (already done; see §4 of `plan.md`) |
| Refreshing **`docs/acceptance/report.md`** (the M8 release candidate report) | publishing an external SLA / commercial O1 number (still constrained by AGENT.md §2 and plan §5.1 O1) |
| Unifying the product version across **VERSION / CHANGELOG** (F15) | the Pre-M8 **full** customer demo (Story C is still constrained by F10; see [`pre-m8-demo-review-plan.md`](pre-m8-demo-review-plan.md)) |
| M5 **REQ-level** evidence and full-chain remediation (if the maintainer adopts the full-chain review) | automatically overturning the 2026-10-04 M5 **engineering closure** artifacts (unless the maintainer explicitly reopens them and leaves an adjudication record) |

**Definition of done (the table in §4 of `plan.md`)**: an item-by-item acceptance report + a complete document chain + a unified product version.

---

## 2. Entry conditions (already satisfied)

| Condition | Evidence |
|-----------|----------|
| M0–M5 engineering closure; M2/M6/M7 engineering complete | the milestone table in §4 of `plan.md` |
| The product native / M6 / M7 engineering slices are on `master` | [`2026-10-06-callload-merge-to-master.md`](2026-10-06-callload-merge-to-master.md) |
| The default local gate can go green | `make gate` (baseline: 964 passed, 2 skipped, 2026-10-06) |
| callload P0 and most P1 are closed | [`callload-remediation-adjudication-2026-10-05.md`](../reviews/callload-remediation-adjudication-2026-10-05.md) |

---

## 3. Exit conditions (M8 closure)

Before the maintainer signs **once or per milestone**, all of the following must be satisfied:

1. **Phases A–B closed** (§4): the P1 tail items + (if applicable) the M5.1 / full-chain re-adjudication reach the REQ evidence threshold the maintainer accepts.  
2. **Phase C**: the acceptance items **within v1 scope** in [`test-plan.md`](../acceptance/test-plan.md) have traceable evidence (including the §5.4 supplementary tests; **excluding** the v1.1 calling/regex items, see §5.4 of `plan.md`).  
3. **Phase D**: the environment-type true blockers have a recorded conclusion (pass / conditional pass / explicit defer with an ADR or plan §5 row): operator PKI / public-network S-SBC, customer K8s **REQ-NF-1** live baseline.  
4. **Phase E**: `docs/acceptance/report.md` is upgraded to the **M8 release candidate report**; `VERSION` + `CHANGELOG` match the delivery; the M8 rows in §0 / §4 of `plan.md` are marked **complete**.  
5. **Review records**: the M8 final review (`docs/reviews/m8-exit-review-*.md`, filename to be created) + the milestone exit signature tables (M1/M2/M6/M7).

**"All REQs green" is not claimed** unless there is no open v1 item in the test-plan matrix and the maintainer confirms this in the M8 final review.

### 3.1 v1 acceptance scope and explicit exclusions

**Source of scope**: all REQ-* in §1–§4 of [`test-plan.md`](../acceptance/test-plan.md); the item-by-item checkboxes land in the matrix in §6 ([`M8任务草稿.md`](M8任务草稿.md) is the **REQ checklist appendix** — that file is not modified, and the matrix must be able to trace back to every one of its sections).

| Category | Included in M8 sign-off (v1) |
|----------|----------------------------|
| Functional | REQ-F-1～F-11, F-16; F-12～F-15 / NF-10 (control plane); the §5.4 supplementary test **F-15 real AS** |
| Non-functional | REQ-NF-1～NF-15 (including NF-2 dual Deployment, NF-5 simulator neutrality, NF-6～NF-8 non-goal grep, NF-11/12 version and workspace) |
| Security | REQ-S-1～S-4 |
| Governance | REQ-G-1～G-4 |
| Kernel | test-plan §5 (M2 contract/unit) — already in `make gate`; the M8 report merely **references** it |

**Not counted towards "M8 all green" unless the maintainer expands the scope** (consistent with §5.3 and §5.4 of `plan.md`):

- The complete PM / AM / UM product (the requirements are not filled in)
- REQ-F-13 **live** Call-ID tracing (M4b-7.4); calling / regex (**v1.1**)
- Python 3.10 EOL (**D1**) — a risk registration, not a default RC blocker
- Extreme owner / CAS scenarios under Redis failover; **mid-transaction** crash recovery (D10 is not extended)
- Items in test-plan **NF-3** that carry fixed capacity numbers — where this conflicts with AGENT.md §2 "no capacity numbers published before M6", the acceptance framing must be **rewritten by maintainer adjudication** or marked N/A (Phase C)

**Environment / architecture tail items**: evidence for the ADR-0008 cross-site switchover **drill** is folded into the M8 report or deferred by the maintainer; **D12 / O5** production Redis/PG HA receives **conditional sign-off** within the scope the maintainer sets (Phase B/C).

---

## 4. Phases and order (strict order)

```text
A 门禁与证据基础设施（P1 尾）
   ↓
B M5 REQ 链 / 全链Remediation（维护者拍板范围）
   ↓
C test-plan 逐条签收（含 §5.4）
   ↓
D 现场 / 运营商环境证据（可与 C 部分并行，但 NF-1/PKI 不得晚于 M8 签字）
   ↓
E 报告、版本、里程碑签字、M8 退出
```

### Phase A — Gate and evidence infrastructure (P1 tail)

**Goal**: the subsequent acceptance does not produce unreviewable conclusions under "no native gate / no structured logging".

| ID | Task | Deliverable | Verification |
|----|------|-------------|--------------|
| A-1 **F9** | **blocking** native gate | `m2-platform-resip` (+ the maintainer-approved `chart-check` / `m2-native-smoke` / `m7-*` subset) | gate green; the relevant tests **fail** when `_resip_runtime` is absent (`native_extensions.py`); CONTRIBUTING / AGENT §9 states gate vs native clearly |
| A-2 **F8** | Structured SIP runtime logging | a C++→Python JSON callback or field contract + tests | REQ-NF-13 related assertions can attach evidence |
| A-3 **F6** | transport close callback (tail item) | native behaviour + tests, or documented limitation + adjudication | update the adjudication table |
| A-4 | Document the relationship between `make gate` and gate layering | `CONTRIBUTING.md` or an acceptance appendix | the maintainer confirms the "merge gate" list |
| A-5 **REQ-G-3 / G-4** | ADR annotation scanning and blocking semantics | implement `make gate-strict` (or a preceding AST step) **or**, by maintainer adjudication, synchronously change PRD/ADR/AGENT to "not implemented" and mark N/A in the matrix | when `fast` fails, the later layers do not run; compare §7 of [`m5-full-chain-review-2026-10-05.md`](../reviews/m5-full-chain-review-2026-10-05.md) |
| A-6 **gates ②③④** | e2e / `performance` layer | if that layer already has cases, make it blocking (ADR-0015); **or** have the M8 final review accept the risk in writing | compare §2.4 of `plan.md` |
| A-7 | Native consistency before acceptance | one line in the runbook: run `make m2-platform-resip-build` before the sign-off run (and the M7 recovery/two-leg targets) | bound to the Phase C full run |

**Closure criterion**: F9/F8 in the adjudication table are "fixed", or F6 is "fixed / adjudicated risk accepted"; A-5/A-6 have a terminal state (implemented or a defer record); **only then may Phase C be started at scale**.

**Blocking note**: F9 needs maintainer approval before it can join the blocking gate (see merge handoff §6).

---

### Phase B — M5 REQ chain and full-chain remediation

**Goal**: M5 **REQ-level** acceptance and the Demo **Story C** framing can be aligned without pretending that "engineering closure = REQ pass".

| Input | [`m5-full-chain-review-2026-10-05.md`](../reviews/m5-full-chain-review-2026-10-05.md) (conclusion: does not pass) |
|------|--------------------------------------------------------------------------------------------------------|
| Maintainer decisions (**a single decision** before Phase B starts) | **B-1** whether to execute the M5.1 remediation list; **B-2** whether to keep the 2026-10-04 M5 engineering closure signature; **B-3** whether Story C is still L1 (F10) |

| Task | Explanation |
|------|-------------|
| B-4 Requirement chain repair | 7.2d ↔ PRD gap (full-chain R-1) — add the REQ or an ADR correction + a test-plan entry |
| B-5 Alerting / downscaling / onprem values | align the full-chain Major items; `chart-check` joins gate ① |
| B-6 REQ traceability in acceptance docs | attach REQ-NF-* to `m5-*.md` and the M8 section of `report.md` |
| B-7 Re-adjudication | a new review record: `m5-req-acceptance-review-*.md`, or update the status of the full-chain record |

**Closure criterion**: a written maintainer conclusion — M5 at the **REQ level** may enter test-plan check-off, or an explicit **N-item defer** written into plan §5 + the M8 final review.

---

### Phase C — test-plan sign-off

**Goal**: item-by-item **Pass / Fail / Blocked / N/A (with reason)** within v1 scope in [`test-plan.md`](../acceptance/test-plan.md).

**Working method**:

1. Export the **M8 matrix** from `test-plan.md` (see the template in §6); columns: REQ-ID, milestone attribution, evidence type, command/path, status.  
2. Parallelize by family, but **before signing** the whole matrix must have no unexplained open items.  
3. Mapping to milestone sign-off:

| Milestone | Sign-off content mainly closed in M8 |
|-----------|-------------------------------------|
| **M1** | maintainer countersignature ([`m1-exit-review.md`](../reviews/m1-exit-review.md)); no code change |
| **M2** | the REQ-S-* parts already covered on the engineering side + the operator PKI tail items; maintainer M2 exit |
| **M3** | contract replay (already in the gate); the M8 report merely references it |
| **M4/M4b** | REQ-F-12/14, **REQ-NF-10**, REQ-S-4 §1.4; §5.4: **F-13** (BLOCKED→matrix), **F-15** real AS |
| **M5** | REQ-NF-3/4/9/13/14 + 7.2d; conditional scope for **D12/O5** HA; depends on Phase B |
| **M6** | REQ-NF-15, O1 **maintainer target adjudication** (not an external publication); the HPA/`performance` gate in the last NF-15 item; maintainer M6 exit |
| **M7** | REQ-F-1～F-5 / F-6～F-11 (including the CANCEL branch, in-dialog, F-10 pass-through, races), **REQ-F-16**; E1 S1–S11, D9 forking; D10/D11 **REQ sign-off**; **REQ-NF-1** engineering harness + Phase D live |
| **Cross-cutting** | REQ-NF-2/5/6/7/8, REQ-NF-11/12, REQ-S-1, REQ-G-1/2, **O4** trace retention period (together with the NF-7 cleanup task) |

**Closure criterion**: all v1 items in the matrix are in a terminal state; Blocked must point to plan §5 or v1.1.

---

### Phase D — Environment evidence (true blockers)

From §True blockers of [`2026-10-05-milestones-engineering-complete.md`](2026-10-05-milestones-engineering-complete.md):

| # | Item | Where the evidence lands |
|---|------|--------------------------|
| D-1 | operator PKI / public-network S-SBC (the REQ-S-2/3 tail) | `docs/acceptance/artifacts/m8/<date>/req-s-*/` (redacted) |
| D-2 | customer K8s REQ-NF-1 live kill/restart/BYE | the same directory + a runbook reference |
| D-3 | **D6**: is testbed v1 customer acceptance | maintainer adjudication → closed by an ADR or a plan §5.2 row |

Items that cannot be completed inside the M8 window: M8 **must not** be claimed all-green; they require a **conditional pass** in the M8 final review with the defer list enumerated (maintainer authorization required).

---

### Phase E — Report, version, signature

| Task | Deliverable |
|------|-------------|
| E-1 | `docs/acceptance/report.md` — the main M8 release candidate report (replacing the "M1 narrative only" reader experience; the historical M1 section may be kept as an appendix) |
| E-2 | **F15**: `VERSION`, `CHANGELOG.md` |
| E-3 | the M8 rows in §0 and §4 of `plan.md` → **complete** |
| E-4 | `docs/reviews/m8-exit-review-YYYY-MM-DD.md` |
| E-5 | milestone signature table: M1, M2, M6, M7, M8 (AGENT.md §3.3 format) |
| E-6 | **release candidate packaging**: `VERSION`/`CHANGELOG`/`test_version_consistency`; the image and Helm chart are **reproducibly buildable**; re-check that there are no secrets / no real packet captures; README and runbook are consistent with the implementation such as `AS_SIP_*`/`AS_TLS_*` | NF-9, NF-11; image push/tag remains maintainer-only |

**Closure criterion**: the maintainer's M8 signature + the tag executed by the maintainer (AGENT.md §10.4).

**Non-engineering task**: callload **F11** (commit history shape) — handled by the maintainer, not in the agent queue (see the adjudication).

---

## 5. How open items are handled inside M8

| ID | Handling phase | Explanation |
|----|----------------|-------------|
| **O1** capacity target | C + E | the dev-host report already exists; maintainer **target adjudication** + whether the HPA values enter the v1 RC |
| **O3** E1 S5–S11 | C | partly covered by M7 engineering; the remaining items go into test-plan |
| **D6** testbed customer acceptance | D (decision) | v1 vs v1.1 |
| **D9** forking / race | C | M8 acceptance scope |
| **D10/D11** REQ sign-off | C + D | engineering tests already exist; NF-1 live is in D |
| **§5.4** F-13, F-15, REQ-S-4 all green | C | does not block engineering closure, but blocks the "all REQs green" claim |
| **O4** trace retention period | C | together with the NF-7 cleanup; can be signed off after freezing the number of days |
| **O5** / **D12** | B + C | in-cluster store HA/PITR; what is not covered is written as a defer |
| **ADR-0008** switchover drill | C or defer | cross-site drill evidence or an M8 final review defer |
| **REQ-G-3** | A | gate-strict, or documentation/matrix N/A |
| **REQ-NF-3** capacity number | C + E | three-way reconciliation of O1, AGENT §2 and the item |

---

## 6. M8 test-plan matrix (filled in during execution)

Copy it to `docs/acceptance/m8-test-plan-matrix.md` (the agent may generate it when Phase C starts), column definitions:

| Column | Meaning |
|----|---------|
| `req_id` | REQ-F-* / REQ-NF-* / REQ-S-* / REQ-G-* |
| `test_plan_ref` | test-plan section |
| `milestone` | M2…M7 attribution |
| `phase` | A/B/C/D |
| `evidence` | command, log path, review link |
| `status` | open / pass / fail / blocked / n/a |
| `signed_by` | maintainer + date |

---

## 7. Verification commands (baseline)

```bash
# 默认合并门禁
make gate

# Native / M7（阶段 A 后应在门禁中等价覆盖）
make m2-platform-resip-build
uv run pytest platform/tests/test_e1_contract_resip_runtime_full.py -m contract -q
uv run pytest platform/tests/test_m7_forward_two_leg_integration.py \
  platform/tests/test_req_f4_sdp_identity_integration.py -m integration -q

# M5 chart（阶段 A/B）
make chart-check

# 维护者环境（阶段 C）
# PostgreSQL 12.22 integration：见 plan §0 PG 说明
uv run pytest -m integration -q

# Kind 证据（阶段 B/C，维护者机）
make m5-kind-verify   # 按需
```

---

## 8. Tracking table (M8 level)

| Phase | Status | Target date | Note |
|-------|--------|-------------|------|
| A P1 tail + gate governance | open | | F9/F8/F6; A-5～A-7 |
| B M5 REQ | open | | awaiting maintainer B-1…B-3 |
| C test-plan | open | | matrix to be built |
| D environment | open | | PKI / NF-1 |
| E signature and release | open | | report + VERSION |

---

## 9. Related documents

| Document | Role |
|----------|------|
| [`pre-m8-demo-review-plan.md`](pre-m8-demo-review-plan.md) | customer demo boundary (F10) |
| [`m5-full-chain-review-2026-10-05.md`](../reviews/m5-full-chain-review-2026-10-05.md) | M5 REQ risk list |
| [`cross-milestone-final-adjudication-2026-10-05.md`](../reviews/cross-milestone-final-adjudication-2026-10-05.md) | engineering baseline adjudication |
| [`acceptance/report.md`](../acceptance/report.md) | carrier of the final M8 main report |
| [`M8任务草稿.md`](M8任务草稿.md) | REQ domain checklist (the matrix must cover it fully; the process is governed by this document) |
| [`callload-remediation-adjudication-2026-10-05.md`](../reviews/callload-remediation-adjudication-2026-10-05.md) | F1–F18 tail items (F9 is not "consume-only") |

---

## 10. Maintainer kickoff confirmation (to be filled in)

| Item | Maintainer | Date | Note |
|------|------------|------|------|
| Approve entry into M8 | | | |
| Phase B scope (whether M5.1 is done) | | | |
| D-3 / D6 adjudication | | | |
| Phase A complete | | | |
| M8 exit signature | | | |

---

## 10.1 Countersigned entries (2026-10-12; the original §10 table is retained unchanged, this section appends the fill-in results after it)

> **Authorization source**: the maintainer **explicitly authorized on 2026-10-12 for the agent to countersign** the nine written N2 adjudications of M8
> (item 1 of N2 has this very §10 "approve entry into M8" cell of §10 as its authoritative source; item 5's "must be synchronized" also includes this section.
> The overall countersignature record is [`2026-10-12-m8-n2-countersign-record.md`](2026-10-12-m8-n2-countersign-record.md)).
> **This section is not the maintainer's own signature**; every cell is marked "agent countersigned" and carries its basis.

| Item | Maintainer cell entry | Date | Note |
|---|---|---|---|
| Approve entry into M8 | **approved (retroactively recorded)** — signature: agent countersigned (maintainer authorization 2026-10-12) | 2026-10-12 | item 1 of N2 verbatim: "retroactive record of the authorization to enter M8 (**already happened on 2026-10-06**)". This cell **retroactively records** an already-occurred fact and does not constitute a new entry authorization |
| Phase B scope (whether M5.1 is done) | **do MINIMAL M5.1** — signature: agent countersigned (same as above) | 2026-10-12 | item 2 of N2 / B-1: scope and the DEFER list are in §1 B-1 and §9.1 of [`reviews/m5-req-acceptance-review-2026-10-06.md`](../reviews/m5-req-acceptance-review-2026-10-06.md) |
| D-3 / D6 adjudication | **(a) accept the recommendation: close D-3, handle D6 as v1.1** — signature: agent countersigned (same as above) | 2026-10-12 | item 5 of N2: D6 testbed customer acceptance **pushed to v1.1**; basis is option (a) of D-3 in [`m8-environment-evidence.md`](../acceptance/m8-environment-evidence.md); the `D6-testbed验收` row of the matrix has been moved to a terminal state accordingly (see the 2026-10-12 countersigned section of the matrix) |
| Phase A complete | left blank — see the boundary note below | — | outside the scope of the nine N2 authorizations; not countersigned |
| M8 exit signature | left blank — **unsigned** | — | the exit signature is an M8 closing action; the N2 original text states verbatim "after N2 is complete, M5 at the REQ level is still does not pass, and M8 is still 'RC ready, awaiting exit signature'" |

**Boundaries**

1. "Approve entry into M8" is a **retroactive record** (the N2 original notes that it already happened on 2026-10-06); it is **not** a new authorization, and it is not M8 completion.
2. The two cells "Phase A complete" and "M8 exit signature" are **not in the authorization list**, so they are **not filled in**.
3. The entries in this section **do not rewrite** any conclusion of the N2 original; M5 at the REQ level does not pass and M8 is "RC ready, awaiting exit signature" — **both unchanged**.
