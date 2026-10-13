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

# M8 Internal Release Wrap-Up — Handoff (2026-10-12)

## 0. Purpose of this handoff

This session completed batch 1 "Release and Packaging". The new session picks up from batch 2 "SIP Differential Testing". This document is the sole execution entry point for the new session — once it is read you can continue; there is no need to review this session's conversation.

## 1. Current status

- **Positioning of this build**: an internal build (complete functions + simulator evidence + reproducible release artifacts), **not the M8 exit sign-off**.
- **Completed**: of the six batches, batch 1 "Release and Packaging" is fully complete and has passed verification.
- **Pending**: batch 2 → 3 → 5 → 4 → 6 (in dependency order).
- **Branch**: master (no changes committed).

## 2. Batch 1 completion items (written to disk, not committed)

### 2.1 Changed files

| File | Change |
|---|---|
| deploy/docker/Dockerfile | Two-stage → three-stage (resip-builder/py-builder/runtime): build the reSIProcate shared library from vendor source plus three native extensions (_resip_runtime/_resip_two_leg/_resip_recovery); runtime ENV: AS_ENABLE_SIP_RUNTIME=1, AS_RESIP_*_BUILD=/app/native, LD_LIBRARY_PATH=/app/lib; EXPOSE corrected to 5060/udp 5060/tcp 5061/tcp |
| platform/src/as_platform/__main__.py | main() wires in SipStackService.from_env()+start(); stop() on drain; fail-closed: extension missing → except → exit 2; backward compatible when the env vars are unset |
| platform/README.md | environment-variable table completed from 10 rows to 30+ rows (AS_SIP_*/AS_TLS_*/AS_PEER_*/AS_RECOVERY_*), annotated with the Helm wiring status and the corresponding values keys |
| CHANGELOG.md | an "Internal build (2026-10-12)" subsection is appended to the `[0.2.0]` section, annotated "internal build, not a release" |
| .dockerignore | exempts the vendor source header files |
| docs/acceptance/artifacts/m5/2026-10-12/PASS-docker-build-digest-2026-10-12.txt | image build evidence: image ID sha256:8f2e1b9465d96a8cb7b9cab286e687a52621f136b570f521df15f6f9112da7c8, native listener confirmed to be listening on UDP 5060 |
| docs/acceptance/artifacts/m5/2026-10-12/PASS-desensitization-check-2026-10-12.txt | desensitization re-check: no keys / certificates / packet captures / password-bearing logs inside the image |
| docs/reviews/m8-batch1-release-packaging-review-2026-10-12.md | batch 1 review record (no gaps, awaiting maintainer review, unsigned) |

### 2.2 Verification results

- make gate: 1104 passed / 2 skipped / 214 deselected (exit 0)
- tests/test_evidence_discipline.py + tests/test_version_consistency.py: 94 passed
- image build exit 0, RESIP_RUNTIME_LISTENING confirms listening on UDP 5060
- desensitization re-check: no sensitive files

### 2.3 Leftover uncommitted changes (not introduced by this batch; left over from earlier sessions)

The following files in the work tree also carry uncommitted changes. They were **not introduced by batch 1**, and the new session must take note:
- docs/acceptance/m8-test-plan-matrix.md
- docs/handoff/2026-10-12-m8-scope-revision-internal-release-plan.md
- docs/plan.md
- docs/reviews/m8-scope-revision-internal-release-plan-review-2026-10-12.md (newly created)

> **Destination pointer (added 2026-10-13; the original text of §2.3 above is preserved unchanged in every respect)**: the uncommitted work-tree changes and the unowned files recorded in this section
> are all consolidated in [`../next-release-v1.1-plan.md`](../next-release-v1.1-plan.md) **§5-6** (documentation and repository hygiene category) —
> that document takes the live `git status` as its source of truth and **does not freeze the list item by item** (the list moves with every commit action, so freezing it makes it stale at once); how to split the commits is the maintainer's decision
> (`AGENT.md` §10.4). Any later status inventory, report, handoff, or new-session kickoff that touches the leftover items in this passage must **cite only that pointer**;
> do not reopen this section's list, and do not list them again under "actions pending the maintainer".

