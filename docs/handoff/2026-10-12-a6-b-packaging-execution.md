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

# 执行记录：A6 执行口径 + B1–B6（2026-10-12）

> **状态：已执行，待维护者评审；不签收任何 REQ / 里程碑。**
> 维护者 2026-10-12 指令：① A6「由谁改」＝ **(a) 写进 release 流程 / 脚本，自动同步**；
> ② `kubeVersion` 最小值**由我反推并告知**；③ **B1–B5 执行，不需要授权，采纳建议**；
> ④ **B6 评审项目单独落盘，并告知**。
>
> 本文一律**追加**，不改写任何既有原文。
> **未执行任何 git 写操作**（无 `commit` / `add` / `push` / `tag` / 建分支 / 改 remote）——
> 注：工作区出现的 staged 状态非本轮所为，见 §8。
>
> **执行环境**：已登记环境 `dev-win03ib7niepf0`（host `WIN-03IB7NIEPF0`）。

---

## 0. 结论速览

| 项 | 结果 |
|---|---|
| **A6 · 由谁改** | ✅ 裁决 **(a) 自动同步**；实现为 `scripts/sync-chart-version.sh`（默认 `--check` 只读，`--apply` 才写）。**当前 `Chart.yaml` 仍未同步**（G4「当前不修改」继续有效） |
| **A6 · `kubeVersion`** | ✅ **最小值 = `>=1.23.0-0`**（由 chart 实际 API 反推，见 §1.2）。**尚未写入 `Chart.yaml`** |
| **B1** | ✅ 建议获采纳并落盘：**内部工程目标下限基线 = 本机 loopback 模型下 CPS 1280 无失败**；对外承诺值**不填**。**O1 取值仍未裁** |
| **B2 / B3** | ⚠️ **性质更正**：取值**已裁**（G6 / G7），本次不涉及"裁决"。等的是**是否启动实现**（需 requirement → ADR → design → review）。**RPO / RTO 数值仍未裁** |
| **B4** | ✅ **Python 3.12 spike 通过**：CPython 3.12.14 下依赖全装、native 扩展可编可加载、`make gate-native` exit 0。已**完整回滚**到 3.10 |
| **B5** | ❌ **不可代签**。N2 九项是**维护者的书面裁决动作**，本文 §5 只整理待裁清单与正本位置 |
| **B6** | ✅ 评审项目已单独落盘：[`../reviews/product-packaging-review-checklist-2026-10-12.md`](../reviews/product-packaging-review-checklist-2026-10-12.md)（16 份逐份 + 4 个通用维度 + 结论栏留空） |

---

## 1. A6 执行口径

### 1.1 「由谁改」＝ (a) 自动同步

实现：`scripts/sync-chart-version.sh`

| 模式 | 行为 |
|---|---|
| `--check`（**默认**） | 只读：比较根 `VERSION` 与 `Chart.yaml` 的 `version` / `appVersion`，有差异则打印 DRIFT 并 **exit 1** |
| `--apply` | 写入 `Chart.yaml`（仅改这两行，其余字节保留） |

**实测**：

```
bash scripts/sync-chart-version.sh --check
→ [sync-chart-version] DRIFT version:     Chart.yaml='0.0.0-skeleton'  VERSION='0.2.0'
→ [sync-chart-version] DRIFT appVersion:  Chart.yaml='0.0.0'          VERSION='0.2.0'
→ exit 1
```

**当前状态：不同步**（根 `VERSION` = `0.2.0`，`Chart.yaml` = `0.0.0-skeleton` / `appVersion: "0.0.0"`）。
脚本只提供能力，**未执行 `--apply`** —— 首次同步的时机与取值仍待维护者决定（G4「当前不修改 `VERSION` 与 `Chart.yaml`」继续有效）。

### 1.2 `kubeVersion` 最小值 = `>=1.23.0-0`（反推明细）

扫描 `deploy/helm/templates/` 实际用到的 API 与特性：

