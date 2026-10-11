# 执行计划：infra 本机安装（helm / kubectl / kind / promtool）

> **落盘日期：2026-10-11。状态：已落盘，待维护者评审。本计划尚未执行。**
>
> **本文是给下一个 session 执行的计划，不是执行记录。** 它不依赖任何对话上下文：
> 从第 2 节照做即可。执行完请另写执行记录，不要把执行结果回填成本文的「已完成」。

## 0. 为什么要做这件事

2026-10-11 的实测结论：本机（`WIN-03IB7NIEPF0`）具备 `docker` / `uv` / `python3.10`，
**不具备** `helm` / `kubectl` / `kind` / `promtool`。因此本机**不能**运行
`make chart-check`、`make alert-check`，也不能做任何 kind 集群级验证。

而 2026-10-05 的 chart / alert 证据是由**另一台机器**产出的（证据里记着
`==> helm lint /home/shudong/project/3rdparty-as/deploy/helm`，同一用户名、同一项目路径），
那台机器具备上述全部四件工具，**但它的身份至今未知、也无法补填**。

后果不是「少几个工具」，而是两条：

1. **`deploy/alerts/` 属交付产品**（[`../architecture/README.md`](../architecture/README.md) §2 判定线），
   其 `as.runtime` / `as.platform` 两组新规则**至今没被任何机器用 promtool 校验过**
   （register §7.5 的 P4）。交付质量校验悬空，责任无处可落。
2. 「项目到底有没有 infra 能力」被反复重新讨论。病根已裁定为**事实载体没有元数据**
   （register §7.4），本计划是该结论的落地动作之一。

## 1. 目标与范围

### 1.1 目标

在**本机**具备 `helm` / `kubectl` / `kind` / `promtool`，使下列验证可在本机运行：

| 目标 | 现状 | 达成后的判定依据 |
|---|---|---|
| `make chart-check` | 本机不可运行 | 末行 `chart-check: OK` |
| `make alert-check` | 本机不可运行 | 末行 `SUCCESS: N rules found`（N 覆盖新增两组） |
| kind 集群级验证（`make m5-cluster-evidence` 等） | 本机不可运行 | 集群起来且脚本 exit 0 |

### 1.2 范围边界（先读这段，可以省掉很多返工）

- **kind / testbed 是脚手架，不得用于客户生产。** 判定线见
  [`../architecture/README.md`](../architecture/README.md) §2；既有落地见
  [`../delivery/install-guide.md`](../delivery/install-guide.md) `:19`、`:91`。
  本计划装出来的 kind 集群只用于**我们自己的**验证，产出的 transcript 属证据分级第 ② 类
  （对外履约依据，**不是客户验收项**）。
- 本计划**不改变任何交付物**：`deploy/helm/`、`deploy/alerts/` 一个字节都不动。
  本计划只往**这台机器**上装工具。
- 本计划**不解决**「2026-10-05 那台机器是谁」。那件事已判定为**无法回填**（见 §8.5）。

## 2. 第 0 步：前置条件核查（先跑，装之前）

> **在装任何东西之前先跑完这一节。** 其中第 1 项是硬闸门。

| # | 查什么 | 命令 | 期望输出 | 不满足时 |
|---|---|---|---|---|
| 1 | **docker daemon 是否真的在跑** | `docker info` | 打印 Server 段（`Containers:` / `Server Version:` 等），exit 0 | **本计划在此中止**（见下方硬闸门） |
| 2 | docker 客户端位置 | `command -v docker` | `/usr/bin/docker`（本机已知） | 先解决 docker 本身，与本计划无关 |
| 3 | 是否有 sudo | `sudo -n true 2>/dev/null && echo yes \|\| echo no` | `yes` 或 `no` 均可 | 本计划**全程不需要 root**；`no` 不影响执行 |
| 4 | 当前用户 | `id -un` | 非 root 更佳 | root 下也能跑，但请改用普通用户执行 |
| 5 | CPU 架构 | `uname -m` | `x86_64` 或 `aarch64` | 其它架构需手工装，`bootstrap-infra.sh` 会明确报错退出 |
| 6 | 可用磁盘 | `df -h . \| tail -1` | 至少 2 GB 可用 | 清理后重试；kind 拉镜像会再吃 1–2 GB |
| 7 | 是否 WSL | `grep -qi microsoft /proc/version && echo WSL \|\| echo native` | `native` 或 `WSL` | WSL2 可用 kind（需 systemd 或手动起 dockerd）；WSL1 **不可用**，中止 |
| 8 | 下载器 | `command -v curl \|\| command -v wget` | 至少一个存在 | 两个都没有则中止，先解决 |

