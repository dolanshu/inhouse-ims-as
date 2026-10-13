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

# M8 发布候选退出评审记录（2026-10-06）

- **评审对象（object）**：M8 发布候选（RC）退出，范围 = RC 计划 §3 退出条件 1–5（阶段 A–B 闭合、阶段 C v1 签收矩阵、阶段 D 环境 true blocker 结论、阶段 E 报告/版本/签字、本总审 + 里程碑签字表）。
- **评审日期（date）**：2026-10-06
- **评审人（reviewer）**：AI agent（维护者缺席期间用户指令 self-decision；**维护者会签 PENDING**，本记录不替代维护者签字，不构成关门结论）。
- **评审结论（conclusion）**：**RC就绪，defer项未清，不宣称全绿；维护者签字后方可关门**（不是"通过"）。

依据：[`2026-10-06-m8-release-candidate-plan.md`](../handoff/2026-10-06-m8-release-candidate-plan.md) §3 / §3.1 / §5、[`plan.md`](../plan.md) §4（M8 定义）/ §5（O/D 未决项）、AGENT.md §3.3（review record 格式）/ §10.4（tag 仅维护者）。

---

## 1. 退出条件逐项核对（RC 计划 §3 条件 1–5）

| # | 退出条件 | 本 RC 状态 | 结论 |
|---|---|---|---|
| 1 | 阶段 A–B 闭合：P1 尾项 + M5.1 / 全链复评达到维护者认可的 REQ 证据门槛 | A：F9 门禁本地就绪、F8 契约落地、F6 documented limitation、gate-strict + performance 阻塞 + runbook；B：MINIMAL M5.1、B-2 降级、B-3 L1，复评 REQ 级不通过 + 10 defer。**维护者认可待补** | 未闭合（待维护者） |
| 2 | 阶段 C：test-plan v1 范围内验收项有可追溯证据 | 矩阵 [`m8-test-plan-matrix.md`](../acceptance/m8-test-plan-matrix.md)：pass 9 / fail 0 / blocked 12 / n-a 4 / open 24；全部 `signed_by` 为维护者待签 | 未闭合（待签收） |
| 3 | 阶段 D：环境类 true blocker 有记录结论 | D-1/D-2 明确 defer，D-3 裁决 pending（建议 v1.1）；记录见 [`m8-environment-evidence.md`](../acceptance/m8-environment-evidence.md) | 记录齐备，终态待维护者 |
| 4 | 阶段 E：`report.md` 升级为 M8 发布候选报告；VERSION + CHANGELOG 与交付一致；`plan.md` §0 / §4 M8 行标记 | report.md §0 已升级（历史保史为附录）；VERSION 维持 `0.2.0`（未 bump，CHANGELOG 首标题一致）；plan.md §0 / §4 M8 行标 **RC就绪、待维护者退出签字**（未标已完成） | 产物就绪，签字待补 |
| 5 | Review records：M8 总审 + 各里程碑退出签字表 | 本文件即 M8 总审；签字表见 §4（M1/M2/M6/M7/M8，全为维护者待签） | 记录已建，签字待补 |

**总评**：5 项中无一项达到"维护者已确认"；RC 产物齐备可供评审，但**不得宣称为全绿或已关门**。

---

## 2. Issues 列表（签字前须逐项终态）

| # | Issue | 现状 | 终态要求 |
|---|---|---|---|
| 1 | **F9 门禁落地 pending** | 本地门禁配置就绪（blocking native 目标 + chart-check + gate-strict），尚未纳入必跑 | 维护者确认 `make gate-strict` 与 blocking 目标在本机可复现为绿 |
| 2 | **矩阵 24 open** | F-1/2/3/4/5/6/7/8/9/10/11/12/14/16、NF-2/5/9/10/13/14/15、S-1/S-4、D12/O5-HA；均有工程证据，待 M8 退出评审签收 | 维护者逐项签收或书面接受 |
| 3 | **矩阵 12 blocked** | F-13、5.4-F-13、F-15、5.4-F-15真AS、NF-1、NF-3、NF-4、NF-7、S-2、S-3、ADR-0008演练、D6；每项已指到 plan §5 / O1 / v1.1 / Phase D | 转终态（证据 / 有条件通过 / defer 授权） |
| 4 | **D-1 运营商 PKI / 外网 S-SBC** | 明确 defer（本环境无 lab 与对端） | 维护者排期采证或书面接受风险 |
| 5 | **D-2 客户 K8s NF-1 live** | 明确 defer（本环境无客户集群） | 同上 |
| 6 | **D-3（D6 testbed v1 验收）** | 维护者裁决 pending；本 RC 建议 v1.1 | 维护者书面裁决 v1 / v1.1 |
| 7 | **M5D 10 项 defer** | C-1、C-2、C-3、C-6、C-7、C-9、H-8、H-11、A-2、T-1（复评 §6；拟新增 M5D-1…M5D-6 由维护者落定） | 关闭或移出 v1（维护者书面） |
| 8 | **O1 容量目标裁决** | dev-host 实测为非 SLA；维护者目标裁决仍 open（plan §5.1 O1） | 维护者目标裁决 |
| 9 | **NF-3 验收口径** | test-plan 固定容量数字与 AGENT §2 冲突 | 维护者裁决改写口径或标 N/A |
| 10 | **D1 风险** | Python 3.10 EOL（2026-10），风险登记，不默认阻断 RC | 维护者确认接受为风险（或立项迁移） |

