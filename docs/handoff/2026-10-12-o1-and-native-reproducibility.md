# 执行记录：integration 层补齐 + native 可复现性 + O1 饱和点探测 + A4 Wave 2 落地

> **状态：已执行，待维护者评审；不签收任何 REQ / 里程碑。**
> 本文记录维护者 2026-10-12 授权的**四件**工作，起因是上一轮收尾时我把其中两项的性质说错了：
> ① 把「起 compose PostgreSQL 跑 integration 层」误归为「容器动作需授权」（并无此规矩，见 §2）；
> ② 把 A4 Wave 2 误归为「我自己划的界」（它实为 2026-10-10 已落盘的裁决，见 §5.1）。
> 本文一律**追加**，不改写任何既有原文。
>
> **本文不签收任何 REQ、不签收任何里程碑、不构成外部验收通过、不解除任何 hold**
> （外部 IOT / 真实环境采证 hold 与 M8 退出签字后置继续有效）。
> **未执行任何 git 写操作**：未 `commit` / `add` / `push` / `tag` / 建分支 / 改 remote。

**执行环境**：已登记环境 **`dev-win03ib7niepf0`**（host `WIN-03IB7NIEPF0`，
Ubuntu 22.04.5 LTS / WSL2 / x86_64，用户 `shudong`）。执行日期：2026-10-12。

---

## 0. 结论速览

| 项 | 结果 | 三元组 / 依据 |
|---|---|---|
| **① integration 层补齐** | ✅ 从「113 errors + 2 failed」变为 **200 passed / 1 skipped / 0 failed / 0 error**（PG 12.22 + `wal_level=logical` + Redis） | `(已验证, docs/acceptance/artifacts/m5/2026-10-12/PASS-integration-pg-logical-2026-10-12.txt, 2026-10-12)` |
| **② 新发现：PG 15 不兼容** | ⚠️ **如实失败**：PG **15.18** 下 integration **1 failed / 76 errors**，根因 `defaclobjtype \|\| ':'` → `AmbiguousFunction: operator is not unique: "char" \|\| unknown`（PG 14+ 把该列类型由 `char` 改为 `"char"`）。**未改任何产品代码** | `(失败, docs/acceptance/artifacts/m5/2026-10-12/FAIL-integration-pg15-2026-10-12.txt, 2026-10-12)` |
| **③ native 可复现性验证**（B4 建议第一步） | ✅ 换**独立缓存目录**从零 `restore` → 构建 reSIProcate + probe → 构建 `_resip_runtime` → `make gate-native` exit 0（**1100 passed / 2 skipped**）。native 构建**可重建且产物可用** | 见 §3 |
| **④ O1 饱和点探测**（B1 建议第二步） | ⚠️ **未测到饱和点**：20 → 1280 CPS **全部 100% 成功、零错误**；唯一退化信号是 `unresolved_sessions` 2 → 13 → 30。**不能据此定任何对外容量值** | 见 §4 |
| **⑤ A4 Wave 2 落地** | ✅ 新建 `testbed/e2e/test_s1_replay_contract.py`（3 条），`pytest -m e2e` 由 5 条 → **8 条**；连续多轮全绿；缺 native 时 **8 failed / 0 skipped** | 见 §5 |
| **最终门禁** | ✅ `make gate` 与 `make gate-native` 均 exit 0，**1100 passed / 2 skipped / 214 deselected**；根守卫 `uv run pytest tests/ -q` → **131 passed** | 见 §7 |

---

## 1. 更正一：没有「容器动作需授权」这条规矩

上一轮我把维护者对**一条具体命令**的授权（`deploy/kind` promtool 等价容器命令，2026-10-10 §0.2 第 2 项）
错误泛化为**一类动作的禁令**。核对后：