### 硬闸门（原文写死，不得绕过）

> **若 `docker info` 不通（daemon 没起来 / 未安装 / 无权限），kind 一律装不了，本计划在此中止。**
>
> 这不是「先装上再说」的情况：kind 创建集群靠的就是 docker daemon。daemon 不通时装好的
> kind 只是一个跑不起来的二进制，会制造「工具已具备」的假象 —— 那正是本轮要消灭的那类混淆。
>
> 此时**允许**做的事只有一件：把 helm / kubectl / promtool 装上（它们与 docker 无关），
> 在执行记录里写明「kind 因 docker daemon 不可用未安装」，并且**不得**在任何文档里把本机
> 登记成具备 kind。

## 3. 安装清单

**统一方式：解压官方 tarball / 单文件到 `tools/bin/`，无需 root，与仓库同生命周期。**

### 3.1 为什么不首选 apt

| 理由 | 说明 |
|---|---|
| 需要 root | 本项目任何步骤都不应依赖 sudo；root 步骤会成为「下次还会不会记得」的隐患 |
| 版本不受控 | apt 给的是发行版当时打包的版本，仓库里没有任何地方记着它是哪个版本 ⇒ 同一份告警规则在两台机器上被两个 promtool 校验出不同结论，事后不可复现 |
| 生命周期错位 | 发行版包装在 checkout 之外，`git clean -xfd` 清不掉，也不会出现在 `git status` 里；工具与仓库同生共死才是本项目要的形态 |
| 供应链不可见 | tarball 有官方 sha256，可写进 `tools/VERSIONS` 强制校验；apt 的来源对本文不可见 |

**apt 不是错的，只是不该是默认。** 若日后维护者裁定用 apt，本计划的 §5 版本固定策略必须同步改写。

### 3.2 清单

| 工具 | 建议版本 | 官方来源 | 安装位置 | 校验命令 | 期望 |
|---|---|---|---|---|---|
| `helm` | `3.16.4` | `https://get.helm.sh/helm-v3.16.4-linux-amd64.tar.gz` | `tools/bin/helm` | `tools/bin/helm version --short` | `v3.16.4+…` |
| `kubectl` | `1.31.4` | `https://dl.k8s.io/release/v1.31.4/bin/linux/amd64/kubectl` | `tools/bin/kubectl` | `tools/bin/kubectl version --client=true` | `Client Version: v1.31.4` |
| `kind` | `0.24.0` | `https://kind.sigs.k8s.io/dl/v0.24.0/kind-linux-amd64` | `tools/bin/kind` | `tools/bin/kind version` | `kind v0.24.0 … linux/amd64` |
| `promtool` | `2.55.1`（取自 prometheus tarball） | `https://github.com/prometheus/prometheus/releases/download/v2.55.1/prometheus-2.55.1.linux-amd64.tar.gz` | `tools/bin/promtool` | `tools/bin/promtool --version` | `promtool, version 2.55.1` |

版本取值依据：

- **helm 3.16.4** —— chart 为 `apiVersion: v2`，需要 Helm 3.x
  （[`../delivery/install-guide.md`](../delivery/install-guide.md) 前置条件第 2 项）。
- **kubectl 1.31.4 + kind 0.24.0** —— 二者配套：kind v0.24.0 的默认节点镜像是
  `kindest/node:v1.31.0`，kubectl 与集群的版本偏移要求是 ±1 minor，取同一 minor 最省事。
  `deploy/kind/m5-kind-up.sh` **没有**固定节点镜像，所以 kind 版本就是节点版本来源。
