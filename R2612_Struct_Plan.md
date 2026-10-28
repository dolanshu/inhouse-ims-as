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
> 证据采集：2026-10-28，全部来自对仓库文件系统、git 索引和 README/AGENT.md/plan.md 原文的直接检查。
> 关联：[R2612_Cont.md](R2612_Cont.md)（剩余项规划）。

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

**是否应该放在根目录**：**应该**（电信仓库惯例：测试器械与测试用例分离）。但**内部治理不合格**：probe 有 tests/ 却不是 workspace 成员（它的测试如何被 pytest 收集？无成文说明）；e2e 用例散在 testbed/ 而非根 tests/，是刻意例外还是漂移无说明；sim-platform 带着与 deploy/ 平行的 chart 混在器械目录里。这是本版保留的最高优先级结构问题。

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

## 3. 根目录文件逐个裁决

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
| R2612_Cont.md | R2612 剩余项规划 | 是（R2612 期间） | 暂留（维护者指示）；闭环后移入 docs/ |
| R2612_Struct_Plan.md | 本文件 | 是（review 期） | 暂留（同上） |
| .venv/ 等五个缓存目录 | 本地产物 | 否 | — 均已 gitignore，正确 |

**根目录总裁决**：正式文件没有一个不该在；唯一实际问题是 .codebuddy/teams/ 误跟踪。

## 4. 与 v2 的差异

| v2 结论 | v3 修订 | 修订理由 |
|---|---|---|
| F-1：apps/ 是纯库、名不副实，建议改名 packages/ | **撤销改名建议**，改为"补 apps/README.md 消歧" | v2 只看了"无进程入口"就下结论，漏了项目自己的架构定义：README 架构图 + ADR-0002 明确 apps/ = 信令面业务应用、one process per use case、进程外壳由 platform `__main__.py` 提供、依赖方向 apps→platform 且被门禁锁定。apps/ 在 IMS 语境下名实相符，是 v2 用错了参照系（web monorepo 惯例而非 IMS 产品语境） |
| F-2：testbed 成员资格混乱 | **维持** | 证据未变（probe 有 tests/ 却非成员、e2e 散放、sim-platform 混放） |
| F-3：kind/ 17 个 m5-\* 脚本堆积 | **维持** | 证据未变 |
| F-4：.codebuddy/teams/ 误跟踪 | **维持** | 证据未变 |
| F-5：scripts/tools 边界无成文 | **维持** | 证据未变 |

## 5. 待维护者裁决

| # | 问题 | 选项 |
|---|---|---|
| Q1 | apps/ 语义消歧 | A. 批准补 `apps/README.md`（写明"IMS 业务用例、进程由 platform 外壳承载、与 services/ 的语义区分"）；B. 不补 |
| Q2 | testbed/probe 的地位 | A. 升级为 workspace 成员；B. 移入 simulators/；C. 维持非成员但在 testbed/README.md 成文说明收集方式 |
| Q3 | testbed/e2e 与 sim-platform | A. 维持现状 + README 成文；B. e2e 并入根 tests/；C. sim-platform 移出 testbed |
| Q4 | kind m5-\* 脚本归位 + .codebuddy teams/ 去跟踪 + scripts/tools README | A. 一批授权执行；B. 逐项再议 |
| Q5 | v2 的文档批次（docs 导航 + reviews/handoff 索引） | 待本文件裁决后一并执行 |
| Q6 | 根目录组织原则 | A. 维持平铺 + README 写明分类地图（本版建议，F-9 修法）；B. 引入 `src/` 收拢产品源码（PostgreSQL 流派，需先出迁移清单评估） |

---

Written to disk: 2026-10-28 (v3.1: added §1 root-organization rationale, F-9, Q6). Status: awaiting maintainer rulings on §5. Nothing executed, nothing committed.
