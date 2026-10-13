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

# E2E 测试计划（草案，待维护者 review）

**日期**：2026-10-09  
**状态**：计划，**未实现**。`pytest -m e2e` 当前 **0 条**。  

> **状态更正（2026-10-11 追加；上一行原文保留不改）**：**Wave 1 已落地**。
> 新建 `testbed/e2e/test_sip_first_edition.py`（A4-1 裁决：独立新文件，不动
> `testbed/simulators/tests/test_product_path.py` 的 `integration` 标记）；
> `uv run pytest -m e2e -q` 由 **0 条**变为 **5 条**，连续 3 次全绿
> （`(已验证, docs/acceptance/artifacts/m5/2026-10-11/PASS-e2e-2026-10-11.txt, 2026-10-11)`）。
> **Wave 2 及以后仍未实现**（14 条 header 对拍、控制面、kind 均未在本次范围）。
> 执行记录：[`../handoff/2026-10-11-w0-native-and-e2e-execution-record.md`](../handoff/2026-10-11-w0-native-and-e2e-execution-record.md) §7。
> **仍未签收任何 REQ**，见本文 §8。
>
> **再更正（2026-10-12 追加；上一段与本节原文一律保留不改）：Wave 2 亦已落地。**
> 维护者 2026-10-12 授权启动 A4 下一批次（Wave 2 的启动前提「Wave 1 完成后启动」已于 2026-10-11 满足）。
> 新建 `testbed/e2e/test_s1_replay_contract.py`（3 条）：入腿与出腿的**归一化**序列对拍、
> **C_in ≠ C_out**（REQ-F-2 子集）、**SDP offer 逐字节恒等**（REQ-F-4，本次纳入、未单列 follow-up）。
> `uv run pytest -m e2e -q` → **8 passed**（Wave 1 的 5 条 + Wave 2 的 3 条）；
> 缺 native 时 **8 failed / 0 skipped**。
> **仍 open**：14 条消息的**逐条 header 对拍**——Wave 2 的定义本身即归一化骨架对拍，不含该子集；
> `test-plan.md` REQ-F-1 的 `- [ ]` **一项未打勾**，状态为「自动化子集已覆盖 / 全文仍 open」。
> 执行记录 [`../handoff/2026-10-12-o1-and-native-reproducibility.md`](../handoff/2026-10-12-o1-and-native-reproducibility.md) §5；
> 回写见 [`../acceptance/2026-10-11-wave2-replay-register.md`](2026-10-11-wave2-replay-register.md) §6。
**关联**：[`test-plan.md`](test-plan.md) 自动化分层；[`../handoff/2026-10-09-sip-native-testing-plan.md`](../handoff/2026-10-09-sip-native-testing-plan.md)（harness / native 门禁）；[`../handoff/pre-m8-demo-review-plan.md`](../handoff/pre-m8-demo-review-plan.md)（kind `as-m71`）。

---

## 1. 定义（本仓库里的 e2e）

**E2E** = 一次自动化里同时满足：

1. **产品 SIP 栈**是 `_resip_runtime`（reSIProcate），不是纯 Python 拼包、也不是只解析日志。  
2. **判决走生产缝**：`decide()` / 已激活规则或等价 `RuleSet` + 出腿 hook；**禁止** `accept_all_invites`（及 `early_cancel_harness`）作为被测 AS 的默认模式。  
3. **路径跨过网元边界**：至少「呼叫源 →（仿真或真实）S-CSCF/S-SBC → AS → 对端 UAS」，并断言 **终态**（结果码、必要时出腿用户号、BYE 不挂死）。  
4. 标记 **`@pytest.mark.e2e`**，由 `make test-e2e` / 门禁层③ 收集；与 `unit` / `contract` / `integration` 分开，避免 `make gate` 被拉长。

**不是 e2e：**

| 现有东西 | 为什么不算 |
|----------|------------|
| E1 S1 `accept_all_invites` | harness：真栈但旁路 `decide()`，只覆盖 100/180/200 |
| E1 S2/S3 单 socket | 真栈 + `decide()`，但无仿真 S-SBC、无完整 14 消息、无控制台 |
| M6 `as_load` → `load_uas_runtime` | 对端是 accept-all UAS，测容量不测业务 |
| `test_derived_baseline.py` | 对契约 **文件** 做断言，不打产品进程 |
| kind demo 脚本 | 证据层；可 **复用** 步骤，但在升格为 pytest e2e 之前不算本计划「已落地」 |

---

## 2. 现状锚点（实现时复用，不重复造轮）

