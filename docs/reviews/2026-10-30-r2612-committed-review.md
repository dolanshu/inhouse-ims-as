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

# R2612 已提交部分评审（10 个 commit，2026-10-30）

> **评审对象**：分支 `R2612` 上 `git merge-base master R2612` = `c3b951e` 之后的 **10 个已提交 commit**
> （`2d8bfaa` `0d740d4` `a81e13d` `d32ff79` `2e259c9` `3b1c873` `3f035af` `4530d05` `c626031` `d48785b`）。
> **不在范围内**：工作区未提交改动（10-30 的 E9–E12 / S8 批次，24 改 + 14 未跟踪），一处不评。
> **上游**：[`../handoff/2026-10-30-r2612-committed-summary.md`](../handoff/2026-10-30-r2612-committed-summary.md)（被评的汇总）、[`../handoff/R2612_Struct_Plan.md`](../handoff/R2612_Struct_Plan.md) §7 执行账本、[`../handoff/2026-10-29-src-consolidation-migration-plan.md`](../handoff/2026-10-29-src-consolidation-migration-plan.md)。
> **方法**：6 个只读子 agent 分工逐 commit 核查 + 父级对全部存疑项在磁盘上独立复核（`git show --stat` / `--name-status` / `git grep` / 链接存在性脚本 / `uv run pytest` / `python3 scripts/check_adr_annotations.py`）。**子 agent 自述的结论一律不直接采信**，凡下表"证据"列带命令输出者均为父级复核结果。
> **未执行**：`make gate` 全量 / docker / kind；**git 写操作：无**（不 commit / 不 push / 不 tag / 不 branch）。
> **Reviewer**：AI agent，代维护者。**需维护者会签**——本记录不替代会签、不闭环任何里程碑。

---

## 0. 需要维护者做的事（按建议值，共 3 项阻塞 + 5 项建议）

> **2026-10-30 更新**：R-1 / R-3 / R-4 / R-5 / R-7 / R-8 / R-9 / R-10 / R-11 / R-12 / R-14 / R-15 / R-16 已按建议值落地（补漏 commit，见 §9）；
> B2 已由维护者裁决打回（`AGENT.md` 不动）；R-6 与 R-2 的引用 follow-up 也已按建议值落地（§9）。

| # | 事项 | 建议值 |
|---|---|---|
| **B1** | E3 漏改的**可执行路径**残留，6 个文件 12 处（R-1） | 补一个"E3 补漏"commit，全部加 `src/` 前缀；建议并入下一次已提交批次，**修完再 push** |
| ~~**B2**~~ | `AGENT.md` §11 三条硬规则在 `2d8bfaa` 被静默删除（R-2） | **已裁决（维护者 2026-10-30）：打回，「AGENT.md 不动」** —— 不恢复三条规则；四处对 `AGENT.md §11` 的引用（`CONTRIBUTING.md` L69、`responsibility-matrix.md` L42、`security-privacy.md` L131/L206）维持现状，另立 follow-up 登记（见 §8 R-2） |
| **B3** | 活文档断链 8 处（R-3），其中 4 处是 E3 造成、2 处是新建即错 | 与 B1 同批一次修完；`R2612_Struct_Plan.md` L21 改 `./R2612_Cont.md`（1 行，保史边界内） |
| P2-1 | 账本 rename 计数 225 与 git 实测 191 不符（R-4） | 订正 `R2612_Struct_Plan.md` L284 为 **191（170 纯 + 21 带改）**，或注明计数口径 |
| P2-2 | 账本收尾行自相矛盾（R-5） | 删 "the E8 changes await the 7th commit"，并把 `c626031`/`d48785b` 补进 commit 枚举 |
| P2-3 | REQ-G-3 的 docstring 整文件豁免 + 窗口不含定义自身 docstring（R-6） | 建议值：docstring 命中改"豁免但计数告警"；或把窗口扩到定义自身 docstring |
| P2-4 | Makefile 消毒段空格/空条目边界（R-7）、compose 无 `restart:`（R-8） | 加一行 `empty :=`；`compose.yml` postgres 补 `restart: unless-stopped` |
| P2-5 | 汇总文档三处数字口径（R-15） | 订正：docs/README 补全为 **6 行**；handoff 索引"36 条"注明为 `3b1c873` 时值（HEAD 38）；rename 224 注明不含两次文档归位（范围总数 226） |

