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

# Review Record — M8 内部版本批次 4：签收与评审

- **评审对象**：批次 4「签收与评审」产出
  - S-1 白名单：拒绝场景补测 + 「白名单变更经审批后生效」取证
    （`platform/tests/test_req_s1_whitelist_rejection.py` 新增 9 条 unit；
    证据 `docs/acceptance/artifacts/m5/2026-10-12/PASS-s1-whitelist-rejection-2026-10-12.txt`、
    `docs/acceptance/artifacts/m5/2026-10-12/FAILCLOSED-s1-whitelist-change-approval-not-wired-2026-10-12.txt`）
  - S-4 RBAC + 审计不可篡改：审计 append-only 验证 + RBAC 权限矩阵验证
    （`services/config-service/tests/test_req_s4_audit_immutability.py` 7 条 unit；
    `services/config-service/tests/test_req_s4_rbac_api_matrix_integration.py` 22 条 integration；
    证据 `PASS-s4-audit-append-only-2026-10-12.txt`、`PASS-s4-rbac-permission-matrix-2026-10-12.txt`）
  - 矩阵 17 个 `open` 行的逐行终态化草案：`docs/acceptance/m8-matrix-finalization-draft-2026-10-12.md`
  - 证据索引 `docs/acceptance/artifacts/m5/README.md`（+6 行：批次 5 的 4 行 + S-1 两行 + S-4 两行）
- **评审日期**：2026-10-12
- **评审人**：AI agent —— **仅评审与列出 gap，不签字**；本文全部裁决为**评审人建议**，须维护者确认后方可执行
- **评审范围依据**：`docs/handoff/2026-10-12-m8-scope-revision-internal-release-plan.md` §2.4；批次 4 提示词 `docs/handoff/2026-10-12-m8-batch4-prompt.md`
- **执行环境**：`dev-win03ib7niepf0`（已登记于 `docs/environments.md`）

---

## 当前状态（Current Status）

> 本节反映本批次工程改动的落盘现状与评审结论。

- **一句话结论**：S-1 拒绝场景补测通过、「白名单变更经审批后生效」能力经取证**不存在**（已 FAILCLOSED 登记，未实现）；S-4 两项补测（审计 append-only、RBAC 权限矩阵）均通过；矩阵 17 个 open 行已逐行给出终态建议 —— **7 行 pass / 10 行 defer**，**全部待维护者 M8 退出评审确认**，本批次不代签任何 REQ。
- **gap 统计**：P0 = 0；P1 = 0；P2 = 0（工程层无阻塞性 gap）。**待裁决项 7 条**（D4-01…D4-07），均属维护者裁决域，非工程 gap。
- **门禁**：`make gate` → `1174 passed, 249 deselected, 11 warnings`，**0 skipped**，exit 0；`tests/test_evidence_discipline.py` → `135 passed`，exit 0。
- **签字状态**：**未签**（签字为维护者的动作）。
- **未闭环项**：7 条待裁决（见 Adjudication 表）；S-1 行、F-16 行、NF-15 行各带一个「可转 pass 的条件」，需维护者先作出口径裁决。

---

## 1. 总体评价

本批次执行严格落在 §2.4「不代签」边界内：

- **S-1**：拒绝场景补测为真实单元级驱动（直接调用 `ResipRuntimeListener._on_invite`），六路拒绝路径钉住 403，并以 `received_at` 探针**正向断言 `decide()` 未执行** —— 这是把「白名单前置拦截」从代码结构断言推进到行为断言的关键一步。同时如实发现并钉住 `authorize_peer` 地址 / 证书两维度为 **OR**（地址命中即放行、不要求对端证书），并在证据中注明**不构成 mTLS 强校验背书**，未向上虚报。
- **S-1 的能力缺口**：`FAILCLOSED-s1-whitelist-change-approval-not-wired-2026-10-12.txt` 逐点取证（`ConfigBundle` 字段集、唯一可审批提案 `ManagedRuleChange` 只管规则、`gate.install` / `install_with_overlap` 无产品调用点、`load_transport_seam_from_env` 仅在构造时读一次），结论「能力不存在」有代码位置支撑；**并且如实登记了矩阵正文 L86 描述与代码事实的冲突**，只登记、不改矩阵 —— 符合纪律。
- **S-4**：把审计不可篡改与 RBAC 权限矩阵从「内核级 / 结构级」推进到「真 PG integration / HTTP 边界」两层，越权落痕（DENIED 审计行）有直连 DB 复核，403 断言精确到权限拒绝 detail 以排除 CSRF / 404 / 双人原则冒充的假绿。边界（结构断言 ≠ 数据库端实测、每权限仅一个代表性端点、越权落痕仅两格、不含外部 IAM / SSO 与运营商 PKI）均写入证据与草案。
- **矩阵终态化**：17 行逐行给理由，pass 一律要求本版新证据；无本版新证据的 F-8、F-16 与依赖外部环境的 NF-13、NF-14、D12/O5-HA 一律 defer，未强行补测、未拼凑证据。

