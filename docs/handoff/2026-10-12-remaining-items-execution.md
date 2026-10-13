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

# Execution Record: Four Wrap-up Items + Two Deferred Items (later on 2026-10-12)

> **Status: executed, pending maintainer review; no REQ / milestone is signed off.**
>
> **Instruction source (maintainer 2026-10-12, semantics transcribed)**: ① The timing and value of A6's first chart sync "all that is missing is you saying when to sync and to what" — the agent judges this itself; ② A3 Phase D scheduling (setting the priority of S5–S11) — judge it yourself; ③ Lane D's four items, choose one of three — judge it yourself; ④ B2 / B3 requirement drafting + B3's RPO / RTO values — **do not do this one, defer it to the next release, mark it properly, and do not raise it again**; ⑤ B1 capacity target value + B5's N3 — judge and complete it yourself; ⑥ **Everything that needs a carrier interface to continue is deferred to the next release, mark it properly, and do not raise it again**; ⑦ **Complete everything else; all work needs no authorization — you make your own judgments, execute, and do not ask.**
>
> This document **only appends** to existing documents and newly creates this record; it **does not rewrite any existing original text**.
> **No git write operation was performed** (no `commit` / `add` / `push` / `tag` / branch creation / remote change).
>
> **Execution environment**: the registered environment **`dev-win03ib7niepf0`** (host `WIN-03IB7NIEPF0`). Execution date: 2026-10-12.

---

## 0. Conclusion Quick View