| 锚点 | 路径 | 已证明 |
|------|------|--------|
| 本地仿真链 + 真栈 + 规则 | `testbed/simulators/tests/test_product_path.py` | T1/T4/T5/F1/F2 结果码、翻译用户号、BYE；UDP/TCP/TLS；**integration**，短时 `as_load` |
| 双腿 / SDP | `platform/tests/test_m7_forward_two_leg_integration.py`、`test_req_f4_sdp_identity_integration.py` | FORWARD 与 SDP 身份；无完整 S-CSCF 链 |
| 契约消息 | `testbed/contracts/sip-baseline/S1-basic-call/` 等 | REQ-F-1 的 14 条 **形状**；尚未对产品栈全文回放 |
| 现场 demo | `scripts/demo-review/story-*.sh`、kind `as-m71` | 客户路径；控制台在 compose，信令在 kind |

**缺口：** 没有 `e2e` 标记；门禁层③ 无用例、不阻塞；REQ-F-1 勾选仍 open。

---

## 3. 范围（建议分波，review 时删减）

### Wave 0 — 把门禁说清楚（文档 + 标记约定）

- 本文件 + `test-plan.md` 分层表（已写）。  
- `pyproject.toml` 的 `e2e` marker 说明与实现对齐。  
- 门禁：在 **至少一条** e2e 稳定前，层③ 保持不阻塞 **或** 改为阻塞但只跑 Wave 1 的 smoke（二选一，见 §6）。

### Wave 1 — 信令 e2e（无控制台）

从 `test_product_path` **升格或拆出** `@pytest.mark.e2e`：

| ID | 场景 | 断言（最小） | 禁止 |
|----|------|----------------|------|
| E2E-SIP-1 | UDP：T1 翻译接通 | 200；出腿用户含翻译结果；BYE 计数与未决会话为 0 | `accept_all_invites` |
| E2E-SIP-2 | UDP：T4 无匹配 | 404；不出腿或不出 BYE 业务腿（与现 `test_product_path` 一致） | harness |
| E2E-SIP-3 | UDP：F2 阻止 | 603 | harness |
| E2E-SIP-4 | TCP、TLS 各一条（可参数化，与现 4 组合对齐或先各 1） | 同 T1 子集 | 测试 CA，不声称 REQ-S-2/S-3 签收 |

**完成标准：** `AS_REQUIRE_NATIVE_EXTENSIONS=1 uv run pytest -m e2e -q` 在已 `make m2-platform-resip-build` 的机器上绿；缺 `.so` 则 **fail**（与 native-contract 策略一致），不 skip。

**明确不做（Wave 1）：** 14 条逐条 header 对拍、控制台、kind、容量数字。

### Wave 2 — REQ-F-1 形状（仍无控制台）

在 Wave 1 拓扑上，对 **一通** T1：

- 采集入/出腿关键消息（方法 + 最终响应码序列，或与 `S1-basic-call` **归一化**对比）。  
- 断言 **C_in ≠ C_out**（REQ-F-2 子集）。  
- SDP offer 入腿与出腿 **逐字节**（REQ-F-4）若实现成本可接受；否则单列 follow-up。

**完成标准：** `test-plan.md` REQ-F-1 勾选改为「自动化子集已覆盖 / 全文仍 open」并链到本用例名，**不**在未对拍 14 条时打勾全文。

### Wave 3 — 控制面 + 信令（可选，重）

- compose 或 test client：规则变更 → 激活 bundle → **重启或热加载策略以仓库实际能力为准** → 再跑 E2E-SIP-1。  
- 与 demo story A 对齐；**不**把浏览器手工步骤写进第一版门禁。

### Wave 4 — kind `as-m71`（发布前证据，默认可选门禁）

- 复用 `kind-up.sh` + `publish-m71-bundle.sh` + 测试页或 `as_load` 打 **产品 Deployment**（非 `load_uas_runtime`）。  
- 标记 `e2e` + `kind`（需新 marker 或 env `AS_E2E_KIND=1`），**按需手动运行**，不进每次 PR，除非维护者要求。

**明确排除：**

- M6 容量 / O1 报告（`performance`）。  
- `accept_all` harness 作为被测 AS。  
- 运营商真 S-SBC / 客户 PKI（M8 环境证据，见 `m8-environment-evidence.md`）。

---

## 4. 与 harness / call load 的边界（写进用例 docstring）

| 被测进程 | 允许 |
|----------|------|
| E2E 里的 AS | `ResipRuntimeListener` 或产品进程壳，**`accept_all_invites=False`**，规则来自 `demo_rules()` 或 bundle |
| 负载发生器 | `as_load` 可以（它是客户端）；**对端 UAS 用 `PeerUas` / 仿真被叫**，不用 `load_uas_runtime.py` |
| 仿真 S-CSCF/S-SBC | `as_simulators` 或 kind `ims-sim`；标注「非运营商」 |

