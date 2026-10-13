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

# 执行记录：infra 本机安装（helm / kubectl / kind / promtool）

> **状态：已执行，待维护者评审；不签收任何 REQ / 里程碑。**
> 本文是 [`2026-10-11-local-infra-bootstrap-plan.md`](2026-10-11-local-infra-bootstrap-plan.md) 的执行记录，
> 按该计划 §7 第 6 项落盘，逐条写「命令 / 实际输出（关键行）/ 结论」。计划原文未回填。
> 执行环境：已登记环境 **`dev-win03ib7niepf0`**（host `WIN-03IB7NIEPF0`，Ubuntu 22.04.5 LTS / WSL2 / x86_64，
> 用户 `shudong`，全程无 root）。执行日期：2026-10-11（本机时区）。
>
> **本记录不签收任何 REQ、任何里程碑、任何 M5 / M8 关门条件**；全部改动未提交，
> commit 的切分与执行由维护者决定。

## 0. 结论速览

| 项 | 结果 |
|---|---|
| 四件工具就位 | ✅ helm 3.16.4 / kubectl 1.31.4 / kind 0.24.0 / promtool 2.55.1，均在 `tools/bin/`（gitignored，不入库） |
| `make chart-check` 本机复跑 | ✅ exit 0，末行 `chart-check: OK` |
| `make alert-check` 本机复跑 | ✅ exit 0，`SUCCESS: 10 rules found`（3 组 10 条，与历史证据同版本 promtool 2.55.1） |
| kind 集群 `as-m5` | ✅ 已创建，context `kind-as-m5` 校验 OK |
| 集群级产品验证 | ❌ **未做**：`M5_STRICT=1 m5-verify` 在新建空集群上如实 FAIL（exit=1，无产品 AS pod），不据此宣称集群级验证通过 |
| 脚本修复 | ✅ `tools/bootstrap-infra.sh` 解压路径 bug 已修（见 §3），**未提交** |
| 网络偏差 | GitHub 对象出口长时间 0 字节、dl.k8s.io 单流限速 ~20KB/s；kubectl / promtool / kind 使用了回退取径，每个回退的溯源与校验见 §5 / §10 |

## 1. 前置条件核查（计划 §2，8 项全过）

| # | 查什么 | 命令 | 实际输出（关键行） | 结论 |
|---|---|---|---|---|
| 1 | docker daemon | `docker info` | `Server Version: 29.2.1` / `Operating System: Ubuntu 22.04.5 LTS`，exit 0 | ✅ 硬闸门通过 |
| 2 | docker 客户端位置 | `command -v docker` | `/usr/bin/docker` | ✅ |
| 3 | sudo | `sudo -n true 2>/dev/null && echo yes \|\| echo no` | `no` | ✅ 全程未用 root |
| 4 | 当前用户 | `id -un` | `shudong`（非 root） | ✅ |
| 5 | CPU 架构 | `uname -m` | `x86_64` | ✅ |
| 6 | 可用磁盘 | `df -h . \| tail -1` | `1007G 95G 861G 10% /` | ✅（远超 2 GB） |
| 7 | 是否 WSL | `grep -qi microsoft /proc/version && echo WSL \|\| echo native` | `WSL`（内核 `6.18.40.1-microsoft-standard-WSL2`） | ✅ WSL2 可用 |
| 8 | 下载器 | `command -v curl` | `/usr/bin/curl` | ✅ |

## 2. env-probe 前后对照

**执行前**（主 agent 当日早前实测）：docker / uv / python3.10 / make / git 为 ✅，
helm / kubectl / kind / promtool 四项 ❌ —— 未找到（tools/bin 与 PATH 均无），无一项「⚠ 装了但不可用」。

**执行后**（本记录撰写时 fresh 实跑 `tools/env-probe.sh`，exit 0）：

