# 执行记录：W0 真栈构建常态化 + A3 复验 + A4 Wave 1 e2e 落地

> **状态：已执行，待维护者评审；不签收任何 REQ / 里程碑。**
> 本文是 [`2026-10-10-unfinished-assessment-and-next-plan.md`](2026-10-10-unfinished-assessment-and-next-plan.md)
> §0-A.1（已授权三项）与 §5 W0 中**本机可执行部分**的执行记录；计划原文未回填，本文一律**追加**。
> 依据：该文 §0-A.6 的 G1–G8 已于 2026-10-10 全部落盘为裁决记录，W0 的 A2 / A3 **不依赖任何未决裁决**；
> 维护者 2026-10-10 的「评审通过不等于执行授权」口径**仍然有效**，本文的记录不替代逐次批准。
>
> **本文不签收任何 REQ、任何里程碑，不构成外部验收通过，不解除任何 hold**
> （外部 IOT / 真实环境采证 hold 与 M8 退出签字后置继续有效）。
> **本次未执行任何 git 写操作**：未 `commit` / `add` / `push` / `tag` / 建分支 / 改 remote；
> 全部改动停留在工作树，commit 拆分由维护者决定。

**执行环境**：已登记环境 **`dev-win03ib7niepf0`**（host `WIN-03IB7NIEPF0`，Ubuntu 22.04.5 LTS / WSL2 / x86_64，
用户 `shudong`，全程无 root）。执行日期：2026-10-11。

---

## 0. 结论速览

| 项 | 结果 | 三元组 / 依据 |
|---|---|---|
| **A2 · 真栈构建常态化** | ✅ 完成。`make m2-platform-resip-build` 成功；`make gate-native` exit 0，**1068 passed / 2 skipped / 206 deselected**；原 7 条 `native_extensions.py` skip 与 1 条 `_resip_recovery` skip **全部消失（真实执行）** | `(已验证, docs/acceptance/artifacts/m5/2026-10-11/PASS-gate-native-2026-10-11.txt, 2026-10-11)` |
| **A3 · Phase A 真栈复验** | ✅ 完成。契约 7 条 + integration 1 条**全绿**（此前从未有真栈复验记录） | `(已验证, docs/acceptance/artifacts/m5/2026-10-11/PASS-phase-a-revalidation-2026-10-11.txt, 2026-10-11)` |
| **A5 · 告警规则语法校验** | ✅ 本机复跑。`make alert-check`（本地 promtool **2.55.1**）→ `SUCCESS: 10 rules found`（3 组 10 条）；`make chart-check` → `chart-check: OK` | 见 §6；P4 的既有闭合（2026-10-11）未被重开 |
| **A4 · e2e Wave 1 落地** | ✅ 完成。新建 `testbed/e2e/test_sip_first_edition.py`，`pytest -m e2e` 由 **0 条**变为 **5 条且连续 3 次全绿**；缺 native 时 **fail 而非 skip**（实测验证） | `(已验证, docs/acceptance/artifacts/m5/2026-10-11/PASS-e2e-2026-10-11.txt, 2026-10-11)` |
| **本地真栈 smoke（E1 / E4 / E5 本地部分）** | ✅ 四项全过：S1 UDP、S1 TCP、TCP runtime（1 passed）、TLS runtime（3 passed） | `(已验证, docs/acceptance/artifacts/m5/2026-10-11/PASS-native-smoke-2026-10-11.txt, 2026-10-11)` |
| **M7 扩展（W0 表格「如需」项）** | ✅ 顺带完成：`_resip_recovery` 与 `_resip_two_leg` 均已构建 | 见 §3.2 |
| **A2 暴露出的既有缺陷** | ⚠️ 发现并**已修**：`RESIP_RUNTIME_LISTENING` 端口正则不含 `advertised=` 字段，**共 5 处**，自 commit `139d299` 落地起从未匹配成功（因缺 `.so` 一直 skip）。修后 `testbed/load` smoke 1 passed、`m6-product-runtime-smoke.sh` exit 0 | 见 §11。**未产生任何容量或性能数字** |
| **根守卫 `uv run pytest tests/ -q`** | ✅ **115 passed** | 见 §8 |
| **普通 `make gate`（非 native 模式）** | ✅ exit 0，**1084 passed / 2 skipped / 211 deselected** | 见 §8（211 = 206 + 本次新增的 5 条 e2e，均被 `-m "unit or contract"` deselect） |

