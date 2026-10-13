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

# 产品化包装 16 份文档 · 评审项目清单（B6）

> **落盘日期：2026-10-12。状态：评审已执行（2026-10-12），16 份结论全部为「需修改」（accept 0 / 驳回 0）；结论由 agent 分批评审 + 主 agent 抽查复核后填写，待维护者确认。**
>
> **本文是 B6 的评审载体**：[`../handoff/2026-10-10-unfinished-assessment-and-next-plan.md`](../handoff/2026-10-10-unfinished-assessment-and-next-plan.md)
> §4 **B6 · 产品化包装 16 份文档的评审**，出口判据为
> 「16 份文档逐份评审，结论（accept / 需修改 / 驳回）留 review record；需修改项闭环后复评；
> `docs/product-packaging-plan.md` §5 的批次状态按评审结果更新」。**谁做：维护者。**
>
> 维护者 2026-10-12 要求「评审项目单独落盘」——本文件即该落盘物：
> 它把「评审什么」固定下来，**不替维护者填任何结论**。
>
> **2026-10-12 追加：维护者指示执行评审并落盘，结论栏由 agent 填写（依据为 2026-10-12 已生效的 G6/G7/G8/G4 等已裁口径与仓库实测）；结论留待维护者确认，不构成对外交付或验收依据。**
>
> **2026-10-12 再追加（闭环复评）**：16 份「需修改」项已全部闭环并复评 —— 复评结论见 **§7**（accept 16 / 需修改 0 / 驳回 0，**待维护者确认**）；§1–§6 为闭环前记录，原文未改。
>
> **本文件所填结论不代替维护者的最终判断**；结论栏已于 2026-10-12 由 agent 填写（见 §3 与 §6），维护者确认前不作为任何签收依据。

---

## 1. 计数口径（先对齐，避免"16 份"指的不是同一批东西）

| 目录 | 计入的 `.md` 份数 | 明细 |
|---|---|---|
| `docs/product/` | **6** | `one-pager.md`、`compliance-matrix.md`、`ne-datasheet.md`、`responsibility-matrix.md`、`security-privacy.md`、`version-lifecycle.md` |
| `docs/operations/` | **7** | `README.md`、`runbook-l1.md`、`runbook-l2.md`、`alert-response-matrix.md`、`fault-demarcation.md`、`rollback-playbook.md`、`backup-restore.md` |
| `docs/delivery/` | **3** | `README.md`、`install-guide.md`、`airgap-package.md` |
| **合计** | **16** | — |

**不计入 16 份、但同批需要过目的附带资产**（评审 16 份时通常要一并看）：

- `docs/operations/grafana-dashboards/` 下 **2 份 Grafana 看板 JSON** + 看板 `README.md`
- `docs/delivery/preflight.sh`
- `docs/delivery/scripts/` 下 `bundle-images.sh`、`load-images.sh`、`images.txt`

---

## 2. 每份都要过的四个通用维度

维护者逐份评审时，建议对**每一份**都回答这四个问题（结论栏即填这四项）：

| # | 维度 | 要回答什么 |
|---|---|---|
| **D-1** | **事实准确性** | 文档所述与仓库**当前实际状态**是否一致？有无 stale 表述（例如仍写「待裁决」但取值已裁、或反过来的） |
| **D-2** | **与已裁决口径的一致性** | 是否与 §0 决策记录表里**已生效**的裁决一致（尤其 O4 / D5 / O5 / D3 / G4 版本口径 / 目标场景与命名 G8） |
| **D-3** | **对外可用性** | 这份能不能作为**对外交付或验收依据**？若不能，缺什么 |
| **D-4** | **follow-up** | 是否需要修改 / 补写 / 等别的裁决；需要的写明依赖 |

结论取值：**accept** / **需修改（写明项）** / **驳回（写明理由）**。

---

## 3. 逐份清单（结论栏已于 2026-10-12 由 agent 填写，待维护者确认）

### 3.1 `docs/product/`（6 份）

| # | 文件 | 已知需重点核对的点 | 结论 | 备注 |
|---|---|---|---|---|
| 1 | [`one-pager.md`](../product/one-pager.md) | 目标场景口径是否为已裁的「xx运营商 内部生产就绪 / 发版评审」（G8）；产品描述名是否为 `In-house IMS Application Server` | 需修改 | G8 三项 stale（:5/:6/:7）；O4/D5/O5 stale（:170-172）；e2e=0（:168） |
| 2 | [`compliance-matrix.md`](../product/compliance-matrix.md) | `:79` / `:117` / `:234` / `:266` 记录的「14 条全文回放未签收」—— 2026-10-12 后 REQ-F-1 已进入「自动化**子集**已覆盖 / 全文仍 open」，此处表述是否需要同步 | 需修改 | G8 stale（:5）；REQ-F-1「14 条未签收」4 处 stale（:79/:117/:234/:266）；e2e 0 条（:263） |
| 3 | [`ne-datasheet.md`](../product/ne-datasheet.md) | **容量取值是否已填** —— O1 取值仍未裁，本次只落了「内部工程目标下限基线」，**对外容量取值应仍为空** | 需修改 | 容量纪律合规（无 1280 数值）；命名 + O4/D5/O5/D3/e2e 共 10 处 stale（:11/:26/:40/:234/:302/:356-359/:367/:382） |
| 4 | [`responsibility-matrix.md`](../product/responsibility-matrix.md) | 与产品定位（部署在运营商网络之外、单租户 on-prem）是否一致 | 需修改 | 产品定位一致性合规；命名 + e2e 2 处 + O4/D5/O5/D3 5 处 stale（:5/:11/:167/:192-194/:198/:213） |
| 5 | [`security-privacy.md`](../product/security-privacy.md) | 2026-10-11 已按 O4 / D5 裁决**追加同步**；但 §4.1 记录的「chart **无备份 Job**」这一事实**未变**，备份恢复方案因此仍未闭合 | 需修改 | O4/D5/O5 已同步且无完成时表述、chart 无备份 Job 事实未变（合规）；残留 :289 状态纪律行 + :5 正文 stale |
| 6 | [`version-lifecycle.md`](../product/version-lifecycle.md) | §7「API 版本兼容策略」是以「**候选、未决策**」形式列出的，**无 ADR** —— 与 Lane D 的 **4.3** 是同一件事 | 需修改 | §7 与 Lane D 4.3 表述正确、§3 纯转述 ADR-0027（合规）；命名 3 处 stale；:118「无自动化」stale（sync-chart-version.sh 已落地） |