| apiVersion / 特性 | 出现的模板 | GA 于 |
|---|---|---|
| `apps/v1` | Deployment / StatefulSet | 1.9 |
| `networking.k8s.io/v1`（Ingress） | `config-service-ingress.yaml` | 1.19 |
| `policy/v1`（PodDisruptionBudget） | `pdb.yaml` | 1.21 |
| `batch/v1`（Job） | `state-migrate-job.yaml` | 1.21 |
| **`autoscaling/v2`（HPA）** | `hpa.yaml` | **1.23** |
| **`ttlSecondsAfterFinished`（Job TTL）** | `state-migrate-job.yaml` | **1.23** |

**约束最大者为 1.23**（HPA v2 与 Job TTL 均于 1.23 GA）⇒ `kubeVersion: ">=1.23.0-0"`。

已扫描确认**不存在**更高门槛的特性：`startupProbe`、`minReadySeconds`、`ephemeralContainers`、
`topologySpreadConstraints`、`seccompProfile`、`appArmorProfile` 均为 0 处命中。

**尚未写入 `Chart.yaml`** —— 写入属 chart 改动，与 G4「当前不修改 `Chart.yaml`」冲突，需维护者另行授权。

---

## 2. B1 · O1 建议获采纳并落盘

落盘位置：[`../plan.md`](../plan.md) §5.1 表下「O1 口径建议」段的**采纳与确认**子段。

| 层 | 本次落盘 |
|---|---|
| **内部工程目标** | **下限基线 = 本机 loopback 模型下 CPS 1280 无失败**（峰值并发 19200、`unresolved_sessions` 30、零 error）。定性为「**已验证下限基线**」，不是目标值、不是承诺值 |
| **对外承诺值** | **不填**，状态「待饱和点测量」 |

**边界**：B1 的**取值仍未裁决** —— `plan.md` §5.1 O1 行「维护者目标裁决仍 open」**继续成立**。
本次落的是**下限基线**，回答「设计与回归按什么量级做」，**不回答**「容量目标是多少」。
**未落任何容量取值 / HPA 阈值 / 容量类告警**；G5 裁决句继续有效。

---

## 3. B2 / B3 · 性质更正（不是"等裁决"，是"等实现授权"）

**更正我上一轮的说法**：我把 B2 / B3 归进「Lane B 六项全等你」，容易被读成"等裁决"。
实际上这两项的**取值早已裁决完毕**：

| 项 | 裁决内容 | 出处 | 真正的状态 |
|---|---|---|---|
| **B2** | O4＝默认 10 天、部署可配；D5＝in-cluster PostgreSQL | §0-A.6 **G6 / B2 + D5** | **已裁**；轨迹存储 / 查询 / 删除**实现未落** |
| **B3** | O5＝站点内 N+1 + 跨站 1+1 warm standby；D3＝Redis primary/replica + Sentinel | §0-A.6 **G7 / B3 + D3** | **已裁**；Redis Sentinel**实现未落**；**RPO / RTO 数值仍未裁** |

因此 B2 / B3 剩下的是**实现工作**，属需求级，按 `AGENT.md` §3 须走
**requirement → ADR → HLD/LLD → 契约 → 代码+测试 → 验收项 + review record**，
**不是一次"执行"指令就能开跑的**。

**我能立刻做的**：起草 requirement / ADR 草案供你确认。要的话说一声。

---

## 4. B4 · Python 3.12 spike（结论：**可行**，已回滚）

### 4.1 前置事实（先说清楚 pin 的实际规模）

`requires-python = ">=3.10,<3.11"` 共 **7 处**（不是先前文档里写的 5 处）：
`platform`、`services/config-service`、`services/console`、`apps/translation`、`apps/anti-fraud`、
`testbed/load`、`testbed/simulators`。

运行时依赖只有 5 个主流包：`fastapi>=0.115`、`httpx>=0.27`、`psycopg[binary]>=3.1`、`redis>=5.0`、`uvicorn>=0.30`。

