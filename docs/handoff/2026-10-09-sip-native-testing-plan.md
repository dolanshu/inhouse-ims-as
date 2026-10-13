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

# Handoff — SIP native testing gate补齐计划 (2026-10-09)

> **Purpose:** 下一 session 执行：真栈（`_resip_runtime`）测试分层、门禁守门、E1/S1 harness 修复。  
> **Not:** 本文件本身不签收 REQ / 里程碑；维护者 commit / push 自行完成。  
> **Prerequisite:** `cur` 分支已删除（内容在 `master` `c2d56e4` 及之后）；`callload` 已删。

---

## 0. 现状摘要（为何要做）

| 事实 | 说明 |
|------|------|
| 产品 SIP | C++ **reSIProcate** → Python 模块 **`_resip_runtime`**（`make m2-platform-resip-build`） |
| `make gate` | `pytest -m "unit or contract"` ≈1012 条；**绝大多数不经过真栈** |
| E1 真栈烟测 | `test_e1_contract_resip_runtime*.py` 共 **7** 条（有 `.so` 才跑；无则 **skip**） |
| `make gate`（① 层） | **不**编 native → E1 **全 skip**，提交门禁**未验** UDP/TLS 产品栈 |
| 本机有 `.so` 时 | **2 failed**：S1 + `accept_all_invites` + SDP → 期望 **200**，实际 **400**（harness 应答 SDP / `minimalHarnessAnswer`） |
| 原则 | **凡 SIP flow 行为验收，应走真栈**；7 条 smoke **不够**（见 `docs/acceptance/test-plan.md` REQ-F-*） |

**失败用例（先修）：**

- `platform/tests/test_e1_contract_resip_runtime.py::test_e1_s1_accept_all_harness_returns_200`
- `platform/tests/test_e1_contract_resip_runtime_full.py::test_e1_s1_accept_all_from_contract_invite`

**根因（已定位）：** `platform/native/resip_runtime/runtime_module.cxx` 中 `acceptHarnessSession` / `minimalHarnessAnswer` 生成的应答 SDP 在 `provideAnswer` → `accept(200)` 时被 reSIProcate 拒绝（Parse 失败或 “Can't provide an answer”）。**不是** ims-sim 模拟器问题。

**同路径集成测（修好后应一并绿）：**

- `platform/tests/test_resip_runtime_integration.py::test_accept_all_invites_harness_mode_returns_200`（`integration` 标记，不在默认 gate）

---

## 1. Phase A — 修复 S1 harness（下一 session 第一步）

### A.1 调查

1. 读 `runtime_module.cxx`：`minimalHarnessAnswer`、`acceptHarnessSession`、`onOffer` / `onOfferRequired`。
2. 对比 reSIProcate 对 `SdpContents` / `HeaderFieldValue` 的构造方式（是否需 `\n` vs `\r\n`、是否应 `session->provideAnswer` 用 offer 派生而非手写）。
3. 本地复现：

```bash
make m2-platform-resip-build
uv run pytest platform/tests/test_e1_contract_resip_runtime.py::test_e1_s1_accept_all_harness_returns_200 -vv
# 或打印 400 body（见会话记录：ParseBuffer expected 'v'）
```

### A.2 实现

- 修 C++ harness 应答生成，使带 SDP 的 INVITE 在 `accept_all_invites=True` 下稳定 **200**。
- 保持 **生产路径**不变：`accept_all_invites` 仅 testbed（`ResipRuntimeListener` 文档已说明）。
- 重编：

```bash
make m2-platform-resip-build
```

### A.3 验证（Phase A 完成标准）

```bash
uv run pytest \
  platform/tests/test_e1_contract_resip_runtime.py::test_e1_s1_accept_all_harness_returns_200 \
  platform/tests/test_e1_contract_resip_runtime_full.py::test_e1_s1_accept_all_from_contract_invite \
  platform/tests/test_resip_runtime_integration.py::test_accept_all_invites_harness_mode_returns_200 \
  -q
```

再跑完整 E1 契约文件（确保 S2/S3/S4 未回退）：

```bash
uv run pytest platform/tests/test_e1_contract_resip_runtime.py platform/tests/test_e1_contract_resip_runtime_full.py -m contract -q
```

最后：

```bash
make gate   # 本机已编扩展时应 0 failed（E1 相关）
```

### A.4 可选文档

- 在 `platform/native/resip_runtime/README.md` 或 `platform/src/as_platform/sip/README.md` 加一句：`accept_all_invites` 与 S1 harness 的边界。

---

## 2. Phase B — 本地「真栈门禁」命令（短平快）

