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

# Open Adjudications and Leftover Issues Register (2026-10-11)

## 0. Nature and Scope of This Document

> **This document is a "register", not an adjudication, not a plan, and not execution authorization.**

- **It only registers items that have not yet been adjudicated.** Records of already-adjudicated items remain authoritative in
  §0-A.6 of [`2026-10-10-unfinished-assessment-and-next-plan.md`](2026-10-10-unfinished-assessment-and-next-plan.md)
  and the §0 "product decision record" table of [`../plan.md`](../plan.md); this document **does not repeat** them and only registers what is **not yet adjudicated**.
- **The purpose of the register is to prevent forgetting**: work in this repository spans multiple machines and multiple sessions, and an open adjudication that is not landed is very easily mistaken in the next
  session for "already adjudicated" or "non-existent". This document gathers such dangling items into one readable place.
- **This document gives no proposal, takes no side, and recommends no leaning.** Each item only states "what the question is / why it was raised / what would be frozen without an adjudication",
  and the conclusion always reads "**awaiting maintainer adjudication**".
- **This document signs off no REQ, signs off no milestone, and constitutes no external acceptance pass.**
- **All dates are 2026-10-11** (the registration date).

### 0.1 How This Document Is Maintained

Following the existing practice of §0-A.5: once an item has been adjudicated, a line stating the adjudication result and date must be **appended** to this document and synced to
the §0 decision record table of `docs/plan.md`; **entries of this document must never be silently deleted**. Even adjudicated entries should be retained as the audit chain.

### 0.2 Numbering Convention

| Prefix | Meaning |
|---|---|
| **G9–G11** | project-level adjudications newly raised by the maintainer on 2026-10-11 (continuing the existing G1–G8 numbering, no renumbering) |
| **P1–P6** | leftover issues found on 2026-10-11 while reviewing the §0-A.6 adjudication records (Pending follow-up) |
| **X1** | items still awaiting external input (External input pending) |
| **S1** | overall work that has been scoped but not started (Scoped but not started) |

---

## 1. First Group: Newly Identified Project-Level Adjudications (from G9, raised by the maintainer on 2026-10-11; the "status" of each table/entry in this section is the current status field and is synced as adjudications are made in §7)

### G9 · Project Scope and Infra Ownership

**The question in one sentence:** is this project "a complete delivery that includes infra", or "application only"?

**Why it was raised (evidence):**

| Direction | Evidence | Location |
|---|---|---|
| supports "includes infra" | `Chart.yaml` + `templates/` (18 files) + `values.yaml` + `values-onprem.example.yaml` | `deploy/helm/` |
| supports "includes infra" | 16 `m5-*.sh` scripts (`m5-kind-up.sh`, `m5-helm-install.sh`, `m5-images.sh`, `m5-verify.sh`, `m5-issu-scale-evidence.sh`, `m5-7.2d-evidence.sh`, etc.) + `manifests/` + `certs/` + `README.md` | `deploy/kind/` |
| supports "includes infra" | the M5 closure conditions include "control-plane cluster deployment proof (including **7.2d**)" | `docs/plan.md:183` |
| supports "includes infra" | the §0 status table records that the M7.1 demo ran successfully on kind (UDP/TCP/TLS, five first-edition call types) | `docs/plan.md:15` |
| **existing wording that causes confusion** | "this machine has no helm / kubectl / kind / promtool" — easily read as "the project lacks that capability", but the original text is a **per-machine tool inventory** | table and `:104` of §1.2 in `docs/handoff/2026-10-10-unfinished-assessment-and-next-plan.md` |
| **counter-evidence one (refutes "the project lacks it")** | `promtool check rules` → `SUCCESS: 5 rules found` | `docs/acceptance/artifacts/m5/2026-10-05/alert-check-full.txt:1-3` |
| **counter-evidence one (continued)** | `chart-check: OK` | `docs/acceptance/artifacts/m5/2026-10-05/chart-check-full.txt` |
| **counter-evidence two (a switch built into the code)** | the fail-closed path when `M5_STRICT=1` and there is no `kind-as-m5` (exit=1), showing the code has long built in "judge only when there is a cluster, fail explicitly when there is none" | `docs/acceptance/artifacts/m5/2026-10-05/m5-strict-context.txt:1-4` |

> **Inference from the counter-evidence (registration, not adjudication):** there exists a machine with complete infra tooling (helm / kubectl / kind / promtool) where the run passed;
> it is simply **not the current machine**; and that machine is **unnamed** in the existing documents.

**Related existing stances (registered, not extrapolated):**

- `AGENT.md:20-28` §1: the product is a "single-tenant on-prem third-party IMS AS", triggered by an S-CSCF through a carrier S-SBC.
- `AGENT.md:30-52` §2: nine non-goals, including "configuration does not go through GitOps" (`:48`) and "no Operator (CRD); use Helm + standard
  Deployment/ConfigMap/Secret" (`:51`).
- ADR-0013 (Helm-only production form, no operator dependency) — `docs/architecture/adr/README.md:29`.

**Layered registration into three items** (on the registration date all three are recorded as "awaiting maintainer adjudication"; the status fields have since been updated per §7): **〔added in this round on 2026-10-11; the previous sentence is retained unchanged〕the status fields were later updated once more in step with actual resolution — G9-b has been *resolved* and G9-c has been *downgraded* (basis in the respective status columns of the table below); neither counts as pending adjudication any more.**

| Sub-item | What must be adjudicated | What would be frozen without an adjudication | Status |
|---|---|---|---|
| **G9-a** | **deliverable boundary**: do infra assets (chart / kind scripts / cluster evidence scripts) count as **deliverables** or as **development scaffolding** | the contents list of the delivery package under `docs/delivery/`; the "what do we deliver" stance in external material | closed (2026-10-11) — see §7.1 (the deliverable-product / scaffolding dichotomy) |
| **G9-b** | **machine capability definition**: whether a (or a class of) "complete infra host" needs to be named/designated | in the existing documents such a machine is unnamed, which makes "this machine has no tools" be misread as "the project has no capability"; cluster-level work cannot be assigned to a definite environment **〔added 2026-10-11; the two columns "what must be adjudicated" and "what would be frozen without an adjudication" above are the original registration-date text and are retained unchanged〕both kinds of harm this item worried about have been resolved: ① "this machine has no tools being misread as the project having no capability" is resolved by layer 2 of §7.4 (§0 item 2 of [`docs/environments.md`](../environments.md) explicitly states "do not infer that the project lacks X from some machine not having X"); ② "cluster-level work cannot be assigned to a definite environment" is resolved by that registry (existing row `dev-win03ib7niepf0`). Therefore this item **no longer constitutes an undecided blocker**.** | **resolved (2026-10-11)** — resolved by the **tool-probing** approach of [`docs/environments.md`](../environments.md) (environment registry) + [`tools/env-probe.sh`](../../tools/env-probe.sh): the environment name is **generated on the spot** by script as `<role>-<lowercase hostname without separators>`, the hostname is **measured** by `uname -n` (no manual lookup needed), and tools are judged in **three states** ("✅ present / ❌ missing / ⚠ installed but unusable"); **naming and manual registration are no longer needed**, and the anonymous "local machine" is no longer relied upon**〔the "status" column of this table is the current status field and is synced as things are actually resolved; the registration-date status "awaiting maintainer adjudication" has been replaced by this cell, but the original text of the two columns above and the original list at §7.5 `:567` are all retained unchanged〕** |
| **G9-c** | **gate ownership**: whether cluster-level verification must be runnable on every developer machine and every PR | how the §1.2 tool table is written; the ownership of e2e and the execution premise of A4-4 | **downgraded (2026-10-11) — overlaps an already effective adjudication, not listed separately as pending adjudication** **〔added 2026-10-11; the column "what must be adjudicated" above is the original registration-date text and is retained unchanged〕rationale: ① **it overlaps an already effective adjudication** — the "must cluster-level verification run on every PR" asked by this item is the same issue as **G2 / A4-4** in §0-A.6 (whether kind e2e enters PR required), and the risk column of option A in **§8.1 ④** of [`2026-10-10-unfinished-assessment-and-next-plan.md`](2026-10-10-unfinished-assessment-and-next-plan.md) already lists "this machine has no kind" as **an inherent risk of that option**, so this item does not constitute an independent pending adjudication. Therefore this item **no longer constitutes an undecided blocker**.**〔the "status" column of this table is the current status field and is synced as things are downgraded; the registration-date status "awaiting maintainer adjudication" has been replaced by this cell, but the original text of the two columns above and the original list at §7.5 `:567` are all retained unchanged〕** |

---

### G10 · Whether a sub-repo / Repo Split Is Needed

**The question in one sentence:** do the infra assets (chart, kind scripts, cluster evidence) need to be stored separately from the application code (submodule /
sub-repo / separate repository)?

**Why it was raised (evidence):**

| Fact | Location |
|---|---|
| **there is no `.gitmodules` and no git submodule anywhere in the repo** — there are currently **no traces of a split at all** | repository root (search finds no hits) |
| the only Python lockfile is the root `uv.lock`, shared by 8 `pyproject.toml` files | root `uv.lock`; `pyproject.toml`, `platform/`, `apps/anti-fraud/`, `apps/translation/`, `services/config-service/`, `services/console/`, `testbed/load/`, `testbed/simulators/` |
| the chart is under `deploy/helm/`, the scripts under `deploy/kind/`, and the two locate each other via `REPO_ROOT` | `deploy/helm/scripts/chart-check.sh:5-6` (`REPO_ROOT` + `${REPO_ROOT}/deploy/helm`) |
| the kind script hardcodes the chart path | `deploy/kind/m5-helm-install.sh:32` (`${ROOT}/deploy/helm`) |

> **Current form (registration, not adjudication):** it is "**physically loose, tightly coupled by path strings**" — separated at the directory level but referring to each other through hardcoded relative paths.

**What would be frozen without an adjudication:** if a split is decided later, the existing path coupling and Makefile targets
(`chart-check` at `Makefile:55-56`, `m5-kind-verify` at `:65-66`, `m5-cluster-evidence` at `:62-63`,
`m5-issu-scale-evidence` at `:68-69`, `m5-7.2d-evidence`, etc.) all have to be rewritten; **the later the decision, the higher the rewrite cost**.

**Status: closed (2026-10-11) — see §7.2 (closed as "do not split the repo", keeping the single-repo form).**

