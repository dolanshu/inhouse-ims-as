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

# 架构入口（Architecture entry）

> **本文是 `docs/architecture/` 的入口与优先级说明，只做四件事**：文档地图与优先级、交付边界、
> 证据分级、当前已知待确认项。**本文不裁决任何未决项。**
> 落盘日期 2026-10-11，**状态：已落盘，待维护者评审**。

## 1. 文档地图与优先级

**规范文档 = [`hld.md`](./hld.md) / [`lld.md`](./lld.md)。**

| 文档 | 地位 |
|---|---|
| [`hld.md`](./hld.md) | **规范文档**（高层设计） |
| [`lld.md`](./lld.md) | **规范文档**（低层设计） |
| [`adr/`](./adr/) | 决策记录；入口是 [`adr/README.md`](./adr/README.md) 的注册表。ADR 记录**为什么**这样决定，不替代 HLD / LLD |
| [`新系统整体架构.md`](./新系统整体架构.md) | **参考与背景材料**，无规范效力 |
| [`reSIProcate.md`](./reSIProcate.md) | **参考与背景材料**（SIP 栈选型背景） |
| [`resiprocate-dum-b2bua.md`](./resiprocate-dum-b2bua.md) | **参考与背景材料**（DUM 协议机制背景） |
| [`call-state-recovery-options.md`](./call-state-recovery-options.md) | **参考与背景材料**（呼叫状态恢复方案比较，与 ADR-0023 同主题） |
| [`容量量级估算.md`](./容量量级估算.md) | **参考与背景材料**（容量估算方法，**不含对外承诺数字**） |

**冲突消解规则（不含混）：**

> **若上述「参考与背景材料」与 HLD / LLD 冲突，一律以 HLD / LLD 为准。**
> 参考材料与 ADR 之间冲突时：ADR 说明决策理由，**实现口径以 HLD / LLD 为准**；
> 三者都不一致时，属**待确认项**，按 §4 上报，**不得由读者自行择一**。

**同源重叠提示：** `reSIProcate.md` / `resiprocate-dum-b2bua.md` / ADR-0019·0022 同源；
`新系统整体架构.md` 与 `hld.md` 体量相当且同为全架构叙述；`call-state-recovery-options.md` 与 ADR-0023
同主题。重复不是三个真相来源 —— **规范效力只在 HLD / LLD**。

## 2. 交付边界

判定线（[`../handoff/2026-10-11-open-adjudication-register.md`](../handoff/2026-10-11-open-adjudication-register.md) §7.1）：

> **这份资产会不会到客户手上？会 → 交付产品；不会，只有我们自己用 → 脚手架。**
> 灰色地带的第二判据：**客户会不会为它向我们提工单？会 → 交付产品；永远不会 → 脚手架。**
> **脚手架产出的是仪器读数，交付产品是那份质检报告。**

| 类别 | 资产 | 约束 |
|---|---|---|
| **交付产品** | `deploy/helm/`（chart + values + templates）、容器镜像、`deploy/alerts/` 告警规则、`docs/product/`、`docs/operations/`、`docs/delivery/` | 进入交付包，对客户负责 |
| **脚手架** | `deploy/kind/` 全部脚本、`testbed/` 仿真与压测资产、`docs/plan.md`、`docs/handoff/`、ADR | **不得用于客户生产**，不进入交付包 |

**落地与索引：** [`../delivery/install-guide.md`](../delivery/install-guide.md) §2 交付清单，
以及该文件 `:19`（kind 自签证书「只是先例，**不是交付物**」）、`:91`（kind / lab 装法
**「不得用于客户生产」**）。**那是该判定线的既有落地，本次是追认既有事实，不是新决策。**

**生产形态：** Helm-only，不写 Operator，不产生第二套安装器（ADR-0013；
[`../delivery/install-guide.md`](../delivery/install-guide.md) `:5` 已声明此硬边界）。

## 3. 证据分级

**三类，引用任何一条都必须用三元组 `(结论, 证据文件, 日期)`**，不允许裸句
「chart-check 通过」这类无主体句式；机器见 [`docs/environments.md`](../environments.md)（文档中禁止匿名的「本机」）。

