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

# R2612 目录结构评审 v3（逐目录：干什么用 / 里面有什么 / 是否该在根目录）

> **状态：分析结论，待维护者裁决**。本版按维护者要求改为逐目录三段式：每个目录先讲清它是干什么的、里面实际装了什么，再回答"是否应该放在根目录"。**覆盖并替代 v2 分析版**；v2 的 F-1（apps 改名建议）在本版被修订，见 §4。
> **v3.1 增补（2026-10-28）**：新增 §1——维护者追问"apps/、services/、platform/ 都是产品源码，docs/ 是文档入口，为什么四个目录在同一级"，§1 是该问题的书面回答，并新增发现 F-9 与裁决项 Q6。
> **v3.2 增补（2026-10-29）**：新增 §3——对其余五个目录（testbed / tests / deploy / scripts / tools）做同等力度判断，含三组组织张力与两处 v3 结论修正；新增发现 F-10、裁决项 Q7。
> 证据采集：2026-10-28，全部来自对仓库文件系统、git 索引和 README/AGENT.md/plan.md 原文的直接检查。
> **编号命名空间声明**：本文的 **F-1…F-10 是"结构发现"编号**（本文件局部使用），与 `docs/plan.md` §0 / `R2612_Cont.md` 的需求编号 **REQ-F-9 等同名不同义**，互不引用。
> 关联：[R2612_Cont.md](./R2612_Cont.md)（剩余项规划）。

---

## 0. 判断标准：什么叫"配占根目录一个位置"

一个目录配在根目录占一个位置，当且仅当：

1. **架构一等构件**——被构建、部署或门禁直接引用，删掉它产品就不成立；
2. **稳定的心智地图地位**——业务开发、平台开发、测试、运维、交付这些不同角色都会高频进入它；
3. **与兄弟目录构成完整分层**——九个目录合起来等于：内核 + 业务 + 控制面 + 测试器械 + 结构守卫 + 部署产物 + 文档 + 两类工具，彼此不重叠、也没有空洞；
4. 反面清单（不配占根目录的）：一次性脚本、临时文档、某个目录的子集、只服务单一角色的杂物——这些该收进子目录。

下面逐目录过这三问。

## 1. 根目录的组织原则：为什么产品源码与 docs/ 同级

**维护者的追问（2026-10-28）**：apps/、services/、platform/ 都是 product 的部分源码，docs/ 是整个产品的文档入口——为什么这四个目录在同一级？

**回答分三层**：

1. **根目录的组织原则是"一个关注点一个入口"，不是"源码 vs 非源码"二分。** 九个目录 = 九个关注点：产品源码三层（内核 platform / 业务 apps / 控制面 services）、测试两件事（器械 testbed / 结构守卫 tests）、交付产物 deploy、文档入口 docs、两类工具（工作流 scripts / 工具链 tools）。docs 与源码同级是 OSS 通行做法——Linux kernel、CPython、Go、rustc 都把 docs/（或 Doc/）与源码目录并列在根。
2. **三个源码目录刻意平铺，因为它们不是"一坨源码"，是三条有依赖方向的架构层。** 本项目的核心设计是"内核承载业务包"：apps → platform（业务用例通过 `decide()` 接缝接入内核）、services → platform（控制面进程）、apps 之间互斥、产品包禁依赖 testbed。这个分层不是纸面说法——`tests/test_workspace_layout.py` 明文校验 workspace 成员恰好落进 kernel / apps / services / testbed 四类，`tests/test_layer_boundaries.py` 从 pyproject 依赖声明机器推导边界。**平铺的根目录 = 把架构图放在第一眼**（AGENT.md §4 的分层图与根目录一一对应）；收拢进一个父目录会把分层藏深一层，且给最常改动的路径加深一级。
3. **追问指出的真实缺口（新发现 F-9）**：这个组织原则**没有被声明出来**。根 README 的目录树只列了名字，没有一句话说明"platform / apps / services 是产品源码三层、其余是支撑件"——所以外人看不出哪三个是产品，"同级"看起来像偶然而不是原则。修法很轻：根 README 加一张分类地图（产品源码 = platform/apps/services；测试 = testbed/tests；交付 = deploy；文档 = docs；工具 = tools/scripts）。

**另一个流派的存在（诚实陈述）**：PostgreSQL 把全部源码收在 `src/` 下、`doc/` 在根——"产品 vs 支撑"的视觉二分同样是正经做法，不是错误答案。选择依据是工具链与规模：本项目只有 3 个源码目录、7 个成员，`src/` 收拢要动根 pyproject workspace 声明、两个门禁测试、Dockerfile COPY 路径、约数十处文档引用（ADR / AGENT.md / README 的目录树与分层图），换来的是根目录少两个条目 + 视觉二分。

**本版建议**：维持平铺，把组织原则写进根 README（F-9 的修法）。`src/` 收拢列为可选项，由维护者裁决（§5 Q6）。

**（2026-10-29 裁决更新）**：维护者选 Q6=B——引入 `src/` 收拢产品源码。本节"维持平铺"的建议被裁决取代；按裁决，第一步是产出迁移清单评估（见 §7 E3），清单经维护者批准后才执行实际迁移。

---

## 2. 九个顶层目录逐个过三问

### 2.1 apps/

**它是干什么用的**：放这个 IMS AS 承载的**业务应用（用例）**。IMS 语境里"应用服务器（AS）"的职能就是承载增值业务；本项目架构（README 架构图、ADR-0002）把 apps/ 定义为"信令面业务应用，**one process per use case**"——每个业务用例一个 Deployment / 一个故障域 / 一个金丝雀单元。业务逻辑通过 `decide()` 纯函数接缝接入 platform 引擎。

**里面有什么**：两个业务应用，都是 Python workspace 成员，标准 src/ + tests/ 布局：
- `translation`（as-translation，号码翻译）：`decision.py` + `outbound.py`；
- `anti-fraud`（as-anti-fraud，反欺诈）：`decision.py`。

**进程怎么来的**（这点 v2 判断不完整，必须说清）：应用本身没有独立入口，**进程外壳由 platform 的 `__main__.py`（"AS process shell"）提供**，应用以业务模块身份被装载。依赖方向是 apps → platform（AGENT.md §4）；platform 永不 import apps——这条由 `platform/tests/test_library_independence.py` 和 `tests/test_layer_boundaries.py` 机器守着。当前 helm 是单一 AS Deployment；"每用例一进程"是 ADR-0002 的目标形态。

