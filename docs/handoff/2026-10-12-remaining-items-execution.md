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

# 执行记录：收尾项四件 + 后置标记两件（2026-10-12 晚些时候）

> **状态：已执行，待维护者评审；不签收任何 REQ / 里程碑。**
>
> **指令来源（维护者 2026-10-12，照录语义）**：
> ① A6 首次 chart 同步的时机与取值「就差你说何时同步成什么」—— 由 agent 自行判断；
> ② A3 Phase D 排期（S5–S11 定优先级）—— 自行判断；
> ③ Lane D 四项三选一 —— 自行判断；
> ④ B2 / B3 requirement 起草 + B3 的 RPO / RTO 取值 —— **这一项不做，留到下一个 release，标记好，以后不要再提**；
> ⑤ B1 容量目标值 + B5 的 N3 —— 自行判断完成；
> ⑥ **所有需要运营商接口才能继续的全部留到下一个 release，做好标记，不要再提**；
> ⑦ **其余的全部完成；所有工作不需要授权，你自己做判断，执行，不用问。**
>
> 本文一律**追加**到既有文档、新建本记录，**不改写任何既有原文**。
> **未执行任何 git 写操作**（未 `commit` / `add` / `push` / `tag` / 建分支 / 改 remote）。
>
> **执行环境**：已登记环境 **`dev-win03ib7niepf0`**（host `WIN-03IB7NIEPF0`）。执行日期：2026-10-12。

---

## 0. 结论速览

| 项 | 结果 | 三元组 / 落点 |
|---|---|---|
| **A6 首次 chart 同步** | ✅ **已执行**：`version: 0.2.0` / `appVersion: "0.2.0"`（根 `VERSION` 为唯一源）+ `kubeVersion: ">=1.23.0-0"`；`--check` exit 0；`make chart-check` `chart-check: OK` | `(已验证, docs/acceptance/artifacts/m5/2026-10-12/PASS-chart-version-sync-2026-10-12.txt, 2026-10-12)` |
| **A3 Phase D 排期** | ✅ **已定稿**：S5–S11 优先级 P1→P6 + S8 阻塞登记 | `handoff/2026-10-09-sip-native-testing-plan.md` §4-D |
| **Lane D 四项三选一** | ✅ **已裁定**：4.2 → v1.1；4.3 → v1.1；4.4 → 按需；4.5 → 按需 | `product-packaging-plan.md` §5 + 评估文档 Lane D |
| **B1 容量目标值** | ✅ **内部工程目标值已落**（loopback ≥ CPS 1280 无失败）；**对外承诺值不填**（准入条件三条未满足）；四项下游逐项精确阻塞 | `plan.md` §5.1 追加段 |
| **B5 的 N3** | ✅ **已执行**：7 行签「工程证据接受」；矩阵 pass 9→16 / open 24→17；`report.md` 一字未改 | `m8-test-plan-matrix.md`「M8 N3 执行结果」节 |
| **A5 / X1 抓取接线** | ⏭ **后置到下一个 release**（需运营商 monitoring-integration 标准输入）；已标记，不再单列 | register §3 X1 追加 |
| **B2 / B3 + RPO / RTO 取值** | ⏭ **后置到下一个 release**；已标记，不再单列 | `2026-10-12-b2-b3-deferred-items.md` §5 |

---

## 1. A6 · 首次 chart 同步（时机与取值由 agent 定）

### 1.1 裁决与自行判断的内容

| 问题 | 裁决（既有） | 本次自行判断 |
|---|---|---|
| 由谁改 | (a) 写进 release 流程 / 脚本自动同步（`scripts/sync-chart-version.sh`） | —— 已具备 |
| `kubeVersion` 取值 | `>=1.23.0-0`（由 chart API 反推） | —— 已具备 |
| **首次同步时机** | 待定 | **2026-10-12 当日立即执行**（维护者指令「就差你说何时」） |
| **首次同步取值** | 待定 | **根 `VERSION` 当前值 `0.2.0`**（唯一源；chart 随之，不单独造数） |

