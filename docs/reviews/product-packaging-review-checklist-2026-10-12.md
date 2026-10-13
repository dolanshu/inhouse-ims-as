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

# Productization Packaging 16 Documents · Review Item Checklist (B6)

> **Written to disk: 2026-10-12. Status: the review has been executed (2026-10-12), and all 16 conclusions are "needs modification" (accept 0 / rejected 0); the conclusions were filled in by the agent after reviewing by batch + spot-check re-verification by the primary agent, and await maintainer confirmation.**
>
> **This document is the review vehicle of B6**: §4 **B6 · Review of the 16 productization packaging documents** of [`../handoff/2026-10-10-unfinished-assessment-and-next-plan.md`](../handoff/2026-10-10-unfinished-assessment-and-next-plan.md),
> and its exit criterion is
> "review the 16 documents one by one, leave the conclusion (accept / needs modification / rejected) in a review record; re-review after the needs-modification items are closed;
> the batch status in §5 of `docs/product-packaging-plan.md` is updated per the review results". **Who does it: the maintainer.**
>
> On 2026-10-12 the maintainer required that "the review items be written to disk separately" —— this document is that deliverable:
> it fixes "what is reviewed" and **fills in no conclusion on the maintainer's behalf**.
>
> **Appended 2026-10-12: the maintainer instructed that the review be executed and written to disk, with the conclusion column filled in by the agent (based on the G6/G7/G8/G4 etc. adjudicated positions already in effect on 2026-10-12 and the repository measurements); the conclusions await maintainer confirmation and do not constitute a basis for external delivery or acceptance.**
>
> **Appended again 2026-10-12 (closure re-review)**: all 16 "needs modification" items have been closed and re-reviewed —— the re-review conclusions are in **§7** (accept 16 / needs modification 0 / rejected 0, **awaiting maintainer confirmation**); §1–§6 are the pre-closure record, unchanged.
>
> **The conclusions filled in this document do not replace the maintainer's final judgment**; the conclusion column was filled in by the agent on 2026-10-12 (see §3 and §6), and before maintainer confirmation it is not a basis for any sign-off.

---

## 1. Counting Basis (align first, to avoid "16 documents" not meaning the same set of things)

| Directory | Number of `.md` Files Counted | Details |
|---|---|---|
| `docs/product/` | **6** | `one-pager.md`, `compliance-matrix.md`, `ne-datasheet.md`, `responsibility-matrix.md`, `security-privacy.md`, `version-lifecycle.md` |
| `docs/operations/` | **7** | `README.md`, `runbook-l1.md`, `runbook-l2.md`, `alert-response-matrix.md`, `fault-demarcation.md`, `rollback-playbook.md`, `backup-restore.md` |
| `docs/delivery/` | **3** | `README.md`, `install-guide.md`, `airgap-package.md` |
| **Total** | **16** | — |

**Incidental assets not counted among the 16 but needing a look in the same batch** (usually reviewed together with the 16):

- **2 Grafana dashboard JSONs** under `docs/operations/grafana-dashboards/` + the dashboard `README.md`
- `docs/delivery/preflight.sh`
- `bundle-images.sh`, `load-images.sh`, `images.txt` under `docs/delivery/scripts/`

---

## 2. The Four Common Dimensions Every Document Must Pass

When the maintainer reviews document by document, it is suggested to answer these four questions for **each** document (the conclusion column records these four items):

| # | Dimension | What Must Be Answered |
|---|---|---|
| **D-1** | **Factual accuracy** | Is what the document states consistent with the repository's **current actual state**? Are there stale statements (for example still writing "pending adjudication" when the value has been adjudicated, or the other way round)? |
| **D-2** | **Consistency with adjudicated positions** | Is it consistent with the adjudications already **in effect** in the §0 decision record table (especially O4 / D5 / O5 / D3 / the G4 version basis / the G8 target scenario and naming)? |
| **D-3** | **External usability** | Can this serve as a basis for **external delivery or acceptance**? If not, what is missing? |
| **D-4** | **follow-up** | Does it need modification / supplementary writing / another adjudication? If so, state the dependency explicitly |

Conclusion values: **accept** / **needs modification (with the items specified)** / **rejected (with the reasons specified)**.

---

## 3. Document-by-Document List (the conclusion column was filled in by the agent on 2026-10-12, awaiting maintainer confirmation)

### 3.1 `docs/product/` (6 documents)