**是否应该放在根目录**：**应该**。① 业务应用是产品的差异化本体——客户买这个 AS 买的就是翻译/反欺诈能力；② apps 与 platform 的分离是架构级边界，被三重门禁守护（library_independence / layer_boundaries / workspace_layout，成员四类 kernel/apps/services/testbed 之一）；③ ADR-0002 的演进方向意味着 apps 会增多，顶层可见性重要。

**必须补的一句说明**：web 工程惯例里 apps/ 指"可独立部署的应用"，本项目 apps/ 指"IMS 业务用例（进程由 platform 外壳承载）"。两种读法都成立，但差异要写进 `apps/README.md` 消歧，否则 web 背景的工程师会像 v2 一样误判。

### 2.2 services/

**它是干什么用的**：放产品的**控制面进程**——两个长期运行的独立服务进程（工程意义上的"服务"，与 apps/ 的 IMS 语义刻意区分）。

**里面有什么**：
- `console`（as-console）：运营控制台，src/ + tests/ + `web/`（前端资源内嵌于服务目录）；
- `config-service`（as-config-service）：配置变更单 API，src/ + tests/，有 `[project.scripts]` 进程入口。config-service 依赖 console 的会话/鉴权内部 API（已在 pyproject 显式声明，无环，test_layer_boundaries.py 守着）。

**是否应该放在根目录**：**应该**。它们是部署产物的一部分（Helm chart 里有独立的 config-service deployment；Docker 构建直接引用），构建/测试/发布都会进入。

### 2.3 platform/

**它是干什么用的**：**SIP 内核/引擎**——所有信令在这里进出与裁决；对 reSIProcate C++ 栈的绑定、进程外壳、StateStore 等核心接缝都在这。

**里面有什么**：`src/as_platform`（Python 包，含 `__main__.py` 进程外壳）；`native/` 下三个 C++ 扩展绑定（resip_runtime / resip_recovery / resip_two_leg）；`tests/`（含 test_library_independence.py）。

**是否应该放在根目录**：**应该**。最大最重要的构件，一切依赖它。`native/` 放 platform 内部而不是顶层是正确的——它是引擎的实现细节，不是独立构件。

### 2.4 testbed/

**它是干什么用的**：**测试器械**——给被测系统提供"对端世界"：模拟终端、负载、探针、契约夹具、e2e 用例、可部署的模拟平台。与 tests/ 的分工：testbed 提供环境和器械，tests/ 放断言。

**里面有什么**：7 个子目录，其中 2 个是 workspace 成员、4 个不是：
- 成员：`simulators`（对端模拟器，可运行，13 个模块）、`load`（负载发生器，有进程入口）；
- 非成员：`contracts/`（decision + sip-baseline 契约夹具，纯数据）、`e2e/`（2 个 e2e 用例文件）、`probe/`（基线探针，含自己的 tests/）、`sim-platform/`（自带 Helm chart 的模拟平台，准部署物）。

**是否应该放在根目录**：**应该**（电信仓库惯例：测试器械与测试用例分离）。但**内部治理不合格**：probe 有 tests/ 却不是 workspace 成员（它的测试如何被 pytest 收集？无成文说明）；e2e 用例散在 testbed/ 而非根 tests/，是刻意例外还是漂移无说明；sim-platform 带着与 deploy/ 平行的 chart 混在器械目录里。这是本版保留的最高优先级结构问题。（**v3.2 修正：见 §3.2** —— pytest 收集机制自洽，真问题降级为"成员资格规则未成文" + probe 语义分裂。）

### 2.5 tests/

**它是干什么用的**：**跨切治理守卫**——不测业务功能，测"仓库结构本身"：布局、依赖边界、版本一致性、需求登记、证据纪律。

**里面有什么**：5 个文件——test_workspace_layout.py（workspace 结构门禁）、test_layer_boundaries.py（依赖边界，从 pyproject 声明自动推导）、test_version_consistency.py、test_requirements_registry.py、test_evidence_discipline.py。

**是否应该放在根目录**：**应该**。跨包守卫放根 tests/、成员单测放成员内，是标准分层；这 5 个守卫正是"结构不会烂回去"的自动化保障。

### 2.6 deploy/

**它是干什么用的**：**一切部署产物**的归口——镜像、本地编排、交付 chart、本地集群、告警规则。on-prem 交付形态下这是一等公民。

**里面有什么**：`docker/`（两个 Dockerfile）、`compose/`（本地编排 + playwright 证据工具链）、`helm/`（交付 chart，20 个模板）、`kind/`（本地集群 + **17 个 m5-\* 前缀证据脚本**堆在顶层）、`alerts/`（Prometheus 规则）。

**是否应该放在根目录**：**应该**。归口正确。内部问题一处：kind/ 顶部的 17 个里程碑脚本应移入 `deploy/kind/scripts/` 子目录（执行时 grep Makefile 引用同步）。

### 2.7 docs/

**它是干什么用的**：全部文档的归口。

**里面有什么**：13 个子目录 217 个 md；reviews/（162 个）与 handoff/（35 个）是两大堆积点，且 README 导航漏掉 design/、agents/、SIP_stack_selection.md 三处。

**是否应该放在根目录**：**应该**。结构层无问题；堆积与导航是内容治理，另案处理（v2 的 S1 批次仍然有效）。

### 2.8 scripts/

**它是干什么用的**：**仓库工作流自动化**——文档守卫、版本同步、评审演示编排。

**里面有什么**：check_adr_annotations.py（ADR 注解守卫）、sync-chart-version.sh（chart 版本同步）、d10-req-nf1-harness.sh、`demo-review/`（11 个文件的演示编排子系统）、`lib/repo-toolchain.sh`（共享 shell 库）。

**是否应该放在根目录**：**应该**。与 tools/ 的分工成立（工作流脚本 vs 工具链二进制），但边界无成文说明，各补一句 README 即可。

### 2.9 tools/

**它是干什么用的**：**本地工具链与环境引导**——开发者机器上装的本地二进制和初始化脚本。

**里面有什么**：`bin/`（helm、kind、kubectl、promtool 四个本地二进制，未跟踪）、bootstrap-infra.sh、env-probe.sh、VERSIONS（工具版本钉子）。

**是否应该放在根目录**：**应该，但它是九个里最可讨论的一个**——有的项目会把这类内容收进 scripts/bin/。保留的依据：bin/ 是"安装目标"而非"仓库内容"，独立成目录能一眼区分"进 git 的自动化"与"不进 git 的本地产物"。

