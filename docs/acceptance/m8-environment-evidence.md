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

# M8 environment evidence record (Phase D)

> **Date**: 2026-10-06
> **Basis**: `docs/handoff/2026-10-06-m8-release-candidate-plan.md` §4 Phase D + items 3–4 of §3 exit conditions;
> the S-2 / S-3 / NF-1 blocked rows in the sign-off matrix `docs/acceptance/m8-test-plan-matrix.md`.
> **Principle**: while maintainers are absent, do not fabricate operator / customer site evidence. This file records only **verifiable current state + gaps + defer conclusions**;
> it does not replace maintainer sign-off or the M8 exit review (`docs/reviews/m8-exit-review-*.md`). Originally written in Chinese.
> **Redaction red line** (AGENT §11 / §13): must not commit private keys, cleartext certificates, real packet captures (pcap/pcapng), or logs containing keys;
> the evidence directory convention is in §0.

## §0 Evidence directory and redaction conventions

- Evidence root: `docs/acceptance/artifacts/m8/<date>/` (`<date>` is the evidence collection date, in the form `2026-10-06`).
- Per-item subdirectories: `req-s-2-pki/` (REQ-S-2), `req-s-3-rotation/` (REQ-S-3), `req-nf-1-live/` (REQ-NF-1).
- Each subdirectory must contain a `README.md` (collection time, environment, collector, version tag) + a redacted command transcript + redacted log excerpts.
- Allowed to commit: command transcripts (keys/fingerprints masked), version numbers / image tags, metadata output such as `openssl x509 -noout -subject -issuer -dates` (serial numbers/fingerprints masked or truncated).
- **Forbidden to commit**: `*.key` / `*.pem` private keys, full cleartext certificates, `*.pcap` / `*.pcapng` real captures, logs containing passwords/tokens.
  The `*.log` / `*.pcap` / `*.pcapng` / `artifacts/` rules in `.gitignore` remain in effect;
  the `!docs/acceptance/artifacts/` exception makes this directory trackable (see `docs/acceptance/artifacts/m8/README.md`),
  and key-like extensions are still ignored, which is expected behaviour.
- Runbook references: `docs/acceptance/m4b-8-runbook.md` (dev HTTPS / browser evidence method),
  `docs/acceptance/m8-native-consistency-runbook.md` (native consistency before sign-off),
  `docs/acceptance/m5-state-stores-runbook.md` (state stores on-site step reference).
  At on-site evidence collection the maintainer designates the runbook version applicable to that run and notes it in the subdirectory README.

## D-1 Operator PKI / external-network S-SBC (REQ-S-2 / REQ-S-3 tail items)

- **Requirement links**: `docs/acceptance/test-plan.md` §3 REQ-S-2 (AS↔S-SBC all TLS, cleartext 5060 rejected, operator PKI issuance chain verified),
  REQ-S-3 (calls unaffected during the old/new certificate coexistence window, new connections use the new certificate); matrix `m8-test-plan-matrix.md` §3 S-2 / S-3 rows (both `blocked`).
- **Expected evidence shape** (to be added when maintainers collect evidence in their environment):
  - `req-s-2-pki/`: operator PKI issuance chain information (`openssl verify -CAfile <masked path>` conclusion excerpts, no cleartext certificates),
    a transcript of the AS→S-SBC TLS handshake command (target address/port masked), a transcript of the cleartext 5060 rejection command (`openssl s_client` / SIP client connection failure excerpts), version tag.
  - `req-s-3-rotation/`: rotation window start and end times, proof of old/new certificate coexistence (metadata command output, masked), observation records showing existing calls held during rotation and new connections using the new certificate (redacted log excerpts), version tag.
- **Current state (measured in this environment, 2026-10-06)**: this environment has **no operator PKI lab and no external-network S-SBC peer**, so the above collection cannot be performed.
  Locally there are only engineering-side TLS integration tests that pass inside `make gate` (an engineering slice, **not** REQ-S-2/S-3 on-site acceptance).
  No operator issuance chain verification and no live proof of cleartext rejection were performed or witnessed — recorded honestly as a gap; no data is fabricated to fill it.
