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

# 3GPP / GSMA / RFC specification compliance matrix

> **Status block (read this before the rest of the document)**
>
> - **Product name**: `In-house IMS Application Server`, **formally adopted as the product / documentation descriptor name** (G8-2; **not a trademark / not a brand claim**), first appearing annotated with the 3GPP Third-Party AS role; hereafter abbreviated in-house AS (`docs/plan.md` §0 "Product Decision Log", G8 line). git repo name: reported renamed to `inhouse-ims-as` by the maintainer (G8-3; repo name and remote URL only; this repo has not had its remote or local path changed); chart name, image name, and OTel service name **remain `3rdparty-as` unchanged**.
> - **This file belongs to**: [`../product-packaging-plan.md`](../product-packaging-plan.md) §1 first-batch deliverable **1.2 (3GPP specification compliance matrix)**. **B6 review status**: this document has left a review record with the B6 review —— [`../reviews/product-packaging-review-checklist-2026-10-12.md`](../reviews/product-packaging-review-checklist-2026-10-12.md) §6 (2026-10-12 initial review) and §7 (2026-10-12 closed-loop re-review); **conclusion pending maintainer confirmation**, and before confirmation it is not used as a basis for external delivery or acceptance (`AGENT.md` §3.3).
> - **Four-state definition**: **Fully** (implemented and with in-repo evidence) / **Partial** (partially implemented or with known gaps) / **N/A** (not applicable per a scope decision, with a stated rationale) / **open** (insufficient evidence; asserting compliance is forbidden). The "N-A" in the plan document is this document's **N/A**.
> - **Evidence rule**: every Fully / Partial cell must give a `file:line` or contract scenario number (S1–S12); **where evidence cannot be found, never write Fully — only open**.
> - **Production stack**: **reSIProcate** (C++, Vovida license), ADR-0019 **accepted**. **sippy is only a testbed behavior baseline** (`testbed/contracts/sip-baseline/README.md:1-6`), **not a production dependency**; `platform/` does not use sippy on the production path.
> - **Un-accepted statements**: **E1 (product-path real-socket diff of S1–S11), E4 (S12 TLS certificate hot-rotation), E5 (state externalization and process-restart recovery) are all un-accepted**, pending M8 acceptance (ADR-0019 §6 step 5 "accepted gaps", §10; [`../plan.md`](../plan.md) §5.1 O2/O3). The native DUM loopback smoke is **not** product E1, not a requirement acceptance (ADR-0022 Evidence).
> - **testbed evidence boundary**: ADR-0014 explicitly excludes testbed from v1 deliverables ([`../product-packaging-plan.md`](../product-packaging-plan.md) §0.3 item 8); simulation results (including the M7.1 simulation platform, callload, M6 dev-host harness) are R&D / demo assets and **must not** serve as operator IOT or live-network evidence; when cited, always label "internal measurement / not for external use".
> - **This document contains no capacity numbers**: O1 (capacity target) **is unresolved** ([`../plan.md`](../plan.md) §5.1), and `AGENT.md` §2 forbids publishing any CPS / CAPS / BHCA / concurrency / latency number before the measured adjudication. The `5060` / `5061` appearing in the text are **protocol port constants**, not capacity metrics (the original note at [`deploy/helm/values.yaml`](../../deploy/helm/values.yaml) L148 says exactly this).
> - **Terminology discipline**: **RC ready ≠ passed**. M8 release-candidate artifacts are ready, but **exit sign-off is still on hold** ([`../acceptance/report.md`](../acceptance/report.md) §0 status line).

---

## 1. Scope and determination method

### 1.1 Applicability

- **Coverage objects**: the in-house IMS AS's **external SIP access plane** (S-CSCF → S-SBC → AS ISC-triggered signaling) and **internal decision plane**; the control-plane internal API is not expanded line by line in this matrix.
- **Network role**: a third-party Application Server **outside** the operator's IMS network; S-CSCF / S-SBC / HSS are operator network elements, appearing only as `testbed/` simulators (`AGENT.md` §1).
- **Access semantics**: **ISC only** (ADR-0003 accepted). The iFC trigger logic is on the S-CSCF/HSS side; the AS side does no iFC canary (review G-P0-5).
- **Not covered**: media plane, billing plane, Diameter plane, compliance section (PDPO see deliverable 3.4), capacity section (blocked by O1).

### 1.2 Four-state determination

| State | Determination condition | Permitted wording |
|---|---|---|
| **Fully** | Behavior implemented, **and** a `file:line` or contract scenario number is findable, **and** it does not depend on un-accepted E1/E4/E5 | "implemented" |
| **Partial** | Implemented but with known gaps, covering only part of the codes/scenarios, or verified only on an engineering slice / testbed harness | "partially implemented; gap: …" |
| **N/A** | Not applicable per a recorded scope decision; must write one line of rationale and basis | "not applicable; rationale: …" |
| **open** | No in-repo evidence, or evidence is only documentation description, paper evaluation, or pending manual check of the spec text | "pending check; blocked: …" |

> **Currently this document has no cell marked Fully**: every positive capability depends on at least one of E1 / E4 / E5, and these three are **not yet accepted** (ADR-0019 §6 step 5, §10). This is the honest state, not an omission.

### 1.3 Evidence tiers

- **A** —— product code + corresponding unit / integration test (`file:line` findable): supports Fully / Partial.
- **B** —— product code only (no corresponding test): capped at Partial. **C** —— documentation / ADR / paper evaluation only: capped at open.
- **D** —— no evidence (spec text not retained in repo, or no line-by-line implementation): can only be open.