**九目录总裁决**：九个全部配占根目录位置，没有多余也没有缺失。需要修的是三个**内部治理**问题（testbed 成员资格、kind 脚本堆积、scripts/tools 边界成文）和一个**消歧说明**（apps 语义）。

## 3. 其余五个目录的深度判断（v3.2 增补）

> 维护者指示（2026-10-29）：对 platform / apps / services / docs 之外的目录做同等力度的判断。本节逐个复核 testbed / tests / deploy / scripts / tools 的根目录资格，并回答三组"为什么是两个 / 为什么混放"的组织张力。**本节补证修正 v3 对 testbed 的两处判断，见 §3.2。**

**新证据（2026-10-29 采集）**：
- 根 pyproject `[tool.pytest.ini_options].testpaths = ["tests", "platform", "apps", "services", "testbed"]` —— pytest 按**目录**收集，testbed/probe/tests 与 testbed/e2e 一直在收集范围内；
- 测试分层由 **pytest markers** 定义（unit / contract / integration / e2e / performance），与目录轴正交；
- uv workspace 成员资格只决定"是否作为可安装包被 uv 管理"，与 pytest 收集是两套机制；
- Makefile：4 个 target 直接引用 `deploy/kind/m5-*.sh`；gate-native 系列全部指向 `testbed/simulators/resip-probe/scripts/m2-native.sh`；chart-check 指向 `deploy/helm/scripts/chart-check.sh`；
- `git ls-files tools/` = VERSIONS、bootstrap-infra.sh、env-probe.sh（bin/ 不跟踪，符合惯例）；
- helm 模板列表中**没有** PrometheusRule 模板 —— `deploy/alerts/` 不随 chart 分发，独立引入。

### 3.1 tests/ —— 5 个文件占一个根目录，值不值？

**它是什么**：5 个跨切守卫（workspace 布局 / 依赖边界 / 版本一致性 / 需求登记 / 证据纪律）。不测产品功能，测"仓库结构本身"——是 AGENT.md 规则的机器执行版。

**判断：维持，无合并选项**。守卫不属于任何一个成员（它们管全部成员），放进任何成员目录都是错位；它们与 testbed 的关系是裁判与器械——守卫测试若依赖 testbed 器械，依赖方向就反了。这是"只能放根目录"的少数目录之一。5 个文件的体量不是问题——每条守卫都在替 review 省争吵。

### 3.2 testbed/ —— 两处 v3 结论修正 + 一个新发现

**修正 1（撤回"probe 成员矛盾"表述）**：v3 称"probe 有 tests/ 却非 workspace 成员是最明显的矛盾"。补证后：pytest 收集与 uv 成员资格**正交**——testpaths 含 "testbed"，probe/tests 一直被收集；成员资格只关乎包安装。probe 无 pyproject（扁平脚本目录），本就不是可安装包，非成员自洽。真问题降级为：**"有 pyproject 才进 workspace，否则留在 testbed 由 pytest 收集"这条规则没有成文**。

**修正 2（e2e-in-testbed 非漂移）**：分层由 markers 定义（`pytest -m e2e`），目录轴回答"器械放哪"——两轴正交是刻意设计，与 §3.1 的"tests/=裁判"裁决自洽。需成文。

**新发现 F-10（probe 语义分裂）**：仓库有两处都叫 probe，新人无法判断"探针在哪"：
- `testbed/probe/` —— Python 基线探针（e1_baseline_probe.py、sequence_compare.py、tls_hot_rotation_probe.py）；
- `testbed/simulators/resip-probe/` —— native 探针 harness（Makefile gate-native 系列全部指向它）。

归一方向交裁决（§6 Q7）。

**sim-platform 混放复核**：自带 chart 的模拟平台是"被测世界的一部分"（模拟客户环境 + 对端平台），不是交付物；与 deploy/ 的 chart 平行不冲突。维持。

### 3.3 deploy/ —— 交付物与本地器具混放复核

**事实分组**：
- 产品交付物：`helm/`（chart 0.2.0，自带 scripts/chart-check.sh 先例）、`docker/`（产品镜像）、`alerts/`（告警规则，不随 chart 分发、独立引入——需一句话成文）；
- 本地开发/证据器具：`compose/`（本地编排 + playwright 证据）、`kind/`（本地集群 + **17 个 m5-\* 脚本堆在顶层**，Makefile 4 个 target 直接引用）。

**判断：维持单目录**。kind/compose 是"把产品在本地跑起来"的两种形态，与交付物同属"部署"一个关注点；拆成 deploy/ + dev-env/ 会把一个心智劈成两个根目录，碎。内部动作两项：m5-\* 移入 `deploy/kind/scripts/`（Makefile 4 处引用同步；与 helm/scripts/ 先例方向一致）；alerts 分发方式成文。

### 3.4 scripts/ 与 tools/ —— 为什么是两个，能不能合一个

**真实分界线**（比 v3 更准的表述）：`scripts/` = **仓库逻辑的一部分**（被 Makefile/gate 直接调用，进 git、进 review）；`tools/` = **把开发机变成能跑仓库的环境**（bootstrap-infra.sh 装的就是 tools/bin/ 里那四样；bin/ 不进 git）。一个面向"仓库怎么做事"，一个面向"机器怎么备好"。

**合并选项评估**：
- A. 维持两个 + 各自一句话 README（本版建议）：成本最低，边界本就清晰，只欠成文；
- B. 合并进 scripts/、bin 改 scripts/bin：省一个根目录条目，代价是丢掉"进 git 的内容 vs 本地产物"的一眼区分，Makefile 引用要改，收益不抵；
- C. tools/ 隐藏化为 .tools/：对 Windows 与部分工具链不友好，否。

### 3.5 汇总

| 目录 | 根目录资格 | 本节动作项 |
|---|---|---|
| tests/ | 维持 | 无（无合并选项，见 §3.1） |
| testbed/ | 维持 | 成员资格规则成文；probe 归一（Q7）；e2e 两轴设计成文 |
| deploy/ | 维持 | m5-\* 归位 kind/scripts/；alerts 分发方式成文 |
| scripts/ | 维持 | 一句话 README |
| tools/ | 维持 | 一句话 README |

**结论：五个目录全部维持根目录资格，无需搬动任何目录。工作量收敛为"四处成文 + 一次脚本归位 + 一个 probe 归一裁决"。**