v1 明确排除重申（不计入全绿）：主叫/正则（v1.1）、PM/AM/UM 完整产品、D1、D10 极端扩展（mid-transaction / owner-CAS 极端）。

---

## 3. 里程碑签字表（E-5）

列定义：对象 / 结论 / 签字 / 日期 / 备注。**以下签字栏全部为维护者待签**；历史引用仅说明既有记录，不构成签字。

| 对象 | 结论 | 签字 | 日期 | 备注 |
|---|---|---|---|---|
| M1 甄别与行为基线 | 门禁达成（历史结论） | 维护者待签 | — | 历史记录 [`m1-exit-review.md`](m1-exit-review.md) 存在；文首 M1 §6 签字仍为历史项 |
| M2 内核 / transport-runtime | 工程完成（2026-10-05），REQ-S-* 验收未签 | 维护者待签 | — | 工程裁决见 `m2-engineering-closure-adjudication-2026-10-05.md`；REQ-S-2/S-3 尾项 D-1 defer |
| M6 容量研究 | 工程完成（2026-10-05），O1 目标未发布 | 维护者待签 | — | 工程裁决见 `m6-engineering-complete-adjudication-2026-10-05.md`；O1 裁决 open |
| M7 生产 SIP 集成 | 工程完成（2026-10-05），REQ-NF-1/E1 全量未签收 | 维护者待签 | — | 工程裁决见 `m7-final-engineering-adjudication-2026-10-05.md`；D10/REQ-NF-1 待 D-2 |
| M8 发布候选 | RC就绪，defer项未清，不宣称全绿（本记录结论） | 维护者待签 | — | 维护者签字 + tag 后方可关门（AGENT §10.4，仅维护者） |

另：M5 为**工程关门（2026-10-04，维护者 chat 授权代签；含义已降级为非 REQ 验收）**，REQ 级不通过（见 [`m5-req-acceptance-review-2026-10-06.md`](m5-req-acceptance-review-2026-10-06.md)）；M3/M4 工程结论见 report 附录历史，REQ 全绿归 M8 或维护者单独签收（plan §5.4）。

---

## 4. E-6 打包校验记录（本总审执行，2026-10-06）

| 检查 | 结果 |
|---|---|
| `uv run pytest tests/test_version_consistency.py -q` | **9 passed**；VERSION `0.2.0`，CHANGELOG 首标题 `== 0.2.0`，未新增版本节 |
| 密钥复检（新 M8 文档） | `BEGIN PRIVATE KEY` 零命中；`--password` / `passwd` 零命中 |
| `helm template` | 已覆盖，引用 `chart-check: OK`（形状证据，不重跑重型构建） |
| README/runbook vs `AS_SIP_*`/`AS_TLS_*` | 实现：`platform/src/as_platform/runtime/transport_env.py`；README 无 env 名（无错名）；runbook `AS_REQUIRE_NATIVE_EXTENSIONS=1` 与实现一致；记文档缺口（非阻塞），无 typo 可改 |
| 镜像 push/tag | 明确留给维护者（AGENT §10.4），未执行 |

---

## 确认（confirmation）