---

### G11 · Whether to Keep the "application without infra" Delivery Form

**The question in one sentence:** besides the complete delivery, is a form that "delivers only the application image/code, without chart and kind infra" also to be supported?

**Difference from G9 (must be registered together, to avoid confusion):**

| | What it asks |
|---|---|
| **G9** | **what this project is right now** — does it include infra, or is it application only |
| **G11** | **whether to provide an additional form in the future** — besides the existing form, whether to add an "without infra" delivery form |

**What would be frozen without an adjudication:**

- the form of the delivery package (the content boundary of the bundle / images list under `docs/delivery/`).
- the product boundary description of `docs/delivery/`.
- the stance towards customers (whether the same product has two delivery forms, and the boundary and responsibility split of each).

**Status: closed (2026-10-11) — see §7.2 (closed as "do not declare a second delivery form").**

---

## 2. Second Group: Leftover Issues Found on 2026-10-11 While Reviewing the §0-A.6 Adjudication Records

### P1 · The Intention of the A4-4 Adjudication Awaits Confirmation (two stances are opposite)〔clarified 2026-10-11: not a contradiction, the stance is governed by G2/A4-4 in §0-A.6〕

**The question in one sentence:** is the adjudication direction of A4-4 "included in PR required" or "not included in PR required"?

**Why it was raised (evidence):**

| Location | Recorded content | Direction |
|---|---|---|
| §8.1 ④ of [`2026-10-10-unfinished-assessment-and-next-plan.md`](2026-10-10-unfinished-assessment-and-next-plan.md) | recommends "**not included in PR required**, only run manually in an environment that has the conditions" | not included |
| the **G2 / A4-4** row of §0-A.6 in the same file | "the direction of kind e2e is an E2E policy **included in PR required**" | included |
| `docs/plan.md:40` | copies the §0-A.6 stance (included in PR required) | included |

> **Additional risk (registration):** the title of §8.1 ④ is "whether kind e2e **never** enters PR required", which is a double-negative formulation
> and can be misread ("never enters" and "whether it never enters" lead to opposite conclusions). **〔Registration correction (2026-10-11, appended; the evidence table above and the original text of this paragraph are all retained, nothing deleted or changed)〕** The "two opposite stances" claimed here **do not hold**: the **G2 / A4-4** row of §0-A.6 (the second row of the table above) is an **already effective adjudication record** — the direction of kind e2e is an E2E policy **included in PR required**; §8.1 ④ (the first row of the table above) is a **recommendation** under the same issue (option B). **A recommendation being overridden by an already effective adjudication is normal process; the two coexisting do not constitute a contradiction requiring re-adjudication.** Registering this item as "awaiting maintainer adjudication" was a **registration stance error** and is hereby withdrawn; **the stance of A4-4 is governed by §0-A.6**.

**What would be frozen without an adjudication:**

- the PR gate form once combined with **A4-2** (**fail**, not skip, when a required native extension is missing) — the combination of the two directly determines
  whether a PR goes red because the environment lacks the native extension, that is, "A4-4 sets the direction and A4-2 sets the red/green stance when the extension is missing"; only the two together constitute
  the complete gate form on the PR critical path. **〔added 2026-10-11; the original text above is retained unchanged〕this item is not a blocker; the stance of A4-4 is governed by the G2 / A4-4 row of §0-A.6 (see the "registration correction" paragraph above).**

**Status: clarified (2026-10-11) — no re-adjudication needed.** The stance of A4-4 is governed by the G2 / A4-4 row of §0-A.6 (the direction of kind e2e is an E2E policy **included in PR required**, and that adjudication **is already effective**); §8.1 ④ is a **recommendation overridden by that adjudication**, and the two coexisting **do not constitute a contradiction**. The previous registration as "awaiting maintainer adjudication" was a registration stance error and is hereby withdrawn; the basis is in the "registration correction" paragraph above this item.

---

### P2 · The Open-Items Table in §5 of `docs/plan.md` Does Not Sync Adjudications

**The question in one sentence:** the adjudication results of 2026-10-10 were not written back into the §5 open-items table, so reading only §5 would wrongly judge that those items are still fully open.

**Why it was raised (evidence):**

| Location | Current state |
|---|---|
| `docs/plan.md:399` | **O4** call-trace retention period — the G6 adjudication of 2026-10-10 (default 10 days, deployment-configurable) was not appended |
| `docs/plan.md:400` | **O5** disaster recovery level — the G7 adjudication of 2026-10-10 (in-site N+1, cross-site 1+1 warm standby) was not appended |
| `docs/plan.md:410` | **D5** call-trace storage — the G6 adjudication of 2026-10-10 (in-cluster PostgreSQL) was not appended |
| `docs/plan.md:396` | **O1** — "the process is adjudicated" (the three-tier decision process) and "the value is not adjudicated" are written together as one sentence, making it hard to tell which half is settled |

> **Comparison:** rows such as `docs/plan.md:406` (D1), `:408` (D3), `:413` (D8), `:414` (D9) in the same table **all have**
> inline annotations of appended adjudications; the O4 / O5 / D5 rows do not, which is a sync omission rather than a deliberate retention.

> **Current-state correction (2026-10-11, appended; the "current state" column above and the "comparison" paragraph are retained as the original registration-date state, nothing deleted or changed):**
> the premises stated by the table above and the "comparison" paragraph **are all now void** — the four rows
> **O1 / O4 / O5 / D5 of the §5 open-items table of `docs/plan.md` now all carry an inline annotation "adjudicated on 2026-10-10 / appended, synced on 2026-10-11"**.
> The row-by-row review of 2026-10-11 confirms the line numbers `:397` / `:400` / `:401` / `:411` are still accurate (no further drift). The essentials of the four annotations:
>
> | Row | Annotation essentials (verified verbatim) |
> |---|---|
> | **O1** `:397` | "**the process is adjudicated, the value is still not adjudicated**" — the 2026-10-10 adjudication adopted the O1 three-tier decision process and required distinguishing the internal target value from the external commitment value; the "maintainer target adjudication still open" **above this row refers only to the value**, and the process must not be taken as unadjudicated on that basis; the capacity value still awaits higher-fidelity M6 measurement and maintainer adjudication, and REQ-NF-3 stays applicable and blocked |
> | **O4** `:400` | "**default retention 10 days, deployment-configurable**"; **the boundary must not be exaggerated** — trace storage / query / delete are not implemented this time, so "adjudicated" only means the value is settled and **does not mean the system cleans up after 10 days**; the cleanup trigger point and the time-origin definition remain implementation details to be defined |
> | **O5** `:401` | baseline = "**in-site N+1 + cross-site 1+1 warm standby**" (including D3 choosing Redis primary/replica + Sentinel, ADR-0008); **the boundary must not be exaggerated** — **no rack / AZ-level fault tolerance is promised**, and **the RPO / RTO numbers are still not adjudicated** |
> | **D5** `:411` | selection = "**in-cluster PostgreSQL**"; Redis continues to be used for runtime checkpoint; **the boundary must not be exaggerated** — **implementation not landed**, and the fact recorded in §4.1 of `security-privacy.md` that the chart has **no backup Job** is unchanged |
>
> Three points must be remembered together, otherwise a secondary error of deriving "already resolved" from "already synced" follows:
>
> 1. **The annotations of all three rows O4 / O5 / D5 explicitly state "this row still has the nature of 'blocking downstream documents'"**, and state that "**it must not be marked 'resolved' just because the adjudication has been made**"
>    — that downstream sync (task E) has also been landed; see the current-state correction of the §2 P3 entry.
> 2. **The annotation of the O1 row does not contain** the above "blocking downstream documents" statement; what it says is **the value is still not adjudicated**; hence the substantive status of O1 **is unchanged**.
> 3. The annotations themselves already put "the adjudication conclusion of the value, the boundary of the landing, and the remaining dependencies" in the same row — the specific harm claimed by this entry,
>    "reading only §5 would wrongly judge that those items are still fully open", **has been resolved**, but the **substantive undecided parts of the four rows are not thereby closed**
>    (implementation not landed / RPO·RTO not adjudicated / O1 value open), and their tracking carrier is precisely those four annotations.

**What would be frozen without an adjudication:** the open-items registration surface (§5) required by §15 of `AGENT.md:289-291` facing the §0 decision record surface;
a reader of §5 only **no longer** wrongly judges that O4 / O5 / D5 are still **fully** open, but without knowing the "boundary must not be exaggerated" wording of the four annotations
they may still wrongly judge in the opposite direction that it is "already implemented".

**Status: closed (2026-10-11).** Basis: the four rows of §5 now carry inline annotations (see the "current-state correction" paragraph above),
and the downstream document sync has been landed (see the current-state correction of the §2 P3 entry). The problem registered by this entry (the registration surface not matching the decision record surface) has been resolved;
**the substantive undecided parts of the four rows are out of this entry's closure scope**, and their tracking carrier is the annotations at `docs/plan.md:396` / `:399` / `:400` / `:410` themselves.

> **Correction note (2026-10-11, a factual correction, not a silent replacement):** the `docs/plan.md` line numbers cited by this entry drifted wholesale because that file was **appended to**
> (the §5 open-items table area uniformly +4 lines), and after opening the original text one by one they were changed to the current real line numbers:
> **O1 `:393` → `:397`, O4 `:396` → `:400`, O5 `:397` → `:401`, D5 `:407` → `:411`**;
> the "comparison" rows above **D1 `:403` → `:407`, D3 `:405` → `:409`, D8 `:410` → `:414`, D9 `:411` → `:415`**.
> Also corrected in the same batch are the stale references to `docs/plan.md` elsewhere in this document: the M5 closure conditions of §1 G9 and §7.3
> `:180` → `:184`, the "blocked items" `:63` → `:66` of §2 P3 and the §5 summary table, the new alert group of §2 P4 and §7.5
> `:64` → `:68`, the supplementary stance of §3 X1 `:51` → `:54`.
> References re-checked and **confirmed to need no change**: `docs/plan.md:15`, `:39`, `:40`, `:41`, and all of `AGENT.md:20-28` /
> `:30-52` / `:48` / `:51` / `:238` / `:289-291`, `docs/delivery/install-guide.md:5` / `:19` / `:91`,
> `PASS-chart-check-2026-10-05.txt:2`, `PASS-alert-check-2026-10-05.txt:1-3`.
> **This time only coordinates were changed; no adjudication conclusion, evidence file path or status semantics was altered.**