## 4. 根目录文件逐个裁决

| 文件 | 干什么用的 | 有用? | 该在根? |
|---|---|---|---|
| README.md | 仓库门面 + 架构总览（含分层图与目录树） | 是 | 是（OSS 标准件） |
| LICENSE / NOTICE | Apache-2.0 许可 | 是 | 是 |
| CONTRIBUTING.md | 贡献流程 | 是 | 是 |
| SECURITY.md | 安全披露通道 | 是 | 是 |
| CODE_OF_CONDUCT.md | 行为准则 | 是 | 是 |
| CHANGELOG.md | 变更记录 | 是 | 是 |
| VERSION | 单一版本源（chart 由脚本同步） | 是 | 是（有 test_version_consistency.py 守着） |
| Makefile | gate / test / demo 统一入口 | 是 | 是 |
| pyproject.toml | uv workspace 虚拟 manifest + 工具链配置 | 是 | 是（唯一合法位置） |
| uv.lock | 全 workspace 锁文件 | 是 | 是 |
| AGENT.md | agent 协作守则 | 是 | 是（业界收敛的根目录惯例，agent 先看根） |
| .gitignore / .dockerignore / .python-version | 构建环境元文件 | 是 | 是 |
| .env.example | 环境变量示例（真实 .env 已忽略） | 是 | 是 |
| .trae/rules/ | 编辑器 agent 规则（2 个文件，有意跟踪） | 是 | 可接受（与 .codebuddy/rules 平行） |
| .codebuddy/ | CodeBuddy 编辑器配置 | 部分是 | **有问题**：rules/hard-rules.md 有意跟踪（对）；但 teams/\<hash\>/\_auto_\*/ 下自动生成的 JSON 也被跟踪了——应 gitignore 掉 teams/ 子树，只留 rules/ |
| R2612_Cont.md | R2612 剩余项规划 | 是（R2612 期间） | 已移至 docs/handoff/（2026-10-29，维护者移动） |
| R2612_Struct_Plan.md | 本文件 | 是（review 期） | 已移至 docs/handoff/（2026-10-29） |
| .venv/ 等五个缓存目录 | 本地产物 | 否 | — 均已 gitignore，正确 |

**根目录总裁决**：正式文件没有一个不该在；唯一实际问题是 .codebuddy/teams/ 误跟踪。

## 5. 与 v2 的差异

| v2 结论 | v3 修订 | 修订理由 |
|---|---|---|
| F-1：apps/ 是纯库、名不副实，建议改名 packages/ | **撤销改名建议**，改为"补 apps/README.md 消歧" | v2 只看了"无进程入口"就下结论，漏了项目自己的架构定义：README 架构图 + ADR-0002 明确 apps/ = 信令面业务应用、one process per use case、进程外壳由 platform `__main__.py` 提供、依赖方向 apps→platform 且被门禁锁定。apps/ 在 IMS 语境下名实相符，是 v2 用错了参照系（web monorepo 惯例而非 IMS 产品语境） |
| F-2：testbed 成员资格混乱 | **维持** | 证据未变（probe 有 tests/ 却非成员、e2e 散放、sim-platform 混放） |
| F-3：kind/ 17 个 m5-\* 脚本堆积 | **维持** | 证据未变 |
| F-4：.codebuddy/teams/ 误跟踪 | **维持** | 证据未变 |
| F-5：scripts/tools 边界无成文 | **维持** | 证据未变 |

**v3.1 / v3.2 增补记录**：v3.1 新增 §1 组织原则、发现 F-9、裁决 Q6；v3.2 新增 §3 五目录深度判断、发现 F-10、裁决 Q7，并修正 F-2 的事实前提（pytest 收集与 uv 成员资格正交，probe 非成员自洽，真问题为规则未成文 + probe 语义分裂）。

## 6. 待维护者裁决

| # | 问题 | 选项 | 裁决（维护者，2026-10-29） |
|---|---|---|---|
| Q1 | apps/ 语义消歧 | A. 补 apps/README.md；B. 不补 | **A** |
| Q2 | testbed/probe 的地位 | A. 升级为 workspace 成员；B. 移入 simulators/；C. 成文说明 | **A**（升级为成员） |
| Q3 | testbed/e2e 与 sim-platform | A. 维持+成文；B. e2e 并入根 tests/；C. sim-platform 移出 | **B**（e2e 并入根 tests/；sim-platform 维持在 testbed） |
| Q4 | kind m5-\* 归位 + .codebuddy teams 去跟踪 + scripts/tools README | A. 一批授权执行；B. 逐项再议 | **A** |
| Q5 | v2 文档批次（docs 导航 + reviews/handoff 索引） | 待本文件裁决后执行 | **go（2026-10-29 维护者补答）：执行 v2 S1 文档批次（docs 导航补全 + reviews/handoff 索引）** |
| Q6 | 根目录组织原则 | A. 维持平铺+README；B. 引入 src/ 收拢（先出迁移清单评估） | **B**（先出迁移清单，批准后再执行） |
| Q7 | probe 语义分裂 | A. 合一两处；B. 保留两处 + testbed/README 区分成文 | **B** |

> v3.2 补证后的推荐项更新：Q2 推荐 C（机制自洽，仅成文）；Q3 中 e2e 疑虑撤回（两轴正交设计），sim-platform 维持。

## 7. 执行计划（依据 §6 裁决，2026-10-29 落盘）

> 每批由一个 writing subagent 串行执行（同一工作树同时只允许一个），主 agent 每批后 `git status` / `git diff` 核对并跑 `make gate`；全程不 commit、不 push、不 tag，commit 切分由维护者决定。

### E1 结构改动批次（对应 Q2=A、Q3=B、Q4=A）—— **已全部执行完成（2026-10-29），逐条结果见右列**

