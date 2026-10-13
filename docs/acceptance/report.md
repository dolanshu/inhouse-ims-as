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

# Acceptance Report — 3rdparty-as · M8 Release Candidate (2026-10-06)

> Status: **M8 release candidate (RC ready, awaiting maintainer exit sign-off)** — no claim of being all-green, not a closure conclusion, contains no maintainer signature.
> Date: 2026-10-06
> Executed by: AI agent (user-instructed self-decision while the maintainer was absent; all signatures in this chapter are **awaiting the maintainer's signature**)
> Basis: [`2026-10-06-m8-release-candidate-plan.md`](../handoff/2026-10-06-m8-release-candidate-plan.md) (RC plan §3 exit conditions / §4 phases A–E / §5 open-item handling), [`plan.md`](../plan.md) §4 (M8 definition) / §5 (O/D open items)
>
> **2026-10-13 addendum (M8 batch 6 / E-1) — the nature of this version**: this version is an **internal build (image tag `as-platform:0.2.0-internal-<date>`)**,
> **not the M8 exit sign-off**. Artifacts = complete functionality + simulator evidence + a reproducibly built release artifact bundle;
> the signing position for all 27 matrix rows marked `pass` is uniformly "**engineering evidence accepted**", which **does not mean REQ-level acceptance passed and does not mean milestone sign-off**.
> See [`../reviews/m8-internal-release-exit-review-2026-10-12.md`](../reviews/m8-internal-release-exit-review-2026-10-12.md) for the internal-version wrap-up review;
> **the M8 milestone is still unsigned** (signature table in [`../reviews/m8-exit-review-2026-10-06.md`](../reviews/m8-exit-review-2026-10-06.md) §3.2).
>
> **2026-10-13 further addendum (path C)**: the maintainer has made the **M8 exit sign-off** under **path C** (including written acceptance of the external hard dependency risk). The sentence above saying "not the M8 exit sign-off" is **retained as history**; **the current status is governed by §0.11**; see the signature block in [`../reviews/m8-exit-review-2026-10-06.md`](../reviews/m8-exit-review-2026-10-06.md) §3.3 and the precondition document [`../reviews/m8-external-dependency-risk-acceptance-2026-10-13.md`](../reviews/m8-external-dependency-risk-acceptance-2026-10-13.md).

## 0. M8 release candidate (2026-10-06)

### 0.1 Scope: what M8 is / is not (RC plan §1)

| M8 is | M8 is not |
|---|---|
| A REQ / test-plan sign-off run backed by evidence (matrix in [`m8-test-plan-matrix.md`](m8-test-plan-matrix.md)) | A new-feature milestone (the PRD scope is not expanded by default) |
| The closing of maintainer milestone exits (M1/M2/M6/M7) together with M8's own sign-off | Redoing the M2–M7 engineering closures (already done, see `plan.md` §4) |
| This report being promoted to the main M8 release candidate report (the historical body is retained as an appendix, not rewritten) | Publishing an external SLA / commercial O1 figure (still bound by AGENT.md §2 and plan §5.1 O1) |
| VERSION / CHANGELOG unifying the product version (F15; this RC: VERSION stays `0.2.0`, not bumped) | A full pre-M8 customer demo (story C is still bound by F10, the L1 position) |
| Converging the M5 REQ-level evidence position (engineering closure ≠ REQ acceptance, see §0.4) | Overturning the 2026-10-04 M5 engineering closure (maintained, with its meaning downgraded; see §0.4) |

Definition of done (`plan.md` §4): item-by-item acceptance report + complete document chain + unified product version — of which "item-by-item acceptance" is judged by the final state of the sign-off matrix plus the maintainer's signature; this RC has only reached "RC ready", not "closed".

### 0.2 Entry baseline

- Baseline commit: `master` @ `8d1c5cd` (2026-10-06; includes the callload merge `139d299`; there are also Phase A working-tree changes awaiting maintainer review, see `git status`).
- `make gate`: **978 passed, 2 skipped** (exit 0; both skips are Route/Record-Route probe gaps in `test_derived_baseline.py`, see matrix row F-5).
- The callload M2/M6/M7 engineering slices have been merged into `master` ([`handoff/2026-10-06-callload-merge-to-master.md`](../handoff/2026-10-06-callload-merge-to-master.md)); merging does not automatically close the M2/M6/M7 maintainer sign-offs.

### 0.3 Phase A summary: gate and evidence infrastructure

- **F8 (A-2)**: the field contract has landed — `resip_runtime_log_contract.py` + 13 contract tests + [`m8-resip-runtime-log-contract.md`](m8-resip-runtime-log-contract.md) + `emit_native_log_event` JSON enrichment; the C++→Python JSON callback is deferred to post-RC (one of the two paths the plan allows). REQ-NF-13 assertions hang off this contract. See [`m8-phase-a-f6-f8-note-2026-10-06.md`](../reviews/m8-phase-a-f6-f8-note-2026-10-06.md) for details.
- **F6 (A-3)**: documented limitation — the registration cap and the dialog-termination deregistration have been verified to exist; the absence of a native transport-close callback is the current design state (reSIProcate's Transport close hook is not wired up, out of RC scope); connections are reclaimed through dialog termination + fingerprint LRU eviction as a fallback; risk acceptance awaits a maintainer ruling.
- **A-4 / A-5 / A-6**: the relationship between `make gate` and gate layering has been documented (CONTRIBUTING); `gate-strict` (the REQ-G-3 ADR-annotation scan, `check_adr_annotations.py`, 69 files clean) is a blocking item; the `performance` layer blocks from M6's first case onwards; the e2e layer still does not block (0 tests).
- **A-7**: the native-consistency runbook required before sign-off is in place: [`m8-native-consistency-runbook.md`](m8-native-consistency-runbook.md) (`make m2-platform-resip-build` plus the M7 recovery/two-leg targets before the sign-off run).

### 0.4 Phase B summary: the M5 REQ chain position

Re-review record: [`m5-req-acceptance-review-2026-10-06.md`](../reviews/m5-req-acceptance-review-2026-10-06.md) (conclusion: conditional pass at the engineering-slice level / fail at the REQ level, 10 items deferred; the maintainer countersignature is pending).

- **B-1**: only MINIMAL M5.1 is executed (Helm H-1…H-4 fail-closed patches + the chart-check onprem matrix + kind K-1/K-2 fail-closed hardening + the HLD/LLD M5 delta + ADR-0008/0013 amendments + REQ chain annotations); the full alert/metric wiring, the OTLP exporter, the scale-down guard participation control, NetworkPolicy egress, and resources/probes are all deferred to after the RC.
- **B-2**: the 2026-10-04 M5 engineering-closure signature is maintained (not revoked, history not rewritten), with its meaning explicitly downgraded to **engineering closure (not REQ acceptance)**.
- **B-3**: story C stays at **L1 (F10)**: only show the chart/alerts shape + a kind summary; it must not be described as the whole chain being accepted or as production alerting/scale-down being closed out.
- Defer composition items (10 items; the proposed new plan §5 rows M5D-1…M5D-6 are for the maintainer to finalise): C-1/C-2/C-3/C-6/C-7/C-9, H-8, H-11, A-2, T-1 (details in the re-review §6).

### 0.5 Phase C summary: test-plan sign-off matrix (no claim of being all-green)

Matrix: [`m8-test-plan-matrix.md`](m8-test-plan-matrix.md) (tracing back `test-plan.md` §1–§5; `signed_by` on all rows is awaiting the maintainer's signature).

**Actual counts (the matrix is authoritative)**: pass **9** (NF-6, NF-8, NF-11, NF-12, G-1, G-2, G-3, G-4, KERNEL-§5; of which G-1/G-2/G-3 are pass-as-mechanism — per-change review still needs the maintainer) / fail **0** / blocked **12** / n-a **4** / open **24**.

**This RC explicitly does not claim being all-green**: none of the 24 open or 12 blocked items is claimed as green; the 4 n-a items are explicit exclusions (caller/regex v1.1, PM/AM/UM, D1 Python 3.10 EOL, D10 extreme extensions), never recorded as pass.

Explicit v1 exclusions (RC plan §3.1 / plan §5.3–§5.4): the complete PM/AM/UM product; REQ-F-13 live trace (M4b-7.4); caller / regex (v1.1); D1; Redis failover owner/CAS extreme scenarios and mid-transaction recovery (D10 not extended); NF-3 items carrying fixed capacity figures (conflicts with AGENT.md §2; awaiting a maintainer ruling either to rewrite the acceptance position or to mark them N/A; plan §5.1 O1 is still open).

### 0.6 Phase D summary: environment evidence

Record: [`m8-environment-evidence.md`](m8-environment-evidence.md); evidence root directory `acceptance/artifacts/m8/<date>/` (`req-s-2-pki/`, `req-s-3-rotation/`, `req-nf-1-live/`, all of which are placeholders awaiting collection; see that file's §0 for the redaction convention).

- **D-1** (operator PKI / external-network S-SBC, the REQ-S-2/S-3 tail): this environment has no lab and no peer, so no evidence can be collected — **explicitly deferred**; S-2/S-3 stay blocked in the matrix.
- **D-2** (customer K8s REQ-NF-1 live kill/restart/BYE): this environment has no customer cluster — **explicitly deferred**; NF-1 stays blocked in the matrix.
- **D-3** (whether the D6 testbed is part of v1 customer acceptance): **maintainer ruling pending**; this RC recommends v1.1 (architecture baseline; unless the customer explicitly asks for v1) and recommends that it have no effect; the D6 row stays blocked until the ruling.

### 0.7 E-6 packaging verification results

- `tests/test_version_consistency.py`: **9 passed**; VERSION stays `0.2.0`, the first CHANGELOG heading is `== 0.2.0` (no new version section, no bump).
- Secret/packet-capture re-check: zero hits for `BEGIN PRIVATE KEY` in the new M8 documents, zero hits for `--password` / `passwd`; the `artifacts/m8/` placeholders contain no fabricated evidence.
- Helm reproducible build: `make chart-check` → **chart-check: OK** (shape evidence, not used as a basis for a REQ pass; heavy builds are not re-run inside the RC).
- README/runbook consistency with `AS_SIP_*`/`AS_TLS_*`: the implementation-side variables are defined in `platform/src/as_platform/runtime/transport_env.py` (`AS_SIP_BIND_ADDRESS` / `AS_SIP_ADVERTISED_ADDRESS` / `AS_TLS_*` / `AS_PEER_*`); the README lists no env names (there is no wrong name and no typo to fix), and the runbook only references `AS_REQUIRE_NATIVE_EXTENSIONS=1` (consistent with `native_extensions.py`) — recorded as a **documentation gap (non-blocking)**: the README lacks an env-variable table; it is recommended that the maintainer add a line linking to the runbook / `transport_env.py`; no spelling errors requiring a fix were found.
- Image push/tag: **explicitly left to the maintainer** (AGENT.md §10.4); not executed in this RC.

### 0.8 Merged list of defer / blocked (each item must reach a final state before signing)

| # | Item | Status | Points to |
|---|---|---|---|
| 1 | 12 blocked in the matrix (F-13, 5.4-F-13, F-15, 5.4-F-15 real AS, NF-1, NF-3, NF-4, NF-7, S-2, S-3, ADR-0008 drill, D6) | blocked | matrix |
| 2 | 24 open in the matrix (F-1/2/3/4/5/6/7/8/9/10/11/12/14/16, NF-2/5/9/10/13/14/15, S-1/S-4, D12/O5-HA) | open (awaiting sign-off at the M8 exit review) | matrix |
| 3 | D-1 / D-2 | explicitly deferred (requires maintainer authorisation to enter the overall review) | §0.6 |
| 4 | D-3 (D6) | ruling pending (v1.1 recommended) | §0.6 |
| 5 | 10 M5D items (C-1, C-2, C-3, C-6, C-7, C-9, H-8, H-11, A-2, T-1) | defer (the composition items of the M5 REQ-level fail) | §0.4 |
| 6 | O1 target ruling / NF-3 position / D1 risk register | open (awaiting a maintainer ruling) | plan §5.1 / §5.2 |

### 0.9 Maintainer to-dos (must be executed by the maintainer before the RC closes)

1. Schedule the operator PKI lab and external-network S-SBC joint debugging (D-1) and the customer K8s live baseline (D-2), producing redacted evidence per env-evidence §0; or accept the risk in writing in the overall review.
2. Give written rulings finalising the D-3 (D6 v1/v1.1), O1 target, NF-3 position and M5D-1…M5D-6 rows.
3. Complete the M1/M2/M6/M7/M8 exit sign-offs (signature table in [`m8-exit-review-2026-10-06.md`](../reviews/m8-exit-review-2026-10-06.md), all awaiting the maintainer's signature); tags are executed only by the maintainer (AGENT.md §10.4).

> Terminology note: "RC ready" in this chapter means the RC artifacts are complete and available for the maintainer's review and signature; "closure" only holds after the maintainer signs. This RC does not reach a "pass" conclusion.
> Historical note: the appendix's original M2a section of this file contains one instance of "all-green" (a 2026-09-28 M2a unit/contract gate snapshot, not an M8 claim); it is retained verbatim for the sake of preserving history; this RC chapter (§0) adds no affirmative all-green statement.

## 0.10 Count synchronisation and internal-version wrap-up statement (M8 batch 6 / E-1, added 2026-10-13)

> This section is written as "retain the original text, append the correction"; the pass 9 / fail 0 / blocked 12 / n-a 4 / open 24 in §0.5's original text is retained as the 2026-10-06 historical values, and **the current counts are governed by this section**.

| Bucket | §0.5 original (2026-10-06) | Current value (matrix section "M8 batch 4 finalised proxy-signing (2026-10-13)") |
|---|---:|---:|
| pass | 9 | **27** |
| fail | 0 | 0 |
| blocked | 12 | **9** |
| n-a | 4 | **9** |
| open | 24 | **0** |
| defer | no such status word at the time | **4** |
| **Total** | **49** | **49** |

The 4 `defer` rows are F-5 / F-8 / F-9 / F-11, meaning they are not accepted in this release and are firmly assigned to v1.1; this is distinct from `blocked` (restriction) and `n-a` (never accepted). See that addendum's third section of the matrix for the definitions and the per-row destination.

The composition of the 27 `pass` rows is: 9 (the 2026-10-06 baseline) + 7 (N3 proxy-signed F-1 / F-2 / F-3 / F-6 / F-7 / F-12 / F-14) + 1 (NF-4 under "accept measured call loss") + 10 (batch 4: F-4 / F-10 / F-16 / NF-2 / NF-5 / NF-9 / NF-10 / NF-15 / S-1 / S-4) = 27. **All are agent proxy-signatures (maintainer-authorised), not the maintainer's own signature**; the position is uniformly "engineering evidence accepted".

**Boundary list**:

1. This section does not claim M8 is all-green and does not claim the M8 exit sign-off.
2. "Engineering evidence accepted" ≠ REQ-level acceptance passed ≠ milestone sign-off.
3. M5 at the REQ level still fails; the internal-version wrap-up does not overturn that conclusion.
4. The 9 `blocked` rows break down as: 5 external-hard-dependency restrictions (NF-1, S-2, S-3, ADR-0008 drill, D12/O5-HA); plus F-15, 5.4-F-15 real AS, NF-13 and NF-14. The condition for reopening an external hard dependency = a separate maintainer ruling + the external resource being in place; deferred ≠ cancelled.
5. An internal version is not a release: VERSION stays `0.2.0`, nothing is tagged, and the chart does not change with the internal build.
6. No git write operation was executed in this batch.

Triple: `(verified, docs/acceptance/m8-test-plan-matrix.md "M8 batch 4 finalised proxy-signing (2026-10-13)" section, 2026-10-13)`.

## 0.11 M8 exit sign-off and risk acceptance (path C, added 2026-10-13)

> This section is written as "retain the original text, append the correction". The header sentence "not the M8 exit sign-off" and §0.10 are both **retained as history**; **the current status is governed by this section**.

1. **M8 exit sign-off status = adjudicated and accepted by the maintainer (the signature block awaits their own signature being filled in)**. The path is **C = sign the M8 exit sign-off + accept the external hard dependency risk in writing**; see the signature block in [`../reviews/m8-exit-review-2026-10-06.md`](../reviews/m8-exit-review-2026-10-06.md) §3.3. **That signature block must not be proxy-signed by an agent**; none of the prior proxy-signing authorisations (N2's nine items, N3, batch 4) included the M8 exit sign-off.
2. **Precondition = written acceptance of four external hard dependency risks**: **D-1** (operator PKI + external-network S-SBC), **D-2** (customer K8s), the **ADR-0008** cross-site switchover drill, and **D12 / O5** production Redis and PostgreSQL HA. These rows **stay `blocked`** and move to the next release; the condition for restarting them = **a separate maintainer ruling + the external resource being in place**; **deferred ≠ cancelled**. Precondition document [`../reviews/m8-external-dependency-risk-acceptance-2026-10-13.md`](../reviews/m8-external-dependency-risk-acceptance-2026-10-13.md).
3. **The 4 `defer` rows (F-5 / F-8 / F-9 / F-11) and the F-13 / NF-7 call trace are moved to v1.1 as projects**; at kick-off they all follow requirement → ADR → design → review; **this version neither starts them nor implements them**.
4. **Boundaries**:
   1. **The signature covers milestone exit, not REQ-level acceptance** — **M5 at the REQ level still fails**, and this section does not rewrite that conclusion.
   2. **Accepting risk ≠ verification passed ≠ these rows moving to a final state**; the four external hard dependencies remain `blocked`.
   3. **M8 is not claimed to be all-green**, and no claim is made that a release has happened; the internal-version position is unchanged (`VERSION` stays `0.2.0`, not bumped, not tagged, chart not synced).
   4. **No external capacity or SLA commitment is produced**; the O1 externally committed value is still left unfilled, and the internal engineering target (loopback CPS 1280) is internal only.
   5. **The matrix counts are unchanged**: pass 27 / defer 4 / blocked 9 / n-a 9 / open 0 / fail 0 (49 total), with the position still "engineering evidence accepted". This section did not change a single line of `m8-test-plan-matrix.md`.
   6. This section executed no git write operation (no add / commit / tag / push / branch / stash); tags are executed only by the maintainer (`AGENT.md` §10.4).
5. Triple: `(adjudicated-pending-own-signature, docs/reviews/m8-external-dependency-risk-acceptance-2026-10-13.md, 2026-10-13)`. Execution environment `dev-win03ib7niepf0`.

> **2026-10-13 proxy-signature correction**: both the M8 exit signature block and the risk-acceptance adjudicator field have been filled in as **agent proxy-signatures (maintainer-authorised on 2026-10-13)** per the maintainer's "**authorise proxy-signing**" instruction of that day, and are **not the maintainer's own signature**; **the M8 milestone is closed accordingly**. The triple above is corrected from "adjudicated-pending-own-signature" to **`(proxy-signed-not-own-signature, docs/reviews/m8-external-dependency-risk-acceptance-2026-10-13.md, 2026-10-13)`**. The remaining boundaries in this section (not covering REQ-level acceptance, not claiming all-green, not producing external capacity / SLA commitments, matrix counts unchanged) **remain in force**.

## Appendix: historical M1 report

## Acceptance Report — 3rdparty-as

> Milestone: **M1 — triage and behavioural baseline**
> Date: 2026-09-28
> Executed by: AI agent (on behalf); the M4b engineering slice + the M4b-8 maintainer signature have been recorded (2026-10-04, chat-authorised proxy-signature); the M1 §6 signature at the head of this document is still a historical item
> Gate basis: `docs/plan.md` §4.1; DoD basis: `AGENT.md` §14

## 1. Conclusion

**The M1 gate was achieved.** M1's output is documentation and a behavioural baseline, with **no product code**, so the code-related DoD items are marked N/A with the reason explained.

## 2. M1 gate check

| Gate item | Status | Evidence |
|---|---|---|
| Every file has an evidence-backed ruling | achieved | searching `docs/migration/triage.md` finds no "undecided / pending ruling / TBD / pending" residue; `b27bb3d` |
| POC commit frozen; message samples and traces captured | achieved (partially) | the per-scenario READMEs in `testbed/contracts/sip-baseline/` record the capture script and date; `92c244c` |
| The baseline is captured and reproducible | achieved (with rulings) | S1 / S2 / S3 / S4 have message files (14 / 4 / 4 / 12 messages); S5-S8 were ruled to be derived baselines and S10 / S11 ruled to be completed by the M2 probe; see `plan.md` §4.1 for details |

> Count correction: S4-caller-cancel actually has **12** message files (`01-in-invite-trunk.txt` … `12-out-ack-core.txt`, and its README also says "message sequence (12 messages)"), not 9. This report takes the actual repository contents as authoritative.

## 3. DoD item-by-item evidence collection (AGENT.md §14)

| # | DoD item | Status | Evidence / N/A reason |
|---|---|---|---|
| 1 | Runs end-to-end against the simulated peer | N/A | M1 has no product code; end-to-end is an M2/M3 acceptance item. M1 only captures the behavioural baseline on the POC side (S1-S4) |
| 2 | Tests added on the layer the change belongs to; `make gate` green | achieved | actually running `make gate` locally (2026-09-28): ruff format `70 files already formatted`; ruff check `All checks passed!`; mypy `Success: no issues found in 7 source files`; pytest `-m "unit or contract"` `44 passed`. The existing 44 tests are the M0 structural guards and library-independence guards; M1 added no product code, so there are no new tests |
| 3 | `ruff format`, `ruff check`, `mypy` clean | achieved | same as above (the same single real run) |
| 4 | The change carried an ADR; when the decision moved, the architecture document was updated | achieved | ADR-0019 (SIP stack selection) Accepted, with its E1 probe verification landing in M1 via `e30c426`; `2341166` completed the requirement→ADR bidirectional references; `b13567a` marked ADR-0001/0002/0003/0018 as accepted |
| 5 | README and affected documents updated | achieved | `docs/plan.md` was updated in this pass (M1 complete, current step M2, new §4.1 gate ruling); the `docs/requirements/README.md` index points at the PRD and acceptance; the PRD has reached v0.2 |
| 6 | There is a CHANGELOG entry; if the delivered content changed, the product version number has been bumped | entry pending / version maintained | the CHANGELOG entry is written in this same synchronisation; `VERSION` stays `0.1.0` — M1 delivers no product code and the delivered content is unchanged, so per ADR-0018 it is not bumped |
| 7 | If POC code was adopted: the corresponding triage row has been cited | N/A | M1 adopted no POC code; POC behaviour serves only as a baseline (`testbed/contracts/`) and does not enter product dependencies (AGENT.md §12) |
| 8 | No secrets were committed | achieved | no credentials, certificates or real packet captures were added at this milestone |
| 9 | Document chain complete: requirement → ADR → HLD/LLD → contract/message samples → acceptance items → review record | partial (HLD/LLD missing) | requirement (PRD v0.2) → ADR-0019 → contract/message samples (S1-S4) → acceptance items (test-plan) → review record (`prd-v0.1-review.md`) is connected end to end; **HLD/LLD do not yet exist**, and are a prerequisite for M2 |
| 10 | If a feature switch was introduced: two-state tests plus acceptance evidence, and a removal condition | N/A | M1 introduced no feature switch (the ADR-0020 mechanism awaits the M2 kernel) |

## 4. Evidence inventory

| Artifact | Location / commit |
|---|---|
| POC file rulings | `docs/migration/triage.md` (`b27bb3d`) |
| Behavioural baseline | `testbed/contracts/sip-baseline/` (`92c244c`) |
| SIP stack selection probe | reSIProcate E1 probe (`e30c426`), corresponding to ADR-0019 |
| requirement→ADR bidirectional references | the "responds to REQ" field in each ADR's header (`2341166`) |
| Requirement standard | `docs/requirements/prd.md` v0.2 (`c9d4899`) |
| Acceptance items | `docs/acceptance/test-plan.md` (`1cb387c`, moved into acceptance) |
| Review records | `docs/reviews/prd-v0.1-review.md`, `docs/reviews/adr-0019-review.md`, `docs/reviews/adr-m1-draft-review.md` |

## 5. Items handed over to M2

| # | Item | Destination |
|---|---|---|
| 1 | Create HLD / LLD (`docs/architecture/hld.md`, `lld.md`), including feature enablement design | M2's first action (AGENT.md §3.1 requires HLD/LLD as a prerequisite for entering Code) |
| 2 | Complete the S10 / S11 comparison scenarios (REQ-F-10 non-2xx branches, REQ-F-11 CANCEL race) | M2 probe phase, added under `testbed/` |
| 3 | If S5 / S6 / S7a / S8 are later changed to real captures, an overturn record must be appended to `plan.md` §4.1 | Silent substitution is not permitted |
| 4 | OTel three signals and the data-plane split (ADR-0005 / 0007) are still skeleton and have not landed | Needed by the M2 kernel; an ADR must be written first |
| 5 | The maintainer signature on this report | Pending |

## 6. Signatures

| Item | Value |
|---|---|
| Milestone conclusion | The M1 gate was achieved |
| Items not achieved | See §3 item 9 (HLD/LLD missing), already listed as an M2 prerequisite in §5 |
| Executed by | AI agent, 2026-09-28 |
| Maintainer signature | To be filled in |

---

## M2a acceptance (2026-09-28)

| Item | Result | Evidence |
|---|---|---|
| `make gate` | all-green | ruff format 95 files / ruff check passed / mypy 19 files clean / pytest **114 passed** (0 skipped) |
| Structural guards | pass | 56 passed; no reverse imports in the kernel |
| unit layer | pass | `decide()` decision matrix 7 cases, rule matching, both gating states, telemetry not blocking, process-shell draining |
| contract layer | pass | the StateStore contract replayed against both `InMemoryStateStore` and `RedisStateStore` (9 cases each) |
| Dependencies | wired up | `redis>=5.0` (locked at 8.1.0) written into `platform/pyproject.toml` and `uv.lock` |
| Document chain | connected | REQ-F/NF/S → ADR-0005/0007/0016 (accepted) → HLD/LLD (reviewed) → contracts (test-plan §5) → code → review records (`m2-design-review.md`, `m2a-kernel-review.md`) |

**Not covered**: TLS transport / SIP adapter (M2b), `CallState` (M3), integration / e2e layer cases (M2b / M3).

---

## M2b boundary seam (2026-09-28)

| Item | Result |
|---|---|
| Gate | ruff 105 files formatted / ruff check passed / mypy 23 files clean / pytest **145 passed** (2 skipped) |
| Deliverables | `platform/src/as_platform/sip/`: peer allowlist (fail-closed), TLS configuration hot rotation (immutable reload), SIP adapter Protocol, decision→status code mapping |
| Tests | `test_transport_seam.py` 9 cases, `test_sip_adapter_seam.py` 9 cases (marker `unit`) |
| Review | `docs/reviews/m2b-seam-review.md` (pass) |

**Not covered**: the stack-binding implementation of the SIP adapter, real certificate loading and handshake, integration / e2e layer cases (all listed for the second half of M2b).

---

## M3 decision modules (2026-09-28)

| Item | Result |
|---|---|
| Gate | ruff 111 files formatted / ruff check passed / mypy 25 files clean / pytest **169 passed** (2 skipped) |
| Deliverables | the decision modules of `apps/translation` and `apps/anti-fraud`, both built on top of the kernel's `decide()` |
| Tests | translation 10 cases, anti-fraud 14 cases (marker `unit`), TDD red→green |
| Review | `docs/reviews/m3-decision-modules-review.md` (pass) |

**Not covered**: the wiring of the counter and the StateStore (depends on undecided D3), replay of the contract case set against both use cases, and the `integration` / `e2e` layers.

---

## M3 contract replay and gate (2026-09-28)

| Item | Result |
|---|---|
| Gate | ruff 116 files formatted / ruff check passed / mypy 25 files clean / `unit or contract` **190 passed** (2 skipped) |
| contract layer | 49 passed (of which 21 are the contract replays added this time) |
| integration layer | 3 passed (the first integration cases, verifying over real sockets that telemetry export does not block the call path) |
| Contract case set | `testbed/contracts/decision/cases.json` 14 cases, replayed against each of `apps/translation` and `apps/anti-fraud` |
| Review | `docs/reviews/m3-gate-review.md` (pass, M3 judged complete) |

**Gate**: layer ② integration has been changed to blocking (AGENT.md §9); layer ③ e2e and layer ④ performance still have no cases and do not block.

---

## M4 configuration governance kernel (2026-09-28)

| Item | Result |
|---|---|
| Gate | ruff 127 files formatted / ruff check passed / mypy 28 files clean / `unit or contract` **254 passed** (2 skipped); integration 3 passed |
| Deliverables | the change-record state machine (7 states, approval audit trail), the immutable version store, batched canary with automatic rollback, and switches entering `ConfigBundle` on the same release chain |
| Tests | 8 state machine, 6 version store, 10 distribution, 7 switch contract, 7 switch release chain cases (marker `unit`), TDD red→green |
| Review | `docs/reviews/m4-config-kernel-review.md` (pass, staged) |

**Not covered**: the PostgreSQL version of `VersionStore`, `services/console` (REQ-S-4), and a real-database end-to-end loop.

---

## M4a configuration governance and access policy evidence (2026-09-28; backend / policy scope only)

| Item | Result |
|---|---|
| Gate | ruff 134 files formatted / ruff check passed / mypy 30 files clean / `unit or contract` **309 passed** (2 skipped); integration 3 passed |
| Deliverables | `services/console/src/as_console/access.py` pure access policy and audit decisions (role/permission matrix, two-person principle, recording rejections too; no HTTP, login, session, password, persistence or UI); ADR-0021 adjudicates D7 and implements runtime override (number range + stable-hash percentage, idempotent decisions) |
| Tests | console 43 cases (access policy), runtime override 11 cases (marker `unit`), TDD red→green |
| Review | `docs/reviews/m4-console-access-review.md` (pass; M4 judged complete) |

**Historical M4a scope ruling (2026-09-28)**: the review at the time judged the backend governance / access policy scope complete; that conclusion does not include the operator UI and does not mean M4 as a whole is complete. The PostgreSQL version of `VersionStore` moves to M5; **M5 must add real-database integration cases and pass end to end**, otherwise M5 may not be judged complete.

### Scope correction (2026-10-01)

The gate and test evidence retained in this section covers only the configuration governance backend, D7 and the pure access policy code; the original review did not examine or accept the frontend. The overall M4-complete conclusion of 2026-09-28 did not include the operator UI, and is now superseded by the user's decision of 2026-10-01: M4 as a whole remains pending until the mandatory M4b UI passes acceptance per REQ-F-12/13/14/15 and REQ-S-4 in [`test-plan.md`](test-plan.md) §1.4, §3. No claim of an existing UI or UI acceptance is made here.

### M4b-1 static console preview (2026-10-01; engineering evidence, NOT M4/M4b ACCEPTANCE)

This section records only the M4b-1 engineering preview; it does not constitute UI acceptance; **M4 remains open**. D4 has been adjudicated to use plain HTML/CSS/JavaScript, with no bundler, build tool or frontend runtime dependency. The preview files are [`index.html`](../../services/console/web/index.html), [`console.css`](../../services/console/web/console.css) and [`console.js`](../../services/console/web/console.js), providing four views: Rules, Change orders, Call traces and Operations; the page is marked `PREVIEW · LOCAL DATA · NOT CONNECTED`, and the data lives only in the current page's memory.

- **Browser interaction**: the browser sandbox refuses untrusted `file://`, so it is opened via the `http://127.0.0.1:8765/` loopback; this is a browser environment limitation, not an application error. Rule creation, editing, enable/disable and deletion are all only queued as local change records. An empty or whitespace-only name shows `Enter a rule name.`; an empty or whitespace-only match value shows `Enter a match value.`; an empty or whitespace-only target shows `Enter target detail.`; an invalid regex shows `Enter a valid regular expression.`. Invalid input does not add to the queue, and a valid regex does get queued. When the rejection reason is empty the rejection is blocked; once filled in the status becomes `Rejected` and the reason is visible. The preview states explicitly that approval only affects the local preview and does not connect to the routing backend.
- **Two-leg call trace**: the fixture has 14 chronologically ordered messages, including the Call-IDs of two independent legs, both legs' INVITE and 100/180/200 responses, both legs' ACK, the inbound BYE, the outbound BYE, the downstream 200 and the upstream 200. Searching with either leg's Call-ID returns the same trace; each message row shows the Call-ID of the leg it belongs to.
- **Responsive and keyboard checks**: at a 390px viewport all four view roots and the body are 375px. Rules keeps Match criteria and hides only version/updated; Change orders hides only requested-by/submitted metadata; Call traces' detail table keeps all seven fields and scrolls internally, and the page root does not overflow. At a 1440px viewport no root exceeds 1440px, and Call traces is 1425px. After selecting a trace with Enter the focus returns to the selected Call-ID; after filtering the selected trace away the focus stays in the search box; after approving from Rules or rejecting from Change orders the focus returns to the current page heading. Rejection-reason validation works.
- **Independent review**: every work step of M4b-1 went through an independent read-only review. The review found and the following were fixed: approval wording that misled by suggesting routing would be affected, whitespace-only match values being accepted, Match criteria being hidden on mobile, whitespace-only names/targets not being intercepted, focus being lost after keyboard operation, an incomplete trace fixture that easily confused the per-leg Call-IDs, and an incorrect 100 Trying direction. The final review of the complete trace fixture found nothing; the post-fix focus-only re-check also found nothing. See [`m4b-1-console-ui-review-2026-10-01.md`](../reviews/m4b-1-console-ui-review-2026-10-01.md).
- **Local verification**: the main agent ran `node --check services/console/web/console.js` successfully. The latest local `make gate`: ruff format 190 files formatted, Ruff fully passing, mypy 36 source files clean, pytest **417 passed, 2 known skips, 15 deselected**. Local only.

**Boundary**: there is currently no backend/API, auth/session, persistent audit, database, live telemetry, production routing, persisted trace store or approval-flow wiring. This preview does not replace the acceptance of REQ-F-12/13/14/15 and REQ-S-4, does not mean M4b is complete, and does not change the overall incomplete state of M4.

---

## M5 Helm and alerts (2026-09-28)

> **The ongoing M5 plan and checklist**: see [`plan.md`](../plan.md) **§4.4–§4.5** (from 2026-10-04). The sections below are historical engineering snapshots; the closure conditions are governed by §4.4.

### M5 engineering closure (2026-10-04)

**Maintainer signature**: 2026-10-04 (chat-authorised proxy-signature); see [`reviews/m5-closure-adjudication-2026-10-04.md`](../reviews/m5-closure-adjudication-2026-10-04.md). This is **not** REQ-level acceptance.

| Item | Result |
|---|---|
| Plan | [`plan.md`](../plan.md) §4.5 |
| Evidence | [`m5-engineering-closure-2026-10-04.md`](m5-engineering-closure-2026-10-04.md) |
| Cluster | kind `as-m5`: rollout restart + scale; `/metrics` inside the Pod contains `as_active_calls` |
| Not included | HPA/O1 thresholds; D3; M7 SIP; config-service **Ready** on ingress requires external PG |

### M5 phase 0 baseline (2026-10-04)

| Item | Result |
|---|---|
| `make gate` | green (863+ passed unit/contract, 2 skipped) |
| `make chart-check` | OK (7 objects by default; config-service + ingress templates; HPA fail-fast) |
| `make test-integration-compose` | **142 passed, 3 skipped** (compose PG 12.22; 3 publication cases skipped because of `wal_level=replica`) |

| Item | Result |
|---|---|
| Deliverables | 9 templates in `deploy/helm/templates/` (per-use-case iteration of Deployment/Service, ConfigMap/Secret, HPA, PDB, SA, NOTES); `values.yaml` extended; 8 rules in `deploy/alerts/as-alerts.yaml` (two groups) |
| Capacity constraints | no CPS / concurrency absolute values anywhere in the repository; HPA thresholds and replica min/max are `null` + `required` guards (installation fails if unfilled); the PDB has no capacity defaults; alerts use only ratios / relative amounts / state amounts |
| Security and continuity | credential placeholders + replacement hints; TLS via customer PKI Secret mounting (rotation without restart); `preStop` draining + extended termination grace period; SA token automount disabled |
| Validation | all plain YAML passes `yaml.safe_load`; the templates did a static balancing self-check (fixing 2 issues: a missing `}}`, and `.Values` inside a range that should be `$`) |
| **Verified** | helm v3.16.2: `helm lint deploy/helm` 0 failed, `helm template as deploy/helm` exit 0; the first render exposed and fixed two left-trim-induced label concatenations in `_helpers.tpl`; the `--set autoscaling.enabled=true` (HPA thresholds unfilled) path failed as expected |

**Items M5 did not complete**: the operational wiring of the scale-down guard (the per-instance `active_calls` metric), the wiring of the PostgreSQL version of `VersionStore` and its real-database integration cases (carried over from M4), and capacity-class alerts (blocked by M6 / O1).

---

## M5 PostgreSQL loop and metrics (2026-09-28)

| Item | Result |
|---|---|
| Gate | ruff 146 files formatted / ruff check passed / mypy 34 source files clean / `unit or contract` **331 passed** (2 skipped); integration **12 passed** |
| PG implementation | `services/config-service/src/as_config_service/postgres_store.py`: versions are **immutably appended** (no UPDATE / DELETE; rollback relies on writing back the previous version's content), **table-name allowlist** (identifiers are not concatenated into SQL), `psycopg` **lazy import** (the module can be imported and unit tests run even without the driver installed) |
| Real-database run | 9 cases in `services/config-service/tests/test_postgres_store_integration.py`, really connecting to a PostgreSQL 16 container on `127.0.0.1:55432`; the governance loop passes: approval → persist → distribute → automatic rollback → retrieve the previous version; `pytest -m integration` across the repository is **12 passed** (9 PG + 3 telemetry export) |
| Metric seam | `platform/src/as_platform/telemetry/metrics.py`: `MetricsRegistry` (thread-safe, does not read the clock, does no IO, deterministically ordered snapshot) and `CallMetrics` (per-instance `as_active_calls`, `as_sip_responses_total` / `as_rule_hits_total` / `as_telemetry_dropped_total`), with the same names as the metric contract in `deploy/alerts/README.md`; export goes through `BoundedQueueSink`, dropping when full and never blocking the call path (ADR-0005) |
| Tests | 9 cases in `platform/tests/test_metrics.py` (marker `unit`), TDD red→green; including concurrent accumulation not losing updates, retrieval by instance, status-code classification, a `capacity=1` sink that neither raises nor blocks and has `dropped_count > 0`, and purity (no clock / no sockets) |
| Review | `docs/reviews/m5-helm-alerts-review.md`: H11 judged complete, with the signing condition changed to "rolling upgrade and scale-down verification in a real environment" |

**Unfinished items**: rolling upgrade and scale-down verification in a real environment (the per-instance `active_calls` metric is already queryable, but rolling upgrade and scale-down without call loss has not yet been verified on a real cluster); capacity-class alerts and HPA thresholds remain blocked by O1 / M6. This module only defines metric names and semantics and **contains no thresholds, targets or default values**.

---

## M5 container image (2026-09-30)

| Item | Result |
|---|---|
| Image | `docker build -t as-platform:dev -f deploy/docker/Dockerfile .` succeeded (191MB, manifest `sha256:3436b8dc84c9…`) |
| In-image verification | `import as_platform` succeeded (Python 3.10.21); the entry point `python -m as_platform --help` works |
| Security and consistency | non-root (`uid=10001`); `EXPOSE 5060/udp 5061/tcp` is consistent with the Helm container ports; ENTRYPOINT aligns with the templates setting no command/args |
| **ISSU measured** | `docker stop` (SIGTERM) inside the container → stops accepting new requests → drains → **exit code 0**; ADR-0009's draining genuinely works in the image |
| Chart rendering | rendered with a real image reference producing `image: "as-platform:dev"`, with `terminationGracePeriodSeconds: 300` and `preStop` both present |

**Unfinished**: rolling upgrade and scale-down verification on a real Kubernetes cluster — this machine has no cluster, and the `kind` / `kubectl` downloads failed on network timeouts (kubectl downloaded only about 3MB of roughly 56MB). This item is listed as a remaining M5 item and must be executed in an environment that has a cluster.

---

## M2b probe harness (2026-09-30)

| Item | Result |
|---|---|
| Deliverables | `testbed/probe/`: `e1_baseline_probe.py` (E1 baseline comparison, real sockets), `tls_hot_rotation_probe.py` (E4 / S12 certificate hot rotation), `sequence_compare.py` (a pure-function sequence comparator), `tests/test_sequence_compare.py` (10 unit cases), `README.md` |
| Comparison position | method / response code, `Call-ID`, the `host:port` of the Request-URI, and body byte-for-byte; header order / `Via` branch / SDP `o=` timestamp are not compared (ADR-0019 §5) |
| Behaviour when the binding is missing | **fails loudly, not skip**: both probes really run and both exit with **exit code 2**, printing `No module named 'resip'` and the `BUILD_PYTHON=ON` build instructions on stderr |
| Transport | the bytes really do go over the wire (`_SocketPeer` uses real sockets, framing by `Content-Length` per RFC 3261 §20.14); what is missing is the adapter on the system-under-test side (the Protocol is defined, not implemented) |
| Gate | ruff format / ruff check / mypy clean; `pytest -m "unit or contract"` 391 passed (2 skipped); `pytest -m integration` 12 passed |

**Harness self-check**: `testbed/probe/tests/test_e1_probe_selfcheck.py` (marker `integration`, 3 cases) uses a fake binding + a local replay server to verify the three paths over real sockets — match → exit 0; tampered expectation → exit 1 and point out the difference; binding missing → exit 2. A real run gives 3 passed. What the self-check proves is that the harness is wired up and that the comparison is live, **not that reSIProcate reproduces the baseline**.

**Currently unverified**: neither E1 (S1–S11) nor E4 (TLS hot rotation) **has been run at all** — this environment has no reSIProcate Python binding
(`BUILD_PYTHON=ON` was not built). The harness landing on disk is not evidence, and the gap list in ADR-0019 §6 step 5 is unchanged.

**The K2 constraint is still in force**: the SIP adaptation layer in `platform/` does not start work until the probe passes.

**Follow-up items**: the E5 (state externalisation / serialisation) probe has not been written yet; the baseline message files for S5–S11 are still missing, and the corresponding scenarios report `NO_BASELINE` in the probe.

## M2 P0 native reproducible path (2026-10-04; not M2 milestone acceptance)

| Item | Result |
|---|---|
| Deliverables | `testbed/simulators/resip-probe/scripts/m2-native.sh` + Makefile `m2-native` / `m2-native-restore` / `m2-native-build` / `m2-native-smoke`; the matrix is in [`m2-native-build-matrix.md`](m2-native-build-matrix.md) |
| Reproduction | `make m2-native` at the repository root: verify the vendor SHA256, unpack reSIProcate 1.14.0 @ `632e215c` offline, build `rutil`/`resip`/`dum` with CMake, link `resip_probe`, UDP S1 loopback smoke (`probe exits OK`) |
| Boundary | **testbed P0 only**; it is not the platform SIP adapter/runtime, not the TLS/peer-policy runtime wiring, not REQ-S acceptance and not M2 closure; the product DUM / `CallController` / Python bridge belong to **M7 (D9)**, see [`m2-adapter-boundary-adjudication-2026-10-04.md`](../reviews/m2-adapter-boundary-adjudication-2026-10-04.md) |
| Review | [`m2-p0-native-repro-review-2026-10-04.md`](../reviews/m2-p0-native-repro-review-2026-10-04.md): **P0 engineering slice Pass**; the maintainer signature is pending |

**Evidence date**: 2026-10-04 (`make m2-native` + `make gate` in the local / maintainer environment).

## M2 transport/runtime engineering closure (2026-10-05)

This section records the evidence summary for the M2 handoff P0–P3 **engineering slices** and the P4 **integration closure slice**. It is **not** M2 milestone acceptance, **not** REQ-S-2/3 (including wire proof of REQ-S-3 dual-cert overlap), and **not** operator PKI / S-SBC acceptance.

| Priority | Engineering slice | Partial evidence |
|---|---|---|
| **P0** | testbed native vendor restore + UDP S1 smoke | `make m2-native-smoke`; [`m2-p0-adjudication-2026-10-05.md`](../reviews/m2-p0-adjudication-2026-10-05.md) |
| **P1** | the boundary between the testbed transport and the product DUM | [`m2-adapter-boundary-adjudication-2026-10-04.md`](../reviews/m2-adapter-boundary-adjudication-2026-10-04.md) |
| **P2** (partial) | ingress seam; testbed TCP S1; product `ResipRuntimeListener` UDP/TLS + fingerprint + plaintext guard | `TransportIngressGate`; `m2-native-smoke-tcp`; `make m2-platform-resip-build`; `test_resip_runtime_integration.py` / `test_resip_runtime_tls_integration.py`; P2b–P2d review/adjudication 2026-10-05 |
| **P3** (partial) | overlap policy + native reload hook | `TlsRotationState` / `install_with_overlap`; `test_tls_rotation.py`; [`m2-p3-tls-rotation-adjudication-2026-10-05.md`](../reviews/m2-p3-tls-rotation-adjudication-2026-10-05.md) |
| **P4** (slice) | blocking gate + focused platform integration | `pytest platform/tests/test_resip_runtime_integration.py platform/tests/test_tls_rotation.py` (integration cases skip when the extension is not built; the rotation unit tests still run) |

**Explicitly not included**: D3 Redis Sentinel; complete REQ-S-2/3 test-plan acceptance; the product TCP transport; operator PKI / external S-SBC mTLS evidence; the M2 maintainer signature and the **M2 exit**. See [`m2-engineering-closure-adjudication-2026-10-05.md`](../reviews/m2-engineering-closure-adjudication-2026-10-05.md) for the combined ruling.

## M7 control-layer engineering closure (2026-10-05)

This section records the M7 **control-layer engineering slice** (the continuation after ADR-0022 was accepted), including the first slice and this continuation. It is **not** M7 milestone acceptance, **not** a D10/REQ-NF-1 pass, and **not** a REQ or K2 release.

| Deliverable | Evidence |
|---|---|
| Pure Python `CallController` | `platform/src/as_platform/sip/call_controller.py`; `platform/tests/test_call_controller.py` (gate) |
| Minimal product two-leg native | `platform/native/resip_two_leg/`; `make m7-platform-two-leg-build`; `platform/tests/test_resip_two_leg_integration.py` (`-m integration`) |
| Product runtime wiring | `ResipRuntimeListener`: ingress → `decide()` → `CallController` → SIP status (not the harness `accept_all_invites`); `platform/tests/test_resip_runtime_call_controller.py` |
| D10 product RecoveryTU (M7.1) | `platform/native/resip_recovery/`; `RecoveryStackSession`; `make m7-platform-recovery-build` |
| Non-blocking recovery continuation (M7.2) | `recovery_coordinator.py`; `platform/tests/test_recovery_coordinator.py` |
| CallController recovery (M7.3) | `restore_from_checkpoint` / `route_in_dialog_bye`; `test_call_controller_recovery.py` |
| Owner/commit (M7.4) | Checkpoint schema v2; `CallCheckpointCommit`; `save_if_generation`; `test_call_checkpoint_owner.py` |
| Checkpoint lifecycle (M7.5) | `CallCheckpointLifecycle`; the same unit tests |
| D10 product integration (M7.6) | `test_d10_product_recovery_integration.py` (`-m integration`; **not** REQ-NF-1 sign-off) |
| REQ-NF-1 engineering harness (M7.7) | `test_d10_req_nf1_harness_integration.py` + `scripts/d10-req-nf1-harness.sh`; `SipStackService` / `__main__.py` (**not** maintainer sign-off) |
| REQ-NF-1 real Redis integration (M7.8) | `test_d10_req_nf1_redis_integration.py` (`-m integration`; `AS_REDIS_URL` or db 15 by default; skips if unreachable; **not** maintainer sign-off) |
| D10 subprocess kill/restart (M7.9) | `test_d10_process_restart_integration.py` + `runtime/_d10_child.py`; Redis + `AS_RECOVERY_CALL_KEYS` (**not** maintainer sign-off) |
| E1 contract guard (narrow) | `test_e1_contract_resip_runtime.py`: S1 accept-all 200 + S2 404 (**not** complete E1 sign-off) |
| FORWARD UAC (product runtime) | `_resip_runtime`: Python `{"status":0,"route_target":...}` → minimal UAC INVITE |
| D10 honest status | [`m7-d10-status-2026-10-05.md`](../reviews/m7-d10-status-2026-10-05.md) — **still failing / unresolved** |
| M7.1–M7.6 engineering rulings | the per-slice reviews/adjudications `docs/reviews/m7-*-2026-10-05.md`; summary [`m7-d10-product-adjudication-2026-10-05.md`](../reviews/m7-d10-product-adjudication-2026-10-05.md) |
| M7.8–M7.9 Redis/restart engineering rulings | [`d10-redis-restart-review-2026-10-05.md`](../reviews/d10-redis-restart-review-2026-10-05.md), [`d10-redis-restart-adjudication-2026-10-05.md`](../reviews/d10-redis-restart-adjudication-2026-10-05.md) |
| M7 engineering summary | [`m7-final-engineering-adjudication-2026-10-05.md`](../reviews/m7-final-engineering-adjudication-2026-10-05.md) — **not** the milestone exit |

**Explicitly not included**: the complete plan §5 D10 baseline (maintainer signature, the unharnessed tag seam, a unified product process model); REQ-NF-1 **sign-off**; the final D9 adapter API ruling; complete E1 S1–S11; fork/CANCEL races; the M7 milestone signature.

**REQ-NF-1 / D10 acceptance checklist (maintainer sign-off, still unchecked):**

- [ ] Kill/restart the **shipping** AS (`python -m as_platform`) with a real Redis dialog record
- [ ] Upstream in-dialog BYE → peer BYE → upstream 200 **without** the harness-only tag rewrite
- [ ] Maintainer sign-off recorded in `acceptance/report.md`

Optional gates: `m7-recovery` (RecoveryTU integration), `m7-two-leg` (two-leg 486); integration cases skip when the native is not built.

## reSIProcate native DUM exploratory evidence (2026-09-30; not acceptance)

This section records only the exploratory native smoke tests and their failure results. It does not change the historical M1/M2 acceptance conclusions, does not constitute product acceptance, K2 release or K2 publication.

| Check | Result | Evidence boundary |
|---|---|---|
| Native DUM S1 self-loop | pass, exit 0; INVITE/180/200/ACK/BYE | A native smoke of the C++ resip-probe against reSIProcate 1.14.0 (commit `632e215c2ca9aee5416bfe1808851ea6fa380044`); not the product E1 |
| Native DUM S4 self-loop | pass, exit 0; CANCEL/487 | A native stack smoke; not the product E1 or REQ acceptance |
| Native TLS S1 | no call established; 503 Certificate Validation Failure, then timeout exit 124 | E4/S12 did not pass and is not accepted; rotation behaviour is still unverified |
| Python E1 harness | after running with an explicit port, `import resip` fails, exit 2 | neither a pass nor a skip; the product adapter does not exist |

An inspection of the upstream source confirms that reSIProcate 1.14.0's `BUILD_PYTHON=ON` enables PyCXX-based rePro routing/plugin targets and does not provide a generic `resip`/DUM Python module. The build artifacts and logs live only in `/tmp/as-resiprocate-userbuild`, not in the repository. Neither E1 nor E4 has product acceptance; E5/REQ-NF-1 state recovery remains unverified. The production stack is still the reSIProcate selected by ADR-0019; this record approves neither starting code work nor publishing K2.

## D9-D11 isolated native probes (2026-10-01; not acceptance)

The following results come from isolated experiments in `/tmp`, using reSIProcate 1.14.0 commit `632e215c2ca9aee5416bfe1808851ea6fa380044` and uv CPython 3.10.21. They supplement the feasibility evidence, change no historical milestone conclusion, are not product acceptance, do not release K2, and do not mean M7 has passed.

| Probe | Observation | Precise evidence and boundary |
|---|---|---|
| D9 CPython native callback | The C++ extension calls Python on the native caller thread and on a worker thread; ordering, Python exception identity/traceback and refcount checks pass. | `/tmp/as-resip-python-bridge-spike/RESULTS.md`. Not a DUM binding; the timings are not product performance metrics. |
| D9 DUM→Python UAS | A real UDP INVITE reaches SipStack+DUM; `onNewSession` makes a GIL-safe call into the existing `as_platform.decision.decide`, an empty RuleSet returns 404; the exception path returns 500 and the process survives. | `/tmp/as-resip-dum-python-slice/RESULTS.md`. The event loop and the Python caller TID differ; not a complete adapter/B2BUA. |
| D9 two-leg failure branch | `Action.FORWARD` creates an outbound UAC; the downstream 486 comes back through the DUM `onFailure` to the inbound UAS; the two legs have different Call-IDs and the transaction ACK completes. | `/tmp/as-resip-dum-two-leg-spike/RESULTS.md`. One failure branch, not complete E1. |
| D9 early CANCEL | The isolated rerun completes `PROBE_B_PASS`: the DUM sends 200/487 to the upstream CANCEL/INVITE, the controller fires `end(DialogSetId)`; the downstream actually receives CANCEL and replies 200/CANCEL and 487/INVITE, and the DUM sends the non-2xx ACK. | `/tmp/as-resip-dum-final-probes/logs/probe-b-final-isolated.log`. Only one early branch; it does not cover the final-response race or forking. Earlier barrier/synchronisation attempts timed out because the runner waited on 100/180. |
| D11 SDP body | Two valid CRLF offers (143 and 233 bytes) compare equal when forwarded verbatim; S1's 230-byte offer reaches downstream verbatim. A different 238-byte answer (SHA-256 `eda2ed79576b309318cfb7580496e751c50094d817ca031e6ae0e8502aad5e9d`) returns verbatim to upstream and differs from the offer. | `/tmp/as-resip-dum-sdp-spike/RESULTS.md`, `/tmp/as-resip-dum-sdp-roundtrip/RESULTS.md`, `/tmp/as-resip-dum-final-probes/logs/probe-a-final.log`. On the first S1 roundtrip the 230-byte answer was identical to the offer, which alone cannot prove a distinct answer. A limited corpus, not a complete adapter/REQ-F-4 acceptance. |
| D10 UAC restart hook | Two subprocesses each create a fresh SipStack+DUM; after Phase A exits, Phase B uses `DialogSetId`, manually restores the To-tag/Route/remote target and increments the CSeq, sends a re-INVITE under the same Call-ID/tags, receives a 200 and ACKs. | `/tmp/as-resip-dum-process-restart/RESULTS.md`. The old `InviteSession` or `SipStack` transaction is not restored, and mapping recovery of the product `CallController` is not proven. The INVITE/ACK transaction of the current baseline has already completed, so this gap only concerns the optional mid-transaction extension; the probe did not test RTP/media. |
| D10 UAS restart | Phase A establishes a UAS dialog and completes 200/ACK; after the process exits a fresh DUM receives the correct BYE for the same dialog and actually returns 481. The source shows that a missing DUM private dialog-set map entry yields 481; no public UAS rehydrate API was found. | `/tmp/as-resip-dum-uas-restart/RESULTS.md`. This 481 makes the current ACK-established-dialog BYE/Redis baseline fail; it is a SIP control-state recovery failure, not evidence of RTP interruption; media was not tested. This result does not prove that a custom DUM extension is impossible. |

**The acceptance conclusion is unchanged: D10 fails / is unresolved.** The current gate is ACK-complete dialog → kill/restart → upstream in-dialog BYE → the replacement routes BYE to the peer → Redis contains a complete dialog record; a fresh DUM returns 481 for that BYE, so the SIP dialog/control-state recovery baseline fails. The UAC hook is not equivalent to UAS or CallController state recovery. REQ-NF-1 remains a hard requirement, M7 acceptance has not passed, and K2 is not released. `SipStack` transaction recovery still in flight at process crash is untested but is not part of the current gate; bringing it in would require separately extending/amending the requirement and test plan and a maintainer ruling. This D10 check has no RTP/media path and does not prove media interruption. D11 only proves native DUM body identity for a limited input set; REQ-F-4 can only be assessed after extending to the complete product adapter, the POC baseline and the boundary variants the stack accepts. The experiments above changed no repository code; this document update did not re-run `make gate` and makes no gate claim.

## Engineering evidence: CallStateCheckpointRepository (2026-10-01; NOT D10 ACCEPTANCE)

This section records only the engineering implementation and verification. It does not change the historical M1 conclusions, does not constitute D10 acceptance, and does not mean any REQ has been accepted; ADR-0023 remains proposed and unaccepted.

- The first version of `platform/src/as_platform/state/call_checkpoint.py` encodes the two established dialog legs as schema-v1 deterministic JSON bytes and stores them as one `StateStore` key/value; the TTL is a positive integer; the namespace and the explicit header allowlist are validated on both the save and load sides; CR, LF and NUL are rejected. The contract test `platform/tests/test_call_state_checkpoint.py`: **14 passed**. This is only serialisation/repository groundwork.
- Local verification on 2026-10-01: the focused contract tests are **14 passed**; `make gate` reported ruff format 188 files formatted, ruff check fully passing, mypy 36 source files clean; pytest **406 passed, 2 skipped, 15 deselected**. Local only.
- A manual real Redis 7 + redis-py check passed: a single key `as:translation:call:redis-checkpoint-test` was written with a positive server-side TTL; a newly created `RedisStateStore`/repository read back a completely identical checkpoint; the temporary container has been removed. This is a manual integration check, not a committed test or acceptance.
- This direction is the user-chosen minimal Redis application-layer checkpoint, recorded in ADR-0023 which is still proposed. Product DUM/CallController integration is missing; there is no UAS rehydrate, no D10 BYE routing proof, no owner fencing/CAS/generation, and no durable-commit/write-before-side-effect guarantee. D10 still fails because of the fresh-DUM 481, REQ-NF-1 is unmet and K2 is blocked; in-flight transaction recovery is not part of the current D10 test plan. RTP/media was neither tested nor added.

## D10 RecoveryTU loopback probe: engineering evidence (2026-10-01; NOT D10 ACCEPTANCE)

This section records testbed-only feasibility evidence. It does not change the result above, namely that a fresh DUM returns 481 for a BYE on the same dialog after a restart, and does not change the D10 fail/unresolved acceptance conclusion. **This is not D10 acceptance; REQ-NF-1 is still NOT PASSED, no REQ has been accepted, the M7 TODOs remain open, and K2 is blocked.**

- The probe files live in `testbed/simulators/resip-probe/d10-recovery/`: `README.md`, `d10_recovery.cxx`, `orchestrate.py`, `run.sh`. The latest main-agent command `bash testbed/simulators/resip-probe/d10-recovery/run.sh` ends in `PASS`, with the runner exiting 0; compiling/linking reSIProcate 1.14.0, with `ldd` and Python syntax checks passing. A disposable Docker Redis 7.4.11 passed typed `CallStateCheckpointRepository` save/load and TTL checks; the checkpoint has been deleted and the Redis container removed.
- Phase A establishes the UAS and outbound UAC legs through the DUM; a fake raw-UDP peer verifies the UAC INVITE/200/ACK. Phase A exits before Phase B starts. Python uses the current `CallStateCheckpointRepository` and a real `RedisStateStore` across processes.
- Phase B creates a fresh SipStack+DUM and registers the front `RecoveryTU`: a matching BYE is routed to the fake peer via the checkpoint and the upstream receives a 200 after the peer returns 200; an unknown BYE falls back to the DUM and returns 481 without being forwarded. `orchestrate.py` passes Ruff check/format.
- The latest local `make gate` in the workspace: ruff format 190 files formatted, ruff check clean, mypy 36 source files clean, pytest **417 passed, 2 known skips, 15 deselected**. This is local evidence, not remote verification.
- Limits: the fixture's route sets are empty; Phase B receives the typed checkpoint from a temporary native adapter file, the Redis lookup runs in Python outside the callbacks and across processes, and the product's asynchronous Redis continuation is untested. The probe's `RecoveryTU` is testbed code, not the product adapter or `CallController`; there is no fencing/generation, no Redis HA/RPO, no in-flight transaction recovery, no RTP/media and no graceful transaction-drain proof. The Phase A/B shutdown logs show client/server transaction state warnings. A fresh DUM still returns 481 without that `RecoveryTU`, so the probe only proves that a custom front TU can route this loopback fixture.

## M4b-3 change-order journal: engineering evidence / NOT M4b/M4 ACCEPTANCE (2026-10-01)

This section records only the M4b-3 implementation and engineering verification. It is **not M4b or M4 acceptance**, does not change the overall incomplete state of M4/M4b, and does not claim acceptance of any REQ.

- **Implementation**: `services/config-service/src/as_config_service/change_order_store.py` provides an append-only PostgreSQL change-order journal; JSON snapshots use a strict, versioned format; the head revision uses CAS/row locks; there are deferred head-to-event foreign keys and database triggers preventing event UPDATE/DELETE; it includes a prefix-safe guard function. The complete legal state transitions and exactly-once audit append are validated; blank reject/rollback reasons are rejected at the pure state machine layer.
- **Tests**: the latest focused run of `services/config-service/tests/test_change_order_store.py` is **9 passed**. The real PostgreSQL integration command `AS_PG_TEST_DSN=postgresql://postgres@127.0.0.1:55432/as_config uv run pytest -q services/config-service/tests/test_postgres_change_order_store_integration.py` is **6 passed** on a temporary PostgreSQL **12.22** (two integration test functions, six parametrized cases), covering append/CAS/history and the database constraints. PostgreSQL 16 compatibility is **not yet verified** and is a non-blocking follow-up; the PG12 result does not represent PG16 or deployment acceptance. The temporary server binds only loopback, the data/logs are in `/tmp/as-m4b-postgres`, and it has been stopped after testing; no system packages were installed and no user or production database was touched.
- **Review and fixes**: the independent reviewer pointed out blank reject/rollback reason consistency, plus DB immutability, head FK, skip and cleanup problems; the implementation fixes have been applied. The final reviewer found no implementation problems with the invariants and recommended adding a rollback blank-reason persistence-validator test; that test has been added and the separate re-review found nothing.
- **M4b-3 stage local gate (historical)**: `make gate` reported Ruff format 197 files; Ruff clean; mypy 38 source files clean; pytest **463 passed, 2 known skips, 21 deselected**. Local results only, local run only; the M4b-4 stage gate has since been updated, see the next section.
- **Scope boundary**: this slice is only the journal engineering groundwork; there is no HTTP API, ManagedRule persistence, authentication/session, UI integration or M4b acceptance. The PG12.22 integration pass does not constitute M4b acceptance and does not mean any REQ has been accepted; PG16 compatibility is still to be verified. M4/M4b as a whole remains open; M5 is still a partial delivery and the M6 status is unchanged; the D10/REQ-NF-1 and PM/AM/UM gaps keep their current recorded status.

See [`m4b-3-change-order-journal-review-2026-10-01.md`](../reviews/m4b-3-change-order-journal-review-2026-10-01.md): the M4b-3 journal slice is a conditional pass within the tested scope on PG12.22; the maintainer signature has been recorded (2026-10-04); PG16 compatibility remains a non-blocking follow-up; it does not mean M4b/M4 completion or REQ acceptance.

## M4b-4 ManagedRule persistence (2026-10-01; engineering evidence, NOT M4b acceptance)

This section records the engineering implementation and verification of the M4b-4 ManagedRule durable store. It does not constitute M4b or M4 acceptance and does not claim acceptance of any REQ. M4b/M4 as a whole remains incomplete.

- **Implementation**: `services/config-service/src/as_config_service/managed_rule_store.py` persists ManagedRule as append-only PostgreSQL snapshots/tombstones; the snapshot is schema-v1 JSON, and revision updates use a row lock + CAS. The database contains deferred head/event foreign keys, triggers rejecting event UPDATE/DELETE/TRUNCATE, a prefix-safe guard function, and audit records with actor/change metadata plus limited timestamp checks.
- **Focused tests**: `test_managed_rule_store.py` (unit) and `test_postgres_managed_rule_store_integration.py` total **38 passed**. Only the integration file's **6 parametrized cases** actually run on a temporary PostgreSQL **12.22**; 38 is the combined total of the two files, not 38 database tests. That integration subset covers create/update/delete history and tombstones, CAS/duplicate, event UPDATE/DELETE/TRUNCATE rejection, deferred FK rollback, and the PostgreSQL >=12 guard.
- **Local gate (M4b-4 stage historical result)**: `make gate` gave Ruff format **200 files formatted**, Ruff clean, mypy **39 source files clean**, pytest **506 passed, 2 known skips, 36 deselected**. Local results only, local run only. In addition, the config-service integration markers are **30 passed, 145 deselected** on PG12.22; this is broader local supplementary evidence, not remote verification or acceptance.
- **Environment and compatibility**: the temporary PostgreSQL 12.22 is an Ubuntu deb unpacked into `/tmp/as-m4b-postgres`, binds only loopback, and was stopped after testing; no system packages were installed. PostgreSQL 16 compatibility is **not yet verified** and is listed as a non-blocking follow-up.
- **Review**: the TRUNCATE immutability, Unicode audit metadata and PostgreSQL version assertion problems raised by the independent review have all been fixed; the final M4b-4 reviewer had no findings. The maintainer sign-off has been recorded (2026-10-04).
- **Scope boundary**: the current implementation only covers management-plane persistence; there is no runtime RuleDTO mapping, regex compilation, HTTP API, authentication/session or UI operation flow. The pass of this slice applies only to the tested PostgreSQL 12.22 scope, does not mean M4b/M4 completion and does not constitute REQ acceptance.

See [`m4b-4-managed-rule-store-review-2026-10-01.md`](../reviews/m4b-4-managed-rule-store-review-2026-10-01.md): the conclusion is only a pass for the tested PostgreSQL 12.22 slice; the maintainer signature has been recorded (2026-10-04); PG16 compatibility remains a non-blocking follow-up.

## M4b-5-2b ChangeOrder journal write API: engineering evidence / NOT M4b/M4 ACCEPTANCE (2026-10-01)

This section records the engineering implementation and verification of M4b-5-2b. It is **not M4b or M4 acceptance** and does not mean any REQ has been accepted. M4b and M4 as a whole remain incomplete; the UI, real authentication/session and persistent console audit are not wired up.

- **Routes and state transitions**: FastAPI provides `POST /internal/v1/change-orders` to create a draft, plus `POST /internal/v1/change-orders/{change_id}/submit`, `/approve` and `/reject`. All writes only append ChangeOrder journal snapshots. Identity, permission callbacks, timestamp and change-ID generation are all injected by `create_app`; submit and approve use independent permission checks, a submitter cannot approve their own, and reject must supply a non-empty reason. Transitions are appended with journal-revision CAS and include request validation and error mapping.
- **Security and consistency boundary**: the auth callbacks of `create_app` are an integration seam, not a real auth provider, login or session. This API does not write ManagedRuleStore, does not apply runtime rules, does not distribute ConfigBundle, and does not provide cross-store atomicity between ChangeOrder and ManagedRuleStore. The coordination of the two persisted states on APPLIED is only handled by 5-2c. The browser/UI is not yet connected and persistent console audit is not implemented.
- **Focused tests**: at the M4b-5-2b stage, the FastAPI write API focused tests are **48 passed**, using fake stores; CAS was not exercised against PostgreSQL through the routes, and the combined behaviour of concurrent API clients with PostgreSQL CAS was not tested. The independent reviewer finally had no findings. There was one Starlette/httpx deprecation warning during testing that does not affect the pass.
- **PostgreSQL and overall gate (M4b-5-2b stage historical snapshot)**: the config-service integration markers are **30 passed, 216 deselected** on PostgreSQL **12.22**, including the durable stores. That stage's local `make gate`: Ruff format **204 files**; Ruff clean; mypy **40 source files clean**; pytest **577 passed, 2 known skips, 36 deselected**, plus one warning. All local results, local run only. PostgreSQL 16 compatibility is unverified and is a non-blocking follow-up; M4b-5-2c and M4b-5-2d2 below are both historical stage evidence; the 6b stage gate snapshot is in the M4b-6b section below.
- **Follow-up and acceptance boundary (M4b-5-2b stage record)**: the planned next step at the time was M4b-5-2c: design first, then coordinate the active ManagedRule snapshot with the ChangeOrder `APPLIED` transition using a shared PostgreSQL transaction; cross-store consistency/atomicity is not claimed before implementation and verification. That step and the later M4b-5-2d1/d2 and M4b-6a/6b engineering slices have all been delivered. The current next step is M4b-7 UI integration, followed by M4b-8 browser acceptance (see this report's latest M4b-6b section and the current status in `docs/plan.md`). No REQ acceptance is achieved by any of this.

See [`m4b-5-2b-write-api-review-2026-10-01.md`](../reviews/m4b-5-2b-write-api-review-2026-10-01.md): the final independent review had no findings; the maintainer signature has been recorded (2026-10-04).

## M4b-5-1 identity/permission-gated read-only API: engineering evidence / NOT M4b ACCEPTANCE (2026-10-01)

This section records only the engineering implementation and verification of M4b-5-1. It is **not M4b or M4 acceptance** and does not claim acceptance of any REQ. M4b-5 as a whole remains open; neither M4b nor M4 is complete.

- **Routes and authorisation**: `services/config-service/src/as_config_service/api.py` provides `GET /internal/v1/managed-rules`, `GET /internal/v1/managed-rules/{rule_id}`, `GET /internal/v1/change-orders` and `GET /internal/v1/change-orders/{change_id}`, reading from the injected durable stores. The data routes inject an identity resolver and a config read authoriser; a missing identity returns 401 and no read permission returns 403. A detail miss returns 404; path IDs are length- and control-character-validated.
- **Responses and exposure surface**: Pydantic nested response models explicitly correspond to ManagedRule / ChangeOrder serialised records with a schema version. A tombstone detail returns `rule: null` and the revision. Since no real auth scheme exists yet, both the docs and the OpenAPI endpoints are disabled; this slice provides no login/session/auth provider.
- **Focused API tests**: at the M4b-5-1 stage, `services/config-service/tests/test_api.py` had **28 passed**, covering authorisation success/denial, list/detail, tombstones, 404, path length and Unicode control validation, and valid `@` / hyphen IDs. The later API suite has been extended. The API `TestClient` has one Starlette deprecation warning, and httpx2 is recommended; as a non-blocking tooling follow-up, this doc-only slice adds no dependency.
- **Database and local gate evidence (M4b-5-1 stage historical snapshot)**: the config-service integration markers are **30 passed, 145 deselected** on a temporary PostgreSQL **12.22**, including the two durable stores; PostgreSQL 16 compatibility remains a non-blocking follow-up. That stage's local `make gate`: Ruff format **203 files formatted**, Ruff clean, mypy **40 source files clean**, pytest **534 passed, 2 known skips, 36 deselected**; plus the one Starlette deprecation warning above. All of these are local results, **local run only**; the PG12 result does not represent PG16 or deployment acceptance. M4b-5-2c and M4b-5-2d2 below are both historical stage evidence; the M4b-6b stage gate snapshot is in the corresponding section below.
- **Not implemented / scope boundary**: runtime rule DTO mapping, regex compilation, write routes, change-order submission/approval/rollback API, auth provider/login/session integration, persisted console audit and UI connection are all unimplemented. This read-only API establishes no atomicity between the ManagedRule and change-order journal stores; that is the design and implementation work of M4b-5-2. M4b-5-1 does not constitute M4b/M4 completion or REQ acceptance.

See [`m4b-5-1-read-api-review-2026-10-01.md`](../reviews/m4b-5-1-read-api-review-2026-10-01.md): the final independent review had no findings; the maintainer sign-off has been recorded (2026-10-04).

## M4b-5-2c APPLIED transaction coordination: engineering evidence / NOT M4b/M4 acceptance (2026-10-01)

This section records the single-PostgreSQL-transaction implementation and verification only. It is **not M4b or M4 acceptance**, does not establish global/distributed atomicity or active-fleet delivery, and does not claim acceptance of any REQ. M4b and M4 remain incomplete.

- **Transaction boundary**: `apply_distributed_change` coordinates typed `CREATE` / `UPDATE` / `DELETE` `ManagedRuleChange` operations with the ChangeOrder `APPLIED` transition using the same psycopg connection. ManagedRuleStore create/append and ChangeOrderStore `append_transition` run with `commit=False`; one commit follows both writes. Errors roll back the transaction. Before reads or writes, the operation verifies exact connection identity and that `psycopg` reports transaction status `IDLE`. The caller must exclusively own that idle connection for the entire call.
- **Integration coverage**: the activation integration file contains seven cases. Coverage includes CREATE, UPDATE, DELETE, the legacy no-proposal path, the different-connection guard, and a stale ChangeOrder revision after a provisional ManagedRule write, verifying rollback of both stores. The latest config-service integration run against PostgreSQL **12.22** was **37 passed, 216 deselected**. PostgreSQL 16 compatibility remains an unverified, nonblocking follow-up.
- **Review and local gate**: the separate activation review found no findings after the idle-connection guard was added; maintainer signoff recorded 2026-10-04. M4b-5-2c stage historical local `make gate`: Ruff format **207 files formatted**, Ruff clean, mypy **41 source files clean**, pytest **577 passed, 2 known skips, 43 deselected**, with one non-failing Starlette warning. Local only; no remote verification was run.
- **Limits and next step at that stage**: this is one PostgreSQL transaction, not cross-host/failover/distributed atomicity; it does not include delivery to the active fleet. It is not D10 or SIP-runtime proof. M4b-5-2b remains journal-only. At the time of this M4b-5-2c stage, next was M4b-5-2d: connect the actual distribution result to the `APPLIED` API path and expose observed status. M4b-6 was the next step after that 5-2c stage; M4b-6a auth/session and M4b-6b durable audit have since been delivered as engineering slices. The current next step is M4b-7 UI operation-flow integration; see the latest M4b-6b section below. No REQ acceptance is claimed.

See [`m4b-5-2c-applied-transaction-review-2026-10-01.md`](../reviews/m4b-5-2c-applied-transaction-review-2026-10-01.md) for the standalone review record and detailed boundaries.

## M4b-5-2d1 PostgreSQL distribution journal (2026-10-02; engineering evidence, NOT M4b acceptance)

This section records the durable distribution journal engineering slice and its test evidence. It is **not M4b or M4 acceptance**, does not claim any REQ has been accepted, and does not mean active-fleet delivery results have been obtained.

- **Scope and persistence**: `services/config-service/src/as_config_service/distribution_store.py` persists purely batch-reported outcomes and observed status, keeping history in immutable event snapshots; it protects journal consistency through deferred head/event consistency triggers, a monotonic `+1` head guard and prefix CAS. The test files are `services/config-service/tests/test_distribution_store.py` and `services/config-service/tests/test_postgres_distribution_store_integration.py`.
- **Behaviour coverage**: begin, batch progress, completion, automatic and explicit rollback, stale/duplicate revision, snapshot immutability, deferred FK, rejecting a head event, rejecting head rewind; the concurrency regression uses two independent connections and deterministically proves before the winner commits that the loser is already in lock wait, covering the PostgreSQL READ COMMITTED joined lock-read race. A hostile shadow `search_path` and writes into a custom schema are also covered.
- **Database and focused tests**: the Distribution unit suite is **51 passed**; the Distribution PostgreSQL integration suite is **8 passed**. The config-service focused tests for ChangeOrder, ManagedRule, Distribution unit + PostgreSQL integration and activation integration total **156 passed**, connecting to a temporary PostgreSQL **12.22** (Ubuntu `12.22-0ubuntu0.20.04.4`), with the DSN host being loopback `127.0.0.1:55432`. This focused result is not remote verification; PostgreSQL 16 was not tested and is a non-blocking follow-up.
- **M4b-5-2d1 stage historical local gate**: the command `make gate`. Ruff format: **211 files already formatted**; Ruff fully passing; mypy **42 source files clean**; pytest `-m "unit or contract"`: **636 passed, 2 skipped, 56 deselected**, plus one non-failing Starlette/httpx deprecation warning. All local results, local run only; the later M4b-6b stage gate snapshot is in the corresponding section below.
- **Review findings and fixes**: the independent review found gaps in the head/event maximum-revision invariant across ChangeOrder, ManagedRule and Distribution; `search_path` shadowing in the trigger functions; inconsistency between the ChangeOrder embedded id and the relational key; and store SQL paths vulnerable to search-path shadowing. After the fixes, all three stores accept a verified keyword-only `schema="public"`, fully qualify the schema in SQL and do not modify the connection's `search_path`. The concurrent lock-wait/read race was also fixed with a deterministic PostgreSQL regression test. The final independent re-review of the database guards, schema qualification and that concurrency test found no remaining concrete defects; the maintainer signature has been recorded (2026-10-04), see the [independent review record](../reviews/m4b-5-2d1-distribution-journal-review-2026-10-02.md).
- **Boundaries and next step**: this store only saves reported batch outcomes; it does not notify AS instances, does not prove fleet delivery, does not activate a ManagedRule or ChangeOrder, and does not constitute global/distributed atomicity. The d2 API/report-to-activation wiring is recorded in the next section as engineering evidence; auth/session, persistent audit, UI operation flows and browser acceptance remain open. M4b/M4 and all REQ acceptance are neither complete nor claimed; the PG12.22 result does not represent PG16 or deployment acceptance.

## M4b-5-2d2 distribution API/report integration (2026-10-02; engineering evidence, NOT M4b acceptance)

This section records the M4b-5-2d2 route/API operation-flow engineering slice. It is **not M4b or M4 acceptance**, does not claim any REQ has been accepted, and does not prove fleet delivery, AS runtime activation or real health attestation.

- **Routes and operation flow**: `POST /internal/v1/change-orders/{change_id}/distribution` starts distribution from `APPROVED`, writing the Distribution begin and the ChangeOrder `DISTRIBUTING` in one PostgreSQL transaction. `GET /internal/v1/change-orders/{change_id}/distribution` returns the observed report status. `POST /internal/v1/change-orders/{change_id}/distribution/reports` accepts the current batch's bool reports: on partial health it commits only the Distribution; on ill health it records the Distribution and the ChangeOrder `ROLLED_BACK` in one transaction; the successful final batch first persists `COMPLETED` and then calls the existing `apply_distributed_change`. `POST /internal/v1/change-orders/{change_id}/apply` only allows `COMPLETED`, and can safely replay an existing `APPLIED` transition whose actor/revision match exactly; `POST /internal/v1/change-orders/{change_id}/rollback` only allows a manual rollback of in-progress distribution and writes both snapshots in one PostgreSQL transaction.
- **Identity, audit and concurrency boundaries**: the routes use an injected `can_approve_change` permission seam, not a real auth provider or session integration; persistent console audit is not implemented. A request-level primitive lock serialises the shared injected PostgreSQL connection within the same app; that connection must be dedicated and must not be shared outside the app or with other callers. The idle/pre-existing-transaction guard and app cleanup guarantee the call boundary, but this is not a cross-process or cross-instance lock.
- **Transaction boundary and report semantics**: Distribution completion is a committed PostgreSQL transaction; the subsequent ManagedRule + ChangeOrder `APPLIED` coordinator is a second PostgreSQL transaction. There is no global/distributed atomicity between the two. The API can only receive reports and has no AS notifier/transport; there is no evidence that the AS has loaded a given version and no real health attestation. Therefore a batch report is not fleet delivery or runtime version verification.
- **Focused verification**: the command `AS_PG_TEST_DSN='postgresql://postgres@127.0.0.1:55432/as_config' uv run pytest -q services/config-service/tests/test_api.py services/config-service/tests/test_postgres_activation_integration.py services/config-service/tests/test_postgres_distribution_store_integration.py`: **79 passed**, with one existing Starlette/httpx deprecation warning. The full config-service integration command `AS_PG_TEST_DSN='postgresql://postgres@127.0.0.1:55432/as_config' uv run pytest -m integration -q services/config-service/tests`: **61 passed, 280 deselected**, the same warning; using a temporary PostgreSQL **12.22** (Ubuntu `12.22-0ubuntu0.20.04.4`). The API unit suite alone is **53 passed**. PostgreSQL 16 was not tested and is a non-blocking follow-up.
- **M4b-5-2d2 stage historical local gate**: `make gate` gave Ruff format **212 files already formatted**; Ruff clean; mypy **42 source files clean**; pytest `-m "unit or contract"` **641 passed, 2 skipped, 67 deselected**; one non-failing Starlette/httpx deprecation warning. All local results, local run only. This result is the d2 stage snapshot; the M4b-5-1, 5-2b, 5-2c and 5-2d1 figures above are also historical snapshots of their respective stages. The later M4b-6b stage gate snapshot (**767 passed, 2 skipped, 131 deselected**) is in the corresponding section below.
- **Independent review findings and fixes**: the review found a P1 connection transaction-sharing race; app-scoped request serialisation, an idle/pre-existing-transaction guard and cleanup have been added for both routers. It also found that P2 `/apply` might reject a safe retry of the original revision; replay is now only accepted when the actor matches exactly, the revision is expected+1 and the last audit action is `mark_applied`, while other stale requests still return 409. The final independent reviewer had no actionable findings on that slice; the maintainer signoff has been recorded (2026-10-04). See the [independent review record](../reviews/m4b-5-2d2-distribution-api-review-2026-10-02.md).
- **Engineering and acceptance boundary**: this slice wires API reports into the existing activation coordinator but implements no notifier, no real AS health evidence, no auth/session, no persistent audit, no UI operation flow and no browser acceptance; runtime schema mapping and executable regex semantics remain unresolved. M4b/M4 stay open, UI browser acceptance is pending, and no REQ acceptance is claimed. The temporary PG12.22 verification does not represent PG16 or deployment acceptance.

## M4b-6a Console password and sessions (2026-10-02; engineering evidence, NOT REQ-S-4 ACCEPTANCE)

This section records the M4b-6a stage's console role/password/session engineering slice. It is **not REQ-S-4, M4b or M4 acceptance** and does not claim any REQ has been accepted. At the time, M4b-6b durable audit, M4b-7 login/UI operation-flow integration and M4b-8 browser acceptance were all still open; M4b-6b has since been delivered (see the latest section at the end of this report), while M4b-7/8 and M4b/M4 as a whole remain incomplete. ADR-0024 is **Accepted** (2026-10-03); the M4b-6a maintainer signature has been recorded (2026-10-04).

- **Implementation path**: `services/config-service/src/as_config_service/auth.py` provides `PostgresConsoleAuthStore`, a strict ADR-0024 PBKDF2 verifier, digest-only session/CSRF token persistence, per-request resolution of currently enabled roles, transactional session revocation, singleton-locked first-admin bootstrap, user management and last-enabled-admin protection. Passwords are verified against the exact UTF-8 input; PBKDF2-HMAC-SHA256 uses 600,000 rounds, a 16-byte salt and 32-byte output, does not normalise/truncate, rejects anything over 1,024 UTF-8 bytes, and compares in constant time. Sessions/CSRF use 256-bit random tokens, storing only digests; the session absolute TTL is at most 8h. `bootstrap_admin.py` provides `as-config-bootstrap-admin`, reading the initial administrator password with `getpass`.
- **API behaviour**: `services/config-service/src/as_config_service/api.py` supports optional session auth in `create_app`; when configured it is the primary, fail-closed path, and the existing callback mode stays compatible but is not a failure fallback. Login requires the ASGI `request.url.scheme` to be HTTPS; no production ingress/trusted-proxy configuration has been verified. It uses `__Host-` cookies, CSRF on writes, the existing RBAC policy, and logout plus account list/create/update. An app-scoped request lock protects the shared auth-store connection within that app and is not a cross-process lock. The store's constraints are dedicated injected PostgreSQL connections; on error it rolls back the entire active transaction, even when the call argument is `commit=False`.
- **Test files and results**: the focused test files `test_api.py`, `test_auth.py`, `test_postgres_auth_integration.py` and `test_postgres_auth_api_integration.py` total **116 passed**, with 11 Starlette/httpx deprecation warnings. The full config-service integration command `AS_PG_TEST_DSN='postgresql://postgres@127.0.0.1:55432/as_config' uv run pytest -m integration -q services/config-service/tests`: **85 passed, 319 deselected**, PostgreSQL **12.22**, with TestClient warnings; PG16 was not tested. Both are local verifications, not remote verification.
- **Local gate snapshot at the M4b-6a stage**: `make gate`: Ruff format **220 files already formatted**; Ruff clean; mypy **44 source files**; `unit or contract` **680 passed, 2 skipped, 91 deselected**; 8 non-failing Starlette/httpx deprecations (one base warning plus TestClient per-request cookie warnings). Local results, local run only.
- **Independent review**: the auth/core and API independent reviewers finally found no remaining concrete findings after the fixes; see the review record [`m4b-6a-auth-session-review-2026-10-02.md`](../reviews/m4b-6a-auth-session-review-2026-10-02.md). The maintainer signoff has been recorded (2026-10-04).
- **Boundaries**: M4b-6a itself contains no durable append-only audit; M4b-6b has since delivered durable audit API/store integration as a separate engineering slice (see below), but that does not represent complete audit acceptance or REQ-S-4 acceptance. The 6a implementation recorded here also contains no application rate limiting, MFA/SSO, browser login UI or authenticated proxy deployment proof. DB runtime-role least-privilege/audit grants are outside the 6a stage and were unverified at the time; the later M4b-6b engineering slice audited the effective grants on PostgreSQL 12.22. Runtime grant configuration in the deployment environment and PostgreSQL 16 remain unverified; this is not deployment acceptance. The existing `TestClient` deprecations do not fail and are local only. The ADR-0024 draft was not accepted by the maintainer; this engineering evidence does not constitute an REQ-S-4 pass and does not meet the test-plan's acceptance conditions.

## M4b-6b Durable audit API/store integration (2026-10-02; engineering evidence, NOT REQ-S-4/M4b ACCEPTANCE)

This section records the final engineering state of the persisted audit store and config API integration. It is the M4b-6b engineering slice, not REQ-S-4, M4b or M4 acceptance, and not security certification; ADR-0024 is **Accepted** (2026-10-03); the M4b-6b maintainer sign-off has been recorded (2026-10-04).

- **Events and data minimisation**: `AuditRecord` stores actor, action, resource, outcome, time and controlled before/after snapshots; the detail is not persisted. Credential-key/value markers and PEM private-key markers are heuristic checks, not a complete secret scanner; a producer allow-list/redaction remains the necessary defence line. The snapshot cap is 64 KiB, with safe length and character bounds on metadata. Login/logout snapshots record only safe user/session timestamps and contain no password or token.
- **Database boundary and permissions**: `PostgresAuditStore` requires explicit migration/owner setup and runs in a dedicated non-public schema; it validates the allow-listed schema object catalog, exact columns/defaults/constraints/triggers and sequence attributes, does not support partitions or PostgreSQL publications, and uses a retained-history guard to prevent the sequence from diverging from the retained history. An owner trigger prevents row mutation/truncate. The runtime role must be NOLOGIN, have no CREATEROLE/membership, and have only schema USAGE, table SELECT and INSERT excluding the `id` column, and sequence USAGE/SELECT; no schema CREATE and no table mutation. Application startup validates the runtime role; a separate login role must `SET ROLE` into the runtime role. Code verification does not prove a deployed database configuration or PG16 compatibility.
- **API and transactions**: by default `create_app` requires a durable `audit_store`; only an explicit `allow_unaudited_callback_mode=True` permits the legacy/test callback mode, and that cannot be used together with session auth. Requests use request-level serialisation and an exactly shared PostgreSQL connection; audited domain writes are first staged with `commit=False` and then committed together with the audit append in the same transaction. Business failures first roll back mutations and then record DENIED (with null snapshots); when audit is unavailable it fails closed and returns a generic 500. All requests record an allowed/denied outcome; unmatched `/internal/v1` GET/HEAD and POST/PUT/PATCH/DELETE/OPTIONS/TRACE/CONNECT are all audited, with identity/permission/CSRF guards preserved.
- **Path privacy**: audited session mode requires an externally supplied 32-byte stable HMAC key. Events store only the route template and the sorted parameter-name HMAC-SHA256 full digest, not raw path/query; key rotation breaks cross-period correlation. The key provisioning/rotation policy has not been accepted.
- **Transaction boundaries**: ChangeOrder, Distribution and ManagedRule proposal activation snapshots cover before/after (including tombstones). The Distribution completion/report audit tx1 and the ManagedRule+ChangeOrder APPLIED/audit tx2 are two PostgreSQL transactions and provide no cross-transaction/distributed atomicity; an audit failure rolls back the transaction it belongs to.
- **The last fully green gate at the M4b-6b stage (historical snapshot)**: `make gate` at the time gave Ruff format **225 files already formatted**; Ruff clean; mypy **45 source files clean**; pytest `-m "unit or contract"` **767 passed, 2 skipped, 131 deselected**, with 11 non-failing Starlette/httpx deprecation warnings. The full config-service integration-marker command on PostgreSQL **12.22** gave **122 passed, 3 skipped, 404 deselected**, with 5 deprecation warnings; 3 publication DDL integration tests skipped because the server uses `wal_level=replica` (the test requires `logical`). The final affected test matrix was **264 passed, 3 skipped, 15 warnings**; the API/audit catchall subset was **89 passed, 15 warnings**. All local results, not remote verification; PostgreSQL 16 was not tested. The above counts are 6b stage evidence, not the current M4b-7 verification.
- **Review and remaining items**: the final independent integrated API/store review had no actionable findings after the fixes; the maintainer signature has been recorded (2026-10-04), see [`m4b-6b-audit-integration-review-2026-10-02.md`](../reviews/m4b-6b-audit-integration-review-2026-10-02.md). M4b-7/8 engineering evidence has progressed; overall REQ/M4 acceptance is still unclaimed; application rate limiting, browser login UI, MFA/SSO, deployed ingress/trusted-proxy proof and PG16 all lack evidence. REQ-S-4, M4b and M4 are all unaccepted.

## M4b-7 Live-read/session shell (2026-10-03; engineering evidence, NOT M4b/REQ ACCEPTANCE)

This section records the M4b-7 read/session shell, ASGI static asset serving/packaging, and the existing ChangeOrder submit/approve/reject engineering slice; the other M4b-7 deployment/operation-flow sub-items and M4b-8 all remain OPEN and constitute neither M4b/M4 nor any REQ acceptance.

- **Refreshed config-service PostgreSQL integration (2026-10-03)**: on the same local PostgreSQL **12.22** as before, after the current API/bootstrap changes the full integration marker run is **122 passed, 3 skipped, 432 deselected, 5 warnings**. The three skips are the publication DDL tests requiring `wal_level=logical`; the current server uses `replica`. Local results, local run only; PG16 untested. This marker run does not cover the integration deployment path where the runtime factory uses DB-backed roles, and does not prove deployed HTTPS ingress or browser operation flows; those remain bound by the 7.2d and 7.6/M4b-8 boundaries respectively. This is the refreshed M4b-7 integration evidence; the **404 deselected** of M4b-6b below is retained as that stage's historical report and is not rewritten.

- **Implemented**: the console supports session restore/login/logout via the same-origin `/internal/v1` (logout uses CSRF), and reads live managed rules and change orders. `?preview=1` keeps the local fixtures; live mode does not fall back to fixtures. Trace and operations explicitly show unavailable.
- **Live existing-order decisions (engineering slice only)**: the live table/modal allows the creator of an existing draft to submit, and a different approver to approve or reject the submitted ChangeOrder. The UI affordance checks the role and the creator, URL-encodes IDs, sends CSRF and re-reads server state after the operation; it offers no rule CRUD/create/edit/write, and no distribution start/reports/rollback UI.
- **Mock-browser evidence only**: a route-mocked submit sends a bodyless `POST /change-orders/{id}/submit` and a CSRF header, and a subsequent reload shows submitted; the creator then sees Details. After a route-mocked approver approve, a reload shows approved. An empty reject sends no request; a valid reason POSTs `{reason}` with CSRF, and a reload shows rejected. These are mock route checks, not real API/DB-backed/browser integration.
- **API self-rejection regression**: the reject endpoint rejects the creator's self-rejection with 403 before the transition/append; the regression asserts the order stays SUBMITTED with no append. Three sibling API tests (creator self-reject, creator self-approve, rejection reason and trimmed audit) give **3 passed, 1 warning** with `uv run pytest -q`. The independent code review of that fix had no actionable findings; this result does not represent acceptance.
- **Current M4b-7 validation summary**: running `make gate` directly is blocked at the first step `ruff format --check .` by formatting differences in untracked, unrelated `testbed/simulators/resip-probe/research/` Python files, so it cannot be reported as passing; after excluding that path, the final scoped validation `uv run ruff format --check --exclude 'testbed/simulators/resip-probe/research/**' .` reports **228 files already formatted**, `uv run ruff check --exclude 'testbed/simulators/resip-probe/research/**' .` passes fully, `uv run mypy` is **46 sources clean**, and `uv run pytest -m 'unit or contract' -q` is **795 passed, 2 skipped, 131 deselected, 11 warnings**. Focused runtime tests are **20 passed** and bootstrap admin tests **6 passed**. The current config-service PostgreSQL 12.22 integration is **122 passed, 3 skipped, 432 deselected, 5 warnings**; the 3 publication DDL tests require `wal_level=logical` and skip because this machine is `replica`. That suite does not cover the runtime-factory DB-backed-roles deployment path, deployed HTTPS ingress or browser operation flows. The above is local verification, local run only; the M4b-6b gate and integration counts remain historical stage evidence; M4b/M4/REQ acceptance remains unclaimed.
- **ASGI static hosting/package engineering slice**: config-service `create_app` serves the packaged console assets from `/` after all `/internal/v1` routers; at source runtime it falls back to `services/console/web`. The `as-console` wheel force-includes `index.html`, `console.js` and `console.css`. This only verifies ASGI app/TestClient routing and the package contents.
- **Runtime factory/CLI engineering slice (2026-10-03)**: config-service provides `as_config_service.runtime:create_runtime_app` and the `as-config-service` command. The runtime factory strictly reads `AS_CONFIG_DSN`, `AS_CONFIG_RUNTIME_ROLE` and `AS_AUDIT_RESOURCE_HMAC_KEY_B64`, establishes exactly one connection, runs `SET ROLE` first and then constructs the stores that share that connection, and relies on audit store startup validation; it performs no schema creation, migration or role provisioning. The bootstrap CLI separately requires `AS_CONFIG_OWNER_DSN` and shares `AS_CONFIG_SCHEMA`; the owner DSN is only for bootstrap and is not the runtime login. Focused fake-connection runtime tests verify that configuration failure precedes connection, the shared connection/order and construction-failure cleanup; bootstrap admin tests **6 passed**. This is a code-level engineering slice, not production deployment or acceptance evidence.
- **Config-service image/Helm wiring engineering slice (2026-10-03)**: a separate root-context Dockerfile is added; `as-config-service` declares the `as-platform` workspace dependency directly so the isolated image can install its API contract import. Helm gains a non-root Deployment that is off by default, a ClusterIP Service, and an optional `networking.k8s.io/v1` Ingress template; the template only supports ingress-nginx, fails closed when enabled by requiring the class to be `nginx`, and pins `ssl-redirect` and `force-ssl-redirect` to `"true"`. The Deployment references `AS_CONFIG_DSN` and the audit HMAC key only from an external runtime Secret, and the runtime role must be provisioned in advance; startup performs no DDL/provisioning. The bootstrap owner DSN is not injected into the Deployment. The Ingress also requires a host/TLS Secret, proxy headers and an explicit non-wildcard trusted proxy list. The actual controller must keep the default `nginx.ingress.kubernetes.io` annotation prefix, and `no-tls-redirect-locations` must not exempt `/`; the chart cannot set or prove these controller-level conditions. Secrets are read only via key references, and both the console and the API are served by the same ASGI Service. 7.2c is template wiring only; there is no real HTTP→HTTPS redirect/rejection or browser credential transport proof, and it does not prove Helm render, image build, a real cluster, HTTPS, trusted-proxy behaviour or the browser operation flow.
- **Focused evidence and limitation for 7.2c/7.2d**: `uv lock --check` passed; `uv build --package as-config-service --wheel --out-dir /tmp/as-config-service-helm-wheel` succeeded; static PyYAML assertions parse `deploy/helm/values.yaml` and confirm that configService/Ingress are off by default, the external Secret name is unset, proxy headers are off and trusted proxies are empty. No Helm lint/template render was possible: the Helm CLI was absent; pulling `alpine/helm:3.16.4` failed on Docker Hub DNS, and the configured mirror attempt was denied by Cloudflare. The dedicated Docker image build could not fetch its Dockerfile frontend because registry access failed. There is no rendered-chart or image-build proof. 7.2c is ingress-nginx HTTPS redirect template wiring only; Helm render, image build, cluster, HTTPS, trusted-proxy and browser proof remain open under 7.2d. These are engineering-slice checks only, not M4b/M4 or REQ acceptance.
- **Engineering verification**: `uv run pytest -q services/config-service/tests/test_api.py`: **74 passed, 11 warnings**. `uv build --package as-console --wheel --out-dir /tmp/as-console-wheel` succeeded; `unzip -l` confirms the wheel contains the three assets above. The earlier `node --check services/console/web/console.js`, the browser preview and the route-mocked live checks remain engineering evidence within their own scopes. The independent reviewer had no actionable findings.
- **Unverified and blocked**: the above API TestClient/package checks do not verify real DB-backed browser auth/session; local run only. The code-level ASGI factory/CLI and Helm wiring exist, but there is no evidence of production HTTPS ingress, TLS termination or deployed trusted-proxy behaviour; scheme trust and same-origin HTTPS deployment still have to be verified (now tracked as M4b-7.2d). The Ingress template's ingress-nginx redirect wiring still has no Helm render or cluster behaviour proof. A standalone Python `http.server` is still only for `?preview=1` static preview and provides no API. ManagedRule create/edit/enable/delete remain blocked by the runtime contract lossless mapping, the bundle compiler and regex semantics; a placeholder/empty ConfigBundle must not be sent. Live distribution actions, the trace source/API, and the AS instance inventory, notification transport and health collector are also missing. Route-mocked browser checks do not prove real API/database/browser integration or fleet delivery; M4b-7.3b–7.6 and M4b-8 remain OPEN, and all M4b/M4/REQ acceptance is unclaimed.

## M4b-7.2c2 Owner-only database setup (2026-10-03; engineering evidence, NOT M4b/M4/REQ ACCEPTANCE)

This focused suite is **39 passed**: migration **8**, runtime **24**, bootstrap admin **7**; this result supersedes the older focused runtime/bootstrap counts in the M4b-7 summary above in this report.

A new manual `as-config-migrate` owner-only CLI initialises the config/audit schema and least-privilege grants before bootstrap and web runtime deployment. It uses only `AS_CONFIG_OWNER_DSN`, verifies that `AS_CONFIG_SCHEMA` (default `as_config`) is owned by the current owner, calls the managed-rule/change-order/distribution/auth stores' `ensure_schema()` and `PostgresAuditStore.ensure_schema(runtime_role)`, then revokes the existing schema/table/sequence/column privileges of `PUBLIC` and the runtime role on the dedicated config schema, and grants only schema `USAGE`, the SELECT/INSERT the stores need, column-limited UPDATE and the bootstrap singleton SELECT. Audit grants are managed entirely by the audit store.

The database login/runtime roles must be created in advance by the DBA; the runtime role must be NOLOGIN, not a superuser, have no CREATEROLE and have no role memberships. The migration performs no CREATE/ALTER ROLE or `SET ROLE`, grants the runtime no `CREATE`, `DELETE` or `TRUNCATE`, and deletes no data. Runtime and bootstrap default to the same non-public `as_config` schema; the runtime app still does no DDL. The owner DSN is a manual-operation credential and never enters Helm values/Secrets or the web Pod.

- **Focused unit evidence**: `uv run --directory services/config-service pytest tests/test_migrate.py tests/test_runtime.py tests/test_bootstrap_admin.py -q`: **39 passed**. The migration tests use fake connection/store factories with no real database credentials; they cover fail-before-connect configuration, public/equal schema rejection, ensure call order, limited grants, failure rollback/close and DSN errors not leaking.
- **Acceptance boundary**: the full `make gate`, Helm lint/template/render, image build and database deployment verification were not run. This code-level slice does not prove actual PostgreSQL permissions/deployment and does not change the OPEN status of 7.2d Helm render/HTTPS ingress/trusted-proxy/browser proof; M4b/M4 and all REQ acceptance still have not passed.

## M4b-7.5 Console fleet inventory UI (2026-10-03; engineering evidence, NOT M4b/M4/REQ ACCEPTANCE)

This section records the live fleet inventory CRUD engineering slice under the Operations view; the backend PG `as_instances` inventory, distribution notify and testbed health probe were delivered in the prior 7.5 API/store slice. It **does not** claim REQ-F-15/M4 acceptance, real AS stack supplementary testing or a distribution UI.

- **Console UI**: in live mode the Operations view lists `/internal/v1/as-instances`; approver/admin can POST/PUT/DELETE (including enable/disable, notify URL and health URL) and uses the same-origin session + `X-CSRF-Token` write path; read-only sessions can GET the list. `?preview=1` still uses the fixture table and does not call the API.
- **API routes**: `GET/POST /internal/v1/as-instances` and `GET/PUT/DELETE /internal/v1/as-instances/{instance_id}` are available in `api.py` when an inventory store is injected.
- **Focused tests**: `node --check services/console/web/console.js`; `uv run --directory services/config-service pytest tests/test_fleet_api.py -q` (including list/create/update inventory regressions).
- **PostgreSQL integration (maintainer environment)**: `uv run pytest -m integration services/config-service/tests/test_postgres_as_instance_store_integration.py -q` (temporary PG 12.22; PG16 untested). This marker run does not prove browser operation flows or AS full-stack notify/health supplementary testing.
- **Distribution UI (7.6 slice)**: live **start / batch report / rollback** inside the change-order review modal (`console.js`); still not full M4b-8 or REQ-F-15 acceptance.

## M4b-7.6 Distribution console UI (2026-10-03; engineering slice, NOT M4b/M4/REQ ACCEPTANCE)

- **UI**: an approved / distributing change order → the Review dialog → Fleet rollout (plan version, batch layout, start, report current batch healthy, rollback).
- **API**: `POST/GET .../distribution`, `POST .../reports`, `POST .../rollback` (consistent with `test_fleet_api.py` / PG pipeline integration).
- **Prerequisites**: Operations registers an enabled instance; when the health URL is configured correctly the batch report triggers a server-side probe.
- **Evidence**: `node --check services/console/web/console.js`; `make gate`; browser HTTPS evidence still belongs to the M4b-8 section.

## M6 capacity harness smoke (2026-10-04; engineering evidence, NOT M6/O1 ACCEPTANCE)

This section records one smoke-level cascade of M6 step 2: `as_load` real UDP sockets with the native reSIProcate `resip_probe` external UAS. It is **not** a capacity measurement, **does not** publish an O1 figure, and **does not** constitute M6 closure or REQ acceptance; D8 remains open.

| Item | Content |
|---|---|
| System under test | reSIProcate 1.14.0 @ `632e215c`; `resip_probe --external S1` (native DUM UAS, dynamic UDP port) |
| Harness | `stack=resip-probe`, `stack-version=1.14.0-632e215c` |
| Reproduction (script) | repository root: `bash testbed/load/scripts/m6-resip-probe-smoke.sh` (requires an already-built probe: `make m2-native-build` or `AS_RESIP_PROBE_BIN`) |
| Reproduction (pytest) | `uv run pytest testbed/load/tests/test_resip_probe_smoke.py -m integration -q` (skips if the probe is missing) |
| Review | [`m6-resip-probe-smoke-review-2026-10-04.md`](../reviews/m6-resip-probe-smoke-review-2026-10-04.md): engineering slice **Pass**; the maintainer signature is pending |

**Boundary**: a single loopback call, no target-side CPU/FD/queue telemetry, no saturation-point observation; the SIPp 3.6.0 smoke remains only generic UAS interoperability evidence, sitting alongside this selected-stack smoke, and neither may be used to infer CPS/concurrency/latency limits.

## M4b-8 Dev HTTPS same-origin stack (runbook + engineering; NOT signed acceptance)

| Item | Status |
|---|---|
| Compose stack | `deploy/compose/README.md` |
| Runbook | [`m4b-8-runbook.md`](m4b-8-runbook.md) |
| Rule scope | **callee+prefix** ([`m4-req-calling-regex-lossless-adjudication-2026-10-03.md`](../reviews/m4-req-calling-regex-lossless-adjudication-2026-10-03.md)) |
| Artifact directory | [`artifacts/m4b-8/README.md`](../../artifacts/m4b-8/README.md) |
| Redacted material path | [`artifacts/m4b-8/2026-10-03/`](../../artifacts/m4b-8/2026-10-03/) (Playwright screenshots + `runbook-checklist.md` + `browser-evidence-log.json`) |
| Reproduction command | `M4B8_E2E_PASSWORD='<dev-only>' deploy/compose/scripts/m4b-8-browser-evidence.sh` |
| Git commit | `1bca9eee74c090964d48a217abfe41bfcdf73dab` (`cur`, message: m4 close) |
| **Maintainer signature** | **Approved** (2026-10-04; chat-authorised AI proxy-signature) — the material under the above paths has been reviewed and the runbook's PASS/FAIL/BLOCKED/N/A is accepted as consistent with the 10-03 closure ruling; this **does not** mean REQ-F-13, 7.2d or the F-15 real AS supplementary testing has passed |
| Automated smoke (2026-10-03) | compose on this machine: after `postgres:12.22` + `up.sh`, `./scripts/smoke-https.sh` is **OK** (the host's `HTTP(S)_PROXY` needs `--noproxy` to reach localhost, which the script already handles) |
| Compose PG integration (2026-10-03) | `AS_PG_TEST_DSN=postgresql://postgres:postgres@127.0.0.1:55432/as_config uv run pytest -m integration -q services/config-service/tests` → **136 passed, 3 skipped** (`wal_level` publication skipped) |
| Playwright browser evidence (2026-10-03) | the same compose stack; headless Chromium; same-origin API sampling is in the artifact log |

**M4b-8 steps N/A / BLOCKED**: step 3 (F-13 trace); 7.2d production preflight (M5); v1.1 caller/regex; F-15 real AS stack supplementary testing (deferred by ruling).