## 3. Pending batches (in dependency order)

### Batch 2 "SIP Differential Testing" (next)

**Execution order (taken from ../handoff/2026-10-09-sip-native-testing-plan.md §4-D; must not be reordered)**:

1. **S8 baseline supplementary capture**: add the Route / Record-Route baseline to the M2 probe capture (the baseline lacks these two headers, which is the root cause of the 2 existing skips). Do not schedule the S8 implementation before the supplementary capture; REQ-F-5 is not signed pass per the N4 stop line. After the supplementary capture lands, it is recommended to slot it in after P3.
2. **P1 S5**: two-leg normalized sequence differential check. F-2 was already counter-signed pass under N3 on 2026-10-12; this is a coverage extension (row status unchanged). Reuses the `testbed/e2e/` framework.
3. **P2 S7a**: expand the SDP pass-through corpus (also serves as the broader corpus for F-4). Add SDP variants carrying media descriptions / multiple m-lines. Advances F-4.
4. **P3 S6**: multi-rule priority + no-match combinations. F-3 was already counter-signed pass under N3; this is a coverage extension. Shares the simulation chain with S2 (404 already green).
5. **P4 S10**: non-2xx (486/480/408) pass-through. Depends first on extending the testbed peer UAS (currently returns only 200). Advances F-10.
6. **P5 S9**: in-dialog routing. Depends on the M7.3 context-restoration engineering slice (already in place). Advances F-9.
7. **P6 S11**: CANCEL and final-response race. A deterministic proof of the two race branches is the most expensive and carries the greatest flaky risk; closing it out as a registered gap is permitted. Advances F-11.

**Other related items**:
- F-8 (the three CANCEL branches) advances together with the S4 cancel harness and the S11 differential check.
- The trace-linkage part of F-16 (the translation decision chain) depends on F-13 — F-13 has been adjudicated as deferred to v1.1, so F-16 is signed only for the non-trace part and the reason is stated.

### Batch 3 "kind/sim Evidence"

Can partially run in parallel with batch 2; F-15 real AS depends on the batch 1 image (already ready). Evidence rows: NF-2, NF-4, NF-9, NF-5, F-15/5.4-F-15真AS, NF-10, 2.5 Backup and Restore (kind bundled PG backup/restore/rebuild drill + runbook walkthrough + measured elapsed time).

### Batch 5 "Performance and Capacity (kind)"

Can run in parallel with batch 3; supplies NF-15 evidence to batch 4.
- NF-15 multi-replica measurement: multiple replicas on kind, recording per-pod CPU/memory utilization.
- HPA threshold entry: after the kind measurement, fill in deploy/helm/values-onprem.example.yaml (annotated "measured on kind, not an external commitment, must be re-measured in the target environment before go-live"); the default values.yaml stays null.
- O1: internal engineering target of loopback CPS 1280 with zero failures (internal only; not written into any external material).
- No capacity-class alerts are to be added; ne-datasheet / 4.1 formal report remain blocked.

### Batch 4 "Sign-off and Review"

Depends on the evidence produced by batches 2/3/5.
- S-1 (allowlist): review the existing evidence + supplementary testing for the missing items.
- S-4 (RBAC + tamper-proof audit): review + supplementary testing for the missing items; durable audit already has an engineering slice.
- Bring each of the 17 open matrix rows to a final state: every row gets exactly one of pass/n-a/defer, and a rationale is mandatory; a pass requires new evidence from this build.

### Batch 6 "Documentation and Reports" (last)

- E-1: promote report.md to the M8 RC report; sync the §0.5 counts to pass 16 / open 17 / blocked 7 / n-a 9 / fail 0.
- E-2: VERSION stays at 0.2.0; CHANGELOG has already had the internal build appended.
- E-3: write back the M8 rows in plan.md §0/§4.
- E-4: internal-build exit review document (explicitly not the M8 exit sign-off).
- E-5: milestone signature table (M1/M2/M6/M7 engineering completion already counter-signed; M8 is not signed).
- E-6: packaging re-check.