---

### P3 · Stale Downstream Documents (Inconsistent with the 2026-10-10 Adjudications)

**The question in one sentence:** two downstream documents still say "awaiting the O4 / D5 adjudication", "O5 undecided", "this document states no retention days", "the repo name is to be renamed",
which is inconsistent with the landed G6 / G7 / G8 adjudications.

**Why it was raised (evidence):**

| File | Line | Old stance still written there |
|---|---|---|
| `docs/product/security-privacy.md` | 5, 6, 8, 35, 53–56, 76–77, 112 | "the retention period is **blocked by O4 / D5**", "**this document states no retention days**", "the storage column says awaiting the **D5** adjudication", "the git repo name is **to be renamed to** `inhouse-ims-as`" |
| `docs/operations/backup-restore.md` | 7, 11, 25, 78, 146, 158–160 | "the disaster recovery level **O5** is undecided", "**O5 / D3** undecided", "retention period (O4) and storage selection (D5)", "no retention days may appear in this document" |
| `docs/plan.md` | 65 | "**blocked items**: **O4** (call-trace retention period) and **D5** (trace storage selection) block the PDPO retention period and storage scheme" |

**Adjudication boundary note (registered, not extrapolated):** the G6 / G7 adjudications explicitly state "**not implemented this time**" for the trace storage/query/delete capability and
"no rack/AZ-level fault tolerance is promised", so **not updating** the downstream documents at that time **was not out of bounds**; objectively, however, it created a stale surface.

**What would be frozen without an adjudication:** external material (the PDPO explanation, the backup/restore manual) would be inconsistent with the adjudicated conclusions; syncing requires **authorization**,
and this document performs no sync action.

> **Current-state correction (2026-10-11, appended; the evidence table above and the "adjudication boundary note" are retained as the original registration-date state, nothing deleted or changed):**
> the **stale surface registered by this entry was resolved on 2026-10-11** — both downstream documents have been synced in the additive form of "the original text above is retained unchanged",
> and `docs/plan.md` has also had an unlock note appended. Review results of 2026-10-11:
>
> | Sync target | Current actual state |
> |---|---|
> | `docs/product/security-privacy.md` | sync notes attached, of the form "**added 2026-10-10 (G6 / G7, synced; the original text above is retained unchanged)**" (e.g. `:8`, `:38`, `:119`, `:273`), marking each of the O4 / D5 / O5 "undecided / awaiting adjudication" annotations as **value adjudicated**, and stating that the basis for "**this document states no days**" has changed from "no adjudication to write" to "**no implementation to write**" |
> | `docs/operations/backup-restore.md` | sync notes attached (e.g. `:8`, `:13`, `:27`, `:166`), changing "O5 / D3 / O4 / D5 undecided" to "**value adjudicated, implementation not landed**"; "this document states no retention days" and "RPO / RTO numbers are not given unilaterally" **remain in effect** |
> | `docs/plan.md` | `:66` has appended "**the unlock status of the row above (added 2026-10-11, the original text of the row above is not changed)**", explicitly stating that the blocking of O4 / D5 **has been unlocked**, and listing the remaining dependencies as three items (landing not started / downstream stale pending sync / **O1 still fully open**). The original text at `:65` is **unchanged** (retained per the "do not change the original text of the row above" convention of that paragraph) |
> | `docs/plan.md:399` / `:400` / `:410` | the annotations of all three rows contain the sentence "**this row still has the nature of 'blocking downstream documents'** …… belongs to task E"; **that task E sync is now complete**, so the referent of this half-sentence **no longer exists**, but the three rows **still may not** be marked "resolved" on that account |
>
> **No original text of `docs/plan.md` is changed back this time** (constraint: only this one register file may be changed). Whether to change back the "referent has become void" wording
> is a later action on `docs/plan.md`, is not within this document's authorization scope, and is only registered here.

> **Follow-up action already executed (appended in the closing round of 2026-10-11; the paragraph above is retained, nothing deleted or changed):** the "later action on `docs/plan.md`" described in the paragraph above
> **was completed additively later the same day** — a correction sentence was appended to the end of each of the four rows `:66`, `:399`, `:400`, `:410` of `docs/plan.md`,
> stating that the **downstream sync referred to by "belongs to task E" is complete** (that is, the thing by which this entry was closed), while restating row by row that the row **still must not be marked "resolved"**.
> **Everything is still append-only with zero deletions or changes**: the original text of the "old stance still written there" in the table above and its inline annotations are all retained as-is, and not a single character was changed back.

> **Boundaries that remain in effect (not relaxed by the sync):** trace storage / query / delete are **not implemented this time**;
> **no rack / AZ-level fault tolerance is promised**; **the RPO / RTO numbers are unadjudicated**; the O1 **value** is still open. These are the boundaries declared item by item by the sync notes themselves,
> and they must not be derived in reverse as "resolved" on account of "the downstream has been synced".

**Status: closed (2026-10-11).** Basis: the sync notes of both downstream documents have been landed line by line, and `docs/plan.md:66` has had an unlock note appended
(see the "current-state correction" paragraph above). The stale surface registered by this entry has been resolved; **the remaining dependencies (implementation not landed / RPO·RTO unadjudicated / O1 value open)
are out of this entry's closure scope**, and their tracking carrier is the annotations at `docs/plan.md:396` / `:399` / `:400` / `:410` and `:66` themselves.
(The line-number corrections in the "coordinate correction note" below are registration-date coordinate corrections, which are a different matter from this status closure; both audit chains are retained.)

---

### P4 · The promtool Validation Has a "Stale Evidence" Gap

**The question in one sentence:** the two newly added alert groups `as.runtime` / `as.platform` have **so far never been validated by promtool**.

**Why it was raised (evidence):**

| Fact | Location |
|---|---|
| the only product of a `promtool check rules` run is `SUCCESS: 5 rules found`, covering the **then-existing original 5 rules** | `docs/acceptance/artifacts/m5/2026-10-05/alert-check-full.txt:1-3` |
| on 2026-10-10 **two alert groups** `as.runtime` / `as.platform` were added under `deploy/alerts/` (the original 5 rules unchanged) | `docs/plan.md:67` |

> **Key inference (registration, not adjudication):** the old artifact **cannot** be used to cross out the "not executed" of the row
> "`make alert-check` (`promtool check rules`) …… alert rule syntax unvalidated" in the §1.2 table.
> That row still holds for the **two newly added groups**.

**What would be frozen without an adjudication:** whether the alert rule set can claim "syntax validated"; and, when §0-A.1 item 1 (containerized promtool validation)
is re-executed, whether the validation scope must explicitly cover the new groups.

**Status: closed (2026-10-11).**

> **Current-state correction (appended in the closing round of 2026-10-11; the original text above is retained, nothing deleted or changed):** the gap registered by P4 (the newly added
> `as.runtime` / `as.platform` groups never validated by promtool) **was closed on 2026-10-11**.
> Status declaration triple: **(verified, docs/acceptance/artifacts/m5/2026-10-11/PASS-alert-check-full-2026-10-11.txt, 2026-10-11)**.
> Validation method: on the registered environment `dev-win03ib7niepf0` (host `WIN-03IB7NIEPF0`), the promtool of
> `prom/prometheus:v2.45.0` was run **in a docker container**
> (`docker run --rm --entrypoint=/bin/promtool -v /home/shudong/project/3rdparty-as/deploy/alerts:/alerts prom/prometheus:v2.45.0 check rules /alerts/as-alerts.yaml`),
> outputting `Checking /alerts/as-alerts.yaml` / `SUCCESS: 10 rules found`.
> The 10 rules = 5 in `as.call-path` (the original 5 already validated on 2026-10-05) + 3 in `as.runtime` + 2 in `as.platform`
> (the latter two groups added on 2026-10-10), i.e. covering all **3 groups / 10 rules**, in the rule file `deploy/alerts/as-alerts.yaml`.
> The main agent **independently re-ran it on the same day on the same host with the same command**: likewise `SUCCESS: 10 rules found`, exit=0.
> The evidence is collected in the index table of [`../acceptance/artifacts/m5/README.md`](../acceptance/artifacts/m5/README.md)
> (the 2026-10-11/PASS-alert-check-full row, noting coverage of 3 groups / 10 rules, image v2.45.0, host).
> **Boundary:** this closure covers only the **syntax validation** of the alert rules; X1 (the alert capture-wiring annotation vs ServiceMonitor/PodMonitor)
> still awaits the carrier's monitoring-integration standard input, and **syntax validation passing does not mean the wiring is closed** (the "relationship to P4" paragraph of §3 X1 remains in effect).

---

### P5 · The Separate Issue of A4-3 Has Not Been Created

**The question in one sentence:** the §0-A.6 adjudication deferred the 14 Wave 2 replay cases to a "separate issue", but that issue still does not exist.

**Why it was raised (evidence):**

| Fact | Location |
|---|---|
| adjudication original text: "the 14 Wave 2 replay cases are deferred to a separate issue"; and it records that "this task **does not create an issue**" | the **G2 / A4-3** row of §0-A.6 (`:57`) in [`2026-10-10-unfinished-assessment-and-next-plan.md`](2026-10-10-unfinished-assessment-and-next-plan.md); `docs/plan.md:39` |
| to date that issue **does not exist** (this register did no remote check and found no in-repo record pointing at it) | — |

**What would be frozen without an adjudication:** the Wave 2 replay cases have only one "destination" (the separate issue) but no carrier; if nobody creates it,
that batch of cases loses a traceable landing point in the next session.

**Status: closed (2026-10-11).**

