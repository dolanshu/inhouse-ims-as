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

# M8 范围修订与内部版本收尾计划（2026-10-12）

> **状态：本文是计划，不是执行记录。**
>
> - **不签收**：本文不签收任何 REQ、不签收任何里程碑、不改签收矩阵任何一行的 `status`、不改 `report.md` 任何计数。文中所有「完成」「终态」字样均指**本计划范围内的工程目标**，非验收结论。
> - **待评审**：本文落盘后**待维护者评审**；评审通过**不等于**执行授权 —— 各批次的启动仍需维护者逐项批准（见 §6）。
> - **触发前提（维护者 2026-10-12 指示）**：必须依赖运营商 / 客户环境的项**移到下一个 release**；**本版前提 = function 必须完成，证据可以使用模拟器**。
> - **上游指针**：[`2026-10-06-m8-release-candidate-plan.md`](2026-10-06-m8-release-candidate-plan.md)（RC 计划，阶段 A–E 总计划）、[`2026-10-07-m8-next-step-plan.md`](2026-10-07-m8-next-step-plan.md)（N2/N3/N4）、[`../acceptance/m8-environment-evidence.md`](../acceptance/m8-environment-evidence.md)（restriction 依据）、[`../acceptance/m8-test-plan-matrix.md`](../acceptance/m8-test-plan-matrix.md)（签收矩阵）、[`2026-10-10-unfinished-assessment-and-next-plan.md`](2026-10-10-unfinished-assessment-and-next-plan.md)（未完成项盘点）。
> - **编号口径声明**：本文沿用仓库既有编号，**不发明新编号**。仓库中存在形似易混的两套编号，本文一律按下列既有用法书写，读法以此表为准：

| 本文写法 | 含义 | 出处 |
|---|---|---|
| `A-1`~`A-7`（带连字符） | RC 计划**阶段 A** 任务（A-1 F9 native 门禁 … A-7 native 一致性 runbook） | RC 计划 §4 阶段 A |
| `A2`~`A6`（不带连字符） | 2026-10-10 盘点 **Lane A** 条目（A2 真栈构建常态化 … A6 版本口径） | [`2026-10-10-unfinished-assessment-and-next-plan.md`](2026-10-10-unfinished-assessment-and-next-plan.md) §4 |
| `B-1`~`B-7`（带连字符） | RC 计划**阶段 B** 任务 | RC 计划 §4 阶段 B |
| `B1`~`B6`（不带连字符） | 2026-10-10 盘点的**维护者裁决项**（B1 O1 容量目标 … B6 包装文档评审） | 同上 §0-A.2 / §4 Lane B |
| `D-1`~`D-3`（带连字符） | RC 计划**阶段 D** 环境证据项（D-1 运营商 PKI / D-2 客户 K8s / D-3 D6 testbed） | RC 计划 §4 阶段 D；[`../acceptance/m8-environment-evidence.md`](../acceptance/m8-environment-evidence.md) |
| `D1`~`D12`（不带连字符） | `plan.md` §5.2 未决项（D1 Python 3.10 EOL … D12 集群内 PG/Redis HA） | [`../plan.md`](../plan.md) §5.2 |
| `E-1`~`E-6`（带连字符） | RC 计划**阶段 E**（报告、版本、签字）任务 | RC 计划 §4 阶段 E |
| `S5`~`S11`（`S7a`/`S8`） | A3 Phase D 真栈对拍场景 | [`2026-10-09-sip-native-testing-plan.md`](2026-10-09-sip-native-testing-plan.md) §4-D |
| `S-1`~`S-4`（带连字符） | 矩阵安全行 `REQ-S-1`~`REQ-S-4` 的简写 | [`../acceptance/m8-test-plan-matrix.md`](../acceptance/m8-test-plan-matrix.md) §3 |
| `F-4`/`NF-2`/`5.4-F-13` 等 | 矩阵行 ID 简写（省略 `REQ-` 前缀，补测行保留 `5.4-` 前缀） | 同上 |

六个工作批次一律用**描述性名称**（「发布与打包」「SIP 对拍」「kind/sim 证据」「签收与评审」「性能与容量」「文档与报告」），**不另造批次编号**。

---

## 0. 事实基线（2026-10-12，照录现状，本文不改写任何正本）

> 本节是后续各节的事实底座。所有条目均引自仓内既有文档；本文**只照录，不改写、不签收**。

### 0.1 签收矩阵现状

以 [`../acceptance/m8-test-plan-matrix.md`](../acceptance/m8-test-plan-matrix.md) 2026-10-12 N2 / N3 代签节登记的计数为准：**pass 16 / open 17 / blocked 10 / n-a 6 / fail 0**。