| Item | Result | Triple / Location |
|---|---|---|
| **A6 first chart sync** | ✅ **Executed**: `version: 0.2.0` / `appVersion: "0.2.0"` (the root `VERSION` is the single source) + `kubeVersion: ">=1.23.0-0"`; `--check` exit 0; `make chart-check` `chart-check: OK` | `(verified, docs/acceptance/artifacts/m5/2026-10-12/PASS-chart-version-sync-2026-10-12.txt, 2026-10-12)` |
| **A3 Phase D scheduling** | ✅ **Finalized**: S5–S11 priorities P1→P6 + S8 blocker registration | `handoff/2026-10-09-sip-native-testing-plan.md` §4-D |
| **Lane D four items, choose one of three** | ✅ **Adjudicated**: 4.2 → v1.1; 4.3 → v1.1; 4.4 → on demand; 4.5 → on demand | `product-packaging-plan.md` §5 + the Lane D section of the assessment document |
| **B1 capacity target value** | ✅ **The internal engineering target value has landed** (loopback ≥ CPS 1280 with no failures); **no external committed value is filled in** (the three admission conditions are unmet); the four downstream items are each blocked for a precise reason | appended paragraph in `plan.md` §5.1 |
| **B5's N3** | ✅ **Executed**: 7 rows signed "engineering evidence accepted"; matrix pass 9→16 / open 24→17; `report.md` unchanged by a single word | the "M8 N3 execution results" section of `m8-test-plan-matrix.md` |
| **A5 / X1 capture wiring** | ⏭ **Deferred to the next release** (requires the carrier's monitoring-integration standard input); marked, no longer itemized separately | append to register §3 X1 |
| **B2 / B3 + RPO / RTO values** | ⏭ **Deferred to the next release**; marked, no longer itemized separately | `2026-10-12-b2-b3-deferred-items.md` §5 |

---

## 1. A6 · First chart sync (timing and value decided by the agent)

### 1.1 The adjudication and what was judged independently

| Question | Adjudication (existing) | Judged independently this round |
|---|---|---|
| Who changes it | (a) written into the release process / the script syncs it automatically (`scripts/sync-chart-version.sh`) | —— already available |
| `kubeVersion` value | `>=1.23.0-0` (reverse-derived from the chart API) | —— already available |
| **Timing of the first sync** | Undecided | **Executed immediately on 2026-10-12** (maintainer instruction "all that is missing is you saying when") |
| **Value of the first sync** | Undecided | **The current value of the root `VERSION`, `0.2.0`** (single source; the chart follows it, no separate number is invented) |

**Why this value**: G4 already ruled that "the root `VERSION` is the single source"; `0.2.0` is the actual current value of `VERSION`, and the sync action merely pulls the chart into agreement with the single source without introducing a new number. **`VERSION` was not bumped** (AGENT.md §8; and there is no release action).

### 1.2 Execution and Measurement

```bash
# BEFORE（如实记录漂移）
bash scripts/sync-chart-version.sh --check
→ [sync-chart-version] DRIFT version:     Chart.yaml='0.0.0-skeleton'  VERSION='0.2.0'
→ [sync-chart-version] DRIFT appVersion:  Chart.yaml='0.0.0'          VERSION='0.2.0'
→ exit 1

# 动作 1：落入裁决的 kubeVersion（deploy/helm/Chart.yaml）
#   kubeVersion: ">=1.23.0-0"

# 动作 2：首次同步
bash scripts/sync-chart-version.sh --apply
→ [sync-chart-version] applied: Chart.yaml version/appVersion -> '0.2.0'

# AFTER
bash scripts/sync-chart-version.sh --check
→ [sync-chart-version] OK: Chart.yaml version/appVersion both = '0.2.0'   → exit 0

HELM_BIN=$PWD/tools/bin/helm make chart-check
→ helm lint deploy/helm → 1 chart(s) linted, 0 chart(s) failed
→ 全部渲染守卫（default 7 kinds / H-3 / H-4 / config-service / ingress /
  autoscaling fail-closed / stateStores / onprem）→ chart-check: OK（exit 0）
```

**Current state of `Chart.yaml`**: `apiVersion: v2` / `name: 3rdparty-as` / `version: 0.2.0` / `appVersion: "0.2.0"` / `kubeVersion: ">=1.23.0-0"` (with the reverse-derivation comment attached).

### 1.3 Collateral Actions and Boundaries

- `CHANGELOG.md`: per §7.2 of the assessment document (externally visible changes must be written back, without bumping the version), one entry was appended to the "Added" section of `[0.2.0]`.
- The evidence file `PASS-chart-version-sync-2026-10-12.txt` was created and registered in the `docs/acceptance/artifacts/m5/README.md` index table.
- **Boundaries**: ① G4's "do not modify `VERSION` and `Chart.yaml` for now" is lifted by the maintainer's 2026-10-12 instruction **only for this sync action**; it does not constitute authorization for later bumps / changes to `VERSION`; ② **"A release has been made" must not be inferred from this sync** — no tag exists and the M8 exit sign-off is still deferred; ③ the chart's **capture wiring** was not touched (X1, see §6); ④ this sync does not change the chart's fail-closed capacity key design (`autoscaling.*` etc. stay null).

---

## 2. A3 · Phase D scheduling finalized (S5–S11 priorities)

**Location**: [`2026-10-09-sip-native-testing-plan.md`](2026-10-09-sip-native-testing-plan.md) §4-D (new section; §4 original text retained).

| Priority | Scenario | REQ | One-line rationale |
|---|---|---|---|
| **P1** | S5 two-leg normalized sequence differential check | F-2 | The Wave 2 bridge capture framework is already in place; extending it to "each leg's INVITE→200→ACK→BYE→200" has the lowest cost and the most direct benefit |
| **P2** | S7a SDP pass-through corpus expansion | F-4 | The byte-identity assertion already exists in e2e; adding more media variants immediately widens D11 coverage |
| **P3** | S6 multi-rule priority + no-match combination | F-3 | The outbound-leg user-number assertion already exists in e2e and shares the simulation chain with S2 (404 already green) |
| **P4** | S10 non-2xx pass-through (486/480/408) | F-10 | The testbed peer UAS must be extended first (it currently only returns 200), so it is scheduled later because it depends on new simulation capability |
| **P5** | S9 in-dialog routing | F-9 | Depends on the M7.3 engineering slice; the in-dialog state machine has high driving complexity |
| **P6** | S11 CANCEL and final response race | F-11 | Deterministic proof of both race branches is the most expensive and carries the greatest flaky risk; closing out with a gap registration is permitted |
| **Blocked** | S8 Route/Record-Route | F-5 | The baseline itself lacks Route / Record-Route headers (the root cause of the 2 existing skips); not scheduled until the M2 probe capture is added, and REQ-F-5 is not signed as pass per the N4 stop line |

**Boundaries**: ① The scheduling **implements no test case**; starting implementation requires authorization; ② S1's 14 item-by-item header differential checks are not in this table (tracked by the wave2 register); ③ No REQ is signed off. `test-plan.md`'s REQ-F-1 boundary section (append pointer) and the native plan's Sign-off box 3 (satisfied) have been synchronized.

---

## 3. B1 · O1 capacity target value (how the agent judged it to land)

**Location**: the "O1 value settled (appended later on 2026-10-12)" paragraph in [`plan.md`](../plan.md) §5.1.

| Layer | Settled result | Basis and boundary |
|---|---|---|
| **Internal engineering target value** | **≥ CPS 1280 with no failures under the loopback model** (peak concurrency 19200, `unresolved_sessions` 30, zero errors) — promoted from a "verified lower-bound baseline" to an **internal engineering target (regression holding line)** | Measured in the 2026-10-12 saturation probe (20→1280 CPS all successful, saturation point not reached), see §4 of [`2026-10-12-o1-and-native-reproducibility.md`](2026-10-12-o1-and-native-reproducibility.md). **Internal only**: it drives the regression magnitude and engineering design; **it must not be written into any external material and must not be used as an SLA** |
| **External committed value** | **Not filled in** (status: awaiting the target-environment measurement batch) | The three "conditions for filling in a value" in ne-datasheet §3 are all unmet: ① there is no measurement of the business decision path (the accept-all harness bypasses `decide()`); ② there is no saturation point observation; ③ there is no real-cluster multi-replica / S-SBC path |

**The four downstream items stay blocked (precise reason per item, not an omission)**:

| Downstream | Precise blocking reason |
|---|---|
| HPA thresholds (M5) | Missing "a measurement batch with per-pod resource utilization (CPU / memory at load)" — the 2026-10-12 probe recorded no resource data; the `hpa.yaml` guard "Fill them from the M6 measurement, not from intuition" remains in effect; the chart's `autoscaling.*` stays null (the fail-closed design is unchanged) |
| Capacity-class alerts | No externally committable capacity anchor; the `as-alerts.yaml` file header basis "Capacity alerts are added after M6, from the measurement" is unchanged; no new `as.capacity` group |
| Capacity values in `ne-datasheet.md` | The three admission conditions are unmet; this document belongs to the B6 lane and is not edited this round (see §5 for the stale surface) |
| The 4.1 performance baseline formal report | Without a measurement of the business decision path there is no formal report; it continues to deliver only the methodology chapter |

**Why no external committed value is filled in**: the only measurement is loopback + accept-all UAS + `hold=0` + a single process, and conclusion 3 in §4 of `2026-10-12-o1-and-native-reproducibility.md` explicitly states that it "cannot support any external capacity value". Filling in an external number on the basis of that evidence would directly violate `AGENT.md` §2 and the fill-in admission conditions of ne-datasheet — **this is evidence discipline, not incompleteness**.

---

## 4. B5 · M8 N3 execution (counter-signing 7 rows as "engineering evidence accepted")

**Location**: the "M8 N3 execution results" section of `m8-test-plan-matrix.md` + §6 of [`2026-10-12-m8-n2-countersign-record.md`](2026-10-12-m8-n2-countersign-record.md).

- The **candidate rows** are the 7 rows named in the N3 original: **F-1 / F-2 / F-3 / F-6 / F-7 / F-12 / F-14**; after checking each row against the current 2026-10-12 evidence (e2e Wave 1+2, the E1 contract, `make gate-native`, the M4 engineering gate closure), open → pass was counter-signed, and every signature note reads "engineering evidence accepted" + "counter-signed by agent (maintainer authorization 2026-10-12)".
- **Counts**: matrix pass 9→16, open 24→17 (the remaining 17 rows match the N4 stop-line list row by row); blocked 10 / n-a 6 / fail 0 unchanged.
- **The N4 stop line was not crossed**: the open 24 / blocked 12 in §0.5 of `report.md` are **unchanged by a single word**; M5 still fails at the REQ level; M8 is still "RC-ready, pending exit sign-off"; not a single `- [ ]` in `test-plan.md` was ticked; no claim is made that the whole test-plan sentence is fully green.
- The sign-off scope of F-12 / F-14 is **limited to called party + prefix** (caller / regex is still n-a, v1.1).

---

## 5. Downstream Stale Registration (not edited this round, registered for follow-up)

After this synchronization, the statements "the chart is out of sync with `VERSION` / `0.0.0-skeleton`" in the following documents are **obsolete at the factual level** (historical records are retained per the record-preservation convention and are not edited back item by item; the write-back of their status is governed by this document and the location in §1.3):

| Document | Obsolete statement (example) | Ownership |
|---|---|---|
| `docs/delivery/airgap-package.md`, `docs/delivery/install-guide.md` | `Chart.yaml` `0.0.0-skeleton` is out of sync with `VERSION` `0.2.0` | B6 lane (16 packaging documents) |
| `docs/operations/rollback-playbook.md` | Same (L3 naming) | B6 lane |
| `docs/product/ne-datasheet.md`, `docs/product/version-lifecycle.md` | Same; the datasheet additionally has an "O1 undecided" statement (which should now read as "the internal engineering target value has landed, the external committed value is undecided") | B6 lane |
| `docs/reviews/product-packaging-execution-record-2026-10-10.md`, `docs/reviews/unfinished-assessment-2026-10-10-review*.md` | Factual snapshot at the registration date | Historical audit chain; not edited back |

**Recommended handling (for the maintainer to decide; out of scope this round)**: the B6 owner handles it in the next documentation synchronization batch using the "keep the original text + append a note" approach; §5 of `product-packaging-plan.md` already has an explanation of the factual-level closure appended (see that file's later-on-2026-10-12 appended block).

> **Destination pointer (appended 2026-10-13; the original text of the recommendation above is retained unchanged)**: the two classes of stale statements in the five downstream documents registered in this section
> (`docs/delivery/airgap-package.md`, `docs/delivery/install-guide.md`, `docs/operations/rollback-playbook.md`,
> `docs/product/ne-datasheet.md`, `docs/product/version-lifecycle.md`) — `0.0.0-skeleton` and "O1 undecided" —
> together with this section's recommended handling (keep the original text + append a note; whether to synchronize is for the maintainer to decide), are
> all consolidated under [`../next-release-v1.1-plan.md`](../next-release-v1.1-plan.md) **§5-1**.
> Subsequent status reviews, reports, handoffs, and new session openings that touch this item always **cite only that pointer**, do not itemize, and no longer list it as an "action for the maintainer".

---

## 6. The Two Items Deferred to the Next Release (marked, no longer itemized separately)

| Item | Where the marker landed | Basis |
|---|---|---|
| **A5 / X1 capture wiring** (annotation vs ServiceMonitor/PodMonitor) | [`2026-10-11-open-adjudication-register.md`](2026-10-11-open-adjudication-register.md) §3 X1 "adjudication written to disk (appended 2026-10-12)" + the status column of the §5 summary table + the A5 status row in §4 of the assessment document + the `plan.md` §0 decision row | Requires the carrier's monitoring-integration standard input; no side is chosen and the chart is not changed before the input arrives. **Subsequent status reviews, reports, handoffs, and session openings always cite only the pointer, do not itemize, do not remind separately, and no longer list it as an "action for the maintainer"** (same basis as §12 of the assessment document) |
| **B2 / B3** (requirement / ADR drafting + **B3's RPO / RTO values**) | [`2026-10-12-b2-b3-deferred-items.md`](2026-10-12-b2-b3-deferred-items.md) §5 + the B2/B3 status rows in §4 of the assessment document + the `plan.md` §0 decision row | Not started this round; the four startup conditions in §4 are retained as is (RPO / RTO require maintainer values and are not adjudicated on their behalf); when scheduling the next release, make the restart timing explicit |

> **Destination pointer (appended 2026-10-13; the original text of the table and of "no longer itemized separately" above is retained unchanged)**: the destinations of the two items in this table are —
> **A5 / X1 capture wiring** → [`../next-release-v1.1-plan.md`](../next-release-v1.1-plan.md) **§2** row 7 (external hard dependency class;
> restart = maintainer adjudication + the carrier's monitoring-integration standard being in place);
> **B2 / B3** → **§4-1 / §4-2** of the same document, with its four startup conditions retained as is in **§4.3** of the same document (must not start without confirmation),
> and the **RPO / RTO values** still requiring maintainer values, see **§7-4**.
> Subsequent status reviews, reports, handoffs, and new session openings that touch the leftover items in this table always **cite only that pointer**; **this table no longer itemizes them** and does not restate them one by one.

---

## 7. List of Files Written in This Round

| File | Nature |
|---|---|
| `deploy/helm/Chart.yaml` | **Modified**: `kubeVersion: ">=1.23.0-0"` (with reverse-derivation comment) + first sync of `version` / `appVersion` → `0.2.0` |
| `CHANGELOG.md` | Appended: one entry under `[0.2.0]` "Added" (no version bump) |
| `docs/acceptance/artifacts/m5/2026-10-12/PASS-chart-version-sync-2026-10-12.txt` | **Newly created** (evidence) |
| `docs/acceptance/artifacts/m5/README.md` | Appended: evidence index row |
| `docs/handoff/2026-10-12-remaining-items-execution.md` | **Newly created** (this document) |
| `docs/handoff/2026-10-09-sip-native-testing-plan.md` | Appended: §4-D scheduling finalization + Sign-off box 3 satisfied |
| `docs/handoff/2026-10-10-unfinished-assessment-and-next-plan.md` | Appended: seven status rows for A3 / A5 / A6 / B1 / B2+B3 / B5 / Lane D |
| `docs/plan.md` | Appended: 6 rows in the §0 decision record table; the "O1 value settled" paragraph in §5.1 |
| `docs/acceptance/test-plan.md` | Appended: REQ-F-1 real-stack boundary section scheduling and coverage status update |
| `docs/acceptance/m8-test-plan-matrix.md` | Appended: the "M8 N3 execution results" section |
| `docs/handoff/2026-10-12-m8-n2-countersign-record.md` | Appended: §6 N3 execution results |
| `docs/handoff/2026-10-11-open-adjudication-register.md` | Appended: §3 X1 adjudication written to disk; X1 status column updated in the §5 summary table |
| `docs/handoff/2026-10-12-b2-b3-deferred-items.md` | Appended: §5 deferred to the next release |
| `docs/handoff/2026-10-12-a6-b-packaging-execution.md` | Appended: §11.1 remaining items handling table |
| `docs/product-packaging-plan.md` | Appended: 4.2–4.5 ownership column in the §5 batch table + the later-on-2026-10-12 appended block |

---

## 8. Final Gate and Evidence

| Check | Result |
|---|---|
| `scripts/sync-chart-version.sh --check` | exit 0 (`OK: Chart.yaml version/appVersion both = '0.2.0'`) |
| `HELM_BIN=$PWD/tools/bin/helm make chart-check` | `chart-check: OK`, exit 0 (helm 3.16.4; 1 chart linted / 0 failed; all render guards passed) |
| `make gate` (ruff format --check / ruff check / mypy / `-m "unit or contract"`) | exit 0, **1102 passed / 2 skipped / 214 deselected**; both SKIPPED cases are the existing Route / Record-Route baseline gaps at `test_derived_baseline.py:245` / `:279`; not one comes from native being missing |
| `uv run pytest tests/ -q` (root guard) | **133 passed** |
| `uv run pytest tests/test_version_consistency.py -q` | **9 passed** |

Triples:

- `(verified, docs/acceptance/artifacts/m5/2026-10-12/PASS-chart-version-sync-2026-10-12.txt, 2026-10-12)`

**Not executed**: `make gate-native` (no native / product code was changed this round; the previous round already ran it successfully earlier the same day with exit 0), any `git` write operation, any `docker` / cluster action.
**No REQ / milestone is signed off**; the §0.5 counts of `report.md` are unchanged; deferring external IOT and real-environment evidence gathering, together with the deferred M8 exit sign-off, remains in effect.

---

**Write date: 2026-10-12. Status: executed, pending maintainer review.**