| # | 动作 | 细节与验证 | 执行结果（E1 批次后核对） |
|---|---|---|---|
| E1-1 | probe 成员化（Q2=A） | probe 现无 pyproject（扁平脚本目录）。步骤：读 `tests/test_workspace_layout.py` 确认门禁对成员的要求（是否强制 src-layout）；按门禁要求建 `testbed/probe/pyproject.toml`（包名 as-probe，必要时改 src/as_probe 布局并同步 import 引用）；加入根 pyproject `[tool.uv.workspace].members` 与 ruff `src` 列表；`uv sync` + `make gate` 验证 | **完成**：建 `testbed/probe/pyproject.toml`（包名 `as-probe`），迁移为 `src/as_probe` 布局并同步 import 引用；已加入根 pyproject 的 workspace members / ruff src / mypy files 列表 |
| E1-2 | e2e 并入根 tests/（Q3=B） | `git mv testbed/e2e/test_*.py tests/e2e/`（新建 tests/e2e/，__pycache__ 不移）；pytest 收集不变（tests/ 已在 testpaths，marker -m e2e 照常）；Makefile L53-59 历史注释按保史约定**不改原文**，在注释块末尾追加一行新注记说明 e2e 已移至 tests/e2e/；grep 全库 `testbed/e2e` 引用同步；`make test-e2e` 验证 5 条仍通过 | **完成**：两个用例文件已 `git mv` 至 `tests/e2e/`；**12 条 e2e passed**（历史口径"5 条"为场景级计数，参数化后实为 12） |
| E1-3 | kind m5-\* 脚本归位（Q4） | `git mv` 17 个 `deploy/kind/m5-*.sh` → `deploy/kind/scripts/`；Makefile 4 处引用同步（m5-cluster-evidence / m5-kind-verify / m5-issu-scale-evidence / m5-7.2d-evidence 四个 target）；grep 全库其余引用同步 | **完成**：实为 **16 个**脚本（v3 计数 17 有误）归位 `deploy/kind/scripts/`，Makefile 引用同步，含脚本内 dirname 层级修正 |
| E1-4 | .codebuddy teams 去跟踪（Q4） | `.gitignore` 追加 `.codebuddy/teams/`；`git rm -r --cached .codebuddy/teams/`（磁盘文件保留，仅解除跟踪；rules/ 保持跟踪） | **完成**：`.gitignore` 已追加，teams/ 子树已解除跟踪（磁盘保留） |
| E1-收尾 | `make gate` 全绿 | 全部改动后跑一次 | **完成（含一段插曲）**：门禁曾暴露 **5 个预先存在的失败**——根因是 commit 521c834 文档英文化未同步守卫测试的字符串预期；经基线 worktree 对照证实非本批引入；已修 `tests/test_evidence_discipline.py` 与 `tests/test_requirements_registry.py` 的预期字符串。现 `make gate` **1181 passed / 0 failed** |

### E2 文档批次（对应 Q1=A、Q4=A、Q7=B；在 E1 完成后按新事实撰写）—— **已完成（本批次，2026-10-29）**

| # | 文件 | 内容 | 执行结果 |
|---|---|---|---|
| E2-1 | `apps/README.md`（新建，Q1=A） | apps/ = IMS 业务用例（one process per use case，ADR-0002）；进程外壳由 platform `__main__.py` 承载，app 以业务模块装载；依赖方向 apps→platform、platform 永不 import apps（门禁锁定）；与 services/ 的语义区分（IMS 业务应用 vs 控制面进程）；每个用例一个 Deployment/故障域的目标形态 | **完成**（英文撰写；既有中文旧版为英文化遗漏，本批改写覆盖）：含语义消歧、依赖方向与门禁引用、与 services/ 对照表、成员清单 |
| E2-2 | `testbed/README.md`（新建，Q7=B） | 两处 probe 的区分成文（testbed/probe = Python 基线探针；simulators/resip-probe = native 探针 harness，gate-native 入口）；成员资格规则成文（有 pyproject 才进 workspace；probe 已于 E1 升级为成员）；sim-platform = 被测世界的一部分、与 deploy/ chart 的关系；e2e 已移至 tests/e2e/（E1-2 之后）与 markers 两轴设计说明 | **完成**（英文撰写；同上为改写覆盖）：两处 probe 对照表、成员资格规则、六个子目录清单、sim-platform 定位专节 |
| E2-3 | `scripts/README.md` + `tools/README.md`（新建，Q4=A） | scripts/ = 仓库逻辑的一部分（被 Makefile/gate 调用，进 git、进 review）；tools/ = 把开发机备好（bootstrap 装的就是 bin/ 四样；bin/ 不进 git）；各列现有条目一句话说明 | **完成**：两文件均新建，含条目表与一句话边界表述（scripts/ = 仓库逻辑；tools/ = 把机器备好；bin/ 不进 git） |
| E2-4 | 本文件执行状态更新 | §7 各条目标注执行结果 | **完成**：即本节状态标注；文末状态行同步更新 |

### E3 src/ 收拢迁移清单（对应 Q6=B 第一步；只调研不改代码）—— **清单已产出并获维护者批准；迁移已全部执行完成（2026-10-29，分支 R2612，批准语"好的，执行吧"）**

产出 `docs/handoff/2026-10-29-src-consolidation-migration-plan.md`：
- 范围调研：根 pyproject（workspace members / pytest testpaths / ruff src）、门禁测试（test_workspace_layout / test_layer_boundaries）、Dockerfile COPY 路径、Makefile、helm chart 构建引用、uv.lock 再生成、全库文档引用（README / AGENT.md / ADR 目录树与分层图）；
- 产出新旧路径映射表（platform→src/platform 等）与分步执行清单、每步验证方式；
- **清单经维护者批准后才执行迁移**；本批次不搬任何目录。

**执行记录（清单 §3 七步；步骤 1–6 为先行批次，步骤 7 最终验证与本文记录为收尾批次，2026-10-29）**：

