# 环境登记（Environments）

> **本文是长期事实登记，不是会话交接件。** 它不会随某次 session 结束而失效，也不会被下一次
> 工作覆盖重写 —— 机器、工具、产出的证据都是仓库的长期属性。
>
> **本文引用环境必须使用表中的「环境名」；禁止再写匿名的「本机」。**
> 依据与批准记录：[`handoff/2026-10-11-open-adjudication-register.md`](handoff/2026-10-11-open-adjudication-register.md) §7.4 第 2 层。

## 0. 口径（维护者 2026-10-11 立场，先读这一段）

> **项目会部署到不同电脑。环境差异是常态，不是缺陷，也不是缺陷的证据。**
> 本仓库的工作跨多台机器、多个 session 进行；任何一条结论如果只在某一台机器上成立，
> 就必须写清它在哪台机器上成立 —— 这正是本文存在的理由。

由此产生三条硬口径：

1. **任何文档不得依赖某台机器的能力。** 判定「项目能不能做 X」时，依据只能是仓库里的资产与
   证据，不是一台机器的 `PATH`。
2. **不得以「某台机器没有 X」推断「项目没有 X」。** 单台机器的工具清单是**这台机器的事实**，
   不是**项目的能力**。2026-10-05 的 chart / alert 证据由一台具备完整 infra 工具、但从未被
   命名的机器产出；而 2026-10-10 落盘的一句匿名的工具否认被读成了「项目无 promtool 能力」。
   **这类混淆的代价是整个里程碑被反复重新讨论。**
3. **本文的环境信息不由人工维护**，由 [`../tools/env-probe.sh`](../tools/env-probe.sh)
   **现场探测生成**（见 §3）。人工填 hostname 的做法已取消：手工表格一定漂移，漂移之后又会被
   当成事实读回去。**不需要人工查 hostname** —— 脚本自己探测。

## 1. 为什么必须有名（背景，不重复论证）

2026-10-05 的 M5 证据文件（chart-check / alert-check）记录的路径是
`==> helm lint /home/shudong/project/3rdparty-as/deploy/helm` —— **同一用户名、同一项目路径**；
而 2026-10-11 实测的工作站上**没有** helm / kubectl / kind / promtool。

⇒ 证据由**另一台机器**产出，而文档中匿名的「本机」实际指代**两台不同的机器**。
这是「项目到底有没有 infra 能力」这一问反复重新争论的直接原因：**事实载体没有元数据**。
给环境起名字，就是给事实载体加元数据。

## 2. 环境登记表

> 本表**只登记已实测的机器**。无法填写的一律**不占位** —— 不写「待填写」行：空占位会被读者
> 读成「有一台机器，只是没人填」，比不写更糟。未测量的机器，等它第一次运行
> [`../tools/env-probe.sh`](../tools/env-probe.sh) 时再进来。

| 环境名 | hostname | 具备工具 | 缺失工具 | 已在此产出的证据 | 备注 |
|---|---|---|---|---|---|
| `dev-win03ib7niepf0` | `WIN-03IB7NIEPF0` | `docker`（`/usr/bin/docker` 29.2.1）、`uv`（`/home/shudong/.local/bin/uv` 0.12.15）、`python3.10`（`/usr/bin/python3.10` 3.10.12）、`helm`（`tools/bin/helm` v3.16.4+g7877b45）、`kubectl`（`tools/bin/kubectl` v1.31.4）、`kind`（`tools/bin/kind` v0.24.0 go1.22.10）、`promtool`（`tools/bin/promtool` 2.55.1）、`make`（`/usr/bin/make` 4.3）、`git`（`/usr/bin/git` 2.34.1）—— 后四件于 2026-10-11 由 `tools/bootstrap-infra.sh` 装入 `tools/bin/`（不入库），bootstrap 后 `tools/env-probe.sh` 实测九项全 ✅ | （无）—— ❌ 缺失与 ⚠ 装了但不可用均为（无）（2026-10-11 bootstrap 后实测；此前 helm / kubectl / kind / promtool 四项曾为「未找到」，见 §2.1 旧数据行） | `docs/reviews/product-packaging-execution-record-2026-10-10.md:132`（`preflight.sh --dry-run` 行为与退出码）；`docs/plan.md` §0 记的 config-service PostgreSQL integration（2026-10-03，本地 PG 12.22）；`docs/acceptance/artifacts/m5/2026-10-11/`（2026-10-11 本机复跑 gate / chart-check / alert-check 各 PASS-，另有 FAILCLOSED-m5-strict-context 与如实 FAIL 的 FAIL-m5-verify-strict，采集与判读见 [`acceptance/artifacts/m5/README.md`](acceptance/artifacts/m5/README.md)） | 当前工作站 / 日常开发环境；OS `Ubuntu 22.04.5 LTS`、架构 `x86_64`。`uv` 位于 `/home/shudong/.local/bin/uv`。**2026-10-11 bootstrap 前**不能运行 `make chart-check` / `make alert-check` / 任何 kind 集群级验证（历史结论保留为审计链）；**2026-10-11 bootstrap 后**三项均可本机运行 —— chart-check / alert-check 已当日复跑通过，kind 集群 `as-m5` 已创建、context `kind-as-m5` 校验 OK；**集群级产品验证未做**（m5-verify-strict 如实 FAIL）。工具安装经过与偏差见 [`handoff/2026-10-11-local-infra-bootstrap-execution-record.md`](handoff/2026-10-11-local-infra-bootstrap-execution-record.md) |