**Specific evidence files cited in this document** (for review spot-checking): `platform/src/as_platform/sip/{adapter,call_controller,message,transport,ingress,resip_runtime}.py`, `platform/native/resip_runtime/runtime_module.cxx`, `platform/tests/{test_call_controller,test_call_controller_recovery,test_sip_message,test_transport_seam,test_transport_ingress,test_resip_runtime_integration,test_resip_runtime_tls_policy_integration,test_resip_two_leg_integration,test_m7_forward_two_leg_integration,test_req_f4_sdp_identity_integration,test_d10_req_nf1_redis_integration}.py`, `apps/translation/src/as_translation/{decision,outbound}.py`, `apps/anti-fraud/src/as_anti_fraud/decision.py`, `testbed/contracts/{sip-baseline,decision}/`, `testbed/simulators/src/as_simulators/{bridge,sut}.py`, `deploy/helm/values.yaml`.

> **Release-applicability discipline**: the specific Release of 3GPP specs such as TS 24.229 has **not** been checked line by line; every release-related judgment in this document is recorded as `open (not checked line by line)`, and **"compliant with Release X" is never written**.

---

## 2. Summary table

| Spec / document | Applicability | State | One-line conclusion | See |
|---|---|---|---|---|
| 3GPP TS 24.229 (IMS SIP, ISC trigger) | Applicable | **Partial** | In-leg decision, two-leg B2BUA, and non-2xx branch after ISC trigger are implemented with evidence; clause-level compliance not checked line by line, recorded as open | §3.1 |
| 3GPP TS 29.228 / 29.229 (Cx) | **Not applicable** | **N/A** | Cx is the interface between HSS and S-CSCF, an internal operator-network-element interface; the AS is not involved | §3.2 |
| 3GPP TS 29.328 / 29.329 (Sh) | **Not applicable** | **N/A** | AS data comes from its own data plane; it does not interact with HSS | §3.3 |
| 3GPP TS 32.260 / 32.299 (billing / CDR) | **Not applicable** | **N/A** | No collection, delivery, rating, or archiving of call records | §3.4 |
| GSMA IR.92 | Applicable (IMS profile / interoperability) | **open** | The spec text is **not retained in the repo**, nor is there line-by-line implementation evidence; to be confirmed line by line after manual check of the text | §3.5 |
| GSMA IR.94 | Applicable (media and security baseline) | **open** | Same as above; this document only describes the scope such a document typically covers, and makes no clause assertion | §3.5 |
| RFC 3261 (SIP) | Applicable | **Partial** | Message construction, status codes, header handling, Dialog/B2BUA, CANCEL/487 are implemented; forking / 3xx / REFER / PRACK-UPDATE interleaving not implemented | §3.6 |
| RFC 6733 (Digest auth) | **Not applicable** | **N/A** | No digest implementation; peer admission relies on allowlist + mTLS | §3.7 |
| RFC 8688 (ToS-SIP / `608 Rejected`) | Applicable (capability declaration may appear) | **open** | Rejection uses `603 Decline`; `608` is **not implemented**, inconsistent with some documentation descriptions | §3.8 |
| RFC 4566 (SDP) | Applicable (pass-through only) | **Partial** | Body passed through byte-for-byte; the AS does not parse, rewrite, or anchor media | §3.6.9 |
| RFC 3265 / 3325 / 3326 / 3428 | Applicability TBD | **N/A** | Product code has no hits (`MIN-SE` / RTP/RTCP / RAck / `Reason:`); no media means not applicable; line-by-line rationale in §3.6.9 | §3.6.9 |

---

## 3. Per-specification matrix

### 3.1 3GPP TS 24.229 —— IMS SIP, ISC trigger

> **Clause-level compliance: open (not checked line by line)**. The repo **does not retain the TS 24.229 text** (`docs/README.md` L34 planned a `docs/specs/` directory, but that directory **does not exist**), so the table below **cites no clause numbers**, only registering "capability item → in-repo evidence". The spec text must be retrieved manually and checked line by line.

| Capability item (clause number not checked line by line) | Applicability | State | Implementation location (file:line) | Evidence | Notes and blockers |
|---|---|---|---|---|---|
| S-CSCF triggers AS with initial INVITE (ISC) | Applicable | **Partial** | `platform/src/as_platform/sip/resip_runtime.py:330`, `platform/native/resip_runtime/runtime_module.cxx:979` | A: `testbed/simulators/tests/test_product_path.py` (integration, across simulated S-SBC and **not** using accept-all) | Only the in-leg arrival and decision are verified; full two-side end-to-end diff is E1, un-accepted |
| In-leg decision by business rules (FORWARD / TRANSLATE / DECLINE / NOT_FOUND) | Applicable | **Partial** | `platform/src/as_platform/sip/adapter.py:128-148`, `platform/src/as_platform/sip/call_controller.py:82-95` | A: `platform/tests/test_call_controller.py`, `apps/*/tests/test_contract_replay.py` | Decision is a pure function; the rule set comes from config, not SIP semantics |
| No matching rule → `404 Not Found` | Applicable | **Partial** | `platform/src/as_platform/sip/adapter.py:25` | A: contract scenario `S2-no-match-404` (`testbed/contracts/sip-baseline/README.md:13`) | Product path implemented; baseline captured by sippy, diff is E1 |
| Policy rejection → `603 Decline` | Applicable | **Partial** | `platform/src/as_platform/sip/adapter.py:24`; anti-fraud over-limit `apps/anti-fraud/src/as_anti_fraud/decision.py:152-156` | A: contract scenario `S3-policy-reject-603` (same README L14) | See §3.8 for the 603/608 divergence |
| Two-leg B2BUA (two legs with independent Call-ID) | Applicable | **Partial** | `platform/native/resip_runtime/runtime_module.cxx:1057-1103` | A: `platform/tests/test_resip_two_leg_integration.py`, `test_m7_forward_two_leg_integration.py` | REQ-F-1 = automated subset covered / full text still open: Wave 2 normalized diff covers the two-leg skeleton sequence, C_in ≠ C_out, SDP offer byte-identical (`testbed/e2e/test_s1_replay_contract.py`); the 14-message line-by-line header diff is not done (2026-10-12 update, originally "14-message full-text replay not signed off") |
| S-SBC transparent bridging | **Not applicable** (operator side) | **N/A** | — | Simulator `testbed/simulators/src/as_simulators/bridge.py:1-6` | Rationale: S-SBC is an operator network element, not our deliverable (ADR-0003) |
| Release applicability | — | **open** | — | D: no text in repo | Fill in after manual retrieval and line-by-line check of the spec text |