---

## 2. Gap 清单

**工程层无 gap。** 以下为**需维护者裁决的事项**，不是本批次的工程缺口（每条均有明确出处与可核验证据）：

| ID | 事项 | 性质 |
|---|---|---|
| D4-01 | S-1「白名单变更经审批后生效」能力不存在，需二选一（纳入变更单＝v1.1 新 feature／或修订矩阵 L86 描述） | 维护者裁决（产品范围） |
| D4-02 | `authorize_peer` 地址 / 证书 OR 语义是否收紧为 AND | 维护者裁决（安全口径，不阻塞 D4-01） |
| D4-03 | 是否引入 `defer` 状态词、是否按草案 §3 改写矩阵计数 | 维护者裁决（矩阵口径） |
| D4-04 | F-16 非轨迹部分可否以 `make gate` 既有覆盖转 pass | 维护者裁决（证据充分性口径） |
| D4-05 | NF-15 是否收窄口径转 pass，或随批次 5 B5-04 一并裁决 | 维护者裁决（验收口径） |
| D4-06 | F-5（Record-Route 转发）、F-9（re-INVITE / UPDATE）、F-11（CANCEL 先于任何下游响应）是否 v1.1 立项 | 维护者裁决（立项） |
| D4-07 | 7 个 pass 建议在 M8 退出评审中逐行确认 | 维护者动作（签字） |

---

## 3. 一致性检查

| 检查项 | 计划 / 上游出处 | 结论 |
|---|---|---|
| S-1 评审现有工程证据 + 缺项补测 | §2.4 表第 1 行；批次 4 提示词 §1 | ✅ 已执行：拒绝场景 9 条 unit 新增并进 `make gate`；「变更经审批」取证 FAILCLOSED |
| S-4 评审 + 缺项补测（append-only、RBAC 矩阵） | §2.4 表第 2 行；批次 4 提示词 §2 | ✅ 已执行：7 条 unit + 22 条 integration（真 PG），既有 `test_postgres_audit_store_integration.py` 复跑 35 passed / 3 skipped |
| 矩阵 17 open 行逐行终态化，每行必带理由 | §2.4 表第 3 行 | ✅ 已执行：`m8-matrix-finalization-draft-2026-10-12.md` §1 共 17 行，逐行给理由与边界 |
| pass 须有本版新证据（三元组留档） | §2.4 表第 3 行 | ✅ 已执行：7 行 pass 均挂 2026-10-12 三元组；F-8 / F-16 如实写「无本版新证据，不构成三元组」 |
| 依赖 X1 或外部环境的行按理由转 defer | §2.4 表第 3 行 + 边界段 | ✅ 已执行：NF-13（X1 后置下一 release）、NF-14（真实触发待环境）、D12/O5-HA（restriction）均为 defer |
| 产出矩阵更新草案，**不直接改矩阵** | §2.4 边界；批次 4 提示词 §4 | ✅ 已执行：草案独立成文；`m8-test-plan-matrix.md` 未被改动（`git status` 中无该文件） |
| 不改 `report.md` 计数 | 批次 4 提示词「硬纪律」 | ✅ 已执行：`docs/acceptance/report.md` 未被改动 |
| 未改任何产品代码 | 批次 4 提示词「缺项补测只做工程层」 | ✅ 已执行：本批次新增文件全部为 `tests/` 下的测试与 `docs/` 下的文档/证据；生产代码零改动（S-1、S-4 取证均为只读核查，未实现该能力） |
| 不执行任何 git 写操作 | 批次 4 提示词「硬纪律」 | ✅ 已执行：无 add / commit / tag / push / branch / 改 remote；全部改动留工作树 |
| 不签收任何 REQ、不代签 | 批次 4 提示词「核心边界」 | ✅ 已执行：草案全部 7 个 pass 建议均标注「待维护者 M8 退出评审确认」；未出现「已签收 / 已通过 / REQ 级验收通过」表述 |
| 证据前缀与实际结论一致 | `docs/acceptance/artifacts/m5/README.md`「文件名即结论」 | ✅ 一致：`PASS-` 对应通过结论；`FAILCLOSED-` 对应「能力不存在 / 门禁待裁决」的显式拒绝登记 |
| FAILCLOSED 行已在索引标注「不是通过证据」 | 同上 | ✅ 已执行：索引 `README.md` 中 `FAILCLOSED-s1-whitelist-change-approval-not-wired-2026-10-12.txt` 行结论列写「**不是通过证据**」，并注明「agent 未实现该能力、不得计入通过清单」 |
| 环境名不写匿名的「本机」 | `docs/environments.md` 规则 (2)；`tests/test_evidence_discipline.py` 规则 5 | ✅ 已执行：本批次全部文档与证据使用 `dev-win03ib7niepf0` |
| review record 格式 | `AGENT.md` §3.2 / §3.3 + 既有 review 文档 | ✅ 已遵循：评审对象、日期、评审人、Current Status、Gap 清单、一致性检查、Adjudication、签字节 |

