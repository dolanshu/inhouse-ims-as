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

# M8 Batch 4 "Sign-off and Review" Completion Handoff (2026-10-12)

## 0. Nature and Scope of This Document

This is the M8 Batch 4 completion handoff, paired review record: `docs/reviews/m8-batch4-signoff-review-2026-10-12.md`; paired matrix finalization draft: `docs/acceptance/m8-matrix-finalization-draft-2026-10-12.md`.

- **It signs off no REQ, changes no matrix state, and changes no `report.md` counts** — all 7 pass recommendations are marked "awaiting maintainer M8 exit review confirmation".
- "Engineering evidence accepted" ≠ REQ-level acceptance passed ≠ milestone sign-off; M5 at REQ level remains not passing, and M8 remains "RC-ready, awaiting exit signature".
- Execution environment: `dev-win03ib7niepf0` (internal compose PostgreSQL for audit re-verification, container `as-m4b8-dev-postgres-1`, DSN `127.0.0.1:55432`, password masked).
- No git write operation was performed; all changes remain in the work tree, and the maintainer splits them into commits.

## 1. Completion Checklist and Triples

| Item | Triple (verdict, evidence, date) |
| --- | --- |
| S-1 whitelist rejection scenario supplementary tests (9 unit) | (verified-rejection-scenarios-only, docs/acceptance/artifacts/m5/2026-10-12/PASS-s1-whitelist-rejection-2026-10-12.txt, 2026-10-12) |
| S-1 evidence collection for "whitelist change takes effect after approval" | (capability-does-not-exist-registered, docs/acceptance/artifacts/m5/2026-10-12/FAILCLOSED-s1-whitelist-change-approval-not-wired-2026-10-12.txt, 2026-10-12) |
| S-4 audit append-only (real PG re-run + 7 structural assertion units) | (verified, docs/acceptance/artifacts/m5/2026-10-12/PASS-s4-audit-append-only-2026-10-12.txt, 2026-10-12) |
| S-4 RBAC permission matrix (22 HTTP boundary integrations) | (verified, docs/acceptance/artifacts/m5/2026-10-12/PASS-s4-rbac-permission-matrix-2026-10-12.txt, 2026-10-12) |
| Row-by-row finalization draft for the matrix's 17 open rows (7 pass / 10 defer, all awaiting maintainer confirmation) | (draft-awaiting-approval, docs/acceptance/m8-matrix-finalization-draft-2026-10-12.md, 2026-10-12) |

## 2. Summary of Key Results