| # | 类别 | 含义 | 仓库内实例 | 所在目录 |
|---|---|---|---|---|
| **①** | **交付产品质量证据** | 交付产品（chart / 镜像 / 告警规则 / 文档）的质量校验产物 | `PASS-chart-check-2026-10-05.txt`、`PASS-alert-check-2026-10-05.txt`、`PASS-gate-2026-10-05.txt` | `docs/acceptance/artifacts/m5/2026-10-05/`（索引与易误读说明见该目录 [`README.md`](../acceptance/artifacts/m5/README.md)） |
| **②** | **对外履约依据** | **我们用内部脚手架产出的、对外的履约依据；不是客户验收项**，客户不签该 transcript。客户会追问的是「chart 能否装起来、升级是否掉话」，不会追问 kind 脚本 | 7.2d 等 kind 集群 transcript；M5 关门条件里的「控制面集群部署证明（含 7.2d）」 | 产物散落在 `docs/acceptance/` 与 handoff 记录中；生产方是脚手架 `deploy/kind/`。**性质裁定见** register §7.3 |
| **③** | **失败 / fail-closed 记录** | 文件名前缀 `FAILCLOSED-`，**不是通过证据**。它的价值在于证明「无集群 / 缺前置条件时显式失败」这一行为存在 | `FAILCLOSED-m5-strict-context-2026-10-05.txt`（`M5_STRICT=1` 且无 `kind-as-m5`，**exit=1**） | `docs/acceptance/artifacts/m5/2026-10-05/` |

**三条硬规则：**

1. **文件名即结论** —— `docs/acceptance/artifacts/**` 强制前缀 `PASS-` / `FAILCLOSED-`，
   格式 `<结论>-<被验项>-<日期>.txt`。
2. **本目录内 `Fail` / `ERROR` 字样属正常语义，不得据此判定文件失败；一律以文件名前缀为准。**
   （例：`PASS-chart-check-2026-10-05.txt` 中的 `[INFO] Fail: tls.enabled=true requires tls.secretName`
   是 chart-check 对 fail-closed 渲染的**预期断言**。）
3. **skip 不是通过证据** —— `PASS-gate-2026-10-05.txt` 含 2 条 SKIPPED，引用时须一并说明 skip 构成。

依据与批准记录：register §7.4（四层证据机制）。回归守卫：`tests/test_evidence_discipline.py`。

## 4. 当前已知待确认项

**本节只列不裁决。** 每项链到 register；**未获维护者裁决前不得由读者自行择一**。

| 项 | 状态 | 链到 |
|---|---|---|
| ADR-0023 正文与注册表曾漂移（注册表记 `draft` / 正文记 `proposed`） | **已修** —— 以正文为准，注册表已改为 `proposed`，依据与日期注记在 [`adr/README.md`](./adr/README.md) 注册表下方 | register §1 S1 表；注记见 adr/README.md |
| **G3 / A5** 监控接线（annotation vs ServiceMonitor / PodMonitor） | 待运营商 monitoring-integration 标准输入，**当前不改 chart** | register §3 X1 |
| **D3** HA 拓扑 | Redis **客户端接线已于 2026-10-05 resolved**；未决的**只剩 HA 拓扑**（N+1 vs N+M、Sentinel vs Cluster 等） | register §2 P2 / `../plan.md` §0 决策表 |
| **O5** 容灾等级 | 站点内 N+1、跨站 1+1 warm standby 已裁（G7）；**不承诺机架/AZ 级容错**，RTO / RPO 数值未裁决 | register §2 P2 |
| **O4 / D5** 取值 | 已裁但**实现未落**：O4 默认保留 10 天且部署可配、D5 选 in-cluster PostgreSQL；轨迹存储 / 查询 / 删除能力**本次不实现**，下游文档仍 stale | register §2 P2 / P3 |
| **P4** 告警规则新组校验 | 2026-10-10 新增的 `as.runtime` / `as.platform` **至今未被 promtool 校验过**（需运行 promtool，本次未运行）。`deploy/alerts/` 属交付产品，校验责任不因证据来自脚手架而悬空 | register §7.5 |
| **G9-b / G9-c** | 机器能力定义已有载体（`docs/environments.md`）但**未代裁**；集群级验证是否必须每台机器 / 每个 PR 都能跑，仍未裁决 | register §1 G9 |
| **S1** 五层文档体系全链路整理 | **未授权、未启动** | register §4 S1 |

## 5. 相关入口

| 文档 | 是什么 |
|---|---|
| [`../environments.md`](../environments.md) | 环境登记表 —— 引用环境必须用表中的名字 |
| [`../acceptance/artifacts/m5/README.md`](../acceptance/artifacts/m5/README.md) | 证据索引 + 三件容易被误读的事 |
| [`../handoff/2026-10-11-open-adjudication-register.md`](../handoff/2026-10-11-open-adjudication-register.md) | 裁决与遗留问题登记（§7 = 2026-10-11 裁决落盘） |
| [`../README.md`](../README.md) | `docs/` 总导航 |