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

# Requirement List Review Record

> Reviewer: AI agent (grilling session + material provenance tracing)
> Date: 2026-09-28
> Review target: `docs/requirements/README.md` (first creation)
> Review conclusion: **Pass**

## Review Scope

Covers all decisions and POC baseline behaviors already done in the M0/M1 stages. In three categories:
- REQ-F functional requirements: from POC baseline S1-S11
- REQ-NF non-functional requirements: from known POC defects + AGENT.md red lines + ADR Context
- REQ-G governance requirements: from AGENT.md §3 + ADR-0020

## Review Method

Verify the source of each item clause by clause:
1. **Each REQ-F**: against the corresponding S-scenario README + message files in `testbed/contracts/sip-baseline/`
2. **Each REQ-NF**: against the Context section of the corresponding ADR + AGENT.md line numbers
3. **Each REQ-G**: against the AGENT.md original text

## Review Findings

### Gap 1: REQ-F-9/REQ-F-10/REQ-F-11 lack POC baseline

| Requirement | POC Status | Adjudication |
|---|---|---|
| REQ-F-9 in-dialog routing | POC has a chained topology, but capture_call.py is not run and there are no independent message samples | Accepted: marked as "to be supplemented in the M2 probe phase", does not block publication of the requirement document |
| REQ-F-10 non-2xx branch | POC ReturnUas only returns 200 OK, no busy branch | Accepted: same as above |
| REQ-F-11 CANCEL race | POC has no explicit race test | Accepted: same as above |

These three are **gaps in POC coverage itself**, not omissions of the requirement list.

### Gap 2: Existing ADRs do not cite REQ numbers

The existing ADRs (0001/0002/0003/0018/0019/0020) imply requirements in their Context sections, but do not explicitly write "this ADR responds to REQ-*".

| Adjudication | Status |
|---|---|
| Accepted: to be filled in uniformly when M2 starts | To be modified |

This catch-up does not retroactively modify the ADR bodies. The first change of M2 is:
1. Add a `corresponding REQ` metadata line to every existing ADR
2. Every REQ entry already has a corresponding ADR annotation (the forward link exists)

### Gap 3: No REQ-S-* (security requirements) category

AGENT.md mentions TLS (ADR-0019) and the certificate hot-rotation gap, but there is no independent security requirements chapter.

| Adjudication | Status |
|---|---|
| Accepted: it is already implied in the current NFR (REQ-NF-5 S-SBC bridging → implicit TLS coverage). If M2 introduces an externalized TLS component, add the REQ-S-* category | Closed |

### Gap 4: Capacity requirements were not formalized

The architecture document has capacity estimates, but there is no corresponding REQ-NF-* entry. AGENT.md L38 says "no capacity figures are published before M6 measurement", and the capacity targets themselves were not frozen in the M0/M1 stages.

| Adjudication | Status |
|---|---|
| Accepted: capacity requirements are assigned to M2, corresponding to independent O1 research | To be opened |

## Adjudication

| Gap | Source | Issue Summary | Adjudication | Fix Plan | Status | Verification Method | Notes |
|---|---|---|---|---|---|---|---|
| 1 | POC baseline | REQ-F-9/10/11 have no POC message samples | Accepted | the requirement document is marked "supplemented in M2" | Closed | the document annotation is checkable | Not a requirement omission, but a POC capability boundary |
| 2 | ADR consistency | Existing ADRs do not explicitly cite REQ numbers | Accepted (filled in M2) | M2's first change: add a `corresponding REQ` metadata line to all ADRs | To be modified | verified by the M2 commit | The forward link (REQ→ADR) already exists |
| 3 | Classification completeness | No REQ-S-* security category | Accepted | Already implicitly covered by the NFR; add as needed in M2 | Closed | document review | — |
| 4 | Capacity requirements | Capacity targets not formalized | Accepted | assigned to the M2 O1 research | To be opened | M2 O1 deliverable | AGENT.md L38 constraint |
| 5 | PRD rewrite | 8 corrections to the PRD's format/content (see Gap 5 below) | All accepted | All already implemented | Modified | PRD v0.1 file | 2026-09-28 maintainer change comments |
| 6 | PRD design stripping | The PRD mixes in design details + technical annotations that do not belong to requirements (see Gap 6 below) | All accepted | strip the design, delete technical annotations, create a design placeholder | Modified | PRD v0.1 file vs the design directory | 2026-09-28 maintainer review, second round |

## Gap 5 (PRD rewrite — maintainer change comments of 2026-09-28)

