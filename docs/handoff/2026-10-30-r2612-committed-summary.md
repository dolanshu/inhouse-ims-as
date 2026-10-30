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

# R2612 已提交部分内容汇总（2026-10-30）

> **性质**：汇总记录，对象是分支 `R2612` 上**已经 commit 的内容**。工作区中尚未提交的改动（10-30 的 E9–E12 / S8 批次，24 个已改文件 + 14 个未跟踪文件）**不在本文范围内**，一处不提。
> **上游**：[`R2612_Struct_Plan.md`](./R2612_Struct_Plan.md)（结构评审 + §7 E1–E8 执行账本）、[`R2612_Cont.md`](./R2612_Cont.md)（剩余项规划）、[`2026-10-29-src-consolidation-migration-plan.md`](./2026-10-29-src-consolidation-migration-plan.md)（E3 迁移清单）。
> **证据采集**：2026-10-30，`git merge-base` / `git log` / `git show --stat --name-status` / `git ls-tree` 的逐条输出，以及对被引文件原文的直接阅读。**本文未重新运行 `make gate` 等任何验证命令**，所有"绿/红"口径均引自上列账本文档当时落盘的记录。
> **git 写操作**：无（不 commit / 不 push / 不 tag）。

---

## 1. 范围与边界

| 项 | 事实 |
|---|---|
| 分支 | `R2612`（本地，未 push） |
| 分叉点 | `git merge-base master R2612` = `c3b951e`（v0.2.0，master 尖端） |
| 已提交 commit 数 | **10**（2026-10-28 两笔，2026-10-29 八笔） |
| 相对 master 的累计差异 | `300 files changed, 2020 insertions(+), 621 deletions(-)` |
| 未提交改动 | 存在，但**不在本文范围**（见抬头声明） |

十个 commit 分三组：**A** 两份规划文档落地（10-28）→ **B** 结构批次 E1–E8（10-29）→ **C** 规划文档归位（10-29）。

---

## 2. 逐 commit 汇总

### A. 规划文档落地（2026-10-28）

| Commit | 内容 | 规模 |
|---|---|---|
| `2d8bfaa` reorignize path | 新建 `R2612_Cont.md`（266 行：M8 之后 18 项剩余工作，三类排序）与 `R2612_Struct_Plan.md`（167 行：九个顶层目录逐目录评审 v3）；`AGENT.md` 5 行同步 | 3 files, +434/-4 |
| `0d740d4` upd | `R2612_Struct_Plan.md` 增补：§1「为什么产品源码与 `docs/` 同级」的三层回答、新发现 F-9、裁决项 Q6 | 1 file, +33/-15 |

### B. 结构批次 E1–E8（2026-10-29，账本见 `R2612_Struct_Plan.md` §7）

