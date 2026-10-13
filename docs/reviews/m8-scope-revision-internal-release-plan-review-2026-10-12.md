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

# Review Record — M8 范围修订与内部版本收尾计划

- **评审对象**：[`docs/handoff/2026-10-12-m8-scope-revision-internal-release-plan.md`](../handoff/2026-10-12-m8-scope-revision-internal-release-plan.md)（状态：计划 / 未提交）
- **评审日期**：2026-10-12
- **评审人**：AI agent（TraeCode）—— 仅评审与列出 gap，**不签字**，裁决为评审人建议、待维护者确认
- **评审范围**：
  - 计划对上游文档的事实陈述一致性（RC 计划、2026-10-10 盘点、2026-10-09 SIP native 计划、验收矩阵 `m8-test-plan-matrix.md`、`m8-environment-evidence.md`、`report.md`、`plan.md`、`deploy/docker/Dockerfile`、`environments.md`、`2026-10-12-o1-and-native-reproducibility.md`）
  - 计划内部一致性（§1 范围重划 / §2 六批次 / §4 完成定义 / §5 移交清单 / §6 裁决项 / §7 边界）
- **评审结论（历史，保留）**：**有条件通过** —— 事实底座经核查基本准确（见 §3）；发现 2 条 P1、2 条 P2，均不推翻本计划的定位（内部版本 / 不签收 M8），但需订正后方可作为执行输入。

---

## 当前状态（Current Status）

> 本节反映当前落盘现状；上方原始评审结论保留为历史。

- **一句话结论**：事实基线核查通过；发现 1 条 P1 与上游不一致（A3 Phase D 顺序）、1 条 P1 计划内部冲突（§4.2 与 §1.1/§5/§7.2），另 2 条 P2。订正前不建议作为执行输入。
- **gap 统计**：P0 = 0；P1 = 2（G-1、G-2）；P2 = 2（G-3、G-4）。其中「待修改」3 条、「非问题（已关闭）」1 条。
- **门禁**：N/A（纯文档评审，无代码改动）。
- **签字状态**：**未签**（签字为维护者的动作）。
- **未闭环项**：G-1、G-2、G-3 待修改；去向均为**被评计划文档**（§0.5 / §2 依赖图 / §2.2 / §4.2 / §5 / §1.1 表 A）；触发条件 = 维护者确认裁决后由 writing subagent 订正被评文档，并在本记录回填复核结论。

---

## 1. 总体评价

本计划定位清晰、边界纪律强（反复声明"不签收任何 REQ / 不签收里程碑、不改矩阵 status、不改 report.md 计数、不执行 git 写操作"），与 `AGENT.md` §3.2、§11 的约束一致。事实底座经逐项核查**基本准确**：矩阵现行计数、open/blocked 行集合、N3 代签口径、`report.md` §0.5 计数、`plan.md` §0 版本口径与 §5.2 / §5.4、Dockerfile 现状、restriction 四层口径、环境登记、编号口径表，均与上游一致（详见 §3）。

主要问题集中在两处：其一是 §2 对 A3 Phase D 排序的处理与上游 §4-D **不一致却被标注为"按 §4-D 落地"**（G-1）；其二是 §4 完成定义对 open restriction 行（D12/O5-HA）的要求与 §1.1/§5/§7.2 相冲突（G-2）。二者均属"半同步"类问题——计划自己的其余章节与上游并未同步，读者据不同章节会得到互相矛盾的结论。

---

## 2. Gap 清单（P0 / P1 / P2）

### G-1（P1）A3 Phase D 执行顺序与上游 §4-D 不一致，且被误标为"按 §4-D 落地"

- **位置**（被评文档）：§0.5（L64）、§2 依赖顺序图（L123–133）、§2.2 执行顺序表（L156–162）。
- **计划写法**：执行顺序写作 `P1 S5 → P6 S11 → P2 S7a → P3 S6 → P4 S10 → P5 S9`，并在 §2.2 声称"排期已定稿于 `2026-10-09-sip-native-testing-plan.md` §4-D，本批次按此落地"（L152）。
- **上游实际**（[`docs/handoff/2026-10-09-sip-native-testing-plan.md`](../handoff/2026-10-09-sip-native-testing-plan.md) §4-D.2，L179–189）：优先级为 **P1 S5 → P2 S7a → P3 S6 → P4 S10 → P5 S9 → P6 S11**；§4-D.3 边界 1（L193）明确"实现按 **P1→P6** 分批启动"。
- **差异与风险**：计划把 P6（S11 CANCEL 与最终响应竞态）从**最后**提到**第 2 位**；而 §2.2 给 S11 的理由（"竞态两分支确定性证明成本最高、flaky 风险最大"）恰是上游 §4-D.2（L188）把它**放最后**的理由——理由与位置自相矛盾，且与"按 §4-D 落地"的表述冲突。
- **建议修复**：二选一——(a) 恢复 §4-D 的原顺序；(b) 若确要重排，在 §2.2 显式声明"本批次对 §4-D 顺序做了调整"并写明调整理由，同时删除/更正"按 §4-D 落地"的表述。两处（§0.5、§2 依赖图、§2.2）须一次性同步。