- **S-1 rejection scenario supplementary tests passed**: added `platform/tests/test_req_s1_whitelist_rejection.py` (9 unit, included in `make gate`), driving the real `ResipRuntimeListener._on_invite`, pinning the six return paths of **403**: whitelist miss / empty policy (fail-closed) / certificate mismatch / endpoint port mismatch / outside CIDR / plaintext UDP-when-TLS-required, and using a `received_at` probe to positively assert that `decide()` was not executed. During the supplementary tests, **faithfully discovered** that the address and certificate dimensions of `authorize_peer` are **OR** (an address hit lets it through, no peer certificate required); this has been pinned and annotated as **not constituting an mTLS strict-verification endorsement** (raised as D4-02).
- **S-1 "change takes effect after approval" capability does not exist**: FAILCLOSED evidence — `ConfigBundle` (`platform/src/as_platform/api/contract.py:71`, fields :89-91) has only version/rules/toggles; the only approvable proposal type `ManagedRuleChange` (`services/config-service/src/as_config_service/change_order.py:68`) only covers rules; `gate.install` / `install_with_overlap` in `platform/src` have **no product call sites**; `load_transport_seam_from_env` is read only once at construction time in `sip_stack_service.py:126`/`:156` (= change Helm values + restart the Pod). **Furthermore, matrix body L86 "whitelist change goes through approval (linked with F-14)" conflicts with code facts**, so it is only registered, and the matrix is not modified (raised as D4-01). The agent **did not implement** this capability.
- **S-4 audit append-only**: re-ran `test_postgres_audit_store_integration.py` on real PostgreSQL (internal compose) → **35 passed / 3 skipped** (all 3 skips are the `wal_level=replica` PUBLICATION gate, **containing no** immutability guard) + added `test_req_s4_audit_immutability.py` with 7 structural assertions (row-level `BEFORE UPDATE OR DELETE` tgtype 27, statement-level `BEFORE TRUNCATE` tgtype 34, guard body `ERRCODE '23514'`, store has no mutation API and the set of public names is closed). **Structural assertion ≠ database-side measurement**; the latter is covered by the real PG integration.
- **S-4 RBAC permission matrix**: added `test_req_s4_rbac_api_matrix_integration.py` with 22 cases, advancing the matrix from kernel pure functions to **20 HTTP boundary cells** (read all 200; submit viewer-only 403; approve / rollback viewer+operator 403; manage_users admin-only 200), with each 403 precisely asserting the permission-denied detail to rule out false greens from CSRF / 404 / two-person-principle impostors; additionally verifies that unauthorized attempts land as **DENIED audit rows** (re-checked by direct DB access) and that the two-person principle is a separate column. Boundaries: each permission is probed with only one representative endpoint, privilege-violation trail is verified on only two cells, and external IAM / SSO and carrier PKI are out of scope.
- **Matrix finalization draft**: gives a recommended final state and rationale row by row for all 17 rows — **7 rows pass** (F-4, F-10, NF-2, NF-5, NF-9, NF-10, S-4), **all awaiting maintainer M8 exit review confirmation**; **10 rows defer** (F-5, F-8, F-9, F-11, F-16, NF-13, NF-14, NF-15, S-1, D12/O5-HA). If adopted wholesale: pass 17 → 24, defer 0 → 10, open 17 → 0, blocked 6 / n-a 9 / fail 0 unchanged. `defer` is a **newly introduced** status word in this draft and may only be used after maintainer confirmation (D4-03).

## 3. Changed File List (all landed, none committed)