```
✅ 具备  docker      /usr/bin/docker                Docker version 29.2.1, build a5c7197
✅ 具备  uv          /home/shudong/.local/bin/uv    uv 0.12.15 (x86_64-unknown-linux-gnu)
✅ 具备  python3.10  /usr/bin/python3.10            Python 3.10.12
✅ 具备  helm        tools/bin/helm                 v3.16.4+g7877b45
✅ 具备  kubectl     tools/bin/kubectl              clientVersion:
✅ 具备  kind        tools/bin/kind                 kind v0.24.0 go1.22.10 linux/amd64
✅ 具备  promtool    tools/bin/promtool             promtool, version 2.55.1 (branch: HEAD, revision: 6d7569…
✅ 具备  make        /usr/bin/make                  GNU Make 4.3
✅ 具备  git         /usr/bin/git                   git version 2.34.1
✅ 具备：docker, uv, python3.10, helm, kubectl, kind, promtool, make, git
❌ 缺失：（无）
⚠ 装了但不可用：（无）
```

结论：计划 §6.1 三条检查全部满足（四件齐全、版本与 `tools/VERSIONS` 逐字一致、无「装了但不可用」）。
说明：kubectl 行的 `clientVersion:` 是 env-probe 对 kubectl 用 `version --client=true -o yaml` 取 YAML 首行的
显示形式；锁定版本由直跑确认：

```
tools/bin/kubectl version --client=true
→ Client Version: v1.31.4 / Kustomize Version: v5.4.2
```

## 3. 执行中发现的脚本 bug 与修复（未提交）

**现象**：首轮 `tools/bootstrap-infra.sh` 实装时 helm / promtool 解压后报
`archive did not contain linux-amd64/helm` 类错误，安装失败。

**根因**：`install_from_tarball` 的调用方把**压缩包内部路径**当作 `inner` 传入，同时又传
`--strip-components=1`，解压后该路径已不存在，存在性检查必然失败。

**修复**（已在工作树，`git diff tools/bootstrap-infra.sh` 可核对；`bash -n` 通过，`--dry-run` 输出不变）：

- helm 调用点：`inner` 由 `"${HOST_OS}-${GOARCH}/helm"` 改为 `"helm"`；
- promtool 调用点：`inner` 由 `"prometheus-${PROMETHEUS_VERSION}.${PLAT}/promtool"` 改为 `"promtool"`；
- `install_from_tarball` 定义上方补 2 行注释：`inner` 是**应用 strip-components 之后**、相对解压根的路径，
  不是压缩包内部完整路径。

**状态**：该修复与本次全部文档改动一样**未提交**，等待维护者决定 commit 拆分。

## 4. 安装经过（逐工具，含偏差与溯源）

统一方式按计划 §3：官方制品装入 `tools/bin/`，无 root。**安装顺序 helm → kubectl → promtool → kind**，
前一轮中断/中止各一次（见 §10），最终以一次完整重跑收口。

### 4.1 helm 3.16.4 —— 官方 tarball，正常路径

```
来源：https://get.helm.sh/helm-v3.16.4-linux-amd64.tar.gz（计划 §3.2 原始 URL）
tools/bin/helm version --short → v3.16.4+g7877b45
```

结论：✅ 按计划路径装成，无偏差。当时 `HELM_SHA256` 尚为空，脚本按设计打「未校验安装」警告；
官方 sha256 已于本轮回填 `tools/VERSIONS` 供日后强制校验。

### 4.2 kubectl 1.31.4 —— 官方 URL + 并行分段下载（偏差：传输方式，非来源）