After the PRD was rewritten from an architecture quick-reference table into a formal top-down PRD, the maintainer raised the following 8 change comments, all of which have been implemented.

| # | Change Comment | Adjudication | Status |
|---|---|---|---|
| 1 | The signaling flow does not mark the protocol standards (RFC 3261 / 3GPP TS 24.229) | Accepted: all signaling REQs are annotated with RFC sections | Modified |
| 2 | "Corresponding ADR" should not be a field in the requirement — the order is reversed; the ADR should reference the REQ in reverse | Accepted: delete all "Corresponding ADR" from the PRD; keep the ADR's "responds to REQ" reverse link | Modified |
| 3 | Acceptance criteria should be in the testplan, not in the requirement | Accepted: create testplan.md, leave the placeholder `（验收标准见 testplan §X.X）` in the PRD | Modified |
| 4 | REQ-F-2's "two legs separated" is an implementation detail, not a requirement — it should say that a differing Call-ID is an RFC 3261 requirement of B2BUA | Accepted: rewrite in protocol language | Modified |
| 5 | REQ-F-6/F-7 lack business context — it is not clear which business scenario triggers them and why this response code was chosen | Accepted: add "when it triggers and why this response code is chosen" | Modified |
| 6 | A requirement should be a formal document, it should not be called README.md | Accepted: rename to prd.md + create a new README.md as the table of contents | Modified |
| 7 | Missing version number and date | Accepted: add v0.1 (draft) + 2026-09-28 + a version history table | Modified |
| 8 | Add the above content to the review record | Accepted: this table is the record | Modified |

## Gap 6 (PRD design stripping — maintainer's second round of changes, 2026-09-28)

After the PRD v0.1 rewrite was completed, the maintainer found during review that the PRD had mixed in design details and technical annotations. A requirements document should describe only "what is needed", not "how to do it". ADR decisions and implementation hints should be stripped out.

| # | Change Comment | Adjudication | Status |
|---|---|---|---|
| 1 | The PRD mixes in design: "PostgreSQL rows", "externalized Redis", "monorepo + uv workspace", "draining traffic diversion" are all ADR decisions, not requirements | Accepted: rewrite the business descriptions in pure requirement language | Modified |
| 2 | All 27 "technical annotation" paragraphs are design hints and should not be contained in a requirements document | Accepted: delete them all and move them verbatim to `docs/design/from-prd-notes.md` | Modified |
| 3 | Create a design placeholder directory to hold the stripped technical details for reference in the M2 design stage | Accepted: create new `docs/design/README.md` + `from-prd-notes.md` | Modified |

### List of Business Description Rewrites

The quoted text below is the exact wording of the PRD v0.1 under review and is kept verbatim.

| REQ | Original Design Hint | Rewritten Pure Requirement Language |
|---|---|---|
| REQ-NF-1 | "会话状态...绝对不能只存在于进程内存里" | "进程重启或故障时，正在进行的呼叫不能断——会话状态、对话状态、业务处理状态必须持久化在进程之外" |
| REQ-NF-2 | "不做阻塞事件循环（POC 的 sippy 模型）" | "一个业务用例一个进程" |
| REQ-NF-3 | "HPA 能基于 active_calls 和 cps 这两个自定义指标" | "支持水平扩展：业务量增加时能增加处理实例，不影响存量呼叫；业务量减少时能安全缩容" |
| REQ-NF-4 | "流程是：新版本副本就绪 → 旧版本副本标记 draining → active_calls 归零 → 副本下线" | "版本升级或配置更新时，正在进行的呼叫不能断。新请求路由到新版本进程，存量呼叫继续完成" |
| REQ-NF-6 | "保留一个 seam（接口定义）" | "保留一个扩展接口定义" |
| REQ-NF-10 | "配置版本存为 PostgreSQL 中的行...变更路径是：控制台 → 审批 → 写入 PostgreSQL → 灰度分发" | "配置变更必须经过审批流程。变更必须可版本化、可追溯、可灰度发布、可回滚。不要求运维人员为改配置去学 Git" |
| REQ-NF-11 | "`./VERSION` 文件是产品 release 版本的唯一源头...pyproject.toml 只携带接口语义化版本" | "产品有且只有一个版本号，所有组件声明自己的接口版本。不允许多个组件各有不同的 release 版本" |
| REQ-NF-12 | "用 `pyproject.toml` 的 `[tool.uv.workspace]` 统一管理依赖。各构建步骤不再需要 `git clone ../as_platform`" | "所有组件在一个仓库内。构建和容器构建不应因跨仓依赖而失败" |

