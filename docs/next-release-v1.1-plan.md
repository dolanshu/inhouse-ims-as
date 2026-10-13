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

# 下一个 release（v1.1 批次）项目计划

> 落盘日期：2026-10-13。**性质：登记载体，不是执行计划，不是排期表。**
> 本文不签收任何 REQ / 里程碑，不改任何矩阵状态词，不改 `docs/acceptance/report.md` 任何计数，
> 未执行任何 git 写操作。

---

## 0. 定位与口径

本文把「本版（M8 内部版）遗留项」从散落的多份文档**合并到单一载体**，供下一个 release 批次排期时一次性取用。

- **本文是下一个 release 批次（记作 v1.1）的单一追踪载体**；当前项目（M8 内部版）已于 2026-10-13 close（[`plan.md`](plan.md) §0 决策记录 2026-10-13「M8 退出签字（路径 C）」行、[`reviews/m8-external-dependency-risk-acceptance-2026-10-13.md`](reviews/m8-external-dependency-risk-acceptance-2026-10-13.md)），其全部遗留项的去向在此收口。
- **「v1.1」是批次代号，不是发行版本号** —— 沿用 [`handoff/2026-10-10-unfinished-assessment-and-next-plan.md`](handoff/2026-10-10-unfinished-assessment-and-next-plan.md) Lane D 表的既有用法（该表明写「『v1.1』按本表既有用法指**下一批次**，**不是正式发行版本定义**」）。发行版本号只看根 `VERSION`（当前 `0.2.0`，未 bump、未 tag）。
- **[`plan.md`](plan.md) §0「版本称呼」行仍为权威口径**：「**没有 v1 / v1.1 定义**……要定义，须写在本文并经维护者确认」。本文**沿用既有用法**，**不**替 `plan.md` 下发行版本定义。
- **后续口径**（与 [`handoff/2026-10-10-unfinished-assessment-and-next-plan.md`](handoff/2026-10-10-unfinished-assessment-and-next-plan.md) §12.2、[`handoff/2026-10-11-open-adjudication-register.md`](handoff/2026-10-11-open-adjudication-register.md) §3 X1 追加段同口径）：任何状态盘点、汇报、handoff、新 session 开场，涉及本版遗留项一律**只写「见本文 §X」的指针**，不逐项展开、不单独提醒、不再列入「待维护者动作」。
- **后置 ≠ 取消**。外部硬依赖类与已裁不做类的重启条件统一为：**维护者另行裁决 + 外部资源到位**；不得因本机工作顺带推进（[`handoff/2026-10-12-m8-scope-revision-internal-release-plan.md`](handoff/2026-10-12-m8-scope-revision-internal-release-plan.md) §1.1 表 A 表后原文）。
- 本文不签收任何 REQ / 里程碑，不构成对外承诺，不产生任何容量或 SLA 数字。

---

## 1. 来源与合并说明

| 既有清单 | 路径 | 本文对应章节 |
|---|---|---|
| M8 外部硬依赖风险接受 §1（四项外部硬依赖） | [`reviews/m8-external-dependency-risk-acceptance-2026-10-13.md`](reviews/m8-external-dependency-risk-acceptance-2026-10-13.md) §1 | §2 |
| M8 外部硬依赖风险接受 §2（v1.1 立项五项） | 同上 §2 | §3（第 1–5 行） |
| M8 范围重划 §1.1 表 A「移出到下一个 release」 | [`handoff/2026-10-12-m8-scope-revision-internal-release-plan.md`](handoff/2026-10-12-m8-scope-revision-internal-release-plan.md) §1.1 | §2 |
| M8 范围重划 §5 移交下一 release 清单 | 同上 §5 | §2、§4-6 |
| 未完成项评估 §12「已裁不做登记区」 | [`handoff/2026-10-10-unfinished-assessment-and-next-plan.md`](handoff/2026-10-10-unfinished-assessment-and-next-plan.md) §12 | §6 |
| `plan.md` §5 未决项登记（§5.1 / §5.2 / §5.2-bis / §5.3 / §5.4） | [`plan.md`](plan.md) §5 | §4 |
| B2 / B3 延后项登记（含 §4 四项启动条件、§5 后置） | [`handoff/2026-10-12-b2-b3-deferred-items.md`](handoff/2026-10-12-b2-b3-deferred-items.md) §0–§5 | §4（第 1–3 行）、§7-4 |
| M8 批次完成交接的「待维护者事项」段 | [`handoff/2026-10-12-m8-batch3-complete-handoff.md`](handoff/2026-10-12-m8-batch3-complete-handoff.md) §6、[`…-batch4…`](handoff/2026-10-12-m8-batch4-complete-handoff.md) §5、[`…-batch5…`](handoff/2026-10-12-m8-batch5-complete-handoff.md) §6、[`…-batch6…`](handoff/2026-10-12-m8-batch6-complete-handoff.md) §5 | §5、§7 |
| M8 批次 1 交接（无「待维护者事项」段，未提交改动记载在 §2.3） | [`handoff/2026-10-12-m8-batch1-complete-handoff.md`](handoff/2026-10-12-m8-batch1-complete-handoff.md) §2.3 | §5-6 |