**未完成 / 不在本次范围**：W1（A6 版本口径的**执行**）、W2（B1–B6，维护者裁决 / 评审，其中 B1 取值仍 open）、
W3（C1–C5，需外部环境，§0 第 2 项 hold）、A4-3 的 Wave 2 十四条回放（载体已由
[`../acceptance/2026-10-11-wave2-replay-register.md`](../acceptance/2026-10-11-wave2-replay-register.md)
承接，实现待 A4 后续批次）、A5 的**抓取接线**（X1，仍待运营商 monitoring-integration 标准输入）。
明细见 §9。

---

## 1. 关键事实：本机此前从未编出过 native 扩展

`make gate-native` 之所以是「最大缺口」，是因为本机在此之前**没有任何** `_resip_*.so`：

| 检查 | 2026-10-11 执行前实测 |
|---|---|
| `find . -name "_resip*.so"` | **无任何命中** |
| `.cache/` 目录 | **不存在**（reSIProcate 源码与构建树从未在本机恢复 / 编译） |
| 后果 | 7 条 `platform/tests/native_extensions.py:24` + 1 条 `test_sip_recovery.py:69` 为 **skip，不是通过** |

本次是自 2026-10-09 [`2026-10-09-sip-native-testing-plan.md`](2026-10-09-sip-native-testing-plan.md)
落盘以来，本机**第一次**跑出真栈门禁。

---

## 2. 前置：native 构建依赖的无 root 取径（本机此前缺两件 dev 包）

`testbed/simulators/resip-probe/scripts/m2-native.sh` 的 `check_native_build_deps()` 要求
`popt` / `libcares` / `openssl` 三个 pkg-config 包。本机实测：**openssl ✅，popt ❌，libcares ❌**
（两个运行时库 `libpopt.so.0` / `libcares.so.2` 在 `/usr/lib/x86_64-linux-gnu/` 存在，但 **dev 包未装**，
无 `.pc`、无头文件）。本机 `sudo` **需要密码**，全程无 root，故走「下载 .deb → 解压到仓库内 `.cache/`（gitignored）→
用环境变量指给 cmake」的取径，**不改动系统**。

### 2.1 为什么不用 vendor 里的 prebuilt 压缩包

`testbed/simulators/resip-probe/vendor/resiprocate-m2-ubuntu20.04-x86_64-prebuilt-20261004.tar.gz`
是 **Ubuntu 20.04 / OpenSSL 1.1** 的构建产物；本机为 **Ubuntu 22.04 / OpenSSL 3**
（`libssl.so.3` / `libcrypto.so.3`）。按该 vendor 目录 `README.md` 的明文要求
（「Reuse the binaries only when `ldd` resolves every dependency … Newer Ubuntu releases commonly
provide OpenSSL 3 instead; in that case rebuild from the bundled source」），
**prebuilt 路径不成立**，本次改为**从随仓源码构建**。

### 2.2 实际执行的命令（可复现）