- **promtool 2.55.1** —— **故意不动**。`deploy/kind/m5-record-artifacts.sh` 里的历史 `/tmp`
  兜底路径用的就是 2.55.1；同一版本的 promtool 校验过的证据，语义上才可比。

> 执行前请与官方发布页核对上表版本号。`tools/bootstrap-infra.sh` 的 URL 由
> `tools/VERSIONS` + `uname` 拼出，**不联网校验版本是否存在**；下错版本号会表现为下载 404。

### 3.3 不装 kustomize（判断与理由）

本仓库**没有任何 kustomize 依赖**：

- chart 渲染走 `helm template`（`deploy/helm/scripts/chart-check.sh`、`make chart-check`）；
- `deploy/` 下无 `kustomization.yaml`；
- kind 清单是裸 YAML（`deploy/kind/manifests/`）。

因此 **kustomize 不列入本计划**。若将来引入：`tools/VERSIONS` 加一行，
`tools/bootstrap-infra.sh` 的 `url_for` / `pinned_for` / `checksum_for` 各加一个分支即可。

## 4. 脚本设计

本轮已落盘两个脚本（**本 session 未执行任何一个**，见 §6.0）：

| 脚本 | 职责 | 调用方式 |
|---|---|---|
| [`../../tools/env-probe.sh`](../../tools/env-probe.sh) | **只读**探测：hostname / OS / 架构 + docker / uv / python3.10 / helm / kubectl / kind / promtool / make / git，区分「具备 / 缺失 / **装了但不可用**」三态 | `tools/env-probe.sh`、`--markdown`、`--json`、`--name`、`--role` |
| [`../../tools/bootstrap-infra.sh`](../../tools/bootstrap-infra.sh) | 把四件工具装进 `tools/bin/`：**无 root、幂等、支持 `--dry-run`、装完自动调用 `env-probe.sh` 验证** | `tools/bootstrap-infra.sh [--dry-run] [--only <tool>] [--force]` |

辅助文件：[`../../tools/VERSIONS`](../../tools/VERSIONS)（版本唯一存放处，见 §5）。
`tools/bin/` 已在 `.gitignore` 中：**二进制不入库**。

### 4.1 设计约束（写死，改动需维护者确认）

1. **无 root。** 任何需要 root 的路径必须**显式报错**，绝不允许脚本内部偷偷 `sudo`。
   目录不可写时报「请修权限或设 `TOOLS_BIN=<可写目录>`」并退出。
2. **幂等。** 已在锁定版本 ⇒ 跳过；`--force` 才重装。中途失败后直接重跑即可。
3. **不写仓库以外的地方。** 只写 `tools/bin/` 与 `$TMPDIR`。
4. **缺工具不是失败。** `env-probe.sh` 缺任何工具仍 exit 0 —— 缺工具是常态。
5. **不打印凭据。** 两个脚本都不打印环境变量、token、内网地址（`AGENT.md` §11 / §13）。

### 4.2 执行顺序（下一 session 的实际操作）

```bash
# 0) 前置核查（§2），尤其 docker info
docker info >/dev/null && echo "docker OK"

# 1) 只读探测，先看清现状（安全，可反复跑）
tools/env-probe.sh

# 2) 看安装计划，不下载任何东西
tools/bootstrap-infra.sh --dry-run

# 3) 真正安装（幂等；需要外网）
tools/bootstrap-infra.sh

# 4) 让 make 找得到 promtool / helm（当前 shell 生效）
export PATH="$PWD/tools/bin:$PATH"

# 5) 复验：三态应当全部变成「✅ 具备」
tools/env-probe.sh
```

## 5. 版本固定策略

### 5.1 一处存放

全部版本在 [`../../tools/VERSIONS`](../../tools/VERSIONS)，格式 `TOOL_VERSION=x.y.z`，
可另附 `TOOL_SHA256=`（留空则只打印警告、不阻断安装）。**升级 = 只改这一个文件**，
脚本本身不硬编码版本号。

### 5.2 升级方式

```bash
vim tools/VERSIONS                  # 改版本号，并顺手填上官方 sha256
tools/bootstrap-infra.sh --dry-run   # 确认 URL 变了
tools/bootstrap-infra.sh             # 幂等重跑，只更新变化的那几个
```