### Content Retained

- RFC 3261 / 3GPP TS protocol references (these are protocol standards, not design)
- Product boundary positioning: single tenant, on-premises, S-SBC transparent bridging
- Non-goals: no media/CDR/LI/Diameter Sh
- REQ-F-2's B2BUA two legs with different Call-ID (stipulated by RFC 3261 §12.1)

## Gap 7 (PRD user stories — maintainer's second round of changes, 2026-09-28)

Add a user story/scenario section to the PRD so that non-technical readers can understand "who uses it and in what scenarios".

| # | Change Comment | Adjudication | Status |
|---|---|---|---|
| 1 | The PRD lacks user stories / use cases | Accepted: add a §1 user stories and scenarios section, 3 actors with 9 US in total | Modified |

### Adjudication

| Gap | Source | Issue Summary | Adjudication | Fix Plan | Status |
|---|---|---|---|---|---|
| 7 | Maintainer review, second round | The PRD has no user stories | Accepted | add a §1 section, and shift the original §1-5 to §2-6 | Modified |

## Gap 8 (PRD v0.2 revision — all 24 Gaps of prd-v0.1-review modified and written to disk)

After PRD v0.1 was published, an independent protocol re-review (prd-v0.1-review) found 24 Gaps (5 class-A protocol defects, 7 class-B coverage gaps, 12 class-C consistency cleanups). This Gap is the Adjudication follow-up of that re-review.

**Key point: overturns the M1 Gap 3 adjudication**. The M1 Gap 3 adjudication "security requirements are implicitly covered by REQ-NF" (i.e. a REQ-S-* category is not required) is judged invalid by prd-v0.1-review B5 —— REQ-NF-5 only talks about S-SBC bridging semantics and contains no security semantics; AGENT.md §13 explicitly says "the trunk is untrusted", and security cannot be implicit. That adjudication is now overturned, and §4 Security Requirements (REQ-S-1 through REQ-S-4) is added in PRD v0.2.