```
偏差原因：GitHub/Fastly 出口被限速至约 20KB/s，脚本单流下载两次停滞（其中一次导致整轮中断）。
取径：同一官方 URL（https://dl.k8s.io/release/v1.31.4/bin/linux/amd64/kubectl）改用并行分段（HTTP Range）下载。
校验：官方 https://dl.k8s.io/release/v1.31.4/bin/linux/amd64/kubectl.sha256
      = 298e19e9c6c17199011404278f0ff8168a7eca4217edad9097af577023a5620f，与安装文件比对 → 一致（match OK）。
复验（本记录撰写时）：
      sha256sum tools/bin/kubectl
      → 298e19e9c6c17199011404278f0ff8168a7eca4217edad9097af577023a5620f  tools/bin/kubectl（逐字一致）
tools/bin/kubectl version --client=true → Client Version: v1.31.4
```

结论：✅ 来源是官方 URL 原件，sha256 官方值强制比对通过；**仅传输方式偏离脚本的单流实现**，
该值已锁定进 `tools/VERSIONS` 的 `KUBECTL_SHA256`。

### 4.3 promtool 2.55.1 —— 官方 quay.io 镜像提取（偏差：来源载体）

```
偏差原因：GitHub release tarball 出口当日约 1 小时完全无数据（0 字节），多波重试全部失败。
取径：官方镜像 quay.io/prometheus/prometheus:v2.55.1
      （digest quay.io/prometheus/prometheus@sha256:2659f4c2ebb718e7695cb9b25ffa7d6be64db013daba13e05c875451cf51b0d3）
      经 docker create + docker cp 提取 promtool 二进制。
tools/bin/promtool --version → promtool, version 2.55.1 (branch: HEAD, revision: 6d7569113f1ca814f1e149f74176656540043b8d)
```

结论：✅ 版本与锁定值 2.55.1 逐字一致；**溯源是官方镜像（digest 如上），不是 release tarball**。
tarball 的官方 sha256（`19700bdd42ec31ee162e4079ebda4cd0a44432df4daa637141bdbea4b1cd8927`，取自官方
sha256sums.txt）已锁定进 `tools/VERSIONS` 并加注说明，供日后 tarball 安装强制校验。
该二进制与 2026-10-05 历史 alert 证据**同版本**，满足计划 §3.2「同一版本才可比」的要求。

### 4.4 kind 0.24.0 —— 官方 tag 源码本机构建（偏差：非 release 二进制）

```
偏差原因：GitHub release 二进制不可达（同 §4.3 的出口故障）。
取径：go install sigs.k8s.io/kind@v0.24.0（官方 tag 源码），
      GOPROXY=https://goproxy.cn,direct（模块完整性经 sumdb 校验，经代理不放行未校验模块）。
工具链：go1.22.10，其 tarball 来自 mirrors.aliyun.com/golang，
      sha256 = 736ce492a19d756a92719a6121226087ccd91b652ed5caec40ad6dbfb2252092（go1.22.10.linux-amd64.tar.gz 官方值）。
tools/bin/kind version → kind v0.24.0 go1.22.10 linux/amd64
```

结论：✅ 是 pinned v0.24.0 的**源码构建**，不是 release 二进制；kind 官方**不发布** sha256，
`tools/VERSIONS` 的 `KIND_SHA256` 保持留空并已加注说明。

### 4.5 kind 节点镜像

```
kindest/node:v1.31.0，1.49GB，自 docker hub 预拉；
digest sha256:25a3504b2b340954595fa7a6ed1575ef2edadf5abd83c0776a4308b64bf47c93（docker images --digests 实录）
```

## 5. bootstrap 最终运行与验证

中断的中间轮之后，最终一次完整重跑：

```
tools/bootstrap-infra.sh
→ 退出码 0；verify 段四行 OK（helm / kubectl / kind / promtool 全部命中锁定版本）；
  随后自动调用 tools/env-probe.sh，九项 ✅、❌（无）、⚠（无）（见 §2）。
```

`tools/bootstrap-infra.sh --dry-run` 在修复后亦重跑过：四条 URL 正常打印、exit 0、不下载任何东西。

## 6. 交付质量与集群级验证（计划 §6.2–§6.4）