```bash
# 1) 随仓源码恢复（sha256 由脚本校验）
make m2-native-restore
# 实测输出：resiprocate-1.14.0-632e215c-source.tar.gz: OK ；prebuilt: OK
#          extracting ... -> .cache/m2-resiprocate/source

# 2) 取两个 dev 包（apt-get download 不需要 root）
mkdir -p /tmp/depdl && cd /tmp/depdl
apt-get download libpopt-dev libc-ares-dev
dpkg-deb -x libc-ares-dev_*_amd64.deb x-libc-ares-dev
dpkg-deb -x libpopt-dev_*_amd64.deb    x-libpopt-dev

# 3) 装进仓库内 .cache/native-deps/（gitignored，不入库）
cd /home/shudong/project/3rdparty-as
mkdir -p .cache/native-deps/usr
cp -a /tmp/depdl/x-libc-ares-dev/usr/. .cache/native-deps/usr/
cp -a /tmp/depdl/x-libpopt-dev/usr/.    .cache/native-deps/usr/
LIB=.cache/native-deps/usr/lib/x86_64-linux-gnu
# dev 包里的 .so 是指向 .so.N 的符号链接，指回系统运行时库（链接期用，运行期仍由系统解析）
ln -sf /usr/lib/x86_64-linux-gnu/libcares.so.2 $LIB/libcares.so
ln -sf /usr/lib/x86_64-linux-gnu/libpopt.so.0  $LIB/libpopt.so

# 4) 构建期环境变量（每条 make 命令前都要带上）
export PKG_CONFIG_PATH="$PWD/.cache/native-deps/usr/lib/x86_64-linux-gnu/pkgconfig"
export CMAKE_PREFIX_PATH="$PWD/.cache/native-deps/usr"
export CMAKE_LIBRARY_PATH="$PWD/.cache/native-deps/usr/lib/x86_64-linux-gnu"
export CPLUS_INCLUDE_PATH="$PWD/.cache/native-deps/usr/include"
export C_INCLUDE_PATH="$PWD/.cache/native-deps/usr/include"
```

**一处实测坑（记录以免重踩）**：只设 `PKG_CONFIG_PATH` + `CMAKE_PREFIX_PATH` 时，cmake 配置能通过，
但编译 `rutil` 时报 `fatal error: ares.h: No such file or directory`
—— reSIProcate 的 `WITH_C_ARES=ON` 只把 `PkgConfig::cares` 挂到链接库，**没有把它的 include 目录加入编译目标**，
必须再用 `CPLUS_INCLUDE_PATH` / `C_INCLUDE_PATH` 补头文件路径。

**本机工具链**：`cmake 3.22.1`、`g++ 11.4.0`、`pkg-config`、`nproc 12`。

---

## 3. A2 · 真栈构建常态化

### 3.1 构建 reSIProcate 与 probe

```bash
make m2-native-build        # = build-resip + build-probe
```
实测：exit 0；`reSIProcate build OK: .cache/m2-resiprocate/build`；
`resip_probe OK: .cache/m2-resiprocate/probe-build/resip_probe`。

### 3.2 构建三个平台扩展

| 命令 | 产物 | 结果 |
|---|---|---|
| `make m2-platform-resip-build` | `platform/native/resip_runtime/build/_resip_runtime.cpython-310-x86_64-linux-gnu.so` | ✅ |
| `make m7-platform-recovery-build` | `platform/native/resip_recovery/build/_resip_recovery.cpython-310-x86_64-linux-gnu.so` | ✅ |
| `make m7-platform-two-leg-build` | `platform/native/resip_two_leg/build/_resip_two_leg.cpython-310-x86_64-linux-gnu.so` | ✅ |

后两个属 W0 表格里的「M7 扩展（如需）」：本次**需要** —— 只有它们就位，`test_sip_recovery.py:69`
那条 skip 才会消失。

### 3.3 `make gate-native` 实测结果

| 运行 | 结果 | 说明 |
|---|---|---|
| 只编出 `_resip_runtime` 时 | **1067 passed / 3 skipped / 206 deselected / 11 warnings**，exit 0 | 剩 1 条 `_resip_recovery` skip + 2 条 `test_derived_baseline` skip |
| 三个扩展齐全后（收口值） | **1068 passed / 2 skipped / 206 deselected / 11 warnings**，exit 0 | 见下 |

**A2 出口判据逐条核对：**

| 出口判据 | 实测 |
|---|---|
| `make m2-platform-resip-build` 成功 | ✅ §3.2 |
| `AS_REQUIRE_NATIVE_EXTENSIONS=1 make gate`（等价 `make gate-native`）跑通 | ✅ exit 0 |
| 原 7 条 `native_extensions.py` skip **消失** | ✅ 收口运行的 `SKIPPED` 段**只剩 2 条**，均来自 `testbed/simulators/tests/test_derived_baseline.py:245` / `:279`（S1-basic-call 未构造 Route / Record-Route header，需专门的 M2 probe capture）——**没有一条**来自 native 扩展缺失 |
| 一次完整 run 结果已留档 | ✅ `PASS-gate-native-2026-10-11.txt` |