| 项 | 记录 |
|---|---|
| 评审结论 | RC就绪，defer项未清，不宣称全绿；维护者签字后方可关门（不是"通过"） |
| 自决策 | M8 Phase E 由 AI agent 在维护者缺席期间按 RC 计划 §4 Phase E（E-1…E-6）执行；用户指令 self-decision；所有签字均为维护者待签 |
| 维护者确认 | **待签字**（本栏须由维护者填写；本记录不构成关门结论） |
| 所需维护者动作 | (1) 确认 blocking 门禁目标与 `gate-strict` 本机可复现为绿；(2) 排期 D-1/D-2 环境采证或书面接受风险；(3) 裁决 D-3（D6）、O1 目标、NF-3 口径、M5D-1…M5D-6 行落定；(4) 完成 M1/M2/M6/M7/M8 退出签字；(5) 仅由维护者执行 tag（AGENT §10.4） |
| 输入评审 | [`2026-10-06-m8-release-candidate-plan.md`](../handoff/2026-10-06-m8-release-candidate-plan.md)、[`m8-test-plan-matrix.md`](../acceptance/m8-test-plan-matrix.md)、[`m8-environment-evidence.md`](../acceptance/m8-environment-evidence.md)、[`m5-req-acceptance-review-2026-10-06.md`](m5-req-acceptance-review-2026-10-06.md)、[`m8-phase-a-f6-f8-note-2026-10-06.md`](m8-phase-a-f6-f8-note-2026-10-06.md) |
| 未采信证据 | `artifacts/m8/` 占位目录（待采证，无证据效力）；`make gate` 本地绿仅为工程门禁，不替代 REQ 签收 |

---

## 3.1 里程碑签字栏代签填写（2026-10-12；§3 表原文保留不改，本节在其后追加填写结果）

> **授权来源**：维护者 **2026-10-12 明确授权由 agent 代签** M8 的 N2 九项书面裁决
> （N2 第 9 项 = M1 / M2 / M6 / M7 签**工程完成**；代签总记录见
> [`../handoff/2026-10-12-m8-n2-countersign-record.md`](../handoff/2026-10-12-m8-n2-countersign-record.md)）。
> **本节不是维护者亲签**，每行标注「agent 代签」并附依据。

| 对象 | 代签填写 | 日期 | 依据（不新造结论，只正式化既有结论） |
|---|---|---|---|
| **M1** 甄别与行为基线 | 结论维持「**门禁达成（有条件通过）**」；签字：**agent 代签（维护者 2026-10-12 授权）** | 2026-10-12 | [`m1-exit-review.md`](m1-exit-review.md) 文首评审结论「有条件通过，条件为 HLD/LLD 补建，已列入 M2 前置，**不回退 M1 结论**」；§6 历史签字项 |
| **M2** 内核 / transport-runtime | 结论维持「**工程完成（2026-10-05）**，REQ-S-* 验收未签」；签字：同上 | 2026-10-12 | `m2-engineering-closure-adjudication-2026-10-05.md`；REQ-S-2/S-3 尾项 D-1 defer |
| **M6** 容量研究 | 结论维持「**工程完成（2026-10-05）**，O1 目标未发布」；签字：同上 | 2026-10-12 | `m6-engineering-complete-adjudication-2026-10-05.md`；O1 裁决 open（2026-10-12 仅落「内部工程目标下限基线」，非目标值） |
| **M7** 生产 SIP 集成 | 结论维持「**工程完成（2026-10-05）**，REQ-NF-1/E1 全量未签收」；签字：同上 | 2026-10-12 | `m7-final-engineering-adjudication-2026-10-05.md`；D10 / REQ-NF-1 待 D-2 |
| **M8** | **未签** —— 本节不填 | — | M8 退出签字属收尾动作，**不在 N2 九项授权范围内** |

**边界（不得据本节推出过度结论）**

1. **「工程完成」≠「里程碑签收」≠「REQ 全绿」。** 四行签的都是**工程完成**这一层；
   `plan.md` §「M6 状态更新」所载「维护者 **M6 里程碑签收**仍 open」**原样保留**，
   `report.md` 的 open / blocked 计数**未改**。
2. M1 签的是「门禁达成（有条件通过）」，其条件（HLD/LLD 补建）原记录为「已列入 M2 前置」；
   本节**不重新判定**该条件是否已闭合。
3. §3 表原「以下签字栏全部为维护者待签」一句，因本节而部分失效（M1/M2/M6/M7 已由代签填）；
   该句**保留为历史**。**M8 行仍为维护者待签**。
4. 本文档文首「维护者会签 PENDING」与结论「RC就绪，defer项未清，不宣称全绿」**均不变**。

## 3.2 内部版收尾后的里程碑签字表状态（2026-10-13；§3 与 §3.1 原文保留不改）

> 本节只追加登记，§3 表与 §3.1 代签结果一字未改。