| 桶 | 行（矩阵行 ID） |
|---|---|
| open 17 | F-4、F-5、F-8、F-9、F-10、F-11、F-16、NF-2、NF-5、NF-9、NF-10、NF-13、NF-14、NF-15、S-1、S-4、D12/O5-HA |
| blocked 10 | F-13、5.4-F-13、F-15、5.4-F-15真AS、NF-1、NF-4、NF-7、S-2、S-3、ADR-0008-演练 |

N3 已代签的 7 行（F-1/F-2/F-3/F-6/F-7/F-12/F-14）签字口径一律是「**工程证据接受**」，不是 REQ 级验收；M5 REQ 级仍是不通过、M8 仍是「RC 就绪、待退出签字」。

### 0.2 外部硬依赖（restriction）

依据 [`../acceptance/m8-environment-evidence.md`](../acceptance/m8-environment-evidence.md)：自 **2026-10-07** 起，Close 之前不做真实运营商 S-SBC / 客户 K8s 测试，下列项保持 `blocked` 或 `open`，**不能签 pass**：

| 外部硬依赖 | 牵动的矩阵行 | 缺什么 |
|---|---|---|
| D-1（运营商 PKI + 外网 S-SBC） | S-2、S-3 | 运营商 PKI lab 与外网 S-SBC 对端 |
| D-2（客户 K8s） | NF-1（live kill/restart/BYE） | 客户 K8s 集群 |
| ADR-0008 跨站点切换演练 | ADR-0008-演练 | 两个客户 / 生产站点（实验室单集群不算） |
| D12 / O5 生产 Redis 与 PostgreSQL HA | D12/O5-HA | 客户生产拓扑上的 Sentinel / 流复制 / PITR（kind bundled state 不是本条） |

### 0.3 不要求客户集群的行

同上文件「同样的 restriction」一节：**REQ-NF-2、REQ-NF-4、REQ-NF-9** 要的是**自有 kind / 实验室集群**，不要求客户集群；**REQ-NF-5** 的仿真 S-SBC 已在 M7.1 做成**透明桥**（无 Kamailio，不是运营商 S-SBC）。这四行是「证据可以用模拟器」这一前提的主要对象。

### 0.4 发布镜像现状

`deploy/docker/Dockerfile` 仍是 **M5 进程壳、不带 SIP 监听**（`ENTRYPOINT ["python", "-m", "as_platform"]`；`EXPOSE 5060/udp 5061/tcp` 只是端口声明）。多处文档明写该缺口「**重开 M8 之前补上**」（[`2026-10-07-m8-next-step-plan.md`](2026-10-07-m8-next-step-plan.md) 文首、[`../plan.md`](../plan.md) §0、[`pre-m8-demo-review-plan.md`](pre-m8-demo-review-plan.md) 发布镜像行）。

### 0.5 A3 Phase D 排期（已定稿，2026-10-12）

[`2026-10-09-sip-native-testing-plan.md`](2026-10-09-sip-native-testing-plan.md) §4-D：**P1 S5 两腿归一化对拍 → P2 S7a SDP corpus → P3 S6 规则优先级 → P4 S10 非 2xx → P5 S9 in-dialog → P6 S11 CANCEL 竞态**（S11 因确定性证明成本最高、flaky 风险最大排最后，与上游理由一致）；**S8 登记为阻塞项** —— 基线缺 Route / Record-Route 头，**M2 probe 补采前不排**，REQ-F-5 按 N4 停止线不签 pass。**排期已定稿，但用例实现一批未落，分批启动需维护者授权。**

### 0.6 性能与容量

- **NF-15 的 HPA 阈值仍阻塞**：缺带 **per-pod CPU / 内存利用率**的测量批次；2026-10-12 饱和点探测（20 → 1280 CPS 全成功、未测到饱和点）**未记录资源数据**，不构成该批次（依据 [`2026-10-12-o1-and-native-reproducibility.md`](2026-10-12-o1-and-native-reproducibility.md) §4）。
- **O1**：内部工程目标（**loopback 模型 CPS 1280 无失败**）已定，**仅限内部**；**对外承诺值仍不填**（G5 / B1；`ne-datasheet.md` §3 填值准入条件三条均未满足）。HPA 阈值、容量类告警、Datasheet 容量取值、4.1 正式报告四项下游维持阻塞。

### 0.7 F-13 / NF-7（呼叫轨迹）

无 trace store / API；**O4**（默认 10 天、部署可配）与 **D5**（in-cluster PostgreSQL）**已裁但实现未落**（2026-10-10 G6 裁决 + [`2026-10-12-b2-b3-deferred-items.md`](2026-10-12-b2-b3-deferred-items.md) 已整体后置）。F-16 的轨迹联动部分依赖 F-13。**2026-10-12 裁定：重大漏项，delay 到 v1.1 作为 feature（requirement → ADR → design → review），本版不实现；F-16 只签非轨迹部分。**

