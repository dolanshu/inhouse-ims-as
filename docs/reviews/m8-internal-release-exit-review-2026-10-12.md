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

**本文是「内部版收尾评审」，不是 M8 退出签字。**

# M8 内部版收尾评审记录（2026-10-12）

- **评审对象（object）**：M8 内部版收尾；范围为批次 1「发布与打包」至批次 6「文档与报告」六批全部产出。
- **评审日期（date）**：2026-10-13（文档批次日期：2026-10-12）。
- **评审人（reviewer）**：AI agent（维护者授权执行批次 1–6）；**维护者确认栏留空待签**。
- **评审结论（conclusion）**：**内部版收尾完成（有条件）**。条件是 M8 退出签字仍后置，排在外部硬依赖闭环之后。**这不是 M8 退出签字，也不是「通过」结论。**
- **执行环境**：`dev-win03ib7niepf0`。

---

## 1. 本版完成项

### 1.1 批次 1：发布与打包

Dockerfile 带 SIP 监听，内部镜像 tag 为 `as-platform:0.2.0-internal-20261012`；已记录构建 digest、运行时 SIP 监听、脱敏检查及环境文档对齐边界。

- `(已验证, docs/acceptance/artifacts/m5/2026-10-12/PASS-docker-build-digest-2026-10-12.txt, 2026-10-12)`
- `(已验证, docs/acceptance/artifacts/m5/2026-10-12/PASS-desensitization-check-2026-10-12.txt, 2026-10-12)`

### 1.2 批次 2：SIP 对拍（A3 Phase D）

- `(已验证, docs/acceptance/artifacts/m5/2026-10-12/PASS-s5-call-id-stability-2026-10-12.txt, 2026-10-12)`
- `(已验证, docs/acceptance/artifacts/m5/2026-10-12/PASS-s6-multi-rule-priority-2026-10-12.txt, 2026-10-12)`
- `(已验证, docs/acceptance/artifacts/m5/2026-10-12/PASS-s7a-sdp-corpus-expansion-2026-10-12.txt, 2026-10-12)`
- `(已验证, docs/acceptance/artifacts/m5/2026-10-12/PASS-s8-baseline-recapture-2026-10-12.txt, 2026-10-12)`
- `(已验证, docs/acceptance/artifacts/m5/2026-10-12/PASS-s9-in-dialog-bye-routing-2026-10-12.txt, 2026-10-12)`
- `(已验证, docs/acceptance/artifacts/m5/2026-10-12/PASS-s10-non-2xx-passthrough-2026-10-12.txt, 2026-10-12)`
- `(已验证, docs/acceptance/artifacts/m5/2026-10-12/PASS-s11-cancel-race-branch1-2026-10-12.txt, 2026-10-12)`

### 1.3 批次 3：kind / sim 证据

- `(已验证, docs/acceptance/artifacts/m5/2026-10-12/PASS-nf2-deployment-isolation-2026-10-12.txt, 2026-10-12)`
- `(已验证-接受实测呼损, docs/acceptance/artifacts/m5/2026-10-12/PASS-nf4-rolling-upgrade-accepted-loss-2026-10-12.txt, 2026-10-12)`
- `(已验证, docs/acceptance/artifacts/m5/2026-10-12/PASS-nf5-simulator-transport-consistency-2026-10-12.txt, 2026-10-12)`
- `(已验证, docs/acceptance/artifacts/m5/2026-10-12/PASS-nf9-namespace-isolation-2026-10-12.txt, 2026-10-12)`
- `(已验证, docs/acceptance/artifacts/m5/2026-10-12/PASS-f15-distribution-lifecycle-rollback-2026-10-12.txt, 2026-10-12)`
- `(已验证, docs/acceptance/artifacts/m5/2026-10-12/PASS-backup-restore-drill-bundled-pg-2026-10-12.txt, 2026-10-12)`

### 1.4 批次 4：签收与评审

- `(已验证-仅拒绝场景, docs/acceptance/artifacts/m5/2026-10-12/PASS-s1-whitelist-rejection-2026-10-12.txt, 2026-10-12)`
- `(已验证, docs/acceptance/artifacts/m5/2026-10-12/PASS-s4-audit-append-only-2026-10-12.txt, 2026-10-12)`
- `(已验证, docs/acceptance/artifacts/m5/2026-10-12/PASS-s4-rbac-permission-matrix-2026-10-12.txt, 2026-10-12)`

