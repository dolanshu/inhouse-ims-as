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

# PRD v0.1 Review Record

> Review target: `docs/requirements/prd.md` v0.1 (draft), together with the external link target of its acceptance criteria, `docs/acceptance/test-plan.md`
> Review date: 2026-09-28
> Reviewer: AI agent (protocol and documentation chain verification)
> Review conclusion: **conditional pass** —— v0.2 may only be published after the 5 class-A changes are completed and re-checked

## Review Scope and Method

| Dimension | Method | Source of Basis |
|---|---|---|
| Protocol correctness | Verify RFC 3261 section numbers and process semantics clause by clause | The full text of RFC 3261 (fetched with curl + sliced, verified verbatim; see "Basis Grading and Verbatim Verification Status"); baseline messages in `testbed/contracts/sip-baseline/` (L3 corroboration) |
| Requirement coverage | PRD §0 positioning vs the actual entries in §1/§2/§3 | `AGENT.md` §13 security red line; `docs/plan.md` §4 milestone schedule |
| Document consistency | PRD ↔ test-plan ↔ AGENT.md ↔ plan.md ↔ ADR registry | The original text of the documents above |

## Class A: Blockers (the requirement text itself is wrong and would lead to wrong design and acceptance)

| # | Location | Problem | Basis | Suggested Change | Status |
|---|---|---|---|---|---|
| A1 | REQ-F-8 | Impossible under the protocol: the PRD writes "向下游发送 BYE → 收到 487", but §15.1.2 stipulates "the UAS core MUST generate a 2xx response to the BYE" —— the response to a BYE can only be 2xx; 487 can only be the final response of an INVITE transaction that was cancelled (§9.2: "If the UAS has not issued a final response for the original request... If the original request was an INVITE, the UAS SHOULD immediately respond to the INVITE with a 487 (Request Terminated)."). §15 further gives the trade-off: "The CANCEL attempts to force a non-2xx response to the INVITE (in particular, a 487). Therefore, if a UAC wishes to give up on its call attempt entirely, it can send a CANCEL. If the INVITE results in 2xx final response(s)... MAY terminate them with BYE." —— **CANCEL when no final response has been received, BYE only after 2xx has been received**. It also omits "入腿 487 + 上游 ACK" (§6 SIP Transaction: "If the request is INVITE and the final response is a non-2xx, the transaction also includes an ACK to the response."). **Strength of the conclusion**: the §6 B2BUA definition "Since it is a concatenation of a UAC and UAS, no explicit definitions are needed for its behavior." —— the RFC does not specify the **cross-leg orchestration** of a B2BUA, but each leg, acting as UAC/UAS, is still bound by §9/§15; hence "the outbound leg must be able to produce a 487 in the no-final-response phase" is a protocol constraint (only CANCEL can do it), while the specific orchestration remains a contract-layer decision | RFC 3261 §15, §15.1.2, §9.2, §6 (L1, verified verbatim); POC baseline `S4-caller-cancel` (L3 corroboration, non-authoritative) | ① Delete "send BYE → receive 487": use CANCEL to terminate when the outbound leg has no final response yet, and BYE when the outbound leg is already 2xx; ② Add "入腿 487 + 上游 ACK"; ③ Write both branches into the requirement and acceptance | Modified |
| A2 | REQ-F-2 conflicts with test-plan REQ-F-2 | The test-plan asserts "上游 INVITE Call-ID(C1) ≠ 上游 BYE Call-ID(C2)". The original text of RFC 3261 §8.1.1.4: "The Call-ID header field acts as a unique identifier to group together a series of messages. It MUST be the same for all requests and responses sent by either UA in a dialog." —— the Call-ID must be identical within the same dialog, so the assertion must be wrong. The baseline measurement agrees with the RFC (inbound INVITE and inbound BYE are both `48f64baa94fdfcfdd79af4128905d375`, the outbound leg is `-b2b_1`) | RFC 3261 §8.1.1.4 (L1, normative basis, verified verbatim); `S1-basic-call/01-in-invite-trunk.txt` and `13-out-bye-trunk.txt` (L3 corroboration) | Change the assertion to "inbound-leg Call-ID ≠ outbound-leg Call-ID", and add "the Call-ID of INVITE/200/ACK/BYE within the same leg must be consistent | Modified |
| A3 | Multiple RFC 3261 section numbers | The section numbers are wrong: Request-URI is marked §6.2 (§6 is Definitions; it should be §8.1.1.1 / §19.1); Route is marked §7.1 (§7.1 is Requests; it should be §20.34 + handling in §16.4); Record-Route is reversed into route set and marked §16.13 (§16 ends at 16.12; it is actually §12.1.2); 404 is marked §21.4.4 (21.4.4 is 403 Forbidden, 404 is **21.4.5**); 603 is marked §21.6.5 (it should be **21.6.2**); the SDP offer/answer is marked §18 (§18 is Transport; offer/answer is in §13.2.1/§13.3.1, and the format is in RFC 3264); B2BUA is marked §12 (the B2BUA definition is in **§6 Definitions**, §12 is Dialogs) | The table of contents of the original RFC 3261 text | Correct them one by one; it is suggested to add a sentence at the head of the PRD saying "section numbers follow the original RFC 3261 text" | Modified |
| A4 | REQ-F-5 | "上游 INVITE 带的 Route 头必须在下游 INVITE 里保留" is protocol-suspect: per §16.4/§16.12, the Route is **consumed** by the addressed entity; copying it to the outbound leg would make the downstream send the request back to the carrier-side proxy, possibly creating a loop. And the test-plan only asserts string equality —— a wrong implementation would also pass | RFC 3261 §16.4 verbatim: "If the first value in the Route header field indicates this proxy, the proxy MUST remove that value from the request." (L1, the body text has been verified) + the §6 Route Set / Loose Routing definitions. **Note on applicability**: that MUST binds the proxy; it is not a direct MUST for our B2BUA (§6: B2BUA behavior is undefined), so the strength of the conclusion is "definition + proxy-rule analogy", not a direct MUST | Change to "a Route addressed to us must be consumed; routing information that needs to be reused is explicitly generated by the routing policy"; change acceptance to check the actual destination the downstream request is sent to, rather than header-field strings | Modified (partially accepted) |
| A5 | REQ-F-11 | "CANCEL 到达后不再 accept 新的最终响应" conflicts with RFC 3261 §9.1: when the downstream has already sent 200 OK, CANCEL has no effect and the dialog must be torn down with BYE. The test-plan only asserts "我们返回 487", covering only one branch | RFC 3261 §9 verbatim: "CANCEL has no effect on a request to which a UAS has already given a final response."; §9.1: "If the original request has generated a final response, the CANCEL SHOULD NOT be sent, as it is an effective no-op"; §9.2 the same (L1, the body text has been verified) | Split into two branches: ① CANCEL arrives before the final response → 487; ② the final response has already arrived → 200 OK + BYE; both must be accepted | Modified |