> **关于 1068 与历史计数的关系**：本文不把它与 2026-10-10 的 `1002 passed / 10 skipped` 作减法解释 ——
> 两者相隔多个 session，期间守卫与测试用例本身持续增长（2026-10-11 早些时候本机的普通 `make gate`
> 已为 `1037 passed / 10 skipped`）。A2 的判据是**「native 相关 skip 是否消失」**，这由收口运行的
> `SKIPPED` 段直接证明，与绝对计数无关。

---

## 4. A3 · SIP native plan 的 Phase A 复验

```bash
uv run pytest platform/tests/test_e1_contract_resip_runtime.py \
              platform/tests/test_e1_contract_resip_runtime_full.py -m contract -q
# → 7 passed in 0.73s

uv run pytest platform/tests/test_resip_runtime_integration.py::test_accept_all_invites_harness_mode_returns_200 -q
# → 1 passed in 0.12s
```

**A3 出口判据逐条核对：**

| 出口判据 | 实测 |
|---|---|
| ① 两个 E1 契约文件（含 `test_e1_s1_accept_all_harness_returns_200`、`test_e1_s1_accept_all_from_contract_invite`）有真实执行结果 | ✅ `7 passed`，契约层 S1–S4 全绿（此前只有改动、**无真栈复验记录**） |
| ② `test_resip_runtime_integration.py::test_accept_all_invites_harness_mode_returns_200`（`integration` 标记，**不在** `-m "unit or contract"` 收集内，须显式指定） | ✅ `1 passed` |
| Phase D 的范围与批次已排期 | ⚠️ **未由本次完成** —— 该 plan Phase D（S1 的 14 条回放、S5–S11 真栈用例）的排期需维护者确认优先级；其中「S1 的 14 条回放」已由 A4-3 的仓内载体 [`../acceptance/2026-10-11-wave2-replay-register.md`](../acceptance/2026-10-11-wave2-replay-register.md) 承接 |
| 该 plan 文末 Sign-off 三框的处置已明确 | ✅ 已在 [`2026-10-09-sip-native-testing-plan.md`](2026-10-09-sip-native-testing-plan.md) 文末**追加**处置：框 1（Phase A）勾选；框 2（Phase C native build job）与框 3（Phase D）标注未完成并写明依据 |

> **2026-10-09 那份 plan 的 §0「本机有 `.so` 时 2 failed」** 在本次真栈复验中**未复现**：
> `test_e1_s1_accept_all_harness_returns_200` 与 `test_e1_s1_accept_all_from_contract_invite` 均通过。
> 这不构成对 REQ 的任何签收，只说明 Phase A 在 commit `18f2bb7` 之后的改动**经真栈复验为绿**。

---

## 5. 本地真栈 smoke（E1 / E4 / E5 的本地部分，不属外部 IOT）

按 [`2026-10-10-unfinished-assessment-and-next-plan.md`](2026-10-10-unfinished-assessment-and-next-plan.md)
§0.1 的例外段与 §5「W0 范围调整」：S1–S4 harness 与**自签证书**的 TLS smoke **不属于外部 IOT**，
不因 §0 第 2 项裁决后置，随 A2 / A3 在 W0 推进。

| 命令 | 实测 |
|---|---|
| `make m2-native-smoke`（S1 UDP，`resip_probe` 跑通到 `RemoteBye`） | exit 0，`smoke passed (S1 UDP)` |
| `make m2-native-smoke-tcp`（S1 TCP loopback） | exit 0，`smoke passed (S1 TCP)` |
| `make m2-native-smoke-tcp-runtime`（产品 TCP runtime integration） | exit 0，`1 passed` |
| `make m2-native-smoke-tls-runtime`（产品 TLS runtime integration，**测试 CA / 自签**） | exit 0，`3 passed`（21.57s） |