### G-2（P1）§4 完成定义与 §1.1/§5/§7.2 对 open restriction 行（D12/O5-HA）的要求相互冲突

- **位置**：§4.2（L246）vs §1.1 表 A（L96、L100）、§5（L260）、§7.2（L286）。
- **计划写法**：§4.2 要求"**17 个 open 行**（含 NF-10、NF-13、NF-14、NF-15 等）全部转终态（pass / n-a / defer，必带理由），**不得留下未解释 open**"。
- **冲突**：`D12/O5-HA` 现行状态为 **open**（矩阵 L117），且属外部硬依赖 restriction 行；§1.1 表 A、§5、§7.2 均要求它"**保持原状态词（open）**"并指向表 A。因此 D12/O5-HA 无法"既转终态、又保持 open"——两条要求不能同时成立。
- **建议修复**：在 §4.2 为 restriction 的 open 行（至少 D12/O5-HA）显式豁免，或将该行从"open 行须转终态"的统计口径中单列并注明去向。

### G-3（P2）"移出下一 release"清单在 §1.1 表 A 与 §5 之间不一致

- **位置**：§1.1 表 A（L91–98）vs §5 移交清单（L262）。
- **说明**：§5 列有"包装 2.5 备份恢复（客户真实集群版）| 客户真实集群演练未做 | 客户真实集群"，但 §1.1 表 A（移出下一 release）**未列该项**，却列了同类外部依赖的"包装 2.4 摘流 / iFC 配合"。两张清单对同类项的收录口径不一致。
- **建议修复**：把"包装 2.5 备份恢复（客户真实集群版）"补入 §1.1 表 A；或在 §5 注明其不在表 A 口径内的理由。

### G-4（P2）§1.2 表 B 与 §2.3 取证表的行归属不完全对应——建议判为**非问题**

- **位置**：§1.2 表 B（L107）vs §2.3 取证表（L172–179）。
- **说明**：§1.2 表 B 把 NF-13 / NF-14 / NF-15 纳入"模拟器 / kind 可取的证据行"大类，但 §2.3 取证表只列 NF-2/NF-4/NF-9/NF-5、F-15 与 5.4-F-15真AS、NF-10；NF-13/NF-14 由 §2.3 尾注（L181）指向"签收与评审"批次处理，NF-15 归 §2.5 批次。
- **判定**：**非问题**（已给出理由后关闭）——行归属实际完整、非遗漏，§2.3 尾注与 §2.5 已分别交代去向；仅是可读性可再优化。
- **可选建议**：在 §2.3 加一句交叉指向，避免读者误以为 NF-13/NF-14/NF-15 被遗漏。

---

## 3. 一致性检查（与上游文档）