---

## 1. 规模与边界（实测）

| 项 | 汇总声称 | 实测 | 判定 |
|---|---|---|---|
| 已提交 commit 数 | 10 | `git rev-list --count c3b951e..HEAD` = **10** | ✅ |
| 累计差异 | 300 files, +2020/-621 | `git diff --shortstat` = **300 files, +2020/-621** | ✅ |
| 范围 rename 总数 | 约 224（191+22+11） | `git log --diff-filter=R` = **226**（224 + `c626031`/`d48785b` 两次文档归位） | ⚠️ 口径见 R-15 |
| `2e259c9` rename | 191（platform 121 / services 54 / apps 16） | **191**；相似度分布 **170×R100 + 21×R081–R099** | ✅ 数字对，但账本 L284 的 225（186+39）**错**，见 R-4 |

---

## 2. 逐 commit 结论

| Commit | 批次 | 结论 | 一句话 |
|---|---|---|---|
| `2d8bfaa` | A | **accept with fixes** | 3 files +434/-4、Cont 266 行、Struct_Plan 167 行均属实；但 `AGENT.md` 5 行是"删 3 条 git 规则 + 移 1 条"，commit message `reorignize path` 未声明 → R-2 |
| `0d740d4` | A | **accept** | 1 file +33/-15 属实；§1 三层回答 / F-9 / Q6 均在位（F-9 编号撞车见 R-14） |
| `a81e13d` | E1 | **accept** | probe 成员化、16 个 `m5-*.sh` 归位 + dirname 三层修正、e2e `git mv`、Makefile 只追加保史注记、`.codebuddy/teams` **6 个**去跟踪（`git show --name-status` 实测 D×6）——全部属实；仅 `.gitignore` 段落位置小瑕（R-16） |
| `d32ff79` | E2 | **accept with fixes** | 3 files +117/-14 属实且三份 README 后续无改动；但 `testbed/README.md` L39 的 testpaths 未随 E3 同步（R-9）、ADR-0014 L76 逐字引用悬空（R-10）、`scripts/README.md` 一句过度概括（R-11） |
| `2e259c9` | E3 | **accept with fixes** | 主体（src 收拢、manifest 五键、`uv.lock` 16 条 editable 全 `src/`、两个门禁守卫、Dockerfile/.dockerignore/kind-up/m2-native、ADR 裁决 (a)）全部到位；**遗留 12 处可执行路径 + 8 处活文档断链**（R-1 / R-3） |
| `3b1c873` | E4 | **accept with fixes** | 两份新索引实测 0 断链（handoff 38/38、reviews 162/162，与已跟踪文件数 39/163 自洽）；但"导航补全 5 行"实测 **6 行**（R-15） |
| `3f035af` | E5+E6 | **accept with fixes** | `parents[1]` 与双口径、非靠放宽白名单变绿（GRANDFATHERED 仍 23 条、阈值未动、唯一 except 是 SyntaxError 回退致严）；实测 `checked 73 files / clean`；但 docstring 整文件豁免与窗口缺口需补口径（R-6） |
| `4530d05` | E7+补漏 | **accept** | 10 个测试文件各加 1 行 libpq 拒连签名（实测 10 + 账本引用 1 = 11 处命中串）、11 个漏移文件已补齐、`src/services/config-service/tests/` 无根残留 |
| `c626031` | E8 | **accept with fixes** | 消毒段位置在 `export UV` 之后、全部规则之前，对配方与唯一递归 `$(MAKE) gate` 均生效；未污染环境零改动属实；两个低概率边界缺陷（R-7） |
| `d48785b` | C | **accept with fixes** | 纯 rename（内容 0 改动）、索引行正确、**未改史实**；唯一遗留是 L21 断链（R-3），且该断链自 `2d8bfaa` 起就存在（汇总 §4-1 归因不全） |

---

## 3. 发现清单

### P1 — 建议修完再 push