| 事实 | 位置 |
|---|---|
| 2026-10-11 infra bootstrap **实际执行了** `docker create` + `docker cp`（从 quay.io 官方镜像提取 promtool） | [`2026-10-11-local-infra-bootstrap-execution-record.md`](2026-10-11-local-infra-bootstrap-execution-record.md) §4.3 |
| 同上，实际执行了 `docker pull kindest/node:v1.31.0`（1.49 GB）与 `kind create cluster --name as-m5` | 同上 §4.5 / §6 |
| 唯一写「须先确认」的是**不可逆动作**：删除 kind 集群 | 同上 §11 |
| `AGENT.md` 中**没有**任何关于 docker / 容器的通用授权条款 | 全文件检索 |

结论：起 compose PostgreSQL 跑 integration 层，是 `make test-integration-compose` 这个**仓库自带 target 的设计目的**，
且可逆（`docker compose down`）。**上一轮不做是我的划界错误，不是受阻。**

---

## 2. integration 层补齐

### 2.1 起 compose PostgreSQL

```bash
# compose 需要 .env；仓库自带 .env.example 的 dev-only 默认值即与 DSN 匹配
cp deploy/compose/.env.example deploy/compose/.env     # 该文件被 .gitignore:44 忽略
docker compose -f deploy/compose/compose.yml up -d postgres
# 注：首次走 compose 时镜像源返回 502；改用 docker pull postgres:12.22 直接拉全后重试成功
# 结果：as-m4b8-dev-postgres-1 / postgres:12.22 / 监听 55432 / wal_level=replica
```

### 2.2 逐档补齐的实测结果

| 配置 | 命令 | 结果 | 三元组 |
|---|---|---|---|
| PG 12.22 `wal_level=replica`，**无** Redis | `make test-integration-compose` | **196 passed / 5 skipped / 0 failed / 0 error**，exit 0 | `(已验证, .../PASS-integration-compose-2026-10-12.txt, 2026-10-12)` |
| 同上 **+ Redis** | `make test-integration-compose` | **198 passed / 3 skipped**，exit 0 | `(已验证, .../PASS-integration-compose-redis-2026-10-12.txt, 2026-10-12)` |
| PG 12.22 **`wal_level=logical`** + Redis（自定义 DSN `:55433`） | `AS_PG_TEST_DSN=... uv run pytest -m integration -q` | **200 passed / 1 skipped**，exit 0 | `(已验证, .../PASS-integration-pg-logical-2026-10-12.txt, 2026-10-12)` |
| PG **15.18** `wal_level=logical` + Redis（自定义 DSN `:55434`） | 同上 | **1 failed / 124 passed / 76 errors**，exit 1 | `(失败, .../FAIL-integration-pg15-2026-10-12.txt, 2026-10-12)` |

**最终 1 条 skip 的成因**：`test_postgres_audit_store_integration.py:947`
「schema publication coverage requires PostgreSQL 15 or newer (current server_version_num=120022)」
—— 即**标准 compose 环境（PG 12.22）下必然 skip**，不是缺陷。

**偏差说明（后两档）**：第 3、4 档偏离了标准 `make test-integration-compose`
（改用自定义 `AS_PG_TEST_DSN` 指向我另起的容器），目的是消除 `wal_level` 与 PG 版本两处 skip。
第 4 档的 PG15 容器复用了 `deploy/compose/postgres/init` 初始化脚本（只读挂载），
**未修改 `deploy/` 任何文件**。

### 2.3 新发现：PG 15 下的 `AmbiguousFunction`（未修，登记）

```
psycopg.errors.AmbiguousFunction: operator is not unique: "char" || unknown
LINE 1: SELECT defaclobjtype || ':' || defaclrole::text FROM pg_catalog.pg_default_acl ...
HINT:  Could not choose a best candidate operator. You might need to add explicit type casts.
```

- **影响面**：77 处（76 errors + 1 failed 同源），全部在 `services/config-service` 的 Postgres 集成测试。
- **根因**：PostgreSQL **14** 起 `pg_default_acl.defaclobjtype` 的类型由 `char` 改为 `"char"`，
  与 `||` 操作符的组合产生歧义，需显式类型转换。