| 计划的陈述 | 上游出处 | 结论 |
|---|---|---|
| 矩阵计数 pass 16 / open 17 / blocked 10 / n-a 6 / fail 0 | [`m8-test-plan-matrix.md`](../acceptance/m8-test-plan-matrix.md) N2/N3 代签节（L138–196） | 属实 |
| open 17 行集合恰为 F-4/F-5/F-8/F-9/F-10/F-11/F-16/NF-2/NF-5/NF-9/NF-10/NF-13/NF-14/NF-15/S-1/S-4/D12/O5-HA | 同上 | 属实 |
| blocked 10 行集合恰为 F-13/5.4-F-13/F-15/5.4-F-15真AS/NF-1/NF-4/NF-7/S-2/S-3/ADR-0008-演练 | 同上 | 属实 |
| N3 代签 7 行（F-1/F-2/F-3/F-6/F-7/F-12/F-14），口径为"工程证据接受"、非 REQ 级验收 | 同上（L170–196） | 属实 |
| `report.md` §0.5 计数仍为 open 24 / blocked 12（pass 9 / n-a 4） | [`report.md`](../acceptance/report.md) §0.5（L44–52） | 属实 |
| `plan.md` §0 无 v1 / v1.1 定义；产品版本号只看根 `VERSION`（当前 0.2.0） | [`plan.md`](../plan.md) §0（L11–18）、`VERSION` | 属实 |
| `plan.md` §5.2 含 D1~D12（含 D5 in-cluster PostgreSQL、D12 集群内 PG/Redis HA） | [`plan.md`](../plan.md) §5.2（L488–495） | 属实 |
| Dockerfile 仍为 M5 进程壳（`ENTRYPOINT ["python", "-m", "as_platform"]`；`EXPOSE 5060/udp 5061/tcp` 仅端口声明） | [`deploy/docker/Dockerfile`](../../deploy/docker/Dockerfile)（L23–40） | 属实 |
| 发布镜像缺口"重开 M8 之前补上"；M8 行"RC 产物就绪、退出签字仍搁置" | [`plan.md`](../plan.md)（L11–18、L192–204）、[`pre-m8-demo-review-plan.md`](../handoff/pre-m8-demo-review-plan.md)（L144）、[`2026-10-07-m8-next-step-plan.md`](../handoff/2026-10-07-m8-next-step-plan.md)（L2–8） | 属实 |
| `plan.md` §5.4：REQ-S-4 正式全绿归 M8 或维护者单独签收 | [`plan.md`](../plan.md)（L551–562） | 属实 |
| restriction：D-1 牵动 S-2/S-3、D-2 牵动 NF-1、ADR-0008 演练、D12/O5-HA；NF-2/NF-4/NF-9 用自有 kind，NF-5 用 M7.1 透明桥（无 Kamailio） | [`m8-environment-evidence.md`](../acceptance/m8-environment-evidence.md)（L26–38、L39–55、L69–85） | 属实 |
| 环境登记 `dev-win03ib7niepf0`（WIN-03IB7NIEPF0）、kind 0.24.0、kubectl 1.31.4、集群 as-m5 / as-m71 | [`environments.md`](../environments.md)（L37–49）、[`m71-sim-platform-evidence.md`](../acceptance/m71-sim-platform-evidence.md)（L10–17） | 属实 |
| o1 文档 §2 `deploy/compose` 为 PG/Redis integration 依赖；§4 20→1280 CPS 全成功、未测到饱和点、未记录资源数据 | [`2026-10-12-o1-and-native-reproducibility.md`](../handoff/2026-10-12-o1-and-native-reproducibility.md)（L48–67、L137–175） | 属实 |
| 编号口径表：RC 计划 A-1~A-7 / B-1~B-7 / D-1~D-3 / E-1~E-6；2026-10-10 盘点 A2~A6（Lane A）/ B1~B6（Lane B） | [`2026-10-06-m8-release-candidate-plan.md`](../handoff/2026-10-06-m8-release-candidate-plan.md) §4；[`2026-10-10-unfinished-assessment-and-next-plan.md`](../handoff/2026-10-10-unfinished-assessment-and-next-plan.md) Lane A/B | 属实 |
| 引用的 7 个 handoff 文件及 N2 代签记录均存在 | `docs/handoff/` | 属实 |
| "A3 Phase D 按 §4-D 落地"（执行顺序） | [`2026-10-09-sip-native-testing-plan.md`](../handoff/2026-10-09-sip-native-testing-plan.md) §4-D | **不符 —— 见 G-1** |

---

## Adjudication（裁决记录）

> 裁决为**评审人建议**，须维护者确认后方可执行；签字为维护者动作。

| ID | 来源 | 问题摘要 | 裁决 | 修改方案 | 状态 | 验证方式 | 备注 |
|---|---|---|---|---|---|---|---|
| G-1 | 评审人（一致性检查） | §0.5/§2/§2.2 的 A3 Phase D 顺序与上游 §4-D 不符，却标为"按 §4-D 落地" | 接受（建议） | 恢复 §4-D 原顺序；或显式声明顺序调整及理由并删除"按 §4-D 落地"表述；三处同步 | 待修改 | 文档更新 | 待维护者确认 |
| G-2 | 评审人（内部一致性） | §4.2"17 个 open 行全部转终态"与 §1.1/§5/§7.2 对 D12/O5-HA"保持 open"冲突 | 接受（建议） | 在 §4.2 豁免 restriction 的 open 行，或将其从"open 须转终态"口径中单列 | 待修改 | 文档更新 | 待维护者确认 |
| G-3 | 评审人（内部一致性） | §1.1 表 A 未收录 §5 中的"包装 2.5 备份恢复（客户真实集群版）" | 接受（建议） | 补入表 A，或在 §5 注明其不在表 A 口径内的理由 | 待修改 | 文档更新 | 待维护者确认 |
| G-4 | 评审人（可读性） | §1.2 表 B 与 §2.3 取证表的行归属不完全对应 | 驳回 | 无需修改；可选：§2.3 加交叉指向 | 已关闭 | 文档已有交代 | 非问题：§2.3 尾注与 §2.5 已分别交代 NF-13/NF-14/NF-15 去向 |