---

## 5. 建议文件布局（实现时）

```text
testbed/simulators/tests/test_product_path.py   # 可保留 integration；或改为 e2e
testbed/e2e/test_sip_first_edition.py           # Wave 1 新文件（推荐，避免 integration 语义混淆）
```

门禁（Wave 1 落地后）：

- job `e2e`：`needs: [native-contract]` 或自带 `m2-platform-resip-build`；  
- `AS_REQUIRE_NATIVE_EXTENSIONS=1 uv run pytest -m e2e -q`；  
- 去掉 `continue-on-error` **仅当** Wave 1 在 `ubuntu-latest` 稳定（OpenSSL 3 与本地缓存路径需在实现时验证）。

---

## 6. 待你 review 的决定

1. Wave 1 是否 **直接改** `test_product_path` 的 marker 为 `e2e`（少文件）还是 **新文件复制断言**（integration 仍给开发者本地快跑）？  
2. 缺 native 时 e2e 是 **fail** 还是 **skip**？（建议与 `native-contract` 一致：**fail**。）  
3. Wave 2 的 14 条对拍是 **本迭代必须** 还是 **单开 issue**？  
4. kind e2e 是否 **永不**进 PR required checks？

---

## 7. 验收（计划本身）

- [ ] 维护者确认 §1 定义与 §6 四项决定  
- [ ] Wave 1 用例进 `master` 且门禁层③ 行为与决定一致  
- [ ] `test-plan.md` REQ-F-1 勾选状态与 Wave 2 是否做完一致（未做完不打勾全文）

---

## 8. 验收三框的当前处置（2026-10-11 追加；§7 原文保留不改）

> 上文三框按保史约定**原文保留**；本节只**追加**当前处置，便于核对。

| §7 框 | 处置（2026-10-11） |
|---|---|
| ① 维护者确认 §1 定义与 §6 四项决定 | ✅ **已确认** —— 四项决定即 `docs/handoff/2026-10-10-unfinished-assessment-and-next-plan.md` §0-A.6 的 **G2 / A4-1…A4-4**，已于 2026-10-10 裁决落盘；本次即按其落地（A4-1 新建文件、A4-2 缺 native 时 fail、A4-3 Wave 2 后置到仓内载体、A4-4 仅登记政策方向**不改配置**） |
| ② Wave 1 用例进 `master` 且门禁层③ 行为与决定一致 | ⚠️ **一半** —— 用例已落地并在本机稳定通过；**进 `master` 需维护者 commit**（本次未做任何 git 写操作）。「门禁层③ 行为与决定一致」中**可本机验证的部分一致**：缺 native 时 fail 不 skip（实测 5 failed / 0 skipped）。**kind e2e 进 PR required 的门禁配置变更未做** —— A4-4 裁决明确「不构成任何配置变更授权」 |
| ③ `test-plan.md` REQ-F-1 勾选状态与 Wave 2 是否做完一致 | ❌ **未做** —— Wave 2 的 14 条对拍未实现，载体为 [`2026-10-11-wave2-replay-register.md`](2026-10-11-wave2-replay-register.md)。**REQ-F-1 的 14 条全文仍 open，本次不勾选、不签收** |

**§8 表格第 ③ 框的更新（2026-10-12 追加；上方表格原文保留不改）**：

| §7 框 | 更新后处置（2026-10-12） |
|---|---|
| ③ `test-plan.md` REQ-F-1 勾选状态与 Wave 2 是否做完一致 | **已按完成标准落盘** —— Wave 2 已实现（`testbed/e2e/test_s1_replay_contract.py`，3 条），状态改为「**自动化子集已覆盖 / 全文仍 open**」并链到用例名（`test-plan.md` REQ-F-1 段）。**14 条逐条 header 对拍仍 open，`test-plan.md` 的所有 `- [ ]` 一项未打勾** —— 这与完成标准「未对拍 14 条时不得打勾全文」一致 |

**本次的边界（避免据「Wave 1 已落地」推出过度结论）**：

- 落地的 4 个用例（E2E-SIP-1…4）覆盖的是**终态结果码 + 出腿翻译结果 + BYE 不挂死**，
  **不含** 14 条消息的逐条 header 对拍、**不含**控制面、**不含** kind、**不含**任何容量数字。
- 被测路径中的 S-CSCF / S-SBC 均为**仿真**（`as_simulators`），TLS 用**测试 CA**；
  按本文 §3「明确排除」条，**不签收 REQ-S-2 / REQ-S-3**。
- 真栈绿属**工程门禁层**证据；`docs/acceptance/report.md` §0.5 的 open 24 / blocked 12 **未改**。