| # | File | Known Points Requiring Focused Verification | Conclusion | Notes |
|---|---|---|---|---|
| 1 | [`one-pager.md`](../product/one-pager.md) | Whether the target scenario matches the adjudicated "xxCarrier internal production readiness / release review" (G8); whether the descriptive product name is `In-house IMS Application Server` | needs modification | Three G8 stale items (:5/:6/:7); O4/D5/O5 stale (:170-172); e2e=0 (:168) |
| 2 | [`compliance-matrix.md`](../product/compliance-matrix.md) | The "14 full-replay items unsigned" recorded at `:79` / `:117` / `:234` / `:266` —— after 2026-10-12 REQ-F-1 has entered "automated **subset** covered / full text still open"; does this wording need to be synced | needs modification | G8 stale (:5); 4 stale instances of REQ-F-1 "14 items unsigned" (:79/:117/:234/:266); e2e 0 items (:263) |
| 3 | [`ne-datasheet.md`](../product/ne-datasheet.md) | **Whether capacity values have been filled in** —— the O1 values are still unadjudicated; this round only landed the "internal engineering target lower-bound baseline", so **the external capacity values should still be empty** | needs modification | Capacity discipline compliant (no 1280 value); 10 stale instances in total for naming + O4/D5/O5/D3/e2e (:11/:26/:40/:234/:302/:356-359/:367/:382) |
| 4 | [`responsibility-matrix.md`](../product/responsibility-matrix.md) | Whether it is consistent with the product positioning (deployed outside the carrier network, single-tenant on-prem) | needs modification | Product positioning consistency compliant; 2 stale for naming + e2e, and 5 stale for O4/D5/O5/D3 (:5/:11/:167/:192-194/:198/:213) |
| 5 | [`security-privacy.md`](../product/security-privacy.md) | It was **additively synced** per the O4 / D5 adjudications on 2026-10-11; but the fact recorded in §4.1 that the "chart has **no backup Job**" has **not changed**, so the backup-restore approach is still not closed | needs modification | O4/D5/O5 are synced with no "completed" statements, and the unchanged fact that the chart has no backup Job is compliant; residual :289 status-discipline line + :5 body text stale |
| 6 | [`version-lifecycle.md`](../product/version-lifecycle.md) | §7 "API version compatibility policy" is listed in the form of "**candidate, undecided**" with **no ADR** —— it is the same thing as Lane D **4.3** | needs modification | §7's wording and Lane D 4.3 are correct and §3 is a pure restatement of ADR-0027 (compliant); 3 stale instances of naming; :118 "no automation" is stale (sync-chart-version.sh has landed) |

### 3.2 `docs/operations/` (7 documents)

| # | File | Known Points Requiring Focused Verification | Conclusion | Notes |
|---|---|---|---|---|
| 7 | [`README.md`](../operations/README.md) | Whether the navigation covers all 8 documents + the dashboards | needs modification | :25 the O4/O5/D3/D5 "undecided" column is stale; :80 e2e=0; the §1 layering table lacks the layer, making the location claimed by alert-response-matrix:6 fall through |
| 8 | [`runbook-l1.md`](../operations/runbook-l1.md) | Whether the front-line handling steps match the actual alert rule set (3 groups, 10 rules in `deploy/alerts/`) | needs modification | :29 wrong citation (the source of 7.2d should be plan §3.2 / deliverable 2.4 row); :47/:194 O5/D3 undecided is stale; :7 e2e=0 |
| 9 | [`runbook-l2.md`](../operations/runbook-l2.md) | Second-line steps; whether capabilities that are not yet implemented (such as trace query, Redis Sentinel) are cited | needs modification | No instance was found of unimplemented capabilities being written as executable steps (compliant); :21 O4/D5 undecided, :98/:180 O5/D3 undecided is stale; :5 e2e=0 |
| 10 | [`alert-response-matrix.md`](../operations/alert-response-matrix.md) | Whether it corresponds rule by rule to the 3 groups and 10 rules in `deploy/alerts/as-alerts.yaml` | needs modification | :68 "check Sentinel/failover status" is not executable under a single-replica chart; O5/D3 undecided is stale; 4 instances of e2e=0; the promtool pass result of 2026-10-11 was not recorded |
| 11 | [`fault-demarcation.md`](../operations/fault-demarcation.md) | Whether the boundary wording is consistent with `responsibility-matrix.md` | needs modification | The boundary wording is consistent with responsibility-matrix (compliant); :38/:117/:298/:299 O4/D5/O5/D3 stale; :15 e2e=0 |
| 12 | [`rollback-playbook.md`](../operations/rollback-playbook.md) | Whether the rollback steps depend on chart version consistency —— A6 has adjudicated "automatic sync" but **the sync has still not happened** | needs modification | It does not claim a drill was performed (compliant); the whole document has 0 mentions of VERSION/Chart.yaml/kubeVersion, so the L3 rollback lacks a version mapping; :126/:162 O5/D3 stale |
| 13 | [`backup-restore.md`](../operations/backup-restore.md) | It was **additively synced** per the O5 / D3 adjudications on 2026-10-11; but the **RPO / RTO values are still unadjudicated**, and D5 (in-cluster PostgreSQL) **is not implemented** | needs modification | RPO/RTO given no values and D5 not implemented are recorded faithfully (compliant); the :166 note was written as a single-column table row breaking the §7 table; :27/:150/:162-164 the main cells still say pending adjudication; :164 and :166 are self-contradictory |

### 3.3 `docs/delivery/` (3 documents)

| # | File | Known Points Requiring Focused Verification | Conclusion | Notes |
|---|---|---|---|---|
| 14 | [`README.md`](../delivery/README.md) | Whether the navigation covers the 3 documents + the scripts | needs modification | The navigation has no dead links (compliant); L82 "manually verify VERSION/Chart" is stale (it should cite sync-chart-version.sh --check); the delivery manifest lacks deploy/alerts/ (only three of the four categories in G9-a have landed) |
| 15 | [`install-guide.md`](../delivery/install-guide.md) | §2's delivery manifest and `:19` / `:91` are the existing landing of the "delivery boundary decision line"; do the installation steps depend on the chart version (`kubeVersion` has been set to `>=1.23.0-0` but is **not yet written into Chart.yaml**)? | needs modification | §2 lacks the alert rules; :39 the chart package name is inaccurate (currently 0.0.0-skeleton.tgz); the §5 fail-closed wording misses the synonymous wording in deployment.yaml and does not point out that allowEmptyAllowlistForTest must be false in production; :195 manual verification is stale |
| 16 | [`airgap-package.md`](../delivery/airgap-package.md) | Whether the offline package steps are consistent with `scripts/bundle-images.sh` / `load-images.sh` / `images.txt` | needs modification | The digest syntax taught by §5/§6 will be rejected by bundle-images.sh:205 (the document contradicts the script); the artifact naming is not faithful; the L191 "when not yet written to disk" parenthetical is outdated; §2 lacks the alert-rule delivery path |