### 0.8 文档计数与已后置项

- `../acceptance/report.md` §0.5 计数**仍为 open 24 / blocked 12**（pass 9 / n-a 4），**未同步** N2/N3 后的矩阵（pass 16 / open 17 / blocked 10 / n-a 6）。
- **X1** 抓取接线已后置（待运营商 monitoring-integration 标准输入，G3 维持待决，不改 chart）；**B2 / B3** 已整体后置到下一个 release；**Lane D 四项**已分别裁为 v1.1 / 按需（4.2 长稳报告 v1.1、4.3 API 版本兼容 v1.1、4.4 白皮书按需、4.5 能力开放机制按需）。

> **去向指针（2026-10-13 追加；上方第 2 条原文一律保留不改）**：本条所列已后置项的去向统一收口于
> [`../next-release-v1.1-plan.md`](../next-release-v1.1-plan.md) —— **X1 抓取接线**见 **§2** 第 7 行（在七项外部硬依赖表内）；
> **B2** 见 **§4-1**、**B3** 见 **§4-2**，两者的四项启动条件原样保留为 **§4.3**（未确认不得启动），B3 的 RPO / RTO 取值见 **§7-4**；
> **Lane D 4.2 / 4.3** 见 **§3-7**（4.4 / 4.5 已裁为「按需」，不在 v1.1 立项列内）。
> 后续状态盘点、汇报、handoff、新 session 开场涉及本条所列遗留项一律**只引该指针**，不逐项展开、不再列入「待维护者动作」。

### 0.9 四层证据机制与版本称呼

- **四层证据机制**（2026-10-11 裁决）：① 文件名即结论（`docs/acceptance/artifacts/**` 强制 `PASS-` / `FAILCLOSED-` 前缀）；② 环境必须有名字（[`../environments.md`](../environments.md) 登记，禁匿名「本机」）；③ 状态三元组 `(结论, 证据文件, 日期)`；④ 守卫测试 `tests/test_evidence_discipline.py`。已登记环境 `dev-win03ib7niepf0`（host `WIN-03IB7NIEPF0`）。
- **版本称呼**：[`../plan.md`](../plan.md) §0 明写**没有 v1 / v1.1 定义**；产品版本号**只看根 `VERSION`**（当前 `0.2.0`）。其他文档里的「v1 / v1.1」不是发行版本定义。

---

## 1. 范围重划

### 1.1 表 A「移出到下一个 release」

| 行 / 项 | 卡点 | 重启所需 |
|---|---|---|
| S-2 / S-3 | 外部硬依赖 D-1：无运营商 PKI lab、无外网 S-SBC 对端（2026-10-07 起 Close 前 restriction） | 运营商 PKI lab + 外网 S-SBC 联调窗口 |
| NF-1（live kill / restart / BYE） | 外部硬依赖 D-2：无客户 K8s 集群 | 客户 K8s 集群 |
| ADR-0008-演练 | 外部硬依赖：跨站点切换需两个客户 / 生产站点，实验室单集群不算 | 双站点（客户 / 生产）环境 |
| D12/O5-HA（生产 Redis / PG HA） | 外部硬依赖：需客户生产拓扑上的 Sentinel / 流复制 / PITR；kind bundled state 不是本条 | 客户生产拓扑 |
| 包装 2.4 摘流 / iFC 配合 | 需 S-CSCF / HSS 侧配合窗口 + 真实集群 | 真实集群 + 网内配合窗口 |
| 包装 2.5 备份恢复（客户真实集群版） | 客户真实集群演练未做；kind bundled state 不是生产备份恢复 | 客户真实集群 |
| X1 抓取接线 | 待运营商 monitoring-integration 标准输入（G3 / A5 维持待决，当前不改 chart） | 运营商 monitoring-integration 标准 |

**「后置 ≠ 取消」。** 重启条件沿用 [`2026-10-10-unfinished-assessment-and-next-plan.md`](2026-10-10-unfinished-assessment-and-next-plan.md) §0 口径：**维护者另行裁决 + 外部资源到位**，**不得因本机工作顺带推进**。矩阵中这些行**保持原状态词**（`blocked` / `open`），本文不改写、不提前转终态。