| # | 事实（证据） | 建议值 |
|---|---|---|
| **R-1** | **E3 漏改的可执行路径，HEAD 仍指向旧根**（`git grep -n "platform/tests\|platform/native" HEAD -- '*.sh' '*.py'`；`git grep -n '"platform" / "src"' HEAD`）：`testbed/load/scripts/m6-{product-runtime-smoke,micro-measure,measure-60s,o1-formal-report}.sh` 各 2 行（L20/21、L32/33）＝ 8 行；`testbed/load/tests/test_product_runtime_smoke.py:32-33`；`deploy/kind/scripts/m5-7.2d-evidence.sh:69`（`${ROOT}/services/config-service`）；`testbed/simulators/resip-probe/d10-recovery/orchestrate.py:35`、`research/d9-dum-python/run_integration.py:25`、`research/d9-two-leg-486/run_integration.py:27`（`REPO / "platform" / "src"`）。前 10 处会直接运行失败，后 3 处 `sys.path.insert` **静默失效**不报错 | 一个"E3 补漏"commit 补 12 处 `src/` 前缀（`research/` 被 `extend-exclude` 排除，不会被 lint 抓到，必须一并手改）；不改历史 |
| **R-2** | `git show 2d8bfaa -- AGENT.md`：删除 §11 三条规则——"**Never push without the maintainer's explicit approval…Not push, not force-push, not tag**"、"**Agents do not create branches**"、"**Never commit keys, certificates, or real traffic captures**"，并把"文档链"一条移到 §5。当前 `AGENT.md` §11 只剩 "Nothing may enter main/master…" 一行。commit message 为 `reorignize path`，未声明。且 `CONTRIBUTING.md:69`、`docs/product/responsibility-matrix.md:42`、`docs/product/security-privacy.md:131,206` 仍在引用 `AGENT.md §11: never commit keys…` → **安全纪律条款被删 + 四处交叉引用悬空** | 恢复三条（默认建议）；若属有意放宽，则明示裁决并改四处引用 |
| **R-3** | **活文档断链 8 处**（链接存在性脚本实测）：`docs/plan.md:522`（`../platform/src/as_platform/sip/README.md`）、`docs/architecture/hld.md:52`、`docs/architecture/call-state-recovery-options.md:126`（7 处 `../../{platform,apps}/…`，同文件 L106-107 已是 `src/`，内部不一致＝漏改铁证）、`src/services/config-service/README.md:29`、`src/apps/anti-fraud/README.md:27`、`src/services/console/README.md:18,59`（四处 `../../docs/…`，E3 造成，迁移前正确）、`src/apps/README.md:23,44`（**新建即错**，应为 `../../docs/…`）、`docs/handoff/R2612_Struct_Plan.md:21`（`../../R2612_Cont.md`，自 `2d8bfaa` 起断） | 与 R-1 同批修：活文档插 `src/`；`src/*/README.md` 补一层 `../`；`R2612_Struct_Plan.md:21` 改 `./R2612_Cont.md` |

### P2 — 建议本批或下一批处理