**边界（不得夸大）**：TLS 用的是**随测试生成的自签测试 CA**，
按既有口径**不签收 REQ-S-2 / REQ-S-3**（那需要运营商 PKI 与外网 S-SBC，属后置的外部采证）。

---

## 6. A5 · 告警规则语法校验与 chart 形状门禁（本机复跑）

本机 2026-10-11 的 infra bootstrap 已把 `helm` / `promtool` 装入 `tools/bin/`（不入库），
故 `tools/bin` 需在 `PATH` 中：

```bash
export PATH="$PWD/tools/bin:$PATH"
make chart-check   # → chart-check: OK（1 chart(s) linted, 0 chart(s) failed），exit 0
make alert-check   # → Checking deploy/alerts/as-alerts.yaml / SUCCESS: 10 rules found，exit 0
```

- `alert-check` 用的本地 **promtool 2.55.1**，与 2026-10-05 历史 alert 证据**同版本**；
  10 条 = `as.call-path` 5 + `as.runtime` 3 + `as.platform` 2（3 组）。
- 这与 register §2 P4 的既有闭合**是同一件事的不同证据基座**，本文**不重开** P4。
- **`promtool` 只是语法校验**：X1（抓取接线 annotation vs ServiceMonitor/PodMonitor）仍待运营商
  monitoring-integration 标准输入，**语法通过 ≠ 接线闭合**。

---

## 7. A4 · e2e Wave 1 落地

### 7.1 依裁决落地（四项裁决均已于 2026-10-10 落盘）

| 裁决 | 落地方式 | 实测 |
|---|---|---|
| **A4-1** 新建独立文件 | 新建 `testbed/e2e/test_sip_first_edition.py`；**不动** `testbed/simulators/tests/test_product_path.py` 的 `integration` 标记 | ✅ integration 层原样保留 |
| **A4-2** 缺 native 时 **fail** | 用例内 `_require_product_stack()`：**无条件 fail**，不做 env 分支、不 skip | ✅ 实测：临时移走 `_resip_runtime*.so` 后 `-m e2e` → **5 failed，0 skipped**（失败信息为 `e2e never skips for a missing native extension (A4-2)`）；随后已还原 `.so` 并复跑确认恢复 |
| **A4-3** Wave 2 的 14 条后置到独立载体 | 载体 = [`../acceptance/2026-10-11-wave2-replay-register.md`](../acceptance/2026-10-11-wave2-replay-register.md)（register §2 P5 已闭合） | ✅ 本次**不实现** 14 条对拍，Wave 1 亦未含（该 plan Wave 1 的「明确不做」条即写明 14 条逐条 header 对拍不在 Wave 1） |
| **A4-4** kind e2e 进 PR required 的 E2E policy | 裁决原文写明「**该方向仅是政策方向登记，不构成任何配置变更授权；本任务不改任何配置文件**」 | ✅ 本次**未改**任何 CI / 门禁配置；新建的是本机可跑的 **非 kind** e2e |

### 7.2 用例与实测

| 用例 ID（该 plan §3） | 测试 | 断言要点 |
|---|---|---|
| E2E-SIP-1 | `test_e2e_sip_1_udp_t1_translated_call_completes` | UDP T1 终态为 **200**；出腿用户为翻译结果 `013800138000`（且入腿主叫 `+8613800138000` 未直达对端）；BYE 数 == 应答数；`unresolved_sessions == 0`；无 `bye_*` 错误 |
| E2E-SIP-2 | `test_e2e_sip_2_udp_t4_no_match_returns_404` | UDP T4 终态 **404**；`+155500030003` 未到达对端 UAS；BYE 数 == 0 |
| E2E-SIP-3 | `test_e2e_sip_3_udp_f2_blocked_returns_603` | UDP F2 终态 **603**；不出业务腿；BYE 数 == 0 |
| E2E-SIP-4 | `test_e2e_sip_4_stream_transport_t1_completes[tcp\|tls]` | TCP 与 TLS 各一条 T1 子集；TLS 用**测试 CA**，docstring 明写「不签收 REQ-S-2 / REQ-S-3」 |