### 3.2 3GPP TS 29.228 / 29.229 —— Cx

| Capability item | Applicability | State | Basis |
|---|---|---|---|
| Cx (Diameter S-CSCF ↔ HSS) | **Not applicable** | **N/A** | **Rationale**: Cx is the interface between HSS and S-CSCF, an **internal operator-network-element interface**; the AS sits outside the IMS network and is ISC-triggered by the S-CSCF through the S-SBC, and does not establish a Diameter session with HSS (`AGENT.md` §1 "implement only the external AS"; [`../architecture/system-architecture.md`](../architecture/system-architecture.md) §9.2 lists "Diameter Sh interface" among explicit exclusions). The repo has **no Diameter/Cx code or config hit**. |

### 3.3 3GPP TS 29.328 / 29.329 —— Sh

| Capability item | Applicability | State | Basis |
|---|---|---|---|
| Sh (Hx / Diameter Sh / SWx related subscription data) | **Not applicable** | **N/A** | **Rationale**: the AS's business data comes from its **own data plane** (rule set, number-translation table, anti-fraud limits), so it need not query subscription data from HSS, hence no Diameter Sh (`AGENT.md` §2 non-goal "no Diameter Sh. Data comes from our own data plane"; [`../architecture/system-architecture.md`](../architecture/system-architecture.md) §9.2 L480). Review G-P0-4 adjudicated: Grafana dashboards and alerts contain **no Sh**, and the compliance matrix marks Sh as N/A ([`../reviews/product-packaging-plan-review-2026-10-09.md`](../reviews/product-packaging-plan-review-2026-10-09.md) L352). |

### 3.4 3GPP TS 32.260 / 32.299 —— billing / CDR

| Capability item | Applicability | State | Basis |
|---|---|---|---|
| Call record (CDR) generation, delivery, archiving | **Not applicable** | **N/A** | **Rationale**: no collection, delivery, archiving, or rating (`AGENT.md` §2; ADR-0017 accepted). Replaced by a Call-ID-based call trace for complaint tracing and anti-fraud evidence ([`one-pager.md`](one-pager.md) §2 "Call records" row). |
| Billing network-element interaction, CDR distribution | **Not applicable** | **N/A** | **Rationale**: billing data belongs to the operator's billing domain; an out-of-network third-party AS does not intervene (same as above; [`../architecture/system-architecture.md`](../architecture/system-architecture.md) §9.2 L478). |

### 3.5 GSMA IR.92 / IR.94

> **Whole-section state: open (to be confirmed line by line after manual retrieval of the spec text)**. The repo **does not retain the IR.92 / IR.94 text** (no `docs/specs/` directory, see §3.1 note), nor is there line-by-line implementation evidence. The table below **only describes the scope such documents typically cover**, and **contains no clause-number assertion and no "already compliant" conclusion**. Rewrite line by line per §1.3 evidence tiers after retrieving the text.

| Scope (typically covered, not a clause assertion) | Applicability | State | Indirectly referenceable repo facts | Blocker |
|---|---|---|---|---|
| IR.92: IMS profile / interoperability (IMS terminal and network-side interop behavior, parameter values) | Applicable | **open** | No direct implementation evidence; `platform/src/as_platform/sip/message.py:38-48` only implements RFC 3261 mandatory headers and magic cookie | Pending manual check of spec text |
| IR.94: media and security baseline (including bearer and security requirements) | Partially applicable | **open** | This product does **no media** (`AGENT.md` §2, ADR-0004), so most of IR.94's media-side clauses are not applicable; the security side has only allowlist + end-to-end TLS (ADR-0016) | Pending manual check of spec text + need to first adjudicate which clauses become N/A with "no media" |

### 3.6 RFC 3261 —— SIP

#### 3.6.1 Methods