- **Conclusion: restriction (2026-10-07)**. Maintainer confirmation: there will be no real operator S-SBC joint debugging and no customer K8s testing before this project closes. D-1 is no longer scheduled for evidence collection. REQ-S-2's "operator PKI issuance chain" and REQ-S-3's rotation window on a real peer cannot be signed as pass before Close. M7.1 was engineering-closed: TLS calls on the test CA already work in kind. Cleartext 5060 remains the first version's optional transport; it was not made "reject cleartext as long as TLS exists". The operator PKI issuance chain remains covered by this restriction.

## D-2 Customer K8s REQ-NF-1 live baseline (kill / restart / BYE)

- **Requirement links**: `docs/acceptance/test-plan.md` §2 REQ-NF-1 (kill/restart does not lose state: kill/restart after the basic call ACK has established a dialog,
  BYE is compared, Redis state recovers); `docs/plan.md` §5.2 D10 ("the REQ-NF-1 acceptance checkbox is still owned by M8 maintainers (K8s live baseline)");
  matrix `m8-test-plan-matrix.md` §2 REQ-NF-1 row (`blocked`, live evidence belongs to Phase D D-2).
- **Expected evidence shape** (to be added when evidence is collected on the customer K8s):
  - `req-nf-1-live/`: cluster and version information (K8s version, image tag, Helm values version), kill/restart command transcripts
    (`kubectl delete pod / rollout restart` object names masked), a before/after dialog state comparison (redacted log excerpts, Call-IDs masked or truncated),
    the BYE comparison conclusion, version tag. Runbook references (see §0).
- **Current state (measured in this environment, 2026-10-06)**: this environment has **no customer K8s cluster**; no live kill/restart/BYE baseline was executed.
  On the engineering side there are only M7 D10 slice evidences (**engineering harness, not live acceptance**):
  - `platform/tests/test_d10_product_recovery_integration.py` (M7.6 product integration slice)
  - `platform/tests/test_d10_req_nf1_harness_integration.py` (M7.7 process shell + REQ-NF-1 engineering harness)
  - `platform/tests/test_d10_req_nf1_redis_integration.py`, `platform/tests/test_d10_process_restart_integration.py`
  - Matrix header note: `test_d10_product_recovery_integration.py → 1 passed` (the ACK-established-dialog engineering slice).
  None of these constitutes REQ-NF-1 live sign-off — keep them distinguished honestly, do not pass them off as such.
- **Conclusion: restriction (2026-10-07)**. No kill / restart / BYE on customer K8s before Close. The customer-cluster clause of REQ-NF-1 cannot be signed as pass before Close. The engineering harness on our own kind is still only an engineering slice. Killing a Pod on the M7.1 simulator platform in a lab cluster does not equal this item either.

## D-3 Whether the D6 testbed is v1 customer acceptance (maintainer adjudication pending)

- **Requirement links**: `docs/plan.md` §5.2 D6 ("whether the testbed must support customer acceptance testing in v1; the architecture document defers it to v1.1");
  matrix `m8-test-plan-matrix.md` conditional row `D6-testbed验收` (`blocked`, belongs to Phase D D-3).
- **Expected evidence shape**: the maintainer adjudication record (v1 inclusion vs v1.1; if included, add customer acceptance cases and the evidence directory; if not, close this item).
- **Current state**: maintainers are absent, so there is **no adjudication**. This file does not adjudicate on their behalf; it records only a recommendation.
- **Conclusion: maintainer adjudication pending; recommend v1.1** (unless the customer explicitly requires v1 acceptance).
  - Rationale: the architecture already has a baseline deferring this to v1.1; there is no customer acceptance input in the M8 window, so including it in v1 would only add an open item without adding verifiable evidence.
  - Follow-up, pick one of two (requires written maintainer confirmation): (a) accept the recommendation → D-3 is closed and the D6 row is handled as v1.1 (matrix `D6-testbed验收` moves to terminal state, with rationale);
    (b) the customer requires v1 → D-3 becomes an evidence collection task, evidence lands in `docs/acceptance/artifacts/m8/<date>/`, and an ADR or a §5 row of `plan.md` is added.
  - Before adjudication: D6 **remains blocked** in the matrix; a terminal state (closed, or an evidence collection plan) is required before the M8 final review, and sign-off must not be given with an open status.