### 4.2 依赖层（隔离 venv，未改仓库）

```
uv venv --python 3.12 /tmp/spike312/venv        → exit 0
uv pip install --python .../python fastapi httpx "psycopg[binary]" redis uvicorn → exit 0
```
装成：`psycopg 3.3.6`、`redis 8.1.0`、`uvicorn 0.54.0`、`starlette 1.7.0`、`pydantic 2.14.1` 等。**依赖层无阻塞。**

### 4.3 完整 spike（改 pin → 重锁 → 重编 native → 跑门禁）

**第一次尝试失败，原因是我命令写错，不是 3.12 的问题**（如实记录）：

```
uv sync --python 3.12        → OK，扩展编成 _resip_runtime.cpython-312-...so
make gate-native             → GATE=2（7 failed, 1092 passed）
```

失败全部集中在两个 E1 真栈契约文件，根因是 `load_resip_runtime_extension()` 返回 `None`。
**真正原因**：`make gate` 内部的 `uv run` 会重新解析解释器，此时 `--python 3.12` 已不生效，
它把环境切回了 **CPython 3.10.12**（日志：`Using CPython 3.10.12 interpreter at: /usr/bin/python3.10`），
于是 3.10 的 `EXTENSION_SUFFIXES` 找不到 `cpython-312` 的 `.so`。

**修正后（用 `UV_PYTHON=3.12` 贯穿到 `uv run`）**：

```
UV_PYTHON=3.12 uv sync                  → SYNC2=0
UV_PYTHON=3.12 make m2-platform-resip-build → EXT2=0（_resip_runtime.cpython-312-x86_64-linux-gnu.so）
UV_PYTHON=3.12 make gate-native         → GATE2=0
→ 1099 passed, 3 skipped, 214 deselected
```

3 条 skip 的构成：2 条是既有的 `test_derived_baseline.py:245` / `:279`，
另 1 条 `test_sip_recovery.py:69` 是因为**本次 spike 只编了 `_resip_runtime`**（未编 recovery / two_leg），
**不是 3.12 的问题**。

### 4.4 结论

**Python 3.12 可行**：依赖可装、native 扩展可编可加载、真栈门禁全绿。

### 4.5 已完整回滚（必读）

spike 会改动 7 处 pin、`uv.lock`、`.venv` 与 native 产物，因此**做完立即回滚**：

```
还原 7 个 pyproject.toml + uv.lock（自 /tmp/spike-backup）
uv sync（3.10）→ SYNC=0
重编三个扩展   → EXT=0（_resip_runtime.cpython-310-...so 等）
make gate-native → GATE=0，1100 passed / 2 skipped / 214 deselected
```

**当前工作树：`git diff --name-only -- '*/pyproject.toml' uv.lock` → 0 处**（完全还原），
门禁计数与 spike 前**逐字一致**。

**若要正式迁移 3.12，仍需**：requirement → ADR → review（`AGENT.md` §3），
以及把 `UV_PYTHON` / `requires-python` 的口径在 CI 里固定下来 —— **本次不落**。

---

## 5. B5 · N2 九项（**不可代签**，本节只整理材料）

**为什么不能由我执行**：B5 的出口判据是「**维护者书面裁决**」，`2026-10-10` 评估文档 §4 B5 明写
「**谁做：维护者（裁决与授权）+ agent（执行）**」。N2 的每一行都是一次**签字**，
我代签等于伪造维护者裁决。

**待裁清单**（正本与须同步处逐字录自
[`2026-10-07-m8-next-step-plan.md`](2026-10-07-m8-next-step-plan.md) §N2）：