矩阵终态登记指针：`(已验证, docs/acceptance/m8-test-plan-matrix.md「M8 批次4 终态化代签（2026-10-13）」节, 2026-10-13)`。现行计数为 pass 27 / defer 4 / blocked 9 / n-a 9 / open 0 / fail 0；签字口径均为「工程证据接受」，全部为 agent 代签（维护者授权），不是维护者亲签。

### 1.5 批次 5：性能与容量

- `(已验证-非饱和点, docs/acceptance/artifacts/m5/2026-10-12/PASS-nf15-multi-replica-measurement-2026-10-12.txt, 2026-10-12)`
- `(已验证-仅限内部, docs/acceptance/artifacts/m5/2026-10-12/PASS-o1-loopback-cps-1280-2026-10-12.txt, 2026-10-12)`
- `(已验证, docs/acceptance/artifacts/m5/2026-10-12/PASS-hpa-threshold-filled-2026-10-12.txt, 2026-10-12)`

`PASS-o1-loopback-cps-1280-2026-10-12.txt` 中的 CPS 1280 仅是内部工程目标，不得写入对外材料。

### 1.6 批次 6：文档与报告

- `(已验证, docs/acceptance/artifacts/m5/2026-10-12/PASS-e6-packaging-recheck-2026-10-12.txt, 2026-10-12)`

---

## 2. 已知 gap 与终态边界

下列 `FAILCLOSED-` / `FAIL-` 文件**一律不是通过证据**：

1. 滚动零丢失未达成；当前 release 只接受已实测呼损范围：`(失败已登记-不是通过证据, docs/acceptance/artifacts/m5/2026-10-12/FAILCLOSED-nf4-rolling-restart-inflight-loss-2026-10-12.txt, 2026-10-12)`。
2. performance 层门禁终态的原始 FAILCLOSED 登记仍不是通过证据；批次 4 的 B5-04 已裁决采用 `(b)`，由 M8 总审书面接受风险关闭，本版不实现 `make gate` 阻塞层：`(失败已登记-不是通过证据, docs/acceptance/artifacts/m5/2026-10-12/FAILCLOSED-performance-gate-terminal-state-2026-10-12.txt, 2026-10-12)`。
3. 白名单变更审批能力不存在：`(能力不存在-不是通过证据, docs/acceptance/artifacts/m5/2026-10-12/FAILCLOSED-s1-whitelist-change-approval-not-wired-2026-10-12.txt, 2026-10-12)`。
4. in-dialog re-INVITE / UPDATE 未实现：`(未实现-不是通过证据, docs/acceptance/artifacts/m5/2026-10-12/FAILCLOSED-s9-reinvite-update-not-implemented-2026-10-12.txt, 2026-10-12)`。
5. CANCEL 先于任何下游响应的分支未实现：`(未实现-不是通过证据, docs/acceptance/artifacts/m5/2026-10-12/FAILCLOSED-s11-cancel-before-any-downstream-response-2026-10-12.txt, 2026-10-12)`。
6. PostgreSQL 15 集成运行失败；标准环境为 PostgreSQL 12.22，本批次未改产品代码：`(失败-不是通过证据, docs/acceptance/artifacts/m5/2026-10-12/FAIL-integration-pg15-2026-10-12.txt, 2026-10-12)`。

另有 4 行 `defer`：F-5 / F-8 / F-9 / F-11，均为本 release 不验收、已定点 v1.1；另有 9 行 `blocked`，属于现行矩阵登记的 restriction / 受限项。`defer`、`blocked` 与 `n-a` 的定义以矩阵「M8 批次4 终态化代签（2026-10-13）」节第三节为准。

---

## 3. 问题清单与对应修改 / 处置

| # | 发现的问题 | 对应修改 / 处置 | 当前状态 |
|---|---|---|---|
| 1 | 重建镜像的 manifest digest 与批次 1 记录值不同 | 保留批次 1 历史 digest，并在 E-6 证据记录新 digest、buildx attestation / manifest-list 差异与「不宣称逐字节一致」边界 | 已记录，不据此宣称镜像内容变化 |
| 2 | `report.md` §0.5 仍是 2026-10-06 历史计数 | 仅追加 §0.10 同步现行计数；历史段落一字不改 | 已同步 |
| 3 | 旧 M8 退出评审签字表未反映内部版收尾状态 | 仅追加 §3.2；M8 保持未签，M1/M2/M6/M7 维持授权代签的工程完成口径 | 已登记 |
| 4 | `plan.md` M8 行尚未回写内部版收尾 | 只生成 `m8-plan-m8-row-draft-2026-10-12.md` 草案，等待维护者确认；未改 `plan.md` | 待维护者确认 |
| 5 | 外部硬依赖与 v1.1 缺口尚未闭环 | 外部依赖保持 `blocked`，F-5/F-8/F-9/F-11 保持 `defer`；不以内部证据替代客户 / 运营商环境 | 后置，不等于取消 |
| 6 | M5 REQ 级验收仍不通过 | 保持既有结论，不用内部版收尾覆盖 REQ 级结论 | 未改变 |