| File | Change |
| --- | --- |
| `platform/tests/test_req_s1_whitelist_rejection.py` | new, 9 unit (S-1 rejection scenarios) |
| `services/config-service/tests/test_req_s4_audit_immutability.py` | new, 7 unit (audit immutability structural assertions) |
| `services/config-service/tests/test_req_s4_rbac_api_matrix_integration.py` | new, 22 integration (RBAC permission matrix HTTP boundary, real PG) |
| `docs/acceptance/artifacts/m5/2026-10-12/PASS-s1-whitelist-rejection-2026-10-12.txt` | new evidence |
| `docs/acceptance/artifacts/m5/2026-10-12/FAILCLOSED-s1-whitelist-change-approval-not-wired-2026-10-12.txt` | new evidence (**not pass evidence**) |
| `docs/acceptance/artifacts/m5/2026-10-12/PASS-s4-audit-append-only-2026-10-12.txt` | new evidence |
| `docs/acceptance/artifacts/m5/2026-10-12/PASS-s4-rbac-permission-matrix-2026-10-12.txt` | new evidence |
| `docs/acceptance/artifacts/m5/README.md` | index table +6 lines (batch 5's 4 lines + 2 S-1 lines + 2 S-4 lines); the FAILCLOSED line contains "not pass evidence" on the same line |
| `docs/acceptance/m8-matrix-finalization-draft-2026-10-12.md` | new matrix finalization draft |
| `docs/reviews/m8-batch4-signoff-review-2026-10-12.md` | new review record |
| `docs/handoff/2026-10-12-m8-batch4-complete-handoff.md` | this handoff, new |

**Left over from other batches (do not mix into this batch's commit)**: `.dockerignore` (batch 1), `deploy/helm/values-onprem.example.yaml` (batch 5), batch 5's four evidence files and its review / handoff, `docs/handoff/2026-10-12-m8-batch4-prompt.md` and `docs/handoff/2026-10-12-m8-batch6-prompt.md` (added by the maintainer, untracked).

**Unchanged**: `docs/acceptance/m8-test-plan-matrix.md`, `docs/acceptance/report.md`, `docs/plan.md`, `docs/environments.md`, any product code and existing tests.

## 4. Verification Results

Environment `dev-win03ib7niepf0`:

- `make gate` → **`1174 passed, 249 deselected, 11 warnings`, 0 skipped**, exit 0.
- `uv run pytest tests/test_evidence_discipline.py -q` → **`135 passed`**, exit 0 (127 before the supplementary tests; the +8 comes from the 4 new evidence files each triggering 2 parameterized guards).
- S-1 new tests → **9 passed**.
- S-4 unit → **7 passed**; S-4 integration → **22 passed** (real PostgreSQL `127.0.0.1:55432`, container `as-m4b8-dev-postgres-1`).
- Existing audit integration re-run → **35 passed, 3 skipped** (all 3 skips are the `wal_level=replica` PUBLICATION gate, containing no immutability guard).

## 5. Items Awaiting the Maintainer

1. **D4-01**: S-1 "whitelist change takes effect after approval" — choose one: ① bring it into the change order (belongs to a new v1.1 feature, not tracked in this version, and the row stays defer); ② revise the matrix L86 wording "whitelist change goes through approval (linked with F-14)", which conflicts with code facts (choosing ② lets the row flip to pass on the strength of the rejection-scenario supplementary test evidence).
2. **D4-02**: whether the whitelist `authorize_peer` address / certificate **OR** semantics should be tightened to AND (currently an address hit lets it through, no peer certificate required).
3. **D4-03**: whether to introduce the `defer` status word and whether to rewrite the matrix counts per draft §3 (pass 17→24 / defer 0→10 / open 17→0).
4. **D4-04**: whether the non-trace portion of F-16 may flip to pass using "2026-10-12 `make gate` 1174 passed + existing decide coverage at matrix L59" as engineering evidence.
5. **D4-05**: whether NF-15's scope should be narrowed to "harness landed + multi-replica measurement" and flipped to pass, or adjudicated together with batch 5 **B5-04**.
6. **D4-06**: whether F-5 (Record-Route product-side forwarding), F-9 (re-INVITE / UPDATE) and F-11 (CANCEL before any downstream response) become v1.1 tracked projects (following the three capability-gap registration documents, of which F-9 / F-11 each have a FAILCLOSED).
7. **D4-07**: confirm the 7 pass recommendations (F-4, F-10, NF-2, NF-5, NF-9, NF-10, S-4) row by row in the M8 exit review.
8. **Work tree commit split**: this batch (3 new tests + 4 evidence files + index +6 lines + draft / review / handoff) forms one group; batch 1's `.dockerignore`, batch 5's `values-onprem.example.yaml` and its evidence / review / handoff are handled separately.
9. **Batch 6 carry-over**: the `report.md` §0.5 counts **take this draft as their value basis** (`docs/handoff/2026-10-12-m8-batch6-prompt.md` E-1); until the draft is approved, batch 6 must not rewrite the counts first.

> **Destination pointer (added 2026-10-13; the original text of the nine maintainer items above is retained unchanged)**: the destinations of the items in this section that have not yet been closed are ——
> **Item 3**: whether the `defer` status word is kept long term (the word was landed via this batch's finalization delegated signature and annotated as "newly introduced this time") →
> [`../next-release-v1.1-plan.md`](../next-release-v1.1-plan.md) **§5-4**;
> **Item 6**: **the v1.1 tracked projects for F-5 (Record-Route) / F-9 (re-INVITE / UPDATE) / F-11 (CANCEL before any downstream response)** →
> the same document **§3 rows 1 / 3 / 4** (F-8 CANCEL three branches, listed alongside, is row 2);
> **Item 5**: NF-15 scope (to be adjudicated together with the measurement batch carrying per-pod utilization) → same document **§4-9**;
> **Item 8**: work tree commit split → same document **§5-6**.
> Any subsequent status inventory, report, handoff, or new-session opening that touches the leftovers of this section must **only cite this pointer**; do not expand them item by item and do not list them again as "maintainer actions".

## 6. Discipline Compliance Declaration

- The main agent wrote no repo file directly; all repo file changes were landed via a writing subagent and verified with `git status` / diff; only one writing subagent ran in the same work tree at any time.
- No git add / commit / tag / push / branch / remote change; no git write operation was performed.
- No matrix row state or "status statistics" was changed; no `report.md` §0.5 counts were changed; no product code or existing tests were changed.
- No REQ signed off, no milestone signed off; all pass recommendations are marked "awaiting maintainer M8 exit review confirmation".
- Rows that depend on an external environment (live collection and real triggering for NF-13 / NF-14, customer production topology for D12/O5-HA) are all deferred and were not force-tested; supplementary testing is limited to the engineering layer (unit / integration / structural assertions).
- Evidence files contain no credentials / tokens / cookies (the audit DSN password is masked as `***`); the environment name is always `dev-win03ib7niepf0`, and the anonymized "local machine" never appears.
- The new FAILCLOSED evidence is marked "not pass evidence" in the index `docs/acceptance/artifacts/m5/README.md`.

---

## 7. Delegated-Signature Execution Result (2026-10-13)

- **Authorization source**: the maintainer's own words on 2026-10-13, "**accept the recommendations, authorize you to sign on my behalf**".
- **Scope landed**: **three adjudications** (B5-04 = **(b)** written risk acceptance at the M8 final review; the S-1 either-or = **①** revise the matrix L86 description; whitelist address / certificate **OR** = **accepted in this version**) and the **17-row final state** have **all been landed**; landing point = the section "M8 Batch 4 Finalization Delegated Signature (2026-10-13)" in `docs/acceptance/m8-test-plan-matrix.md` (additive; the matrix body rows and the "status statistics" original text are unchanged).
- **Final counts**: **pass 27 / defer 4 / blocked 9 / n-a 9 / open 0 / fail 0** (`defer` is the status word newly introduced this time: F-5 / F-8 / F-9 / F-11; three rows registered as blocked due to restrictions: NF-13 / NF-14 / D12/O5-HA).
- **Newly changed files in this batch** (added on top of the §3 list of this document):
  | File | Change |
  | --- | --- |
  | `docs/acceptance/m8-test-plan-matrix.md` | **appended a section** "M8 Batch 4 Finalization Delegated Signature (2026-10-13)"; body and each "status statistics" section unchanged |
  | `docs/handoff/2026-10-12-m8-batch4-complete-handoff.md` | appended §7 of this document |
  | `docs/acceptance/m8-matrix-finalization-draft-2026-10-12.md` | appended §6 "Execution status (2026-10-13)", original text unchanged (the draft becomes an archive) |
  | `docs/reviews/m8-batch4-signoff-review-2026-10-12.md` | appended the section "Adjudication result (2026-10-13, maintainer has decided and authorized delegated signature)", original text unchanged |
- **The `docs/acceptance/report.md` §0.5 counts were left untouched**, deferred to batch 6 (**E-1**) which will execute per the above counts; the `docs/plan.md` M8 row write-back likewise belongs to batch 6 (**E-3**).
- **Nature of the signature**: all signature fields read "**agent delegated signature (authorized by the maintainer on 2026-10-13)**", not a personal maintainer signature; **the M8 milestone is still unsigned** (internal version, not signed off).
- **No git write operation was performed** (no add / commit / tag / push / branch / stash); all changes remain in the work tree, and the maintainer splits them into commits. Execution environment `dev-win03ib7niepf0`.