> 批次 2「SIP 对拍」**未留下完成交接文档**（`docs/handoff/` 下无 `m8-batch2` 文件）；本文不为其补写。

---

## 2. 外部硬依赖类（重启 = 维护者裁决 + 外部资源到位）

措辞沿用 [`reviews/m8-external-dependency-risk-acceptance-2026-10-13.md`](reviews/m8-external-dependency-risk-acceptance-2026-10-13.md) §1 与 [`handoff/2026-10-12-m8-scope-revision-internal-release-plan.md`](handoff/2026-10-12-m8-scope-revision-internal-release-plan.md) §1.1 表 A / §5 的原文。

| 既有编号 / 条目 | 卡点（缺什么） | 本版证据为何不能替代 | 重启所需 | 来源指针 |
|---|---|---|---|---|
| **D-1 / S-2 / S-3**（运营商 PKI + 外网 S-SBC） | 缺**运营商 PKI lab** 与**外网 S-SBC 对端** | 本版 TLS 使用**测试 CA**（自签证书链），**不等于运营商签发链**；M7.1 仿真透明桥不是运营商 S-SBC；测试 CA 不签 REQ-S-2 / REQ-S-3 | 运营商 PKI lab + 外网 S-SBC 联调窗口 | `reviews/m8-external-dependency-risk-acceptance-2026-10-13.md` §1 第 1 项；`handoff/2026-10-12-m8-scope-revision-internal-release-plan.md` §1.1 第 1 行 / §5 第 1 行 |
| **D-2 / NF-1 live**（kill / restart / in-dialog BYE，客户 K8s） | 缺**客户集群** | **kind 自有集群不是客户 K8s**：网络策略、存储类、节点行为与真实运维动作均不可等价；kind 证据只到工程与集成层 | 客户 K8s 集群 | 同上 §1 第 2 项；`handoff/…m8-scope-revision…` §1.1 第 2 行 / §5 第 2 行 |
| **ADR-0008** 跨站点切换演练 | 需**两个客户 / 生产站点**才能做站点级切换 | **实验室单集群不算**：单集群无站点边界、无跨站点时钟与网络分区条件，演练结论不可迁移 | 双站点（客户 / 生产）环境 | 同上 §1 第 3 项；`handoff/…m8-scope-revision…` §1.1 第 3 行 / §5 第 3 行 |
| **D12 / O5-HA**（生产 Redis / PostgreSQL HA） | 缺**生产级 HA 部署**（Sentinel / Cluster、流复制、PITR） | **kind bundled state 不是生产 HA**：不覆盖 Sentinel 故障转移、PostgreSQL 流复制与 PITR 恢复演练；备份恢复演练只在 bundled PG 上验证过 | 客户生产拓扑 | 同上 §1 第 4 项；`handoff/…m8-scope-revision…` §1.1 第 4 行 / §5 第 4 行 |
| **包装 2.4 摘流 / iFC 配合** | 需 S-CSCF / HSS 侧配合窗口 + 真实集群 | 真实集群演练未做；iFC 触发责任在 S-CSCF / HSS 侧 | 真实集群 + 网内配合窗口 | `handoff/2026-10-12-m8-scope-revision-internal-release-plan.md` §1.1 第 5 行 / §5 第 5 行 |
| **包装 2.5 备份恢复**（客户真实集群版） | 客户真实集群演练未做（**kind 工程演练版已在本版做**，见该文档 §6 第 3 项） | kind bundled state 不是生产备份恢复；不验证 PITR / 对象存储 / 跨站 | 客户真实集群 | 同上 §1.1 第 6 行 / §5 第 6 行 |
| **X1 抓取接线**（annotation vs ServiceMonitor / PodMonitor） | 待运营商 monitoring-integration 标准输入（G3 / A5 维持待决，当前不改 chart） | `promtool` 语法校验通过不等于抓取接线闭合（P4 是语法、X1 是接线，两者不同） | 运营商 monitoring-integration 标准 | 同上 §1.1 第 7 行 / §5 第 7 行；`handoff/2026-10-11-open-adjudication-register.md` §3 X1「裁决落盘（2026-10-12 追加）」 |

这七项在矩阵中**保持原状态词**（`blocked` / `open`），本文不改写、不提前转终态（[`handoff/2026-10-12-m8-scope-revision-internal-release-plan.md`](handoff/2026-10-12-m8-scope-revision-internal-release-plan.md) §1.1 表后原文）。

---

## 3. v1.1 立项类（走 requirement → ADR → design → review 新 feature 流程）

第 1–5 行沿用 [`reviews/m8-external-dependency-risk-acceptance-2026-10-13.md`](reviews/m8-external-dependency-risk-acceptance-2026-10-13.md) §2 表原文。