| 检查 | 命令 | 实际输出（关键行） | 结论 |
|---|---|---|---|
| chart-check | `export PATH="$PWD/tools/bin:$PATH"; make chart-check` | exit 0；末行 `chart-check: OK`；`1 chart(s) linted, 0 chart(s) failed`；`[INFO] Fail:` 两行属 fail-closed 预期断言 | ✅ 计划 §6.2 达成 |
| alert-check | `make alert-check` | exit 0；`SUCCESS: 10 rules found`（N=10 > 5，覆盖 as.call-path 5 + as.runtime 3 + as.platform 2） | ✅ 计划 §6.3（P4 核心）达成，且为与 2026-10-05 证据**同版本**的本地 promtool 2.55.1 |
| kind 集群 | `kind create cluster --name as-m5 --wait 120s` | exit 0（节点镜像见 §4.5） | ✅ |
| context | `kubectl config get-contexts -o name \| grep -qx kind-as-m5 && echo "context OK"` | 打印 `context OK` | ✅ 计划 §6.4 达成 |

**集群级产品验证未做**：`M5_STRICT=1 bash deploy/kind/m5-verify.sh` 在新建 `as-m5` 集群上 **exit=1** ——
集群只有空控制面，`No resources found in as-m5 namespace.`（产品 AS pod 未部署），jsonpath 断言越界。
这是**如实失败**，不是通过证据：印证计划 §7「装齐工具不等于集群级验证已通过」。集群未删除，留给后续授权的部署验证。

## 7. 证据采集脚本运行结果（deploy/kind/m5-record-artifacts.sh）

```
export PATH="$PWD/tools/bin:$PATH"
bash deploy/kind/m5-record-artifacts.sh
→ 脚本最终退出码 1（因含一项如实 FAIL，见下）；产物落 docs/acceptance/artifacts/m5/2026-10-11/
```

| 采集项 | 退出码 | 产物 |
|---|---|---|
| gate | 0 | `PASS-gate-2026-10-11.txt`（`1037 passed, 10 skipped, 206 deselected`，**含 SKIPPED 项**）与 `PASS-gate-sample-2026-10-11.txt` |
| chart-check | 0 | `PASS-chart-check-2026-10-11.txt` / `PASS-chart-check-sample-2026-10-11.txt` |
| alert-check | 0 | `PASS-alert-check-2026-10-11.txt`（`SUCCESS: 10 rules found`）/ `PASS-alert-check-sample-2026-10-11.txt` |
| m5-strict-context | 0（context 在位） | `FAILCLOSED-m5-strict-context-2026-10-11.txt` —— 按采集脚本设计**一律**记 FAILCLOSED，永不作为通过证据 |
| m5-verify-strict | **1** | `FAIL-m5-verify-strict-2026-10-11.txt` / `FAIL-m5-verify-strict-sample-2026-10-11.txt` —— **如实失败**，原因见 §6 |

产物三元组（索引与判读见 [`../acceptance/artifacts/m5/README.md`](../acceptance/artifacts/m5/README.md)）：

- `(已验证, docs/acceptance/artifacts/m5/2026-10-11/PASS-gate-2026-10-11.txt, 2026-10-11)`
- `(已验证, docs/acceptance/artifacts/m5/2026-10-11/PASS-chart-check-2026-10-11.txt, 2026-10-11)`
- `(已验证, docs/acceptance/artifacts/m5/2026-10-11/PASS-alert-check-2026-10-11.txt, 2026-10-11)`
- `(失败, docs/acceptance/artifacts/m5/2026-10-11/FAIL-m5-verify-strict-2026-10-11.txt, 2026-10-11)`
- `FAILCLOSED-m5-strict-context-2026-10-11.txt` 不是通过证据，不以三元组引用。

## 8. 产物落盘后的全量自检（计划 §6.6）

```
uv run pytest tests/ -q   → 94 passed in 0.41s（exit 0）
uv run ruff check .       → All checks passed!（exit 0）
```