| Capability item | Applicability | State | Implementation location (file:line) | Evidence | Notes |
|---|---|---|---|---|---|
| Initial INVITE (UAS in-leg) | Applicable | **Partial** | `platform/native/resip_runtime/runtime_module.cxx:979-1055` | A: `platform/tests/test_resip_runtime_log_contract.py` etc. | REQ-F-1 = automated subset covered / full text still open (Wave 2 normalized diff; the 14-message line-by-line header diff not done, 2026-10-12 update, originally "14-message full text not signed off") |
| ACK | Applicable | **Partial** | Handled by DUM; under the `accept_all_invites` harness, fixed 100/180/200/ACK (`platform/src/as_platform/sip/README.md:7-8`) | C: harness nature | `accept_all_invites` is testbed-only, **not the production path** |
| BYE | Applicable | **Partial** | In-leg BYE → out-leg `end()`: `runtime_module.cxx:1117-1140` | A: `platform/tests/test_d10_req_nf1_redis_integration.py` (post-recovery in-dialog BYE) | The recovery path has an engineering implementation; the **product path is un-accepted** |
| CANCEL (caller abandons, including 487 branch) | Applicable | **Partial** | `runtime_module.cxx:1226-1242` (the `early_cancel_harness` keeps the early state); for B2BUA CANCEL see `README.md:19` | A (harness form only) + C | Race (S11) baseline missing, see §4 |
| REFER / call transfer | Applicable | **open (not implemented)** | `runtime_module.cxx:1251-1260`: `onRefer` / `onReferNoSub` / `onReferRejected` / `onReferAccepted` are **all empty implementations** | A (empty implementation is itself evidence) | ADR-0019 §5.1 lists REFER as a non-threshold scenario to be filled in |
| forking | Applicable | **open (not implemented)** | `runtime_module.cxx:1182`: `onForkDestroyed` empty | A (empty implementation is itself evidence) | ADR-0019 §5.1 |
| 3xx redirect | Applicable | **open (not implemented)** | `runtime_module.cxx:1183`: `onRedirected` empty | A (empty implementation is itself evidence) | ADR-0019 §5.1 |
| PRACK / UPDATE interleaving | Applicable | **open (not implemented)** | Product code has no corresponding handling branch | D: no hit | ADR-0019 §5.1 |
| re-INVITE (hold / resume) | Applicable | **open (not implemented)** | `platform/src/` has no hold/resume business branch; only the D10 probe recovered an in-dialog re-INVITE (ADR-0022 Evidence) | C (probe, not product code) | ADR-0019 §5.1 |

#### 3.6.2 Status codes

| Capability item | Applicability | State | Implementation location (file:line) | Evidence | Notes |
|---|---|---|---|---|---|
| `404 Not Found` | Applicable | **Partial** | `adapter.py:25,145-146` | A: contract scenario S2 | — |
| `603 Decline` | Applicable | **Partial** | `adapter.py:24,142-143` | A: contract scenario S3 | See the 603/608 divergence in §3.8 |
| `403 Forbidden` (in-leg unauthorized) | Applicable | **Partial** | `platform/src/as_platform/sip/resip_runtime.py:39,334-346` | A: `platform/tests/test_resip_runtime_integration.py:151`, `test_resip_runtime_tls_policy_integration.py:175-196`, `test_resip_runtime_tls_integration.py:222` | Plaintext rejection and allowlist miss **share** 403 |
| `500` (exception / no route) | Applicable | **Partial** | `runtime_module.cxx:1044,1051` | A | Two paths: callback throws exception and `statusCode == 0` |
| Downstream non-2xx **pass-through set {408, 480, 486, 503, 504}** | Applicable | **Partial** | `platform/src/as_platform/sip/call_controller.py:19-21,98-104`; native same logic `runtime_module.cxx:466-484` | A (Python side) + A (native-side mapping function) | **The native product path has an end-to-end test only for `486`** (`test_resip_two_leg_integration.py`, `test_m7_forward_two_leg_integration.py`); the other four codes have no product-path evidence |
| All other 4xx–6xx uniformly mapped to `502 Bad Gateway` | Applicable | **Partial** | `call_controller.py:20,100-104`; `runtime_module.cxx:479-483` | B | **Partial rationale**: the mapping rule is implemented and has a unit test, but the product path has no end-to-end verification for codes outside the pass-through set. Also note: the independent two-leg spike has a narrower scope (`platform/native/resip_two_leg/two_leg_module.cxx:358` maps only `486`, everything else 502) — **the spike is not the production adapter** |
| `487 Request Terminated` | Applicable | **Partial** | `runtime_module.cxx:1226-1242` (harness keeps early state so DUM returns 487) | A (harness) + C | The full semantics of both branches on the product path await E1 |
| Other 1xx/2xx/3xx codes | Applicable | **open** | — | D | Not checked line by line |

#### 3.6.3 Header fields

| Capability item | Applicability | State | Implementation location (file:line) | Evidence | Notes |
|---|---|---|---|---|---|
| Request mandatory headers (To / From / CSeq / Call-ID / Max-Forwards / Via) | Applicable | **Partial** | `platform/src/as_platform/sip/message.py:44-45,369-378` | A: `platform/tests/test_sip_message.py` | Missing → `ValueError`, no incomplete request sent |
| `Via` branch magic cookie `z9hG4bK` | Applicable | **Partial** | `message.py:47-48,381-388` | A | The module **does not generate** branches (forbidden to read the clock / take randomness, ADR-0002) |
| `Content-Length` overwritten by body byte count | Applicable | **Partial** | `message.py:41-42,314-327` | A | Overwrite is in place, preserving caller field order |
| Body byte-for-byte pass-through (SDP not re-encoded) | Applicable | **Partial** | `message.py:12-16,72-73,442-458`; native forward `runtime_module.cxx:1204-1205` | A: `platform/tests/test_req_f4_sdp_identity_integration.py` | REQ-F-4 **acceptance incomplete** ([`../plan.md`](../plan.md) §5.2 D11) |
| Duplicate headers kept duplicate (not folded) | Applicable | **Partial** | `message.py:61-78,214-254` | A | Carried as a `(name, value)` sequence |
| Route consumption / Record-Route route-set extraction | Applicable | **Partial** | `runtime_module.cxx:840-856` (`buildRouteSetList`), `:606,645,699` | A (extraction) + D (flip-leg behavior end-to-end) | Baseline S8 covered by the same S1 capture; S9 missing (§4) |
| Out-leg `Request-URI`: only user changed, host/port from `AS_SIP_NEXT_HOP` | Applicable | **Partial** | `apps/translation/src/as_translation/outbound.py:43-52,63-88` | A: `apps/translation/tests/` | TLS uses `sips:`; user rewrite happens only on a TRANSLATE decision |
| `Contact` rewritten to TLS port in TLS scenarios | Applicable | **Partial** | `runtime_module.cxx:51-91` (`TransportContactDecorator`), mount point `:1456` | B (code) + C (testbed A/B reload record) | Only rewrites the first Contact of the **response**: `scheme=sips` + `port`, and removes the `transport` parameter |
| Whether the AS itself inserts Record-Route | Applicable | **open** | Product code does not explicitly set it (`runtime_module.cxx` has no Record-Route insertion point) | D | Behavior is decided by DUM default; needs manual check of the spec text to confirm expectedness |
| `Diversion` / `History-Info` / `Replaces` / `Privacy` | Applicable | **N/A** | Code has no hit | D (grep no match) | **Rationale**: this product only does number translation and anti-fraud decisions; it does not process call Diversion / history-info / call-transfer replacement / privacy identity. These appear only in the POC capture-baseline text as operator-side fields; product code neither parses nor rewrites them |
| `P-Asserted-Identity` | Applicable | **open** | Product runtime does not parse it; the simulated SUT reads it to get the caller (`testbed/simulators/src/as_simulators/sut.py:183-184`); the checkpoint header-extension mechanism uses it as a test sample (`platform/tests/test_call_state_checkpoint.py:82`) | B/C | **Not N/A**: ADR-0019 §5.1 lists "P-Asserted-Identity and trust-domain allowlist validation" as a **scenario to be filled in**; the product-path allowlist validation target is the **certificate fingerprint / IP**, not PAI |