> **本行由 2026-10-11 实测写入；后续请用 `tools/env-probe.sh` 重新生成，不要手工编辑本行。**
> 本行是本轮实测真值，本次未改动。补齐 helm / kubectl / kind / promtool 的执行计划见
> [`handoff/2026-10-11-local-infra-bootstrap-plan.md`](handoff/2026-10-11-local-infra-bootstrap-plan.md)。
>
> **2026-10-11 追加（重贴）：** 上方「本次未改动」记录的是**首次落盘那一轮**——那一轮里探测脚本**跑不起来**
> （`tr` 参数报错），本行与 §2.1 的数据行是**手工写的**。脚本修复后已在本机实跑
> `bash tools/env-probe.sh --markdown`（退出码 0），本行已按**该次真实输出**重贴。
> 上方「后续请用 `tools/env-probe.sh` 重新生成、不要手工编辑本行」的说明**不变、仍然有效**：
> 下次工具清单变化就重跑脚本整段粘贴，不要手工编辑。

> **2026-10-11 追加（infra bootstrap 后重贴；上文原样保留，不删改；待维护者评审）：**
> [`handoff/2026-10-11-local-infra-bootstrap-plan.md`](handoff/2026-10-11-local-infra-bootstrap-plan.md) 已执行完毕，
> 本行「具备工具 / 缺失工具 / 已在此产出的证据 / 备注」四栏已按 bootstrap 后 fresh `tools/env-probe.sh` 输出**整行重贴**：
> helm / kubectl / kind / promtool 四项由「未找到」变为 ✅ 具备（路径 `tools/bin/`，不入库），缺失工具栏为（无）。
> 「已在此产出的证据」与「备注」的历史记载**保留未删，只做追加**。kubectl 的版本号 v1.31.4 来自直跑
> `tools/bin/kubectl version --client=true`（`Client Version: v1.31.4`）与 `tools/bootstrap-infra.sh` 校验段；
> env-probe 判定依据列显示 `clientVersion:` 是其 `version --client=true -o yaml` 取首行的显示形式（见 §2.1 注），
> 非版本缺失。执行记录：[`handoff/2026-10-11-local-infra-bootstrap-execution-record.md`](handoff/2026-10-11-local-infra-bootstrap-execution-record.md)。

### 2.1 逐工具实测矩阵（由 `tools/env-probe.sh --markdown` 生成）

本表的列与 [`../tools/env-probe.sh`](../tools/env-probe.sh) `--markdown` 输出**逐列对应**，整段粘贴即可。
「环境名」列按 **`<角色>-<hostname 小写去分隔符>`** 生成，**默认角色 `dev`**（规则见 §3 第 4 条）。
本轮**未落盘数据行**：脚本是本轮新建的，本次会话只写脚本、不执行，数据行必须由执行者现场生成，
**不得手工补写**。

**2026-10-11 补记（上一段记录的是「首次落盘那一轮」的状况）：** 脚本修复后已在本机实跑
`bash tools/env-probe.sh --markdown`（退出码 0），下表数据行 = 该次真实输出**整段粘贴**，非手工补写。
脚本没输出的一律不补写：本轮四列缺失工具都由脚本判为「未找到」，**没有任何一格需要填「未探测」**。