## 4. The six adjudicated items (do not re-ask)

1. F-13/NF-7 call trace = a major omission, deferred to v1.1 as a feature; not implemented in this build; F-16 is signed only for the non-trace part.
2. The internal build does not bump: VERSION stays at 0.2.0, CHANGELOG appends an internal build entry inside the 0.2.0 section, the image tag uses as-platform:0.2.0-internal-<date>, and the chart is no longer kept in sync.
3. 2.5 Backup and Restore: this build performs a complete kind engineering drill (bundled PG backup/restore/rebuild + runbook walkthrough + measured elapsed time), and explicitly states that this is not equivalent to the customer's real cluster edition.
4. NF-15 HPA thresholds: after the kind multi-replica + per-pod CPU/memory measured data has been produced, fill in values-onprem.example.yaml (annotated "measured on kind, not an external commitment, must be re-measured in the target environment before go-live"); the default values.yaml stays null; ne-datasheet / capacity alerts / the 4.1 formal report remain blocked.
5. Batches 2/3 receive full authorization in one go.
6. Batches 1/4/6 (and the implied batch 5) likewise receive full authorization. → All six batches are authorized.

## 5. Hard discipline (violating it means rework)

- The main agent only plans / reviews / reports and does not write files directly. Every file-writing action is delegated to a writing subagent (Task tool subagent_type=general_purpose_task); only one writing member is allowed in a work tree at a time.
- Do not perform any git write operation (no add/commit/tag/push/change remote/create branch); how to split commits is the maintainer's decision.
- Do not sign off any REQ, do not sign off any milestone, do not change the status of any matrix row, do not change the counts in report.md. When writing documents, always "preserve the original text unchanged and append a correction".
- Four-layer evidence mechanism: the filename is the conclusion (docs/acceptance/artifacts/** mandates the PASS- / FAILCLOSED- prefix); the environment must have a name (write the environment name already registered in environments.md, dev-win03ib7niepf0; anonymous "this machine" is forbidden); every status is a triple (conclusion, evidence file, date); guard test tests/test_evidence_discipline.py.
- Do not invent new identifiers; reference existing ones.
- Do not publish any external capacity figure; the internal engineering target (loopback CPS 1280) is internal only.

## 6. Environment information

- Registered environment: dev-win03ib7niepf0 (host WIN-03IB7NIEPF0)
- Tools are in tools/bin (helm 3.16.4 / kubectl 1.31.4 / kind 0.24.0 / promtool 2.55.1, versions pinned in tools/VERSIONS)
- Existing kind clusters: as-m5 (context kind-as-m5), as-m71
- docker is available
- Build/test commands are in the Makefile (make gate / make gate-native / make chart-check / make test-integration-compose / make m2-platform-resip-build)

## 7. New-session kickoff ritual

The new session's first actions:

1. Read AGENT.md, docs/README.md, the current milestone in docs/plan.md, and docs/acceptance/m8-test-plan-matrix.md
2. Read this handoff document
3. Use git status to check the current state of the work tree
4. Start from item 1 of batch 2 (S8 baseline supplementary capture)

## 8. Key pointers

- The sole execution basis for this batch: docs/handoff/2026-10-12-m8-scope-revision-internal-release-plan.md
- SIP differential-testing plan: docs/handoff/2026-10-09-sip-native-testing-plan.md §4-D
- Sign-off matrix: docs/acceptance/m8-test-plan-matrix.md (currently pass 16 / open 17 / blocked 7 / n-a 9 / fail 0; F-13/5.4-F-13/NF-7 have already been moved to n-a)
- Review record: docs/reviews/m8-scope-revision-internal-release-plan-review-2026-10-12.md (G-1/G-2/G-3 are closed)
- Environment registry: docs/environments.md
- Batch 1 review: docs/reviews/m8-batch1-release-packaging-review-2026-10-12.md

---

Date written to disk: 2026-10-12. This document does not sign off any REQ, does not sign off any milestone, and does not change any matrix status.