| # | 要签署的结论 | 正本 | 须同步 |
|---|---|---|---|
| 1 | 进入 M8 的授权补记（2026-10-06 已发生） | RC 计划 §10 | — |
| 2 | B-1 最小 M5.1；B-2 维持 2026-10-04 工程关门并降级为非 REQ 验收；B-3 故事 C 保持 L1 | `m5-req-acceptance-review-2026-10-06.md` | — |
| 3 | F8 接受「字段契约已落地」；C++ JSON 回调留在 RC 后 | `m8-phase-a-f6-f8-note-2026-10-06.md` §5 | `callload-remediation-adjudication` |
| 4 | F6 接受 **documented limitation**（长连接无 dialog 终止时只靠 2048 指纹 LRU 与 4096 连接上限） | 同上 §5 | adjudication F6 行；**结论不是「已修复」** |
| 5 | D6 testbed 客户验收放 **v1.1** | `m8-environment-evidence.md` D-3 | 矩阵 `D6-testbed验收` 改 n-a；RC 计划 §10 |
| 6 | NF-3 标 **n-a** | `m8-test-plan-matrix.md` | — |
| 7 | 确认四项排除：主叫/正则、PM/AM/UM、D1、D10 极端扩展 | 矩阵对应 n-a 行 `signed_by` | D1 备注写为已接受风险，或另立迁移项 |
| 8 | M5D-1…M5D-6 **移出 v1** | `plan.md` §5 新行（**维护者写**） | M5 REQ 复评会签栏；不落这 6 行，M5 REQ 维持不通过 |
| 9 | M1 / M2 / M6 / M7 签 **工程完成** | `m1-exit-review.md` 等 | `m8-exit-review` |

**注**：N2 完成后 **M5 REQ 级仍是不通过**、M8 仍是「RC 就绪、待退出签字」（原文 §N2 末句）。

---

## 6. B6 · 评审项目已单独落盘

文件：[`../reviews/product-packaging-review-checklist-2026-10-12.md`](../reviews/product-packaging-review-checklist-2026-10-12.md)

- **16 份的计数口径已对齐**：`docs/product/` 6 份 + `docs/operations/` 7 份（含其 `README.md`）+ `docs/delivery/` 3 份（含其 `README.md`）= **16**
- 附带资产单列（2 份 Grafana JSON、看板 README、`preflight.sh`、`scripts/` 3 个文件）
- 每份都过 **4 个通用维度**：D-1 事实准确性 / D-2 与已裁决口径一致 / D-3 对外可用性 / D-4 follow-up
- **16 份逐份列出已知需重点核对的点**（如 `ne-datasheet.md` 的容量取值必须仍为空、`security-privacy.md` 的 chart 无备份 Job 事实未变、`version-lifecycle.md` §7 与 Lane D 的 4.3 是同一件事）
- **结论栏一律留空** —— 我没有评审、没有签收

---

## 7. 本轮改动的文件

| 文件 | 性质 |
|---|---|
| `scripts/sync-chart-version.sh` | **新建**（A6 自动同步，默认只读校验） |
| `docs/reviews/product-packaging-review-checklist-2026-10-12.md` | **新建**（B6 评审载体） |
| `docs/handoff/2026-10-12-a6-b-packaging-execution.md` | **新建**（本文） |
| `docs/plan.md` | 追加：§0 决策表 A6 行；§5.1「采纳与确认」段 |
| 7 个 `pyproject.toml` + `uv.lock` | **改后已完整还原，当前零 diff**（B4 spike 的临时改动） |

---

## 8. 两点如实说明

1. **未执行任何 git 写操作**。工作区若出现 staged（`M ` / `A `）状态，非本轮所为
   （本轮只做文件读写、make / uv / docker 命令），**也没有 commit / push / tag / 建分支**。
2. **B5 我没有代签**，B2 / B3 我没有开工。前者是维护者的签字动作，后者需 requirement → ADR 流程；
   把这两类说成"已执行"会制造假证据，故如实列为未完成。

---

**落盘日期：2026-10-12。状态：已执行，待维护者评审。**
不签收任何 REQ / 里程碑，不构成外部验收通过；外部 IOT 与真实环境采证 hold 继续有效。