| # | 既有编号 | 内容 | 为何在本版不实现 | 启动流程 | 来源指针 |
|---|---|---|---|---|---|
| 1 | **F-5** | 产品 AS 转发 trunk 侧 **Record-Route** | 本版不立项、不实现（矩阵该行为 `defer`） | requirement → ADR → design → review | `reviews/m8-external-dependency-risk-acceptance-2026-10-13.md` §2 第 1 项 |
| 2 | **F-8** | **CANCEL 三分支真栈对拍** + native C++→Python JSON 回调 | 同上 | 同上 | 同上 §2 第 2 项 |
| 3 | **F-9** | **in-dialog re-INVITE / UPDATE** | 同上 | 同上 | 同上 §2 第 3 项 |
| 4 | **F-11** | **CANCEL 先于任何下游响应** | 同上 | 同上 | 同上 §2 第 4 项 |
| 5 | **F-13 / 5.4-F-13 / NF-7 呼叫轨迹** | 按 Call-ID 查 SIP 消息轨迹 + 保留期清理；**判为重大漏项**（POC 基线能力回退，产品级实现至今为零） | 同上；无 trace store / API；O4 与 D5 已裁但实现未落 | 同上 | 同上 §2 第 5 项；`plan.md` §0 决策记录 2026-10-12「F-13 / NF-7」行；`plan.md` §5.4 表后「重大漏项裁定」段 |
| 6 | **REQ-F-12 主叫 / 正则规则**（四维 UI） | 主叫与正则两维能力 | M4 live 仅被叫 + 前缀；F-12 / F-14 签收范围**仅限被叫 + 前缀**，主叫 / 正则仍 `n-a` | 同上 | `plan.md` §5.4 表「主叫 / 正则规则（REQ-F-12 四维 UI）」行（计划归属 = v1.1）；`handoff/2026-10-12-remaining-items-execution.md` §4 末句 |
| 7 | **Lane D 4.2**（7×24 长稳报告）与 **4.3**（API 版本兼容策略） | 4.2 生产就绪评审需要稳定性证据；4.3 收口 `version-lifecycle.md` §7 的「候选、未决策」占位 | 归属裁定为「v1.1」，不纳入本版里程碑；4.3 属新增决策，需 requirement + ADR + review record | 同上 | `handoff/2026-10-10-unfinished-assessment-and-next-plan.md` Lane D 表与「状态（2026-10-12 晚些时候追加）」段；`plan.md` §0 决策记录 2026-10-12「Lane D 四项归属三选一裁定」行 |
| 8 | **零呼损滚动升级增强 feature** | 滚动升级零呼损（进程级 drain、S-SBC 透明桥 + StateStore、实例粘性、维护窗口口径等候选方向） | REQ-NF-4 本版按「接受实测呼损」签 pass（**非「零丢失已达成」**）；严格零呼损列今后 release 增强，本版不立项、不定义需求 | 同上 | `plan.md` §0 决策记录 2026-10-12「REQ-NF-4 滚动升级按『接受实测呼损』签收 pass」行；`reviews/m8-batch3-kind-sim-evidence-review-2026-10-12.md` B3-02 |
| 9 | **FM**（Fault Management） | 故障管理能力 | 定位为**未来项目 / 未来批次的新 feature**；当前不立项、不实现、不定义需求、不补 demo 或功能文档 | 未来启动时走既有新 feature 流程（requirement → ADR → design → review） | `handoff/2026-10-11-open-adjudication-register.md` §2 P6「现状更正」、§5 汇总表 P6 行；`plan.md` §0 决策记录 2026-10-11 P6 行 |
| 10 | **REQ-F-14 联动：白名单变更经审批后生效**（M8 批次 4 **D4-01** 的选项①） | 把「白名单变更」纳入变更单审批流 | D4-01 是**二选一、至今未裁**：① 纳入变更单（属 v1.1 新 feature，本版不立项，该矩阵行维持 `defer`）；② 修订矩阵 L86「白名单变更走审批（F-14 联动）」这一与代码事实冲突的说法（选②则该行可凭拒绝场景补测证据转 pass）。本行只对应选项① | requirement → ADR → design → review | [`handoff/2026-10-12-m8-batch4-complete-handoff.md`](handoff/2026-10-12-m8-batch4-complete-handoff.md) §5 第 1 项 |

启动流程一律 `requirement → ADR → HLD/LLD → 契约 → 代码+测试 → 验收项 + review record`（`AGENT.md` §3）。

---

## 4. 取值已裁、实现未落 / 待维护者取值类