> **去向指针（2026-10-13 追加；上方表 A 与本段口径原文一律保留不改）**：表 A 的七行连同本段重启条件口径，
> 统一收口于 [`../next-release-v1.1-plan.md`](../next-release-v1.1-plan.md) **§2**（外部硬依赖类）—— 第 1–4 行对应
> D-1 / S-2 / S-3、D-2 / NF-1 live、ADR-0008 演练、D12 / O5，第 5–6 行对应包装 2.4 / 2.5，第 7 行对应 X1 抓取接线；
> 该节措辞沿用本表与本段原文。另：**O1 对外承诺值**见同文档 **§4-6**，v1.1 立项 feature 见 **§3**。
> 后续状态盘点、汇报、handoff 涉及表 A 遗留项一律**只引该指针**，**本清单不再逐项复述**。

### 1.2 表 B「本版必须完成」

| 类别 | 内容 | 对应矩阵行 / 依据 |
|---|---|---|
| v1 范围内 **function 工程完成** | SIP 对拍批次（A3 Phase D：S5 / S7a / S6 / S9 / S10 / S11 + S8 前置补采） | F-4、F-5、F-8、F-9、F-10、F-11、F-16（见 §2 批次「SIP 对拍」） |
| 模拟器 / kind 可取的证据行 | kind / M7.1 sim 可取的集群级与话务级证据 | NF-2、NF-4、NF-5、NF-9、NF-10、NF-13、NF-14、NF-15；F-15 与 5.4-F-15真AS（kind + sim 全栈） |
| 发布动作（RC 计划阶段 E） | report.md、VERSION / CHANGELOG、plan.md 回写、内部版退出评审文档、里程碑签字表、打包复检 | E-1~E-6（见 §2 批次「文档与报告」） |

**F-13 / NF-7 已裁定（2026-10-12，维护者）：判重大漏项，delay 到 v1.1 作为 feature，本版不实现**（详见 §6 第 1 项裁决结果）。

### 1.3 本版的定位（一句话）

**本版 = 内部版本：function 完整 + 模拟器证据 + 可重复构建的发布工件。本版不是 M8 退出签字** —— M8 退出签字仍排在外部硬依赖（表 A）之后，`plan.md` §4 M8 行的最终表述由维护者确认。

---

## 2. 本版工作分解（六个批次，标注依赖顺序）

**依赖顺序**：

```text
批次 1「发布与打包」（最先，无依赖）
   ↓
批次 2「SIP 对拍」（S8 前置补采 → P1 S5 → P2 S7a → P3 S6 → P4 S10 → P5 S9 → P6 S11）
   ↓
批次 3「kind/sim 证据」（与批次 2 可部分并行；F-15 真 AS 依赖批次 1 的镜像）
   ↓
批次 4「签收与评审」（依赖批次 2/3/5 产出证据）
   ↓
批次 5「性能与容量（kind）」（可与批次 3 并行；向批次 4 供 NF-15 证据）
   ↓
批次 6「文档与报告」（最后，依赖前五个批次）
```

**授权（2026-10-12，维护者）**：§2 **六个批次全部一次性全量授权**（批次 2 / 3 见 §6 第 5 项；批次 1 / 4 / 6 为本次一并授权；批次 5 by §6 第 4 项）。agent 按上述依赖顺序自行推进；每批 / 每项落地另留 review record；矩阵行保持原状态词；不签任何 REQ；不执行任何 git 写操作。

### 2.1 批次「发布与打包」（最先，无依赖）

| 项 | 内容 | 依据 |
|---|---|---|
| Dockerfile 带 SIP 监听 | 发布镜像当前是 M5 进程壳、不带 SIP 监听（§0.4），本批次补上 | [`2026-10-07-m8-next-step-plan.md`](2026-10-07-m8-next-step-plan.md) 文首「重开之前，发布镜像再带上 SIP 监听」 |
| 镜像可重复构建 + digest 记录 | 复现构建并记录 image digest | RC 计划 E-6 |
| helm values-onprem / compose 一致性 | 交付三态（chart onprem values / compose / 镜像）版本与配置一致 | RC 计划 E-6、B-5 |
| 脱敏复检 | 工件内无密钥、无 pcap、无含口令日志 | [`../acceptance/m8-environment-evidence.md`](../acceptance/m8-environment-evidence.md) §0 脱敏红线；RC 计划 E-6 |
| README / runbook 与 `AS_SIP_*` / `AS_TLS_*` 实现一致 | 交付文档与代码实际环境变量逐条对齐 | RC 计划 E-6 |

**边界**：镜像 push / tag 仅维护者执行（RC 计划 E-6）；本批次不 bump 根 `VERSION`（取值待 §6 第 2 项裁决）。

### 2.2 批次「SIP 对拍」（A3 Phase D 落地）

**前置**：**S8** —— M2 probe 补采 Route / Record-Route 基线（基线缺这两个头，2 条既有 skip 的根因）；**补采前不排 S8 实现**，REQ-F-5 在补采前按 N4 停止线不签 pass。