| Commit | 批次 | 内容 | 规模 |
|---|---|---|---|
| `a81e13d` | **E1** | ① `testbed/probe` 成员化：新建 `testbed/probe/pyproject.toml`（包名 `as-probe`），脚本迁入 `testbed/probe/src/as_probe/` 并同步 import 与 3 个测试文件；② `testbed/e2e/` 两个用例 `git mv` 至 `tests/e2e/`（Makefile 历史注释按保史约定只追加一行新注记）；③ `deploy/kind/` 顶部 **16 个** `m5-*.sh` 归位 `deploy/kind/scripts/`（含脚本内 dirname 层级修正），Makefile 4 个 target 引用同步；④ `.gitignore` 追加 `.codebuddy/teams/` 并对该子树 `git rm --cached`（6 个自动生成 JSON 解除跟踪，磁盘保留）；⑤ 修 `tests/test_evidence_discipline.py`、`tests/test_requirements_registry.py` 的预期字符串（修的是 521c834 文档英文化遗留的守卫漂移，非本批引入） | 35 files, +147/-230 |
| `d32ff79` | **E2** | 新建 `scripts/README.md`、`tools/README.md`（各一句话边界：scripts = 仓库逻辑、tools = 把开发机备好、`bin/` 不进 git）；`testbed/README.md` 改写为英文（两处 `probe` 消歧、成员资格规则、sim-platform 定位） | 3 files, +117/-14 |
| `2e259c9` | **E3** | `git mv platform/ apps/ services/ → src/`，本笔 **191 处 rename**（platform 121 / services 54 / apps 16），另 50 处修改、2 新增、1 删除；根 `pyproject.toml` 六键同步（workspace members / pytest testpaths / ruff src / mypy files / mypy path；`extend-exclude` 按清单本就无需改）；`uv.lock` 的 editable 全部指向 `src/…` 并把 `testbed/probe` 纳入（成员 7 → 8）；门禁 `tests/test_layer_boundaries.py` 四层分类与断言/提示文本、`src/platform/tests/test_library_independence.py` 深度与成员判定；构建部署侧 `.dockerignore`、两个产品 Dockerfile、两个 `testbed/sim-platform/Dockerfile*`、`kind-up.sh`、`m2-native.sh` 6 处、`scripts/check_adr_annotations.py` 的 `_scan_roots` + GRANDFATHERED 键、`scripts/demo-review/*`、`d10-req-nf1-harness.sh`、`deploy/compose/` README + 脚本；活文档约 36 处路径同步；ADR 按裁决 (a) 在 `docs/architecture/adr/README.md` 加注、ADR 正文不改 | 244 files, +791/-340 |
| `3b1c873` | **E4** | `docs/README.md` 导航补全 **6 行**（`requirements/`、`design/`、`SIP_stack_selection.md`、`agents/`、reviews 索引、handoff 索引）；新建 `docs/reviews/README.md`（162 条索引）与 `docs/handoff/README.md`（**36 条索引**——`3b1c873` 当时值；`c626031`/`d48785b` 各加一条后 HEAD 为 38 条），0 断链 | 3 files, +246 |
| `3f035af` | **E5 + E6** | `scripts/check_adr_annotations.py`：① `_repo_root()` L98 由 `parents[2]` 改 `parents[1]`（脚本诞生于 `scripts/ci/` 时深度正确，上移到 `scripts/` 后一直休眠、每次打印 `checked 0 files`）；② 新增 `_module_docstring()`（`ast.get_docstring`），header 判定改为「模块 docstring ∪ 前 15 行原始行」双口径。修复后 REQ-G-3 首次真跑：`checked 73 files`，21 条违规全部判为头窗口伪影（引用位于 L16–33，落在原 15 行窗口外），**零加注解、零扩白名单**，gate-strict 复绿 | 1 file, +45/-30 |
| `4530d05` | **E7 + 补漏** | ① 10 处 `_NETWORK_UNAVAILABLE_MESSAGES` 各追加一行 `"server closed the connection unexpectedly"`（libpq 对拒连的措辞，原六签名遗漏；PG 缺失时由 ERROR 变 SKIP）；② **补齐 `2e259c9` 漏移的 11 个 `services/config-service/tests/` 文件到 `src/services/`**（详见 §4-2）；③ `docs/environments.md` 新增 §7 本地测试容器治理（四容器族谱、restart 策略、PG≥13 勿同端口）；④ 账本 E5/E6/E7 | 13 files, +215/-16 |
| `c626031` | **E8** | `Makefile` 顶部新增 `LD_LIBRARY_PATH` 消毒段：按 `:` 拆词、剔除含 `ai-agent` 的目录后重新 export（Trae 注入的捆绑 libstdc++ 最高 GLIBCXX_3.4.25，低于 native resip 扩展所需的 3.4.29+，曾造成 `make gate` 假红）；未污染环境由 `ifneq` 守卫零改动。实现由批准稿的 `$(filter %ai-agent%,…)` 改为 `foreach + if + findstring`（GNU make `filter` 只认单个 `%`，批准稿为静默 no-op）；`R2612_Struct_Plan.md` 移入 `docs/handoff/` | 3 files, +22/-3 |

### C. 规划文档归位（2026-10-29）

| Commit | 内容 | 规模 |
|---|---|---|
| `d48785b` | 维护者把 `R2612_Cont.md` 移入 `docs/handoff/`（纯 rename）；`docs/handoff/README.md` 增一行索引；`R2612_Struct_Plan.md` §4 根目录文件表中 `R2612_Cont.md` 的处置格更新 | 3 files, +2/-1 |

---

## 3. 按主题看已提交部分改动了什么