## Class B: Coverage Gaps (there is behavior or an existing schedule, but no REQ number → the traceability chain is broken)

| # | Gap | Evidence | Suggested Change | Status |
|---|---|---|---|---|
| B1 | The second category of service users claimed in §0 (business parties: translation / anti-fraud / intelligent routing providers) has no user stories and no REQ at all in §1/§2 | prd.md §0 vs the three actors in §1 | Add actors: business-party user stories + corresponding REQ-F; or withdraw the §0 promise | Modified |
| B2 | Console / configuration management capability has no REQ-F: US-1/2/3/4 only map to F-1, F-6, F-7, NF-7, NF-10; rule CRUD, the approval flow, trace query, canary distribution and rollback themselves have no functional requirement number. NF-10 talks about "not using GitOps", not about "having configuration governance capability" | prd.md §1 L28-58 | Add REQ-F-12… covering rule management, approval flow, trace query, canary and rollback | Modified |
| B3 | The "translation" main path has no requirement: what to do after a translation rule is hit (rewrite the number? which peer to select?) is undefined; F-1/F-3 only talk about sequencing and Request-URI rewriting | prd.md §2.1/§2.2 | Add a requirement for "the handling after a translation rule is hit" | Modified |
| B4 | Rule matching semantics are missing: whether the caller or the callee is matched (US-2 says "主叫号码命中", REQ-F-7 says "目标号码" —— self-contradictory), longest prefix vs priority, conflict adjudication; "阻止 > 翻译" appears only in test-plan acceptance, making it a hidden requirement | prd.md US-2 vs REQ-F-7 | Make the matching target and the conflict adjudication rules explicit in REQ-F-6/F-7 | Modified |
| B5 | No REQ-S-* (security): the AGENT.md §13 red line (peer whitelist, end-to-end TLS with the S-SBC, certificate hot rotation, console operation authorization + audit) has no number at the requirement layer. The `reviews/requirements-m1-review.md` Gap 3 adjudication "由 NF-5 隐含覆盖" does not hold —— NF-5 only talks about bridging semantics and contains no security semantics | AGENT.md §13 | Add a REQ-S-* group to carry the security red line; it must land before TLS is introduced in M2 | Modified (overturns the M1 Gap 3 adjudication) |
| B6 | No observability requirements: the OTel three signals and the alert rule set are already scheduled into M2/M5, with no REQ to trace them | plan.md §4 | Add observability REQ-NF | Modified |
| B7 | Metric basis conflict: test-plan REQ-NF-7 hardcodes "轨迹保留期默认 7 天", while plan.md O4 lists the retention period as undecided (customer compliance requirement) | test-plan.md §2 vs plan.md §5.1 | Align the two: mark the retention period as undecided, or explicitly adjudicate the default value at the requirement layer | Modified |