> **Current-state correction (appended in the closing round of 2026-10-11; the original text above is retained, nothing deleted or changed):** the maintainer **adjudicated on 2026-10-11**:
> the "separate issue" referred to by A4-3 **uses an in-repo doc as its carrier** (this project has no external issue tracker; in-repo documents are the tracking system).
> The carrier file = [`../acceptance/2026-10-11-wave2-replay-register.md`](../acceptance/2026-10-11-wave2-replay-register.md)
> (newly created on 2026-10-11): the 14 baseline artifacts (the 14 message files `01-in-invite-trunk.txt` … `14-in-200-trunk.txt` under
> `testbed/contracts/sip-baseline/S1-basic-call/`, listed verbatim in §2 of that doc), the
> replay work definition (`:66-74` of the Wave 2 section of [`../acceptance/2026-10-09-e2e-test-plan.md`](../acceptance/2026-10-09-e2e-test-plan.md)),
> the related requirements (REQ-F-1 / F-2 / F-4) and the start prerequisites are all traceable.
> **This closure covers only the disappearance of the "missing carrier" gap**; the **implementation of the 14 cases itself still belongs to the A4 e2e batch**
> (currently `pytest.mark.e2e` has 0 hits in test code and Wave 1 has not landed either, to be started after Wave 1 is complete),
> and this closure **does not sign off REQ-F-1** (all 14 of its items remain open).

---

### P6 · The Term "FM" Has No Source

**The question in one sentence:** the G3 row of §0-A.6 contains "FM stands for Fault Management", but that concept has no traceable source in earlier records.

**Why it was raised (evidence):**

| Location | Does FM appear |
|---|---|
| the **G3 / A5** row of §0-A.6 (`:58`) | **appears**: "FM stands for Fault Management, managed per the new feature process, with demo/feature documents added at implementation time" |
| the **G3** row of §0-A.2 (`:23`) | **does not appear** |
| the whole of §8.2 | **does not appear** |
| `docs/plan.md:41` | **retained** that sentence when copying §0-A.6 |

> **Nature (registration, not adjudication):** it is a term **newly introduced** at adjudication time with **no traceable source**, not a continuation of an existing stance.

**What would be frozen without an adjudication:** whether the G3 / A5 scope includes FM as a feature; the process carrier of "managed per the new feature process" is unclear.

**Status: clarified (2026-10-11) — closed.**

> **Current-state correction (appended in the closing round of 2026-10-11; the original text above is retained, nothing deleted or changed):** the maintainer **clarified on 2026-10-11**, with nothing added or removed:
> the "**FM stands for Fault Management, managed per the new feature process, with demo/feature documents added at implementation time**" of the **G3 / A5** row in §0-A.6
> (`:58` of [`2026-10-10-unfinished-assessment-and-next-plan.md`](2026-10-10-unfinished-assessment-and-next-plan.md),
> `:41` of [`../plan.md`](../plan.md)) was **deliberately introduced** at adjudication time — **it is not a typo and not unfounded improvisation**.
> Boundary: FM is a **new feature of a future project / future batch**; the work on FM as a new feature **is not completed in the current project, it is a matter for later, and needs no attention now** ——
> the current project **does not track it, does not implement it, does not define requirements, and adds no demo or feature document**.
> The G3 / A5 adjudication sentence (`:58` and `plan.md:41`) is **retained and not deleted**; when FM is started in the future it will be managed per this repository's **existing new feature process**
> (requirement → ADR → design → review, see §3.4 of `AGENT.md`).
> Status: **clarified (2026-10-11), closed.**

---

## 3. Third Group: Still Awaiting External Input

### X1 · Selection of the G3 / A5 Alert Capture Wiring

**The question in one sentence:** the annotation vs ServiceMonitor/PodMonitor question takes no side for now, awaiting the carrier's monitoring-integration standard input.

**Why it was raised (evidence):**

| Fact | Location |
|---|---|
| adjudication original text: "remains pending: annotation vs ServiceMonitor/PodMonitor **takes no side for now**; awaiting the carrier's monitoring-integration standard input; **do not change the chart for now**" | the G3 row of §0-A.6 (`:59`) in [`2026-10-10-unfinished-assessment-and-next-plan.md`](2026-10-10-unfinished-assessment-and-next-plan.md); `docs/plan.md:41` |
| supplementary stance: the **"stance-priority addendum"** `:69` of the same file reads **verbatim**: "**G3 (A5 monitoring wiring) still awaits the carrier's monitoring-integration standard input; do not change the chart for now.**" | `:70` of [`2026-10-10-unfinished-assessment-and-next-plan.md`](2026-10-10-unfinished-assessment-and-next-plan.md) |
| the same stance **copied** into `docs/plan.md`: `docs/plan.md:53` reads **verbatim** "**G3 (A5) still awaits the carrier's monitoring-integration standard; do not change the chart for now**" — parenthetical: that copy has **two fewer qualifiers** than `:70` (no "monitoring wiring" inside the parentheses; no "input" after "standard"). **The original wording in the table above ("A5 monitoring wiring" + "standard input") is verbatim identical to `:70`**, and the more complete wording is governed by `:70`; the original text of `docs/plan.md` is **not changed back** (this document only registers) | `docs/plan.md:53` |

**Relationship to P4 (registration):** P4 is "rule **syntax** unvalidated", X1 is "**capture wiring** not closed"; they differ,
and `promtool` passing does not mean the wiring is closed.

**What would be frozen without an adjudication:** the chart's capture wiring (the "do not change the chart" stance remains in effect).

**Status:** awaiting maintainer adjudication — **it currently remains pending**, awaiting external input.

> **Adjudication landed (appended 2026-10-12; the original text above is retained unchanged)**: the maintainer decided on 2026-10-12 — **X1 is left to the next release**. Rationale: the capture-wiring selection needs the **carrier's monitoring-integration standard input** before it can continue; until the input is in place, no side is taken and the chart is not changed (the capture wiring of `deploy/helm/` stays as-is; the 2026-10-12 change to `Chart.yaml` was limited to the version / appVersion / kubeVersion of A6 and is unrelated to this item). This stance is consistent with §12 "adjudicated-but-not-done register area" of [`2026-10-10-unfinished-assessment-and-next-plan.md`](2026-10-10-unfinished-assessment-and-next-plan.md): **any subsequent status inventory, report, handoff or session opening that touches X1 writes only "see this row"; it does not expand item by item, does not remind separately, and is no longer listed as a "maintainer action"**. This row **constitutes no execution authorization** and does not close the capture wiring itself; if the carrier's standard input arrives, the rescheduling will be re-planned at that time and a restart record appended to this row.

> **Destination pointer (appended 2026-10-13; the original X1 adjudication text above is all retained unchanged)**: the landing point of the "next release" described in this paragraph is
> [`../next-release-v1.1-plan.md`](../next-release-v1.1-plan.md) — **the X1 capture wiring** is registered in **row 7 of §2** of that document
> (of the external hard-dependency class; restart = a separate maintainer adjudication + the carrier's monitoring-integration standard being in place, and the blocker plus "why this version's evidence cannot substitute"
> follow the original text of this paragraph). The existing stance of this paragraph that "any subsequent status inventory, report, handoff or session opening that touches X1 writes only 'see this row', does not expand item by item,
> does not remind separately, and is no longer listed as a maintainer action" **is unchanged**; accordingly it becomes "see row 7 of §2 of that document".

---

## 4. Fourth Group: Overall Work That Has Been Scoped but Not Started

### S1 · End-to-End Cleanup of the requirement / ADR / design / coding / testing Layers

**The question in one sentence:** raised by the maintainer on 2026-10-11; an end-to-end cleanup of the five-layer document system is needed to solve the current stance confusion at the root.

**Scope (registered, five layers in total):** requirement system → ADR system → design document deduplication → coding boundaries → testing layering.

**Facts already found by this survey (registered as input, solutions not expanded):**

| Layer | Fact found | Location |
|---|---|---|
| requirements | `docs/requirements/` has only 3 files (`prd.md`, `README.md`, `req-nf-15-testbed-performance.md`) | `docs/requirements/` |
| requirements | all 40 REQs are in `prd.md`: REQ-F-1…16, REQ-NF-1…16, REQ-S-1…4, REQ-G-1…4, **with no numbering gaps** | `docs/requirements/prd.md:162` (from REQ-F-1) – `:536` (REQ-G-4) |
| requirements | **REQ-NF order is disordered**: NF-9 comes before NF-6 | `docs/requirements/prd.md:373` (REQ-NF-9) vs `:387` (REQ-NF-6) |
| requirements | **the status matrix is not under `requirements/`** but in the acceptance directory | `docs/acceptance/m8-test-plan-matrix.md:42-44` (header `req_id / test_plan_ref / milestone / phase / evidence / status / signed_by`); §0.5 of `docs/acceptance/report.md` |
| requirements | **dangling reference**: step 4 of the opening ritual in §10.4 of `AGENT.md` requires reading `docs/acceptance/criteria.md`, but **that file does not exist** | `AGENT.md:238`; compare `docs/architecture/hld.md:160`, `docs/architecture/lld.md:158`, `docs/reviews/hld-lld-design-review-2026-09-30.md:12,20`, all of which record its absence |
| ADR | 28 files in total (0000 is the template), numbering 0000–0027 is **contiguous** | `docs/architecture/adr/` |
| ADR | status distribution: accepted 24 / superseded-in-part 1 (0011) / proposed 1 (0023) / draft 1 (0025) | `docs/architecture/adr/README.md:14-43` and the body of each ADR |
| ADR | **the registry has drifted from the bodies**: `README.md:39` and `:41` record 0023 / 0025 as `draft`, but the body of 0023 says `Status: proposed` | `docs/architecture/adr/README.md:39,41` vs `docs/architecture/adr/0023-redis-call-state-checkpoint.md` |
| design | three overlap groups: ① `reSIProcate.md` ≒ `resiprocate-dum-b2bua.md` ≒ same source as ADR-0019/0022; ② `system-architecture.md` (about 34.9KB) ≒ `hld.md` (about 34.4KB), comparable in size and both full-architecture narratives; ③ `call-state-recovery-options.md` ≒ same topic as ADR-0023 | `docs/architecture/` |
| design | the above three groups have **no priority guidance** (which one is authoritative is not stated) | — |
| testing | marker definitions: `unit` / `contract` / `integration` / `e2e` / `performance` | `pyproject.toml:48-54` |
| testing | test file distribution: 53 under `platform/tests/**`; 15 under `testbed/{probe,load,simulators}/tests`; 2 in the root `tests/` | — |
| testing | **`pytest.mark.e2e` has 0 file hits repo-wide** (mentioned only in documents) ⇒ `-m e2e` necessarily collects 0 cases | repo-wide search finds no test file hits |
| testing | `make test` still runs the three layers unit/contract → integration → **e2e** in order | `Makefile:41-44` |

**Status: the cleanup of all five layers is fully complete (2026-10-11, two batches); from now on only the ADR system evolves naturally with new ADRs, and no further cleanup batches are planned.**