---

## Adjudication（裁决记录）

> 裁决为**评审人建议**，须维护者确认后方可执行；签字为维护者动作。状态列一律「**待维护者确认**」。

| ID | 来源 | 问题摘要 | 裁决（建议） | 修改方案 | 状态 | 验证方式 | 备注 |
|---|---|---|---|---|---|---|---|
| **D4-01** | 批次 4 S-1 取证 | 「白名单变更经审批后生效」能力不存在，而矩阵正文 L86 仍写「白名单变更走审批（F-14 联动）」 | 二选一：① 纳入变更单（属 v1.1 新 feature，本版不立项，S-1 行维持 defer）；② 修订矩阵 L86 该说法 —— 若选②，S-1 行可凭拒绝场景补测证据转 pass | 选①：另行起草 requirement → ADR → design → review；选②：由维护者或授权 agent 改矩阵 L86 描述 | 待维护者确认 | 选①查 v1.1 feature 流程登记；选②查矩阵 L86 文本 | 依据 `FAILCLOSED-s1-whitelist-change-approval-not-wired-2026-10-12.txt` |
| **D4-02** | 批次 4 S-1 补测发现 | `authorize_peer` 地址 / 证书两维度为 **OR**（地址命中即放行、不要求对端证书） | 是否收紧为 AND；如收紧属 v1.1 立项 | 已钉住现行为于 unit 用例并注明「不构成 mTLS 强校验背书」；收紧需立项 | 待维护者确认 | 单元用例断言方向随裁决改变 | 不阻塞 D4-01；与 REQ-S-2 / REQ-S-3（restriction）区分 |
| **D4-03** | 草案 §2 / §3 | 是否引入 `defer` 状态词；是否按草案 §3 改写矩阵计数 | 建议引入 `defer`（区别于 `blocked`＝restriction、`n-a`＝永不验收）并按 §3 改写 | 由维护者或授权 agent 改矩阵正文各行 status 与「状态统计」；`report.md` §0.5 随批次 6 E-1 同步 | 待维护者确认 | 矩阵 status 与计数逐行核对 | 若否决 `defer`，需改挂 `blocked` 或维持 `open`，计数口径随之变 |
| **D4-04** | 草案 §1 F-16 | 非轨迹部分（decide 翻译用例）无本版留档证据，只有 `make gate` 既有覆盖 | 建议：若接受「2026-10-12 `make gate` 1174 passed + 矩阵 L59 既有 decide 覆盖」为工程证据，则非轨迹部分转 pass | 转 pass 后轨迹联动部分仍随 F-13 保持不验收、永不记 pass | 待维护者确认 | 核对 `make gate` 运行记录与矩阵 L59 evidence 栏 | 承接维护者 2026-10-12「F-16 只签非轨迹部分」裁定 |
| **D4-05** | 草案 §1 NF-15 | harness 已落地并有实测，但明确未测饱和点；`performance` 层门禁终态（B5-04）未裁 | 二选一：① 口径收窄为「harness 落地 + 多副本实测」→ 转 pass；② 随批次 5 B5-04 一并裁决后决定 | 转 pass 则矩阵该行 evidence 栏须写明「非饱和点、非对外承诺」 | 待维护者确认 | 矩阵 NF-15 行 status / evidence 核对 | 四份证据文件均自述「不签收 REQ-NF-15」 |
| **D4-06** | 草案 §1 F-5 / F-9 / F-11 | 三项实现缺口（Record-Route 产品侧转发、re-INVITE / UPDATE、CANCEL 先于任何下游响应） | 建议按 v1.1 立项处理，本版不立项；三行维持 defer | 立项走新 feature 流程（requirement → ADR → design → review） | 待维护者确认 | 三份能力缺失登记文件 + v1.1 登记 | 承接 `FAILCLOSED-s9-reinvite-update-not-implemented`、`FAILCLOSED-s11-cancel-before-any-downstream-response`、`PASS-s8` 的 out-of-scope 节 |
| **D4-07** | 草案 §1 全部 pass 建议行 | 7 个 pass 建议（F-4、F-10、NF-2、NF-5、NF-9、NF-10、S-4）需逐行确认 | 建议在 M8 退出评审中逐行确认后方可计入矩阵 pass | 确认后由维护者或授权 agent 改矩阵 status 与签字栏 | 待维护者确认 | M8 退出评审记录逐行签字 | 「工程证据接受」≠ REQ 级验收通过 ≠ 里程碑签收 |