#### 3.6.4 Dialog and B2BUA

| Capability item | Applicability | State | Implementation location (file:line) | Evidence | Notes |
|---|---|---|---|---|---|
| B2BUA: UAS leg and UAC leg independent, each with its own Call-ID | Applicable | **Partial** | `runtime_module.cxx:1057-1103`; `call_controller.py:31-49` | A: `platform/tests/test_resip_two_leg_integration.py` | After recovery the leg identifier is rebuilt from the checkpoint: `call_controller.py:236-255` |
| Leg association and in-flight state cleanup | Applicable | **Partial** | `call_controller.py:115-120,170-230` | A: `platform/tests/test_call_controller.py` | The controller is **in-memory state**; the recoverable context is a single checkpoint |
| Independent Via / transaction timer per leg | Applicable | **Partial** | Owned by DUM / `SipStack` (ADR-0022 Decision) | C | The controller does not re-implement retransmission and timers |

#### 3.6.5 CANCEL and 487

| Capability item | Applicability | State | Implementation location (file:line) | Evidence | Notes |
|---|---|---|---|---|---|
| In-leg CANCEL → `200 OK`, and sends CANCEL downstream | Applicable | **Partial** | `platform/src/as_platform/sip/README.md:18-19`; `runtime_module.cxx:1226-1242` | A (harness form) | Product-path semantics depend on DUM behavior, no product-path end-to-end sign-off yet |
| Caller abandons → `487` | Applicable | **Partial** | Same as above | A (harness) + C | ADR-0022 records DUM returning 200/487 to an in-leg initial INVITE CANCEL and reporting `RemoteCancel` |
| CANCEL vs final-response race (S11) | Applicable | **open** | — | D | POC has no race test, baseline missing (§4) |

#### 3.6.6 in-dialog requests

| Capability item | Applicability | State | Implementation location (file:line) | Evidence | Notes |
|---|---|---|---|---|---|
| Post-recovery in-dialog BYE sent downstream per Route | Applicable | **Partial** | `call_controller.py:257-262`; `runtime_module.cxx:1117-1140` | A: `platform/tests/test_call_controller_recovery.py`, `test_d10_req_nf1_redis_integration.py` | **Engineering slice, not REQ-NF-1 sign-off** ([`../plan.md`](../plan.md) §5.2 D10) |
| Other in-dialog requests (re-INVITE / UPDATE / INFO / MESSAGE / NOTIFY) | Applicable | **open** | `runtime_module.cxx:1244-1250` callbacks empty | A (empty implementation is itself evidence) | Consistent with the §3.6.1 methods table |

#### 3.6.7 Transport and TLS

| Capability item | Applicability | State | Implementation location (file:line) | Evidence | Notes |
|---|---|---|---|---|---|
| SIP over UDP `5060` | Applicable | **Partial** | `deploy/helm/values.yaml:150-153`; `platform/src/as_platform/runtime/sip_stack_service.py:168-169` | A (helm chart-check / values) | Port is a protocol constant, not a capacity number |
| SIP over TLS `5061` | Applicable | **Partial** | `deploy/helm/values.yaml:153`; `sip_stack_service.py:171` | A | Same as above |
| SIP over TCP | Applicable | **Partial** | `sip_stack_service.py:157-159,170` (`AS_SIP_ENABLE_TCP` on, port from `AS_SIP_TCP_PORT` / `SIP_LISTEN_PORT`, default `0` = do not listen) | A | **TCP off by default**. Also note: `deploy/docker/Dockerfile:37` exposes `5061/tcp` as a container port, inconsistent with the values.yaml criterion that `5061 = TLS` — a documentation/packaging scope open item |
| When TLS required, plaintext rejected before parsing | Applicable | **Partial** | `platform/src/as_platform/sip/ingress.py:24,178-194`; call site `resip_runtime.py:296-298,334-335` | A | Plaintext rejection happens **before** `decide()` and message parsing |
| Certificate hot-rotation (no restart, no dropped in-flight calls) | Applicable | **open** | Mechanism: `ingress.py:70-100` (overlap window), `runtime_module.cxx:1497-1501` (`SipStack::reloadCertificates()`), `runtime_module.cxx:1706-1720` (Python entry) | C (testbed-only smoke) | **E4 has no lab evidence → open** (ADR-0019 §6 step 5 item 2, §10; native TLS S1 once failed with 503 Certificate Validation Failure). **Do not** present it as having passed acceptance |