| # | 既有编号 | 已裁的取值 | 仍未落的部分 | 阻塞源 | 来源指针 |
|---|---|---|---|---|---|
| 1 | **B2 / O4 / D5** 呼叫轨迹保留与存储 | O4＝默认保留 **10 天**、部署可配；D5＝**in-cluster PostgreSQL**；Redis 继续用于 runtime checkpoint | 轨迹**存储 / 查询 / 删除实现未落**；清理触发点与时间起算口径属「实现细节待定义」；`security-privacy.md` §4.1 记录的 chart **无备份 Job** 事实不变 | B2 的 requirement / ADR 起草已整体后置（见 §4-3）；F-13 / NF-7 亦转 v1.1 立项（§3-5） | `handoff/2026-10-12-b2-b3-deferred-items.md` §0 表 B2 行、§1（交付物与已知前置事实）；`plan.md` §0 决策记录 G6 行；`plan.md` §5.2 D5 行 |
| 2 | **B3 / O5 / D3** Redis HA 与容灾 | O5＝**站点内 N+1 + 跨站 1+1 warm standby**（不承诺机架 / AZ 级容错）；D3＝**Redis primary/replica + Sentinel**（ADR-0008），不选 Redis Cluster | **Sentinel 实现未落**；ADR-0008 是否覆盖 Sentinel 具体拓扑（几个 Sentinel、quorum、与 K8s 调度的关系）待确认；**RPO / RTO 数值仍未裁** | 同 §4-3；RPO / RTO 属对外可用性承诺，须维护者取值（§7-4） | `handoff/2026-10-12-b2-b3-deferred-items.md` §0 表 B3 行、§2（交付物与已知前置事实）、§5；`plan.md` §0 决策记录 G7 行 |
| 3 | **B2 / B3 的四项启动条件** | —（条件本身，非取值） | 下次开工前先逐项确认（四项条件原样保留，见下） | 未确认不得启动 | `handoff/2026-10-12-b2-b3-deferred-items.md` §4 |
| 4 | **M5D-1 … M5D-6** | — | 六行全部「移出 v1」且**保持未实现**；M5D-1 / M5D-5 阻塞于 O1 取值 → 无法排期；M5D-4 / M5D-6 阻塞于 D12 / O5（O5 容灾基线已裁、实现未落）→ 亦无法排期 | §5.1 **O1** / **D12 · O5** | `plan.md` §5.2-bis 表与表后「边界」段 |
| 5 | **PM / AM / UM** 产品管理能力缺口 | — | 需求待补：尚无获批的完整 requirement / acceptance（PM 缺 PRD 与验收标准；AM 缺告警生命周期管理；UM 缺完整账号生命周期、SSO / MFA 等） | 需求与验收标准获批前不并入任何批次 | `plan.md` §5.3 表 |
| 6 | **O1** 对外承诺值 | **内部工程目标 = loopback 模型下 ≥ CPS 1280 无失败**（仅限内部，不得写入任何对外材料） | **对外承诺值仍不填**；HPA 阈值 / 容量类告警 / ne-datasheet 容量取值 / 4.1 正式报告四项下游维持阻塞 | 缺业务判决路径实测 / 饱和点观测 / 目标环境多副本（`ne-datasheet.md` §3 填值准入条件三条均未满足） | `plan.md` §5.1 受阻项段与 2026-10-11 追加更正段；`plan.md` §0 决策记录 2026-10-12「B1 / O1 取值落定一层」行；`handoff/2026-10-12-m8-scope-revision-internal-release-plan.md` §0.6、§5 第 8 行 |
| 7 | **REQ-F-1** 的 14 条逐条 header 对拍 | — | 自动化子集已覆盖、**全文仍 open**；`test-plan.md` REQ-F-1 段的所有 `- [ ]` **一项未打勾** | 用例实现本身待 A4 e2e 批次（Wave 1 落地后启动），属 v1.1 排期事项 | `acceptance/2026-10-11-wave2-replay-register.md`「REQ-F-1 勾选」行；`plan.md` §0 决策记录 2026-10-11 P5 行 |
| 8 | **A3 Phase D** S5–S11 真栈用例实现 + **S8** 基线补采 | 排期已定稿：**P1 S5 → P2 S7a → P3 S6 → P4 S10 → P5 S9 → P6 S11** | **用例实现一批未落**，分批启动需维护者授权；**S8 登记为阻塞项** —— 基线缺 Route / Record-Route 头，M2 probe 补采前不排；REQ-F-5 按 N4 停止线不签 pass | S8 需 M2 probe 补采；其余需分批启动授权 | `handoff/2026-10-12-m8-scope-revision-internal-release-plan.md` §0.5；`handoff/2026-10-09-sip-native-testing-plan.md` §4-D；`plan.md` §0 决策记录 2026-10-12「A3 Phase D 排期定稿」行 |
| 9 | **NF-15** HPA 阈值 | 已裁：**填 `values-onprem.example.yaml`，默认 `values.yaml` 保持 null**（注明「kind 实测、非对外承诺、上线前须目标环境复测」） | 缺**带 per-pod CPU / 内存利用率**的测量批次；2026-10-12 饱和点探测未记录资源数据，不构成该批次；矩阵 NF-15 行维持 `open` | G5 四项下游（HPA 阈值 / 容量告警 / ne-datasheet / 4.1 报告）维持阻塞 | `handoff/2026-10-12-m8-scope-revision-internal-release-plan.md` §0.6 第 1 条、§6 第 4 项；`handoff/2026-10-12-m8-batch5-complete-handoff.md` §6 第 5 项 |
| 10 | **REQ-F-15** 完整 AS 栈 / **REQ-S-4** 正式全绿 / **PostgreSQL 16** | — | 三项补测仍 open（REQ-F-15 非 testbed notify / health；REQ-S-4 与 M4 工程关门分离；PG 16 为非阻塞 follow-up，证据基线 12.22） | 与 §4.4.3 / M7 集成后补测口径相关；C5 已把 REQ-F-13 / F-15 / S-4 / PG 16 一并登记为「已裁不做」（见 §6） | `plan.md` §5.4 补测表（REQ-F-15 行、REQ-S-4 行、PostgreSQL 16 行） |