| 对象 | 状态 | 签字 | 日期 | 备注 |
|---|---|---|---|---|
| M1 | 工程完成 | agent 代签（维护者 2026-10-12 授权） | 2026-10-12 | §3.1 已填，本批次维持不变；「工程完成」≠ 里程碑签收 ≠ REQ 全绿 |
| M2 | 工程完成 | agent 代签（维护者 2026-10-12 授权） | 2026-10-12 | §3.1 已填，本批次维持不变；「工程完成」≠ 里程碑签收 ≠ REQ 全绿 |
| M6 | 工程完成 | agent 代签（维护者 2026-10-12 授权） | 2026-10-12 | §3.1 已填，本批次维持不变；「工程完成」≠ 里程碑签收 ≠ REQ 全绿 |
| M7 | 工程完成 | agent 代签（维护者 2026-10-12 授权） | 2026-10-12 | §3.1 已填，本批次维持不变；「工程完成」≠ 里程碑签收 ≠ REQ 全绿 |
| **M8** | **内部版本，不签收** | **未签 —— 维护者待签** | — | 本版 = 内部版收尾（function 完整 + 模拟器证据 + 可重复构建工件），**不是 M8 退出签字**；M8 退出签字排在外部硬依赖闭环之后。内部版收尾评审见 [`m8-internal-release-exit-review-2026-10-12.md`](m8-internal-release-exit-review-2026-10-12.md) |

**边界**：

1. 本节不签 M8，也不签任何 REQ。
2. `agent 代签（维护者 2026-10-12 授权）` 不等于维护者亲签。
3. 文首「维护者会签 PENDING」与结论「RC就绪，defer项未清，不宣称全绿」均维持不变。
4. 本批次未执行任何 git 写操作；commit 拆分与 tag 仍由维护者决定。

## 3.3 M8 退出签字（路径 C，2026-10-13；§3 / §3.1 / §3.2 原文保留不改）

> §3 表原「以下签字栏全部为维护者待签」与 §3.2 的 M8「内部版本，不签收」**保留为历史**。
> 本节登记维护者 2026-10-13 按**路径 C** 作出裁决后的**终态**：M8 里程碑要 close，路径为
> **签 M8 退出签字 + 同时书面接受外部硬依赖风险**。

| 对象 | 结论 | 签字 | 日期 | 备注 |
|---|---|---|---|---|
| **M8 发布候选** | **M8 退出签字 —— 含维护者书面接受外部硬依赖风险（路径 C）** | **agent 代签（维护者 2026-10-13 授权）**（**不是维护者亲签**） | `2026-10-13` | 前提文件 [`m8-external-dependency-risk-acceptance-2026-10-13.md`](m8-external-dependency-risk-acceptance-2026-10-13.md)；四项外部硬依赖（D-1 / D-2 / ADR-0008 演练 / D12-O5）**保持 `blocked`**、转下一 release；4 行 `defer` 与 F-13 / NF-7 转 v1.1 立项。**签字覆盖里程碑退出，不覆盖 REQ 级验收**（M5 REQ 级仍不通过）；不宣称 M8 全绿；矩阵 27 行 `pass` 口径仍为「工程证据接受」 |
| M1 / M2 / M6 / M7 | 维持 §3.1 的「工程完成（agent 代签，维护者 2026-10-12 授权）」 | agent 代签（维护者 2026-10-12 授权） | 2026-10-12 | 不受本节影响；「工程完成」≠ 里程碑签收 ≠ REQ 全绿 |

**边界**：

1. **本节不代签。** M8 退出签字栏**只能由维护者亲签填写**；本表该栏留空待填。此前所有代签授权（N2 九项、N3、批次 4）**均不含 M8 退出签字**。
1-bis. **2026-10-13 授权更正**：维护者已就 **M8 退出签字栏**显式下达「**授权代签**」指令。上述第 1 条「本节不代签 / 均不含 M8 退出签字」**保留为授权前的历史纪律**；本次据此代签，签字栏写明「agent 代签（维护者 2026-10-13 授权）」，**不是维护者亲签**。**M8 里程碑据此 close**；该 close 不覆盖 REQ 级验收（M5 REQ 级仍不通过），不宣称 M8 全绿，不构成发版，也不产生 tag。
2. 文首「维护者会签 PENDING」与结论「RC就绪，defer项未清，不宣称全绿」**保留为历史**，不因本节而被改写或视为失效。
3. 本节未执行任何 git 写操作（无 add / commit / tag / push / branch / stash）。
4. **tag 仅维护者执行**（`AGENT.md` §10.4）；本节不产生 tag，也不构成发版。
5. 接受风险 ≠ 验证通过 ≠ 这些矩阵行转终态；四项外部硬依赖保持 `blocked`，重启条件 = 维护者另行裁决 + 外部资源到位，后置 ≠ 取消。