| 环境名 | hostname | OS | 架构 | docker | uv | python3.10 | helm | kubectl | kind | promtool | make | git |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `dev-win03ib7niepf0` | `WIN-03IB7NIEPF0` | Ubuntu 22.04.5 LTS | x86_64 | ✅ `/usr/bin/docker` Docker version 29.2.1, build a5c7197 | ✅ `/home/shudong/.local/bin/uv` uv 0.12.15 (x86_64-unknown-linux-gnu) | ✅ `/usr/bin/python3.10` Python 3.10.12 | ❌ — 未找到（tools/bin 与 PATH 均无） | ❌ — 未找到（tools/bin 与 PATH 均无） | ❌ — 未找到（tools/bin 与 PATH 均无） | ❌ — 未找到（tools/bin 与 PATH 均无） | ✅ `/usr/bin/make` GNU Make 4.3 | ✅ `/usr/bin/git` git version 2.34.1 |

**2026-10-11 补记（infra bootstrap 后；上行保留为 bootstrap 前真值，不删改；待维护者评审）：**
[`handoff/2026-10-11-local-infra-bootstrap-plan.md`](handoff/2026-10-11-local-infra-bootstrap-plan.md) 已执行完毕，
四件 infra 工具装入 `tools/bin/`（不入库）。下表数据行 = bootstrap 后 fresh
`bash tools/env-probe.sh --markdown`（退出码 0）输出**整段粘贴**（表头 + 分隔行 + 数据行），非手工补写：

