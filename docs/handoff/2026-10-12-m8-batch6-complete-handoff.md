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

# M8 Batch 6 "Documentation and Reports" Completion Handoff (2026-10-12)

## 0. Nature and Boundaries of This Document

This is the M8 batch 6 completion handoff. Batch 6 is the **final batch** of the six-batch split of M8 and depends on the output of batches 1–5; the accompanying review record is `docs/reviews/m8-batch6-docs-report-review-2026-10-12.md`.

- **Positioning of this version**: internal version — functionally complete + simulator evidence + reproducible build artifacts. **Not the M8 exit sign-off**; it does not constitute a release.
- **This batch signs off no REQ**, does not change matrix status (the matrix final state is landed by the batch 4 counter-signature section), **does not change `docs/plan.md`**, and does not change `VERSION` / `CHANGELOG.md`.
- **No claim that M8 is fully green, no claim that a release has been made**; "internal version wrap-up complete" ≠ "M8 exit sign-off".
- **Execution environment**: `dev-win03ib7niepf0` (already registered in `docs/environments.md`).
- **No git write operation was performed**; all changes remain in the working tree for the maintainer to split into commits.

## 1. Completion List (6/6) and Triples

| Item | Landing file | Triple (conclusion, evidence, date) |
|---|---|---|
| **E-1** Count synchronization | `docs/acceptance/report.md` +35 lines (internal version header 6 lines + 29 lines in §0.10 "count synchronization and internal version wrap-up statement") | (verified, `docs/acceptance/report.md` §0.10, 2026-10-13) |
| **E-2** Version and change log | `VERSION` = `0.2.0`; the `[0.2.0]` section of `CHANGELOG.md` already contains a `### Internal build (2026-10-12)` subsection | (confirmed, **unchanged**, `VERSION` / `CHANGELOG.md`, 2026-10-12) |
| **E-3** `plan.md` §0 / §4 M8 row | `docs/acceptance/m8-plan-m8-row-draft-2026-10-12.md` (36 lines) | (**draft only**, `docs/plan.md` unchanged, `docs/acceptance/m8-plan-m8-row-draft-2026-10-12.md`, 2026-10-12) |
| **E-4** Internal version wrap-up review | `docs/reviews/m8-internal-release-exit-review-2026-10-12.md` (113 lines) | (verified, `docs/reviews/m8-internal-release-exit-review-2026-10-12.md`, 2026-10-12) |
| **E-5** Milestone exit review append | `docs/reviews/m8-exit-review-2026-10-06.md` §3.2 (+19 lines) | (verified, `docs/reviews/m8-exit-review-2026-10-06.md` §3.2, 2026-10-12) |
| **E-6** Packaging re-check | `docs/acceptance/artifacts/m5/2026-10-12/PASS-e6-packaging-recheck-2026-10-12.txt` (74 lines) + index +1 line | (verified, `docs/acceptance/artifacts/m5/2026-10-12/PASS-e6-packaging-recheck-2026-10-12.txt`, 2026-10-12) |