- **步骤 1–2（基线 + 搬移）**：三目录 `git mv` 至 `src/`，本笔共 **191 处 rename**（170 纯 rename + 21 rename 后又有修改；git 实测 `git show --name-status --diff-filter=R 2e259c9`）；口径说明：汇总文档里的"224"= 本笔 191 + `a81e13d` 22 + `4530d05` 11，若再计入 `c626031`/`d48785b` 两次文档归位则范围总数为 226；**10 个文件深度修复**——6 处直接 `parents[2]→[3]`（gen-cert 解析三处、test_m2_native_probe_smoke、test_m5_verify_strict、test_e1_contract_resip_runtime_full）、3 处 walk-up **fallback**（`test_sip_message.py` L418 与两处 `test_contract_replay.py`——**实际为 parents[3]→[4]，计划原文统一写 parents[2]→[3] 对这两个文件有误，按文件实际内容修正**）、`test_library_independence.py` 3 处（REPOSITORY_ROOT 深度、KERNEL_SOURCE 插 `src` 段、成员判定改 `src/platform`）；
- **步骤 3（manifest + 锁）**：根 pyproject **六键**按计划同步（`[tool.uv.workspace].members`、`[tool.pytest.ini_options].testpaths`、`[tool.ruff].src`、`[tool.ruff].extend-exclude`（计划即标注无需改动）、`[tool.mypy].files`、`[tool.mypy].mypy_path`）；`uv.lock` 未按计划字面全量重建，改用"**恢复 HEAD 锁 + 增量 uv lock**"避免全量重建的版本漂移——16 条 editable 全部指向 `src/…`，testbed 三条不变，E1/E2 未暂存的锁改动由 uv 重新解析语义等价复原；
- **步骤 4（门禁测试）**：`tests/test_layer_boundaries.py` 四层分类逻辑与断言/提示文本同步；
- **步骤 5（构建/部署/工具，17 处编辑）**：`.dockerignore`、`deploy/docker/` 两个 Dockerfile、`testbed/sim-platform/` 两个 Dockerfile*、`kind-up.sh`、Makefile `m71-sim`、`m2-native.sh` 6 处、`scripts/check_adr_annotations.py`（`_scan_roots` + GRANDFATHERED 键）、`scripts/demo-review/` 5 文件、`d10-req-nf1-harness.sh`、`deploy/compose/` README + 脚本；
- **步骤 6（活文档清扫）**：36 个文件路径引用同步；ADR 裁决 (a) 加注于 `docs/architecture/adr/README.md` L26（`docs/acceptance/`、`docs/reviews/`、历史 `docs/handoff/`、`CHANGELOG.md`、`docs/migration/`、`R2612_*` 均未触碰）；
- **步骤 7（最终验证链，2026-10-29）**：`make gate` **1181 passed / 249 deselected / 0 failed**（与 E1 基线一致）；`make gate-strict` **check_adr_annotations: clean**（既有现象如实记录：`_repo_root()` 深度 bug 使扫描器休眠、打印 `checked 0 files`，23 条 GRANDFATHERED 键以非致命 warning 打印 "allowlist entry no longer needed"）；`make chart-check` **OK**（helm v3.16.4 以 `HELM_BIN` 临时指向 /tmp/linux-amd64，lint 0 chart(s) failed、全部模板守卫通过）；`make alert-check` **SUCCESS: 10 rules found**；`make test-e2e` **12 passed / 1418 deselected**；`uv run pytest -m integration -q`：**82 passed / 12 skipped / 137 errors + 1 failed，逐条甄别全部为环境性、零迁移致因**——137 error + 1 failed 的签名唯一：psycopg 连 `127.0.0.1:55432` 被拒（本机未起 PostgreSQL 服务；本机 libpq 对拒连的措辞是 "server closed the connection unexpectedly"，不在部分测试文件 skip 分类器 `_NETWORK_UNAVAILABLE_MESSAGES` 的六种签名内，故按 ERROR/FAILED 落地而非设计预期的 SKIP——既有测试基建局限，非迁移引入）；12 个 skip 均按设计：9 个 pg store 集成（无 postgres）+ 2 个 d10 redis（6379 拒连）+ 1 个 resip 扩展未构建；迁移敏感的 6 个 gen-cert 路径解析集成用例显式运行全绿（6 passed in 42.37s）。

**与计划的偏离**：① GRANDFATHERED 实为 **23 键**（计划 §2.4 写 26）；② 两处 `test_contract_replay.py` fallback 深度按实际为 parents[3]→[4]（计划统一写 parents[2]→[3]）；③ `uv.lock` 重建方式改为"恢复 HEAD 锁 + 增量 uv lock"（见步骤 3）。

**移交维护者的独立事项（已执行，2026-10-29 E5 批次）**：`scripts/check_adr_annotations.py` 的 `_repo_root()`（L98）由 `parents[2]` 修为 `parents[1]`——维护者批准"修parents"，E5 批次一行修复落地。史实更正：扫描器并非自诞生休眠——它诞生于 `scripts/ci/`，当时 `parents[2]` 恰为仓库根；后上移到 `scripts/` 深度未改，才转为休眠（每次打印 `checked 0 files`）。修复后 REQ-G-3 扫描首次真实运行：`checked 73 files`，实测浮出 **21 个既有 REQ-G-3 违规**（metrics.py×5、auth.py×7、call_controller.py×2、redis_store.py×2、downscale_guard.py / adapter.py / ingress.py / in_memory.py / telemetry `__init__.py` 各 1；本条原先预估分布 auth×6 与实际 ×7 有出入，以实际输出为准）；23 条 GRANDFATHERED 键 stale=0 全部正确命中。`make gate` 不受影响仍全绿（扫描器按 ADR-0015 只在 gate-strict）。**gate-strict 现为诚实红（21 项）：triage（逐条补 ADR 注解或进 allowlist）待维护者裁决后作为 E6 执行**。执行细节见下方 E5 小节。

**未提交声明**：全部改动留在工作树，commit 切分归维护者。

### E4 文档导航批次（对应 Q5=go）—— **已完成（2026-10-29）**

| # | 文件 | 内容 | 执行结果 |
|---|---|---|---|
| E4-1 | docs/README.md | 导航补全（只增补不重写）：Deciding what to build 表增 `requirements/`、`design/`、`SIP_stack_selection.md` 三行；Building it 表增 `agents/` 一行；For reviewers 表增 `reviews/README.md` 一行；Local environment and tooling 表增 `handoff/README.md` 一行 | **完成**：11 个子目录与顶层散放 md（plan.md / environments.md / product-packaging-plan.md / next-release-v1.1-plan.md / SIP_stack_selection.md）全部有导航条目 |
| E4-2 | docs/reviews/README.md（新建） | 全目录 review record 索引（日期｜文件链接｜主题一行），按文件名日期升序、22 个无文件名日期的 M0–M4 早期记录列前；目录说明含 `## Adjudication` 裁决表列说明（ID/来源/问题摘要/裁决/修改方案/状态/验证方式/备注） | **完成**：162 条索引 = 162 个既有 md（README 自身排除）；主题取自各文件首个 H1/H2；162 个相对链接逐一 `test -f` 通过，0 断链，链接集合与文件集合完全一致 |
| E4-3 | docs/handoff/README.md（新建） | 全目录交接文档索引（同上格式），目录说明 2 句（handoff = 会话交接/迁移清单类记录） | **完成**：36 条索引 = 36 个既有 md；0 断链，链接集合与文件集合完全一致 |