### 3.2 `docs/operations/`（7 份）

| # | 文件 | 已知需重点核对的点 | 结论 | 备注 |
|---|---|---|---|---|
| 7 | [`README.md`](../operations/README.md) | 导航是否覆盖全部 8 份文档 + 看板 | 需修改 | :25 O4/O5/D3/D5 列未决 stale；:80 e2e=0；§1 分层表缺 4 层致 alert-response-matrix:6 定位落空 |
| 8 | [`runbook-l1.md`](../operations/runbook-l1.md) | 一线处置步骤与实际告警规则集（`deploy/alerts/` 3 组 10 条）是否对得上 | 需修改 | :29 引用错误（7.2d 出处应为 plan §3.2/交付物 2.4 行）；:47/:194 O5/D3 未决 stale；:7 e2e=0 |
| 9 | [`runbook-l2.md`](../operations/runbook-l2.md) | 二线步骤；是否引用了尚未实现的能力（如轨迹查询、Redis Sentinel） | 需修改 | 未发现把未实现能力写成可执行步骤（合规）；:21 O4/D5 未决、:98/:180 O5/D3 未决 stale；:5 e2e=0 |
| 10 | [`alert-response-matrix.md`](../operations/alert-response-matrix.md) | 是否与 `deploy/alerts/as-alerts.yaml` 的 3 组 10 条规则逐条对应 | 需修改 | :68「查 Sentinel/failover 状态」在单副本 chart 下不可执行；O5/D3 未决 stale；4 处 e2e=0；promtool 2026-10-11 通过结果未留痕 |
| 11 | [`fault-demarcation.md`](../operations/fault-demarcation.md) | 与 `responsibility-matrix.md` 的边界口径是否一致 | 需修改 | 与 responsibility-matrix 边界口径一致（合规）；:38/:117/:298/:299 O4/D5/O5/D3 stale；:15 e2e=0 |
| 12 | [`rollback-playbook.md`](../operations/rollback-playbook.md) | 回滚步骤是否依赖 chart 版本一致性 —— A6 已裁「自动同步」但**当前仍未同步** | 需修改 | 未声称已演练（合规）；全篇 0 处提及 VERSION/Chart.yaml/kubeVersion，L3 回滚缺版本映射；:126/:162 O5/D3 stale |
| 13 | [`backup-restore.md`](../operations/backup-restore.md) | 2026-10-11 已按 O5 / D3 裁决**追加同步**；但 **RPO / RTO 数值仍未裁**，且 D5（in-cluster PostgreSQL）**实现未落** | 需修改 | RPO/RTO 未给数值、D5 实现未落如实（合规）；:166 注记被写成单列表格行打断 §7 表格；:27/:150/:162-164 主单元格仍写待裁决；:164 与 :166 自相矛盾 |

### 3.3 `docs/delivery/`（3 份）

| # | 文件 | 已知需重点核对的点 | 结论 | 备注 |
|---|---|---|---|---|
| 14 | [`README.md`](../delivery/README.md) | 导航是否覆盖 3 份文档 + 脚本 | 需修改 | 导航无死链（合规）；L82「人工核对 VERSION/Chart」stale（应引 sync-chart-version.sh --check）；交付清单缺 deploy/alerts/（G9-a 四类只落三类） |
| 15 | [`install-guide.md`](../delivery/install-guide.md) | §2 交付清单与 `:19` / `:91` 是「交付边界判定线」的既有落地；安装步骤是否依赖 chart 版本（`kubeVersion` 已定为 `>=1.23.0-0`，**尚未写入 Chart.yaml**） | 需修改 | §2 缺告警规则；:39 chart 包名不实（当前 0.0.0-skeleton.tgz）；§5 fail-closed 文案漏 deployment.yaml 同义文案且未提示 allowEmptyAllowlistForTest 生产须 false；:195 人工核对 stale |
| 16 | [`airgap-package.md`](../delivery/airgap-package.md) | 离线包步骤与 `scripts/bundle-images.sh` / `load-images.sh` / `images.txt` 是否一致 | 需修改 | §5/§6 所教 digest 写法会被 bundle-images.sh:205 拒绝（文档与脚本相悖）；产物命名未如实；L191「未落盘时」括注过期；§2 缺告警规则交付路径 |