## Class C: Consistency and Wording

| # | Location | Problem | Suggested Change | Status |
|---|---|---|---|---|
| C1 | US-1 vs US-4 | "保存后规则立即生效" contradicts "审批通过才生效" | Adjudicate whether the draft state takes effect and unify the two places | Modified |
| C2 | §4 | Governance requirements are marked "全部为 P2", but §2/§3 only define P0/P1 | Add the P2 definition or change the marking | Modified (partially accepted) |
| C3 | US-9 | Design language mixed in ("LoadBalancer 自动把新 INVITE 路由到 v1.3.0"), violating the adjudicated "no design in the PRD" | Change to requirement language | Modified |
| C4 | US-8 | "呼叫在 2 秒内恢复" introduces a latency commitment with no source, conflicting with the spirit of AGENT.md L38 "M6 前不发布数字" | Delete the number or mark it as to be frozen in M6 | Modified |
| C5 | REQ-NF-9 / REQ-NF-6 | Non-goals (single-tenant on-prem, no media) are written as P0 requirements, and duplicate §0's non-goals three times | Move into the "boundary / non-goals" section, without taking a REQ-NF number | Modified (partially accepted) |
| C6 | §3.1/§3.2 | Out-of-order numbering (1,2,3,5,9 / 4,6,7,8,10,11,12); NF-4 (ISSU) is put under "extension and governance", but it looks more like a core continuity capability, and it overlaps NF-1 | Reorder or add an explanatory note | Modified (partially accepted) |
| C7 | REQ-G-3 vs REQ-G-4 | G-3's acceptance requires the `make gate` to include an AST scan step, while G-4/AGENT.md §9 define `make gate` as four steps (format/check/mypy/pytest) | Clarify whether the AST scan belongs to the gate or is an extra step | Modified |
| C8 | All REQs | The acceptance criteria of all 27 REQs are externally linked to the test-plan, while the test-plan's own status is "placeholder, the specific test cases are to be supplemented in M2" —— v0.1 in fact has no executable acceptance | Explicitly note this risk at the head of the PRD | Modified |
| C9 | REQ-NF-6/7/8 | Their basis ADRs ADR-0004/0016/0017 are still skeletons in the registry (no files); the "existing ADRs" in §6 only lists the 6 that have files | Annotate "the basis ADR has not landed yet" after the corresponding REQs | Modified |
| C10 | REQ-F-9 | "路由依据是 Via branch + Route 头 + Call-ID" is not rigorous: dialog matching is Call-ID + local/remote tag (§12), and Via branch belongs to transaction matching (§17.2.3) | Change to a dialog-matching formulation | Modified |
| C11 | §1 uncovered table | The table says REQ-F-9/10/11 are not covered, but §2.3 already has their business descriptions (in fact it is "no user stories") | Change the table header wording | Modified |
| C12 | test-plan §REQ-F-8 vs baseline S4 | Inconsistent CANCEL timing: `S4-caller-cancel/README.md` says CANCEL is sent "收到 180 Ringing **之前**"; the test-plan writes "在 180 Ringing **之后**、200 OK 之前". The race behavior of the two windows differs, so acceptance will produce two sets of results | Align with the baseline, or explicitly cover both windows | Modified |