1. **产品源码收拢 `src/`**：`platform/`、`apps/`、`services/` 三个目录整迁 `src/`，全程 `git mv` 保史；累计约 **224 处 rename**（`2e259c9` 191 + `a81e13d` 22 + `4530d05` 11）；该数**不含** `c626031`/`d48785b` 两次文档归位，若计入则本范围总数为 226。`testbed/`、`tests/`、`deploy/`、`docs/`、`scripts/`、`tools/` 留在根目录不动。
2. **workspace 与成员**：成员 7 → **8**（新增 `as-probe`）；成员路径改为 `src/platform`、`src/apps/translation`、`src/apps/anti-fraud`、`src/services/config-service`、`src/services/console`，`testbed/{simulators,load,probe}` 不变；导入根包名（`as_platform` 等 8 个）**一个都没改**。
3. **根 manifest 与锁**：`[tool.uv.workspace].members`、`[tool.pytest.ini_options].testpaths`、`[tool.ruff].src`、`[tool.mypy].files`、`[tool.mypy].mypy_path` 五键加 `src/` 前缀；`uv.lock` 的 16 条 editable 同步（账本记录：采用"恢复 HEAD 锁 + 增量 `uv lock`"而非全量重建，避免版本漂移）。
4. **门禁守卫**：`test_layer_boundaries.py` 的四层分类逻辑与断言/提示文本；`test_library_independence.py` 的 `REPOSITORY_ROOT` 深度、`KERNEL_SOURCE` 插入 `src` 段、成员判定改 `src/platform`；两个文档守卫的预期字符串随英文化同步。账本口径 `make gate` **1181 passed / 249 deselected / 0 failed**。
5. **构建与部署**：`Makefile`（`m71-sim` 路径改 `src/platform/tests/`、4 个 `m5-*` target 指向 `deploy/kind/scripts/`、e2e 归位保史注记一行、LD_LIBRARY_PATH 消毒段）；`.dockerignore`；`deploy/docker/Dockerfile`、`config-service.Dockerfile`；`testbed/sim-platform/Dockerfile`、`Dockerfile.product`、`kind-up.sh`；`m2-native.sh` 6 处；`deploy/compose/` README + 脚本。
6. **工具链**：`scripts/check_adr_annotations.py` 修根 + 修头窗口（REQ-G-3 首次真跑，21 项判为伪影，23 条 GRANDFATHERED 键 stale=0）；`scripts/demo-review/{lib,story-a..d}.sh`、`scripts/d10-req-nf1-harness.sh` 的 pytest node id 与构建目录默认值同步。
7. **测试基建**：e2e 归位 `tests/e2e/`（12 passed）；probe 成员化并进入 workspace；PG 拒连由 ERROR 变 SKIP；`docs/environments.md` §7 记录容器族谱、restart=unless-stopped 与 PG16 同端口冲突坑。
8. **文档**：迁移清单 `2026-10-29-src-consolidation-migration-plan.md` 落盘；`docs/README.md` 导航补全；`docs/reviews/README.md`（162 条）+ `docs/handoff/README.md`（36 条，`3b1c873` 当时值；HEAD 38 条）两条新索引，0 断链；`apps/`、`scripts/`、`tools/`、`testbed/` 四份 README；活文档路径约 36 处；ADR 走裁决 (a)：正文不改，只在 ADR README 加注。
9. **卫生与保史**：`.codebuddy/teams/` 去跟踪；`docs/acceptance/`、`docs/reviews/` 正文、历史 handoff、`CHANGELOG.md`、`docs/migration/triage.md` 一律未触碰。

---

## 4. 已提交范围内的遗留项（三条，均带建议值）

| # | 事实 | 建议值 |
|---|---|---|
| 1 | `d48785b` 把 `R2612_Cont.md` 移入 `docs/handoff/` 后，`docs/handoff/R2612_Struct_Plan.md` L21 的关联链接仍写 `` [R2612_Cont.md](../../R2612_Cont.md) ``，解析到仓库根 → **已断链**（已于 2026-10-30 补漏批次改为 `./R2612_Cont.md`）；该 commit 只更新了索引行与 §4 表格处置格，未改这处正文链接 | 改为 `./R2612_Cont.md`（一行；属保史边界内的路径修正，非改史实） |
| 2 | `2e259c9` 漏移 `services/config-service/tests/` 下 11 个文件，使 `3b1c873`、`3f035af` 两个 commit 处于"根 `services/` 残留 11 文件"的中间态；`4530d05` 已补齐，HEAD 最终态正确 | 不修历史（最终态已正确、rename 相似度仍可追踪）；若介意历史可读性，可选把结构三笔 squash 后再落地 |
| 3 | 10 个 commit 全在本地，未 push；`master` 仍在 `c3b951e` | 先完成本汇总的对齐，再由维护者决定 push 与 commit 切分 |

---

## 5. 声明

- 本文只覆盖 `git merge-base master R2612`（`c3b951e`）之后的 10 个已提交 commit；**不含任何工作区未提交内容**。
- 本文未执行 `make gate` / `uv` / `docker` 等验证命令，所有通过口径均引自 `R2612_Struct_Plan.md` §7 当时落盘的账本记录。
- 撰写过程未做任何 git 写操作（commit / push / tag / branch 均无）。