```
uv run pytest -m e2e -q
→ 5 passed, 1292 deselected, 1 warning      （连续 4 次：4.85s / 4.76s / 4.51s / 4.81s，均 5 passed）

> **deselected 计数说明**：同一命令在收尾复跑时为 `1292`（全仓收集 1297）。
> 差额 16 来自根守卫 `tests/test_evidence_discipline.py` 对证据文件的逐文件参数化 ——
> 本次新增的 8 个证据文件使守卫用例 +16（99 → 115），全仓收集数随之上升。
> 两次都是同一命令的真实输出，**不是** e2e 用例数的变化：e2e 恒为 5 条。
```

**e2e 而非 integration 的三条属性**（写进用例 module docstring）：被测 AS 是**产品栈**
（`_resip_runtime` + `ResipRuntimeListener`）；判决走**生产缝**（`decide()` over `demo_rules()`，
`accept_all_invites` 保持关闭）；路径**跨网元边界**（负载发生器 → 仿真 S-CSCF → 仿真 S-SBC → AS → 对端 UAS）。

**一处实现取舍（记录）**：`run_load` 在负载窗口内的**呼叫条数**随 `duration_seconds` / `workers`
与场景是否立即终断而变（实测单场景 `workers=1` 时，T1 为 1 条、T4 / F2 为 3 条）。
因此断言**只对终态响应码集合与「BYE 数 == 应答数」这类不变量**取值，
不对条数写死 `== 1`，避免把时序抖动固化成 flaky 断言。

### 7.3 与 S1 第 4 项的关系（未改行为，只补注记）

S1 第一批把 `-m e2e` 从 `make test` 移出，原因是当时 `-m e2e` 收集为空、必然 exit 5。
现在 e2e 已非空，该注释的事实前提变了，故在 `Makefile` 的 `test` target 注释上**追加一句注记**
说明现状；**`make test` 的实际行为一个字未改** —— 是否把 e2e 层重新纳入 `make test`
属门禁配置变更，与 A4-4 同属**维护者裁决**范围（A4-4 的裁决明确「不构成任何配置变更授权」）。

---

## 8. 证据清单（一律用三元组表述）

| 三元组 | 内容 |
|---|---|
| `(已验证, docs/acceptance/artifacts/m5/2026-10-11/PASS-gate-native-2026-10-11.txt, 2026-10-11)` | `make gate-native` → `1068 passed, 2 skipped, 206 deselected, 11 warnings`，exit 0；**含 2 条 SKIPPED**（均来自 `test_derived_baseline.py:245` / `:279`，非 native 缺失） |
| `(已验证, docs/acceptance/artifacts/m5/2026-10-11/PASS-phase-a-revalidation-2026-10-11.txt, 2026-10-11)` | A3 复验：契约 7 passed + integration 1 passed |
| `(已验证, docs/acceptance/artifacts/m5/2026-10-11/PASS-e2e-2026-10-11.txt, 2026-10-11)` | `uv run pytest -m e2e -q` → `5 passed, 1292 deselected`（收尾复跑值；同日更早的运行为 `1276 deselected`，差额 16 来自新增证据文件使根守卫参数化用例 +16，e2e 恒为 5 条，见 §7.2） |
| `(已验证, docs/acceptance/artifacts/m5/2026-10-11/PASS-native-smoke-2026-10-11.txt, 2026-10-11)` | 四项本地真栈 smoke，逐项 `exit=0` |

另有本机复跑（与 2026-10-11 同日早些时候的 bootstrap 轮为同一被验项，非新结论）：
`make chart-check` → `chart-check: OK`；`make alert-check` → `SUCCESS: 10 rules found`。

**根守卫**：`uv run pytest tests/ -q` → **115 passed**（2026-10-11 收尾实测）。
该计数随守卫用例增长而变：本次新增的 8 个证据文件被
`tests/test_evidence_discipline.py::test_evidence_filename_states_its_verdict` 逐文件参数化覆盖，
故守卫数随之上升；与 register 记录的 62 / 68 / 76 / 94 / 99 属不同 session 的实测事实，不冲突。