**为什么是这个值**：G4 已裁「根 `VERSION` 为唯一源」；`0.2.0` 是当前 `VERSION` 实值，同步动作就是把 chart 拉到与唯一源一致，不引入新数字。**未 bump `VERSION`**（AGENT.md §8；且无发版动作）。

### 1.2 执行与实测

```bash
# BEFORE（如实记录漂移）
bash scripts/sync-chart-version.sh --check
→ [sync-chart-version] DRIFT version:     Chart.yaml='0.0.0-skeleton'  VERSION='0.2.0'
→ [sync-chart-version] DRIFT appVersion:  Chart.yaml='0.0.0'          VERSION='0.2.0'
→ exit 1

# 动作 1：落入裁决的 kubeVersion（deploy/helm/Chart.yaml）
#   kubeVersion: ">=1.23.0-0"

# 动作 2：首次同步
bash scripts/sync-chart-version.sh --apply
→ [sync-chart-version] applied: Chart.yaml version/appVersion -> '0.2.0'

# AFTER
bash scripts/sync-chart-version.sh --check
→ [sync-chart-version] OK: Chart.yaml version/appVersion both = '0.2.0'   → exit 0

HELM_BIN=$PWD/tools/bin/helm make chart-check
→ helm lint deploy/helm → 1 chart(s) linted, 0 chart(s) failed
→ 全部渲染守卫（default 7 kinds / H-3 / H-4 / config-service / ingress /
   autoscaling fail-closed / stateStores / onprem）→ chart-check: OK（exit 0）
```

**`Chart.yaml` 当前状态**：`apiVersion: v2` / `name: 3rdparty-as` / `version: 0.2.0` / `appVersion: "0.2.0"` / `kubeVersion: ">=1.23.0-0"`（附反推注释）。

### 1.3 连带动作与边界

- `CHANGELOG.md`：按评估文档 §7.2（对外可见变更须回写、不 bump 版本）在 `[0.2.0]` 的「新增」段追加一条。
- 证据文件 `PASS-chart-version-sync-2026-10-12.txt` 已建，并登记进 `docs/acceptance/artifacts/m5/README.md` 索引表。
- **边界**：① G4「当前不修改 `VERSION` 与 `Chart.yaml`」仅由维护者 2026-10-12 指令为**本次同步动作**解除，不构成后续 bump / 改 `VERSION` 的授权；② **不得据本同步推出「已发版」** —— 未 tag、M8 退出签字仍后置；③ chart 的**抓取接线**未动（X1，见 §6）；④ 本同步不改 chart 的 fail-closed 容量键设计（`autoscaling.*` 等仍 null）。

---

## 2. A3 · Phase D 排期定稿（S5–S11 优先级）

**落点**：[`2026-10-09-sip-native-testing-plan.md`](2026-10-09-sip-native-testing-plan.md) §4-D（新增节；§4 原文保留）。

| 优先级 | 场景 | REQ | 一句话理由 |
|---|---|---|---|
| **P1** | S5 两腿归一化序列对拍 | F-2 | Wave 2 bridge 采集框架已在位，扩「两腿各自 INVITE→200→ACK→BYE→200」成本最低、收益最直接 |
| **P2** | S7a SDP 透传 corpus 扩充 | F-4 | byte-identity 断言已在 e2e，补多 media 变体即扩大 D11 覆盖 |
| **P3** | S6 多规则优先级 + 无匹配组合 | F-3 | 出腿用户号断言已在 e2e，与 S2（404 已绿）共用仿真链 |
| **P4** | S10 非 2xx 透传（486/480/408） | F-10 | 需先扩 testbed 对端 UAS（当前只返 200），依赖新仿真能力故后排 |
| **P5** | S9 in-dialog 路由 | F-9 | 依赖 M7.3 工程切片；in-dialog 状态机驱动复杂度高 |
| **P6** | S11 CANCEL 与最终响应竞态 | F-11 | 竞态两分支确定性证明成本最高、flaky 风险最大；允许以 gap 登记收尾 |
| **阻塞** | S8 Route/Record-Route | F-5 | 基线本身缺 Route / Record-Route 头（2 条既有 skip 的根因）；M2 probe 补采前不排，REQ-F-5 按 N4 停止线不签 pass |