---

## 4. The Three Boundaries Most Easily Missed During Review

1. **"Adjudicated" does not mean "implemented".** O4 (10-day retention) / D5 (in-cluster PG) / O5 (N+1 + cross-site 1+1) / D3 (Redis Sentinel)
   have only had their **values** adjudicated; trace storage query/deletion and Redis Sentinel are **both not implemented**.
   Any completion-tense statement of the form "the system cleans up after 10 days" or "Sentinel switches over automatically" in a document is a needs-modification item.
2. **A green real stack on this machine is not external capacity.** The saturation-point probe of 2026-10-12 (CPS 1280 with no failures) is
   a **lower-bound baseline under this machine's loopback model**, not a capacity target value and not a commitment value;
   the capacity values of `ne-datasheet.md` **must not** be filled in on that basis.
3. **A `promtool` pass does not mean the alerts are usable.** Syntax validation has passed (3 groups, 10 rules), but **the scrape wiring X1 is not closed**;
   any statement involving "the alerts can be received" needs attention.

---

## 5. Write-back After the Review Is Complete (by the maintainer or per their instruction)

- [x] Fill in the conclusion and notes for all 16 documents one by one (accept / needs modification / rejected) —— **completed 2026-10-12**: conclusions in §3, the detail of the needs-modification items in §6
- [ ] Re-review after the needs-modification items are closed, and **append** the re-review results to this document (the original text is unchanged) —— **not executed (2026-10-12)**: none of the needs-modification items has been closed, and the re-review will be performed after closure
- [x] Re-review after the needs-modification items are closed, and append the re-review results to this document (the original text is unchanged) —— **executed 2026-10-12 (this row is an append; the "not executed" in the previous row is the pre-closure state, preserved as an audit chain)**: the 16 re-review conclusions are in §7 (accept 16 / needs modification 0 / rejected 0, awaiting maintainer confirmation); among the incidental assets, the dashboard README and the three delivery scripts moved from "needs modification" to accept.
- [x] Update the batch status in §5 of `docs/product-packaging-plan.md` per the review results —— **completed 2026-10-12**
- [x] Sync the review conclusions back into the exit criterion of §4 **B6** of [`../handoff/2026-10-10-unfinished-assessment-and-next-plan.md`](../handoff/2026-10-10-unfinished-assessment-and-next-plan.md) —— **completed 2026-10-12**

---