**`make gate`（普通模式，非 native）**：exit 0，**1084 passed / 2 skipped / 211 deselected**。
`211 deselected` 比 native 模式前的 `206` 多 5 —— 即本次新增的 5 条 e2e（被 `-m "unit or contract"` 排除）。

**静态检查**：`uv run ruff check testbed/e2e/` → `All checks passed!`；
`uv run ruff format --check testbed/e2e/` → `1 file already formatted`；
`make gate` 内含的 `ruff format --check .` / `ruff check .` / `mypy` 均通过。

---

## 9. 范围外 / 未做事项（逐条写明，不含糊）

| 未做 | 理由 / 归属 |
|---|---|
| **A6 版本口径的执行**（同步 `Chart.yaml` version / appVersion、声明 `kubeVersion`） | G4 裁决写明「当前不修改 `VERSION` 与 `Chart.yaml`」；`kubeVersion` 的最小值「由所用 API 反推，本次不作数值裁决」。**本次未改** `VERSION` / `Chart.yaml` |
| **A5 抓取接线**（annotation vs ServiceMonitor/PodMonitor） | **X1 仍待运营商 monitoring-integration 标准输入**；裁决写明「当前不改 chart」。`deploy/helm/` 一个字节未动 |
| **A4 Wave 2 的 14 条对拍** | 载体已就位（wave2-replay-register），实现待 A4 后续批次；**不签收 REQ-F-1**，其 14 条全文仍 open |
| **Phase C（native build 进 CI 且 required）** | 属 CI 配置变更，需维护者授权；本次只在**本机**常态化 |
| **Phase D（S5–S11 真栈用例）排期** | 需维护者确认优先级 |
| **W2 · B1–B6** | B1（O1）**取值仍 open**；B2 / B3 / B4 的取值已裁但**实现未落 / 未授权**；B5（M8 N2 九项 + 签字）、B6（16 份包装文档评审）属**维护者**动作 |
| **W3 · C1–C5** | 需外部环境，且 §0 第 2 项 hold 继续有效。**不以本机真栈绿充抵任何一项** |
| **`deploy/` 任何改动** | chart / alerts / kind 脚本**一个字节未动** |
| **git 写操作** | 无 `commit` / `add` / `push` / `tag` / 建分支 / 改 remote |

---

## 10. 需要维护者注意的三件事

1. **本机 native 构建依赖一个仓库外的临时目录**（`.cache/native-deps/`，gitignored、不入库）。
   换一台机器（或清空 `.cache/`）后，`make m2-platform-resip-build` 会退回「缺 dev 包」状态，
   需按 §2.2 重做，或在有 root 的机器上直接 `apt-get install libpopt-dev libc-ares-dev`。
   **这是一条新的机器能力事实**，尚未写进 [`../environments.md`](../environments.md) 的登记行
   （该表由 `tools/env-probe.sh` 生成、不得手改，故本次只在本文记录，是否把它纳入探测脚本**待维护者决定**）。
2. **A4-4 与「e2e 是否回到 `make test`」是同一个未决口**，本次**未替维护者裁决**：
   `make test` 的行为保持 S1 第一批的原样（只跑 unit/contract + integration）。
3. **真栈绿不等于 REQ 级验收通过**：本次所有结论都是**工程门禁层**的证据，
   `report.md` §0.5 的 open 24 / blocked 12 **一个字未改**，不签收任何 REQ，不签收任何里程碑。

---

## 11. A2 暴露出的一个既有缺陷（已修，需维护者确认）

**这正是 A2 的价值所在**：把 skip 变成真实执行之后，一个此前**从未被发现**的缺陷立刻现形。

### 11.1 现象

`testbed/load/tests/test_product_runtime_smoke.py::test_product_resip_runtime_uas_smoke`
在真栈就位后**第一次真正运行即失败**：

```
Failed: timed out waiting for RESIP_RUNTIME_LISTENING:
RESIP_RUNTIME_LISTENING address=127.0.0.1 advertised=127.0.0.1 udp_port=45749
```

### 11.2 根因（不是本机环境问题）