**执行顺序**（排期已定稿于 [`2026-10-09-sip-native-testing-plan.md`](2026-10-09-sip-native-testing-plan.md) §4-D，本批次按此落地）：

| 顺序 | 场景 | 推进的矩阵行 | 前置 / 备注 |
|---|---|---|---|
| 0 | S8 基线补采（M2 probe Route / Record-Route） | **F-5**（补采是签收 F-5 的前置） | 不补采则不排 S8；补采完成后建议插在 P3 之后 |
| 1 | P1 S5 两腿归一化序列对拍 | F-2 **已于 2026-10-12 N3 代签 pass**，此处为 coverage 扩展（不改行状态） | 无（复用 `testbed/e2e/` 框架） |
| 2 | P2 S7a SDP 透传 corpus 扩充（兼 F-4 更广 corpus） | **F-4** | 补带 media 描述 / 多 m-line 的 SDP 变体 |
| 3 | P3 S6 多规则优先级 + 无匹配组合 | F-3 **已于 2026-10-12 N3 代签 pass**，此处为 coverage 扩展（不改行状态） | 与 S2（404 已绿）共用仿真链 |
| 4 | P4 S10 非 2xx（486 / 480 / 408）透传 | **F-10** | 依赖先扩 testbed 对端 UAS（当前只返 200） |
| 5 | P5 S9 in-dialog 路由 | **F-9** | 依赖 M7.3 context restoration 工程切片（已在位） |
| 6 | P6 S11 CANCEL 与最终响应竞态 | **F-11** | 竞态两分支确定性证明成本最高、flaky 风险最大；允许以 gap 登记收尾 |

其余关联：**F-8**（CANCEL 三分支）随 S4 cancel harness 与 S11 的对拍推进；**F-16**（翻译决策链）的**轨迹联动部分依赖 F-13** —— F-13 已裁定 delay v1.1，故 F-16 **只签非轨迹部分并写明理由**。

**授权前提（2026-10-12 更新）**：A3 Phase D 的**实现分批启动已由维护者一次性全量授权**（批次 2 含 S8 基线补采与 P1–P6 全部，P4 含扩 testbed UAS 非 2xx 分支）；agent 按 §4-D 顺序自行分批推进，**每批落地另留 review record**；**本计划不代签、不预设任何一行转 pass**。

### 2.3 批次「kind/sim 证据」

自有 kind / 实验室集群即可、不要求客户集群的行（§0.3）+ 模拟器可取的证据：

| 行 | 证据内容 | 环境 |
|---|---|---|
| NF-2 | kill translation 不影响 anti-fraud（双 Deployment 隔离 live 验证） | kind |
| NF-4 | M7.1 sim 话务 + kind 滚动零丢失（带真实 SIP 话务的滚动验证，补当前 blocked 行的缺口） | sim + kind |
| NF-9 | 命名空间故障隔离（Redis 挂 / AS 崩不影响另一 namespace） | kind |
| NF-5 | 换仿真器一致性（以 M7.1 透明桥为对照） | sim |
| F-15 / 5.4-F-15真AS | 真 AS 全栈分发 / 健康 / 自动 + 手动回滚 | kind + sim |
| NF-10 | live 灰度分发 / 回滚（随 F-15 真 AS 一并取证） | 同 F-15 真 AS |
| 2.5 备份恢复（工程演练） | kind bundled PG 备份 / 恢复 / 重建演练 + runbook 走查 + 实测耗时记录（RTO 量级，非承诺） | kind |

**边界**：以上均为**工程 / 集成层证据**，不升级为运营商或客户验收（见 §3）；NF-13 / NF-14 的 live 采集与真实触发涉及 X1（抓取接线，已后置），其终态在「签收与评审」批次按理由处理。（NF-15 不在上表内并非遗漏：归 §2.5「性能与容量」批次；NF-13 / NF-14 去向见本段前句。）

**授权（2026-10-12）**：本批次（含 2.5 kind 演练）已由维护者一次性全量授权；每批落地另留 review record。

### 2.4 批次「签收与评审」

| 行 / 项 | 内容 |
|---|---|
| S-1（白名单） | 评审现有工程证据 + 缺项补测；白名单变更走审批（与 F-14 联动） |
| S-4（RBAC + 审计不可篡改） | 评审 + 缺项补测；**durable audit 已有工程切片**（M4b-6b durable audit API / store：`PostgresAuditStore` + owner trigger 阻止 mutation / truncate），本批次补其正式全绿所缺部分（`plan.md` §5.4：REQ-S-4 正式全绿归 M8 或维护者单独签收） |
| 矩阵 17 open 行逐行终态化 | 每行给出 **pass / n-a / defer** 之一，**必带理由**；pass 须有本版新证据（三元组留档）；依赖 X1 或外部环境的行（如 NF-13 / NF-14 的 live 采集与真实触发）按理由转 defer 或提请维护者评审 |