### 4.3 B2 / B3 的四项启动条件（`handoff/2026-10-12-b2-b3-deferred-items.md` §4 原样保留）

- [ ] 维护者授权启动 requirement 起草
- [ ] **B3 的 RPO / RTO 数值**已有取值（否则 requirement 无处落验收标准）
- [ ] 确认 B2 的 PG 部署形态与 ADR-0026 的关系（修订还是新 ADR）
- [ ] 确认 B2 / B3 是否**合并**为一份「状态与持久化」requirement + ADR，还是分开

### 4.4 M5D-1 … M5D-6（`plan.md` §5.2-bis）

| 行 | 聚合的 defer 项 | 内容 | 阻塞源 | 状态 |
|---|---|---|---|---|
| **M5D-1** | C-1、C-2、C-3、C-9 | 告警规则与指标阈值 / 调用点：告警 6 条死规则（4 指标不存在 + 2 零调用点）、`clamp_min` 数学错误、telemetry 阈值 `> 0` 语义不符、指标零生产调用点 | §5.1 **O1**（阈值须 M6 实测）＋ §5.3 PM/AM ＋ M7 E1 | **移出 v1** |
| **M5D-2** | C-6、T-1 | 缩容守卫参控（当前读入只 log、不参与判定）＋ feature 开关开 / 关两态行为测试 | ADR-0020 / M7 actuation 未决；ADR-0020 默认态 / 灰度策略未决 | **移出 v1** |
| **M5D-3** | C-7 | OTLP 导出（当前为 NoOp sink，入队即丢） | §5.3 PM（OTel traces / logs 未落地） | **移出 v1** |
| **M5D-4** | H-8 | NetworkPolicy 无 Egress、源标签过宽 | §5.1 **D12 / O5**（HA 拓扑与客户 SLA） | **移出 v1** |
| **M5D-5** | H-11 | 无 resources（BestEffort）、AS 无 startupProbe、config-service tcpSocket 探针语义 | §5.1 **O1** / M6（sizing 下游于实测） | **移出 v1** |
| **M5D-6** | A-2 | 跨站点切换演练未做（ADR-0008 指派给 M5） | §5.1 **O5**（容灾等级客户 SLA） | **移出 v1** |

**并入说明（§8-14）**：Lane B4（Python 3.10 EOL / D1）的正式迁移**无编号、无载体** —— 3.12 验证 spike 已**完整回滚**（7 处 `requires-python` pin + `uv.lock` 全部还原，`git diff` → 0 处，重编回 cpython-310），正式迁移仍未做，需 requirement → ADR → review。该缺口与 **D1**（Python 3.10 EOL）同源，本表不为其单列新行，与 D1 一并跟踪（[`handoff/2026-10-10-unfinished-assessment-and-next-plan.md`](handoff/2026-10-10-unfinished-assessment-and-next-plan.md) Lane B4「spike 实测结论（2026-10-12）」与「正式迁移仍未做」两条；`plan.md` §5.2 D1 行）。

---

## 5. 文档与仓库卫生类（无外部依赖，可在 v1.1 排期时一并收口）