- **为什么当前不阻塞**：仓库标准环境是 `deploy/compose/compose.yml` 明写的 **postgres:12.22**。
- **为什么值得登记**：PostgreSQL **12 已于 2024-11 EOL**。这与 D1（Python 3.10 EOL）是**同类问题** ——
  标准环境跑在已 EOL 的依赖上，一旦升级 PG 就会踩到。
- **本次处置**：**未改任何产品代码**（属产品代码改动，需 requirement → ADR → design → review 全流程）。
  仅如实落 `FAIL-` 证据并在此登记，**是否立项修复由维护者决定**。

---

## 3. native 构建可复现性验证（B4 / G1 建议的第一步）

**为什么先做这一步**：B4（Python 3.12 spike）的裁决只定了处置选择，并写明「是否与 W0 native build 绑定执行未裁决」。
我的建议是**不并入**，理由是若把一次 Python minor 迁移绑进**首次** native 构建，
「首次真栈门禁是否成立」与「3.12 是否可用」两个结论会互相污染、无法分别归因。
该建议的前置动作就是先证明「native 构建本身可重建」——否则无从归因。

**方法**：用**独立缓存目录**从零重建，不破坏既有可用构建。

```bash
export PKG_CONFIG_PATH="$PWD/.cache/native-deps/usr/lib/x86_64-linux-gnu/pkgconfig"
export CMAKE_PREFIX_PATH="$PWD/.cache/native-deps/usr"
export CPLUS_INCLUDE_PATH="$PWD/.cache/native-deps/usr/include"
export C_INCLUDE_PATH="$PWD/.cache/native-deps/usr/include"
export AS_RESIP_CACHE_ROOT="$PWD/.cache/m2-repro-check"

make m2-native-restore            # exit 0（vendor sha256 校验 + 源码提取到新目录）
make m2-native-build              # exit 0（reSIProcate + resip_probe 从零编译）
make m2-platform-resip-build      # exit 0
make gate-native                  # exit 0，1100 passed / 2 skipped / 211 deselected
```

**结果：native 构建可重建，且新路径下的产物可用。**

**两处实测坑（记录以免重踩）**

1. **漏 `restore` 会 fail-closed**：直接跑 `make m2-native-build` 会因新缓存目录无源码而报错
   `reSIProcate source not found ... run: m2-native.sh restore`。这正是 `make m2-native`
   （restore → build → smoke）存在的原因；脚本的错误提示是有效的。
2. **`AS_RESIP_CACHE_ROOT` 残留会让产物指错路径**：验证完成后我在同一 shell 里重跑
   `make m2-platform-resip-build`，RPATH 仍指向 `.cache/m2-repro-check` —— 一是**环境变量残留**
   （复用 shell 时 `export` 仍在），二是 **cmake 已缓存** `-DCMAKE_BUILD_RPATH`（删掉 `build/` 才重新生效）。
   最终处理：`unset` 环境变量 → 删 `platform/native/*/build/` → 重建 → 用 `readelf -d` 确认
   RUNPATH 回到 `.cache/m2-resiprocate/build`，再跑 `make gate-native` 确认 exit 0。

**给 B4 的结论**：native 构建已证明可重建，因此 3.12 spike 可以**单独一次改动**进行，
任何失败都能干净归因到 3.12，不会与「首次构建本就不稳」混淆。

---

## 4. O1 饱和点探测（B1 建议第二步）

**背景**：维护者表示 O1 取值「不能随便给个数」。我的建议是**不凭空给数**，而是先补一个不依赖外部的事实。
落盘位置：[`../plan.md`](../plan.md) §5.1 表下方的「O1 口径建议（2026-10-12 追加）」段。

**探测配置**（一次性脚本置于 `/tmp`，**不入库**，命令序列全文见本节以便复现）：