---

## 4. 三条评审时最容易漏的边界

1. **「已裁决」不等于「已实现」。** O4（10 天保留）/ D5（in-cluster PG）/ O5（N+1+跨站 1+1）/ D3（Redis Sentinel）
   都只裁了**取值**；轨迹存储查询删除、Redis Sentinel **均未实现**。
   凡文档中出现「系统按 10 天清理」「Sentinel 自动切换」一类**完成时**表述，都属需修改项。
2. **本机真栈绿不等于对外容量。** 2026-10-12 的饱和点探测（CPS 1280 无失败）是
   **本机 loopback 模型下的下限基线**，不是容量目标值，也不是承诺值；
   `ne-datasheet.md` 的容量取值**不得**据此填写。
3. **`promtool` 通过不等于告警可用。** 语法校验已过（3 组 10 条），但**抓取接线 X1 未闭合**；
   涉及「告警能收到」的表述都需留意。

---

## 5. 评审完成后的回写（维护者或按其指示执行）

- [x] 16 份逐份填结论（accept / 需修改 / 驳回）与备注 —— **2026-10-12 完成**：结论见 §3，需修改项明细见 §6
- [ ] 需修改项闭环后复评，并在本文件**追加**复评结果（原文不改） —— **未执行（2026-10-12）**：需修改项均未闭环，复评待闭环后进行
- [x] 需修改项闭环后复评，并在本文件追加复评结果（原文不改） —— **2026-10-12 执行（本行为追加；上一行的「未执行」为闭环前状态，保留为审计链）**：16 份复评结论见 §7（accept 16 / 需修改 0 / 驳回 0，待维护者确认）；附带资产中看板 README 与三个交付脚本由「需修改」转 accept。
- [x] `docs/product-packaging-plan.md` §5 的批次状态按评审结果更新 —— **2026-10-12 完成**
- [x] 评审结论同步回 [`../handoff/2026-10-10-unfinished-assessment-and-next-plan.md`](../handoff/2026-10-10-unfinished-assessment-and-next-plan.md) §4 **B6** 的出口判据 —— **2026-10-12 完成**

---

**落盘日期：2026-10-12。状态：清单已建，评审结论待维护者填写。**
（本文件不评审、不签收任何文档，不代替维护者判断，不构成对外交付或验收依据。）
**2026-10-12 追加（上方落款为清单建立时原文，保留为审计链）：评审已执行，结论见 §3 与 §6；16 份全部「需修改」（accept 0 / 驳回 0），待维护者确认。**
**2026-10-12 再追加（上方各行为闭环前状态，保留为审计链）**：需修改项已闭环并复评，结论见 §7（accept 16 / 需修改 0 / 驳回 0，待维护者确认）。

---

## 6. 评审记录（2026-10-12）

> **性质**：本节是 B6 第一项出口判据（「16 份逐份评审，结论留 review record」）的落地记录。
> **不签收任何 REQ、不签收任何里程碑、不构成对外交付或验收通过**；结论由 agent 填写，**待维护者确认**。
> 评审方式：三个只读评审代理分批评审（product / operations / delivery）+ 主 agent 抽查复核 4 条关键证据。

### 6.1 汇总

| 批次 | 份数 | accept | 需修改 | 驳回 |
|---|---|---|---|---|
| `docs/product/` | 6 | 0 | 6 | 0 |
| `docs/operations/` | 7 | 0 | 7 | 0 |
| `docs/delivery/` | 3 | 0 | 3 | 0 |
| **合计** | **16** | **0** | **16** | **0** |

**附带资产（不计入 16 份）**：`grafana-dashboards/overview.json`、`sip-signaling.json`、`scripts/images.txt` = **accept**；
`grafana-dashboards/README.md`、`preflight.sh`、`scripts/bundle-images.sh`、`scripts/load-images.sh` = **需修改**（明细见 6.4）。

### 6.2 逐份需修改项明细

（每份列要点与行号；「合规点」是该份已核实无问题的部分，一并记录以免复评时重复劳动。）

#### docs/product/