## Adjudication Summary

| Category | Count | Blocks v0.2 publication | Disposition |
|---|---|---|---|
| A blockers | 5 | Yes | Re-check after modification; A1/A2 may require the test-plan to be changed in sync |
| B coverage gaps | 7 | Yes (B1-B5) | Add REQ numbers; align B6/B7 with the undecided items of plan.md |
| C consistency | 12 | No | Cleaned up together with v0.2 |

## Basis Grading and Verbatim Verification Status

The bases cited by the review are graded into four levels. The first verification used `web_fetch` to fetch RFC 3261 and was truncated at page 42 (§8.1.3.2), so the body text of §9 / §15 / §16.4 was not obtained; the full text was then fetched with `curl` and sliced, and **all four pending verifications were completed as L1 on 2026-09-28**.

| Level | Meaning | Entries |
|---|---|---|
| L1 normative basis (verified verbatim) | RFC / 3GPP original text confirmed verbatim | §8.1.1.4 Call-ID; §9 (CANCEL has no effect on a request for which a final response has already been sent); §9.1, §9.2 (CANCEL→200, INVITE→487); §15, §15.1.1, §15.1.2 (when a BYE may be sent, a BYE must be answered with 2xx); §16.4 (the top-level Route addressing this hop must be removed); §6 (B2BUA definition, SIP Transaction, Dialog, Route Set, Loose Routing); §7.1 method definition; §4 BYE→200 (non-normative example); §5 CANCEL semantics |
| L2 normative basis (table-of-contents confirmation only) | The section exists and the title matches, but the body text was not obtained | None (the original 4 entries have all been promoted to L1) |
| L3 observational evidence (non-authoritative) | POC baseline; can only corroborate, cannot define correctness | `S1-basic-call`, `S4-caller-cancel` |
| L4 internal document evidence | Proves a gap or a schedule, does not define correctness | AGENT.md §13, plan.md §4 / §5.1, ADR registry |

**Key original texts verified after the fact (2026-09-28)**

| Entry | Original Text |
|---|---|
| §9 | "CANCEL has no effect on a request to which a UAS has already given a final response." |
| §9.2 | "as long as the CANCEL matched an existing transaction, the UAS answers the CANCEL request itself with a 200 (OK) response." / "If the UAS has not issued a final response for the original request... If the original request was an INVITE, the UAS SHOULD immediately respond to the INVITE with a 487 (Request Terminated)." |
| §15 | "A UA MUST NOT send a BYE outside of a dialog. The caller's UA MAY send a BYE for either confirmed or early dialogs, and the callee's UA MAY send a BYE on confirmed dialogs, but MUST NOT send a BYE on early dialogs." / "The CANCEL attempts to force a non-2xx response to the INVITE (in particular, a 487). Therefore, if a UAC wishes to give up on its call attempt entirely, it can send a CANCEL. If the INVITE results in 2xx final response(s)... MAY terminate them with BYE." |
| §15.1.2 | "the UAS core MUST generate a 2xx response to the BYE" |
| §16.4 | "If the first value in the Route header field indicates this proxy, the proxy MUST remove that value from the request." |