### 5.3 与仓库内既有硬编码版本的关系

| 位置 | 硬编码内容 | 本计划如何处理 |
|---|---|---|
| `deploy/kind/m5-record-artifacts.sh` | `/tmp/prometheus-2.55.1.linux-amd64/promtool` 作为**最后兜底** | **保留**（不删历史路径），查找顺序已改为 ① `tools/bin/promtool` → ② `PATH` → ③ `/tmp` 旧路径。三者都没有时 `alert-check` 落 `FAIL-` 产物并写明 promtool 不可用，**不静默跳过** |
| `Makefile:59`（`alert-check`） | 裸 `promtool` | **不改**。装完用 `export PATH="$PWD/tools/bin:$PATH"` 满足它 |
| `deploy/kind/m5-kind-up.sh` | 未固定节点镜像 | **不改**。节点版本随 kind 版本走（§3.2） |
| `deploy/kind/m5-ingress-evidence.sh:30` | ingress-nginx 清单跟随 `main` 分支 | 与本计划无关；属另一条可复现性问题，**本次不处理** |

**约束**：`PROMETHEUS_VERSION` 一旦与 `/tmp` 旧路径的 2.55.1 分叉，
`tools/VERSIONS` 的注释里必须写明「自 X 起 promtool 版本与历史证据不同源，旧证据不可直接对比」。

## 6. 验证步骤（可证伪）

> **没跑出证据就不算装完。** 每一条都必须给出可核对的产物路径。

### 6.0 执行前的已知状态（不得当成已验证）

本 session **只写了脚本、没有执行任何脚本**（受全局约束：shell 脚本除 `bash -n` 语法检查外不执行）。
因此下列两条**尚未被验证过**，下一 session 必须先跑一遍：

```bash
tools/env-probe.sh                  # 期望：docker/uv/python3.10 为 ✅，helm/kubectl/kind/promtool 为 ❌
tools/bootstrap-infra.sh --dry-run   # 期望：四条 url 打印出来，exit 0，不下载任何东西
```

若二者报错，**先修脚本再装工具**，不要绕过。

### 6.1 工具就位

| 检查 | 命令 | 期望 |
|---|---|---|
| 四件齐全 | `tools/env-probe.sh` | helm / kubectl / kind / promtool 四行全为 `✅ 具备` |
| 版本正确 | `tools/env-probe.sh` | 版本号与 `tools/VERSIONS` 逐字一致 |
| 无「装了但不可用」 | 同上 | 「装了但不可用」一栏为（无） |

### 6.2 chart-check（交付产品质量证据）

```bash
export PATH="$PWD/tools/bin:$PATH"
make chart-check
```

- 期望：exit 0，末行 `chart-check: OK`，含 `1 chart(s) linted, 0 chart(s) failed`。
- `[INFO] Fail:` 行属**预期断言**（fail-closed 渲染守卫），不代表失败。
- 产物：`docs/acceptance/artifacts/m5/<日期>/PASS-chart-check-<日期>.txt`
  与 `PASS-chart-check-sample-<日期>.txt`。
- **命名由脚本负责**：直接跑 `bash deploy/kind/m5-record-artifacts.sh` 会自动按退出码分流
  `PASS-` / `FAIL-` 并写明真实退出码；代价是它会先跑 `make gate`（较慢）。
  只想要 chart / alert 两份证据时，可手工执行本节与 §6.3 的命令，再按上述文件名落盘。

### 6.3 alert-check（**P4：本次的核心目标**）

```bash
make alert-check
```

- 期望：exit 0，末行 `SUCCESS: N rules found`，且 **N 必须大于 5** ——
  2026-10-10 新增了 `as.runtime` / `as.platform` 两组，原 5 条未改。
  **`N == 5` 说明这次校验没覆盖到新增组，不足以划掉 P4。**
- 产物：`PASS-alert-check-<日期>.txt` / `PASS-alert-check-sample-<日期>.txt`。
- 记录写法必须是三元组：`(已验证, docs/acceptance/artifacts/m5/<日期>/PASS-alert-check-<日期>.txt, <日期>)`。