1. **one-pager.md**：① `:7` 目标场景 stale —— 仍写「xx运营商 内部上线评审 / 当前默认方向 / 尚未形成正式决策落点」，应为已裁口径「xx运营商 内部生产就绪/发版评审」（G8-1）；② `:5` 命名 stale ——「文档暂用名 / 不是已正式批准的产品名」已被 G8-2 推翻（描述名正式采用，非商标/品牌宣称）；③ `:6`「repo 名拟改为」stale（G8-3 记为已完成）；④ `:168`「e2e marker 为 0」stale（实际 8 条稳定通过）；⑤ `:170` O4「未决」stale（已裁默认 10 天、部署可配；实现未落）；⑥ `:171` D5「未决」stale（已裁 in-cluster PostgreSQL）；⑦ `:172` O5「未决」且仍列「N+1 单节点 / N+M 机架或 AZ」选项 stale（已裁站点内 N+1 + 跨站 1+1；未裁项仅剩 RPO/RTO 数值）。合规点：`:10/:34/:142/:169` 关于 O1 未裁、不写容量数字的表述与现状一致。
2. **compliance-matrix.md**：① `:5` 命名 stale（同 1②③）；② `:79`/`:117`/`:234`/`:266`「14 条全文回放未签收」stale —— REQ-F-1 现为「自动化子集已覆盖 / 全文仍 open」（Wave2 归一化对拍覆盖 S1 双腿骨架、C_in≠C_out、SDP 逐字节恒等；14 条逐条 header 对拍未做）；③ `:263`「e2e 0 条」stale。合规点：`:12`/`:13`/`:35`/`:187`/`:220-222` 的 open 标注与证据等级纪律如实。
3. **ne-datasheet.md**：容量纪律**完全合规** —— 全篇无 CPS/BHCA/CAPS 数值，§3 只给模型结构与测量方法学，§3.6 填值准入三前置状态标注准确，未把 2026-10-12 CPS 1280 下限基线写成容量值。需修改：① `:1`/`:5` 命名 stale；② `:11`/`:382`「O1/O4/O5/D3/D5 未决」stale；③ `:26`/`:367`「e2e=0」stale；④ `:40`/`:234`/`:270-271`/`:274`/`:297`/`:302`/`:358`/`:359` O5/D3「未决」且 `:302` 仍列「机架/AZ」待选 stale；⑤ `:356`/`:357` O4/D5「未决」stale。合规点：版本不同步（`:23`/`:314`/`:340`）、X1 抓取缺口（`:216`/`:300`/`:328`/`:364`）、告警 3 组 10 条对应均如实；「chart 无备份 Job」事实未变。
4. **responsibility-matrix.md**：产品定位一致性**完全合规**（单租户 on-prem、部署在运营商网络之外、S-CSCF 经 S-SBC 触发，与 ADR-0003/G-P0-5 一致）。需修改：① `:5` 命名 stale；② `:11`/`:198`「e2e=0」stale；③ `:167`/`:192`/`:193`/`:194`/`:213` O4/D5/O5/D3「未决」stale，其中 `:194` 与 `:168`（ADR-0008 N+1 + 1+1 温备）自相矛盾。
5. **security-privacy.md**：O4/D5/O5 同步质量最好（9 处追加式注记，无任何「系统按 10 天清理」完成时表述；「chart 无备份 Job」事实未变且已实证）。需修改：① `:289` 状态纪律总结行 stale 且无注记覆盖（「e2e marker 为 0；O1/O4/O5/D1/D3/D5 未决」）；② `:5` 正文命名 stale（`:6` 注记已覆盖，建议正文改写、注记保留为审计链）；③ `:259-260` 正文与注记并存易误读，建议同步。
6. **version-lifecycle.md**：§7「API 版本兼容策略 = 候选、未决策、无 ADR」与 Lane D 4.3 为同一件事且出口条件完整（合规）；§3 逐条转述 ADR-0027 不新增承诺（合规）。需修改：① `:5`/`:6`/`:231` 命名 stale；② `:118`「版本 bump 无自动化」stale —— `scripts/sync-chart-version.sh` 已于 2026-10-12 落地（默认 `--check` 只读、drift exit 1；`--apply` 未执行，G4「当前不修改」继续有效）；③ `:79`/`:241` 的「建议修法」应升级为「已裁自动同步、脚本就绪、首次执行时机待维护者决定」。

#### docs/operations/

7. **README.md**：导航覆盖 7 份 + 看板且链接有效（合规）。需修改：① `:25` 仍把 O4/O5/D3/D5 列为「未决项」；② `:80`「e2e = 0」stale；③ §1 分层表只有 L1/L2 两行，`alert-response-matrix.md:6` 自称的「L1/L2 之上层」位置在 README 中不存在（跨文档断链）。
8. **runbook-l1.md**：告警 10 条逐条对应、X1 抓取缺口未被掩盖、可触发性判断准确（合规）。需修改：① `:29` 引用错误 ——「M4b-7.2d / M8 7.2d blocked」的出处标为 `product-packaging-plan.md` §0.3 第 1、3 条，但该两条分别是「M8 退出签字搁置」「运营商 PKI 无 lab 证据」，7.2d 的真实出处是 §3.2 与交付物 2.4 行；② `:47`/`:194`「Redis HA 仍是未决项 O5/D3」stale；③ `:7`「e2e marker = 0」stale。
9. **runbook-l2.md**：未发现把未实现能力（轨迹查询、Sentinel 切换）写成可执行步骤（合规）；`:202` 主动标注原件引用无法解析（良好自查）。需修改：① `:21`「O4/D5 未裁决」stale；② `:98`/`:180`「Sentinel 拓扑 / Redis HA 属未决 O5/D3」stale（应改为取值已裁、chart 仍单副本、failover 实测行为无证据）；③ `:5`「e2e marker = 0」stale。
10. **alert-response-matrix.md**：与 as-alerts.yaml 3 组 10 条逐条对应、与 ne-datasheet §6 一致（合规）。需修改：① `:68` 首查动作第 3 步「查 Sentinel/failover 状态」在单副本 chart 下无对象可查（不可执行步骤）；② `:192` 及 `:68` 证据列「O5/D3 未决」stale；③ `:10`/`:14`/`:109`/`:189` 共 4 处「e2e=0」stale；④ `promtool check rules` 2026-10-11 通过（10 rules found）的结果未在本文留痕；⑤ `:6` 位置描述与 README §1 断链（同 7③）。
11. **fault-demarcation.md**：与 responsibility-matrix 的归属/抓包责任口径逐行一致（合规）。需修改：① `:38` 第⑤项「O4/D5 未裁决」stale；② `:117`/`:298`「O5/D3 未决」stale；③ `:299`「O4/D5 待裁决」stale；④ `:15`「e2e marker = 0」stale。
12. **rollback-playbook.md**：未声称做过真实集群演练（`:115`/`:134`/`:157` 均如实标注）（合规）。需修改：① **全篇（乃至全目录）0 处提及 VERSION/Chart.yaml/appVersion/kubeVersion** —— L3 `helm rollback <revision>` 缺「revision → 产品版本」映射前置，§5 演练记录模板无法回填产品版本，回退证据链对外不可验证；② `:126`/`:162`「O5/D3 未决」stale。
13. **backup-restore.md**：RPO/RTO 不单方面给数值、D5 实现未落、无「按 10 天清理」完成时表述（合规）；是 operations 批唯一被 2026-10-11 任务 E 覆盖的一份。需修改：① `:166` 的追加注记被写成单列表格行，插在 §7 四列表格中间，渲染后列数不匹配；② `:27`/`:150`/`:162`/`:163`/`:164` 主单元格仍写「待裁决/未决」（有注记覆盖但读者先读到过期结论）；③ `:164`「只能写待裁决」与 `:166` 注记自相矛盾。