> **Current-state correction (appended in the closing round of 2026-10-11; the survey table above and the registration-date "awaiting maintainer adjudication" status sentence are retained as the audit chain, nothing deleted or changed):**
> the **first batch of the S1 five-layer cleanup is complete (2026-10-11)** — the execution plan
> [`2026-10-11-s1-document-structure-cleanup.md`](2026-10-11-s1-document-structure-cleanup.md) and the
> execution record [`2026-10-11-s1-execution-record.md`](2026-10-11-s1-execution-record.md).
> The 6 tasks of the first batch: ① fixing the broken link in the AGENT.md opening ritual (`criteria.md` → `m8-test-plan-matrix.md`);
> ② the within-group REQ-NF order check passed (no file changed); ③ adding the REQ-NF-16 row to the acceptance matrix (status=open);
> ④ moving the empty e2e layer out of the Makefile `test` target; ⑤ creating `tests/test_requirements_registry.py` (6 test functions);
> ⑥ the meta-rule of §8 of this register.
> **The design document overlap has been resolved by §1 "document map and priority" of [`../architecture/README.md`](../architecture/README.md)**:
> the normative documents = `hld.md` / `lld.md`; reference / background material (including `system-architecture.md` and the reSIProcate same-source material)
> always defers to HLD / LLD on conflict; the same-source overlaps are annotated in that section.
> **The ADR drift has been fixed**: the 0023 row of the registry in [`../architecture/adr/README.md`](../architecture/adr/README.md) has been changed to
> `proposed`, with a 2026-10-11 note below the table stating "the body is authoritative, 0025 draft is left unchanged".
> Self-check: `uv run pytest tests/ -q` → **76 passed** (re-run in the closing round of 2026-10-11).
> **S1 is neither marked "fully complete" nor still "not started"**: whether to start follow-up batches for further ADR-system cleanup and coding-boundary cleanup
> **requires separate maintainer authorization** — a follow-up batch is a new authorization item, not a dangling adjudication, so S1 **is not counted as "pending adjudication"**.