| # | Category | Summary | Adjudication | Fix Plan | Status | Verification |
|---|---|---|---|---|---|---|
| A1 | P0 protocol | REQ-F-8 BYE→487 direction is reversed | Accepted | Rewrite REQ-F-8 into two branches (early cancel CANCEL / dialog already established BYE), split the test-plan into three timing scenarios | Modified | prd-v0.2 REQ-F-8, test-plan §1.3-REQ-F-8 |
| A2 | P0 protocol | The REQ-F-2 Call-ID assertion direction is reversed (the same leg's Call-ID must be identical) | Accepted | The PRD business description stays unchanged (already correct); the test-plan is fully changed: inbound leg ≠ outbound leg + consistent within the same leg | Modified | test-plan §1.1-REQ-F-2 |
| A3 | P0 protocol | 7 wrong RFC section numbers | Accepted | Correct them one by one; add a "protocol section number notes" block at the head of the PRD | Modified | grep RFC sections across the whole of prd-v0.2 |
| A4 | P0 protocol | REQ-F-5 Route semantics are wrong (blindly copying the upstream Route header) | Accepted | Rewrite the business description as "consume the addressing this-hop Route + routing policy generates it explicitly"; change the test-plan acceptance | Modified | prd-v0.2 REQ-F-5, test-plan §1.1-REQ-F-5 |
| A5 | P0 protocol | REQ-F-11 CANCEL race only writes one branch | Accepted | Split into two branches (CANCEL arrives first / final response arrives first), add RFC 3261 §9.1/§9.2 references | Modified | prd-v0.2 REQ-F-11, test-plan §1.3-REQ-F-11 |
| B1 | P1 coverage | Missing the business-side user stories of Actor 4 | Accepted | Add Actor 4 + US-10 (translation query) + US-11 (anti-fraud query) | Modified | prd-v0.2 §1 |
| B2 | P1 coverage | Console/configuration management has no REQ-F | Accepted | Add new §2.4 Console and Configuration Management: REQ-F-12/13/14/15 | Modified | prd-v0.2 §2.4 |
| B3 | P1 coverage | The translation main path has no REQ | Accepted | Add new §2.5 Business Decision Chain: REQ-F-16 handling after a translation rule is hit | Modified | prd-v0.2 §2.5 |
| B4 | P1 coverage | REQ-F-6/F-7 matching semantics are ambiguous | Accepted | Append matching rules to REQ-F-6; append matching rules + priority to REQ-F-7 | Modified | prd-v0.2 REQ-F-6/F-7 |
| B5 | P1 coverage | No REQ-S-* (security requirements) | Accepted (**overturns the M1 Gap 3 adjudication**) | Add new §4 Security Requirements: REQ-S-1 through REQ-S-4 | Modified | prd-v0.2 §4 |
| B6 | P1 coverage | No observability requirements | Accepted | Add new REQ-NF-13 (OTel three signals), REQ-NF-14 (alert rule set) | Modified | prd-v0.2 §3.2 |
| B7 | P1 coverage | Trace retention period conflicts with plan.md O4 | Accepted | Change PRD + test-plan to "retention period to be decided — frozen in M4" | Modified | prd-v0.2 REQ-NF-7, test-plan §2-REQ-NF-7 |
| C1 | P2 consistency | US-1 "takes effect immediately" contradicts US-4 "takes effect after approval" | Accepted | Change US-1 to "submit → approve → take effect" | Modified | prd-v0.2 US-1 |
| C2 | P2 consistency | Governance P2 has no definition | Accepted | Add the P2 priority definition at the beginning of governance §5 | Modified | prd-v0.2 §5 |
| C3 | P2 consistency | US-9 mixes in design language (LoadBalancer) | Accepted | Change to requirement language | Modified | prd-v0.2 US-9 |
| C4 | P2 consistency | US-8 "recovers within 2 seconds" has no source | Accepted | Change to "calls are not interrupted" + "the latency commitment is to be frozen in M6" | Modified | prd-v0.2 US-8 |
| C5 | P2 consistency | §0 non-goals duplicate REQ-NF/S | Accepted | Add a formalize note at the end of §0 pointing to the corresponding REQ | Modified | prd-v0.2 §0 |
| C6 | P2 consistency | NF-4 ISSU attribution + out-of-order numbering | Accepted | Move REQ-NF-4 from §3.2 into the §3.1 core architecture constraint group | Modified | prd-v0.2 §3.1 |
| C7 | P2 consistency | AST scan attribution: `make gate` vs an extra step | Accepted | PRD REQ-G-3 + AGENT.md §9 clarified in sync: AST is outside the gate, it is an extra step / `make gate-strict` | Modified | prd-v0.2 REQ-G-3, AGENT.md §9 |
| C8 | P2 consistency | All PRD acceptance criteria are external-link placeholders with no identifier | Accepted | Add an "acceptance criteria status" declaration at the head of the PRD | Modified | prd-v0.2 header |
| C9 | P2 consistency | REQ-NF-6/7/8 are based on the ADR skeleton | Accepted | Add an ADR annotation at the end of each REQ | Modified | prd-v0.2 REQ-NF-6/7/8 |
| C10 | P2 consistency | The basis for F-9 routing is not rigorous (Via branch is transaction matching) | Accepted | Change to a dialog-matching formulation (Call-ID + tag) | Modified | prd-v0.2 REQ-F-9 |
| C11 | P2 consistency | The §1 "not covered" table's wording is inaccurate (business descriptions are already written) | Accepted | Change the table header to "user stories still missing + POC baseline" | Modified | prd-v0.2 §1 |
| C12 | P2 consistency | The test-plan REQ-F-8 CANCEL timing is inconsistent with baseline S4 | Accepted | The test-plan is split into three timing scenarios (before 180 / after 180 before 200 / after 200) | Modified | test-plan §1.3-REQ-F-8 |

### Adjudication Summary

| Category | Count | Adjudication | Status |
|---|---|---|---|
| A blockers | 5 | All accepted | All modified |
| B coverage gaps | 7 | All accepted | All modified (including the overturn of M1 Gap 3) |
| C consistency | 12 | All accepted | All modified |

## Review Conclusion

The requirement list passes. All 24 Gaps found by prd-v0.1-review were **adjudicated as accepted**, and the corresponding changes have all been written to disk into PRD v0.2.

**Special note**: in this Gap 8, prd-v0.1-review B5 **overturns** the requirements-m1-review Gap 3 adjudication that "REQ-S-* is implicitly covered by REQ-NF" —— security requirements must be formalized into traceable and acceptance-testable REQ-S-* entries. PRD v0.2 adds §4 Security Requirements to carry out this adjudication.

The reviewer confirms:
- The source of every REQ-F entry is traceable
- Every REQ-NF entry corresponds to an existing ADR
- The format conforms to the AGENT.md §3 definition
- The catch-up notes and the ADR's backward relationship are clear
- The overturning of M1 Gap 3 is recorded in this document