- E-2 note: `VERSION` has been adjudicated as not bumped and stays `0.2.0`; the internal build subsection of `CHANGELOG.md` already exists (containing four items: "this is an internal version, not a release", the image tag format, chart not synchronized, and this version's positioning), so **nothing is appended again**.
- E-3 note: the draft contains three suggestions (§0 current in-progress step cell append sentence, §0 product decision record new row, §4 M8 row status column suggested value) plus boundaries; **`docs/plan.md` was not modified**, and the final wording is confirmed by the maintainer.

## 2. Summary of Key Results

- **report.md count synchronization**: current values **pass 27 / defer 4 / blocked 9 / n-a 9 / open 0 / fail 0, 49 rows in total** (basis = section 4 of the "M8 batch 4 finalization counter-signature (2026-10-13)" section of `docs/acceptance/m8-test-plan-matrix.md`). The 2026-10-06 historical values in the original §0.5 text (pass 9 / fail 0 / blocked 12 / n-a 4 / open 24) are **retained unchanged**, handled in the "keep the original text, append a correction" manner. The entire `pass` basis is "**engineering evidence accepted**", counter-signed by the agent (maintainer authorization), **not the maintainer's own signature**.
- **The M8 row is not signed off**: in **§3.2** of `docs/reviews/m8-exit-review-2026-10-06.md`, **M8 status = "internal version, not signed off", signature = "unsigned — pending maintainer signature"**; M1/M2/M6/M7 keep "engineering complete (counter-signed by agent, maintainer authorization 2026-10-12)".
- **Eight measured items in E-6**: version consistency, evidence discipline guard, `make gate`, image rebuild, sanitization re-check, SIP listening runtime, Helm reproducible rendering, environment variable item-by-item check — **six passed + one deviation** (the image digest differs from batch 1; the new digest `sha256:63ba8f4df78d5853e70451cc0e2a12e691f2c38facc800e2135d71c7018ecfdb` was recorded as planned; the difference is at the manifest layer: buildx v0.31.1 produced a manifest list with attestation this time, and `{{.Id}}` takes the manifest list digest; the CACHED status of each layer shows the layer contents are unchanged. **We do not claim a content change, and we do not claim byte-for-byte identity with batch 1**).
- **16 environment variables checked item by item with no drift**: the implementation side `platform/src/as_platform/` (with `runtime/transport_env.py` as the main entry point) reads 16 in total from `AS_SIP_*` / `AS_TLS_*` / `AS_PEER_*`; coverage `platform/README.md` 16/16, `docs/operations/runbook-l2.md` 3/16, `docs/delivery/install-guide.md` 1/16, root `README.md` 0/16. The reverse check shows that the `AS_SIP_NEXT_HOP` / `_PORT` / `_TLS_PORT` appearing in the documentation are not in `platform/src` but are implemented in `apps/translation/src/as_translation/outbound.py:44/:48/:50`, so **this is not drift and not a wrong name**. The missing env table in the root `README.md` is a pre-existing documentation gap (non-blocking, registered in §0.7 of `report.md`); this batch does not fill it.

## 3. List of Changed Files (8 files in this batch, corresponding to the six items E-1~E-6; all uncommitted)

| File | Change |
|---|---|
| `docs/acceptance/artifacts/m5/2026-10-12/PASS-e6-packaging-recheck-2026-10-12.txt` | **New** 74-line evidence file (E-6) |
| `docs/reviews/m8-internal-release-exit-review-2026-10-12.md` | **New** 113 lines (E-4) |
| `docs/acceptance/m8-plan-m8-row-draft-2026-10-12.md` | **New** 36-line draft (E-3; `docs/plan.md` **unchanged**) |
| `docs/reviews/m8-batch6-docs-report-review-2026-10-12.md` | **New** review record |
| `docs/handoff/2026-10-12-m8-batch6-complete-handoff.md` | **New** handoff (this document) |
| `docs/acceptance/report.md` | **Appended +35 lines** (header 6 + §0.10 twenty-nine), pure append with zero deletions (E-1) |
| `docs/reviews/m8-exit-review-2026-10-06.md` | **Appended +19 lines** (§3.2) (E-5) |
| `docs/acceptance/artifacts/m5/README.md` | **Appended +1 line** of index (E-6 evidence registration) |

**Not part of this batch; do not mix into this batch's commit** (this batch's agent did not touch the following four):

- `.dockerignore` — leftover change from batch 1.
- `.gitignore` and `docs/intro.md` — the maintainer's own changes.
- `.codebuddy/teams/...` — an untracked IDE directory.

**Observation**: the batch's files listed above were in a **staged** state when verified (`git status --short` shows `A` / `M` in the first column). This batch's agent **performed no git write operation**, and that staged state **was not produced by this batch** (there are concurrent maintainer changes in the same working tree). The commit split is decided by the maintainer.

## 4. Verification Results

Execution environment `dev-win03ib7niepf0`.