#### 3.6.8 Security

| Capability item | Applicability | State | Implementation location (file:line) | Evidence | Notes |
|---|---|---|---|---|---|
| Peer allowlist (IP / CIDR / `host:port` / certificate fingerprint) | Applicable | **Partial** | `platform/src/as_platform/sip/transport.py:48-63,249-298` | A: `platform/tests/test_transport_seam.py` | Certificate hit or address hit, **either** passes (ADR-0016) |
| Empty policy fail-closed | Applicable | **Partial** | `transport.py:257-273` | A | Helm side also has a render-time fail-closed switch `allowEmptyAllowlistForTest` (`values.yaml:162-165`), default `false` |
| Client certificate required by default (mTLS) | Applicable | **Partial** | `transport.py:75-93` (`require_client_certificate: bool = True`, and empty `ca_path` errors) | A | Exception: harness / simulation chain may turn it off |
| SRTP / media encryption | **Not applicable** | **N/A** | — | — | **Rationale**: no media, no SRTP (`AGENT.md` §2, ADR-0004: media needs are borne by the in-network MRF; the AS only gives decisions) |

#### 3.6.9 Other RFCs (SDP / MIN-SE / RTP-RTCP / RAck / Reason)

| Capability item | Applicability | State | Basis |
|---|---|---|---|
| RFC 4566 (SDP) | Applicable (pass-through only) | **Partial** | `platform/src/as_platform/sip/message.py:12-16` (body byte-for-byte pass-through, AS does not parse SDP); `NOTICE:34` registers it as pass-through only. Evidence A: `platform/tests/test_req_f4_sdp_identity_integration.py`. **REQ-F-4 acceptance incomplete** |
| RFC 3265 (`MIN-SE`) | Applicability TBD | **N/A** | **Rationale**: product code has no `MIN-SE` hit; session-timer capability belongs to DUM (ADR-0022 Decision), not implemented by the AS application layer |
| RFC 3325 (RTP/RTCP) | **Not applicable** | **N/A** | **Rationale**: no media (ADR-0004); code has no RTP/RTCP hit |
| RFC 3326 (RAck) | Applicability TBD | **N/A** | **Rationale**: reliable provisional responses are owned by the SIP stack's (`SipStack`) transaction layer; the AS application layer does not implement them (ADR-0022 Decision: the controller must not re-implement stack transactions and retransmission); code has no `RAck` hit |
| RFC 3428 (`Reason:` header) | Applicability TBD | **N/A** | **Rationale**: product code has no `Reason:` construction hit; failure is expressed by the status code itself (`call_controller.py:98-104`) |

> Every row in this table uses "no code hit → N/A" as the basis, and **does no spec-clause inference**.

### 3.7 RFC 6733 —— SIP Digest authentication

| Capability item | Applicability | State | Basis |
|---|---|---|---|
| HTTP Digest authentication (`WWW-Authenticate` / `Authorization` / nonce) | **Not applicable** | **N/A** | **Rationale**: the AS, as a signaling endpoint within the IMS trust domain, **does not implement digest authentication**; peer admission relies on the **TLS end-to-end + peer allowlist (IP/CIDR/certificate fingerprint)** combination (ADR-0016; `platform/src/as_platform/sip/transport.py:249-298`). The repo has **no digest / `WWW-Authenticate` / nonce handling hit** (the only `digest` in `platform/` appears in the FNV hash `platform/src/as_platform/gating/overrides.py:73` and certificate-fingerprint computation `runtime_module.cxx:224-232`, both unrelated to SIP digest auth). |

### 3.8 RFC 8688 —— ToS-SIP / `608 Rejected`

| Capability item | Applicability | State | Implementation location | Evidence | Notes |
|---|---|---|---|---|---|
| Capability declaration `+sip.608` | Applicable (passively appears) | **Partial** | Appears in the POC capture baseline's in-leg INVITE (`testbed/contracts/sip-baseline/S1-basic-call/01-in-invite-trunk.txt:19` etc.) | A (baseline text) | This is the **operator-side peer's** declaration; the AS itself does not emit this Feature-caps |
| Respond to anti-fraud/blocking decision with `608 Rejected` | Applicable | **open (not implemented)** | The product path **emits `603 Decline`** (`adapter.py:24,142-143`; anti-fraud over-limit `apps/anti-fraud/src/as_anti_fraud/decision.py:152-156`) | A | The decision-module comment explicitly classifies 608 as "the adaptor's concern, **not this module's**" (`decision.py:22-25`) |
| Documentation consistency | — | **open** | — | D | **Divergence note**: `608 Rejected (RFC 8688)` still appears in the descriptions of `apps/README.md:8`, `apps/anti-fraud/README.md:3`, `apps/anti-fraud/pyproject.toml:4`, and the POC-status description at [`../architecture/system-architecture.md`](../architecture/system-architecture.md) L80, inconsistent with the `603` the product code actually emits. **This matrix takes the code as authoritative**: the product path currently emits only `603`. Whether to add 608 requires a new ADR + contract change |

---

## 4. Test evidence baseline

### 4.1 Contract scenarios S1–S12 coverage

Per [`../../testbed/contracts/sip-baseline/README.md`](../../testbed/contracts/sip-baseline/README.md) (L10-31). The baseline was captured by **sippy** on the POC, recording only **externally observable message behavior**, not sippy API.