---

## 签字

- **签字状态**：**未签**。
- **授权基础**：无。本次评审由 AI agent 执行，仅产出 gap 清单与建议裁决；裁决与签字须由维护者作出（`AGENT.md` §3.2、§3.3）。
- **评审结论**：**有条件通过**。条件即上表 D4-01…D4-07 全部经维护者确认，且 D4-07 的 7 行在 M8 退出评审中逐行确认。

---

---

## 裁决结果（2026-10-13，维护者已决并授权代签）

> **授权来源**：维护者 2026-10-13 原话「**接受建议，授权你代签**」。
> Adjudication 表 D4-01…D4-07 **逐条登记为已决**，状态列由「待维护者确认」改为「**已决并执行**」。
> 落点为 `docs/acceptance/m8-test-plan-matrix.md` 的「M8 批次4 终态化代签（2026-10-13）」节。

| ID | 裁决（已决） | 采纳值 | 状态 |
|---|---|---|---|
| **D4-01** | S-1「白名单变更经审批后生效」二选一 | **① 修订矩阵 L86 描述** —— 删去「白名单变更走审批（F-14 联动）」这一无代码支撑的说法；「白名单纳入变更单」另立 **v1.1 feature 候选**，不阻塞 S-1 行 | 已决并执行 |
| **D4-02** | `authorize_peer` 地址 / 证书 OR 语义是否收紧为 AND | **本版接受 OR**（不改代码、不写 ADR）；收紧为 AND 列 **v1.1 安全增强候选**，需先确认 S-SBC 是否必带客户端证书 | 已决并执行 |
| **D4-03** | 是否引入 `defer` 状态词 + 按草案 §3 改写计数 | **采纳** —— 引入 `defer` 状态词，并按本节计数改写（原矩阵正文各行与「状态统计」保留不改，新值登记于矩阵追加节） | 已决并执行 |
| **D4-04** | F-16 非轨迹部分可否转 pass | **接受**「2026-10-11 `PASS-gate-native` + 2026-10-12 本批次收尾 `make gate` 1174 passed + 矩阵 L59 既有 decide 覆盖」为工程证据 → **非轨迹部分转 pass**（轨迹联动随 F-13 归 v1.1） | 已决并执行 |
| **D4-05** | NF-15 是否收窄口径转 pass | **随批次 5 B5-04 裁决 (b)**（M8 总审书面接受风险，本版不实现 `make gate` 阻塞层）→ **转 pass**；范围 = harness 落地 + 多副本实测，**不含饱和点、不含对外阈值** | 已决并执行 |
| **D4-06** | 三项实现缺口是否 v1.1 立项 | **F-5 / F-9 / F-11 定点 v1.1**（feature 或缺陷修复），**F-8 定点 v1.1 工程补测**；本版不立项、不实现 | 已决并执行 |
| **D4-07** | 十行 pass 建议逐行确认 | **十行 pass 建议已由维护者授权逐行代签**：F-4 / F-10 / F-16 / NF-2 / NF-5 / NF-9 / NF-10 / NF-15 / S-1 / S-4 | 已决并执行 |

**终态计数**（登记于矩阵追加节）：**pass 27 / defer 4 / blocked 9 / n-a 9 / open 0 / fail 0**。

### 签字

- **签字**：**agent 代签（维护者 2026-10-13 授权）；M8 里程碑未签，内部版本不签收。**
- **评审结论**：由「**有条件通过**」登记为「**有条件通过 —— 条件已满足并已执行**」（条件即 D4-01…D4-07 全部经维护者裁决并授权代签）。
- 本节签字为 **agent 代签**，**不是维护者亲签**；`docs/acceptance/report.md` §0.5 计数未动（归批次 6 E-1）；未执行任何 git 写操作；执行环境 `dev-win03ib7niepf0`。

---

（本记录为批次 4 评审 round 1；本批次不签收任何 REQ、不签收里程碑、不改矩阵任何行状态、不改 `report.md` 任何计数、未执行任何 git 写操作。）

> 更正（2026-10-13）：上一行是**代签前**的 round 1 声明。维护者 2026-10-13 已「接受建议、授权代签」，本记录的 D4-01…D4-07 已按上文「裁决结果」节执行，矩阵 17 行终态已随之落地（见 `docs/acceptance/m8-test-plan-matrix.md`「M8 批次4 终态化代签（2026-10-13）」节）。代签签字一律为「agent 代签（维护者 2026-10-13 授权）」，**M8 里程碑仍未签**（内部版本、不签收）。