#### docs/delivery/

14. **README.md**：导航覆盖 3 份 + 4 个脚本资产、无死链、三步流程表与 preflight.sh 12 个检查段对应（合规）。需修改：① L82（及 §5 第 4 行）「VERSION/Chart 不同步 → 打包时人工核对」stale，应改为「跑 `scripts/sync-chart-version.sh --check`（只读，drift 即 exit 1）；`--apply` 留待维护者首次同步」；② §2/§3 交付清单未列入 `deploy/alerts/` 告警规则 —— G9-a 定义的四类交付产品只落地三类。
15. **install-guide.md**：§2 判定线落地（`:19`/`:91`）、命令序列与 runbook 逐字一致（合规）。需修改：① §2 交付清单缺告警规则行；② `:39`「`3rdparty-as-<version>.tgz`」不实 —— `helm package` 按 Chart.yaml name/version 命名，当前产物实为 `3rdparty-as-0.0.0-skeleton.tgz`（与 VERSION 0.2.0 未同步）；③ §5 fail-closed 文案只引 `validate-install.yaml:6/9/12`，漏 `deployment.yaml:12/15` 同义文案（2026-10-11 chart-check 工件实证一次 lint 输出 4 条 Fail），且未提示 `sip.allowEmptyAllowlistForTest`（values.yaml:165）生产必须为 false；④ `:195`「人工核对三者」stale（同 14①）；⑤（建议）`:148`「已绿」为裸状态句，应补 (结论, 证据文件, 日期) 三元组。
16. **airgap-package.md**：与 bundle/load 脚本的步骤、产物、退出码逐项对应，无第二套安装形态（合规）。需修改：① **§5/§6 与 images.txt 所教的 digest 固定写法（`repository:tag@sha256:...`）会被 `bundle-images.sh:205` 的格式校验拒绝**（该校验 glob 写反，任何 digest 条目必中 `die`）——文档与脚本相悖，属对外交付硬伤；② §3 产物命名未如实（tgz 按 Chart.yaml 命名当前为 `0.0.0-skeleton`；未传 `--platform` 时 tar 后缀为 `unspecified`）；③ L191「install-guide.md 未落盘时」括注过期（已落盘）；④ §2 缺告警规则交付路径说明。

### 6.3 跨文件共性问题（建议单独立项，本评审不执行修改）

1. **「任务 E」同步覆盖缺口**：2026-10-11 的下游文档同步（register §2 P3）只覆盖 `product/security-privacy.md` 与 `operations/backup-restore.md`；其余 14 份 .md 仍写「O4/O5/D3/D5 未决」。本批 16 份中 15 份的 stale 直接源于此。建议按同一纪律补同步后复评。
2. **e2e 口径过期**：全批 9+ 处「e2e marker = 0」；实际已有 8 条稳定通过。根源在 `docs/acceptance/test-plan.md` marker 表未同步（其 REQ-F-1 段已更新）。建议先修该表再回填各册。
3. **chart 版本一致性缺位**：VERSION 0.2.0 与 Chart.yaml 0.0.0-skeleton 未同步、kubeVersion 未写入 —— 直接影响 rollback-playbook L3 可执行性、install-guide/airgap 产物命名、version-lifecycle 的「无自动化」表述。`scripts/sync-chart-version.sh` 已就绪，首次 `--apply` 时机待维护者决定。
4. **交付清单缺告警规则**：delivery 三份 + README 均未按 G9-a 列入 `deploy/alerts/`（promtool 已验 3 组 10 条；X1 抓取接线未闭合需向客户说明）。
5. **附带资产功能缺陷**：`bundle-images.sh:205` digest 校验写反；`load-images.sh` `--values` 承诺推断 Secret 名未实现（仅存在性检查）；`preflight.sh:509-510` 外部 Redis/Sentinel 部署误报「运行态状态存储不可用」（--strict 下阻断安装；Sentinel 时 REDIS_URL 本就不该出现）；`preflight.sh:34` 注释坏字节。另：`load-images.sh:146/196` 用 mapfile、preflight 用 bash 4.4 数组展开，三脚本未声明 bash 版本底线。