| # | 事实（证据） | 建议值 |
|---|---|---|
| **R-4** | `R2612_Struct_Plan.md:284` 记"**225 处 rename**（186 纯 + 39 改）"；git 实测 `2e259c9` = **191**（170×R100 + 21×R081–R099） | 订正账本为 191（170 纯 + 21 带改），并说明与汇总"224"的口径差（224 含 `a81e13d` 22 + `4530d05` 11） |
| **R-5** | `R2612_Struct_Plan.md` 末行同句写 "**E8 done**" 与 "**the E8 changes await the 7th commit**"，且只枚举六笔 commit（缺 `c626031`/`d48785b`） | 删后半句，补两笔 commit |
| **R-6** | E6 的双口径：命中模块 docstring 即**整文件豁免**；且逐定义窗口不含定义自身 docstring（`postgres_store.py:135 PostgresVersionStore` 的 "See ADR-0006" 在 L136，不计入，靠文件级豁免才绿）。抽查 `RedisStateStore` / `ScaleDownPlan` / `may_remove` / `PostgresVersionStore` 均属此类 | docstring 命中改"豁免但计数告警"；或窗口扩到定义自身 docstring。与 ADR-0015 §④"reviewer 一步跳到 rationale"的张力需一句口径说明 |
| **R-7** | Makefile L40-44：依赖 `empty` 未被定义（`space := $(empty) $(empty)`）；路径含空格会被 `subst` 拆词破坏，前导/尾随/连续 `:` 产生的空条目被折叠（等价移除 cwd 搜索项）。仅在命中 ai-agent 时触发 | 加一行显式 `empty :=`；空格场景建议 `ifneq ($(findstring $(space),$(LD_LIBRARY_PATH)),)` 时跳过消毒保原值 |
| **R-8** | `docs/environments.md` §7 记 `restart=unless-stopped`，但 `deploy/` 全树无 `restart:` 键（compose 默认 no），策略来自 `docker update` → 不可复现 | `deploy/compose/compose.yml` postgres 补 `restart: unless-stopped`，§7 注明施加方式并登记三个 ad-hoc 容器的 `docker run` |
| **R-9** | `testbed/README.md:39` 仍写 testpaths `tests, platform, apps, services, testbed`；根 `pyproject.toml:59` 已是 `tests, src/platform, src/apps, src/services, testbed` | 同步 1 行（若文档守卫断言过该串需一并核对） |
| **R-10** | `docs/architecture/adr/0014-three-layer-testbed.md:76` 逐字引用旧 `testbed/README.md` 的三层表与三条规则（"Load testing must go through real sockets" / "v1 does not deliver the testbed…" / "SIPp…GPL, internal use only"），当前 README 三者全部 grep 不到 | 在 `testbed/README.md` 补回可引用原句（ADR 正文按裁决不动） |
| **R-11** | `scripts/README.md:17-20` 的"被 Makefile/gate 直接调用"对 `sync-chart-version.sh`、`d10-req-nf1-harness.sh`、`lib/repo-toolchain.sh` 不成立（Makefile 只引用 `demo-review/*` 与 `check_adr_annotations.py`） | 改措辞为"…or run manually as engineering capability"，或标注"当前未接入 target" |
| **R-12** | 活文档**文本**漂移（非链接，不判失败）：`README.md` 环境变量表与根目录树仍写 `apps/translation/src/…`、`services/config-service/…`、`platform/ apps/ services/`；`docs/architecture/lld.md:142,168`、`docs/product/one-pager.md:182`、`docs/product/compliance-matrix.md:93,277,280` 旧路径 | 与 R-3 同批处理 |
| **R-13** | ADR 正文链接断链：`0023:32,89,90,91`、`0024:79`、`0025:107,108`（`../../../{platform,apps,services}/…`） | **可接受**：按 E3 裁决 (a) 正文不改；维持登记，不改 |
| **R-14** | `R2612_Struct_Plan.md` 的 F-1…F-10 是"结构发现"编号，与仓库既有 `REQ-F-9`（`docs/plan.md:82`、`R2612_Cont.md:54`）同名不同义 | 改称 `S-F-n`，或在该编号首次出现处加一句命名空间声明 |
| **R-15** | 汇总文档三处口径：`docs/README.md` 补全实测 **6 行**（`requirements/`、`design/`、`SIP_stack_selection.md`、`agents/`、reviews 索引、handoff 索引）非 5 行；handoff 索引"36 条"是 `3b1c873` 时值（HEAD 38，`c626031`/`d48785b` 各 +1）；rename "224" 不含两次文档归位（范围总数 226） | 订正三处数字（属汇总文档自身的订正，非代码缺陷） |
| **R-16** | `.gitignore` 的 `.codebuddy/teams/` 落在末尾"Office temporary lock files"段之后，语义应属 L46-51 的 agent session 段 | 移动两行（可选，纯卫生） |

---

## 4. 实测为绿的项（正面证据）

| 项 | 证据 |
|---|---|
| 门禁守卫 | `uv run pytest -q tests/test_layer_boundaries.py src/platform/tests/test_library_independence.py tests/test_workspace_layout.py` → **87 passed**（四层分类、`REPOSITORY_ROOT` 深度、`KERNEL_SOURCE` 插 `src`、成员判定 `src/platform` 自洽） |
| REQ-G-3 扫描器 | `python3 scripts/check_adr_annotations.py` → **`checked 73 files` / `check_adr_annotations: clean`**；`_repo_root` L101 `parents[1]`；GRANDFATHERED 仍 23 条、阈值未动 → 非"放宽变绿" |
| 两份新索引 | 链接存在性脚本：`docs/handoff/README.md` 38/38 通、`docs/reviews/README.md` 162/162 通；与 `git ls-files` 计数（39 / 163）自洽 |
| manifest 与锁 | 根 `pyproject.toml` 五键带 `src/`（`extend-exclude` 指向 `testbed/…` 无需改，判断正确）；`uv.lock` 16 条 editable 全 `src/…`，零旧根；成员 7→8（`as-probe`） |
| E1 脚本归位 | `deploy/kind/scripts/` 16 个 `m5-*.sh`；抽查 `m5-verify.sh:16`、`m5-7.2d-evidence.sh:16`、`m5-lib.sh:17,25` 的 `dirname "$0"/../../..` 三层正确；Makefile L92/95/98/101 四 target 同步；e2e 保史注记只追加（L69-70）原文未动 |
| 卫生 | `.codebuddy/teams` 去跟踪实测 D×6；根目录已无 `platform/ apps/ services/` |
| E7 | 10 个测试文件各加 1 行 `"server closed the connection unexpectedly"`（`git show 4530d05` 精确核对）；`src/services/config-service/tests/` 无根残留 |
| E8 | Makefile L37-44 位于全部规则之前、`export UV` 之后；未污染环境 `ifneq` 守卫零改动 |
| C | `d48785b` 纯 rename，§1–§6 结论与 F-/Q- 裁决原样未动，仅处置格更新 → 在保史边界内 |