| # | 条目 | 现状 | 建议归属 | 来源指针 |
|---|---|---|---|---|
| 1 | 五份下游 stale 表述 —— `docs/delivery/airgap-package.md`、`docs/delivery/install-guide.md`、`docs/operations/rollback-playbook.md`、`docs/product/ne-datasheet.md`、`docs/product/version-lifecycle.md` 的 `0.0.0-skeleton` 与「O1 未裁决」 | 事实层面已过期（chart 已首次同步到 `0.2.0`、O1 内部工程目标值已落），原文按保史约定保留、未逐处回改 | 由包装文档负责方在下一次文档同步批次按「**原文保留 + 追加注记**」处理；**待维护者决定，本轮未 edit** | `handoff/2026-10-12-remaining-items-execution.md` §5 表与「处置建议（待维护者决定，不在本轮范围）」段 |
| 2 | PG 15.18 下 config-service 集成测试失败登记（`AmbiguousFunction`，PG 14+ 类型变更） | 已如实落 `FAIL-` 证据、**未改任何产品代码**；标准环境为 PG 12.22 故当前不阻塞，但 PG 12 已 EOL，与 **D1** 同类 | **是否立项修复待维护者决定** | `plan.md` §0 决策记录 2026-10-12「授权后的四项执行」行第 ② 项；`handoff/2026-10-10-unfinished-assessment-and-next-plan.md` 第 425–427 行与第 999 行 |
| 3 | `plan.md` §0 / §4 M8 行最终表述草案 | 草案在 `docs/acceptance/m8-plan-m8-row-draft-2026-10-12.md`，**未合并进 `plan.md`**，无合并责任人 | 待维护者确认表述后合并（批次 6 的 E-3 未执行该合并） | `handoff/2026-10-12-m8-batch6-complete-handoff.md` §5 第 1 项 |
| 4 | `defer` 状态词是否引入 | 批次 4 草案（7 pass / 10 defer）把 `defer` 作为**新增**状态词，须维护者确认后方可使用（D4-03）；2026-10-13 批次 4 终态化代签已按该词落终态计数 pass 27 / defer 4 / blocked 9 / n-a 9 并注明「defer 为本次新增状态词」 | 是否长期沿用**待维护者确认** | `handoff/2026-10-12-m8-batch4-complete-handoff.md` §2 末句、§5 第 3 项、§7「终态计数」行 |
| 5 | NF-15 矩阵行维持 `open` | 批次 5 明写「本批次不动」；是否在批次 4 终态化由该批次决定，交接对象未背书 | 随 §4-9 的测量批次一并裁决 | `handoff/2026-10-12-m8-batch5-complete-handoff.md` §6 第 5 项、§8「批次 5 判定 pass」段 |
| 6 | 工作树未提交改动与无归属文件（`.dockerignore`、`docs/intro.md`、批次 1 §2.3 记录的 4 个未提交改动文件、各批次 prompt 文件等；跟踪状态以现场为准） | **以 `git status` 现场为准，本文档不逐项固化**（清单随提交动作变化，固化即过期）；commit 拆分由维护者决定（`AGENT.md` §10.4） | 维护者：commit 拆分与 tag | `handoff/2026-10-12-m8-batch1-complete-handoff.md` §2.3；`handoff/2026-10-12-m8-batch3-complete-handoff.md` §6 第 3 项；`handoff/2026-10-12-m8-batch4-complete-handoff.md` §5 第 8 项；`handoff/2026-10-12-m8-batch5-complete-handoff.md` §6 第 3 项；`handoff/2026-10-12-m8-batch6-complete-handoff.md` §5 第 7 项 |
| 7 | `docs/acceptance/report.md` §0.5 计数口径不一致 | §0.5 原文（2026-10-06）为 open 24 / blocked 12 / pass 9 / n-a 4，与矩阵终态 pass 27 / defer 4 / blocked 9 / n-a 9 不一致；已有 §0.10「计数同步与内部版收尾声明」追加说明，§0.5 原文保留为历史值 | 不回改 §0.5；读者以 §0.10 为准 | `acceptance/report.md` §0.5、§0.10 |
| 8 | **performance 层门禁终态**（M8 批次 5 **B5-04**） | 二选一**至今未裁**：① 实现 `make gate` 阻塞层；② M8 总审书面接受风险。2026-10-13 路径 C 已书面接受**外部硬依赖风险**，但**没有就该层单独落裁**，故本项不能视为已被路径 C 覆盖 | 待维护者另行确认；确认后按 §9 启动前置另行排期 | [`handoff/2026-10-12-m8-batch5-complete-handoff.md`](handoff/2026-10-12-m8-batch5-complete-handoff.md) §6 第 1–2 项 |
| 9 | **config-service 单连接 PG 重启后不自动重连**（M8 批次 3 **B3-04**；`500` → 重启恢复） | 是否立项**未裁**；评审记录 B3-04 仍标「待维护者确认 / 待裁决」 | 待维护者在 §7 类动作中逐行裁决 | [`handoff/2026-10-12-m8-batch3-complete-handoff.md`](handoff/2026-10-12-m8-batch3-complete-handoff.md) §6 第 2 项、第 4 项 |
| 10 | **白名单 `authorize_peer` 地址 / 证书 OR → AND 语义**（M8 批次 4 **D4-02**） | 当前**地址命中即放行、不要求对端证书**；是否收紧为 AND **未裁**（属安全口径，不由 agent 代裁） | 待维护者裁决 | [`handoff/2026-10-12-m8-batch4-complete-handoff.md`](handoff/2026-10-12-m8-batch4-complete-handoff.md) §5 第 2 项 |
| 11 | **根 `README.md` 环境变量表缺口** | 当前 **0/16** 覆盖；非阻塞，`docs/acceptance/report.md` §0.7 已登记 | 随下一次文档同步批次一并处理 | [`handoff/2026-10-12-m8-batch6-complete-handoff.md`](handoff/2026-10-12-m8-batch6-complete-handoff.md) §5 第 5 项 |

---

## 6. 已裁不做（保留记录，≠ closed）

登记表照抄 [`handoff/2026-10-10-unfinished-assessment-and-next-plan.md`](handoff/2026-10-10-unfinished-assessment-and-next-plan.md) §12.1：