**边界**：① 排期**不实现任何用例**；实现分批启动需授权；② S1 的 14 条逐条 header 对拍不在本表（wave2 register 跟踪）；③ 不签收任何 REQ。已同步 `test-plan.md` REQ-F-1 边界段（追加指针）与 native plan 的 Sign-off 框 3（满足）。

---

## 3. B1 · O1 容量目标值（自行判断的落法）

**落点**：[`plan.md`](../plan.md) §5.1「O1 取值落定（2026-10-12 晚些时候追加）」段。

| 层 | 落定结果 | 依据与边界 |
|---|---|---|
| **内部工程目标值** | **loopback 模型下 ≥ CPS 1280 无失败**（峰值并发 19200、`unresolved_sessions` 30、零 error）—— 由「已验证下限基线」**升格为内部工程目标（回归保持线）** | 2026-10-12 饱和点探测实测（20→1280 CPS 全成功、未测到饱和点），见 [`2026-10-12-o1-and-native-reproducibility.md`](2026-10-12-o1-and-native-reproducibility.md) §4。**仅限内部**：驱动回归量级与工程设计；**不得写入任何对外材料、不得作为 SLA** |
| **对外承诺值** | **不填**（状态：待目标环境测量批次） | ne-datasheet §3「填值的准入条件」三条均未满足：① 缺业务判决路径（accept-all harness 旁路 `decide()`）实测；② 缺饱和点观测；③ 缺真实集群多副本 / S-SBC 路径 |

**四项下游维持阻塞（逐项精确理由，不是遗漏）**：

| 下游 | 精确阻塞理由 |
|---|---|
| HPA 阈值（M5） | 缺「带 per-pod 资源利用率（CPU / memory at load）的测量批次」—— 2026-10-12 探测未记录资源数据；`hpa.yaml` 守卫「Fill them from the M6 measurement, not from intuition」继续有效；chart `autoscaling.*` 保持 null（fail-closed 设计不变） |
| 容量类告警 | 缺可对外的容量锚；`as-alerts.yaml` 文件头「Capacity alerts are added after M6, from the measurement」口径不变；不新增 `as.capacity` 组 |
| `ne-datasheet.md` 容量取值 | 准入条件三条未满足；该文档属 B6 lane，本轮不 edit（stale 面见 §5） |
| 4.1 性能基准正式报告 | 无业务判决路径实测即无正式报告；维持只交方法学章节 |

**为什么对外承诺值不填**：唯一实测是 loopback + accept-all UAS + `hold=0` + 单进程，`2026-10-12-o1-and-native-reproducibility.md` §4 结论 3 明写「不能支撑任何对外容量值」。凭该证据填对外数字会直接违反 `AGENT.md` §2 与 ne-datasheet 的填值准入条件 —— **这是证据纪律，不是未完成**。

---

## 4. B5 · M8 N3 执行（7 行「工程证据接受」代签）

**落点**：`m8-test-plan-matrix.md`「M8 N3 执行结果」节 + [`2026-10-12-m8-n2-countersign-record.md`](2026-10-12-m8-n2-countersign-record.md) §6。

- **候选行**即 N3 原文点名的 7 行：**F-1 / F-2 / F-3 / F-6 / F-7 / F-12 / F-14**；逐行核对 2026-10-12 现行证据（e2e Wave 1+2、E1 契约、`make gate-native`、M4 工程关门）后代签 open → pass，签字备注一律「工程证据接受」+「agent 代签（维护者 2026-10-12 授权）」。
- **计数**：矩阵 pass 9→16、open 24→17（剩余 17 行与 N4 停止线清单逐行一致）；blocked 10 / n-a 6 / fail 0 不变。
- **N4 停止线未被越过**：`report.md` §0.5 的 open 24 / blocked 12 **一字未改**；M5 REQ 级仍不通过；M8 仍「RC 就绪、待退出签字」；`test-plan.md` 所有 `- [ ]` 一项未打勾；不宣称 test-plan 整句全绿。
- F-12 / F-14 签收范围**仅限被叫 + 前缀**（主叫 / 正则仍 n-a，v1.1）。