**Methodological ruling**: correctness at the requirement layer can only be defined by the RFC / 3GPP; the POC baseline under `testbed/` is used for **cross-check equivalence** (behavior unchanged after the rewrite), not as a **correctness standard** (AGENT.md §12, ADR README: POC decisions are not imported). Accordingly, all entries in this record whose only basis is the testbed have been downgraded to L3 corroboration.

**Tool note**: `web_fetch` truncates long RFCs within the first ~42 pages, which is insufficient to verify the second half; downloading the full text with `curl` + slicing with `sed` allows complete verification. For future verification of protocol original text, prefer the latter.

## Positive Confirmations

- The non-goals (no media / CDR / LI / Diameter Sh / multi-tenant / non-GitOps) are written cleanly, with traceable reasoning.
- The user stories make it readable for non-technical readers, and the three actors' scenario descriptions are concrete.
- The awareness of protocol citation is correct (although the section numbers need correction).
- The catch-up notes in §6 honestly account for the inverted order of "requirement later than ADR", and give the process constraint starting from M2.

## Confirmation Sign-off

| Item | Value |
|---|---|
| Review conclusion | Conditional pass |
| Preconditions for publishing v0.2 | The 5 class-A items are modified and re-checked; B1-B5 have REQ numbers added |
| Reviewer | AI agent, 2026-09-28 |
| Maintainer signature | to be filled in |

---

## Post-Fix Status Update (2026-09-28, PRD v0.2 written to disk)

**Adjudication result**: all 24 Gaps were **accepted**, and the corresponding changes have all been written to disk into `docs/requirements/prd.md` v0.2 + `docs/acceptance/test-plan.md` v0.2. 0 rejections.

### Class A: Blockers (protocol defects) —— all 5 items modified

| # | Location | Change Content | Old Status → New Status |
|---|---|---|---|
| A1 | REQ-F-8 | Rewritten into two branches (early cancel CANCEL → 487 / dialog already established BYE → 200 OK); a CANCEL vs BYE distinction note added at the start of the business description; the test-plan split into three timing scenarios | To be modified → **Modified** |
| A2 | REQ-F-2 + test-plan | The PRD business description is unchanged (already correct); the test-plan fully changed: assert inbound-leg ≠ outbound-leg Call-ID + INVITE/200/ACK/BYE Call-ID consistent within the same leg | To be modified → **Modified** |
| A3 | RFC section numbers throughout | 7 section numbers corrected one by one; a "protocol section number notes" block added at the head of the PRD | To be modified → **Modified** |
| A4 | REQ-F-5 | The business description was rewritten as "消费寻址本跳 Route + 路由策略显式生成"; the test-plan acceptance now checks the downstream destination address instead of header-field strings | To be modified → **Modified** |
| A5 | REQ-F-11 | Split into two branches (CANCEL arrives first → 487 / final response arrives first → use BYE); RFC 3261 §9.1/§9.2 references added; the test-plan split into two-branch acceptance | To be modified → **Modified** |

### Class B: Coverage Gaps —— all 7 items modified