- C++ 侧（`platform/native/resip_runtime/runtime_module.cxx:1478-1480`）实际输出
  `address=… advertised=… udp_port=…` —— 这与
  [`../acceptance/m8-resip-runtime-log-contract.md`](../acceptance/m8-resip-runtime-log-contract.md) §3
  记录的行格式**一致**（该文档示例行即含 `advertised=`）。
- 但消费方用的是**不含 `advertised=`** 的旧正则
  `RESIP_RUNTIME_LISTENING address=127\.0\.0\.1 udp_port=(\d+)` —— 永远匹配不上，必然超时。
- `git log -S` 显示：`advertised=` 的打印与该 smoke 用例**同在 commit `139d299`** 落地，
  即**这条例行从落地的那一刻起就没能匹配过**；它之所以一直没红，只是因为本机（以及被记录到的各次运行）
  从来没有 `.so`，用例一直在 **skip**。

**同一缺陷共 5 处**：`testbed/load/tests/test_product_runtime_smoke.py` 的 `_LISTEN_RE`，
以及 `testbed/load/scripts/` 下 4 个 M6 脚本的 `_UAS_UDP_RE`
（`m6-product-runtime-smoke.sh`、`m6-product-runtime-micro-measure.sh`、
`m6-product-runtime-measure-60s.sh`、`m6-o1-formal-report.sh`）——
后四者用 `sed -nE` 提取端口，同样会永远取不到端口而 `die`。

### 11.3 修法（向后兼容，不引入容量数字）

正则改为**把 `advertised=` 作为可选字段**：

| 位置 | 改法 |
|---|---|
| `testbed/load/tests/test_product_runtime_smoke.py` | `_LISTEN_RE` → `RESIP_RUNTIME_LISTENING address=127\.0\.0\.1 (?:advertised=\S+ )?udp_port=(\d+)`（Python `re`，捕获组序号不变） |
| `testbed/load/scripts/m6-*.sh`（4 个） | `_UAS_UDP_RE` → `… address=127\.0\.0\.1 (advertised=[^ ]+ )?udp_port=([0-9]+)`，`sed` 反向引用 `\1` → `\2`（ERE **不支持** `(?:…)`，故用捕获组并把端口改为 `\2`） |

**验证**：

- `uv run pytest testbed/load/tests/test_product_runtime_smoke.py -q` → **1 passed**（此前 failed，60s 超时）
- `bash testbed/load/scripts/m6-product-runtime-smoke.sh` → exit 0，
  `smoke passed (established_sessions=1)`，`UAS UDP port: 45662`（此前会在取端口处 `die`）
- 正则双格式实测：`advertised=` 在/不在**均能**取到端口（45749 / 5060）
- `uv run ruff check testbed/load/` → `All checks passed!`；`ruff format --check` → `12 files already formatted`；
  4 个 shell 脚本 `bash -n` 通过

**边界**：本次**未产生、也未改写**任何容量或性能数字；修的是**端口提取正则**，
M6 的历史测量报告与 O1 结论**不在本次范围内**。

### 11.4 另一项实测事实（未修，属环境依赖）

`make test` 的 integration 层在本机**跑不全**：`services/config-service` 的 Postgres 集成用例需要
`127.0.0.1:55432` 的 PostgreSQL（compose 提供），本机未起该服务 ⇒
**113 errors + 1 failed（PG 相关）+ 11 skipped**；`make test` 最终 exit 2。
这与本次改动**无关**（同样的情况在任何未起 compose PG 的机器上都会出现），
且**不是** A2 / A3 / A4 的出口判据。启动 compose PG 属容器动作，**本次未做**，如实登记。

---

**落盘日期：2026-10-11。状态：已执行，待维护者评审。**
（对应计划：[`2026-10-10-unfinished-assessment-and-next-plan.md`](2026-10-10-unfinished-assessment-and-next-plan.md)
§0-A.1 / §5 W0；环境登记：[`../environments.md`](../environments.md)；
证据索引：[`../acceptance/artifacts/m5/README.md`](../acceptance/artifacts/m5/README.md)。）