> **Second batch (closing batch) of 2026-10-11 appended; the survey table above, the first batch's "current-state correction" and the various historical status sentences are retained as the audit chain, nothing deleted or changed:**
> **the cleanup of all five S1 layers (requirements / ADR / design / coding / testing gate stance) is fully complete.**
> ① **the ADR system is fully re-reviewed and consistent**: opening the bodies of 0001–0027 one by one, the 25 English `Status` lines plus the 2 Chinese status lines of 0011 / 0019
> all match the registry values; 0011 ↔ 0019 superseded-in-part is bidirectionally traceable; there are no out-of-range references to ADR-0028+;
> of the 206 ADR links under `docs/**`, 205 are valid, and there is **1 pre-existing broken link**
> (the reference at `docs/acceptance/m5-engineering-closure-2026-10-04.md:43` to ADR-0026 lacks the `../` prefix),
> which has been registered in the "second full review" note of [`../architecture/adr/README.md`](../architecture/adr/README.md),
> and per the history-preservation convention this batch does not fix the original text of the historical document, leaving the decision to the maintainer's review — basis: the second review note of the ADR README.
> ② **the coding layer boundaries are machine-enforced**: the new [`../../tests/test_layer_boundaries.py`](../../tests/test_layer_boundaries.py),
> using a read-only ast scan (data sources are the root workspace declaration and each member's pyproject, no hardcoded member list), guards four horizontal boundaries + member classification:
> app mutual exclusion, product packages (apps / services) not depending on testbed, internal imports must be explicitly declared in the dependent's pyproject,
> and the declared internal dependency graph being acyclic (the intra-services dependency clarification was appended to §4 of `AGENT.md` in sync: the only existing case is config-service → console,
> explicitly declared and not forming a cycle), plus a structural supporting test requiring every member to fall into exactly one of the kernel / apps / services / testbed classes;
> the measured current state is **all 5 tests compliant and passing**.
> ③ **§4 of AGENT.md has appended the intra-services dependency clarification** (note added 2026-10-11, not relaxing the app mutual exclusion or the testbed ban).
> **The implementation of e2e cases in the testing layer belongs to the A4 batch, it is not an S1 gap**; S1 signs off no REQ / milestone, and all notes of this batch await maintainer review.
> Execution record: §11 of [`2026-10-11-s1-execution-record.md`](2026-10-11-s1-execution-record.md).

---

## 5. Summary Table (for quick cross-checking; the "status" column in the table is the current status field and is synced as adjudications are made in §7)

| ID | The question in one sentence | What would be frozen without an adjudication (summary) | Status |
|---|---|---|---|
| **G9-a** | do infra assets count as deliverables or as development scaffolding | the delivery package list and the external stance | closed (2026-10-11) — see §7.1 (the deliverable-product / scaffolding dichotomy) |
| **G9-b** | whether a "complete infra host" needs to be named | cluster-level work has no definite environment; "this machine has no tools" is misread | **resolved (2026-10-11)** — solved by `docs/environments.md` + `tools/env-probe.sh` in the tool-probing form, no naming or manual registration needed any more (basis in the status column of §1 G9-b; the status column is the current status field and is synced as things are actually resolved) |
| **G9-c** | whether cluster-level verification must run on every machine / every PR | the §1.2 tool table; the premise of A4-4 | **downgraded (2026-10-11)** — overlaps the already effective §0-A.6 G2 / A4-4, not listed separately as pending adjudication (basis in the status column of §1 G9-c) |
| **G10** | whether to do a sub-repo / repo split | the rewrite cost of the path coupling and Makefile targets (the later, the higher) | closed (2026-10-11) — see §7.2 (closed as "do not split the repo") |
| **G11** | whether to keep the "application without infra" form | the delivery package form, the `docs/delivery/` boundary, the customer stance | closed (2026-10-11) — see §7.2 (closed as "do not declare a second delivery form") |
| **P1** | two opposite stances on A4-4 (included / not included in PR required) | the gate form once combined with A4-2 | clarified (2026-10-11) — no re-adjudication needed; governed by §0-A.6 G2/A4-4 (basis in the "registration correction" paragraph of §2 P1) |
| **P2** | `plan.md` §5 did not sync the O4 / O5 / D5 adjudications | the §15 open-items registration surface is inconsistent with the §0 decision surface | closed (2026-10-11) — the four rows now carry inline annotations; see the "current-state correction" of §2 P2 |
| **P3** | stale downstream documents (security-privacy / backup-restore / plan.md:65) | external material is inconsistent with the adjudicated conclusions | closed (2026-10-11) — both downstream documents have had sync notes appended and plan.md:66 has had an unlock note appended; see the "current-state correction" of §2 P3 |
| **P4** | the newly added `as.runtime` / `as.platform` were never validated by promtool | whether the alert rule set can claim its syntax is validated | **closed (2026-10-11)** — containerized promtool v2.45.0 in docker validated `SUCCESS: 10 rules found` (3 groups / 10 rules); triple `(verified, docs/acceptance/artifacts/m5/2026-10-11/PASS-alert-check-full-2026-10-11.txt, 2026-10-11)`; see the "current-state correction" of §2 P4 (the X1 capture wiring still awaits external input; syntax passing ≠ wiring closed) |
| **P5** | the separate issue of A4-3 was not created | the Wave 2 replay cases lose a traceable landing point | **closed (2026-10-11)** — the "separate issue" is replaced by an in-repo carrier: [`../acceptance/2026-10-11-wave2-replay-register.md`](../acceptance/2026-10-11-wave2-replay-register.md); the implementation of the cases themselves waits for the A4 batch; see the "current-state correction" of §2 P5 |
| **P6** | the term "FM" has no source | whether the G3 / A5 scope includes FM; the process carrier is unclear | **clarified (2026-10-11), closed** — FM was confirmed by the maintainer as deliberately introduced at adjudication time and is positioned as a new feature of a future project / future batch; the current project does not track it, does not implement it and adds no documents; the G3/A5 adjudication sentence is retained; see the "current-state correction" of §2 P6 |
| **X1** | the alert capture wiring (annotation vs ServiceMonitor/PodMonitor) | the chart's capture wiring (do not change the chart for now) | **deferred to the next release (maintainer decision on 2026-10-12)** — requires the carrier's monitoring-integration standard input; until the input is in place, no side is taken and the chart is not changed; subsequent inventories only cite the pointer and no longer list it separately (see the appended record of §3 X1) |
| **S1** | end-to-end cleanup of the requirement / ADR / design / coding / testing layers | the stances of the five layers stay confused | **the cleanup of all five layers is fully complete (2026-10-11, two batches)**; from now on only the ADR system evolves naturally with new ADRs and no further cleanup batches are planned; second batch: a full re-review of ADR 0001–0027 is consistent (1 pre-existing broken link registered for maintainer handling), the coding boundaries are machine-enforced by the new `tests/test_layer_boundaries.py` (5 tests all green), and §4 of `AGENT.md` has the intra-services dependency clarification appended; the implementation of e2e cases belongs to the A4 batch and is not an S1 gap; see the two "current-state corrections" of §4 S1 |

---

## 6. Status Section (Must Read)

- **All items listed in this document are "awaiting maintainer adjudication".** This document contains no adjudicated conclusion and gives no recommended leaning.
- **This document constitutes no execution authorization**: it authorizes no file modification, no build/test/container action, and no git write operation.
- **This document constitutes no external acceptance pass**: it produces no acceptance evidence and lifts no hold (the external IOT and real-environment evidence collection hold
  remains in effect).
- **This document constitutes no REQ sign-off or milestone sign-off**: it signs off no REQ, signs off no milestone, and changes neither the §5 open-items table
  nor the §0 decision record table of `plan.md`.
- **Maintenance convention**: once any item has been adjudicated, **append** a record per the §0-A.5 practice (stating the adjudication result and date) and sync it to
  the §0 decision record table of `docs/plan.md`; **entries of this document must never be silently deleted**.
- **Scope of this round's action**: this round only created this one file; it modified, deleted or moved no other file; it ran no `make` / `pytest` /
  `docker` and no git write operation.
- **Landed**: 2026-10-11. **Status: landed, awaiting maintainer review.**

### 6.1 Correction (2026-10-11, appended; the original text of §6 above is all retained, nothing deleted or changed)

> **Where item 1 of §6 above conflicts with this correction, this correction prevails.** The text above says "**all items listed in this document are 'awaiting maintainer adjudication'**"
> and "**this document contains no adjudicated conclusion**" — these two sentences **held when it was landed on the registration date**, and no longer hold after §7 was landed. Per §0.1,
> the original text above is retained as the audit chain and **this paragraph only appends, it does not change anything back**.

**One: the items listed in this document are not all pending adjudication.** As of 2026-10-11, **5 items are closed**:

| ID | Closure date | Closure basis (section) |
|---|---|---|
| **G9-a** | 2026-10-11 | §7.1 (the delivery boundary decision line: the deliverable-product / scaffolding dichotomy, with the criterion "does the asset reach the customer") |
| **G10** | 2026-10-11 | §7.2 (closed as "do not split the repo", keeping the single-repo form) |
| **G11** | 2026-10-11 | §7.2 (closed as "do not declare a second delivery form") |
| **P2** | 2026-10-11 | the "current-state correction" paragraph of the §2 P2 entry (the four rows O1 / O4 / O5 / D5 of §5 of `docs/plan.md` now carry inline annotations) |
| **P3** | 2026-10-11 | the "current-state correction" paragraph of the §2 P3 entry (sync notes appended to `security-privacy.md` / `backup-restore.md`, unlock note appended to `plan.md:66`) |

**Two: 8 items still pending adjudication / handling**: **G9-b, G9-c, P1, P4, P5, P6, X1, S1**. **〔correction in the closing round of 2026-10-11; the sentence above is the original registration-date text and is retained unchanged〕the current stance is "7 items still pending adjudication / handling": G9-b, G9-c, P4, P5, P6, X1, S1** — **P1 had its registration withdrawn in this round and is not counted as pending adjudication** (basis in the "registration correction" paragraph of §2 P1: the G2 / A4-4 of §0-A.6 is an already effective adjudication, and §8.1 ④ is a recommendation overridden by it). **〔further correction appended in this round on 2026-10-11; the original text of both the "8 items" and the "7 items" above is retained unchanged〕the current stance is "5 items still pending adjudication / handling": P4, P5, P6, X1, S1** — **G9-b has been resolved** (solved by the `docs/environments.md` environment registry + on-the-spot probing by `tools/env-probe.sh` in the tool-probing form: the environment name is generated as `<role>-<hostname>`, the hostname is measured by `uname -n`, and tools are judged in three states ("✅ present / ❌ missing / ⚠ installed but unusable"), so naming and manual registration are no longer needed; basis in the status column of §1 G9-b) and **G9-c has been downgraded** (it overlaps the already effective §0-A.6 G2 / A4-4 — the option A risk column of §8.1 ④ in `2026-10-10-unfinished-assessment-and-next-plan.md` already lists "this machine has no kind" as an inherent risk of that option, so it does not constitute an independent pending adjudication; basis in the status column of §1 G9-c). **Two boundaries, from which no new conclusion may be drawn: ① the "5 items closed" in item one above does not include G9-b / G9-c** — they are respectively **resolution** and **downgrade**, not "adjudication closure" in the sense of §7, so that count **remains 5** and is **not changed**; **② the substantive undecided content of the five items P4 / P5 / P6 / X1 / S1 was not touched by a single character in this round and their status is still pending**, and this paragraph only corrects the counts and the list stance; it does not adjudicate any of them on the maintainer's behalf. ** **〔further correction in the closing round of 2026-10-11; the original text of the three places "8 items", "7 items" and "5 items" above is all retained and not changed back〕the current stance is "1 item pending adjudication: X1".** The destinations of the original 5 items (P4, P5, P6, X1, S1): **P4 is closed** (2026-10-11, containerized promtool v2.45.0 in docker validated `SUCCESS: 10 rules found`; the triple and basis are in the "current-state correction" of §2 P4); **P5 is closed** (2026-10-11, the "separate issue" replaced by the in-repo carrier [`../acceptance/2026-10-11-wave2-replay-register.md`](../acceptance/2026-10-11-wave2-replay-register.md); basis in the "current-state correction" of §2 P5); **P6 is clarified** (2026-10-11, FM confirmed by the maintainer as deliberately introduced at adjudication time and positioned as a new feature of a future project / future batch; basis in the "current-state correction" of §2 P6); **the first batch of S1 is complete and the remainder is resolved or pending authorization** (the 6 tasks of the first batch covered the requirements / testing layers, the design overlap has been resolved by §1 of `docs/architecture/README.md`, and the ADR 0023 drift has been fixed; basis in the "current-state correction" of §4 S1) — **S1 is not counted as "pending adjudication": a follow-up batch is a new authorization item, not a dangling adjudication**. Accordingly, the list of pending adjudication / handling now consists only of **X1**. This is consistent with the §8.1 meta-rule: "**this document's list has no minimum length. Once an issue is resolved it is removed from the list, and the list getting shorter is a normal outcome**" — P4 / P5 are removals after the issue was resolved, P6 is a removal after clarification, and S1 is a stance update after the first batch completed; none is padding for appearance, and none adjudicates X1 on the maintainer's behalf.**

**Three: cross-check of the consistency between the "register items not closed this round" list of §7 and the status column of the §5 summary table (row-by-row cross-check of the original text this round):**

| ID | Status column of the §5 summary table | What §7 actually records | Cross-check conclusion |
|---|---|---|---|
| **G9-a** | awaiting maintainer adjudication (`:372`) | §7.1 "**closes G9-a**" | **inconsistent** — the §5 status column is the original registration-date status and was missed when closing; **〔closing round of 2026-10-11〕eliminated** — the status column at §5 `:372` has been synced to "closed (2026-10-11) — see §7.1" |
| **G10** | awaiting maintainer adjudication (`:375`) | §7.2 "closed as 'do not split'" | **inconsistent** — same as above; **〔closing round of 2026-10-11〕eliminated** — the status column at §5 `:375` has been synced to "closed (2026-10-11) — see §7.2" |
| **G11** | awaiting maintainer adjudication (`:376`) | §7.2 "closed as 'do not declare a second form'" | **inconsistent** — same as above; **〔closing round of 2026-10-11〕eliminated** — the status column at §5 `:376` has been synced to "closed (2026-10-11) — see §7.2" |
| **P2** | closed (2026-10-11) (`:378`) | §7 has appended at the end "P2 / P3 have been removed from this list" | consistent |
| **P3** | closed (2026-10-11) (`:379`) | same as above | consistent |
| **P4** | awaiting maintainer adjudication (`:380`) | §7.5 "**that gap is retained as a pending execution item** (running `promtool` is required, it is not run this round)", but the "register items not closed this round" list at the end of §7.5 (`:567`) **lists only 7 items and does not include P4** | **the list omitted it** — both the §5 table and the body of §7.5 record P4 as not closed, so the "actual not-closed fact" governs and **P4 counts as still pending**; the original text of that §7 list is retained and not changed back |

> **Coordinate note (appended 2026-10-11, the same approach as the coordinate correction note of §2 P2):** the line numbers in the table above are the **real line numbers after this append was completed**,
> each verified by opening the original text; that list of §7 is now at `:567` (its "P2 / P3 removed" append paragraph follows immediately after).
> All appends before this paragraph (including the "follow-up action already executed" paragraph of §2 P3 and this §6.1 paragraph) shift the later line numbers as a whole,
> so the current coordinates are given once here: **only coordinates are changed, and no status semantics is changed.**

Two supplementary explanations (to avoid again wrongly deriving "already resolved" from the "list"):

1. The **original text of that list at the end of §7.5 actually contains only 7 items** (G9-b, G9-c, P1, P5, P6, X1, S1) and **does not list P4**;
   this correction adds P4 according to the actual records of the §5 table and the body of §7.5, which is a **registration stance** correction and not a substitute for the maintainer adjudicating P4. **〔closing round of 2026-10-11〕the P1 listed in the original text of that list has had its registration withdrawn and is no longer counted as pending adjudication; the original text of the §7.5 list (including P1) is retained and not changed back.**
2. The status columns of the three rows G9-a / G10 / G11 of the §5 summary table conflict with §7 (those three rows were missed when closing), and this paragraph only registers and explains the correction;
   it **does not change back the original §5 table**; readers judging the current status defer to this paragraph and §7. **〔closing round of 2026-10-11〕** that "no change back" was the practice on the registration date; the **status fields** of G9-a / G10 / G11 in §1 / §5 have now been written back as "closed (2026-10-11)" pointing to §7.1 / §7.2 per the convention that "the status column is the current status field and is synced as §7 adjudications are made" — **updating a status field is not "silently rewriting existing original text"** (the history-preservation convention protects descriptive body text and evidence); the cross-check records, body text and coordinates above are all retained unchanged, and **not a single character of any unclosed item's status was touched**.

> **Destination pointer (appended 2026-10-13; the original text of the "two supplementary explanations" above is retained unchanged)**: the remaining registration-stance inconsistencies in this document —
> the **§7.5 list omitting P4** pointed to by item 1 and the **status omissions for G9-a / G10 / G11 in the §5 summary table** pointed to by item 2 — are registered in
> rows 3 / 4 of **§8** (the zero-leftover cross-check table) of [`../next-release-v1.1-plan.md`](../next-release-v1.1-plan.md) and in
> **§5-7** (handling stance: do not change back the original §0.5 / §5 table; readers defer to the appended paragraph). **The original text of this document is not changed back**,
> the paragraphs above continue to serve as the audit chain of that time; subsequent status inventories, reports and handoffs only cite this pointer and do not reopen the adjudications of those two items on that basis.

**Four: correction of similar statements in one go:**

- The §0 text "this document gives no proposal, takes no side, recommends no leaning … the conclusion always reads '**awaiting maintainer adjudication**'" (`:12-13`) — that sentence is a **writing convention of the registration date**,
  and it **remains in effect** for the items in this document that are **still not closed**; but it must not be taken to mean that the 5 closed items "are still awaiting adjudication".
- The maintenance convention of §0.1 (`:19-20`) **itself has no conflict and remains in effect**: this paragraph and §7 append per that convention and delete no existing entry.
- The measured re-check record of the landing note at the end of the document (`:575-580`, which records "62 passed") is in the **appended** paragraph at the end of that section; the original 62 record is retained.
- The "**scope of this round's action**: this round only created this one file; it modified, deleted or moved no other file" and "**this document constitutes no execution authorization**:
  it authorizes no file modification …" of §6 **describe only that registration-date session**, and have been superseded by the authorized actions recorded in §7 (the 7 evidence files of §7.4 renamed with `git mv`,
  the new `docs/environments.md` and `tests/test_evidence_discipline.py`). That contradiction **existed before this round** (caused by the §7 session),
  and is only registered and corrected here; the remaining items of §6 (constitutes no execution authorization / constitutes no external acceptance pass / constitutes no REQ or milestone sign-off / maintenance convention)
  **remain in effect**, and this paragraph does not change their force.