| 项 | 登记结论 | 不做的影响（**只说一次**） |
|---|---|---|
| **C1** 外部部分 | **不做** | E1 / E4 / E5 中需要运营商 PKI 或客户 K8s 的部分长期 open（本地真栈部分已随 A2 / A3 完成） |
| **C2** D-1 运营商 PKI + 外网 S-SBC | **不做** | REQ-S-2 / REQ-S-3 长期 open |
| **C3** D-2 客户 K8s REQ-NF-1 live | **不做** | REQ-NF-1 live（kill / restart / BYE）长期 open |
| **C4** 包装 2.4 摘流 / 2.5 备份恢复演练 | **不做** | 上述两项演练记录缺失 |
| **C5** REQ-F-13 / F-15 / S-4 / PostgreSQL 16 | **不做** | 四项补测长期 open |
| **W3** | **随 C 栏一并登记为不做** | 同上 |

- **「不做 ≠ closed」** —— 这些 REQ 在 `docs/acceptance/report.md` 中**仍为 open**，open / blocked 计数**不因本节而改**（§12.2 第 2 条）。
- 若将来重启外部采证，**届时**重新排期，并在**本节追加**重启记录，不改写本节（§12.2 第 4 条）。
- 后续一切盘点只引指针，不逐项复述（§12.2 第 1 条）。

---

## 7. 待维护者亲签 / 取值（agent 不得代签、不得代裁）

| # | 事项 | 当前状态 | 为何不能由 agent 完成 | 来源指针 |
|---|---|---|---|---|
| 1 | **M8 退出签字栏的维护者亲签** | 签字栏 = **agent 代签（维护者 2026-10-13 授权）**，**不是维护者亲签**；授权前的历史纪律「本栏不得由 agent 代签」保留为授权前原文 | 代签 ≠ 亲签；该栏的效力来源只能是维护者本人 | `reviews/m8-external-dependency-risk-acceptance-2026-10-13.md` §4 签字节与表后两条 2026-10-13 填写；`acceptance/report.md` §0.11 第 1 条 |
| 2 | **M1 退出签字** | 「维护者签字」栏 = **待填**（评审人栏为 AI agent，2026-09-28） | 签字栏只能由维护者填写 | `reviews/m1-exit-review.md` §确认签字表；`plan.md` §0「M1 完成日期」行 |
| 3 | **M6 里程碑签收** | **仍 open**（M2 / M6 / M7 为「工程完成」，≠ 里程碑签收） | 里程碑签收属维护者动作；「工程完成」≠「里程碑签收」≠「REQ 全绿」 | `plan.md` §0 当前状态行（「维护者 M6 里程碑签收仍 open」）与 2026-10-12 N2 代签行边界段 |
| 4 | **B3 的 RPO / RTO 取值** | **仍未裁**（O5 / D3 拓扑取值已裁，RPO / RTO 数值属留空） | 属**对外可用性承诺**，须维护者取值，不由 agent 代裁 | `handoff/2026-10-12-b2-b3-deferred-items.md` §2.1 第 1 项、§5 第 3 条；`plan.md` §0 决策记录 G7 行 |
| 5 | **O1 对外承诺值** | **不填**（内部工程目标 = loopback 模型 CPS 1280 无失败，仅限内部） | 对外容量 / SLA 数字须维护者裁决；`ne-datasheet.md` §3 填值准入条件三条均未满足 | `plan.md` §5.1 受阻项段；`plan.md` §0 决策记录 2026-10-12「B1 / O1 取值落定一层」行 |
| 6 | **A4-4 的门禁配置变更授权**（e2e 是否重新纳入 `make test`、kind e2e 是否进 PR required） | 裁决明写：**这是配置变更授权，A4-4 裁决明确本次不授权；要改需维护者另行批准** | 配置变更授权只能由维护者给出；A4-4 只落了政策方向 | `handoff/2026-10-10-unfinished-assessment-and-next-plan.md` §13.1 表第 2 行；`plan.md` §0 决策记录 G2 / A4-4 行 |

---

## 8. 零空遗留核对表

本表逐项核对「已声明 close 但条目无归属」的情况；**每一项都必须在本文有落点**，不留无归属的遗留。