---

## 4. 限制说明

1. 模拟器 / kind 证据是工程与集成层证据，**不升级为运营商或客户验收**。
2. 测试 CA ≠ 运营商 PKI；不签收 REQ-S-2 / REQ-S-3。
3. kind bundled state ≠ 生产 Redis / PostgreSQL HA；D12 / O5 不验收。
4. M7.1 仿真透明桥 ≠ 运营商 S-SBC。
5. accept-all harness ≠ 业务判决路径，因此 **O1 对外承诺值仍不填**；内部工程目标 loopback CPS 1280 仅限内部，不得写入对外材料。
6. 内部版本 ≠ 发行版：VERSION 维持 `0.2.0`、未 tag、chart 不随 internal build 变更。
7. **本文不构成 M8 退出签字**。M8 退出签字排在外部硬依赖 D-1（运营商 PKI + 外网 S-SBC）、D-2（客户 K8s）、ADR-0008 跨站点演练、D12 / O5 生产 HA 闭环之后。
8. 本批次未执行任何 git 写操作；commit 拆分由维护者决定。

---

## 5. 修改后的确认签字

| 项 | 记录 |
|---|---|
| 评审结论 | **内部版收尾完成（有条件）**；不是「通过」结论 |
| 条件 | M8 退出签字继续后置，排在外部硬依赖闭环之后 |
| 评审人 | AI agent（维护者授权执行批次 1–6） |
| M8 退出签字栏 | **未签（维护者待签）** |
| 维护者确认 | **待签字** |
| 所需维护者动作 | (1) 确认 `docs/plan.md` M8 行最终表述；(2) 给出外部硬依赖排期或书面接受风险；(3) 决定 commit 拆分；(4) 决定并仅由维护者执行 tag |

---

## 6. 路径 C 更正（2026-10-13；以上各节原文保留不改）

> 本节只追加更正，§1–§5 一字未改。

维护者已于 **2026-10-13** 按**路径 C** 作出 **M8 退出签字** —— 即「签 M8 退出签字 + 同时**书面接受外部硬依赖风险**」。据此：

1. 本文文首「**本文是「内部版收尾评审」，不是 M8 退出签字**」与 §5 签字节（M8 退出签字栏 = 未签），**保留为内部版收尾阶段的历史结论**，不因本次签字而被改写或视为失效。
2. **现行状态以 [`m8-exit-review-2026-10-06.md`](m8-exit-review-2026-10-06.md) §3.3 与风险接受前提文件 [`m8-external-dependency-risk-acceptance-2026-10-13.md`](m8-external-dependency-risk-acceptance-2026-10-13.md) 为准**。
3. 本文仍作为**内部版收尾评审存档**保留，**其中的 FAILCLOSED / gap / 限制说明全部继续有效** —— **不因 M8 签字而失效**：
   - §2 六项 `FAILCLOSED-` / `FAIL-` 文件**一律不是通过证据**的判定继续有效；
   - §4 八条限制说明（测试 CA ≠ 运营商 PKI、kind bundled state ≠ 生产 HA、accept-all harness ≠ 业务判决路径、内部版本 ≠ 发行版等）继续有效；
   - §4 第 7 条「本文不构成 M8 退出签字」作为**本文自身的历史定位**保留，M8 退出签字现登记于 `m8-exit-review-2026-10-06.md` §3.3。
4. **接受风险 ≠ 验证通过 ≠ 这些行转终态**：四项外部硬依赖（D-1 / D-2 / ADR-0008 演练 / D12-O5）保持 `blocked` 并转下一 release，重启条件 = 维护者另行裁决 + 外部资源到位，后置 ≠ 取消。
5. **签字覆盖里程碑退出，不覆盖 REQ 级验收** —— M5 REQ 级仍是不通过；不宣称 M8 全绿。
6. 本节未执行任何 git 写操作；tag 仅维护者执行（`AGENT.md` §10.4）。执行环境 `dev-win03ib7niepf0`。