---

## 5. 结论

**accept with fixes —— 10 笔 commit 的主体（src/ 收拢、workspace 与锁、门禁守卫、REQ-G-3 扫描器修复、容器治理、LD_LIBRARY_PATH 消毒、文档归位）方向正确、实测可复核、无"放宽守卫换绿"痕迹。**

必须在 push 前处理 **B1 / B2 / B3**（R-1 可执行路径 12 处、R-2 `AGENT.md` 三条规则被删 + 四处引用悬空、R-3 断链 8 处）；P2 六项建议同批或下一批处理。**本评审不替代 `make gate` 全量复跑**（未执行），也不闭环任何里程碑。

**2026-10-30 补漏批次后**：B1 / B3（R-1、R-3）已修；B2 经维护者裁决打回（`AGENT.md` 不动，不再阻塞 push，其引用 follow-up 已改指 §13）；R-4/R-5/R-6/R-7/R-8/R-9/R-10/R-11/R-12/R-14/R-15/R-16 均已修（R-6 走"豁免但计数告警"，`make gate-strict` 复跑 clean、21 条 docstring-only 浮出）。本评审仍不替代 `make gate` 全量复跑（未执行），也不闭环任何里程碑。落地范围与"仍未随 commit"的例外见 §9。

本记录**未覆盖**工作区 24 个已改文件与 14 个未跟踪文件。

## 6. 签署

| Role | Name | Date | Signature |
|---|---|---|---|
| Reviewer（AI agent，代） | AI agent（6 子 agent 分工 + 父级复核） | 2026-10-30 | 见上文 |
| **Maintainer（本人签署）** | | | **待维护者填写** |

## 7. 下游

1. B1–B3 落地 → 才谈 push 与 commit 切分（十个 commit 全在本地，`master` 仍在 `c3b951e`）。
2. R-4 / R-5 属账本诚实性修正，建议与 B1 同批，避免账本与 git 长期背离。
3. R-6 的口径若改动，会触发 `check_adr_annotations.py` 行为变化 → 需重跑 `make gate-strict` 并如实记录。

## 8. Adjudication

