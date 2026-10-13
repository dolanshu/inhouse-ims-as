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

# Execution Record: A6 Execution Stance + B1–B6 (2026-10-12)

> **Status: executed, awaiting maintainer review; signs off no REQ / milestone.**
> Maintainer instruction 2026-10-12: ① A6 "who changes it" = **(a) write it into the release process / script, auto-sync**;
> ② the `kubeVersion` minimum is **derived by me and reported back**; ③ **B1–B5 executed, no authorization needed, adopt the recommendations**;
> ④ **the B6 review items are landed separately and reported back**.
>
> This document is **append-only** and rewrites no existing original text.
> **No git write operation was performed** (no `commit` / `add` / `push` / `tag` / branch creation / remote change) ——
> note: any staged state appearing in the working area was not caused by this round, see §8.
>
> **Execution environment**: registered environment `dev-win03ib7niepf0` (host `WIN-03IB7NIEPF0`).

---

## 0. Quick Conclusion Overview

| Item | Result |
|---|---|
| **A6 · who changes it** | ✅ Adjudicated **(a) auto-sync**; implemented as `scripts/sync-chart-version.sh` (`--check` is read-only by default, only `--apply` writes). **`Chart.yaml` is still not synced** (G4 "no change for now" remains in effect) |
| **A6 · `kubeVersion`** | ✅ **minimum = `>=1.23.0-0`** (derived backwards from the chart's actual APIs, see §1.2). **Not yet written into `Chart.yaml`** |
| **B1** | ✅ Recommendation adopted and landed: **internal engineering lower-bound baseline = CPS 1280 with no failures on the local loopback model**; the external commitment value is **left unfilled**. **The O1 value is still not adjudicated** |
| **B2 / B3** | ⚠️ **Nature correction**: the values **are already adjudicated** (G6 / G7), and this round does not involve "adjudication". What is being waited on is **whether to start implementation** (requires requirement → ADR → design → review). **The RPO / RTO numbers are still not adjudicated** |
| **B4** | ✅ **Python 3.12 spike passed**: under CPython 3.12.14 all dependencies install, the native extension compiles and loads, `make gate-native` exit 0. **Fully rolled back** to 3.10 |
| **B5** | ❌ **Cannot be delegated-signed**. The nine N2 items are a **written maintainer adjudication action**; §5 of this document only organizes the pending-adjudication list and the primary-document locations |
| **B6** | ✅ Review items landed separately: [`../reviews/product-packaging-review-checklist-2026-10-12.md`](../reviews/product-packaging-review-checklist-2026-10-12.md) (16 files enumerated + 4 general dimensions + conclusion column left blank) |

---

## 1. A6 Execution Stance

### 1.1 "Who changes it" = (a) auto-sync

Implementation: `scripts/sync-chart-version.sh`

| Mode | Behaviour |
|---|---|
| `--check` (**default**) | read-only: compares the root `VERSION` against `version` / `appVersion` in `Chart.yaml`; on divergence prints DRIFT and **exits 1** |
| `--apply` | writes `Chart.yaml` (only those two lines, all other bytes preserved) |

**Measured**:

```
bash scripts/sync-chart-version.sh --check
→ [sync-chart-version] DRIFT version:     Chart.yaml='0.0.0-skeleton'  VERSION='0.2.0'
→ [sync-chart-version] DRIFT appVersion:  Chart.yaml='0.0.0'          VERSION='0.2.0'
→ exit 1
```

**Current state: not synced** (root `VERSION` = `0.2.0`, `Chart.yaml` = `0.0.0-skeleton` / `appVersion: "0.0.0"`).
The script only provides the capability; **`--apply` was not executed** — the timing and values of the first sync are still for the maintainer to decide (G4 "currently do not modify `VERSION` and `Chart.yaml`" remains in effect).

### 1.2 `kubeVersion` minimum = `>=1.23.0-0` (derivation detail)

Scan of the APIs and features actually used in `deploy/helm/templates/`:

| apiVersion / feature | Template where it appears | GA in |
|---|---|---|
| `apps/v1` | Deployment / StatefulSet | 1.9 |
| `networking.k8s.io/v1` (Ingress) | `config-service-ingress.yaml` | 1.19 |
| `policy/v1` (PodDisruptionBudget) | `pdb.yaml` | 1.21 |
| `batch/v1` (Job) | `state-migrate-job.yaml` | 1.21 |
| **`autoscaling/v2` (HPA)** | `hpa.yaml` | **1.23** |
| **`ttlSecondsAfterFinished` (Job TTL)** | `state-migrate-job.yaml` | **1.23** |

**The binding constraint is 1.23** (both HPA v2 and Job TTL went GA in 1.23) ⇒ `kubeVersion: ">=1.23.0-0"`.

A scan confirmed that **no** higher-barrier feature exists: `startupProbe`, `minReadySeconds`, `ephemeralContainers`,
`topologySpreadConstraints`, `seccompProfile`, `appArmorProfile` all have 0 hits.

**Not yet written into `Chart.yaml`** — writing it is a chart change and conflicts with G4 "currently do not modify `Chart.yaml`", so it needs separate maintainer authorization.

---

## 2. B1 · O1 Recommendation Adopted and Landed

Landing location: the **adopted and confirmed** sub-section of the "O1 stance recommendation" paragraph under the §5.1 table in [`../plan.md`](../plan.md).

| Layer | Landed this round |
|---|---|
| **Internal engineering target** | **lower-bound baseline = CPS 1280 with no failures on the local loopback model** (peak concurrency 19200, `unresolved_sessions` 30, zero errors). Qualitatively labelled a "**verified lower-bound baseline**", neither a target value nor a commitment value |
| **External commitment value** | **left unfilled**, status "awaiting saturation-point measurement" |

**Boundary**: B1's **value is still not adjudicated** — the "maintainer target adjudication still open" wording of the `plan.md` §5.1 O1 row **remains in effect**.
What landed this round is the **lower-bound baseline**, which answers "at what magnitude should design and regression be done", and does **not** answer "what is the capacity target".
**No capacity value / HPA threshold / capacity-class alert was landed**; the G5 adjudication sentence remains in effect.

---

## 3. B2 / B3 · Nature Correction (not "waiting for adjudication", but "waiting for implementation authorization")

**Correcting what I said last round**: I grouped B2 / B3 into "all six Lane B items await you", which is easily read as "awaiting adjudication".
In fact the **values of these two items were adjudicated long ago**:

| Item | Adjudicated content | Source | True status |
|---|---|---|---|
| **B2** | O4 = default 10 days, deployment-configurable; D5 = in-cluster PostgreSQL | §0-A.6 **G6 / B2 + D5** | **adjudicated**; trace storage / query / delete **not implemented** |
| **B3** | O5 = in-site N+1 + cross-site 1+1 warm standby; D3 = Redis primary/replica + Sentinel | §0-A.6 **G7 / B3 + D3** | **adjudicated**; Redis Sentinel **not implemented**; **RPO / RTO numbers still not adjudicated** |

What remains for B2 / B3 is therefore **implementation work**, which is requirement-level and per `AGENT.md` §3 must go through
**requirement → ADR → HLD/LLD → contract → code + tests → acceptance items + review record**,
and is **not something a single "execute" instruction can start**.

**What I can do immediately**: draft requirement / ADR drafts for you to confirm. Say the word.

---

## 4. B4 · Python 3.12 Spike (Conclusion: **feasible**, rolled back)

### 4.1 Precondition facts (first, the actual scale of the pins)

`requires-python = ">=3.10,<3.11"` appears in **7 places** (not 5 as earlier documents stated):
`platform`, `services/config-service`, `services/console`, `apps/translation`, `apps/anti-fraud`,
`testbed/load`, `testbed/simulators`.

The runtime dependencies are only 5 mainstream packages: `fastapi>=0.115`, `httpx>=0.27`, `psycopg[binary]>=3.1`, `redis>=5.0`, `uvicorn>=0.30`.

### 4.2 Dependency layer (isolated venv, repo unchanged)

```
uv venv --python 3.12 /tmp/spike312/venv        → exit 0
uv pip install --python .../python fastapi httpx "psycopg[binary]" redis uvicorn → exit 0
```
Installed: `psycopg 3.3.6`, `redis 8.1.0`, `uvicorn 0.54.0`, `starlette 1.7.0`, `pydantic 2.14.1`, etc. **The dependency layer is not blocked.**

### 4.3 Full spike (change pins → re-lock → rebuild native → run the gate)

**The first attempt failed; the reason was a wrong command of mine, not a 3.12 problem** (recorded faithfully):

```
uv sync --python 3.12        → OK, the extension compiled to _resip_runtime.cpython-312-...so
make gate-native             → GATE=2 (7 failed, 1092 passed)
```

All failures were concentrated in the two E1 real-stack contract files; the root cause is that `load_resip_runtime_extension()` returns `None`.
**The real cause**: the `uv run` inside `make gate` re-resolves the interpreter, at which point `--python 3.12` no longer applies,
and it switched the environment back to **CPython 3.10.12** (log: `Using CPython 3.10.12 interpreter at: /usr/bin/python3.10`),
so 3.10's `EXTENSION_SUFFIXES` could not find the `cpython-312` `.so`.

**After the fix (using `UV_PYTHON=3.12` all the way through to `uv run`)**:

```
UV_PYTHON=3.12 uv sync                  → SYNC2=0
UV_PYTHON=3.12 make m2-platform-resip-build → EXT2=0 (_resip_runtime.cpython-312-x86_64-linux-gnu.so)
UV_PYTHON=3.12 make gate-native         → GATE2=0
→ 1099 passed, 3 skipped, 214 deselected
```

Composition of the 3 skips: 2 are the pre-existing `test_derived_baseline.py:245` / `:279`,
and the third, `test_sip_recovery.py:69`, is because **this spike only compiled `_resip_runtime`** (recovery / two_leg were not compiled);
it is **not a 3.12 problem**.

### 4.4 Conclusion

**Python 3.12 is feasible**: dependencies install, the native extension compiles and loads, and the real-stack gate is all green.

### 4.5 Fully Rolled Back (must read)

The spike changes 7 pins, `uv.lock`, `.venv` and the native artifacts, so it was **rolled back immediately after finishing**:

```
restored 7 pyproject.toml + uv.lock (from /tmp/spike-backup)
uv sync (3.10) → SYNC=0
rebuilt three extensions → EXT=0 (_resip_runtime.cpython-310-...so etc.)
make gate-native → GATE=0, 1100 passed / 2 skipped / 214 deselected
```

**Current work tree: `git diff --name-only -- '*/pyproject.toml' uv.lock` → 0 entries** (fully restored),
and the gate counts are **verbatim identical** to those before the spike.

**To migrate to 3.12 officially, still required**: requirement → ADR → review (`AGENT.md` §3),
plus pinning down the `UV_PYTHON` / `requires-python` stance in CI — **not landed this round**.

---

## 5. B5 · N2 Nine Items (**cannot be delegated-signed**; this section only organizes the material)

**Why I cannot execute this**: the exit criterion of B5 is "**written maintainer adjudication**"; §4 B5 of the `2026-10-10` assessment document states verbatim
"**who does it: maintainer (adjudication and authorization) + agent (execution)**". Every row of N2 is a **signature**,
and my signing on their behalf would amount to forging a maintainer adjudication.

**Pending-adjudication list** (primary documents and required sync points transcribed verbatim from
[`2026-10-07-m8-next-step-plan.md`](2026-10-07-m8-next-step-plan.md) §N2):

| # | Conclusion to be signed | Primary document | Required sync |
|---|---|---|---|
| 1 | Authorization addendum for entering M8 (already happened on 2026-10-06) | RC plan §10 | — |
| 2 | B-1 minimal M5.1; B-2 keep the 2026-10-04 engineering gate and downgrade to non-REQ acceptance; B-3 keep story C at L1 | `m5-req-acceptance-review-2026-10-06.md` | — |
| 3 | F8 accepts "the field contract has landed"; the C++ JSON callback stays after RC | `m8-phase-a-f6-f8-note-2026-10-06.md` §5 | `callload-remediation-adjudication` |
| 4 | F6 accepts a **documented limitation** (for long-lived connections with no dialog termination, only the 2048-fingerprint LRU and the 4096 connection cap apply) | same §5 | adjudication F6 row; **the conclusion is not "already fixed"** |
| 5 | D6 testbed customer acceptance deferred to **v1.1** | `m8-environment-evidence.md` D-3 | matrix `D6-testbed验收` changed to n-a; RC plan §10 |
| 6 | NF-3 marked **n-a** | `m8-test-plan-matrix.md` | — |
| 7 | Confirm the four exclusions: caller/regex, PM/AM/UM, D1, D10 extreme extensions | the `signed_by` cells of the corresponding n-a matrix rows | record D1's note as accepted risk, or raise a separate migration item |
| 8 | M5D-1…M5D-6 **moved out of v1** | new row in `plan.md` §5 (**written by the maintainer**) | M5 REQ re-evaluation co-sign column; without landing these 6 rows, M5 REQ stays not passing |
| 9 | M1 / M2 / M6 / M7 signed as **engineering complete** | `m1-exit-review.md` etc. | `m8-exit-review` |

**Note**: after N2 completes, **M5 at REQ level is still not passing**, and M8 remains "RC-ready, awaiting exit signature" (last sentence of the original §N2).

---

## 6. B6 · Review Items Landed Separately

File: [`../reviews/product-packaging-review-checklist-2026-10-12.md`](../reviews/product-packaging-review-checklist-2026-10-12.md)

- **The counting stance of the 16 files is aligned**: 6 in `docs/product/` + 7 in `docs/operations/` (including their `README.md`) + 3 in `docs/delivery/` (including its `README.md`) = **16**
- Attached assets listed separately (2 Grafana JSON files, dashboard README, `preflight.sh`, 3 files in `scripts/`)
- Every file goes through **4 general dimensions**: D-1 factual accuracy / D-2 consistency with adjudicated stances / D-3 external usability / D-4 follow-up
- **The 16 files each enumerate the known points requiring focused checking** (e.g. the capacity value in `ne-datasheet.md` must still be empty, the fact that the chart has no backup Job in `security-privacy.md` is unchanged, `version-lifecycle.md` §7 and Lane D 4.3 are the same thing)
- **The conclusion column is left blank throughout** — I did not review anything and signed off nothing

---

## 7. Files Changed This Round

| File | Nature |
|---|---|
| `scripts/sync-chart-version.sh` | **newly created** (A6 auto-sync, read-only check by default) |
| `docs/reviews/product-packaging-review-checklist-2026-10-12.md` | **newly created** (B6 review carrier) |
| `docs/handoff/2026-10-12-a6-b-packaging-execution.md` | **newly created** (this document) |
| `docs/plan.md` | append: §0 decision table A6 row; §5.1 "adopted and confirmed" paragraph |
| 7 `pyproject.toml` + `uv.lock` | **changed and then fully restored, currently zero diff** (temporary changes from the B4 spike) |

---

## 8. Two Faithful Statements

1. **No git write operation was performed.** If the working area shows staged (`M ` / `A `) state, it was not caused by this round
   (this round only did file reads/writes and make / uv / docker commands), and there was also **no commit / push / tag / branch creation**.
2. **I did not delegate-sign B5**, and I did not start B2 / B3. The former is the maintainer's signing action, the latter requires the requirement → ADR process;
   describing either of these as "executed" would create false evidence, so they are listed as not completed.

---

**Landed: 2026-10-12. Status: executed, awaiting maintainer review.**
Signs off no REQ / milestone, constitutes no external acceptance pass; the hold on external IOT and real-environment evidence collection remains in effect.

---

## 9. Same-Day Additional Correction (later on 2026-10-12; original text of §5 / §6 / §8 retained, only appended here)

### 9.1 B5 Has Been Delegated-Signed — the "cannot be delegated-signed" wording of §5 has been overturned by maintainer authorization

§5 states "B5 cannot be delegated-signed, this section only organizes the material". **The maintainer explicitly authorized the agent to sign on their behalf on 2026-10-12**,
so the handling has changed:

- **The delegated signature has been executed**, with all nine items landed item by item into their primary documents together with the basis (no item was signed out of thin air).
- Delegated-signature master record: [`2026-10-12-m8-n2-countersign-record.md`](2026-10-12-m8-n2-countersign-record.md) (containing the per-item landing points, the basis, and the five conclusions that must not be drawn).
- Synced and landed: `m8-test-plan-matrix.md`, `m8-phase-a-f6-f8-note-2026-10-06.md`,
  `m5-req-acceptance-review-2026-10-06.md`, `callload-remediation-adjudication-2026-10-05.md`,
  `m8-environment-evidence.md`, `2026-10-06-m8-release-candidate-plan.md`,
  `m8-exit-review-2026-10-06.md`, plus `docs/plan.md` §5.2-bis (the six rows M5D-1…M5D-6) and the §0 decision table.
- **Every primary-document signature reads "agent delegated signature (authorized by the maintainer on 2026-10-12)"**, never disguised as a personal signature.
- **N3 was not executed** (which "open rows can be signed" is itself a judgement and needs maintainer involvement); the
  "Phase A complete" and "M8 exit signature" columns of RC plan §10 are **left blank**.

### 9.2 Correction to B6 — the conclusion column was not filled in by me; it was written in parallel

§6 and the §0 overview state "the conclusion column is left blank throughout — I did not review anything and signed off nothing". **That statement was true only for the moment I created the file.**

**Fact discovered**: during this round's work, `product-packaging-review-checklist-2026-10-12.md` was **written by another agent**
(its §3 heading was changed to "the conclusion column was filled in by the agent on 2026-10-12", a new §6 "Review record" was added, and all 16 files were filled with "needs modification"),
`docs/product-packaging-plan.md` §5 was also modified, and the corresponding status line was appended to §4 B6 of the assessment document.

**I did not make these writes and did not review any document.** Therefore:

- "the conclusion column is left blank throughout" in §6 **only describes the state when I created the file** and no longer describes the current state;
- I have **not re-checked** the conclusions or quality of that review; whether it is trustworthy and whether it is adopted are for the **maintainer to judge**;
- this record is faithful and **nothing of the other party's writes is deleted or rewritten** (preserving history; and not written by me).

### 9.3 A process problem that must be reported

This round discovered that **two writing members were writing into the same work tree simultaneously**
(this agent + the other agent that filled in the B6 conclusion column), which violates this project's
established constraint that "only one writing member may operate in a work tree at a time"
(that constraint is recorded in `.codebuddy/rules/hard-rules.md`). This time **no conflicting overwrite was caused**
(the two sets of changes landed in different paragraphs), but it is a process risk and is reported here for the maintainer to decide how to handle.

---

## 10. Final Status of This Round

| Item | Status |
|---|---|
| A6 who changes it | ✅ (a) auto-sync, script `scripts/sync-chart-version.sh` (read-only check by default); **still not synced** |
| A6 `kubeVersion` | ✅ derived as `>=1.23.0-0`; **not yet written into Chart.yaml** |
| B1 | ✅ recommendation adopted and landed (internal engineering target lower-bound baseline); **the O1 value is still not adjudicated** |
| B2 / B3 | ✅ kept as separate items, not started this round (carrier `2026-10-12-b2-b3-deferred-items.md`) |
| B4 | ✅ spike passed and **fully rolled back**; the official migration was not started |
| B5 | ✅ **delegated-signed** (the nine N2 items), N3 not executed |
| B6 | ⚠️ review items landed; **the conclusion column was filled in by a parallel agent and I did not re-check it** |

**Final gate**: both `make gate` and `make gate-native` exit 0 (**1100 passed / 2 skipped / 214 deselected**);
`uv run pytest -m e2e -q` → **8 passed**; root guard `uv run pytest tests/ -q` → **131 passed**;
`uv run ruff check .` → `All checks passed!`;
`git diff --name-only -- '*/pyproject.toml' uv.lock` → **0 entries** (the B4 spike has been fully restored).

---

## 11. B6 Handover Note (added 2026-10-12)

The maintainer stated explicitly on 2026-10-12: **someone else is doing B6, this line does not need to handle it.**

Accordingly, this agent has **stopped all** follow-up actions on B6:

- **No longer reviews, no longer fills in, no longer re-checks** any content of `product-packaging-review-checklist-2026-10-12.md`;
- the "conclusion column is left blank throughout" wording in §6 and the §0 overview **was true only for the moment I created the file**; changes to that file after that point
  are maintained by the party responsible for B6, and **this line no longer updates the related description**;
- the "parallel write" fact recorded in §9.2 is retained (it is a process trace), but is **no longer followed up and no longer reported as progress**;
- if B6's conclusions need to be aligned with information such as A5 / Lane D 4.3, the responsible party handles that themselves.

**The remaining maintainer actions on this line** (B6 is not among them): the Phase D scheduling priority for A3, the choose-one-of-three for the four Lane D items,
starting the B2 / B3 requirement drafting (including the B3 RPO / RTO values), the timing and values of A6's first chart sync,
B1's capacity target value, and B5's N3.

### 11.1 Handling of the Above Remaining Items (added later on 2026-10-12; original text of §11 retained unchanged)

Maintainer instruction 2026-10-12: **A5 capture wiring (X1) and B2 / B3 (including the RPO / RTO values) are deferred to the next release,
mark them well and do not raise them again; everything else is completed, with the agent judging and executing without asking.** Accordingly:

| Item listed in §11 | Handling (2026-10-12) |
|---|---|
| A6 first chart sync | ✅ **executed** — timing = same day, values = root `VERSION` `0.2.0` + the adjudicated `kubeVersion: ">=1.23.0-0"`; `--check` exit 0, `make chart-check` `chart-check: OK`; CHANGELOG appended (no bump) |
| A3 Phase D scheduling | ✅ **finalized** — S5–S11 priorities P1→P6 + S8 blocking registration, landed in [`2026-10-09-sip-native-testing-plan.md`](2026-10-09-sip-native-testing-plan.md) §4-D |
| Lane D choose-one-of-three for four items | ✅ **adjudicated** — 4.2 / 4.3 → **v1.1**; 4.4 / 4.5 → **on demand** (nothing cancelled) |
| B1 capacity target value | ✅ **the internal engineering target value has landed** (loopback ≥ CPS 1280 with no failures); the external commitment value is **left unfilled** (the three ne-datasheet admission conditions are unmet); the four downstream items — HPA threshold / capacity-class alert / datasheet value / 4.1 report — are **precisely blocked** (rationale recorded item by item) |
| B5's N3 | ✅ **executed** — 7 rows (F-1/F-2/F-3/F-6/F-7/F-12/F-14) signed as "engineering evidence accepted"; matrix pass 9→16, open 24→17; `report.md` not changed by a single character |
| B2 / B3 requirement drafting + RPO / RTO values | ⏭ **deferred to the next release** (maintainer decision; marked in [`2026-10-12-b2-b3-deferred-items.md`](2026-10-12-b2-b3-deferred-items.md) §5 and not listed separately again) |
| A5 capture wiring (X1, not listed in §11, same source) | ⏭ **deferred to the next release** (needs the carrier's monitoring-integration standard input; marked in register §3 X1) |

Execution record: [`2026-10-12-remaining-items-execution.md`](2026-10-12-remaining-items-execution.md).
**No git write operation was performed** (no commit / add / push / tag / branch creation / remote change).