| Scenario | Content | Baseline state | Product-path evidence | Determination |
|---|---|---|---|---|
| S1 | Basic call INVITE→100→180→200→ACK→BYE→200 | ✅ captured | `accept_all_invites` harness covers in-bound 100/180/200 (with SDP) | Partial (REQ-F-1 = automated subset covered / full text still open: the 14-message line-by-line header diff not done, 2026-10-12 update) |
| S2 | No matching rule → `404` | ✅ captured | Goes through `decide()` | Partial |
| S3 | Policy rejection → `603` | ✅ captured | Goes through `decide()` | Partial |
| S4 | Caller abandons → CANCEL → `200 OK` → `487` | ✅ captured | `early_cancel_harness` keeps early state | Partial (harness form) |
| S5 | Two-leg B2BUA, two legs with different Call-ID | ✅ same S1 capture | `test_resip_two_leg_integration.py` | Partial |
| S6 | Request-URI rewrite | ✅ same S1 capture | `apps/translation/src/as_translation/outbound.py:63-88` | Partial |
| S7a | SDP fully passed through | ✅ same S1 capture | `test_req_f4_sdp_identity_integration.py` | Partial (acceptance incomplete) |
| S7b | SDP rewritten per contract | ❌ baseline missing (POC has no such function) | — | open |
| S8 | Route / Record-Route handling | ✅ same S1 capture | `runtime_module.cxx:840-856` extracts route set | Partial |
| S9 | in-dialog request routing | ⚠️ POC has chained probe, `capture_call.py` does not run, needs indirect inference | Post-recovery in-dialog BYE has an engineering test | open (baseline is indirect inference) |
| S10 | Non-2xx (`486` / `480` / `408`) branches | ❌ baseline missing (POC ReturnUas only returns 200) | Product path has an end-to-end test only for `486` | Partial (only 486) |
| S11 | CANCEL vs final-response race | ❌ baseline missing | None | open |
| S12 | TLS certificate hot-rotation (E4 hard constraint, not E1 threshold) | ❌ not done (ADR-0019 §6 step 5 item 2) | Testbed-only smoke only | **open (E4)** |

### 4.2 Decision contract

[`../../testbed/contracts/decision/`](../../testbed/contracts/decision/) is the **decision contract** (data, not a capture): `cases.json` has **14 cases** total, field semantics in its `README.md:29-79`.

- Decision outcome four values: `forward` / `translate` / `decline` / `not_found`; rule action three values: `forward` / `translate` / `block`, where `block` → `decline` (`README.md:46-49`).
- `applies_to` three values: `both` / `translation` / `anti-fraud`. The same input is **deliberately different** on TRANSLATE: the core leaves the out-leg number empty, filled back by the translation case, while anti-fraud **deliberately does not rewrite** (`README.md:63-78`).
- Replay: `uv run pytest -m contract -q` (`README.md:87-99`).
- Number normalization: separators have no routing meaning, missing `+` is filled with `+` (`README.md:80-85`).

### 4.3 Layering status (citation is restricted)

Per [`../acceptance/test-plan.md`](../acceptance/test-plan.md) L14-23:

- **① fast `unit or contract`**: with the `.so` present runs the real stack; **S1/S4 go through the `accept_all_invites` harness** (bypassing `decide()`), S2/S3 go through `decide()`.
- **② integration `integration`**: a real-stack subset — TCP/TLS, FORWARD two-leg, SDP, `test_product_path` (sim chain + rules, **no** accept-all).
- **③ e2e `e2e`**: **8 stably passing** (Wave 1 five `testbed/e2e/test_sip_first_edition.py` + Wave 2 three `testbed/e2e/test_s1_replay_contract.py`; when the native extension is missing they fail, not skip; 2026-10-12 correction, originally "0"); REQ-F-1 = automated subset covered / full text still open.
- **Capacity `performance`**: the M6 product-runtime load-test peer is the **accept-all harness**, **not** the business-decision path.

> `accept_all_invites` is **not** ims-sim, and **not** the production path; REQ-F-1's 14-message B2BUA is **not** signed off by the harness (`test-plan.md` L23, L31). **2026-10-12 correction (e2e scope)**: REQ-F-1 = automated subset covered / full text still open —— Wave 2 normalized diff covers the two-leg skeleton sequence, C_in ≠ C_out, SDP offer byte-identical (`testbed/e2e/test_s1_replay_contract.py`); the 14-message line-by-line header diff is not done.

---

## 5. Explicit non-goals list (N/A summary)

| Thing not done | One-line rationale | Basis |
|---|---|---|
| Media / RTP / transcoding / DTMF / MRF / media anchoring | Out-of-network media relay is triangular routing and touches voice compliance; playback is done by the in-network MRF; the AS only gives decisions | `AGENT.md` §2; ADR-0004 |
| CDR collection / delivery / archiving / rating | Replaced by a Call-ID-based call trace | `AGENT.md` §2; ADR-0017 |
| Lawful interception (LI) | IRIs belong to in-network elements; third-party AS intervention introduces cross-jurisdiction exposure | `AGENT.md` §2; [`../architecture/system-architecture.md`](../architecture/system-architecture.md) §9.2 |
| Diameter Sh (TS 29.328 / 29.329) | Data comes from own data plane, no HSS interaction | `AGENT.md` §2; review G-P0-4 |
| Diameter Cx (TS 29.228 / 29.229) | Cx is the HSS↔S-CSCF internal interface, an operator network element | §3.2 |
| Billing (TS 32.260 / 32.299) | Billing data belongs to the operator's billing domain | ADR-0017 |
| Multi-tenant | Operator delivery is itself one system per customer; single-tenant is natural physical isolation | `AGENT.md` §2 |
| GitOps for config | Do not require operator ops to learn Git to change a number range; config stored as PostgreSQL rows | `AGENT.md` §2; ADR-0006 |
| Write an Operator (CRD) | Helm + standard Deployment / ConfigMap / Secret are sufficient | `AGENT.md` §2; ADR-0013 |
| S-SBC transparent bridging | Operator-side network-element responsibility, not our deliverable | ADR-0003; [`../../testbed/simulators/src/as_simulators/bridge.py`](../../testbed/simulators/src/as_simulators/bridge.py) is only a simulation |
| SIP digest auth (RFC 6733) | Peer admission relies on TLS + allowlist, not digest challenge | §3.7 |
| iFC trigger / canary trigger by number-range percentage | Belongs to the S-CSCF/HSS side; the AS only implements the business decision after ISC trigger | [`../product-packaging-plan.md`](../product-packaging-plan.md) §1 deliverable 2.4; review G-P0-5 |