### 6.4 kind 集群级验证（**脚手架，不是客户验收项**）

前置：`docker info` 通过（§2 第 1 项）。

```bash
export PATH="$PWD/tools/bin:$PATH"
kind create cluster --name as-m5 --wait 120s
kubectl config get-contexts -o name | grep -qx kind-as-m5 && echo "context OK"
```

- 期望：打印 `context OK`。
- **拉镜像需要外网**；离线环境下 kind 必然失败，不要反复重试（见 §8.2）。
- 产物若落进 `docs/acceptance/**` 或 handoff 记录，属证据分级第 ② 类
  （[`../architecture/README.md`](../architecture/README.md) §3）：**对外履约依据，不是客户验收项**。

### 6.5 产物命名的强制约定

所有 `docs/acceptance/artifacts/**` 下的证据按**文件名即结论**落盘，由
[`../../tests/test_evidence_discipline.py`](../../tests/test_evidence_discipline.py) 守卫：

| 前缀 | 含义 | 是通过证据？ |
|---|---|---|
| `PASS-` | 命令 exit 0 | 是 |
| `FAIL-` | 命令跑了但非零退出 | **不是** |
| `FAILCLOSED-` | 显式拒绝而非猜测 | **不是** |

格式 `<结论>-<被验项>[-sample]-<YYYY-MM-DD>.txt`。
**不得**把失败的运行写成 `PASS-`；守卫会拒绝这种文件名。

### 6.6 全量自检

```bash
uv run pytest tests/ -q        # 证据纪律 + 工作区布局守卫
uv run ruff check .
```

期望：全绿。若 `tests/` 红，多半是产物命名违规（§6.5），**不要改测试去迁就产物**。

## 7. 收尾回写清单

装完之后，以下位置**必须**同步更新（缺一项就等于没做完）：

| # | 位置 | 改什么 |
|---|---|---|
| 1 | [`../environments.md`](../environments.md) §2.1 | 跑 `tools/env-probe.sh --markdown`，把逐工具矩阵的数据行粘进去 |
| 2 | [`../environments.md`](../environments.md) §2 | 登记表「缺失工具」栏去掉已补齐的四项；**保留 `WIN-03IB7NIEPF0` 这行真值** |
| 3 | [`../environments.md`](../environments.md) §2.3 | 勾掉「P4 待校验」，并**注明校验所用环境名** |
| 4 | register §7.5 与 [`../plan.md`](../plan.md) §0 | **P4 状态更新**：写明 `as.runtime` / `as.platform` 已由 promtool 2.55.1 校验，附三元组 `(结论, 证据文件, 日期)` |
| 5 | [`../../tools/VERSIONS`](../../tools/VERSIONS) | 填入四件工具的官方 sha256（若未填，须在执行记录里列为待办） |
| 6 | 新建执行记录 | `docs/handoff/<日期>-local-infra-bootstrap-execution-record.md`，逐条写「命令 / 实际输出 / 结论」 |

> **全部 review record 一律标「待维护者评审」，不得自行签收。**
> 本计划**不签收**任何 REQ、任何里程碑、任何 M5 / M8 关门条件。
> 装齐工具**不等于**「集群级验证已通过」—— 后者要有它自己的证据。

> 环境名按默认规则 **`<角色>-<hostname 小写去分隔符>`** 生成，**默认角色 `dev`**：
> `WIN-03IB7NIEPF0` → `dev-win03ib7niepf0`，与登记表既有行一致（维护者 2026-10-11 裁决：角色作前缀）。
> 要换前缀用 `tools/env-probe.sh --role infra`，要完全覆盖用 `--name`。
> 环境名以**登记表为准**：改名等于换环境，须经维护者确认。

## 8. 风险与回退

### 8.1 分步失败怎么办