### 6.4 附带资产结论明细

| 资产 | 结论 | 要点 |
|---|---|---|
| `grafana-dashboards/overview.json` | accept | 15 面板与 README 声明一致；指标名全部命中 `platform/src/as_platform/telemetry/metrics.py:34-39`；无容量数字、无 Sh 面板、description 已声明抓取未闭合 |
| `grafana-dashboards/sip-signaling.json` | accept | 7 面板；同上；label 使用合规 |
| `grafana-dashboards/README.md` | 需修改 | `:46` 面板 5 描述与 JSON 两个独立 target 不一致；`:141`「O5/D3 未决」stale；`:9`「e2e=0」stale |
| `delivery/preflight.sh` | 需修改 | `:509-510` 外部 Redis/Sentinel 误报 WARN（--strict 阻断）；bash≥4.4 底线未声明；`:34` 坏字节。检查项与 chart/values 对应关系总体正确 |
| `delivery/scripts/bundle-images.sh` | 需修改 | `:205` digest 校验 glob 写反；`:95` `--destination` 为 usage 未文档化的孤儿选项 |
| `delivery/scripts/load-images.sh` | 需修改 | `--values` 帮助文本承诺「推断必需 Secret 名」但仅做存在性检查；其余行为与文档一致 |
| `delivery/scripts/images.txt` | accept | 与 values.yaml 默认镜像逐条一致；tag 留空回落 appVersion（当前 0.0.0）已如实说明；digest 先例待脚本修复后可用 |

### 6.5 复评与闭环

- 16 份需修改项**均未闭环**，复评**未执行**；闭环后须在本文件**追加**复评结果（原文不改）。
- 修改动作本身**未获授权执行**：本评审只填结论，不改动 16 份文档与附带资产的任何字节。
- 维护者确认本评审结论后，B6 出口判据第 2 项（需修改项闭环后复评）方可推进。

**（本文件 §6 不评审、不签收任何文档之外的既有结论，不构成对外交付或验收依据。）**

---

## 7. 复评（2026-10-12；需修改项闭环后执行）

> **性质**：本节是 B6 出口判据第 2 项（「需修改项闭环后复评」）的落地记录，落实 §6.5「闭环后须在本文件**追加**复评结果（原文不改）」的约定 —— **§1–§6 原文一律未改**。
>
> **复评范围**：§6.2 逐份列出的 16 份「需修改」项 + §6.3 五条跨文件共性问题 + §6.4 附带资产结论。
>
> **复评方式**：三个可写 subagent 分批评审-闭环（product / operations / delivery）+ 主 agent 以 `git status` / `git diff` 逐批核对改动面，并抽查关键实证（`bash -n` 三脚本全过；`bundle-images.sh --dry-run` 四条目实证：合法 digest / 缺 tag / 非 sha256 / 纯 tag 分别 exit 0 / 1 / 1 / 0；stale 残留全批扫描）后复评填写。
>
> **边界（与 §6 相同）**：本节不签收任何 REQ、不签收任何里程碑、不构成对外交付或验收通过；全部结论**待维护者确认**。

### 7.1 汇总

| 批次 | 份数 | 闭环前结论（§6） | 闭环后复评结论 | 说明 |
|---|---|---|---|---|
| `docs/product/` | 6 | 需修改 6 | **accept 6**（待维护者确认） | 需修改项全部闭环 |
| `docs/operations/` | 7 | 需修改 7 | **accept 7**（待维护者确认） | 需修改项全部闭环 |
| `docs/delivery/` | 3 | 需修改 3 | **accept 3**（待维护者确认） | 需修改项全部闭环 |
| **合计** | **16** | **需修改 16** | **accept 16**（待维护者确认） | accept 16 / 需修改 0 / 驳回 0 |

**附带资产复评**：`grafana-dashboards/README.md`、`delivery/preflight.sh`、`delivery/scripts/bundle-images.sh`、`delivery/scripts/load-images.sh` 由「需修改」转为 **accept（待维护者确认）**；`grafana-dashboards/overview.json`、`sip-signaling.json`、`scripts/images.txt` 维持 **accept**（本轮未改动；`images.txt` 备注中「digest 先例待脚本修复后可用」一项已随 `bundle-images.sh:205` 修复而消解）。

### 7.2 逐份复评（对应 §6.2 各条）