| ID | 来源 | 问题摘要 | 裁决 | 修改方案 | 状态 | 验证方式 | 备注 |
|---|---|---|---|---|---|---|---|
| R-1 | `2e259c9` E3 | 6 文件 12 处路径仍指旧根，前 10 处运行失败、后 3 处 sys.path 静默失效 | 必须修 | 补 `src/` 前缀，一个"E3 补漏"commit | 已修（2026-10-30 补漏批次，随补漏 commit） | 逐个脚本 dry-run + `git grep` 复扫 | 阻塞 push |
| R-2 | `2d8bfaa` | `AGENT.md` §11 三条硬规则被静默删除，四处文档引用悬空 | **维护者裁决：AGENT.md 不动（打回「恢复三条」建议）** | 不改 `AGENT.md`；引用改指向现行条款：密钥/证书/抓包 → `AGENT.md` §13（实测 **8 文件 16 处**，评审件正文的"四处"为计数偏少） | **已裁决 + follow-up 已修**（2026-10-30） | `grep` §11 复核：`docs/operations/{README,runbook-l1,runbook-l2,fault-demarcation,backup-restore}.md`、`docs/product/{security-privacy,responsibility-matrix}.md`、`docs/environments.md` | 不再阻塞 push；剩余的 §11 引用见 §9 例外 |
| R-3 | `2e259c9` / `2d8bfaa` | 活文档断链 8 处（4 处 E3 造成、2 处新建即错、1 处规划文档自链） | 必须修 | 插 `src/` / 补 `../` / 改 `./R2612_Cont.md` | 已修（2026-10-30 补漏批次，随补漏 commit） | 链接存在性脚本复跑 | 阻塞 push |
| R-4 | `R2612_Struct_Plan.md:284` | 账本 rename 225 vs git 实测 191（170 纯 + 21 改） | 订正账本 | 改为 191 并说明口径 | 已修（2026-10-30 补漏批次，随补漏 commit） | `git show --name-status --diff-filter=R 2e259c9` | 诚实性 |
| R-5 | `R2612_Struct_Plan.md` 末行 | 同句 "E8 done" 与 "await the 7th commit" 矛盾，commit 枚举缺两笔 | 订正账本 | 删后半句 + 补 `c626031`/`d48785b` | 已修（2026-10-30 补漏批次，随补漏 commit） | 人工复核 | 诚实性 |
| R-6 | `3f035af` E6 | docstring 命中＝整文件豁免；逐定义窗口不含定义自身 docstring | 维护者采纳：豁免但**计数告警** | 模块 docstring 仍豁免，但每个"只靠 docstring 通过"的名字逐条打印非致命 warning（口径说明写入脚本 docstring） | **已修**（2026-10-30） | `make gate-strict` 复跑：clean、exit 0，**21 条 docstring-only 全部浮出** | 与 ADR-0015 §④的张力已加一句口径说明 |
| R-7 | `c626031` E8 | Makefile 依赖 `empty` 未定义；含空格路径被破坏、空条目被折叠 | 加固（建议） | 加 `empty :=`；空格场景跳过消毒 | 已修（2026-10-30 补漏批次，随补漏 commit） | 构造含空格 `LD_LIBRARY_PATH` 试跑 | 仅命中 ai-agent 时触发 |
| R-8 | `4530d05` E7 | `restart=unless-stopped` 无仓库内定义，不可复现 | 补声明（建议） | compose.yml 补 `restart:` + §7 注明施加方式 | 已修（2026-10-30 补漏批次，随补漏 commit） | `docker compose config` 复核 | 运行态事实 |
| R-9 | `d32ff79` E2 | `testbed/README.md:39` testpaths 未随 E3 同步 | 修 1 行 | 改 `src/` 前缀 | 已修（2026-10-30 补漏批次，随补漏 commit） | 与根 `pyproject.toml:59` 比对 | — |
| R-10 | `d32ff79` E2 | ADR-0014 L76 逐字引用的三条规则在当前 README 已不存在 | 补回原句（建议） | `testbed/README.md` 补可引用句，ADR 正文不动 | 已修（2026-10-30 补漏批次，随补漏 commit） | grep 三条原句 | 裁决 (a) |
| R-11 | `d32ff79` E2 | `scripts/README.md:17-20` "被 Makefile 直接调用"对 3 个条目不成立 | 改措辞 | 改"run manually"或标注未接入 target | 已修（2026-10-30 补漏批次，随补漏 commit） | Makefile grep | — |
| R-12 | E3 活文档 | `README.md` / `lld.md` / `one-pager.md` / `compliance-matrix.md` 旧路径文本 | 同批修 | 插 `src/` | 已修（2026-10-30 补漏批次，随补漏 commit） | `git grep` 复扫 | 非链接，不判失败 |
| R-13 | E3 裁决 (a) | ADR 0023/0024/0025 正文链接断链 | 可接受，不改 | 维持登记 | 已裁决 | — | 正文不改 |
| R-14 | `0d740d4` | 结构发现 F-9 与 REQ-F-9 同名不同义 | 消歧（建议） | 改称 `S-F-n` 或加命名空间声明 | 已修（2026-10-30 补漏批次，随补漏 commit） | grep 冲突处 | 编号体系 |
| R-15 | 汇总文档 | docs/README 补全 6 行（非 5）；handoff 索引 36→38；rename 224 vs 226 | 订正汇总 | 三处数字订正 | 已修（2026-10-30 补漏批次，随补漏 commit） | `git show` 复核 | 文档自身口径 |
| R-16 | `a81e13d` | `.codebuddy/teams/` 落在 `.gitignore` 错误段落 | 可选 | 移到 agent session 段 | 已修（2026-10-30 补漏批次，随补漏 commit） | 人工 | 纯卫生 |