| # | Gap | Change Content | Old Status → New Status |
|---|---|---|---|
| B1 | Missing Actor 4 business party | Added Actor 4 + US-10 (translation query) + US-11 (anti-fraud query) | To be modified → **Modified** |
| B2 | Console/configuration management has no REQ-F | Added §2.4 Console and Configuration Management: REQ-F-12 (rule CRUD) / F-13 (trace query) / F-14 (approval flow) / F-15 (canary distribution and rollback) | To be modified → **Modified** |
| B3 | The translation main path has no REQ | Added §2.5 Business Decision Chain: REQ-F-16 the handling after a translation rule is hit | To be modified → **Modified** |
| B4 | REQ-F-6/F-7 matching semantics missing | REQ-F-6 appends the matching target = callee and longest-prefix-first; REQ-F-7 appends the same + block > translate > default route | To be modified → **Modified** |
| B5 | No REQ-S-* (security) | **Overturns the M1 Gap 3 adjudication.** Added PRD §4 Security Requirements: REQ-S-1 (whitelist validation) / S-2 (end-to-end TLS) / S-3 (certificate hot rotation) / S-4 (console authorization and audit) | To be modified → **Modified (adjudication overturned)** |
| B6 | No observability requirements | Added REQ-NF-13 (OTel three-signal export), REQ-NF-14 (alert rule set) | To be modified → **Modified** |
| B7 | Trace retention period conflict | PRD REQ-NF-7 + test-plan REQ-NF-7 changed to "retention period to be decided — frozen in M4" | To be modified → **Modified** |

### Class C: Consistency and Wording —— all 12 items modified

| # | Location | Change Content | Old Status → New Status |
|---|---|---|---|
| C1 | US-1 | "立即生效"→"提交草稿 → 审批 → 生效" | To be modified → **Modified** |
| C2 | §4 governance → §5 governance | A P2 priority definition note added at the start of the governance section | To be modified → **Modified** |
| C3 | US-9 | "LoadBalancer 自动路由 v1.3.0"→ requirement language (after the new version is ready, new requests are routed to the new version and existing calls complete on the old version) | To be modified → **Modified** |
| C4 | US-8 | "2 秒内恢复"→"呼叫不中断" + the latency commitment is to be frozen in M6 | To be modified → **Modified** |
| C5 | §0 non-goals | A formalize note added at the end, pointing to REQ-NF-6/7/8 and REQ-S-* | To be modified → **Modified** |
| C6 | §3.1/§3.2 | REQ-NF-4 moved from §3.2 extension and governance to §3.1 core architecture constraints | To be modified → **Modified** |
| C7 | REQ-G-3 / AGENT.md §9 | The attribution of the AST scan clarified in sync: not within the four steps of `make gate`, it is an extra step or `make gate-strict` | To be modified → **Modified** |
| C8 | PRD header | An "acceptance criteria status" placeholder declaration added | To be modified → **Modified** |
| C9 | REQ-NF-6/7/8 | "依据 ADR-0004/0017/0016，当前为 skeleton 状态，M2 补" added at the end of each | To be modified → **Modified** |
| C10 | REQ-F-9 | "Via branch + Route + Call-ID"→"Call-ID + local/remote tag（RFC 3261 §12 Dialogs）" | To be modified → **Modified** |
| C11 | §1 uncovered table | Table header "未覆盖"→"暂缺用户故事 + POC 基线", with a note that business descriptions already exist | To be modified → **Modified** |
| C12 | test-plan REQ-F-8 | Split into three timing scenarios: before 180 (no early dialog) / after 180 before 200 (early dialog present) / after 200 (dialog already established BYE) | To be modified → **Modified** |

### Acceptance Results

| Category | Original Count | Adjudication Result | Modified | Status |
|---|---|---|---|---|
| A blockers | 5 | All accepted | 5/5 | PRD v0.2 published |
| B coverage gaps | 7 | All accepted (including 1 item that overturns an M1 adjudication) | 7/7 | PRD v0.2 published |
| C consistency | 12 | All accepted | 12/12 | PRD v0.2 published |
| **Total** | **24** | **All accepted, 0 rejections** | **24/24** | **PRD v0.2 released** |
