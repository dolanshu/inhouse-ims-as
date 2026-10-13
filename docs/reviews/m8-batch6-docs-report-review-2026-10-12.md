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

# Review Record — M8 internal build batch 6: documentation and report

- **Review target**: batch 6 "documentation and report" outputs, six items E-1～E-6 in total
  - **E-1** count synchronization: `docs/acceptance/report.md` — appended an internal-build header (6 lines) + new section §0.10 "count synchronization and internal-build close-out statement" (29 lines), **+35 lines** in total, **pure append, zero deletions**; the original counts in §0.5 (pass 9 / fail 0 / blocked 12 / n-a 4 / open 24) are preserved as the 2026-10-06 historical values, and the current counts are governed by §0.10.
  - **E-2** version and change-record confirmation: `VERSION` / `CHANGELOG.md` — **confirmed only, unchanged**. `VERSION` = `0.2.0` (adjudicated not to bump); the `[0.2.0]` section of `CHANGELOG.md` already contains a `### Internal build (2026-10-12)` subsection (with four items: "this is an internal build, not a release", the image tag format, chart not synced, and this build's positioning), so it is **not appended again**.
  - **E-3** draft of the `docs/plan.md` §0 / §4 M8 rows: **draft only, `plan.md` not changed**. Draft `docs/acceptance/m8-plan-m8-row-draft-2026-10-12.md` (36 lines), containing three proposals (a sentence appended to the current in-progress step cell in §0, a new row in the §0 product decision record, a proposed status value for the §4 M8 row) and boundary notes.
  - **E-4** internal-build close-out review: `docs/reviews/m8-internal-release-exit-review-2026-10-12.md` — newly created, 113 lines. Its very first sentence is "**this document is an internal-build close-out review, not the M8 exit signature**"; it contains evidence triples for the six batches' completed items, 6 FAIL/FAILCLOSED gaps, 8 restriction statements, and a sign-off section (the M8 exit signature field = unsigned).
  - **E-5** append to the milestone exit review: `docs/reviews/m8-exit-review-2026-10-06.md` — §3.2 appended at the end (**+19 lines**). M1/M2/M6/M7 keep "engineering complete (agent proxy signature, maintainer authorization 2026-10-12)"; **M8 status = "internal build, not signed off", signature = "unsigned — pending maintainer signature"**.
  - **E-6** packaging re-check: new evidence `docs/acceptance/artifacts/m5/2026-10-12/PASS-e6-packaging-recheck-2026-10-12.txt` (74 lines); the index `docs/acceptance/artifacts/m5/README.md` **+1 line**.
- **Review date**: 2026-10-12 (execution date 2026-10-13)
- **Reviewer**: AI agent — **reviews and lists gaps only, does not sign**; all verdicts in this document are **reviewer recommendations** and may only be executed after maintainer confirmation
- **Basis of review scope**: the batch 6 prompt (the "documentation and report" batch of the M8 six-batch split); `AGENT.md` §3.3; upstream `docs/handoff/2026-10-12-m8-scope-revision-internal-release-plan.md`
- **Execution environment**: `dev-win03ib7niepf0` (already registered in `docs/environments.md`)

---

## Current Status

> This section reflects the as-landed state of this batch's engineering changes and the review conclusion.

- **One-line conclusion**: all six items (E-1～E-6) of batch 6 "documentation and report" **have landed**; the `report.md` counts are synchronized with the matrix terminal state (pass 27 / defer 4 / blocked 9 / n-a 9 / open 0 / fail 0, 49 rows in total), and the M8 milestone row explicitly reads "**internal build, not signed off**" — **internal-build close-out complete (conditional)**; this batch **signs off no REQ and does not sign the M8 exit signature**.
- **Gap statistics**: P0 = 0; P1 = 0; P2 = 0 (no blocking gaps at the engineering layer). **5 items await maintainer adjudication** (see the Gap list), all of which belong to the maintainer's adjudication domain, not engineering gaps.
- **Gate**: `make gate` → `1174 passed, 249 deselected, 11 warnings`, all four steps exit 0; `tests/test_version_consistency.py` → `9 passed`; `tests/test_evidence_discipline.py` → `137 passed` after adding the new evidence.
- **Sign-off state**: **unsigned — pending maintainer signature** (sign-off is the maintainer's action).
- **Unclosed items**: 5 items pending adjudication (① final wording of the `plan.md` M8 row; ② image digest inconsistent with batch 1; ③ environment variable table gap in the root `README.md`; ④ external hard dependencies and the 4 `defer` rows still awaiting scheduling or written risk acceptance; ⑤ the M8 exit signature still deferred), plus commit splitting and the tag (maintainer only).

---

## 1. Overall assessment

This batch is the last of the six batches; its nature is "close-out and alignment", not additional testing and not signature:

- **E-1 count synchronization**: adopted the "keep the original text unchanged, append the correction" approach, fully preserving the 2026-10-06 historical values in §0.5 and establishing the current values in a new §0.10, which states within the section the composition of the 27 `pass` rows (9 baseline + 7 N3 proxy signatures + 1 NF-4 + 10 batch 4) and that "all are agent proxy signatures, with the framing uniformly being engineering-evidence acceptance". **It makes no claim that M8 is fully green and no claim that a release has occurred**; the six boundary statements are written out one by one, which complies with the discipline.
- **E-2 version confirmation**: `VERSION` stays at `0.2.0`, and since `CHANGELOG.md` already has an internal build subsection it is not appended again — the judgement "confirmed only, unchanged" holds, avoiding the noise of "duplicate traces for the sake of traceability".
- **E-3 draft-only approach**: `plan.md` is a no-edit file; this batch only produced a draft as a separate document, put not a single character on `plan.md`, and the boundary is clear.
- **E-4 / E-5 wording discipline**: E-4 separates "internal-build close-out review" from "M8 exit signature" in its very first sentence; E-5 writes the M8 status as "internal build, not signed off" and the signature field as "unsigned — pending maintainer signature". Neither place contains any affirmative statement about full green or an exit signature.
- **E-6 packaging re-check**: all eight measurements (version consistency, evidence discipline guards, gate, image rebuild, desensitization re-check, SIP listener runtime, Helm reproducible rendering, item-by-item environment variable check) are backed by commands and raw output; the **deviation that the image digest differs from batch 1 is recorded faithfully with an attribution explanation** — claiming neither a content change nor byte-for-byte identity — which is the most commendable piece of honest handling in this batch.

---

## 2. Item-by-item check

| Item | Landing point | Triple (conclusion, evidence, date) | Conclusion |
|---|---|---|---|
| **E-1** | `docs/acceptance/report.md` +35 lines (header 6 + §0.10 twenty-nine) | (verified, `docs/acceptance/report.md` §0.10, 2026-10-13) | ✅ Pure append, zero deletions; §0.5 historical values preserved; current counts governed by §0.10 |
| **E-2** | `VERSION` / `CHANGELOG.md` | (confirmed-unchanged, `VERSION` = `0.2.0`; `CHANGELOG.md` `[0.2.0]` section `### Internal build (2026-10-12)`, 2026-10-12) | ✅ Confirmed only, unchanged; the internal build subsection already exists, not appended again |
| **E-3** | `docs/acceptance/m8-plan-m8-row-draft-2026-10-12.md` (36 lines) | (drafted-plan.md-unchanged, `docs/acceptance/m8-plan-m8-row-draft-2026-10-12.md`, 2026-10-12) | ✅ Draft only; `docs/plan.md` was not modified |
| **E-4** | `docs/reviews/m8-internal-release-exit-review-2026-10-12.md` (113 lines) | (verified, `docs/reviews/m8-internal-release-exit-review-2026-10-12.md`, 2026-10-12) | ✅ The very first sentence declares "not the M8 exit signature"; the M8 exit signature field = unsigned |
| **E-5** | `docs/reviews/m8-exit-review-2026-10-06.md` §3.2 (+19 lines) | (verified, `docs/reviews/m8-exit-review-2026-10-06.md` §3.2, 2026-10-12) | ✅ M8 = "internal build, not signed off", signature "unsigned — pending maintainer signature" |
| **E-6** | `docs/acceptance/artifacts/m5/2026-10-12/PASS-e6-packaging-recheck-2026-10-12.txt` (74 lines) + index +1 | (verified, `PASS-e6-packaging-recheck-2026-10-12.txt`, 2026-10-12) | ✅ Eight measurements passed; one deviation (image digest) recorded faithfully |

### 2.1 E-6 measurement detail

Execution environment `dev-win03ib7niepf0`, execution date 2026-10-13, evidence date 2026-10-12.

| Item | Command | Result |
|---|---|---|
| Version consistency | `uv run pytest tests/test_version_consistency.py -q` | `9 passed`, exit 0 |
| Evidence discipline guards | `uv run pytest tests/test_evidence_discipline.py -q` | `135 passed` when E-6 was executed; re-run after this batch added its evidence files gives `137 passed` (+2 comes from the new evidence files increasing the parameterized root-guard cases, **expected**) |
| Gate | `make gate` | All four steps exit 0; `1174 passed, 249 deselected, 11 warnings` |
| Image rebuild | `docker build -t as-platform:0.2.0-internal-20261012 -f deploy/docker/Dockerfile .` | exit 0, all steps CACHED (2.5s). New image id `sha256:63ba8f4df78d5853e70451cc0e2a12e691f2c38facc800e2135d71c7018ecfdb`; batch 1 recorded `sha256:8f2e1b9465d96a8cb7b9cab286e687a52621f136b570f521df15f6f9112da7c8` — **inconsistent; the new digest has been recorded as planned**. The difference occurs at the manifest layer (buildx v0.31.1 produced an attestations-carrying manifest list this time, and `{{.Id}}` takes the manifest list digest); the layers being CACHED means the layer content did not change. **It claims neither a content change nor byte-for-byte identity with batch 1** |
| Desensitization re-check | `find /app` inside the image for `*.pem/*.key/*.pcap/*.pcapng/*.crt/*.p12/*.jks` + `grep -ri password\|passwd\|secret /app --include='*.log'` | No sensitive files, no password-bearing logs → **PASS** |
| SIP listener runtime | `docker run --rm -e AS_SIP_ACCEPT_ALL_INVITES=1 -e AS_SIP_UDP_PORT=5060 as-platform:0.2.0-internal-20261012` | `RESIP_RUNTIME_LISTENING address=127.0.0.1 advertised=127.0.0.1 udp_port=5060` |
| Helm reproducible rendering | `make chart-check` (`tools/bin/helm` 3.16.4) | `chart-check: OK` |
| Item-by-item environment variable check | Implementation side `platform/src/as_platform/` (`runtime/transport_env.py` as the main entry) | Reads a total of **16** `AS_SIP_*` / `AS_TLS_*` / `AS_PEER_*` variables, see the table below |

> **Explanation of the increasing counts**: the root guard is parameterized by evidence file. When E-6 was executed, `make gate` = `1174 passed` / `tests/test_evidence_discipline.py` = `135 passed`; after adding this batch's evidence, the closing re-run gives `1176 passed` / `137 passed`. The evidence file keeps the snapshot from execution time.

**The 16 environment variables read by the implementation**: `AS_PEER_ALLOWED_ADDRESSES`, `AS_PEER_ALLOWED_CERT_FINGERPRINTS`, `AS_SIP_ACCEPT_ALL_INVITES`, `AS_SIP_ADVERTISED_ADDRESS`, `AS_SIP_BIND_ADDRESS`, `AS_SIP_DISABLE_UDP`, `AS_SIP_ENABLE_TCP`, `AS_SIP_ROUTE_HOOK`, `AS_SIP_TCP_PORT`, `AS_SIP_TLS_PORT`, `AS_SIP_UDP_PORT`, `AS_TLS_CA_PATH`, `AS_TLS_CERT_PATH`, `AS_TLS_ENABLE`, `AS_TLS_KEY_PATH`, `AS_TLS_REQUIRE_CLIENT_CERT`.

**Documentation coverage**: `platform/README.md` **16/16**; `docs/operations/runbook-l2.md` 3/16 (subset references); `docs/delivery/install-guide.md` 1/16; root `README.md` **0/16** (no environment variable table).

**Reverse check**: `AS_SIP_NEXT_HOP` / `_PORT` / `_TLS_PORT` appear in the documentation but are not in `platform/src`; they are implemented in `apps/translation/src/as_translation/outbound.py:44/:48/:50`, so they are **neither drift nor wrong names**.

**Conclusion**: **no wrong names / typos / drift found**; the root `README.md` missing an env table is an **existing documentation gap** (non-blocking, already registered in `report.md` §0.7) and is not filled in by this batch.

### 2.2 Current matrix counts

The single source of values = section four of the "M8 batch 4 terminalization proxy signature (2026-10-13)" section of `docs/acceptance/m8-test-plan-matrix.md`.

| Bucket | Current value |
|---|---:|
| pass | **27** |
| defer | **4** |
| blocked | **9** |
| n-a | **9** |
| open | **0** |
| fail | **0** |
| **Total** | **49** |

Framing: all `pass` values are "**engineering evidence acceptance**", signed by agent proxy signature (under maintainer authorization), and are **not the maintainer's own signature**.

---

## 3. Gap list

**No gaps at the engineering layer.** P0 = 0 / P1 = 0 / P2 = 0. The following are **items requiring maintainer adjudication**, not engineering gaps of this batch:

| No. | Item | Nature |
|---|---|---|
| ① | The final wording of the `plan.md` M8 row awaits confirmation (draft already produced: `docs/acceptance/m8-plan-m8-row-draft-2026-10-12.md`) | Maintainer adjudication (documentation wording) |
| ② | The image digest is inconsistent with batch 1 (the new digest `sha256:63ba8f4df78d…` has been recorded; whether to unify the build framing is undecided) | Maintainer adjudication (build framing) |
| ③ | Environment variable table gap in the root `README.md` | Non-blocking; already registered in `report.md` §0.7 |
| ④ | The external hard dependencies (D-1 carrier PKI + external-network S-SBC, D-2 customer K8s, ADR-0008 cross-site drill, D12/O5 production HA) and the 4 `defer` rows (F-5 / F-8 / F-9 / F-11) still await scheduling or written risk acceptance | Maintainer adjudication (scheduling / risk acceptance) |
| ⑤ | The M8 exit signature is still deferred | Maintainer action (signature) |

---

## 4. Consistency check

| Check item | Plan / upstream source | Conclusion |
|---|---|---|
| No-edit files untouched (`docs/plan.md`, `docs/acceptance/m8-test-plan-matrix.md`, `VERSION`, `CHANGELOG.md`) | Batch 6 prompt "hard discipline" | ✅ Executed: none of the four was modified by this batch |
| The three append-style changes are pure additions (`+1` / `+35` / `+19`), zero deletions | Batch 6 prompt E-1 / E-5 / E-6 | ✅ Executed: `git diff --cached --stat` shows README index +1, `report.md` +35, `m8-exit-review-2026-10-06.md` +19, all insertions, no deletions |
| Gate and both guards fully green | `AGENT.md` / `make gate` definitions | ✅ Executed: all four steps of `make gate` exit 0 (`1174 passed, 249 deselected, 11 warnings`); `test_version_consistency.py` `9 passed`; `test_evidence_discipline.py` `137 passed` |
| Evidence file name prefix consistent with the four-layer mechanism | "The filename is the conclusion" in `docs/acceptance/artifacts/m5/README.md` | ✅ Consistent: E-6 uses the `PASS-` prefix, consistent with the actual passing conclusion |
| New evidence registered in the index | Same as above | ✅ Executed: `docs/acceptance/artifacts/m5/README.md` +1 line |
| Environment names do not use the anonymous "local machine" | Rule (2) of `docs/environments.md`; rule 5 of `tests/test_evidence_discipline.py` | ✅ Executed: this document and the E-6 evidence always use `dev-win03ib7niepf0` |
| No REQ signed off, no M8 signature | Batch 6 prompt "hard discipline" | ✅ Executed: the full text contains no wording such as "signed off / REQ-level acceptance passed / M8 fully green / release completed" |
| No git write operations executed | Same as above | ✅ Executed: no add / commit / tag / push / branch / remote change; all changes left in the working tree |
| review record format (five elements) | `AGENT.md` §3.3 | ✅ Followed: ① review target ② review date and reviewer ③ review conclusion ④ issue list and corresponding fixes ⑤ confirmation signature after the changes |

---

## Adjudication

> The verdict is a **reviewer recommendation** and may only be executed after maintainer confirmation; sign-off is the maintainer's action. The status column is uniformly "**pending maintainer confirmation**".
> **This batch renders no verdict and signs nothing by proxy.**

| Item | Source | Issue summary | Verdict (recommendation) | Fix plan | Status | Verification method |
|---|---|---|---|---|---|---|
| **①** | E-3 draft | The final wording of the M8 row in `docs/plan.md` §0 / §4 is undecided | Recommend the maintainer directly adopt or revise the three proposals in `docs/acceptance/m8-plan-m8-row-draft-2026-10-12.md` | The maintainer or an authorized agent changes `plan.md` (the agent did not change it in this batch) | Pending maintainer confirmation | Check the `plan.md` §0 step cell / product decision record / §4 M8 status column |
| **②** | E-6 image rebuild | This run's image id `sha256:63ba8f4df78d…` is inconsistent with batch 1's `sha256:8f2e1b9465d9…`; the difference is at the manifest layer (buildx v0.31.1 produces an attestations-carrying manifest list) | Recommend either/or: ① unify the buildx build framing to reproduce the shape of batch 1's digest; ② give written acceptance of the new framing "the manifest list digest is authoritative" | If ① is chosen, `docker build` must be re-run and compared; if ② is chosen, the framing change must be noted in the E-6 evidence and in this document | Pending maintainer confirmation | Re-run `docker build` and compare `{{.Id}}`; or check the framing note in the E-6 evidence |
| **③** | E-6 environment variable check | The root `README.md` has no environment variable table (0/16 coverage) | Recommend adding the table, or giving written acceptance of the gap (non-blocking, already registered in `report.md` §0.7) | The maintainer or an authorized agent adds the env table to `README.md`; this batch does not add it | Pending maintainer confirmation | Check whether the root `README.md` contains a complete table of the 16 variables |
| **④** | Upstream D-1 / D-2 / ADR-0008 / D12-O5 and the 4 `defer` rows | The external hard dependencies are not scheduled; F-5 / F-8 / F-9 / F-11 are pinpointed to v1.1 but not yet raised as items | Recommend giving a schedule or written risk acceptance; F-5 / F-8 / F-9 / F-11 go through the v1.1 item-raising process | Scheduling registration or written acceptance by the final review; raising items goes requirement → ADR → design → review | Pending maintainer confirmation | Check the v1.1 registration and the final review risk-acceptance record |
| **⑤** | E-4 / E-5 sign-off section | The M8 exit signature is still deferred | Recommend the maintainer sign separately in the M8 exit review; this batch only completed the internal-build close-out | Maintainer signature (cannot be signed by proxy) | Pending maintainer confirmation | Check the M8 signature field in §3.2 of `m8-exit-review-2026-10-06.md` |
| **(Additional) commit splitting** | Current working-tree state | This batch's 8 files are mixed with batch 1's leftover `.dockerignore`, the maintainer's own changes (`.gitignore`, `docs/intro.md`), and the untracked IDE directory `.codebuddy/teams/...` | Recommend splitting commits by origin and not mixing this batch in | The maintainer chooses the `git add` scope and commits | Maintainer action | Item-by-item check via `git status --short` |
| **(Additional) tag** | `AGENT.md` §10.4 | No tag for an internal build | Keep not tagging; tags are executed only by the maintainer | None | Maintainer action | `git tag -l` |

> Note: commit splitting and tagging are maintainer actions rather than review verdicts; they are listed in this section only as a reminder and do not constitute a verdict recommendation.
>
> **2026-10-13 maintainer adjudication (②)**: the image digest framing **chooses ② — written acceptance of the new framing**, with the manifest list digest produced by buildx v0.31.1 being authoritative (`sha256:63ba8f4df78d…`), and the build is **not re-run** to reproduce the shape of batch 1's `sha256:8f2e1b9465d…`. Both digests in the E-6 evidence and the statement "layers are CACHED, no claim of byte-for-byte identity" are final and will not be changed.

---

## Sign-off

- **Sign-off state**: **unsigned — pending maintainer signature**.
- **Reviewer**: AI agent (reviews and lists gaps only, does not sign).
- **Authorization basis**: the maintainer has authorized **executing** the six M8 batches (per §6 item 6 of `docs/handoff/2026-10-12-m8-scope-revision-internal-release-plan.md`; execution authorization ≠ signature authorization). This batch signs no REQ or milestone by proxy; sign-off remains the maintainer's action.
- **Review conclusion**: **conditional pass** — all six items (E-1～E-6) of batch 6 "documentation and report" **have landed**, and the **internal-build close-out is complete (conditional)**; the condition is that ①～⑤ in the table above are all confirmed by the maintainer.
- **M8 exit signature field**: **unsigned — pending maintainer signature** (internal build, not signed off).
- **REQ**: **this batch signs off no REQ**.
- Execution environment `dev-win03ib7niepf0`; this batch executed no git write operations; `docs/plan.md`, `docs/acceptance/m8-test-plan-matrix.md`, `VERSION`, and `CHANGELOG.md` were not modified.

---

(This record is the batch 6 "documentation and report" review. This document signs off no REQ, does not sign the M8 milestone signature, makes no claim that M8 is fully green, and makes no claim that a release has occurred; "internal-build close-out complete" does not equal "M8 exit signature".)