在 §3 落地前，维护者本地约定：

```bash
make m2-platform-resip-build
AS_REQUIRE_NATIVE_EXTENSIONS=1 make gate
# 或显式：
AS_REQUIRE_NATIVE_EXTENSIONS=1 uv run pytest -m "unit or contract" -q
```

`AS_REQUIRE_NATIVE_EXTENSIONS=1` 时，缺扩展 **fail** 而非 skip（`platform/tests/native_extensions.py`）。

**Makefile 可选增强（下一 session）：**

- 增加 `make gate-native`：`AS_REQUIRE_NATIVE_EXTENSIONS=1` + 依赖 `m2-platform-resip-build`（或检测 `.so` 存在）。
- 将未提交的 `Makefile` **UV / `.local/bin` 解析** 与 `repo-toolchain` 改动 **commit 到 master**（当前工作区可能仍有未提交 diff）。

---

## 3. Phase C — 编扩展并纳入阻塞 merge 的门禁

参考：`docs/reviews/callload-m2-m6-m7-demo-branch-review-2026-10-05.md` **F9**。

### C.1 新 job 或扩展现有 job（建议）

| Step | 内容 |
|------|------|
| 依赖 | `ubuntu-latest` + apt：`build-essential` `cmake` `libssl-dev` 等（对齐 `docs/acceptance/m2-native-build-matrix.md`） |
| Build | `make m2-native-restore`（若需要）+ `make m2-platform-resip-build` |
| Test | `AS_REQUIRE_NATIVE_EXTENSIONS=1 uv run pytest -m "unit or contract" -q` |
| 可选 | 同 job 跑 `pytest -m integration` 中与 `_resip_runtime` 相关的子集（见 §4 矩阵） |

### C.2 与现有 `fast` 的关系

- **方案 1（推荐）：** `fast` 保持无 native（快）；**新增 required** `native-contract` job。
- **方案 2：** `fast` 内增加 native build（变慢，单 job 简单）。

### C.3 验收

- PR 上 native job **红则不可 merge**。
- 故意破坏 `minimalHarnessAnswer` 时 job 必须失败。

---

## 4. Phase D — 覆盖率矩阵（相对 `sip-baseline` / test-plan）

**目标：** 从「7 条 E1 smoke」扩展到与 `docs/acceptance/test-plan.md` 对齐的**分阶段**真栈回放。

| 契约目录 | REQ / 含义 | 当前自动化（真栈） | 目标 |
|----------|------------|-------------------|------|
| S1-basic-call | REQ-F-1…F-5 基础 | E1：S1 harness 200（**红**）；无 14 条全文回放 | Phase A 修 harness；**D1** 增加 14 消息回放或 derived + 真栈 |
| S2-no-match-404 | REQ-F-6 | E1 **绿**（有 .so） | 保持；门禁必跑 |
| S3-policy-reject-603 | REQ-F-7 | E1 **绿** | 保持 |
| S4-caller-cancel | REQ-F-8 等 | E1 full **487 绿** | 保持 |
| S5–S11 | F-2/F-4/路由等 | 部分 **integration** / 未覆盖 | **D2** 按优先级加 `test_e1_*` 或 integration |

**`make gate` 外的真栈用例（应在 Phase C/D 纳入 integration 或 native build 门禁）：**

| 文件 | 标记 | 约条数 |
|------|------|--------|
| `test_resip_runtime_integration.py` | integration | 3 |
| `test_resip_runtime_tcp_integration.py` | integration | 1 |
| `test_resip_runtime_tls_integration.py` | integration | 3 |
| `test_resip_runtime_tls_policy_integration.py` | integration | 2 |
| `test_m7_forward_two_leg_integration.py` | integration | 1 |
| `test_resip_two_leg_integration.py` | integration | 1 |
| `test_req_f4_sdp_identity_integration.py` | integration | 3 |
| `test_req_s3_overlap_integration.py` | integration | 1 |
| D10 `test_d10_*_integration.py` | integration | 若干 |
| `testbed/simulators/tests/test_product_path.py` | integration | 4 |

**非真栈（勿与 SIP flow 混淆）：** `test_resip_runtime_log_contract.py`（日志解析）、`test_resip_runtime_call_controller.py`（unit）。

---

## 4-D. Phase D 排期定稿（2026-10-12 追加；§4 原文保留不改）

> **性质：排期与优先级决定。** 维护者 2026-10-12 指令「A3 Phase D 排期由 agent 自行判断、执行、不用问」。
> 本节回答「S5–S11 真栈用例按什么顺序做」；**不实现任何用例、不签收任何 REQ**。
> 用例实现属 A3/A4 后续批次，每批落地时另留 review record。