---

## 9. 同日追加更正（2026-10-12 晚些时候；§5 / §6 / §8 原文保留，此处只追加）

### 9.1 B5 已代签 —— §5「不可代签」的表述已被维护者授权推翻

§5 写的是「B5 不可代签，本节只整理材料」。**维护者 2026-10-12 明确授权 agent 代签**，
因此该处置已变更：

- **已执行代签**，九项逐项落正本并附依据（无一项凭空签）。
- 代签总记录：[`2026-10-12-m8-n2-countersign-record.md`](2026-10-12-m8-n2-countersign-record.md)（含九项逐项落点、依据、五条不得推出的结论）。
- 同步落盘：`m8-test-plan-matrix.md`、`m8-phase-a-f6-f8-note-2026-10-06.md`、
  `m5-req-acceptance-review-2026-10-06.md`、`callload-remediation-adjudication-2026-10-05.md`、
  `m8-environment-evidence.md`、`2026-10-06-m8-release-candidate-plan.md`、
  `m8-exit-review-2026-10-06.md`，以及 `docs/plan.md` §5.2-bis（M5D-1…M5D-6 六行）与 §0 决策表。
- **各正本签字一律写「agent 代签（维护者 2026-10-12 授权）」**，不伪装成亲签。
- **N3 未执行**（「哪些 open 行可签」本身是判断，需维护者参与）；RC 计划 §10 的
  「阶段 A 完成」「M8 退出签字」两栏**未填**。

### 9.2 B6 的更正 —— 结论栏并非我填写，是并行写入

§6 与 §0 速览写「结论栏一律留空 —— 我没有评审、没有签收」。**该表述只对我建文件的那一刻为真。**

**发现的事实**：本轮工作过程中，`product-packaging-review-checklist-2026-10-12.md` 被**另一个 agent 写入**
（§3 标题改为「结论栏已于 2026-10-12 由 agent 填写」、新增 §6「评审记录」、16 份全部填「需修改」），
`docs/product-packaging-plan.md` §5 亦被改动，评估文档 §4 B6 段也被追加了对应的状态行。

**我没有做这些写入，也没有评审任何一份文档。** 因此：

- §6 中「结论栏一律留空」**仅描述我建文件时的状态**，不再描述当前状态；
- 那份评审的**结论与质量我未复核**，是否可信、是否采纳，**由维护者判断**；
- 本次如实记录，**不删除、不改写对方的写入**（保史；且非我所写）。

### 9.3 一条必须报告的流程问题

本次发现**同一工作树上有两个 writing member 同时写入**
（本 agent + 填写 B6 结论栏的另一个 agent），这违反了本项目
「一个工作树同时只能有一个 writing member」的既定约束
（该约束记录在 `.codebuddy/rules/hard-rules.md`）。本次**未造成冲突性覆盖**
（双方改动落在不同段落），但属于流程风险，特此报告，由维护者决定如何处置。

---

## 10. 本轮最终状态

| 项 | 状态 |
|---|---|
| A6 由谁改 | ✅ (a) 自动同步，脚本 `scripts/sync-chart-version.sh`（默认只读校验）；**当前仍未同步** |
| A6 `kubeVersion` | ✅ 反推得 `>=1.23.0-0`；**尚未写入 Chart.yaml** |
| B1 | ✅ 建议采纳并落盘（内部工程目标下限基线）；**O1 取值仍未裁** |
| B2 / B3 | ✅ 已单独留 item，本轮不启动（载体 `2026-10-12-b2-b3-deferred-items.md`） |
| B4 | ✅ spike 通过并**已完整回滚**；正式迁移未启动 |
| B5 | ✅ **已代签**（N2 九项），N3 未执行 |
| B6 | ⚠️ 评审项目已落盘；**结论栏由并行 agent 填写，我未复核** |