**边界**：签收动作仍须维护者授权 / 评审；本文只列计划，不代签；「工程证据接受」≠ REQ 级验收通过 ≠ 里程碑签收（N3 口径延续）。

### 2.5 批次「性能与容量（kind）」

| 项 | 内容 | 边界 |
|---|---|---|
| NF-15 多副本测量批次 | kind 上多副本测量，**记录 per-pod CPU / 内存利用率** | 这是 HPA 阈值填写的前提；2026-10-12 饱和点探测未记录资源数据，不能复用为该批次 |
| HPA 阈值填写 | kind 实测数据产出后填 `values-onprem.example.yaml`；默认 `values.yaml` 保持 null | 已裁定（§6 第 4 项，2026-10-12）；示例内注明「kind 实测、非对外承诺、上线前须目标环境复测」；`hpa.yaml` 守卫不变 |
| performance 层门禁（RC 计划 A-6） | 终态二选一：实现为阻塞层，或 M8 总审书面接受风险 | 不自作实现、不自行接受风险 |
| O1 | 内部工程目标（loopback CPS 1280 无失败）已定，仅限内部 | **对外承诺值仍不填**（G5 / B1；Datasheet 填值准入条件三条未满足） |
| 容量类告警 | 仍不新增 | G5 裁决句继续有效；`ne-datasheet.md` 容量取值、4.1 正式报告维持阻塞 |

**边界**：本批次不发布任何对外容量数字（AGENT.md §2）；内部工程目标值不得写入任何对外材料。

### 2.6 批次「文档与报告」（RC 计划阶段 E）

| ID | 任务 | 内容 |
|---|---|---|
| E-1 | `report.md` 升为 M8 RC 报告 | 并把 §0.5 计数同步为矩阵现行值 **pass 16 / open 17 / blocked 10 / n-a 6 / fail 0**（现为 open 24 / blocked 12，见 §0.8） |
| E-2 | VERSION / CHANGELOG | **已裁定：不 bump**（§6 第 2 项，2026-10-12）—— VERSION 维持 `0.2.0`，CHANGELOG 在 0.2.0 节内追加 internal build 条目；`plan.md` §0「版本称呼」行继续有效 |
| E-3 | `plan.md` §0 / §4 M8 行回写 | 按本版实际收尾状态回写；M8 行的最终表述由维护者确认 |
| E-4 | 内部版退出评审文档（`docs/reviews/`） | **明确不是 M8 退出签字** |
| E-5 | 里程碑签字表 | M1 / M2 / M6 / M7 的「工程完成」已由维护者 2026-10-12 授权代签（N2 第 9 项）；**M8 不签** |
| E-6 | 打包复检 | `test_version_consistency`；镜像与 Helm 可重复构建；复检无密钥 / 无真实抓包；README 与 runbook 与 `AS_SIP_*` / `AS_TLS_*` 实现一致 |

---

## 3. 证据环境口径（模拟器证据分级）

**可用环境**（均须按四层机制留档）：

| 环境 | 用途 | 登记 / 依据 |
|---|---|---|
| 自有 kind（`as-m5` / `as-m71`） | 集群级证据（NF-2 / NF-4 / NF-9、F-15 真 AS、NF-10、NF-15 多副本） | [`../environments.md`](../environments.md)（kind 0.24.0 / kubectl 1.31.4 已登记） |
| M7.1 仿真 S-SBC（测试 CA，UDP / TCP / TLS，call load） | 话务对拍（NF-4）、换仿真器一致性（NF-5） | [`../acceptance/m71-sim-platform-evidence.md`](../acceptance/m71-sim-platform-evidence.md) |
| `deploy/compose` | PostgreSQL / Redis 依赖（integration 层） | [`2026-10-12-o1-and-native-reproducibility.md`](2026-10-12-o1-and-native-reproducibility.md) §2 |
| `dev-win03ib7niepf0`（host `WIN-03IB7NIEPF0`） | 门禁 / 构建 / 饱和点探测 | [`../environments.md`](../environments.md) |

**明确「不算」**（模拟器证据的降级口径）：

| 有的 | 不等于 | 后果 |
|---|---|---|
| 测试 CA 上的 TLS 呼叫 | 运营商 PKI 签发链 | S-2 / S-3 仍归表 A |
| kind bundled state | 生产 Redis / PG HA | D12/O5-HA 仍归表 A |
| M7.1 sim 透明桥 | 运营商 S-SBC | 不解除 D-1 restriction |
| accept-all harness | 业务判决路径 | O1 对外承诺值仍不填（上述三样 + 真实集群多副本测量均缺） |

