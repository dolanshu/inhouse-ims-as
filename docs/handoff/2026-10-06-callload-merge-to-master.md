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

# callload → master merge preparation (2026-10-06)

> **Status (2026-10-06)**: **merged** — `master` @ `139d299` (squash; gate configuration **unchanged**); see §6 execution record.  
> **Scope**: the checklist and framing the maintainer uses before merging the `callload` engineering slice into `master` (historical record retained).  
> **Basis**: [`2026-10-05-callload-review-response-plan.md`](2026-10-05-callload-review-response-plan.md), [`callload-remediation-adjudication-2026-10-05.md`](../reviews/callload-remediation-adjudication-2026-10-05.md), [`cross-milestone-final-adjudication-2026-10-05.md`](../reviews/cross-milestone-final-adjudication-2026-10-05.md).

---

## 6. Execution record (2026-10-06)

| Step | Result |
|------|------|
| `923a8c1` on `callload` | gate configuration + merge handoff docs |
| `merge master` → `callload` | pulled in `m5-full-chain-review-2026-10-05.md` |
| `make gate` on `callload` | 964 passed, 2 skipped |
| `merge callload` → `master` | **fast-forward** → `4b4566b` |
| follow-up `764aa75` | narrowed gate trigger scope + merge record doc |
| `origin` push | first push rejected; gate configuration changes **removed**, then squash re-pushed |

## 6b. Maintainer sign-off (optional countersignature)

| Item | Maintainer | Date | Note |
|----|------------|------|------|
| Approve callload → master | maintainer chat | 2026-10-06 | |
| master SHA after merge | `4b4566b` | 2026-10-06 | includes `merge master` into `callload` |
| F10 framing read | | | Story C L1 |

---

## 1. Branch facts (at authoring time)

| Item | Value |
|---|---|
| `callload` HEAD | `dc3c951` (`fix`) |
| `master` HEAD | `04afc5a` (`M5 review`) |
| merge-base | `2318f9c` |
| Commits unique to `callload` | 7 (including `6778030`…`dc3c951`; see `git log master..callload`) |
| Commits unique to `master` | **1**: `04afc5a` — added [`m5-full-chain-review-2026-10-05.md`](../reviews/m5-full-chain-review-2026-10-05.md) (conclusion "does not pass") |
| Uncommitted working tree | gate configuration, `.gitignore` (see §2.1) |

**Merge direction**: once the maintainer approves, merge `callload` into `master` (recommended: first `merge master` into `callload` to resolve divergence, then fast-forward or merge commit into `master`).

---

## 2. Hard gates before merging

### 2.1 The working tree must be committed first

Review **F9** requires the native extension to participate in the blocking gate. Local equivalents: `make m2-platform-resip-build` + `AS_REQUIRE_NATIVE_EXTENSIONS=1 make gate`; `chart-check` / `alert-check` (M5-0c) correspond to `make chart-check` / `make alert-check`; `m2-native-smoke`, `m2-platform-resip`, `m7-recovery`, `m7-two-leg` correspond to `make m2-native-smoke`, `make m2-platform-resip-build` and the matching integration targets.

**Before merging**: commit `.gitignore` (`.cache/`, `!docs/acceptance/artifacts/`) and the other working-tree changes separately on `callload`, and pass green **at least** `make gate` + the native path after `make m2-platform-resip-build`.

### 2.2 Local verification (maintainer)

```bash
make gate
make m2-native-restore m2-native-build m2-platform-resip-build
uv run pytest platform/tests/test_e1_contract_resip_runtime.py \
  platform/tests/test_e1_contract_resip_runtime_full.py -m contract -q
# 可选：m7-platform-recovery-build / two-leg-build + 对应 integration
```

### 2.3 Content reconciliation with `04afc5a` (F10, not a git blocker)

- After the merge the repository **simultaneously** holds the M5 full-chain "does not pass" review and the Pre-M8 **Story C L1 framing** ([`pre-m8-demo-review-plan.md`](pre-m8-demo-review-plan.md) F10 section).
- The external framing **must not** change because of the merge: Story C still covers only the chart/alert **shape** plus a kind summary, and does not claim M5 full-chain acceptance.
- Update the pre-M8 F10 section only after M5.1 Remediation is closed on `cur` (unrelated to the merge).

### 2.4 Known open items (do not block the engineering merge, but do block milestone/REQ sign-off)

| ID | Status | Tracked after the merge |
|----|--------|-------------------------|
| F8 | not closed | structured logging before M8 |
| F6 | partially fixed | native transport close callback |
| F11 | maintainer | historical commit shape, do not restructure |
| M2/M6/M7 **milestone exit** | not signed off | [`plan.md`](../plan.md) §4 |
| REQ-NF-1 / all E1 / O1 publication | not accepted | M8 |

---

## 3. Suggested maintainer operation order

1. **Decide**: explicitly approve "`callload` → `master`" (AGENT.md §11).
2. **Commit** the §2.1 working tree; re-run §2.2 before rebase/merge if needed.
3. **`git checkout callload && git merge master`** (pulls in `04afc5a`); on conflict the principle is **keep both review documents**, and for code follow the callload engineering slice.
4. Once the **gate is green**, `git checkout master && git merge callload` (or PR + squash, the maintainer's call).
5. Update [`plan.md`](../plan.md) §0 "Current step in progress" — mark callload as merged; the next entry point is **M8**.
6. Optional: append a "merged into master @ `<sha>` `<date>`" line to [`callload-remediation-adjudication-2026-10-05.md`](../reviews/callload-remediation-adjudication-2026-10-05.md).

---

## 4. Post-merge statement (external / internal)

### 4.1 The merge **equals**

- `master` contains the post-M2 first-half native product runtime, the M6 harness + O1 dev-host report chain, the M7 E1/FORWARD/D10 engineering slice, the Pre-M8 demo script and review fixes (F1–F7, F9–F18 etc., see adjudication).
- Repository-root `make m2-native` / `make m2-platform-resip-build` and `AS_REQUIRE_NATIVE_EXTENSIONS=1 make gate` (once F9 lands) become the **trunk default** engineering path.

### 4.2 The merge **does not equal**

- M2 / M6 / M7 **maintainer milestone sign-off**
- M5 full-chain or M5.1 **acceptance passed**
- REQ-S-2/3, REQ-NF-1, external O1/SLA, customer NF-1 formal sign-off
- Pre-M8 **full** customer demo (the full Story C operations narrative remains constrained by F10)

---

## 5. Related documents

| Document | Role |
|----------|------|
| [`callload-m2-m6-m7-demo-branch-review-2026-10-05.md`](../reviews/callload-m2-m6-m7-demo-branch-review-2026-10-05.md) | branch review original + Adjudication table |
| [`2026-10-05-callload-review-response-plan.md`](2026-10-05-callload-review-response-plan.md) | P0/P1/P2 disposition and tracking table |
| [`2026-10-05-milestones-engineering-complete.md`](2026-10-05-milestones-engineering-complete.md) | M2/M6/M7 engineering inventory |
| [`pre-m8-demo-review-plan.md`](pre-m8-demo-review-plan.md) | customer demo boundary (includes F10) |

---

## 6. Maintainer sign-off (historical template; execution see §6 execution record at the top of this document)

| Item | Maintainer | Date | Note |
|----|------------|------|------|
| Approve callload → master | | | |
| Gate + §2.2 green | | | |
| master SHA after merge | | | |
| F10 framing read | | | Story C L1 |