## 9. 落地说明（2026-10-30 补漏批次）

**一个 commit，只含下列文件的修改**（工作区其余已改 / 未跟踪文件一处未带入）：

| 项 | 文件 |
|---|---|
| R-1 | `testbed/load/scripts/m6-{product-runtime-smoke,product-runtime-micro-measure,product-runtime-measure-60s,o1-formal-report}.sh`、`testbed/load/tests/test_product_runtime_smoke.py`、`deploy/kind/scripts/m5-7.2d-evidence.sh`、`testbed/simulators/resip-probe/d10-recovery/orchestrate.py`、`…/research/d9-{dum-python,two-leg-486}/run_integration.py` —— 实测共 **9 个文件 14 处**（评审件正文的"6 文件 12 处"为计数口径偏少，以磁盘复扫为准） |
| R-3 | `docs/plan.md`、`docs/architecture/hld.md`、`docs/architecture/call-state-recovery-options.md`、`src/{services/config-service,services/console,apps,apps/anti-fraud}/README.md`、`docs/handoff/R2612_Struct_Plan.md` |
| R-4 / R-5 / R-14 | `docs/handoff/R2612_Struct_Plan.md` |
| R-7 | `Makefile` |
| R-8 | `deploy/compose/compose.yml`、`docs/environments.md` |
| R-9 / R-10 | `testbed/README.md` |
| R-11 | `scripts/README.md` |
| R-12 | `docs/architecture/lld.md`、`docs/product/one-pager.md`、`docs/product/compliance-matrix.md` |
| R-15 | `docs/README.md`（handoff 索引 36 → 38） |
| R-16 | `.gitignore` |

**已改但刻意未随该 commit**（都落在维护者当前未提交内容里，避免混入）：

| 项 | 文件 | 原因 |
|---|---|---|
| R-15（三处数字） | `docs/handoff/2026-10-30-r2612-committed-summary.md`（未跟踪） | 属"现有未提交内容"；已在工作树订正，随后与评审件一并单独 commit |
| R-2 裁决标记 | 本评审件（未跟踪） | 同上 |

### 后续两个 commit（2026-10-30，同批）

| commit | 内容 | 验证 |
|---|---|---|
| R-6 | `scripts/check_adr_annotations.py`：模块 docstring 仍豁免，但"只靠 docstring 通过"的名字逐条打印非致命 warning；口径说明写入脚本 docstring | `make gate-strict` 复跑：**clean / exit 0**，21 条 docstring-only 全部浮出（`downscale_guard`、`adapter`、`call_controller`×2、`ingress`、`in_memory`、`redis_store`×2、`telemetry/*`×8、`auth.py`×6 分布） |
| R-2 follow-up | 8 个活文档 16 处 `AGENT.md §11` 引用改指 §13（Security）| `grep` 复扫 |

**仍未随任何 commit**（工作树）：

| 项 | 文件 | 原因 / 建议值 |
|---|---|---|
| R-12 的 `README.md` 两处 | `README.md` L272 / L280（已改好） | 该文件已被未提交的 134 行环境变量表占用，git 只能整文件提交 → 随维护者下一批提交 |
| §11 引用（git 规则类） | `docs/product/version-lifecycle.md` L132/L261、`docs/operations/rollback-playbook.md` L135 | 两个文件均已脏 → 同上，随下一批改 |
| §11 引用（ADR 正文 / 历史记录） | `docs/architecture/adr/0018:78`、`0015:81`；`docs/reviews/*`、`docs/handoff/*` 若干 | 按裁决 (a)：ADR 正文与史实记录不改（ADR-0018/0015 引用的"Git rules / Do not skip hooks"条款在现行 §11 仍在，非悬空） |
| agent 侧三条规则 | `.codebuddy/rules/hard-rules.md`、`\.trae/rules/hard-rules.md` | 未动：两条"Git 红线"章节逐字保留着被删的三条规则，是纪律的实际存身处 —— 建议值：将来引用可指向这两处 |

**未做**：R-2 本体（`AGENT.md` 不动，维护者裁决）、R-13（已裁决不改）。