---

## 6. Open items and blockers

| Item | Blocker source | Impact surface | When closable |
|---|---|---|---|
| E1 (S1–S11 product-path real-socket diff) | Not executed; `docs/specs/` has no text, baseline captured by sippy, S7b/S9/S10/S11 missing | §3.1 / §3.6 / §4 entire-section state ceilings | M8 acceptance ([`../plan.md`](../plan.md) §5.1 O2/O3) |
| E4 (S12 TLS certificate hot-rotation) | No lab evidence; native TLS S1 once 503 Certificate Validation Failure | §3.6.7 Transport and TLS, §3.6.8 Security | M8 acceptance + operator PKI (REQ-S-2 / REQ-S-3) |
| E5 (state externalization and process-restart recovery) | Default DUM UAS restart test returns 481; no public UAS rehydrate API | §3.6.4 / §3.6.6 | After design-gap review; REQ-NF-1 stays a hard requirement (ADR-0022) |
| TS 24.229 clause-level compliance and Release applicability | Spec text not retained in repo | §3.1 all cells; all release-related judgments | Manual retrieval and line-by-line check |
| GSMA IR.92 / IR.94 | Spec text not retained in repo, no line-by-line implementation evidence | §3.5 entire section | Manual retrieval of text + first adjudicate which clauses become N/A with "no media" |
| Whether to implement `608 Rejected` | Documentation and code scope inconsistent (§3.8) | §3.8, §5 | New ADR + contract change + review |
| TCP port scope (Dockerfile `5061/tcp` vs values `5061 = TLS`) | Packaging scope not aligned | §3.6.7 | Maintainen adjudication then fix packaging docs |
| Whether `AS` should insert Record-Route | Product code does not explicitly set it; behavior decided by DUM default | §3.6.3 | Manual check of spec text + joint debugging with S-SBC |
| Acceptance items D10 / REQ-F-4 / REQ-S-4 etc. | Engineering slice ≠ REQ acceptance | §3.6.3, §3.6.6 | Line-by-line acceptance report + maintainer sign-off |
| ADR-0023 (Redis checkpoint), ADR-0025 (managed-plane compile contract) | Status still **draft** ([`../architecture/adr/README.md`](../architecture/adr/README.md) L39, L41) | When citing their design as evidence | After review passes |
| O1 capacity target | Unresolved | This document contains no capacity numbers; Datasheet capacity section (Class B) blocked | Maintainer adjudication |

---

## 7. Traceability

| Item | Content |
|---|---|
| Corresponding deliverable | [`../product-packaging-plan.md`](../product-packaging-plan.md) §1 first batch **1.2 (3GPP specification compliance matrix)**; Class A (not dependent on open items, see that doc §3.2) |
| Incorporated review comments | **G-P0-4** —— Sh-related dashboards / alerts removed from scope, compliance matrix marks Sh **N/A** (§3.3; also see plan doc §1 deliverables 2.1 / 2.2 deleted `sh-interface.json`)<br>**G-P1-6** —— matrix notes **E1/E4/E5 pending M8 acceptance**, **sippy is testbed baseline only** (see status block and §3.6.7) |
| ADRs cited | ADR-0003 (ISC single access semantics, accepted), ADR-0004 (media seam, accepted), ADR-0006 (config governance, accepted), ADR-0013 (Helm-only, accepted), ADR-0014 (layered testbed; testbed not a v1 deliverable), ADR-0016 (in-boundary security, accepted), ADR-0017 (no CDR, accepted), **ADR-0019 (SIP stack selection, accepted)**, ADR-0022 (product CallController atop DUM, accepted; D10/REQ-NF-1 still open); **ADR-0023, ADR-0025 still draft** |
| REQ / acceptance items cited | REQ-F-1 (14-message B2BUA), REQ-F-2 (two-leg Call-ID), REQ-F-3 (Request-URI), REQ-F-4 (SDP byte-identical), REQ-F-5 (Route/Record-Route), REQ-F-6 (404), REQ-F-7 (603), REQ-F-10 (non-2xx branch), REQ-NF-1 (restart without dropping calls), REQ-NF-5 (ISC semantics), REQ-S-1/S-2/S-3 (peer allowlist / operator PKI / certificate hot-rotation), REQ-NF-13 (log-field contract); E1 / E4 / E5 still open |
| Same-batch deliverables | [`one-pager.md`](one-pager.md) (1.1), [`ne-datasheet.md`](ne-datasheet.md) (1.3), [`responsibility-matrix.md`](responsibility-matrix.md) (3.3), [`version-lifecycle.md`](version-lifecycle.md) (3.5), [`security-privacy.md`](security-privacy.md) (3.4) **all landed** |
| Status discipline | This document only registers **evidence state**, and does not constitute an acceptance conclusion; M8 exit sign-off still on hold, **RC ready ≠ passed** ([`../acceptance/report.md`](../acceptance/report.md) §0) |

---

> **Before maintainer review, every `open` in this matrix must not be upgraded to "compliant" in external materials.** There is only one upgrade path: fill in **A-tier evidence** (product code + corresponding test `file:line`, or contract scenario number), and walk the full requirement → ADR → HLD/LLD → contract → acceptance → review record chain per `AGENT.md` §3.