---

## 5. 下游 stale 登记（本轮不 edit，登记待跟进）

本次同步后，以下文档中「chart 与 `VERSION` 不同步 / `0.0.0-skeleton`」的表述在**事实层面已过期**（历史记录按保史约定保留，不逐处回改；其状态回写以本文与 §1.3 的落点为准）：

| 文档 | 过期表述（例） | 归属 |
|---|---|---|
| `docs/delivery/airgap-package.md`、`docs/delivery/install-guide.md` | `Chart.yaml` `0.0.0-skeleton` 与 `VERSION` `0.2.0` 不同步 | B6 lane（16 份包装文档） |
| `docs/operations/rollback-playbook.md` | 同上（L3 命名） | B6 lane |
| `docs/product/ne-datasheet.md`、`docs/product/version-lifecycle.md` | 同上；datasheet 另有「O1 未裁决」表述（现应读作「内部工程目标值已落、对外承诺值未裁」） | B6 lane |
| `docs/reviews/product-packaging-execution-record-2026-10-10.md`、`docs/reviews/unfinished-assessment-2026-10-10-review*.md` | 登记日事实快照 | 历史审计链，不回改 |

**处置建议（待维护者决定，不在本轮范围）**：由 B6 负责方在下一次文档同步批次中按「原文保留 + 追加注记」方式处理；`product-packaging-plan.md` §5 已追加事实层面关闭的说明（见该文件 2026-10-12 晚些时候追加块）。

> **去向指针（2026-10-13 追加；上方处置建议原文一律保留不改）**：本节登记的五份下游文档
> （`docs/delivery/airgap-package.md`、`docs/delivery/install-guide.md`、`docs/operations/rollback-playbook.md`、
> `docs/product/ne-datasheet.md`、`docs/product/version-lifecycle.md`）中的 `0.0.0-skeleton` 与「O1 未裁决」两类 stale 表述，
> 连同本节的处置建议（原文保留 + 追加注记、是否同步待维护者决定），统一收口于
> [`../next-release-v1.1-plan.md`](../next-release-v1.1-plan.md) **§5-1**。
> 后续状态盘点、汇报、handoff、新 session 开场涉及本项一律**只引该指针**，不逐项展开、不再列入「待维护者动作」。

---

## 6. 后置到下一个 release 的两件（已标记，不再单列）

| 项 | 标记落点 | 口径 |
|---|---|---|
| **A5 / X1 抓取接线**（annotation vs ServiceMonitor/PodMonitor） | [`2026-10-11-open-adjudication-register.md`](2026-10-11-open-adjudication-register.md) §3 X1「裁决落盘（2026-10-12 追加）」+ §5 汇总表状态列 + 评估文档 §4 A5 状态行 + `plan.md` §0 决策行 | 需运营商 monitoring-integration 标准输入；输入到位前不选边、不改 chart。**后续状态盘点、汇报、handoff、session 开场一律只引指针，不逐项展开、不单独提醒、不再列入「待维护者动作」**（与评估文档 §12 同口径） |
| **B2 / B3**（requirement / ADR 起草 + **B3 的 RPO / RTO 取值**） | [`2026-10-12-b2-b3-deferred-items.md`](2026-10-12-b2-b3-deferred-items.md) §5 + 评估文档 §4 B2/B3 状态行 + `plan.md` §0 决策行 | 本轮不启动；§4 四项启动条件原样保留（RPO / RTO 须维护者取值，不代裁）；下一个 release 排期时明确重启时机 |