**落盘纪律**：所有证据按四层机制（§0.9）落盘 —— `PASS-` / `FAILCLOSED-` 文件名前缀、`environments.md` 登记环境名、状态三元组 `(结论, 证据文件, 日期)`、守卫测试 `tests/test_evidence_discipline.py`。**不以工具就位充抵证据，不以 skip / 未跑当绿。**

---

## 4. 本版完成定义（内部发布关门条件）

全部满足方可称「内部版本收尾完成」：

1. **批次完成度**：§2 六个批次的出口判据全部满足，或经维护者书面调整后等价满足。
2. **矩阵终态**：17 个 open 行中，外部硬依赖 restriction 行 D12/O5-HA 按 §1.1 表 A 保持 open 并指向表 A（不要求转终态），其余 16 行全部转终态（pass / n-a / defer，必带理由），不得留下未解释 open；10 个 blocked 行中，本版可取证的行（NF-4、F-15、5.4-F-15真AS）有终态；F-13 / 5.4-F-13 / NF-7 已裁定 delay v1.1 作为 feature，转终态 n-a（详见 §6 第 1 项），restriction 行（S-2 / S-3 / NF-1 / ADR-0008-演练 / D12/O5-HA）保持原状态词并指向表 A。
3. **RC 报告与版本一致**：`report.md` §0.5 计数与矩阵现行值一致；`VERSION` / `CHANGELOG` 与交付工件一致（版本号口径：不 bump，见 §6 第 2 项）。
4. **不宣称清单**：**不宣称 M8 全绿、不宣称 M8 退出签字**；除已代签「工程证据接受」的行外，不宣称任何 REQ 级验收通过。
5. **tag 仅维护者**：本计划不执行任何 git 写操作；commit 拆分、tag、push 均由维护者决定与执行（AGENT.md §10.4）。

---

## 5. 移交下一 release 清单（重开 M8 时的输入）

| 行 / 项 | 卡点 | 重启所需 |
|---|---|---|
| S-2 / S-3 | D-1：无运营商 PKI lab、无外网 S-SBC 对端 | 运营商 PKI lab + 外网 S-SBC 联调窗口 |
| NF-1（live kill / restart / BYE） | D-2：无客户 K8s 集群 | 客户 K8s 集群 |
| ADR-0008-演练 | 需两个客户 / 生产站点 | 双站点环境 |
| D12/O5-HA | 需客户生产拓扑上的 Sentinel / 流复制 / PITR | 客户生产拓扑 |
| 包装 2.4 摘流 / iFC 配合 | 需 S-CSCF / HSS 侧配合 + 真实集群 | 真实集群 + 网内配合窗口 |
| 包装 2.5 备份恢复（客户真实集群版） | 客户真实集群演练未做（kind 工程演练版已在本版做，见 §6 第 3 项） | 客户真实集群 |
| X1 抓取接线 | 待运营商 monitoring-integration 标准输入 | 运营商 monitoring-integration 标准 |
| O1 对外承诺值 | 缺业务判决路径实测 / 饱和点观测 / 目标环境多副本（`ne-datasheet.md` §3 填值准入条件三条均未满足） | 真实集群多副本 + S-SBC 路径测量 |
| F-13 / 5.4-F-13 / NF-7（呼叫轨迹，重大漏项） | 已裁定 delay v1.1 作为 feature；无 trace store / API；O4 与 D5 已裁但实现未落 | v1.1 启动时走新 feature 流程（requirement → ADR → design → review） |

**重启条件同 §1 表 A 口径**：维护者另行裁决 + 外部资源到位；后置 ≠ 取消；不得因本机工作顺带推进。B2 / B3（requirement + ADR 起草）与 Lane D 四项已分别后置，载体为 [`2026-10-12-b2-b3-deferred-items.md`](2026-10-12-b2-b3-deferred-items.md) 与 [`2026-10-10-unfinished-assessment-and-next-plan.md`](2026-10-10-unfinished-assessment-and-next-plan.md) Lane D，本清单不重复展开。

> **去向指针（2026-10-13 追加；上方移交清单与本段原文一律保留不改）**：本清单已并入
> [`../next-release-v1.1-plan.md`](../next-release-v1.1-plan.md) —— 七项外部硬依赖见 **§2**；
> F-13 / 5.4-F-13 / NF-7 呼叫轨迹与其余 v1.1 立项 feature 见 **§3**；**O1 对外承诺值**见 **§4-6**；
> B2 / B3 见 **§4-1 / §4-2**（含 §4.3 四项启动条件）。
> 后续任何状态盘点、汇报、handoff，以及重开 M8 时整理「下一 release 输入」，一律**只引该指针**，**本清单不再逐项复述**。