**最终门禁**：`make gate` 与 `make gate-native` 均 exit 0（**1100 passed / 2 skipped / 214 deselected**）；
`uv run pytest -m e2e -q` → **8 passed**；根守卫 `uv run pytest tests/ -q` → **131 passed**；
`uv run ruff check .` → `All checks passed!`；
`git diff --name-only -- '*/pyproject.toml' uv.lock` → **0 处**（B4 spike 已完整还原）。

---

## 11. B6 移交说明（2026-10-12 追加）

维护者 2026-10-12 明确：**B6 有其他人在做，本线不用管。**

据此，本 agent 对 B6 的后续动作**全部停止**：

- **不再评审、不再填写、不再复核** `product-packaging-review-checklist-2026-10-12.md` 的任何内容；
- §6 与 §0 速览中「结论栏一律留空」的表述**仅对我建文件那一刻为真**，此后该文件的改动
  由负责 B6 的一方自行维护，**本线不再更新相关描述**；
- §9.2 记录的「并行写入」事实保留（属流程留痕），但**不再跟进、不再报告进展**；
- 若 B6 的结论需要与 A5 / Lane D 4.3 等信息对齐，由负责方自行处理。

**本线剩余的待维护者动作**（B6 不在其列）：A3 的 Phase D 排期优先级、Lane D 四项三选一、
B2 / B3 的 requirement 起草启动（含 B3 的 RPO / RTO 取值）、A6 首次 chart 同步的时机与取值、
B1 的容量目标值、B5 的 N3。

### 11.1 上述剩余事项的处置（2026-10-12 晚些时候追加；§11 原文保留不改）

维护者 2026-10-12 指令：**A5 抓取接线（X1）与 B2 / B3（含 RPO / RTO 取值）留到下一个 release，
做好标记，以后不要再提；其余全部完成，由 agent 自行判断、执行、不用问。** 据此：

| §11 所列事项 | 处置（2026-10-12） |
|---|---|
| A6 首次 chart 同步 | ✅ **已执行** —— 时机=当日、取值=根 `VERSION` `0.2.0` + 裁决的 `kubeVersion: ">=1.23.0-0"`；`--check` exit 0、`make chart-check` `chart-check: OK`；CHANGELOG 追加（未 bump） |
| A3 Phase D 排期 | ✅ **已定稿** —— S5–S11 优先级 P1→P6 + S8 阻塞登记，落 [`2026-10-09-sip-native-testing-plan.md`](2026-10-09-sip-native-testing-plan.md) §4-D |
| Lane D 四项三选一 | ✅ **已裁定** —— 4.2 / 4.3 → **v1.1**；4.4 / 4.5 → **按需**（无一项取消） |
| B1 容量目标值 | ✅ **内部工程目标值已落**（loopback ≥ CPS 1280 无失败）；对外承诺值**不填**（ne-datasheet 准入条件三条未满足）；HPA 阈值 / 容量类告警 / datasheet 取值 / 4.1 报告四项下游**精确阻塞**（理由逐条落盘） |
| B5 的 N3 | ✅ **已执行** —— 7 行（F-1/F-2/F-3/F-6/F-7/F-12/F-14）签「工程证据接受」；矩阵 pass 9→16、open 24→17；`report.md` 一字未改 |
| B2 / B3 requirement 起草 + RPO / RTO 取值 | ⏭ **后置到下一个 release**（维护者决定；已标记于 [`2026-10-12-b2-b3-deferred-items.md`](2026-10-12-b2-b3-deferred-items.md) §5，以后不再单列） |
| A5 抓取接线（X1，§11 未列、同源） | ⏭ **后置到下一个 release**（需运营商 monitoring-integration 标准输入；已标记于 register §3 X1） |

执行记录：[`2026-10-12-remaining-items-execution.md`](2026-10-12-remaining-items-execution.md)。
**未执行任何 git 写操作**（未 commit / add / push / tag / 建分支 / 改 remote）。