| Item | Command | Result |
|---|---|---|
| Gate | `make gate` | `1174 passed, 249 deselected, 11 warnings`, four steps exit 0 |
| Version consistency guard | `uv run pytest tests/test_version_consistency.py -q` | `9 passed`, exit 0 |
| Evidence discipline guard | `uv run pytest tests/test_evidence_discipline.py -q` | `137 passed` after adding the new evidence (`135 passed` when E-6 was executed; the +2 comes from the new evidence increasing the root guard's parameterized cases, which is expected) |
| Helm reproducible rendering | `make chart-check` (`tools/bin/helm` 3.16.4) | `chart-check: OK` |
| Image rebuild | `docker build -t as-platform:0.2.0-internal-20261012 -f deploy/docker/Dockerfile .` | exit 0 (all steps CACHED, 2.5s) |
| Sanitization re-check | `find /app` + `grep -ri password\|passwd\|secret` inside the image | No sensitive files, no password-bearing logs → PASS |
| SIP listening runtime | `docker run --rm -e AS_SIP_ACCEPT_ALL_INVITES=1 -e AS_SIP_UDP_PORT=5060 …` | `RESIP_RUNTIME_LISTENING address=127.0.0.1 advertised=127.0.0.1 udp_port=5060` |

> **Note on self-incrementing counts**: the root guard is parameterized by evidence file, so adding evidence makes the counts self-increment. When E-6 was executed, `make gate` = `1174 passed, 249 deselected` and `tests/test_evidence_discipline.py` = `135 passed`; after this batch added `PASS-e6-packaging-recheck-2026-10-12.txt`, the wrap-up re-run gives `make gate` = `1176 passed, 249 deselected` (exit 0), `tests/test_evidence_discipline.py` = `137 passed`, `tests/test_version_consistency.py` = `9 passed`. **The evidence file retains the snapshot from execution time**; the numbers are not retroactively edited.

## 5. Items Pending the Maintainer

1. **Final wording confirmation for the `docs/plan.md` §0 / §4 M8 row** — the draft is at `docs/acceptance/m8-plan-m8-row-draft-2026-10-12.md` (this batch did not change `plan.md`).
2. **Scheduling of external hard dependencies or written risk acceptance** — D-1 (carrier PKI + external-network S-SBC), D-2 (customer K8s), the ADR-0008 cross-site drill, D12/O5 production HA.
3. **v1.1 initiation for the 4 `defer` rows (F-5 / F-8 / F-9 / F-11) and the F-13 / NF-7 call traces**.
4. **Image digest basis** — whether to unify the buildx build method to reproduce the digest shape of batch 1 (`sha256:8f2e1b9465d96a8cb7b9cab286e687a52621f136b570f521df15f6f9112da7c8`), or to accept in writing the new basis of "the manifest list digest governs".
   (**Adjudicated 2026-10-13: option ② chosen**, accepting in writing the new manifest list digest basis; the build is not re-run)
5. **Whether to fill the environment variable table gap in the root `README.md`** — currently 0/16 coverage, non-blocking, registered in §0.7 of `report.md`.
6. **The M8 exit sign-off is still deferred** — this batch only completed the internal version wrap-up and did not sign M8.
   (**Handled on 2026-10-13 via path C**: the M8 exit sign-off is signed off by the maintainer, including written acceptance of external hard dependency risk; the signature block awaits their personal signature, see §3.3 of `docs/reviews/m8-exit-review-2026-10-06.md`)
7. **Commit split and tag** — executed only by the maintainer (`AGENT.md` §10.4); no tag for the internal version.

> **Destination pointer (appended 2026-10-13; the original text of the seven items above is retained unchanged)**: the destinations of the items in this section that are not yet closed are —
> **Item 1**: whether the final wording draft for the `docs/plan.md` §0 / §4 M8 row is merged →
> [`../next-release-v1.1-plan.md`](../next-release-v1.1-plan.md) **§5-3** (draft carrier = `docs/acceptance/m8-plan-m8-row-draft-2026-10-12.md`, to be merged after the maintainer confirms the wording);
> **Item 2**: scheduling of the four external hard dependencies (D-1 / D-2 / ADR-0008 drill / D12-O5) — the risk has been accepted in writing via path C and they stay
> `blocked` and carry over to the next release → same document **§2** (restart = separate maintainer adjudication + external resources in place; deferred ≠ cancelled);
> **Item 3**: v1.1 initiation for the 4 `defer` rows (F-5 / F-8 / F-9 / F-11) and the F-13 / NF-7 call traces → same document **§3 rows 1–5**;
> **Item 6**: the M8 exit signature block is now **counter-signed by agent (maintainer authorization 2026-10-13)**, **not the maintainer's own signature** → same document **§7-1**;
> **Item 7**: commit split and tag (executed only by the maintainer) → same document **§5-6**.
> Subsequent status reviews, reports, handoffs, and new session openings that touch the leftover items in this section always **cite only that pointer**, do not itemize, and no longer list them as "actions for the maintainer".

## 6. Discipline Compliance Statement

- The main agent did not write any repository file directly; only one writing subagent existed at a time in this working tree, and the two writers were **serial** (this one started only after the previous one closed).
- **No git write operation was performed** (no add / commit / tag / push / branch / remote change / stash); all changes remain in the working tree.
- No code changes, no matrix status changes, no `docs/plan.md` changes, no `VERSION` / `CHANGELOG.md` changes.
- **No REQ is signed off and the M8 milestone signature is not signed**; no claim that M8 is fully green, no claim that a release has been made.
- Evidence contains no credentials / tokens / DSNs / cookies; the sanitization re-check has confirmed no sensitive files or password-bearing logs inside the image.
- Triples and environment names are complete: evidence always reads `(conclusion, evidence file, date)`, the environment name is always `dev-win03ib7niepf0`, and no anonymous "this machine" ever appears.
- The existing numbering system is reused (E-1~E-6, N2/N3/N4, D4-01…, B5-04, O1/O4/O5, D1~D12, G1–G8); no new numbering was invented.