| 环境名 | hostname | OS | 架构 | docker | uv | python3.10 | helm | kubectl | kind | promtool | make | git |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `dev-win03ib7niepf0` | `WIN-03IB7NIEPF0` | Ubuntu 22.04.5 LTS | x86_64 | ✅ `/usr/bin/docker` Docker version 29.2.1, build a5c7197 | ✅ `/home/shudong/.local/bin/uv` uv 0.12.15 (x86_64-unknown-linux-gnu) | ✅ `/usr/bin/python3.10` Python 3.10.12 | ✅ `/home/shudong/project/3rdparty-as/tools/bin/helm` v3.16.4+g7877b45 | ✅ `/home/shudong/project/3rdparty-as/tools/bin/kubectl` clientVersion: | ✅ `/home/shudong/project/3rdparty-as/tools/bin/kind` kind v0.24.0 go1.22.10 linux/amd64 | ✅ `/home/shudong/project/3rdparty-as/tools/bin/promtool` promtool, version 2.55.1 (branch: HEAD, revision: 6d7569 | ✅ `/usr/bin/make` GNU Make 4.3 | ✅ `/usr/bin/git` git version 2.34.1 |

> **kubectl 格说明（`clientVersion:` 是脚本输出原文，非手工补写）：** env-probe 对 kubectl 探测命令为
> `version --client=true -o yaml`，判定依据列显示的是 YAML 首行 `clientVersion:` 原样输出；锁定版本
> v1.31.4 由直跑 `tools/bin/kubectl version --client=true`（`Client Version: v1.31.4`）、
> `tools/bootstrap-infra.sh` 校验段（exit 0）与安装文件 sha256 官方值逐字比对一致三重确认。
> 本轮 plain 输出末尾：❌ 缺失：（无）；⚠ 装了但不可用：（无）。

**三种状态的读法（脚本按此区分，勿混为一谈）：**

| 记号 | 含义 | 判据 |
|---|---|---|
| ✅ 具备 | 工具可解析**且**版本命令成功 | 有路径 + 有版本号 |
| ❌ 缺失 | 解析不到可执行文件 | `tools/bin/` 与 `PATH` 均无 |
| ⚠ 装了但不可用 | 二进制存在但跑不通 | 版本命令非零退出，或退出 0 却无输出 |

> **「装了但不可用」是本轮新识别的易混淆点**：装了 ≠ 能用。把它算进「具备」，等于用一个
> 跑不起来的二进制去支撑一条「已验证」结论 —— 与「文件名即结论」同源，都是让载体撒谎。

### 2.2 尚未归属的证据（不得默认归给任一环境）

| 证据文件 | 状态 |
|---|---|
| `docs/acceptance/artifacts/m5/2026-10-05/PASS-gate-2026-10-05.txt` / `PASS-gate-sample-2026-10-05.txt` | 产出环境**未登记**。同一批次入库，但本文只对 chart / alert 两份有路径证据（`helm lint` 绝对路径），gate 那两份无同类线索，故不推定 |
| `docs/acceptance/artifacts/m5/2026-10-05/FAILCLOSED-m5-strict-context-2026-10-05.txt` | 产出环境**未登记**；内容为 fail-closed 记录（`exit=1`），**不是通过证据** |

### 2.3 待校验项（执行前先在本文登记执行环境）

- **P4 的 promtool 校验**：2026-10-10 新增的 `as.runtime` / `as.platform` 两组告警规则至今未被任何
  已登记环境校验过（需运行 `promtool check rules`，**本次未运行**）。执行前应先在本文登记执行环境。

> **2026-10-11 收尾轮追加更正（上方 P4 条目原文保留，不删改）：** P4 已由已登记环境
> **`dev-win03ib7niepf0`**（host `WIN-03IB7NIEPF0`）以 **docker 容器化方式**完成校验 ——
> 容器镜像 `prom/prometheus:v2.45.0` 内的 promtool 对 `deploy/alerts/as-alerts.yaml` 执行
> `check rules`，输出 `SUCCESS: 10 rules found`（as.call-path 5 + as.runtime 3 + as.platform 2，共 3 组），
> 主 agent 同日同 host 同命令独立复跑 exit=0。
> 三元组：**(已验证, docs/acceptance/artifacts/m5/2026-10-11/PASS-alert-check-full-2026-10-11.txt, 2026-10-11)**。
> **与工具矩阵的关系（二者不矛盾）：** 该环境 PATH 中**仍无本地 promtool 二进制**，
> §2 / §2.1 工具矩阵的 promtool 格**维持 env-probe 实测「❌ — 未找到」不变**（矩阵行由
> `tools/env-probe.sh` 生成，**不得手改**）；容器化 promtool 校验不改变 PATH 事实 —— 缺本地二进制
> 与「能用 docker 跑容器内 promtool」同时成立。
> **不影响其余待执行项：** 本地工具安装计划
> [`handoff/2026-10-11-local-infra-bootstrap-plan.md`](handoff/2026-10-11-local-infra-bootstrap-plan.md)
> 的其余目标（helm / kubectl / kind 本地就位、chart-check 本机复跑、kind 集群证据）**不受 P4 闭合影响，
> 仍按该计划待执行 / 待授权**。

> **2026-10-11 追加（infra bootstrap 轮；上方 P4 docker 闭合注原文保留，不删改；待维护者评审）：**
> 本地 promtool **2.55.1** 现已就位（`tools/bin/promtool`，与 2026-10-05 历史 alert 证据**同版本**；
> 二进制溯源为官方镜像 `quay.io/prometheus/prometheus@sha256:2659f4c2ebb718e7695cb9b25ffa7d6be64db013daba13e05c875451cf51b0d3`
> 提取，见执行记录），`make alert-check` 已在本机（环境 `dev-win03ib7niepf0`）复跑：
> `promtool check rules` → **`SUCCESS: 10 rules found`**（as.call-path 5 + as.runtime 3 + as.platform 2，共 3 组）。
> 三元组：**(已验证, docs/acceptance/artifacts/m5/2026-10-11/PASS-alert-check-2026-10-11.txt, 2026-10-11)**。
> 本注**升级** P4 的证据基座（docker 容器化 prometheus v2.45.0 → 与历史证据同版本的本地 promtool 2.55.1），
> **不改变** P4 已闭合的裁决本身；状态维持「已关闭」，本追加待维护者评审。
> 执行记录：[`handoff/2026-10-11-local-infra-bootstrap-execution-record.md`](handoff/2026-10-11-local-infra-bootstrap-execution-record.md)。

## 3. 如何新增 / 更新一行（不需要人工查 hostname）

1. 在目标机器上进入仓库根目录，运行：

   ```bash
   tools/env-probe.sh              # 人看的表格：三种状态一目了然
   tools/env-probe.sh --markdown   # 直接粘进 §2.1 的表格行
   ```

   两个命令都是**只读**的：不安装任何东西、不改系统状态、不需要 root，可重复执行。
   缺工具时退出码仍是 0 —— **缺工具是常态，不是脚本失败**。

2. 把 `--markdown` 的输出**整段**（表头 + 分隔行 + 数据行）粘进 §2.1。
   本表已有表头与分隔行，粘贴时保持列序不变。

3. 同步更新 §2 登记表对应行。首次出现的环境按「**追加一行**」处理，不改动既有行。

4. **命名规则：`<角色>-<hostname 小写去分隔符>`，默认角色 `dev`。**
   `WIN-03IB7NIEPF0` → `dev-win03ib7niepf0`，与 §2 既有行一致 —— 维护者 2026-10-11 裁决：
   **角色作前缀**。换角色用 `--role`（`tools/env-probe.sh --role infra` → `infra-win03ib7niepf0`）；
   完全覆盖环境名用 `--name`（`tools/env-probe.sh --name my-env`）。
   **登记表以名字为键，不以生成规则为键** —— 改名等于换环境，须经维护者确认。

5. **照实写缺失项。** 缺 helm 就写缺 helm；「装了但版本命令报错」必须记成
   ⚠ 装了但不可用，不能记成具备。**不得**因为一台机器缺工具就去推论「项目缺能力」。

## 4. 引用规范：状态声明三元组

**凡写「已验证 / 未验证」，一律写成三元组 `(结论, 证据文件, 日期)`，不允许裸句。**

| | 示例 | 说明 |
|---|---|---|
| ✅ 正向 | `(已验证, docs/acceptance/artifacts/m5/2026-10-05/PASS-chart-check-2026-10-05.txt, 2026-10-05)` | 结论、证据文件、日期三者齐备，读者可自行打开核对 |
| ❌ 反例 | 「chart-check 通过」 | **禁止** —— 未说明在哪台机器跑的，读者无法判断该结论可否在当前环境复现，正是 2026-10-11 之前反复返工的根因 |

补充约定：

- **三件容易被误读的事**（`FAILCLOSED-` 文件不是通过证据、chart-check 的 `[INFO] Fail:` 属预期断言、
  `PASS-gate-*.txt` 含 SKIPPED 项）见
  [`acceptance/artifacts/m5/README.md`](acceptance/artifacts/m5/README.md)。
- **本目录内 `Fail` / `ERROR` 字样属正常语义，不得据此判定文件失败；一律以文件名前缀为准。**
- 机器能力之外的**项目**能力不由本文裁决；交付边界见
  [`handoff/2026-10-11-open-adjudication-register.md`](handoff/2026-10-11-open-adjudication-register.md) §7.1。

## 5. 安全边界

**本文不含任何凭据、token、地址**（`AGENT.md` §11 / §13）：不写密码、证书私钥、token、DSN、
cookie，也不写真实 IP / 域名 / registry 地址。工具路径只写到解释能力所必需的程度；
`tools/env-probe.sh` 的输出同样受此约束 —— 它只打印工具路径、版本与机器标识，
**不打印任何环境变量**。证据文件同样受此约束，见 `acceptance/artifacts/m5/README.md` 末行。

## 6. 维护约定

- **环境信息由脚本生成，不由人工填写**（§0 第 3 条）。人工登记表已被取消。
- 新增环境 = **追加一行**，不改动既有行；**hostname 不得为空字符串，也不得留占位符**。
  本表不写「待填写」行：写不出 hostname 就说明这台机器还没被探测过。
- 工具增减必须带**实测日期**；「大概有」不构成登记。
- 守卫：[`../tests/test_evidence_discipline.py`](../tests/test_evidence_discipline.py) 强制
  `tools/env-probe.sh` 存在且可执行、本文不得再出现空 hostname 占位、本文必须链到该脚本。
- 本表与 [`architecture/README.md`](architecture/README.md) 的证据分级、
  [`handoff/2026-10-11-open-adjudication-register.md`](handoff/2026-10-11-open-adjudication-register.md) §7.4
  构成第 2 层机制，回归由 `tests/test_evidence_discipline.py` 守卫。

**落盘日期：2026-10-11。状态：已落盘，待维护者评审。**
（2026-10-11 变更：删除无法填写的 infra 占位行；环境信息改为由 `tools/env-probe.sh` 现场探测生成；
新增 §0 口径段、§2.1 逐工具矩阵、§3 更新步骤。`dev-win03ib7niepf0` 一行为实测真值，未改动。
同日：`tools/env-probe.sh` 的默认命名规则由「角色作后缀」改为「**角色作前缀**，默认角色 `dev`」，
与既有行一致；`--role` / `--name` 的语义不变。依据：维护者 2026-10-11 裁决。）
**2026-10-11 第三次变更（按真实输出重贴）：** 上文「`dev-win03ib7niepf0` 一行为实测真值，未改动」记录的是
**首次落盘那一轮**——那一轮探测脚本跑不起来，该行是手工写的。脚本修复后本机实跑
`bash tools/env-probe.sh --markdown`（退出码 0），§2 登记表行与 §2.1 矩阵数据行已按该次真实输出重贴
（新增 `make` / `git` 两列实测值、OS 与架构；`helm` / `kubectl` / `kind` / `promtool` 四项确认均为「未找到」）。
版本号一律来自脚本输出，未手工补写任何一格。§2.1 原「本轮未落盘数据行」的说明按审计链要求**保留未删**，
其后的补记说明现状。§0 口径、§3 命名规则、§4 三元组、§5 安全边界、§6 维护约定均未改动。