```bash
uv run python platform/tests/fixtures/load_uas_runtime.py   # 取 RESIP_RUNTIME_LISTENING udp_port
uv run python -m as_load --host 127.0.0.1 --port "$PORT" \
    --cps "$CPS" --duration 15 --hold 0 --workers "$W" --timeout 5 \
    --stack as-platform-resip-runtime --stack-version 1.14.0-632e215c --out "$OUT"
```

**实测结果**（`workers = max(4, cps/5)`，每档 15 s）：

| CPS | workers | planned | established | peak | unresolved | errors |
|---|---|---|---|---|---|---|
| 20 | 4 | 300 | 300 | 2 | 0 | 0 |
| 40 | 8 | 600 | 600 | 2 | 0 | 0 |
| 80 | 16 | 1200 | 1200 | 2 | 0 | 0 |
| 160 | 32 | 2400 | 2400 | 2 | 0 | 0 |
| 320 | 64 | 4800 | 4800 | 2 | 0 | 0 |
| 640 | 128 | 9600 | 9600 | 13 | 0 | 0 |
| 1280 | 256 | 19200 | 19200 | 30 | 0 | 0 |

**结论（三条，均不得反向夸大）**

1. **在 20 → 1280 CPS 区间内未观察到饱和点**：`established == planned`、零 error。
   饱和点（若存在）**在 1280 CPS 之上，不在本次可测范围内**。
2. **唯一可观测的退化信号**是 `unresolved_sessions`：≤320 CPS 时为 2，640 时 13，1280 时 30。
   它是**会话未及时收敛**的计数上升，可作为后续工程关注的候选指标，但**不是失败率**。
3. **本结果不能支撑任何对外容量值**。模型为 **loopback UDP + accept-all UAS + `hold=0`**，
   无真实网络路径、无 S-SBC、被叫侧不做业务处理、会话生命周期极短、单进程无多副本。

**对 B1 的实际作用**：它把「内部工程目标」的**下限基线**从 M6 的「CPS 20 / 并发 1200」抬到
「**本机 loopback 模型下 CPS 1280 无失败**」——但这仍是**下限**，不是目标值，更不是承诺值。
对外承诺值仍须留到有 S-SBC 路径与真实集群多副本测量之后。
**本次未落任何容量取值 / HPA 阈值 / 容量类告警**；G5 裁决句「在 M6 证据与维护者决策前，不落容量取值」继续有效。

---

## 5. A4 Wave 2 落地

### 5.1 更正二：Wave 2 是已落盘裁决，不是我自行划的界

上一轮我把它说成「不是 blocker、是我自己划的界」，**这个说法是错的**。原文：

> | **G2 / A4-3** | Wave 2 的 14 条回放用例后置到独立 issue | 本迭代仅登记为 gap；本任务**不创建 issue**。 |
> —— [`2026-10-10-unfinished-assessment-and-next-plan.md`](2026-10-10-unfinished-assessment-and-next-plan.md) §0-A.6（`:57`）

register §2 **P5** 闭合的只是「**载体缺失**」这一 gap（以仓内 doc 替代 issue），并明写
「用例实现本身仍属 A4 e2e 批次……**待 Wave 1 完成后启动**」。

**准确状态**：裁决已就位（后置）、载体已就位（[`../acceptance/2026-10-11-wave2-replay-register.md`](../acceptance/2026-10-11-wave2-replay-register.md)）、
**启动前提已满足**（Wave 1 于 2026-10-11 落地）。缺的是**「是否启动 A4 下一批次」的授权**，
维护者 2026-10-12 已授权。本节的工作是**执行该授权**，不推翻 A4-3 裁决。

### 5.2 落地内容

新建 **`testbed/e2e/test_s1_replay_contract.py`**（3 条 e2e 用例），按载体 §3 的对拍定义：