### 4-D.1 现状锚点（排期依据，2026-10-12 实测口径）

| 场景 | REQ | 当前真栈覆盖 | 缺口 |
|---|---|---|---|
| S5 双腿 B2BUA | F-2 | **部分**：e2e Wave 2 `test_e2e_s1_replay_second_leg_starts_a_new_call_id`（C_in≠C_out）+ `test_m7_forward_two_leg_integration.py` | 两腿**各自**归一化序列对拍 |
| S6 Request-URI 改写 | F-3 | **部分**：e2e E2E-SIP-1 出腿用户号断言 + `test_product_path.py` T1 + derived baseline 翻译场景 | 多规则优先级 / 无匹配组合的真栈对拍 |
| S7a SDP 完全透传 | F-4 | **子集**：e2e Wave 2 SDP offer 逐字节恒等 + `test_req_f4_sdp_identity_integration.py` + D11 fixtures | 更大 corpus（多 media 变体） |
| S8 Route/Record-Route | F-5 | **未覆盖**：`test_derived_baseline.py` 2 skip（S1 基线无 Route / Record-Route 头） | **先决缺口在基线本身**，需 M2 probe 补采 |
| S9 in-dialog 路由 | F-9 | **工程切片**：M7.3 `restore_from_checkpoint` / `route_in_dialog_bye` | in-dialog re-INVITE / UPDATE / BYE 真栈对拍 |
| S10 非 2xx 分支（486/480/408） | F-10 | **工程切片**：D9 adapter 486 映射已解决 | 对端返回非 2xx 的真栈透传对拍（testbed 对端当前只返 200） |
| S11 CANCEL 与最终响应竞态 | F-11 | **工程切片**：D9 forking / final-response race 归属 M8 验收 | 竞态两分支真栈对拍 |

### 4-D.2 优先级（P1 最高）

| 优先级 | 场景 | 为什么排这个位置 | 前置依赖 | 落地形态 |
|---|---|---|---|---|
| **P1** | S5 两腿归一化序列对拍 | Wave 2 的 bridge 采集框架已在位，扩成「两腿各自 INVITE→200→ACK→BYE→200」是成本最低、收益最直接的一条；把 REQ-F-2 从「子集」推成 fuller coverage | 无（复用 `testbed/e2e/` 框架） | e2e |
| **P2** | S7a SDP 透传 corpus 扩充 | byte-identity 断言已在 e2e；补带 media 描述 / 多 m-line 的 SDP 变体 corpus 即可扩大 D11 覆盖面 | 无 | e2e |
| **P3** | S6 多规则优先级 + 无匹配组合 | 出腿用户号断言已在 e2e；补「规则优先级 / 无匹配 404」组合，与 S2（404 已绿）共用仿真链 | 无 | e2e |
| **P4** | S10 非 2xx 透传 | 有 D9 工程基础，但**依赖先扩 testbed 对端 UAS**（当前只返 200，无法表达 486/480/408）—— 依赖新的仿真能力，故排在纯 e2e 扩充之后 | 扩 `as_simulators` / `PeerUas` 非 2xx 分支 | e2e 或 integration |
| **P5** | S9 in-dialog 路由 | 依赖 M7.3 context restoration 工程切片；需要 in-dialog 状态机驱动（re-INVITE / UPDATE / BYE），用例复杂度高 | M7.3 工程切片（已在位） | integration |
| **P6** | S11 CANCEL 竞态 | 竞态两分支的**确定性证明成本最高、flaky 风险最大**；放最后，且明确允许以 gap 登记收尾（竞态归属 M8 验收） | S4 cancel harness（487 已绿） | integration |
| **阻塞（不排优先级）** | S8 Route/Record-Route | 基线本身缺 Route / Record-Route 头（2 条既有 skip 的根因）。**补采前不排实现**；补采完成后建议插在 P3 之后。REQ-F-5 在补采前按 N4 停止线**不签 pass** | M2 probe 补采（Route / Record-Route 头） | 补采后重排 |

### 4-D.3 三条边界

1. **本排期不实现任何用例。** 实现按 P1→P6 分批启动，每批需维护者授权（或同等授权口径），落地时留 review record。
2. **S1 的 14 条逐条 header 对拍不在本表内** —— 它属 S1 的既有 gap，载体为 [`../acceptance/2026-10-11-wave2-replay-register.md`](../acceptance/2026-10-11-wave2-replay-register.md)（Wave 2 已落地归一化骨架，14 条逐条对拍仍未实现）。
3. **不签收任何 REQ。** 排期只定顺序；任何一条场景的签收以该批用例的证据 + 评审为准。