> 复核 round 1 判定 G-1 / G-2 / G-3 三处均已真正关闭（详见下方「AI 复核结论」节），状态列更新待维护者确认。

---

## AI 复核结论（Verification）

本轮为**首次评审**，尚未进行订正后复核。G-1 / G-2 / G-3 处置完成后，须由**独立复核 agent** 回到被评文档正文逐条实证（不得采信本表自述），判定"真正关闭 / 表面关闭 / 未关闭"，并检查是否引入新的不一致，再回填本节。

### 复核 round 1（2026-10-12）

**复核人**：独立复核 agent（m8-verifier）。复核方法：回到被评计划正文读取现行文本（不采信任何转述），与上游 [`2026-10-09-sip-native-testing-plan.md`](../handoff/2026-10-09-sip-native-testing-plan.md) §4-D.2 / §4-D.3 及 [`m8-test-plan-matrix.md`](../acceptance/m8-test-plan-matrix.md) L117 逐条比对。

**逐条实证结果**：

| ID | 判定 | 证据（被评计划现行文本，行号 + 摘录） |
|---|---|---|
| G-1 | **真正关闭** | 三处均为上游 §4-D.2 原序（P1 S5 → P2 S7a → P3 S6 → P4 S10 → P5 S9 → P6 S11）：§0.5 排期段（L64）「P1 S5 两腿归一化对拍 → P2 S7a SDP corpus → P3 S6 规则优先级 → P4 S10 非 2xx → P5 S9 in-dialog → P6 S11 CANCEL 竞态」；§2 依赖顺序图（L126）「S8 前置补采 → P1 S5 → P2 S7a → P3 S6 → P4 S10 → P5 S9 → P6 S11」；§2.2 执行顺序表（L157–163）第 1–6 行依次为 P1 S5 / P2 S7a / P3 S6 / P4 S10 / P5 S9 / P6 S11，第 0 行为 S8 基线补采（与上游 §4-D.2 阻塞行「补采完成后建议插在 P3 之后」口径一致）。§2.2 表上方「本批次按此落地」（L153）现已属实；场景列与备注列逐行与上游 P1–P6 的「为什么排这个位置」对应（如 P6 行 L163「确定性证明成本最高、flaky 风险最大」与上游放最后的理由一致），未串行。 |
| G-2 | **真正关闭** | §4 第 2 条（L247）已显式豁免：「17 个 open 行中，外部硬依赖 restriction 行 D12/O5-HA 按 §1.1 表 A 保持 open 并指向表 A（不要求转终态），其余 16 行全部转终态……10 个 blocked 行中……restriction 行（S-2 / S-3 / NF-1 / ADR-0008-演练 / D12/O5-HA）保持原状态词并指向表 A」。与 §1.1 表 A（L96 收列 + L101「保持原状态词（blocked / open）」）、§5（L261）、§7.2（L287）不再冲突；D12/O5-HA 上游口径为 open + restriction（矩阵 L117「不能签 pass | open」）亦相符。 |
| G-3 | **真正关闭** | §1.1 表 A（L98）已收录「包装 2.5 备份恢复（客户真实集群版）| 客户真实集群演练未做；kind bundled state 不是生产备份恢复 | 客户真实集群」，与 §5（L263）同项口径一致。 |
| G-4 | **已关闭（非问题）** | 维持原判定；可选交叉指向已加——§2.3 尾注（L182）现含「（NF-15 不在上表内并非遗漏：归 §2.5「性能与容量」批次；NF-13 / NF-14 去向见本段前句。）」。 |

**新引入问题检查**：

- 复核中发现 §2.3 边界段把「NF-13 / NF-14 的 live 采集与真实触发涉 X1、终态在『签收与评审』批次按理由处理」说了两遍（原句 + 新加括号句）。已执行修正：括号句精简为仅保留交叉指向的最小形式（NF-15 去向 + NF-13/NF-14 指回前句），修正后该段中 NF-13 / NF-14 / NF-15 三行的去向各自只有一处交代、无遗漏、无重复。
- 修正后复查：未发现新的不一致——该修正不涉及任何顺序、口径或状态词表述，仅删除重复。

**边界声明**：本复核只针对订正落地，**不签收任何 REQ / 里程碑**，不构成维护者确认；Adjudication 表状态列更新待维护者确认。

---

## 签字

- **签字状态**：**未签**。
- **授权基础**：无。本次评审由 AI agent 执行，仅产出 gap 清单与建议裁决；裁决与签字须由维护者作出（`AGENT.md` §3.2、§3.3；`.trae/rules/review-adjudication.md`）。

---

（本记录为评审 round 1；被评对象为**计划**，本记录不签收任何 REQ、不签收任何里程碑、不改矩阵任何行状态。）