---

## 7. Adjudications Landed (2026-10-11)

> **Nature of this section:** the following items were explicitly approved by the maintainer on 2026-10-11 and **have moved from "pending adjudication" to "adjudicated"**.
> This section **only appends** and rewrites no existing registration content of §1–§6 — the original entries are retained as the audit chain per §0.1.
> This section **signs off no REQ, signs off no milestone, and constitutes no external acceptance pass**.

### 7.1 The Delivery Boundary Decision Line

> **Decision line = will this asset reach the customer? Yes → deliverable product; no, only we use it → scaffolding.**
> Second criterion for the grey zone: **will the customer ever raise a support ticket about it to us? Yes → deliverable product; never → scaffolding.**

**Scaffolding produces instrument readings; a deliverable product is the inspection report.** Specifically for this project:

| Category | Assets |
|---|---|
| **deliverable product** | `deploy/helm/` (chart + values + templates), container images, the alert rules of `deploy/alerts/`, `docs/product/`, `docs/operations/`, `docs/delivery/` |
| **scaffolding** | all scripts of `deploy/kind/`, the simulation and load-test assets of `testbed/`, `docs/plan.md`, `docs/handoff/`, ADRs |

**Conclusion drawn from this:** the §2 delivery list of `docs/delivery/install-guide.md` and the existing wording at lines 19 and 91
**are precisely the existing implementation of that decision line**, so this time it is a **ratification of existing facts, not a new decision**. The essentials of the basis:

- `:19` — `deploy/kind/m5-gen-certs.sh` is only a kind self-signed precedent, **"not a deliverable"**;
- `:91` — the kind / lab installation form **"must not be used in customer production"**;
- the §2 delivery list — every listed deliverable falls inside the "deliverable product" column, and none is taken from scaffolding.

**Closes G9-a.** Status: adjudicated (the delivery boundary = the deliverable-product / scaffolding dichotomy, with the criterion above).

### 7.2 The Two Pending Items Closed Together This Round

**G10 (sub-repo) → closed as "do not split".**

- the only real motive for splitting the repo is "kind polluting the impression of the main repo";
- §7.1 has determined that kind is **scaffolding that the customer never sees**, so the **motive disappears**;
- moreover the current state has **no `.gitmodules` and no submodule**, and 8 `pyproject.toml` files share the root `uv.lock`.

Status: adjudicated (do not split). The single-repo form of the current state is kept; no sub-repo / submodule is created.

**G11 (application without infra) → closed as "do not declare a second form".**

- the deliverable product list is now unique: **chart + image + documentation**;
- consistent with ADR-0013 "Helm-only, no Operator, no second installer"
  ([`../architecture/adr/README.md`](../architecture/adr/README.md));
- `docs/delivery/install-guide.md:5` also already declares this hard boundary.

Status: adjudicated (do not declare a second delivery form).

### 7.3 Adjudication of the Nature of the M5 "Control-Plane Cluster Deployment Proof"

The "control-plane cluster deployment proof (including 7.2d)" among the M5 closure conditions at `docs/plan.md:183` =
**an external basis for performance produced with our internal scaffolding**; it is **not a customer acceptance item** (the customer does not sign that transcript).

Basis: what the customer will press is "can the chart be installed, does an upgrade drop calls", not the kind scripts.
The evidence grading is in category ② of §3 of [`../architecture/README.md`](../architecture/README.md).

### 7.4 Root-Cause Adjudication and the Four-Layer Mechanism (the core of this round)

**Root-cause determination:**

> The "does the project have infra capability" confusion that keeps recurring this time **is not a cognition problem; it is that the fact carriers have no metadata**.

Verified facts:

| Fact | Source |
|---|---|
| the current machine hostname `WIN-03IB7NIEPF0` has **no** helm / kubectl / kind / promtool | measured on 2026-10-11 |
| the path recorded in the evidence file is `==> helm lint /home/shudong/project/3rdparty-as/deploy/helm` | `docs/acceptance/artifacts/m5/2026-10-05/PASS-chart-check-2026-10-05.txt:2` |

**The same user name and the same project path** ⇒ the evidence was produced **on another machine**, while the anonymous "local machine" in the documents actually refers to
**two different machines** — that is the direct cause of every renewed argument.

On that basis the following **four-layer mechanism** is approved and executed:

| Layer | Mechanism | Landing location |
|---|---|---|
| **1** | **the file name is the conclusion** — evidence files under `docs/acceptance/artifacts/**` are forced to carry the prefix `PASS-` / `FAILCLOSED-`, in the format `<verdict>-<item under test>-<date>.txt` | `git mv` has been executed on all 7 files in `docs/acceptance/artifacts/m5/2026-10-05/` |
| **2** | **environments must have names** — a new machine registry | [`docs/environments.md`](../environments.md) (newly created this round) |
| **3** | **the status declaration triple** — anything writing "verified / not verified" must be written as `(verdict, evidence file, date)`; a bare sentence is not allowed | §"citation convention" of `docs/environments.md` |
| **4** | **guard tests** — forbid regression | [`tests/test_evidence_discipline.py`](../../tests/test_evidence_discipline.py) (newly created this round) |

**Layer 1 rename mapping (for resolving the existing references of §1 / §2 — those rows keep their original text per §0.1 and are not changed back):**

| Before renaming (as written in §1 / §2) | After renaming |
|---|---|
| `2026-10-05/gate-full.txt` | `2026-10-05/PASS-gate-2026-10-05.txt` |
| `2026-10-05/gate-sample.txt` | `2026-10-05/PASS-gate-sample-2026-10-05.txt` |
| `2026-10-05/chart-check-full.txt` | `2026-10-05/PASS-chart-check-2026-10-05.txt` |
| `2026-10-05/chart-check-sample.txt` | `2026-10-05/PASS-chart-check-sample-2026-10-05.txt` |
| `2026-10-05/alert-check-full.txt` | `2026-10-05/PASS-alert-check-2026-10-05.txt` |
| `2026-10-05/alert-check-sample.txt` | `2026-10-05/PASS-alert-check-sample-2026-10-05.txt` |
| `2026-10-05/m5-strict-context.txt` | `2026-10-05/FAILCLOSED-m5-strict-context-2026-10-05.txt` |

**Index sync:** the index table of [`docs/acceptance/artifacts/m5/README.md`](../acceptance/artifacts/m5/README.md) has been updated,
and three easily misread facts are stated explicitly (a `FAILCLOSED-` file is not pass evidence; the `[INFO] Fail:` of chart-check is an expected assertion;
`PASS-gate-*.txt` contains SKIPPED entries), together with the principle "the file name prefix governs".

### 7.5 Ownership of Responsibility for P4

`deploy/alerts/as-alerts.yaml` is a **deliverable product** (§7.1), so **its syntax validation must be somebody's responsibility**.

Current state and the gap:

| Fact | Source |
|---|---|
| `SUCCESS: 5 rules found` **only covers the original 5 rules as they were at the time** | `docs/acceptance/artifacts/m5/2026-10-05/PASS-alert-check-2026-10-05.txt:1-3` |
| on 2026-10-10 the two groups `as.runtime` / `as.platform` were added (the original 5 rules unchanged) | `docs/plan.md:67` |
| **those two groups have never been validated by any machine** | —— |

**That gap is retained as a pending execution item** (running `promtool` is required; it is **not run** this round).
Ownership of responsibility: the syntax validation of a deliverable product is a delivery responsibility and must not be left dangling on the grounds that "the evidence comes from a scaffolding environment".

> **〔correction appended in the closing round of 2026-10-11; the original text of "that gap is retained as a pending execution item (running promtool is required, it is not run this round)" above is retained, nothing deleted or changed〕**
> That gap **was executed with containerized promtool in docker on 2026-10-11 and closed**: on the registered environment `dev-win03ib7niepf0`
> (host `WIN-03IB7NIEPF0`), `promtool check rules /alerts/as-alerts.yaml` of `prom/prometheus:v2.45.0` was run,
> outputting `SUCCESS: 10 rules found`
> (as.call-path 5 + as.runtime 3 + as.platform 2, 3 groups / 10 rules in total).
> Triple: **(verified, docs/acceptance/artifacts/m5/2026-10-11/PASS-alert-check-full-2026-10-11.txt, 2026-10-11)**;
> the main agent independently re-ran it on the same day on the same host with the same command, exit=0. See the "current-state correction" of §2 P4 for details.
> **X1 (the capture wiring) is not within this closure**: syntax validation passing does not mean the annotation vs ServiceMonitor/PodMonitor wiring is closed.

**Register items not closed this round (still awaiting maintainer adjudication/handling):** G9-b (the machine capability definition, which layer 2 has given a carrier for but which this section does not adjudicate for you),
G9-c (gate ownership), P1, P5, P6, X1, S1.

> **appended 2026-10-11:** **P2 / P3 have been removed from this list** (both are **closed (2026-10-11)**; the closure basis is in the
> "current-state correction" paragraph of the §2 P2 / P3 entries). Not one of the other listed items was touched. **〔appended in the closing round of 2026-10-11〕the registration of P1 has been withdrawn and it is no longer counted as pending adjudication** (basis in the "registration correction" paragraph of §2 P1: the G2 / A4-4 of §0-A.6 is an already effective adjudication, and §8.1 ④ is a recommendation overridden by it); **the original text of the list above (including P1) is retained unchanged**. **〔appended in this round on 2026-10-11; the original text of the list above (including G9-b / G9-c / P1) is all retained unchanged〕G9-b has been resolved and G9-c has been downgraded, and neither is counted as pending adjudication either** (basis in the status columns of §1 G9-b / G9-c respectively: G9-b is solved by the on-the-spot probing of `docs/environments.md` + `tools/env-probe.sh`, so naming and manual registration are no longer needed; G9-c overlaps §0-A.6 G2 / A4-4 (the same issue) and is likewise not counted as pending adjudication). Accordingly, **the current pending adjudication / handling stance of this list is 5 items: P4, P5, P6, X1, S1** — in sync with the count in item two of §6.1. **Note that the original text of this list, starting at `:567`, still lists only 7 items and does not list P4**: the basis for including P4 is the actual record of the §5 table and the body of §7.5 (see item three of §6.1 and supplementary explanation 1 there), and that supplementation stance remains in effect; this paragraph does not change it.**