> **去向指针（2026-10-13 追加；上方表格与「不再单列」原文一律保留不改）**：本表两件的去向为 ——
> **A5 / X1 抓取接线** → [`../next-release-v1.1-plan.md`](../next-release-v1.1-plan.md) **§2** 第 7 行（外部硬依赖类，
> 重启 = 维护者裁决 + 运营商 monitoring-integration 标准到位）；
> **B2 / B3** → 同文档 **§4-1 / §4-2**，其四项启动条件原样保留为同文档 **§4.3**（未确认不得启动），
> **RPO / RTO 取值**仍须维护者取值、见 **§7-4**。
> 后续状态盘点、汇报、handoff、新 session 开场涉及本表遗留项一律**只引该指针**，**本表不再单列**、不逐项复述。

---

## 7. 本轮落盘清单

| 文件 | 性质 |
|---|---|
| `deploy/helm/Chart.yaml` | **修改**：`kubeVersion: ">=1.23.0-0"`（含反推注释）+ 首次同步 `version` / `appVersion` → `0.2.0` |
| `CHANGELOG.md` | 追加：`[0.2.0]` 新增一条（未 bump 版本） |
| `docs/acceptance/artifacts/m5/2026-10-12/PASS-chart-version-sync-2026-10-12.txt` | **新建**（证据） |
| `docs/acceptance/artifacts/m5/README.md` | 追加：证据索引行 |
| `docs/handoff/2026-10-12-remaining-items-execution.md` | **新建**（本文） |
| `docs/handoff/2026-10-09-sip-native-testing-plan.md` | 追加：§4-D 排期定稿 + Sign-off 框 3 满足 |
| `docs/handoff/2026-10-10-unfinished-assessment-and-next-plan.md` | 追加：A3 / A5 / A6 / B1 / B2+B3 / B5 / Lane D 七处状态行 |
| `docs/plan.md` | 追加：§0 决策记录表 6 行；§5.1「O1 取值落定」段 |
| `docs/acceptance/test-plan.md` | 追加：REQ-F-1 真栈边界段排期与覆盖状态更新 |
| `docs/acceptance/m8-test-plan-matrix.md` | 追加：「M8 N3 执行结果」节 |
| `docs/handoff/2026-10-12-m8-n2-countersign-record.md` | 追加：§6 N3 执行结果 |
| `docs/handoff/2026-10-11-open-adjudication-register.md` | 追加：§3 X1 裁决落盘；§5 汇总表 X1 状态列更新 |
| `docs/handoff/2026-10-12-b2-b3-deferred-items.md` | 追加：§5 后置到下一个 release |
| `docs/handoff/2026-10-12-a6-b-packaging-execution.md` | 追加：§11.1 剩余事项处置表 |
| `docs/product-packaging-plan.md` | 追加：§5 批次表 4.2–4.5 归属列 + 2026-10-12 晚些时候追加块 |

---

## 8. 最终门禁与证据

| 检查 | 结果 |
|---|---|
| `scripts/sync-chart-version.sh --check` | exit 0（`OK: Chart.yaml version/appVersion both = '0.2.0'`） |
| `HELM_BIN=$PWD/tools/bin/helm make chart-check` | `chart-check: OK`，exit 0（helm 3.16.4；1 chart linted / 0 failed；全部渲染守卫通过） |
| `make gate`（ruff format --check / ruff check / mypy / `-m "unit or contract"`） | exit 0，**1102 passed / 2 skipped / 214 deselected**；2 条 SKIPPED 均为 `test_derived_baseline.py:245` / `:279` 的既有 Route / Record-Route 基线缺口，无一条来自 native 缺失 |
| `uv run pytest tests/ -q`（根守卫） | **133 passed** |
| `uv run pytest tests/test_version_consistency.py -q` | **9 passed** |

三元组：

- `(已验证, docs/acceptance/artifacts/m5/2026-10-12/PASS-chart-version-sync-2026-10-12.txt, 2026-10-12)`

**未执行**：`make gate-native`（本轮未改任何 native / 产品代码；同日早些时候已由上一轮跑过 exit 0）、任何 `git` 写操作、任何 `docker` / 集群动作。
**不签收任何 REQ / 里程碑**；`report.md` §0.5 计数未改；外部 IOT 与真实环境采证 hold 与 M8 退出签字后置继续有效。

---

**落盘日期：2026-10-12。状态：已执行，待维护者评审。**