## The same restriction: other items that require a real customer network

After checking `test-plan.md` §1–§4, the following also cannot be evidenced on a customer network before Close, and are therefore likewise marked as restrictions:

| Item | Why it counts as a real customer network |
|---|---|
| **ADR-0008 cross-site switchover drill** | It needs two customer/production sites, not a single lab cluster |
| **D12 / O5 production Redis and PostgreSQL HA** | It needs Sentinel / streaming replication / PITR on the customer's production topology. Bundled state in kind is not this item |

The items below mention a cluster, S-SBC, or live, but are **not** marked as the same restriction: what they need is a lab or a simulation, not the customer's network.

| Item | Disposition |
|---|---|
| REQ-NF-2, REQ-NF-4, REQ-NF-9 | Our own kind / lab cluster suffices; a customer cluster is not required |
| REQ-NF-5 | The simulated S-SBC was already made into a transparent bridge in M7.1 (no Kamailio). It is not an operator S-SBC |
| "SIP over TLS, cleartext rejected" within REQ-S-2 | M7.1 already ran TLS calls on the test CA. Cleartext 5060 is still optional, and "cleartext is rejected" is not signed. The operator PKI issuance chain remains under the D-1 restriction |
| REQ-NF-3, REQ-NF-13, REQ-NF-14, REQ-F-13, REQ-F-15 | What is missing is a criterion, a monitoring backend, or product capability — not a customer IMS / customer K8s |

## Relationship to the M8 exit

- D-1, D-2, the ADR-0008 drill, and D12/O5 production HA are **restrictions**: no evidence is collected before Close, they stay `blocked` or `open` in the matrix, and cannot be signed as pass. The M7.1 simulator platform does not lift these restrictions.
- D-3 is still pending adjudication; this file's v1.1 recommendation has no force.
- The D-1/D-2 directories under `docs/acceptance/artifacts/m8/` stay empty. The state is a restriction, not "awaiting evidence".

---

### D-3.1 Countersignature result (2026-10-12; the D-3 original text is kept unmodified, this section is appended after it)

> **Authorization source**: on **2026-10-12 maintainers explicitly authorized the agent to countersign** the nine written M8 N2 adjudications
> (item 5 of N2, the authoritative text, is exactly this D-3; the full countersign record is at
> [`../handoff/2026-10-12-m8-n2-countersign-record.md`](../handoff/2026-10-12-m8-n2-countersign-record.md)).
> **This section is not a maintainer's own signature**: it is marked "agent countersignature" and carries its basis.

**Adjudication (N2 item 5)**: **accept option (a)** — D-3 is **closed** and the D6 row is handled as **v1.1**.
Signature: **agent countersignature (maintainer authorization dated 2026-10-12)**.

**Basis (no newly invented conclusion)**: the two options given in the D-3 original text:
> (a) accept the recommendation → D-3 is closed and the D6 row is handled as v1.1 (matrix `D6-testbed验收` moves to terminal state, with rationale)

**Synchronizations already executed**:

| Location | Action |
|---|---|
| The `D6-testbed验收` row of `m8-test-plan-matrix.md` | status changed from `blocked` to terminal `n-a`, rationale "D6 testbed customer acceptance is deferred to v1.1" |
| The "D-3 / D6 adjudication" field in §10 of `2026-10-06-m8-release-candidate-plan.md` | the (a) conclusion has been filled in |

**Boundaries**

1. Deferring D6 to v1.1 **does not mean** D6 is cancelled — it remains in the §5.2 D6 row of [`../plan.md`](../plan.md) and within the v1.1 scope,
   and is **not accepted in this cycle and never recorded as pass**.
2. This section does **not** turn D-3 into an evidence collection task (that is option (b) of the either/or, which was not adopted).
3. The D-3 original sentence "before adjudication: D6 remains blocked in the matrix" is **no longer applicable** because of this section's adjudication; that sentence is retained as history.