> **〔correction appended in the local-toolchain round of 2026-10-11; all the paragraphs above (including the docker closure correction of P4) are retained unchanged; awaiting maintainer review〕**
> The local promtool **2.55.1** (`tools/bin/promtool`, the **same version** as the historical alert evidence of 2026-10-05) completed **native** validation
> of `deploy/alerts/as-alerts.yaml` on the same day on the registered environment **`dev-win03ib7niepf0`** (host `WIN-03IB7NIEPF0`):
> `promtool check rules` → **`SUCCESS: 10 rules found`** (as.call-path 5 + as.runtime 3 + as.platform 2, 3 groups / 10 rules in total; the rule set is unchanged).
> Triple: **(verified, docs/acceptance/artifacts/m5/2026-10-11/PASS-alert-check-2026-10-11.txt, 2026-10-11)**.
> This append **upgrades the evidence basis of P4** — from containerized prometheus **v2.45.0** in docker to **the local promtool 2.55.1 of the same version as the historical evidence**,
> and it **neither changes nor reopens** the closure of P4: **the status remains "closed"**, and no re-adjudication is performed this time.
> The native binary was traced back to extraction from the official quay.io image (the GitHub release tarball was unreachable that day, so it is not a release-tarball installation),
> and the installation path plus the network deviation are in [`2026-10-11-local-infra-bootstrap-execution-record.md`](2026-10-11-local-infra-bootstrap-execution-record.md).

---

**Landing note:** this section is the adjudication record appended on 2026-10-11, **awaiting maintainer review**; it signs off no REQ or milestone,
constitutes no external acceptance pass and lifts no hold. Execution boundary: this round **did not run** `make`, **did not run** `docker`,
and **did not run** `promtool` (so the P4 alert rule validation was still not done); only the root `tests/` was run per the task F authorization
(`uv run pytest tests/ -q` (62 passed)) plus read-only ruff / git queries; **no git write operation was performed**
— `git mv` was used only to rename evidence files (rename detection is preserved, all 7 files are R with zero content changes), and there was **no commit,
no branch creation and no remote change**.

> **Measured re-check append (closing round of 2026-10-11; the original "62 passed" text above is retained, nothing deleted or changed):**
> re-running the root `tests/` later that same day: **`uv run pytest tests/ -q` → `68 passed` (0.27s)**.
> **62 and 68 do not conflict**; they are **measured facts of two different sessions**: the difference comes from the **2** guard cases
> subsequently added to [`tests/test_evidence_discipline.py`](../../tests/test_evidence_discipline.py) ——
>
> | # | New guard case | What it locks down |
> |---|---|---|
> | 1 | `test_environment_probe_markdown_mode_actually_runs` | **actually runs** `bash tools/env-probe.sh --markdown`, requiring exit code 0 and an output whose first line contains the header `环境名`; previously there was only the `bash -n` syntax check, while that probe **in fact failed on every real invocation** with `tr: when not truncating set1, string2 must be non-empty` (measured 2026-10-11; it had never really been run before) |
> | 2 | `test_bootstrap_infra_offers_a_dry_run_and_help` | `tools/bootstrap-infra.sh` exists and still carries the `--dry-run` / `--help` flags, making a side-effect-free dry run possible; **only a static text assertion, the script is not executed** (to avoid a unit test really downloading and installing binaries) |
>
> That file now has 15 `def test_` (some are parameterized, hence 68 collected); the evidence file name / index annotation /
> environment registry / anonymous "local machine has none" line scanning guards of the two layers above are all pre-existing parts.
> **The boundaries stated above ("promtool not run", "no git write operation performed") are not relaxed by this round**: this round only does **document appends** and
> **read-only queries** (`git log` / `git status` / `git diff --stat`); it **did not run** `make` / `docker` / `promtool`,
> **did not commit, did not create a branch, did not change the remote and did not touch tags**. The P4 alert rule syntax validation **was still not done**.

> **Closing round further append of 2026-10-11 (P4 closed; the original texts "62 passed", "68 passed", "the P4 alert rule syntax validation was still not done" etc. are all retained, nothing deleted or changed):**
> **P4 was closed on 2026-10-11**, triple **(verified, docs/acceptance/artifacts/m5/2026-10-11/PASS-alert-check-full-2026-10-11.txt, 2026-10-11)**
> — containerized promtool v2.45.0 in docker validated the 3 groups / 10 rules with `SUCCESS: 10 rules found`,
> and the main agent independently re-ran the same command on the same day on the same host (`WIN-03IB7NIEPF0`) with exit=0; see the "current-state correction" of §2 P4 and the appended correction of §7.5.
> This round the main agent **performed only one read-only docker promtool validation**: the container was `--rm` and had no side effects other than the mounted validation path,
> **not a single byte of `deploy/alerts/` was changed**; the document wrap-up of this round **performed no git write operation** (no commit / add / push / tag / branch creation / remote change),
> and `make` was not run. Re-run of the root `tests/`: **`uv run pytest tests/ -q` → `76 passed` (0.27s)**
> — like 62 / 68, these are measured facts of different sessions (the guard cases keep being added batch by batch), and the three numbers do not conflict.

---

## 8. Meta-Rule (appended 2026-10-11)

### 8.1 List Length and Withdrawal of Entries

This document's list has no minimum length. Once an issue is resolved it is removed from the list, and the list getting shorter is a normal outcome; entries must not be added in order to maintain the form, to pad the item count, or to make the register look complete. If an entry was previously listed as pending adjudication by mistake, it should be withdrawn rather than kept.

**Background**: this rule emerged from the 2026-10-11 review; the background is that on that day "already-adjudicated items were re-listed as pending adjudication" and "items already resolved by actual work were still listed as pending adjudication" kept recurring. The standard practice for withdrawing a registration is: append a correction note at the original entry (stating the reason and date for withdrawal), and append corrections to the §5 summary table and the relevant counts in §6/§7; the original text is always retained as the audit chain.

---

## 9. Correction of Line-Number Reference Drift in `docs/plan.md` (appended 2026-10-12)

> This section **only appends** corrections; all `docs/plan.md:<line number>` references registered in §1–§8 of this document are **all retained and not changed back**
> (consistent with the existing practice of §7.5 "`:180` → `:184`").

**Cause**: between 2026-10-11 and 2026-10-12, content was **appended** to `docs/plan.md` (3 new rows in the §0 decision record table,
26 lines of the "O1 stance recommendation" paragraph after the §5.1 table), which shifted some of the line references registered here.
What is registered is **the line numbers at the time of registration**, which is not an error; this section gives the current line numbers relocated by anchor text.

| Reference registered here | Anchor text (used for relocation) | Current line number | Drift |
|---|---|---|---|
| `docs/plan.md:15` | §0 status table "the step currently in progress" (the M7.1 demo runs on kind) | `15` | 0 (unaffected) |
| `docs/plan.md:39` | **G2 / A4-3** of the §0 decision record table (Wave 2 replay) | `39` | 0 |
| `docs/plan.md:40` | **G2 / A4-4** of the §0 decision record table (kind e2e and the PR boundary) | `40` | 0 |
| `docs/plan.md:41` | **G3 / A5** of the §0 decision record table (monitoring wiring) | `41` | 0 |
| `docs/plan.md:53` | the row holding the **2026-10-11 note** of the §0 decision record table (the G3(A5) copy) | `53` | 0 |
| `docs/plan.md:65` | the **blocked items** paragraph under "product packaging delivery status" | `76` | +11 |
| `docs/plan.md:66` | the "unlock status of the row above" paragraph of the same section (the three remaining dependencies) | `77` | +11 |
| `docs/plan.md:67` | the "code side: only two alert rule groups added under `deploy/alerts/`" of the same section | `78` | +11 |
| `docs/plan.md:183` | the **M5** row of the milestone table (the closure condition contains "control-plane cluster deployment proof (including 7.2d)") | `194` | +11 |
| `docs/plan.md:396` | the **O1** row of the §5.1 open-items table | `407` | +11 |
| `docs/plan.md:399` | the **O4** row of the §5.1 open-items table | `410` | +11 |
| `docs/plan.md:400` | the **O5** row of the §5.1 open-items table | `411` | +11 |
| `docs/plan.md:406` | the **D1** row of the §5.2 open-items table | `456` | +50 |
| `docs/plan.md:408` | the **D3** row of the §5.2 open-items table | `458` | +50 |
| `docs/plan.md:410` | the **D5** row of the §5.2 open-items table | `460` | +50 |

**Drift explanation**: references up to §5.1 and before are uniformly **+11** (5 rows accumulated in the §0 decision record table);
the §5.2 references add **+39** on top (the "O1 stance recommendation" paragraph and the "adopted and confirmed" paragraph added after the §5.1 table), totalling **+50**.

> **Third refresh (appended again later on 2026-10-12; the "current line number" column above has been refreshed, and the drift stance is now `+11` / `+50`)**:
> on 2026-10-12 `docs/plan.md` had appended the "A6 execution stance" row and the "the nine M8 N2 items have been counter-signed by the agent" row
> of the §0 decision table (+1 in §0 in total, +5 accumulated), plus the "§5.2-bis · the M5 defer items are settled (M5D-1…M5D-6)" section of §5.
> Note that §5.2-bis is inserted **after** the §5.2 table and **before** §5.3, so the D1 / D3 / D5 rows inside the §5.2 table
> are **affected only by the +5 of §0 and the +39 of §5.1**, and not by §5.2-bis.
> This section only corrects line-number positioning; the substantive stance of the §5 summary table and the §7 lists is **not changed by a single character**.

**Boundary**: this section only corrects **line-number positioning** and **does not change** the substantive content, conclusion or status of any item.
The "closed / pending" stance of the §5 summary table and the §7 lists is **not changed by a single character**;
**X1 remains the only current pending adjudication item**.