| # | 文件 | 需修改项闭环情况（对应 §6.2 第 N 条） | 复评结论 |
|---|---|---|---|
| 1 | `one-pager.md` | ① `:7` 目标场景 → G8-1 正式口径（xx运营商 内部生产就绪 / 发版评审）；② `:5` 命名 → G8-2 描述名正式采用；③ `:6` repo 名 → G8-3 报告已完成；④ `:168` e2e → 8 条稳定通过 + REQ-F-1「自动化子集已覆盖 / 全文仍 open」；⑤⑥⑦ `:170-172` O4 / D5 / O5 → G6 / G7 已裁口径（删「N+M 机架或 AZ」列举）。O1 未裁决保持不动 | accept |
| 2 | `compliance-matrix.md` | ① `:5` 命名 → G8；② `:79` / `:117` / `:234` / `:266` 四处 REQ-F-1 表述 → 「自动化子集已覆盖 / 全文仍 open」（未写成全文已签收）；③ `:263` e2e → 8 条 | accept |
| 3 | `ne-datasheet.md` | 命名 + `:11` / `:382` 术语纪律拆分（O1 仍未裁 / O4·D5 已裁 G6 / O5·D3 已裁 G7）；`:26` / `:367` e2e；`:40` / `:234` / `:270-271` / `:274` / `:297` / `:302` / `:356-359` O4/D5/O5/D3 → G6/G7（`:302` 删 N+M 列举）；`:314` / `:340` / `:327` 版本与 kubeVersion → G4/A6（脚本就绪、首次 `--apply` 待维护者、`>=1.23.0-0` 未写入）。**容量纪律仍为零数值（合规）** | accept |
| 4 | `responsibility-matrix.md` | 命名 + `:11` / `:198` e2e；`:27` / `:47`（mermaid label）O4；`:167` / `:192-194` O5/D3（`:194` 删 N+M 列举、与 `:168` ADR-0008 矛盾已消除）；`:213` 状态纪律同步。产品定位一致性仍合规 | accept |
| 5 | `security-privacy.md` | `:5` 正文命名改写（`:6` G8 注记保留为审计链）；`:10` / `:259` / `:260` / `:264` O4/D5/O5 → G6/G7 主单元格更新；`:289` 状态纪律行同步。「chart 无备份 Job」事实未变（合规）；无「系统按 10 天清理」完成时表述（合规） | accept |
| 6 | `version-lifecycle.md` | `:5` / `:6` / `:231` 命名；`:118`「版本 bump 无自动化」→ `scripts/sync-chart-version.sh` 已落地（默认 `--check` 只读、drift exit 1；`--apply` 未执行，G4 继续有效）；`:79` / `:241`「建议修法」→ 已裁自动同步 + 脚本就绪 + 首次执行时机待维护者。§7 与 Lane D 4.3 表述、§3 纯转述 ADR-0027 仍合规 | accept |
| 7 | `operations/README.md` | `:25` 未决项列举同步（O1 仍未裁 / O4·O5·D3·D5 已裁）；`:80` e2e；§1 分层表补「跨层参考（L1 / L2 之上层）」行（`alert-response-matrix:6` 断链已修）；`:86` 命名纪律 | accept |
| 8 | `runbook-l1.md` | `:29` 引用错误已修（7.2d 出处改为 `product-packaging-plan.md` §3.2 交付物 2.4 行，不再指向 §0.3 第 1、3 条）；`:47` / `:194` O5/D3；`:7` e2e。告警 10 条对应仍合规 | accept |
| 9 | `runbook-l2.md` | `:21` O4/D5；`:98` / `:180` O5/D3（「脑裂窗口幂等契约仍未实现」保留）；`:5` e2e。仍未把未实现能力写成可执行步骤（合规） | accept |
| 10 | `alert-response-matrix.md` | `:68` 「查 Sentinel / failover 状态」改为「先确认部署形态（chart 单副本无 Sentinel 可查）→ 客户侧外部 Redis 按客户工具查」两步；`:192` 及 `:68` 证据列 O5/D3；4 处 e2e（`:10` / `:14` / `:109` / `:189`）；`promtool check rules` 2026-10-11 通过结果已留痕（三元组 + 「语法通过 ≠ 抓取接线闭合」）；`:6` 与 README §1 新行对齐。3 组 10 条逐条对应仍合规 | accept |
| 11 | `fault-demarcation.md` | `:38` 第⑤项、`:117`、`:298` / `:299` O4/D5/O5/D3；`:15` e2e。与 responsibility-matrix 边界口径仍一致（合规） | accept |
| 12 | `rollback-playbook.md` | L3 已补「版本映射前置」（revision ↔ chart `version` / `appVersion` ↔ 根 `VERSION` 三者入证据链）+ 如实标注当前不同步 / `--check` / 首次 `--apply` 待维护者 / `kubeVersion` 已定未写入；§5 演练记录模板「版本 from → to」行补版本映射填写要求；`:126` / `:162` O5/D3。未声称已演练（合规） | accept（附注：chart 实际同步待维护者，见 §7.4-1） |
| 13 | `backup-restore.md` | `:166` 注记已移出 §7 表格（列数不匹配渲染事故已修，表格恢复连续四列）；`:27` / `:150` / `:162` / `:163` / `:164` 主单元格更新为已裁口径，`:164`「只能写待裁决」与注记的矛盾已消除。RPO/RTO 仍未给数值、D5 实现未落如实（合规） | accept（附注：RPO/RTO 待客户 + 维护者，见 §7.4-2） |
| 14 | `delivery/README.md` | §5 第 4 行 / L82「人工核对 VERSION/Chart」→ `scripts/sync-chart-version.sh --check`（只读、drift exit 1；`--apply` 留待维护者）；§2 目录表补 `deploy/alerts/` 告警规则行（G9-a 四类交付产品补齐）；§3 依赖服务行 O5/D3；§5 第 7 行 e2e；命名。导航无死链（合规） | accept |
| 15 | `install-guide.md` | §2 交付清单补告警规则行；`:39` 包名如实化（当前产物 `3rdparty-as-0.0.0-skeleton.tgz`）；§5 补 `deployment.yaml` 两条同义 fail 文案 + `sip.allowEmptyAllowlistForTest` 生产必须 false 提示；`:148`「已绿」补 (结论, 证据文件, 日期) 三元组；`:195` 人工核对 stale；`:18` / `:200` / `:201` O5/D3/e2e | accept |
| 16 | `airgap-package.md` | §5 / §6 所教 digest 写法与脚本相悖 → `bundle-images.sh:205` 已修且 `--dry-run` 实证接受（正文未改写，实证见 §7.3 第 5 条）；产物命名如实化（tgz 按 Chart.yaml 命名；未传 `--platform` 时 tar 后缀 `unspecified`）；L191「未落盘时」过期括注已删；§2 补告警规则行；§7 第 1 / 8 行版本与 O5/D3。与 bundle/load 脚本步骤对应仍合规 | accept |