| # | 现象（出处） | 本文落点 |
|---|---|---|
| 1 | `reviews/m8-external-dependency-risk-acceptance-2026-10-13.md` §4 签字栏「维护者亲签 —— 待填写」 | §7-1 |
| 2 | `docs/acceptance/report.md` §0.11 / M8 退出签字与亲签分离 | §7-1 |
| 3 | `handoff/2026-10-11-open-adjudication-register.md` §7.5 清单漏列 P4（只列 7 项），§6.1 按实际记载补入 | §5-7（登记口径不一致，原文不回改） |
| 4 | 同上 §5 汇总表 G9-a / G10 / G11 状态漏改，靠 §6.1 兜底 | §5-7 |
| 5 | `handoff/2026-10-10-unfinished-assessment-and-next-plan.md` Lane B6「accept 16 / 需修改 0 / 驳回 0」但同句列出 6 项未闭环（chart `--apply`、`kubeVersion`、RPO / RTO、O1、X1、真实集群） | §4（chart 同步已执行、`kubeVersion` 已写入；RPO / RTO → §4-2；O1 → §4-6）与 §2（X1、真实集群） |
| 6 | 同 §12 C1–C5、W3「已裁不做 ≠ closed」、无重启载体 | §6 |
| 7 | M8 批次 1 完成但 4 个文档未提交改动、无归属 | §5-6 |
| 8 | M8 批次 3：`.dockerignore`、`docs/intro.md`（未跟踪、来源不明）、`batch5-prompt.md` 反复记为遗留无归属 | §5-6 |
| 9 | M8 批次 4：7 pass / 10 defer 草案中 `defer` 状态词未批，10 行悬空 | §5-4 |
| 10 | M8 批次 5：NF-15 矩阵行维持 `open`，本批次明确不接、交接对象未背书 | §5-5 / §4-9 |
| 11 | M8 批次 6：`plan.md` §0 / §4 M8 行表述草案未合并 | §5-3 |
| 12 | `handoff/2026-10-12-remaining-items-execution.md` §5 五份文档 stale、处置建议无载体无排期 | §5-1 |
| 13 | `plan.md` §5.2-bis M5D-1…M5D-6「移出 v1」之后无落点 | §4-4 |
| 14 | `handoff/2026-10-10-unfinished-assessment-and-next-plan.md` Lane B4：Python 3.12 spike 已回滚，正式迁移无编号无载体 | §4（并入 D1 行说明，见 §4.4 末段） |
| 15 | `handoff/2026-10-12-remaining-items-execution.md` §4：F-12 / F-14 主叫 / 正则「仍 n-a，v1.1」无登记载体 | §3-6 |
| 16 | `docs/reviews/product-packaging-plan-review-2026-10-09.md`：声称 24 项 gap 全关闭，但备注列仍留有「待 O1 裁决」「待 O4/D5 裁决」的行（G-P0-3、G-P0-8、G-P1-3 与 G-P1-5、G-P1-8） | §4-6（O1）/ §4-1（O4 / D5） |
| 17 | `handoff/2026-10-12-m8-scope-revision-internal-release-plan.md` §0.8：`report.md` §0.5 计数未同步 | §5-7 |
| 18 | M8 批次 5 §6 第 1–2 项（performance 层门禁终态 B5-04）此前在本文无落点 | §5-8 |
| 19 | M8 批次 3 §6 第 2、4 项（B3-04 config-service PG 重连）此前在本文无落点 | §5-9 |
| 20 | M8 批次 4 §5 第 2 项（D4-02 `authorize_peer` OR / AND 语义）此前在本文无落点 | §5-10 |
| 21 | M8 批次 4 §5 第 1 项（D4-01 白名单变更审批）此前在本文无落点 | §3-10 |
| 22 | M8 批次 6 §5 第 5 项（根 `README.md` 环境变量表缺口）此前在本文无落点 | §5-11 |

---

## 9. 启动前置与停止线

- **启动流程**：`requirement → ADR → HLD/LLD → 契约 → 代码+测试 → 验收项 + review record`（`AGENT.md` §3）；**每项启动前须有维护者显式授权**。
- **停止线**：未取得外部资源 / 未获维护者裁决的项**不得开工**；**不得因本机工作顺带推进**（沿用 [`handoff/2026-10-12-m8-scope-revision-internal-release-plan.md`](handoff/2026-10-12-m8-scope-revision-internal-release-plan.md) §1.1 表后口径）。
- **后置 ≠ 取消**；重启条件统一为「**维护者另行裁决 + 外部资源到位**」。
- **本文是载体**：重启时在本文对应行**追加**记录，**不改写既有行**（与 §6、`handoff/2026-10-12-b2-b3-deferred-items.md` §5 同口径）。

---

## 10. 边界（不得据本文推出过度结论）

1. 本文不签收任何 REQ / 里程碑，不改任何矩阵状态词，不改 `docs/acceptance/report.md` 计数。
2. 本文**不是发行版本定义**；根 `VERSION` 仍为 `0.2.0`，未 bump、未 tag；tag 仅维护者执行（`AGENT.md` §10.4）。
3. 把项收进本文**不等于已排期**，更不等于已启动或已实现。
4. 第 2 节的外部硬依赖：**接受风险 ≠ 验证通过**；**重启 ≠ 自动开始**。
5. 第 4 节「取值已裁」**不等于已实现** —— O4 / D5 / O5 / D3 均为「取值已裁、实现未落」。
6. 内部工程目标（loopback 模型 CPS 1280 无失败）**仅限内部**，不得写入任何对外材料；本文不产生任何对外容量 / SLA 数字。
7. **M5 REQ 级仍是不通过**；M8 签字覆盖里程碑退出，不覆盖 REQ 级验收。
8. 本文不执行任何 git 写操作（无 add / commit / tag / push / 建分支 / 改 remote）。
9. 本文若被后续证据或维护者裁决推翻，**须追加行说明**（日期 + 被推翻条目 + 依据），不得静默替换。
10. 第 5 节第 8 项（performance 层门禁终态）**不得视为已被 2026-10-13 路径 C 覆盖** —— 路径 C 接受的是外部硬依赖风险，与该层的二选一是两件事。

---

落盘日期：2026-10-13。状态：已登记，未排期，未启动，未实现。