---

## 5. Phase E — M2 smoke 与 demo 边界（证据层）

真栈但不替代契约全集：

```bash
make m2-native-smoke
make m2-native-smoke-tcp-runtime
make m2-native-smoke-tls-runtime
```

Demo / kind：`docs/handoff/pre-m8-demo-review-plan.md`（`as-m71`）— 人工 + 脚本证据，**不**并入 `make gate`，但发布前应跑 story A/B。

---

## 6. 建议执行顺序（给下一 session）

1. **Phase A** — 修 `minimalHarnessAnswer` / harness 200，三条 pytest 绿。  
2. **Commit** — C++ + 任何 Python/文档；未提交的 `Makefile`（UV）、`publish_m71_bundle.py`（ruff）一并整理。  
3. **Phase B** — 本地 `AS_REQUIRE_NATIVE_EXTENSIONS=1 make gate` 习惯化；可选 `make gate-native`。  
4. **Phase C** — 增加 native required build job。  
5. **Phase D** — 按矩阵逐场景加测试（先 S1 14 条或子集，再 S5/S7/S8…）。  
6. **Phase E** — 里程碑/demo 前跑 M2 smoke + demo reset 检查。

---

## 7. 相关路径

| 项 | 路径 |
|----|------|
| 原生模块 | `platform/native/resip_runtime/` |
| Python 缝 | `platform/src/as_platform/sip/resip_runtime.py` |
| E1 测试 | `platform/tests/test_e1_contract_resip_runtime*.py` |
| 契约消息 | `testbed/contracts/sip-baseline/` |
| 扩展 skip/fail | `platform/tests/native_extensions.py` |
| 评审 F9 | `docs/reviews/callload-m2-m6-m7-demo-branch-review-2026-10-05.md` |
| M7 E1 签收范围 | `docs/reviews/m7-e1-contract-review-2026-10-05.md`（未含 S1 harness 200） |

---

## 8. `cur` / `callload` 清理（已完成 2026-10-09）

- **`origin/callload`** — 已删。  
- **`cur` / `origin/cur`** — 已删；M5.1 与 toolchain 在 **`master`**（含 `c2d56e4` 等）。  
- 克隆若仍见本地 `cur`：`git fetch --prune && git branch -D cur`。

---

## Sign-off（本计划）

- [x] Phase A 完成（3 条 S1/harness pytest 绿） —— **2026-10-11 真栈复验通过**：
  `platform/tests/test_e1_contract_resip_runtime.py` + `test_e1_contract_resip_runtime_full.py` `-m contract` → **7 passed**；
  `test_resip_runtime_integration.py::test_accept_all_invites_harness_mode_returns_200`（`integration` 标记，须显式指定）→ **1 passed**。
  三元组 `(已验证, docs/acceptance/artifacts/m5/2026-10-11/PASS-phase-a-revalidation-2026-10-11.txt, 2026-10-11)`。
  注：本计划 §0 记录的「本机有 `.so` 时 **2 failed**」在本次真栈复验中**未复现**；
  这不构成对任何 REQ 的签收。执行记录 [`2026-10-11-w0-native-and-e2e-execution-record.md`](2026-10-11-w0-native-and-e2e-execution-record.md) §4
- [ ] Phase C native build job 绿且 required —— **未完成（2026-10-11 标注）**：
  CI job 未创建，属 CI 配置变更，需维护者授权；本次只在**本机**把 `make gate-native` 跑常态化
  （`1068 passed / 2 skipped / 206 deselected`，exit 0）
- [x] Phase D 至少 S1 全链或明确推迟项写入 `test-plan.md` / `plan.md` —— **2026-10-12 满足**：S5–S11 的排期与优先级已定稿并落本文 §4-D（P1 S5 两腿归一化对拍 → P6 S11 竞态；S8 因基线缺 Route / Record-Route 头登记为阻塞项，补采前不排；S1 的 14 条逐条 header 对拍仍由 wave2 register 跟踪）。排期由维护者 2026-10-12 授权 agent 自行判断；**未实现任何用例、未签收任何 REQ**。
  —— **未完成（2026-10-11 标注，原文保留）**：「S1 的 14 条回放」已由 A4-3 的仓内载体 [`../acceptance/2026-10-11-wave2-replay-register.md`](../acceptance/2026-10-11-wave2-replay-register.md) 承接，但**用例未实现**；S5–S11 真栈用例的排期需维护者确认优先级