**验证**：`make gate` **1181 passed / 249 deselected / 0 failed**（2026-10-29）；守卫测试无红，无需同步任何预期字符串。既有 review/handoff 文件零触碰：`git status --short docs/reviews docs/handoff` 仅两个新增 README，外加 E3 批次既有未跟踪的 `docs/handoff/2026-10-29-src-consolidation-migration-plan.md`（非本批产出）。

### E5 REQ-G-3 扫描器根修复（对应移交事项）—— **已完成（2026-10-29）；gate-strict 诚实红待 E6 triage**

| 项 | 记录 |
|---|---|
| 改动 | `scripts/check_adr_annotations.py` L98：`return Path(__file__).resolve().parents[2]` → `parents[1]`（本批仅此一行，docstring 与其余零改动；该文件 diff 相对 HEAD 另含 E3 步骤 5 的既有未提交改动——GRANDFATHERED 键加 `src/` 前缀、`_scan_roots` 加 `src/` 段） |
| 修复前行为 | 脚本位于 `scripts/`，`parents[2]` 指向仓库上一级 `/home/shudong/project`（脚本诞生于 `scripts/ci/` 时 `parents[2]` 恰为仓库根，上移后深度未改）→ 扫描根不存在 → 每次打印 `checked 0 files`、永远 clean，扫描器休眠 |
| 修复后行为 | `parents[1]` = 仓库根，REQ-G-3 扫描首次真实运行 |
| 扫描验证 | `uv run python scripts/check_adr_annotations.py`：stderr `checked 73 files`；stdout 列 21 条 "lacks an ADR annotation (REQ-G-3)"，EXIT=1；stderr 无 stale warning → 23 条 GRANDFATHERED 键全部命中（stale=0） |
| 21 条分布 | `src/services/config-service/src/as_config_service/auth.py`×7（IssuedSession / RevokedSession / PostgresConsoleAuthStore / create_session / resolve_session / revoke_user_sessions / revoke_session）；`src/platform/src/as_platform/telemetry/metrics.py`×5（MetricsRegistry / CallMetrics / set_downscale_removable / set_state_store_available / record_telemetry_dropped）；`src/platform/src/as_platform/sip/call_controller.py`×2（CallController / restore_from_checkpoint）；`src/platform/src/as_platform/state/redis_store.py`×2（RedisStateStore / load_redis_store_from_env）；各 1：`ops/downscale_guard.py`（ScaleDownPlan）、`sip/adapter.py`（respond_with_metrics）、`sip/ingress.py`（TransportIngressGate）、`state/in_memory.py`（InMemoryStateStore）、`telemetry/__init__.py`（TelemetryEvent） |
| make gate | **1181 passed / 249 deselected / 0 failed**（2026-10-29）；扫描器不在 gate 内，按 ADR-0015 只在 gate-strict |
| 后续 | 21 项违规的 triage 已由 E6 完成甄别与处置（全部为 header 窗口伪影，零注解、零扩白名单，gate-strict 复绿），见下方 E6 小节 |

### E6 REQ-G-3 头窗口伪影修正（对应 21 条违规甄别）—— **已完成（2026-10-29）**

维护者授权按独立判断推进（"E6,为什么需要我裁决？"）。

| 项 | 记录 |
|---|---|
| 甄别结论 | 21 条违规**全部为 header 窗口伪影**，非真实 REQ-G-3 gap：9 个被标记文件的模块 docstring 均已引用治理 ADR，但首个引用多位于 L16–22，落在 `HEADER_LINE_COUNT = 15` 的原始行窗口之外；修复前脚本 L48–49 注释自述设计意图 "the same-file header is the leading lines holding the module docstring"——license 头占 12 行、docstring 起始于 L13 附近，其 ADR 引用常在 L16+，15 行窗口装不下，属实现与设计意图不符 |
| 9 文件 docstring 引用行号（逐行核实） | `src/platform/src/as_platform/` 下：`ops/downscale_guard.py` L21（ADR-0010）与 L34（ADR-0009，docstring 跨 L13–38，两处均在内）；`sip/adapter.py` L22（ADR-0019）；`sip/call_controller.py` L16（ADR-0022）；`sip/ingress.py` L16（ADR-0016）；`state/in_memory.py` L17（ADR-0002/0007）；`state/redis_store.py` L16（ADR-0007）；`telemetry/__init__.py` L18（ADR-0005）；`telemetry/metrics.py` L21（ADR-0010）+ L33（ADR-0005）；`src/services/config-service/src/as_config_service/auth.py` L16（ADR-0024） |
| 处置 | `scripts/check_adr_annotations.py`：新增模块级 `_module_docstring()`（`ast.get_docstring` 提取，`SyntaxError` 回退空串，置于 `_scan_roots` 后）；`_scan_file` 改为读盘一次复用（`text` → docstring + `splitlines()`）；header 判定改为两口径——**模块 docstring ∪ 前 15 行原始行**任一命中即整文件豁免；同步头部注释块说明两口径及依据。依据即脚本自身注释声明的设计意图（见上），**零注解改动、零扩白名单、GRANDFATHERED 23 键零改动**；stale / main / MARKER_SUBSTRINGS 等其余逻辑逐字未动 |
| GRANDFATHERED 核实 | 23 键所在 9 文件（api.py、as_instance_store.py、managed_rule_store.py、sip_stack_service.py、transport_env.py、recovery.py、recovery_coordinator.py、resip_recovery.py、resip_runtime.py）前 25 行均无 ADR 引用——修复后这些定义仍走白名单命中，23 键保持 used、stderr 零 stale warning、白名单零改动 |
| 验证 | `uv run python scripts/check_adr_annotations.py`：stdout 恰为 `check_adr_annotations: clean`，stderr 恰为 `checked 73 files`、无任何 stale warning，EXIT=0；`make gate` **1181 passed / 249 deselected / 0 failed**（本批曾因新增表达式换行不符 formatter 被拦一次，按 `ruff format` 期望修正后全绿）；`make gate-strict` 全绿（1181 passed / 249 deselected + `checked 73 files` / `check_adr_annotations: clean`） |

### E7 测试容器治理与 skip 签名（维护者整体授权）—— **已完成（2026-10-29）**

