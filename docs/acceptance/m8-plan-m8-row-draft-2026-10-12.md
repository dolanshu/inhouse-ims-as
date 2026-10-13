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

# Write-back draft for the `docs/plan.md` M8 row (M8 batch 6 / E-3, 2026-10-12)

## 0. Nature

This document is a write-back **draft**; `docs/plan.md` is **completely unmodified**. This draft must be confirmed by maintainers before a maintainer or an authorized agent executes it. This batch performed no git write operations. Execution environment: `dev-win03ib7niepf0`.

## 1. Recommendation one: §0 "Current in-progress step" cell

Recommendation: append the following complete text at the end of that cell, without changing existing content:

> **Added 2026-10-13**: M8 internal-version close-out was completed by batches 1–6 (complete functionality + simulator evidence + reproducible build artifacts; matrix terminal state pass 27 / defer 4 / blocked 9 / n-a 9 / open 0 / fail 0, all under the "engineering evidence accepted" criterion); **the M8 exit sign-off is still unsigned** and still ranks after closure of external hard dependencies (S-2 / S-3, NF-1, the ADR-0008 drill, D12/O5-HA). See [`../reviews/m8-internal-release-exit-review-2026-10-12.md`](../reviews/m8-internal-release-exit-review-2026-10-12.md) for the internal-version close-out review.

## 2. Recommendation two: §0 "Product decision record" table

Recommendation: add one row (appended, existing rows unchanged):

| Date | Decision | Direction | Basis |
|---|---|---|---|
| 2026-10-13 | **M8 internal-version close-out complete (not the M8 exit sign-off)** | Batches 1–6 all landed (release and packaging / SIP comparison / kind-sim evidence / sign-off and review / performance and capacity / documentation and reporting); matrix terminal state pass 27 / defer 4 / blocked 9 / n-a 9 / open 0 / fail 0 (criterion = engineering evidence accepted); VERSION stays `0.2.0` with no bump, CHANGELOG gains an internal build entry inside the `[0.2.0]` section, image tag `as-platform:0.2.0-internal-<date>`, chart not synced; **M8 is not signed**. **Must not be inferred from this row**: M8 signed off / released / the O1 external value filled in | [`report.md`](report.md) §0.10 (batch 6 / E-1); [`../reviews/m8-exit-review-2026-10-06.md`](../reviews/m8-exit-review-2026-10-06.md) §3.2 (batch 6 / E-5); [`../reviews/m8-internal-release-exit-review-2026-10-12.md`](../reviews/m8-internal-release-exit-review-2026-10-12.md); the "M8 batch 4 terminalization countersignature (2026-10-13)" section of `m8-test-plan-matrix.md`; `(verified, docs/acceptance/artifacts/m5/2026-10-12/PASS-e6-packaging-recheck-2026-10-12.txt, 2026-10-12)` |

## 3. Recommendation three: "Status" column of the M8 row in the §4 milestone table

| Original | Recommended value |
|---|---|
| **RC artifacts ready; exit sign-off still on hold (2026-10-07)**. M7.1 engineering close-out done. Still to be revisited after the pre-Close restrictions are lifted … Original status: RC ready, awaiting maintainer exit sign-off (2026-10-06) | **Internal-version close-out complete (2026-10-13)**: complete functionality + simulator evidence + reproducible build artifacts; matrix terminal state **pass 27 / defer 4 / blocked 9 / n-a 9 / open 0 / fail 0** (the sign-off criterion is uniformly "engineering evidence accepted", not REQ-level acceptance). **The M8 exit sign-off is still unsigned** — it ranks after closure of external hard dependencies (S-2 / S-3, NF-1, the ADR-0008 drill, D12/O5-HA). **Original status: RC artifacts ready; exit sign-off still on hold (2026-10-07)** |

Basis: `(verified, "M8 batch 4 terminalization countersignature (2026-10-13)" section of docs/acceptance/m8-test-plan-matrix.md, 2026-10-13)`; `(verified, docs/acceptance/artifacts/m5/2026-10-12/PASS-e6-packaging-recheck-2026-10-12.txt, 2026-10-12)`; internal-version close-out review [`../reviews/m8-internal-release-exit-review-2026-10-12.md`](../reviews/m8-internal-release-exit-review-2026-10-12.md).

## 4. Boundaries

1. This draft does not change a single line of `docs/plan.md`.
2. The final wording of the M8 row is confirmed by maintainers.
3. This draft does not sign M8, does not sign any REQ, and does not claim M8 is all green.
4. The internal version is not a release; nothing was tagged, and the O1 externally committed value remains unfilled.
5. This batch performed no git write operations; how to split the commits is maintainers' decision.
6. The execution environment is fixed to `dev-win03ib7niepf0`.

> **Status 2026-10-13**: this draft was adopted by maintainers and execution authorized; the M8 row was adjusted per **path C** (M8 exit sign-off plus written acceptance of external hard dependency risk), and the write-back has landed in `docs/plan.md`. This draft is retained as an archive.