| 失败点 | 现象 | 处理 |
|---|---|---|
| 下载失败 | `download failed` | 检查外网 / 代理；`bootstrap-infra.sh` 可重复跑，已装好的自动跳过 |
| 校验和不符 | `checksum mismatch` | **立即停止**。不要用 `--force` 绕过。核对官方发布页；仍不符则上报，**不要**改 `tools/VERSIONS` 去凑 |
| `promtool` 存在但跑不出版本 | 探测显示「装了但不可用」 | 多为解压层级不对；`rm -f tools/bin/promtool` 后 `--only promtool` 重装 |
| `make chart-check` 仍找不到 helm | PATH 未生效 | `export PATH="$PWD/tools/bin:$PATH"`。若需长期生效（写 shell 配置），**先问维护者** —— 改用户环境超出本计划 |
| kind 创建集群超时 | `--wait 120s` 超时 | 多为镜像拉不下来（网络）。见 §8.2。**不要**反复重试 |

### 8.2 docker 镜像拉取的网络前提

`kind create cluster` 需要从公网拉 `kindest/node:v1.31.0`（约 1 GB）。
**无外网或受限时 kind 必然失败**，且失败信息通常是 timeout，容易被误读成「kind 装坏了」。
遇到这种情况：在执行记录里写明「kind 因镜像不可达未验证」，**不得**写「kind 不可用」。
helm / kubectl / promtool 与镜像无关，照常可用。

### 8.3 只回退某一个工具

```bash
rm -f tools/bin/kind && tools/bootstrap-infra.sh --only kind
```

回退 = 删除单个文件 + 幂等重装：不需要 root、不影响其它工具、不产生任何 git 变更。
整体回退：`rm -rf tools/bin`（该目录在 `.gitignore` 中，删除不产生 git 变更）。

### 8.4 哪些动作不可逆

| 动作 | 可逆性 |
|---|---|
| `rm -rf tools/bin` | **可逆**（重装即可） |
| 改 `tools/VERSIONS` 的版本号 | 可逆，但**已产出的证据随之失去可比性** —— 证据里记录的是当时的版本。改版本前先想清楚 |
| `kind delete cluster --name as-m5` | **不可逆**：集群里的运行态数据全部消失。本计划不删集群；要删先确认 |
| `kind create cluster` 拉取的镜像 | 占磁盘（1–2 GB），删集群不一定回收镜像 |
| 修改 `deploy/` 下任何文件 | **不在本计划授权范围内**（见 §9） |

### 8.5 无法回退 / 无法解决的事项

- **2026-10-05 那台机器的身份**：已判定**无法回填**（维护者 2026-10-11）。
  不要为了「让登记表好看」去猜一个 hostname 填进去 —— 那是本轮明令禁止的空占位回潮。
  该批证据的归属保持「未登记」，见 [`../environments.md`](../environments.md) §2.2。

## 9. 停止线

**本计划不授权以下任何一项。执行中发现需要越过，停下并上报维护者：**

| 不授权 | 说明 |
|---|---|
| `git push` / `git tag` / 建分支 / 改 remote | 未经维护者在**当次对话**中明确批准，绝不做 |
| 改根 `VERSION` 或 `deploy/helm/Chart.yaml` | 版本口径（G4/A6）仍待裁决 |
| 把 kind 集群证据当**客户验收项** | M5「控制面集群部署证明」已裁定为**对外履约依据，不是客户验收项**（register §7.3） |
| 签收任何 REQ / 里程碑 | 一律标「待维护者评审」 |
| 改 `deploy/alerts/` 以让 promtool 通过 | 告警规则若校验失败，是**要修的缺陷**，不是要改的规则 |
| 用 `sudo` 绕过权限问题 | 脚本会显式报错；绕过脚本的 sudo 等于让本计划的「无 root」承诺失效 |
| 为「让 gate 变绿」而放宽守卫测试 | 守卫红 = 产物或环境不合规，应修产物/环境，不应改守卫 |

**遇上下表任一情形，立即停止并在执行记录中写明「已停下 + 原因 + 需要谁裁决」：**
需要越过停止线、需要 root、需要改交付物、发现计划与仓库实际状态不符。

---

**本计划未执行任何安装动作**：本 session 未运行 `tools/env-probe.sh`、未运行
`tools/bootstrap-infra.sh`、未下载任何 tarball、未创建任何 kind 集群、未执行任何 `make` target。
**落盘日期：2026-10-11。状态：已落盘，待维护者评审。**