| 项 | 记录 |
|---|---|
| 容器治理 | `docker rm -v as-pg-test`（PG16/55432 端口冲突源，stopped 状态，仅挂一个匿名卷随 `-v` 清除）→ 输出容器名，删除成功；`docker update --restart unless-stopped as-m4b8-dev-postgres-1 as-redis-test as-pg-logical-test as-pg15-test` → 四容器名逐一回显，更新成功（as-pg-logical-test 与 as-pg15-test 处于 Exited，仅改策略不启动）；inspect 复核：四容器 `restart=unless-stopped` 全部生效，`docker inspect as-pg-test` 报 `no such object` |
| skip 签名修复 | grep `_NETWORK_UNAVAILABLE_MESSAGES` 全仓共 **10 个定义副本**（全在 `src/services/config-service/tests/`，远多于预检已知 3 个）：as_instance_store L47、change_order_store L46、activation L67、managed_rule_pipeline L57、auth_api L54、audit_store L39、managed_rule_store L45、migrate L32、distribution_store L56、auth L50；每个元组仅追加一行 `"server closed the connection unexpectedly"`（libpq 对拒连的包装措辞，本机 E3 实测；原六签名全为 socket 层短语漏了它），元组其余内容与格式零改动 |
| 双向验证 | 活 DSN `AS_PG_TEST_DSN=postgresql://postgres:postgres@127.0.0.1:55432/as_config uv run pytest src/services/config-service/tests/test_postgres_auth_api_integration.py -q` → **19 passed**（PG 在跑，skip 分支不触发）；死端口同命令 DSN 换 `127.0.0.1:59999` → **19 skipped**，skip 原因消息即 `…server closed the connection unexpectedly`（修复前该形态为 error）——本批核心验证通过 |
| 文档化 | `docs/environments.md` 追加 §7 Local test containers：四容器族谱表（as-m4b8-dev-postgres-1 55432 canonical 集成 PG／as-redis-test 6379 d10 redis／as-pg-logical-test 55433、as-pg15-test 55434 逻辑复制验收专用）、`make test-integration-compose`（AS_PG_TEST_DSN→55432）与 d10 redis（6379）的依赖关系、restart=unless-stopped（2026-10-29 起，防宿主机重启后静默退网——2026-10-12 曾发生且两周未察觉）、PG≥13 勿同端口（PG16 实测报 `operator is not unique: "char" || unknown`，曾误导排障）、as-pg-test 已于 2026-10-29 移除；既有内容零改动 |
| make gate | **1181 passed / 249 deselected / 0 failed**（2026-10-29）；`tests/test_evidence_discipline.py` 137 passed 先行单验，environments.md 追加小节未触发任何守卫 |
| 备注 | distribution_store 的 `_is_network_unavailable(exc)` 为内联 `psycopg.OperationalError` 判断（非其余 9 副本的参数化形态），但元组 marker 机制相同，追加签名同样生效，按 grep 为准一并修复 |

### E8 Makefile LD_LIBRARY_PATH 消毒（提交后环境插曲）—— **已完成（2026-10-29）**

| 项 | 记录 |
|---|---|
| 现象 | 六笔结构 commit 落盘后新开 shell 跑 `make gate` 假红：`test_recovery_coordinator` 失败（worker 异常被 executor 吞掉，表象为断言失败而非环境错误）；`env -u LD_LIBRARY_PATH make gate` 实测 1181 passed，定位到环境层 |
| 根因 | Trae 服务端给新 shell 注入 LD_LIBRARY_PATH，含 `.../trae-cn-server/bin/stable-*/modules/ai-agent` 与 `.../ai-agent/bin`；其捆绑 libstdc++.so.6 最高仅 GLIBCXX_3.4.25，而 `src/platform/native/resip_recovery/build/_resip_recovery…so` 与 `.cache/m2-resiprocate` 下 reSIProcate 库需要 3.4.29/3.4.30 → 动态链接器命中捆绑旧库 → native 扩展 ImportError |
| 修复 | `Makefile` 顶部变量区新增消毒段：LD_LIBRARY_PATH 按 `:` 拆词、剔除含 `ai-agent` 的目录后重新 `export`；`lib/nss` 等其余条目保留；未污染环境（过滤结果为空）走 `ifneq` 守卫零改动；除该段外 Makefile 其余内容一个字符未改。与批准文本的唯一偏离：命中行改用 `foreach + if + findstring`（子串匹配）——实测 GNU make `filter` 模式仅允许单个 `%` 通配符、第二个 `%` 按字面处理，批准稿的 `$(filter %ai-agent%,…)` 为静默 no-op（最小用例 `$(filter %ai-agent%,/x/modules/ai-agent /y/lib/nss /z/ai-agent/bin)` 返回空、`$(filter %.c,a.c b.h)` 正常返回 `a.c`，污染与干净环境结果一致） |
| 验证 | 污染 shell 下直接 `make gate` 全绿 **1181 passed / 249 deselected / 0 failed**（2026-10-29，不再需要 `env -u LD_LIBRARY_PATH`）；过滤逻辑经 `make --eval` 注入临时 rule 的子进程 `echo $$LD_LIBRARY_PATH` 复核：真实 Trae 污染输出仅余 `…/lib/nss` 条目，模拟串 `…/modules/ai-agent:…/lib/nss:…/ai-agent/bin` 输出仅余 `/y/lib/nss`，未污染环境（LD_LIBRARY_PATH 空）`DIRS=[]` 守卫零改动 |

### 暂缓项

- Q5（v2 文档批次：docs/README 导航补全 + reviews/handoff 索引）已裁决（2026-10-29 维护者补答 go），已作为 E4 执行完成。

---

Written to disk: 2026-10-28; v3.2 2026-10-29; rulings recorded 2026-10-29 (Q1=A Q2=A Q3=B Q4=A Q6=B Q7=B). Status per §7: **E1 done, E2 done (docs batch, 2026-10-29), E3 done (src/ consolidation migration executed and verified, 2026-10-29), E4 done (docs navigation + reviews/handoff index, 2026-10-29), E5 done (REQ-G-3 scanner repo-root fix; gate-strict honestly red with 21 pre-existing violations pending E6 triage, 2026-10-29), E6 done (REQ-G-3 header-window artifact fixed — 21 items pass via module-docstring citations, zero annotations, zero allowlist growth, 2026-10-29), E7 done (test-container governance + PG-unreachable skip signature, 2026-10-29), E8 done (Makefile LD_LIBRARY_PATH sanitization, 2026-10-29)**. Six structural commits a81e13d/d32ff79/2e259c9/3b1c873/3f035af/4530d05, plus c626031 (E8 Makefile 消毒 + 结构计划归位) and d48785b (C 延续计划归位), landed on branch R2612, not pushed; commit 切分归维护者。