| 用例 | 断言 |
|---|---|
| `test_e2e_s1_replay_both_legs_match_the_normalised_baseline` | 入腿与出腿的**归一化**消息序列与 `S1-basic-call` 基准骨架一致：各为 `INVITE → 200 → ACK → BYE → 200`（1xx 按「最终响应码序列」口径丢弃）。请求与响应**分列断言**：二者在 bridge 内走不同代码路径，交错顺序是时序相关的，不能固化 |
| `test_e2e_s1_replay_second_leg_starts_a_new_call_id` | **C_in ≠ C_out**（REQ-F-2 子集）：入腿 INVITE 的 Call-ID 与出腿 INVITE 的 Call-ID **无交集** |
| `test_e2e_s1_replay_sdp_offer_is_byte_identical_across_legs` | **REQ-F-4**：出腿 INVITE 的 body 与入腿 INVITE 的 body **逐字节相等**（本次**纳入**，未单列 follow-up） |

**采集方式（如实说明代价）**：观测点是 AS 两侧的 `TransparentBridge`（`north` = 入腿 / trunk 侧，
`south` = 出腿 / core 侧）；在**测试模块内**用 `monkeypatch` 包装 `_on_message`（收该腿请求）与
`_forward_response`（收该腿响应）。**产品代码与 `as_simulators` 一个字节未改**；
代价是本用例依赖**私有 API**，bridge 内部改名会导致本文件失效。

**三个实现取舍（避免写出 flaky 断言）**

1. **patch 必须在 bridge 构造之前**安装 —— `SipServer` 在 `TransparentBridge.__init__` 里就绑定了
   `self._on_message`，实例构造后再 patch 类属性无效。（首次实现踩了这个坑，表现为「采集到 0 条」。）
2. **不假设「一通呼叫」**：负载窗口内的呼叫条数是时序相关的，故按 **Call-ID 分组**，
   对**每一通完整呼叫**断言骨架，且要求至少一通。
3. **按 SIP 事务（CSeq）折叠重传**：初版断言被 200 OK 的重传打成 `(200, 200, 200, 200)`；
   按 CSeq 去重后回到基准的 `(200, 200)`。

### 5.3 实测

```
uv run pytest -m e2e -q                          → 8 passed, 1308 deselected   （Wave 1 的 5 条 + Wave 2 的 3 条）
uv run pytest testbed/e2e/test_s1_replay_contract.py -q  → 3 passed            （连续 4 次稳定）
临时移走 _resip_runtime*.so 后 uv run pytest -m e2e -q  → 8 failed, 0 skipped   （A4-2 成立）
```

### 5.4 回写（按载体 §5 的约定）

- [`../acceptance/2026-10-11-wave2-replay-register.md`](../acceptance/2026-10-11-wave2-replay-register.md)
  已**追加** §6「实现结果回写」。
- [`../acceptance/test-plan.md`](../acceptance/test-plan.md) REQ-F-1 状态已按 e2e 计划 Wave 2 完成标准
  改为「**自动化子集已覆盖 / 全文仍 open**」并链到用例名；**所有 `- [ ]` 一项未打勾**
  （14 条逐条 header 对拍仍 open）。
- [`../acceptance/2026-10-09-e2e-test-plan.md`](../acceptance/2026-10-09-e2e-test-plan.md) 已追加 Wave 2 状态更正。

**边界**：Wave 2 的定义本身即**归一化骨架**对拍，**不含** 14 条逐条 header、
不含 100/180 临时响应序列、不含 Via branch 模式、不含 Route 消费。
**不签收 REQ-F-1 全文，不签收 REQ-F-2 / REQ-F-4，不签收任何里程碑。**

---

## 6. 落盘清单（本轮改动的文件）