证据纪律守卫接受了全部新产物与文档改动（守卫用例数随批次增长，76 → 94 为不同 session 的实测事实，
与 register §7.5 落盘说明的 62 / 68 / 76 同理不冲突）。

## 9. 版本固定回写（计划 §7 第 5 项）

`tools/VERSIONS`：`HELM_SHA256` / `KUBECTL_SHA256` / `PROMETHEUS_SHA256` 已填官方值，
`KIND_SHA256` 保持留空（官方不发布）；kubectl 值已与实际安装文件逐字比对一致（§4.2）；
prometheus 值为 release tarball 口径并加注本机二进制的镜像溯源；kind 加注源码构建口径。
**版本号一律未动。**

## 10. 偏差汇总（对照计划 §3.2 的原始取径）

**网络退化背景（如实记录）**：2026-10-11 约 22:00–23:05+（本机时区），GitHub 对象出口降到 0 字节
（多波并行/串行重试全部失败）；docker 的 daocloud 镜像源在该时间窗的部分时段 502；
dl.k8s.io 单流被限速约 20KB/s（并行分段可用）。**回退取径仅在官方 URL 不可达时使用**，
每个回退的溯源与校验如下：

| 工具 | 计划 §3.2 取径 | 实际取径 | 偏差性质 | 溯源校验 |
|---|---|---|---|---|
| helm | 官方 tarball | 官方 tarball（不变） | 无 | 版本串 `v3.16.4+g7877b45`；官方 sha256 已回填待日后校验 |
| kubectl | 官方单流下载 | **同一官方 URL**，并行分段传输 | 仅传输方式 | 官方 `.sha256` 与安装文件逐字一致（§4.2，本记录撰写时复验仍一致） |
| promtool | GitHub release tarball | 官方 quay.io 镜像提取 | 来源载体 | 镜像 digest 已记录（§4.3）；tarball 官方 sha256 已回填 `tools/VERSIONS` 供日后强制校验 |
| kind | 官方 release 二进制 | 官方 tag 源码本机构建 | 构建方式 | 版本串含 `v0.24.0`；go 工具链 tarball sha256 为官方值；模块经 sumdb 校验 |

其余执行面偏差：

- 首轮 bootstrap 在 kubectl 下载停滞处被中断，另有一次中间轮中止；收口以最终一次完整重跑为准（exit 0）。
- 采集脚本随附的 `m5-verify-strict` 采集超出计划 §6.2–§6.4 的授权清单，属脚本在「集群在位」时的既有行为；
  其 FAIL 结果如实落盘并已上报（§6 / §7），未做任何补救性改名。

## 11. 范围外 / 未做事项

- **`deploy/` 一个字节未动**（chart / alerts / kind 脚本均在授权范围外）。
- **未做任何 git 写操作**：未 `commit` / `add` / `push` / `tag` / 建分支 / 改 remote；
  `tools/bootstrap-infra.sh` 的修复与全部文档改动停留在工作树，等待维护者评审与 commit 拆分。
- **未签收任何 REQ / 里程碑**；P4 的既有闭合（docker-based，2026-10-11）未被重开，
  本次只是追加同版本本地复验注（见 register §7.5 追加更正，待维护者评审）。
- 执行过程中的 `parl2` 后台循环是当次排障用的实验性辅助手段，已停止，从未进入仓库任何文件。
- kind 集群 `as-m5` **保留未删**（集群级部署验证待另行授权）；删除属不可逆动作，须先确认（计划 §8.4）。

---

**落盘日期：2026-10-11。状态：已执行，待维护者评审。**
（对应计划：[`2026-10-11-local-infra-bootstrap-plan.md`](2026-10-11-local-infra-bootstrap-plan.md)；
环境登记：[`../environments.md`](../environments.md) §2 / §2.1；证据索引：
[`../acceptance/artifacts/m5/README.md`](../acceptance/artifacts/m5/README.md)。）