---

## 6. 待维护者裁决项（开工前）

| # | 裁决项 | 影响 |
|---|---|---|
| 1 | **F-13 / NF-7 trace store** | **已裁定（2026-10-12，维护者）：判重大漏项，delay 到 v1.1，作为 feature 走新流程；本版不实现。** F-16 轨迹联动部分只签非轨迹部分 |
| 2 | **内部版本号与 CHANGELOG 条目口径** | **已裁定（2026-10-12，维护者）：不 bump** —— VERSION 维持 `0.2.0`；CHANGELOG 在 0.2.0 节内追加 internal build 条目（注明 internal、非发行版）；镜像 tag 用 `as-platform:0.2.0-internal-<date>` 区分；chart 不再同步；`plan.md` §0「版本称呼」行继续有效 |
| 3 | **2.5 备份恢复** | **已裁定（2026-10-12，维护者）：kind 完整工程演练纳入本版** —— kind bundled PG 上做备份/恢复/重建演练 + runbook 走查 + 实测耗时记录，落 `PASS-` / `FAILCLOSED-` 证据；明写不等于客户真实集群版（客户版在下一 release，见 §5），不验证 PITR / 对象存储 / 跨站 |
| 4 | **NF-15 HPA 阈值** | **已裁定（2026-10-12，维护者）：填 `values-onprem.example.yaml`，默认 `values.yaml` 保持 null** —— kind 多副本 + per-pod 资源利用率批次产出数据后，把 `autoscaling` 阈值写进 onprem 示例并注明「kind 实测、非对外承诺、上线前须目标环境复测」；fail-closed null 与 `hpa.yaml` 守卫不动；ne-datasheet / 容量告警 / 4.1 正式报告仍阻塞（G5 四项下游） |
| 5 | **批次 2 / 3 的启动授权** | **已授权（2026-10-12，维护者）：一次性全量授权批次 2 与批次 3** —— 批次 2 含 S8 基线补采与 P1–P6 全部（P4 含扩 testbed UAS 非 2xx 分支）；批次 3 含 2.5 kind 演练；agent 按 §4-D 顺序自行分批推进，每批落地另留 review record；矩阵行保持原状态词，不签任何 REQ |
| 6 | **批次 1 / 4 / 6（及隐含批次 5）的启动授权** | **已授权（2026-10-12，维护者）：一并全量授权** —— 至此 §2 六个批次全部授权；按依赖顺序推进，每批 / 每项留 review record；矩阵行保持原状态词，不签任何 REQ，不执行 git 写操作 |

---

## 7. 边界（不得据本计划推出过度结论）

1. **本文不签收任何 REQ / 里程碑，不改矩阵任何行 `status`，不改 `report.md` 任何计数**；所有「完成 / 终态」字样均指本计划范围内的工程目标。
2. **「移出下一 release」≠ 取消、≠ 解决**；后置项在矩阵中**保持原状态词**（`blocked` / `open`）—— 六字纪律：后置 ≠ 取消。
3. **模拟器证据是工程 / 集成层证据，不升级为运营商或客户验收**；测试 CA ≠ 运营商 PKI、kind bundled state ≠ 生产 HA、sim 透明桥 ≠ 运营商 S-SBC、accept-all harness ≠ 业务判决路径。
4. **本版关门 ≠ M8 退出签字**；`plan.md` §4 M8 行的最终表述由维护者确认，M8 总审确认栏在外部硬依赖闭环前保持空白。
5. **本文未执行任何 git 写操作**（无 `add` / `commit` / `tag` / `push` / 建分支 / 改 remote）；commit 拆分由维护者决定。
6. 本文若被后续证据或维护者裁决推翻，**须追加行说明**（日期 + 被推翻条目 + 依据），不得静默替换。

---

**落盘日期：2026-10-12。状态：计划，待维护者评审。**

（上游：[`2026-10-06-m8-release-candidate-plan.md`](2026-10-06-m8-release-candidate-plan.md)、[`2026-10-07-m8-next-step-plan.md`](2026-10-07-m8-next-step-plan.md)、[`../acceptance/m8-environment-evidence.md`](../acceptance/m8-environment-evidence.md)、[`../acceptance/m8-test-plan-matrix.md`](../acceptance/m8-test-plan-matrix.md)、[`2026-10-10-unfinished-assessment-and-next-plan.md`](2026-10-10-unfinished-assessment-and-next-plan.md)。
本文件不签收任何 REQ、不签收任何里程碑、不改矩阵任何行状态、不构成任何对外承诺。）