| 文件 | 性质 |
|---|---|
| `testbed/e2e/test_s1_replay_contract.py` | **新建**（A4 Wave 2，3 条 e2e） |
| `docs/handoff/2026-10-12-o1-and-native-reproducibility.md` | **新建**（本文） |
| `docs/acceptance/artifacts/m5/2026-10-12/*.txt` | **新建**（8 个证据文件，含 1 个 `FAIL-`） |
| `docs/plan.md` | 追加：§5.1 表下「O1 口径建议」段 + §0 决策记录表 1 行 |
| `docs/acceptance/test-plan.md` | 追加：REQ-F-1「自动化覆盖状态」段（勾选未动） |
| `docs/acceptance/2026-10-11-wave2-replay-register.md` | 追加：§6 实现结果回写 |
| `docs/acceptance/2026-10-09-e2e-test-plan.md` | 追加：Wave 2 状态更正 |
| `docs/acceptance/artifacts/m5/README.md` | 追加：2026-10-12 证据索引行 |
| `docs/handoff/2026-10-10-unfinished-assessment-and-next-plan.md` | 追加：§11.7 / §11.8 / §10.3 B4 排期补充 |

---

## 7. 最终门禁与证据

| 检查 | 结果 |
|---|---|
| `make gate`（ruff format --check / ruff check / mypy / `-m "unit or contract"`） | exit 0，**1100 passed / 2 skipped / 214 deselected**；2 条 SKIPPED 均来自 `test_derived_baseline.py:245` / `:279`（S1-basic-call 未构造 Route / Record-Route header，需专门的 M2 probe capture），**无一条**来自 native 缺失 |
| `make gate-native` | exit 0，同上计数 |
| `uv run pytest -m e2e -q` | **8 passed, 1308 deselected** |
| `uv run pytest tests/ -q`（根守卫） | **131 passed** |
| `uv run ruff check .` | `All checks passed!` |

三元组：

- `(已验证, docs/acceptance/artifacts/m5/2026-10-12/PASS-integration-compose-2026-10-12.txt, 2026-10-12)`
- `(已验证, docs/acceptance/artifacts/m5/2026-10-12/PASS-integration-compose-redis-2026-10-12.txt, 2026-10-12)`
- `(已验证, docs/acceptance/artifacts/m5/2026-10-12/PASS-integration-pg-logical-2026-10-12.txt, 2026-10-12)`
- `(失败, docs/acceptance/artifacts/m5/2026-10-12/FAIL-integration-pg15-2026-10-12.txt, 2026-10-12)`

---

## 8. 本机容器与目录状态（未清理，供维护者决定）

本轮为跑 integration 与探测而起的容器**全部保留未删**（删除属不可逆动作，不擅自执行）：

| 容器 | 镜像 | 端口 | 用途 |
|---|---|---|---|
| `as-m4b8-dev-postgres-1`（compose） | postgres:12.22（→ `wal_level=replica`） | 55432 | 标准 `make test-integration-compose` |
| `as-redis-test` | redis:7-alpine | 6379 | 消除 2 条 Redis skip |
| `as-pg-logical-test` | postgres:12.22，`-c wal_level=logical` | 55433 | 消除 3 条 publication skip |
| `as-pg15-test` | postgres:15-alpine，`-c wal_level=logical` | 55434 | PG15 兼容性探测（产出 `FAIL-` 证据） |
| `as-m5-control-plane`（kind，上一轮保留） | kindest/node:v1.31.0 | — | 上一轮 infra bootstrap |
| `as-pg-test`（上一轮之前遗留，Exited） | postgres:16-alpine | 无端口映射 | 非本轮所起，未动 |

另：`deploy/compose/.env` 由 `.env.example` 复制而来（`.gitignore:44` 忽略，不入库），
内容为仓库自带的 dev-only 默认值；`.cache/m2-repro-check/` 为可复现性验证的临时缓存（`.cache/` 被忽略）。

---

**落盘日期：2026-10-12。状态：已执行，待维护者评审。**
（证据索引：[`../acceptance/artifacts/m5/README.md`](../acceptance/artifacts/m5/README.md)；
环境登记：[`../environments.md`](../environments.md)。）