### 7.3 跨文件共性问题复评（对应 §6.3 五条）

| # | 共性问题（§6.3） | 复评结果 |
|---|---|---|
| 1 | 「任务 E」同步覆盖缺口（其余 14 份仍写 O4/O5/D3/D5 未决） | **已闭环**：14 份 + 看板 README 的「未决」表述已按 G6 / G7 同步为已裁口径（保留「实现未落 / RPO-RTO 未裁」限定）；security-privacy 与 backup-restore 的既有追加注记保留为审计链 |
| 2 | e2e 口径过期（全批 9+ 处「e2e marker = 0」） | **已闭环**：根因 `docs/acceptance/test-plan.md` 自动化分层表 ③ 行已修（0 条 → 8 条稳定通过 + REQ-F-1 口径），16 份 + 看板 README 的全部 e2e 表述已回填 |
| 3 | chart 版本一致性缺位 | **部分闭环**：文档侧已全部同步为「G4/A6 已裁 + 脚本就绪 + 首次 `--apply` 待维护者」；rollback-playbook L3 已补 revision → chart version → 产品 VERSION 映射；install-guide / airgap 产物命名已如实化。**未闭环**：Chart.yaml 实际同步与 kubeVersion 写入（见 §7.4-1） |
| 4 | 交付清单缺告警规则（G9-a 四类只落三类） | **已闭环**：delivery 三份文档均已补入 `deploy/alerts/`（3 组 10 条 + promtool 2026-10-11 通过三元组 + X1 抓取未闭合需向客户说明） |
| 5 | 附带资产功能缺陷 | **已闭环**：`bundle-images.sh:205` digest 校验 glob 已修（并新增非 sha256 拒绝、`--destination` 文档化）；`load-images.sh` `--values` 文案改为如实（不解析、不推断）；`preflight.sh` 外部 Redis/Sentinel 误报已修（Sentinel 已配置 → PASS）、`:34` 坏字节已修；三脚本统一声明 bash ≥ 4.4 底线 |

### 7.4 复评中仍未闭环的项（不构成文档缺陷，列明依赖）

| # | 未闭环项 | 依赖 |
|---|---|---|
| 1 | 首次 `scripts/sync-chart-version.sh --apply`（Chart.yaml `version` / `appVersion` 对齐 `VERSION`）与 `kubeVersion: ">=1.23.0-0"` 写入 | 维护者决定时机与取值（G4「当前不修改 `VERSION` 与 `Chart.yaml`」继续有效） |
| 2 | RPO / RTO 数值 | 客户与维护者共同记录（backup-restore.md 按纪律留空） |
| 3 | O1 容量取值 | 维护者裁决（各文档容量章节按纪律留空） |
| 4 | X1 告警抓取接线 | 运营商 monitoring-integration 标准输入 + 维护者裁决（G3 维持待决，当前不改 chart） |
| 5 | 7.2d / 真实集群演练与 M8 退出签字 | 外部环境（外部 IOT 与真实环境采证后置的裁决继续有效） |
| 6 | 轨迹存储 / 查询 / 删除与 Redis Sentinel 的**实现** | B2 / B3 已单独留 item（`docs/handoff/2026-10-12-b2-b3-deferred-items.md`），本轮不启动 |

### 7.5 本轮改动面与边界

- **改动文件共 21 个**：`docs/acceptance/test-plan.md`（e2e 口径根因）+ `docs/product/` 6 份 + `docs/operations/` 8 份（7 份 + 看板 README）+ `docs/delivery/` 6 份（3 份文档 + 3 个脚本）。
- **未改动**：`deploy/`（含 `Chart.yaml` / `as-alerts.yaml`）、根 `VERSION`、任何产品代码与测试、`docs/plan.md` 与 handoff / reviews 既有文字、两份看板 JSON 与 `scripts/images.txt`。
- **未执行**：任何 git 写操作；`sync-chart-version.sh --apply`；任何构建 / 测试 / 容器动作。全部改动停留在工作树，commit 拆分由维护者决定。
- 复评结论**待维护者确认**；确认前本清单 §7 不构成对外交付或验收依据。

**（本文件 §7 不签收任何 REQ / 里程碑，不构成对外交付或验收依据。）**