**Written to disk: 2026-10-12. Status: the checklist has been created, and the review conclusions await the maintainer's filling in.**
(This document reviews nothing and signs off no document; it does not replace the maintainer's judgment and does not constitute a basis for external delivery or acceptance.)
**Appended 2026-10-12 (the signature block above is the original text at checklist creation, preserved as an audit chain): the review has been executed, the conclusions are in §3 and §6; all 16 are "needs modification" (accept 0 / rejected 0), awaiting maintainer confirmation.**
**Appended again 2026-10-12 (the rows above are the pre-closure states, preserved as an audit chain)**: the needs-modification items have been closed and re-reviewed, the conclusions are in §7 (accept 16 / needs modification 0 / rejected 0, awaiting maintainer confirmation).

---

## 6. Review Record (2026-10-12)

> **Nature**: this section is the landing record of the first exit criterion of B6 ("review the 16 documents one by one and leave the conclusion in a review record").
> **It signs off no REQ, signs off no milestone, and does not constitute external delivery or an acceptance pass**; the conclusions were filled in by the agent and **await maintainer confirmation**.
> Review method: three read-only review agents reviewed by batch (product / operations / delivery) + the primary agent spot-checked and re-verified 4 pieces of key evidence.

The quoted original text in §6.2 and §6.4 is the exact wording in the documents under review and is kept verbatim.

### 6.1 Summary

| Batch | Count | accept | needs modification | rejected |
|---|---|---|---|---|
| `docs/product/` | 6 | 0 | 6 | 0 |
| `docs/operations/` | 7 | 0 | 7 | 0 |
| `docs/delivery/` | 3 | 0 | 3 | 0 |
| **Total** | **16** | **0** | **16** | **0** |

**Incidental assets (not counted among the 16)**: `grafana-dashboards/overview.json`, `sip-signaling.json`, `scripts/images.txt` = **accept**;
`grafana-dashboards/README.md`, `preflight.sh`, `scripts/bundle-images.sh`, `scripts/load-images.sh` = **needs modification** (details in 6.4).

### 6.2 Document-by-Document Details of the Needs-Modification Items

(For each document the key points and line numbers are listed; the "compliant points" are the parts of that document already verified as problem-free, recorded together so as to avoid duplicated effort at re-review time.)

#### docs/product/

1. **one-pager.md**: ① `:7` target scenario stale —— it still writes "xxCarrier internal go-live review / current default direction / a formal decision landing point has not yet been formed", which should be the adjudicated position "xxCarrier internal production readiness / release review" (G8-1); ② `:5` naming stale —— "文档暂用名 / 不是已正式批准的产品名" has been overturned by G8-2 (the descriptive name is formally adopted, not a trademark/brand claim); ③ `:6` "repo name planned to be changed to" is stale (G8-3 records it as completed); ④ `:168` "e2e marker is 0" is stale (actually 8 items pass stably); ⑤ `:170` O4 "undecided" is stale (the default of 10 days has been adjudicated and is deployment-configurable; the implementation has not landed); ⑥ `:171` D5 "undecided" is stale (in-cluster PostgreSQL has been adjudicated); ⑦ `:172` O5 "undecided" and still listing the "N+1 single node / N+M racks or AZ" options is stale (in-site N+1 + cross-site 1+1 has been adjudicated; the only remaining unadjudicated items are the RPO/RTO values). Compliant points: `:10/:34/:142/:169` statements about O1 being unadjudicated and no capacity figures being written are consistent with reality.
2. **compliance-matrix.md**: ① `:5` naming stale (same as 1②③); ② `:79`/`:117`/`:234`/`:266` "14 full-replay items unsigned" is stale —— REQ-F-1 is now "automated subset covered / full text still open" (the Wave2 normalized cross-check covers the S1 two-leg skeleton, C_in≠C_out, and SDP byte-for-byte identity; the 14 item-by-item header cross-check was not done); ③ `:263` "e2e 0 items" is stale. Compliant points: the open annotations and the evidence-grading discipline at `:12`/`:13`/`:35`/`:187`/`:220-222` are faithful.
3. **ne-datasheet.md**: the capacity discipline is **fully compliant** —— the whole document contains no CPS/BHCA/CAPS values, §3 only gives the model structure and measurement methodology, the §3.6 entry-approval three-precondition status annotation is accurate, and the CPS 1280 lower-bound baseline of 2026-10-12 has not been written as a capacity value. Needs modification: ① `:1`/`:5` naming stale; ② `:11`/`:382` "O1/O4/O5/D3/D5 undecided" stale; ③ `:26`/`:367` "e2e=0" stale; ④ `:40`/`:234`/`:270-271`/`:274`/`:297`/`:302`/`:358`/`:359` O5/D3 "undecided" and `:302` still listing "rack/AZ" as to be chosen is stale; ⑤ `:356`/`:357` O4/D5 "undecided" stale. Compliant points: the version desynchronization (`:23`/`:314`/`:340`), the X1 scrape gap (`:216`/`:300`/`:328`/`:364`), and the correspondence of the 3 alert groups and 10 rules are all faithful; the fact that the "chart has no backup Job" has not changed.
4. **responsibility-matrix.md**: product positioning consistency is **fully compliant** (single-tenant on-prem, deployed outside the carrier network, S-CSCF triggered via S-SBC, consistent with ADR-0003/G-P0-5). Needs modification: ① `:5` naming stale; ② `:11`/`:198` "e2e=0" stale; ③ `:167`/`:192`/`:193`/`:194`/`:213` O4/D5/O5/D3 "undecided" stale, among which `:194` contradicts `:168` (ADR-0008 N+1 + 1+1 warm standby).
5. **security-privacy.md**: the O4/D5/O5 sync quality is the best (9 additive notes, with no completion-tense statement of the form "the system cleans up after 10 days"; the fact that the "chart has no backup Job" has not changed and has been empirically verified). Needs modification: ① `:289` the status-discipline summary line is stale and not covered by any note ("e2e marker is 0; O1/O4/O5/D1/D3/D5 undecided"); ② `:5` body-text naming is stale (the `:6` note already covers it; it is suggested to rewrite the body text and keep the note as an audit chain); ③ `:259-260` the coexistence of body text and note is easy to misread, and it is suggested to synchronize them.
6. **version-lifecycle.md**: §7 "API version compatibility policy = candidate, undecided, no ADR" is the same thing as Lane D 4.3 and its exit conditions are complete (compliant); §3 restates ADR-0027 item by item without adding new promises (compliant). Needs modification: ① `:5`/`:6`/`:231` naming stale; ② `:118` "version bump has no automation" is stale —— `scripts/sync-chart-version.sh` landed on 2026-10-12 (read-only by default with `--check`, exit 1 on drift; `--apply` not executed, and G4 "currently no modification" remains in effect); ③ the "suggested fix" at `:79`/`:241` should be upgraded to "automatic sync adjudicated, script ready, first execution timing pending the maintainer's decision".

#### docs/operations/

7. **README.md**: the navigation covers 7 documents + the dashboards and the links are valid (compliant). Needs modification: ① `:25` still lists O4/O5/D3/D5 as "undecided items"; ② `:80` "e2e = 0" is stale; ③ the §1 layering table has only the L1/L2 rows, so the "layer above L1/L2" position claimed by `alert-response-matrix.md:6` does not exist in the README (a cross-document broken link).
8. **runbook-l1.md**: the 10 alerts correspond rule by rule, the X1 scrape gap is not glossed over, and the triggerability judgments are accurate (compliant). Needs modification: ① `:29` wrong citation —— the source of "M4b-7.2d / M8 7.2d blocked" is marked as items 1 and 3 of §0.3 of `product-packaging-plan.md`, but those two items are respectively "the M8 exit sign-off is shelved" and "no lab evidence for carrier PKI"; the true source of 7.2d is §3.2 and the deliverable 2.4 row; ② `:47`/`:194` "Redis HA is still the undecided item O5/D3" is stale; ③ `:7` "e2e marker = 0" is stale.
9. **runbook-l2.md**: no instance was found of unimplemented capabilities (trace query, Sentinel switchover) being written as executable steps (compliant); `:202` proactively notes that a citation to the original cannot be resolved (good self-check). Needs modification: ① `:21` "O4/D5 unadjudicated" is stale; ② `:98`/`:180` "Sentinel topology / Redis HA belongs to undecided O5/D3" is stale (it should be changed to: the values have been adjudicated, the chart is still single-replica, and there is no evidence of measured failover behaviour); ③ `:5` "e2e marker = 0" is stale.
10. **alert-response-matrix.md**: it corresponds rule by rule to the 3 groups and 10 rules in as-alerts.yaml and is consistent with ne-datasheet §6 (compliant). Needs modification: ① `:68` step 3 of the first-check action "check Sentinel/failover status" has nothing to check under a single-replica chart (a non-executable step); ② `:192` and the `:68` evidence column "O5/D3 undecided" are stale; ③ `:10`/`:14`/`:109`/`:189` — 4 instances of "e2e=0" are stale; ④ the result of `promtool check rules` passing on 2026-10-11 (10 rules found) was not recorded in this document; ⑤ the position description at `:6` is broken against README §1 (same as 7③).
11. **fault-demarcation.md**: it is line-by-line consistent with responsibility-matrix on attribution/packet-capture responsibility (compliant). Needs modification: ① `:38` item ⑤ "O4/D5 unadjudicated" is stale; ② `:117`/`:298` "O5/D3 undecided" are stale; ③ `:299` "O4/D5 pending adjudication" is stale; ④ `:15` "e2e marker = 0" is stale.
12. **rollback-playbook.md**: it does not claim a real-cluster drill was performed (`:115`/`:134`/`:157` are all annotated faithfully) (compliant). Needs modification: ① **the whole document (indeed the whole directory) has 0 mentions of VERSION/Chart.yaml/appVersion/kubeVersion** —— the L3 `helm rollback <revision>` lacks the "revision → product version" mapping precondition, the §5 drill record template cannot be back-filled with the product version, and the rollback evidence chain is not externally verifiable; ② `:126`/`:162` "O5/D3 undecided" are stale.
13. **backup-restore.md**: RPO/RTO are not unilaterally given values, D5 is not implemented, and there is no completion-tense statement of the form "cleanup after 10 days" (compliant); it is the only document of the operations batch covered by 2026-10-11 task E. Needs modification: ① the additive note at `:166` was written as a single-column table row inserted in the middle of the four-column §7 table, so the column count does not match after rendering; ② the main cells at `:27`/`:150`/`:162`/`:163`/`:164` still say "pending adjudication / undecided" (the notes cover them but the reader reads the stale conclusion first); ③ `:164` "can only write pending adjudication" contradicts the note at `:166`.

#### docs/delivery/

14. **README.md**: the navigation covers 3 documents + 4 script assets, has no dead links, and the three-step process table corresponds to the 12 check sections of preflight.sh (compliant). Needs modification: ① L82 (and row 4 of §5) "VERSION/Chart not synchronized → manual verification at packaging time" is stale and should be changed to "run `scripts/sync-chart-version.sh --check` (read-only, exit 1 on drift); `--apply` is left to the maintainer's first synchronization"; ② the §2/§3 delivery manifest does not list the `deploy/alerts/` alert rules —— only three of the four delivery product categories defined by G9-a have landed.
15. **install-guide.md**: §2's decision line has landed (`:19`/`:91`) and the command sequence is word-for-word consistent with the runbook (compliant). Needs modification: ① the §2 delivery manifest lacks an alert-rule row; ② `:39` "`3rdparty-as-<version>.tgz`" is inaccurate —— `helm package` is named after the name/version in Chart.yaml, and the current artifact is actually `3rdparty-as-0.0.0-skeleton.tgz` (not synchronized with VERSION 0.2.0); ③ the §5 fail-closed wording only cites `validate-install.yaml:6/9/12` and misses the synonymous wording at `deployment.yaml:12/15` (the 2026-10-11 chart-check artifact empirically shows one lint output with 4 Fails), and does not point out that `sip.allowEmptyAllowlistForTest` (values.yaml:165) must be false in production; ④ `:195` "manually verify all three" is stale (same as 14①); ⑤ (suggested) `:148` "already green" is a bare status sentence and should be supplemented with the (conclusion, evidence file, date) triple.
16. **airgap-package.md**: it corresponds item by item to the steps, artifacts and exit codes of the bundle/load scripts, with no second installation form (compliant). Needs modification: ① **the digest pinning syntax taught by §5/§6 together with images.txt (`repository:tag@sha256:...`) will be rejected by the format validation at `bundle-images.sh:205`** (that validation's glob is written backwards, so any digest entry hits `die`) —— the document contradicts the script, which is a hard defect for external delivery; ② the artifact naming in §3 is not faithful (the tgz is named after Chart.yaml and is currently `0.0.0-skeleton`; without `--platform`, the tar suffix is `unspecified`); ③ the L191 "when install-guide.md is not yet written to disk" parenthetical is outdated (it has landed); ④ §2 lacks the alert-rule delivery path description.

### 6.3 Cross-File Common Issues (it is suggested to open a separate item; this review does not execute the modifications)

1. **The "task E" sync coverage gap**: the downstream document sync of 2026-10-11 (register §2 P3) only covered `product/security-privacy.md` and `operations/backup-restore.md`; the other 14 .md files still write "O4/O5/D3/D5 undecided". 15 of the 16 documents in this batch have stale items stemming directly from this. It is suggested to complete the sync under the same discipline and then re-review.
2. **The e2e basis is outdated**: there are 9+ instances of "e2e marker = 0" across the batch, while 8 items actually pass stably. The root cause is that the marker table in `docs/acceptance/test-plan.md` was not synced (its REQ-F-1 section has been updated). It is suggested to fix that table first and then back-fill each document.
3. **Chart version consistency is missing**: VERSION 0.2.0 and Chart.yaml 0.0.0-skeleton are not synchronized, and kubeVersion is not written —— this directly affects the executability of rollback-playbook L3, the artifact naming of install-guide/airgap, and the "no automation" statement of version-lifecycle. `scripts/sync-chart-version.sh` is ready; the timing of the first `--apply` is pending the maintainer's decision.
4. **The delivery manifest lacks the alert rules**: none of the three delivery documents + README lists `deploy/alerts/` per G9-a (promtool has verified 3 groups and 10 rules; the X1 scrape wiring being unclosed must be explained to the customer).
5. **Functional defects in the incidental assets**: the digest validation at `bundle-images.sh:205` is written backwards; the `--values` promise in `load-images.sh` to infer the Secret name is not implemented (only an existence check); `preflight.sh:509-510` falsely reports "runtime state store unavailable" for external Redis/Sentinel deployments (blocking installation under --strict; REDIS_URL should not be present at all under Sentinel); `preflight.sh:34` has a bad byte. In addition: `load-images.sh:146/196` uses mapfile and preflight uses bash 4.4 array expansion, and the three scripts do not declare a bash version floor.

### 6.4 Details of the Incidental Asset Conclusions

| Asset | Conclusion | Key Points |
|---|---|---|
| `grafana-dashboards/overview.json` | accept | The 15 panels are consistent with the README statement; all metric names hit `platform/src/as_platform/telemetry/metrics.py:34-39`; no capacity figures, no Sh panel, and the description declares that scraping is unclosed |
| `grafana-dashboards/sip-signaling.json` | accept | 7 panels; same as above; label usage is compliant |
| `grafana-dashboards/README.md` | needs modification | The description of panel 5 at `:46` is inconsistent with the two independent targets in the JSON; `:141` "O5/D3 undecided" is stale; `:9` "e2e=0" is stale |
| `delivery/preflight.sh` | needs modification | External Redis/Sentinel falsely reported as WARN at `:509-510` (blocking under --strict); the bash≥4.4 floor is not declared; bad byte at `:34`. The correspondence between the check items and chart/values is correct overall |
| `delivery/scripts/bundle-images.sh` | needs modification | The digest validation glob at `:205` is written backwards; `:95` `--destination` is an orphan option not documented in the usage |
| `delivery/scripts/load-images.sh` | needs modification | The `--values` help text promises "inferring the required Secret name" but only performs an existence check; the remaining behaviour is consistent with the documentation |
| `delivery/scripts/images.txt` | accept | Consistent item by item with the default images in values.yaml; the empty tag falling back to appVersion (currently 0.0.0) is explained faithfully; the digest precedent will be usable after the script is fixed |

### 6.5 Re-review and Closure

- The needs-modification items of the 16 documents are **all unclosed**, and the re-review is **not executed**; after closure the re-review results must be **appended** to this document (the original text is unchanged).
- The modification actions themselves are **not authorized to be executed**: this review only fills in conclusions and does not change a single byte of the 16 documents or the incidental assets.
- After the maintainer confirms this review's conclusions, item 2 of the B6 exit criterion (re-review after the needs-modification items are closed) can be advanced.

**(§6 of this document reviews nothing beyond the documents and signs off no existing conclusions, and does not constitute a basis for external delivery or acceptance.)**

---

## 7. Re-review (2026-10-12; executed after the needs-modification items were closed)

> **Nature**: this section is the landing record of item 2 of the B6 exit criterion ("re-review after the needs-modification items are closed"), implementing the convention in §6.5 that "after closure the re-review results must be **appended** to this document (the original text is unchanged)" —— **the original text of §1–§6 is unchanged throughout**.
>
> **Re-review scope**: the 16 "needs modification" items listed document by document in §6.2 + the 5 cross-file common issues in §6.3 + the incidental asset conclusions in §6.4.
>
> **Re-review method**: three writable subagents reviewed and closed by batch (product / operations / delivery) + the primary agent verified the change surface batch by batch with `git status` / `git diff`, and spot-checked the key empirical evidence (`bash -n` passed for all three scripts; four items of `bundle-images.sh --dry-run` empirically verified: a valid digest / a missing tag / a non-sha256 / a pure tag exited 0 / 1 / 1 / 0 respectively; a full-batch scan of stale residue) before filling in the re-review conclusions.
>
> **Boundaries (the same as §6)**: this section signs off no REQ, signs off no milestone, and does not constitute external delivery or an acceptance pass; all conclusions **await maintainer confirmation**.

### 7.1 Summary

| Batch | Count | Pre-closure conclusion (§6) | Post-closure re-review conclusion | Notes |
|---|---|---|---|---|
| `docs/product/` | 6 | needs modification 6 | **accept 6** (awaiting maintainer confirmation) | All needs-modification items closed |
| `docs/operations/` | 7 | needs modification 7 | **accept 7** (awaiting maintainer confirmation) | All needs-modification items closed |
| `docs/delivery/` | 3 | needs modification 3 | **accept 3** (awaiting maintainer confirmation) | All needs-modification items closed |
| **Total** | **16** | **needs modification 16** | **accept 16** (awaiting maintainer confirmation) | accept 16 / needs modification 0 / rejected 0 |

**Incidental asset re-review**: `grafana-dashboards/README.md`, `delivery/preflight.sh`, `delivery/scripts/bundle-images.sh`, `delivery/scripts/load-images.sh` moved from "needs modification" to **accept (awaiting maintainer confirmation)**; `grafana-dashboards/overview.json`, `sip-signaling.json`, `scripts/images.txt` remain **accept** (unchanged this round; the item "the digest precedent will be usable after the script is fixed" in the `images.txt` notes has been resolved by the fix at `bundle-images.sh:205`).

### 7.2 Document-by-Document Re-review (corresponding to each item in §6.2)

| # | File | Closure Status of the Needs-Modification Items (corresponding to item N of §6.2) | Re-review Conclusion |
|---|---|---|---|
| 1 | `one-pager.md` | ① `:7` target scenario → the official G8-1 position (xxCarrier internal production readiness / release review); ② `:5` naming → G8-2 descriptive name formally adopted; ③ `:6` repo name → G8-3 records it as completed; ④ `:168` e2e → 8 items pass stably + REQ-F-1 "automated subset covered / full text still open"; ⑤⑥⑦ `:170-172` O4 / D5 / O5 → the adjudicated G6 / G7 positions (the "N+M racks or AZ" enumeration was removed). O1 remains unadjudicated and unchanged | accept |
| 2 | `compliance-matrix.md` | ① `:5` naming → G8; ② the four REQ-F-1 statements at `:79` / `:117` / `:234` / `:266` → "automated subset covered / full text still open" (not written as fully signed off); ③ `:263` e2e → 8 items | accept |
| 3 | `ne-datasheet.md` | Naming + the terminology discipline split at `:11` / `:382` (O1 still unadjudicated / O4·D5 adjudicated per G6 / O5·D3 adjudicated per G7); `:26` / `:367` e2e; `:40` / `:234` / `:270-271` / `:274` / `:297` / `:302` / `:356-359` O4/D5/O5/D3 → G6/G7 (the N+M enumeration was removed at `:302`); `:314` / `:340` / `:327` version and kubeVersion → G4/A6 (script ready, first `--apply` pending the maintainer, `>=1.23.0-0` not written). **The capacity discipline still has zero values (compliant)** | accept |
| 4 | `responsibility-matrix.md` | Naming + `:11` / `:198` e2e; `:27` / `:47` (mermaid label) O4; `:167` / `:192-194` O5/D3 (the N+M enumeration was removed at `:194` and the contradiction with `:168` ADR-0008 has been eliminated); `:213` status discipline synced. Product positioning consistency remains compliant | accept |
| 5 | `security-privacy.md` | The `:5` body-text naming rewritten (the `:6` G8 note is kept as an audit chain); `:10` / `:259` / `:260` / `:264` O4/D5/O5 → G6/G7 main cells updated; the `:289` status-discipline line synced. The fact that the "chart has no backup Job" has not changed (compliant); there is no completion-tense statement of the form "the system cleans up after 10 days" (compliant) | accept |
| 6 | `version-lifecycle.md` | `:5` / `:6` / `:231` naming; `:118` "version bump has no automation" → `scripts/sync-chart-version.sh` has landed (read-only by default with `--check`, exit 1 on drift; `--apply` not executed, G4 remains in effect); `:79` / `:241` "suggested fix" → automatic sync adjudicated + script ready + first execution timing pending the maintainer. §7's wording and Lane D 4.3, and §3 being a pure restatement of ADR-0027, remain compliant | accept |
| 7 | `operations/README.md` | The `:25` undecided-item enumeration synced (O1 still unadjudicated / O4·O5·D3·D5 adjudicated); `:80` e2e; the §1 layering table gained a "cross-layer reference (layer above L1 / L2)" row (the `alert-response-matrix:6` broken link is fixed); `:86` naming discipline | accept |
| 8 | `runbook-l1.md` | The `:29` wrong citation is fixed (the source of 7.2d was changed to the deliverable 2.4 row of §3.2 of `product-packaging-plan.md` and no longer points at items 1 and 3 of §0.3); `:47` / `:194` O5/D3; `:7` e2e. The correspondence of the 10 alerts remains compliant | accept |
| 9 | `runbook-l2.md` | `:21` O4/D5; `:98` / `:180` O5/D3 ("the split-brain window idempotency contract is still not implemented" is retained); `:5` e2e. Unimplemented capabilities are still not written as executable steps (compliant) | accept |
| 10 | `alert-response-matrix.md` | `:68` "check Sentinel / failover status" was changed into two steps "first confirm the deployment form (the single-replica chart has no Sentinel to check) → for the customer's external Redis, check with the customer's tooling"; `:192` and the `:68` evidence column O5/D3; 4 instances of e2e (`:10` / `:14` / `:109` / `:189`); the result of `promtool check rules` passing on 2026-10-11 has been recorded (triple + "syntax pass ≠ scrape wiring closed"); `:6` aligned with the new row of README §1. The rule-by-rule correspondence of the 3 groups and 10 rules remains compliant | accept |
| 11 | `fault-demarcation.md` | `:38` item ⑤, `:117`, `:298` / `:299` O4/D5/O5/D3; `:15` e2e. The boundary wording is still consistent with responsibility-matrix (compliant) | accept |
| 12 | `rollback-playbook.md` | L3 has gained the "version mapping precondition" (revision ↔ chart `version` / `appVersion` ↔ root `VERSION`, all three in the evidence chain) + it faithfully annotates that they are currently not synchronized / `--check` / the first `--apply` pending the maintainer / `kubeVersion` set but not written; the "version from → to" row of the §5 drill record template now requires the version mapping to be filled in; `:126` / `:162` O5/D3. No claim of a drill having been performed (compliant) | accept (with a note: the actual chart synchronization is pending the maintainer, see §7.4-1) |
| 13 | `backup-restore.md` | The `:166` note has been moved out of the §7 table (the column-mismatch rendering incident is fixed and the table is back to a continuous four columns); the main cells at `:27` / `:150` / `:162` / `:163` / `:164` were updated to the adjudicated positions, and the contradiction between `:164` "can only write pending adjudication" and the note is eliminated. RPO/RTO still given no values and D5 not implemented are faithful (compliant) | accept (with a note: RPO/RTO pending the customer + maintainer, see §7.4-2) |
| 14 | `delivery/README.md` | §5 row 4 / L82 "manually verify VERSION/Chart" → `scripts/sync-chart-version.sh --check` (read-only, exit 1 on drift; `--apply` left to the maintainer); the §2 directory table gained the `deploy/alerts/` alert-rule row (the four G9-a delivery products are now complete); the §3 dependent-service row O5/D3; §5 row 7 e2e; naming. The navigation has no dead links (compliant) | accept |
| 15 | `install-guide.md` | The §2 delivery manifest gained an alert-rule row; the package name at `:39` made faithful (current artifact `3rdparty-as-0.0.0-skeleton.tgz`); §5 gained the two synonymous fail texts of `deployment.yaml` + the note that `sip.allowEmptyAllowlistForTest` must be false in production; `:148` "already green" gained the (conclusion, evidence file, date) triple; `:195` manual verification stale; `:18` / `:200` / `:201` O5/D3/e2e | accept |
| 16 | `airgap-package.md` | The digest syntax taught by §5 / §6 contradicted the script → `bundle-images.sh:205` has been fixed and `--dry-run` empirically accepts it (the body text was not rewritten, the evidence is in §7.3 item 5); artifact naming made faithful (the tgz is named after Chart.yaml; without `--platform` the tar suffix is `unspecified`); the outdated L191 "when not yet written to disk" parenthetical was deleted; §2 gained an alert-rule row; §7 rows 1 / 8 version and O5/D3. The correspondence with the bundle/load script steps remains compliant | accept |

### 7.3 Re-review of the Cross-File Common Issues (corresponding to the 5 items in §6.3)

| # | Common Issue (§6.3) | Re-review Result |
|---|---|---|
| 1 | The "task E" sync coverage gap (the other 14 documents still write O4/O5/D3/D5 undecided) | **Closed**: the "undecided" wording of the 14 documents + the dashboard README has been synced to the adjudicated positions per G6 / G7 (retaining the "implementation has not landed / RPO-RTO unadjudicated" qualifiers); the existing additive notes in security-privacy and backup-restore are kept as an audit chain |
| 2 | The e2e basis is outdated (9+ instances of "e2e marker = 0" across the batch) | **Closed**: the root cause `docs/acceptance/test-plan.md` automation layering table row ③ is fixed (0 items → 8 items passing stably + the REQ-F-1 position), and all e2e statements of the 16 documents + the dashboard README have been back-filled |
| 3 | Chart version consistency is missing | **Partially closed**: the document side has all been synced to "G4/A6 adjudicated + script ready + the first `--apply` pending the maintainer"; rollback-playbook L3 has gained the revision → chart version → product VERSION mapping; the artifact naming of install-guide / airgap has been made faithful. **Not closed**: the actual Chart.yaml synchronization and the kubeVersion writing (see §7.4-1) |
| 4 | The delivery manifest lacks the alert rules (only three of the four G9-a categories landed) | **Closed**: all three delivery documents have added `deploy/alerts/` (3 groups and 10 rules + the triple for the promtool pass of 2026-10-11 + a note that the X1 scrape wiring being unclosed must be explained to the customer) |
| 5 | Functional defects in the incidental assets | **Closed**: the digest validation glob at `bundle-images.sh:205` is fixed (and non-sha256 rejection plus `--destination` documentation were added); the `load-images.sh` `--values` wording was made faithful (no parsing, no inference); the external Redis/Sentinel false report in `preflight.sh` is fixed (Sentinel configured → PASS), and the bad byte at `:34` is fixed; the three scripts uniformly declare the bash ≥ 4.4 floor |

### 7.4 Items Still Unclosed in the Re-review (these do not constitute document defects; the dependencies are stated)

| # | Unclosed Item | Dependency |
|---|---|---|
| 1 | The first `scripts/sync-chart-version.sh --apply` (aligning the Chart.yaml `version` / `appVersion` with `VERSION`) and the writing of `kubeVersion: ">=1.23.0-0"` | The maintainer decides the timing and the values (G4 "currently no modification of `VERSION` and `Chart.yaml`" remains in effect) |
| 2 | RPO / RTO values | Recorded jointly by the customer and the maintainer (backup-restore.md is left blank per the discipline) |
| 3 | O1 capacity values | Maintainer adjudication (the capacity chapters of each document are left blank per the discipline) |
| 4 | X1 alert scrape wiring | Carrier monitoring-integration standard input + maintainer adjudication (G3 remains pending, the chart is not changed currently) |
| 5 | 7.2d / real-cluster drill and the M8 exit sign-off | External environment (the adjudication deferring external IOT and real-environment evidence collection remains in effect) |
| 6 | The **implementation** of trace storage / query / deletion and Redis Sentinel | B2 / B3 already have separate items left open (`docs/handoff/2026-10-12-b2-b3-deferred-items.md`); not started this round |

### 7.5 The Change Surface of This Round and Its Boundaries

- **21 files changed in total**: `docs/acceptance/test-plan.md` (the root cause of the e2e basis) + 6 documents in `docs/product/` + 8 documents in `docs/operations/` (7 + the dashboard README) + 6 files in `docs/delivery/` (3 documents + 3 scripts).
- **Unchanged**: `deploy/` (including `Chart.yaml` / `as-alerts.yaml`), the root `VERSION`, any product code or tests, `docs/plan.md` and the existing handoff / reviews text, the two dashboard JSONs and `scripts/images.txt`.
- **Not executed**: any git write operation; `sync-chart-version.sh --apply`; any build / test / container action. All changes stay in the working tree, and the commit split is decided by the maintainer.
- The re-review conclusions **await maintainer confirmation**; before confirmation, §7 of this checklist does not constitute a basis for external delivery or acceptance.

**(§7 of this document signs off no REQ / milestone and does not constitute a basis for external delivery or acceptance.)**
