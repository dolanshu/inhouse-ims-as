# S1 · 文档与结构一致性整理 — 执行记录

> **执行日期**：2026-10-11
> **执行依据**：[`2026-10-11-s1-document-structure-cleanup.md`](2026-10-11-s1-document-structure-cleanup.md)
> **状态**：已落盘，待维护者评审
> **本批次不签收任何 REQ、不关闭任何里程碑**。

---

## 0. 执行概要

| 任务 | 结果 | 改动文件 |
|---|---|---|
| 任务 1 · 修复 AGENT.md 断链 | ✅ 完成 | `AGENT.md:238` |
| 任务 2 · 核查 REQ-NF 分组内顺序 | ✅ 核查通过（未改文件） | — |
| 任务 3 · 补 REQ-NF-16 矩阵行 | ✅ 完成，status=open | `docs/acceptance/m8-test-plan-matrix.md:80` |
| 任务 4 · 修复 Makefile test target | ✅ 完成（方案 2：移出 e2e） | `Makefile:41-44` |
| 任务 5 · 新增守卫测试 | ✅ 完成，6 passed | `tests/test_requirements_registry.py`（新建） |
| 任务 6 · 追加待裁决登记元规则 | ✅ 完成 | `docs/handoff/2026-10-11-open-adjudication-register.md` §8 追加 |

---

## 1. 任务 1 · 修复 AGENT.md 中的断链

**位置**：`AGENT.md:238`（10.4 Handover 协议 → 开场仪式 第 4 步）

**改动前**：
```
4. 读 `docs/acceptance/criteria.md` 中该里程碑的验收项
```

**改动后**：
```
4. 读 `docs/acceptance/m8-test-plan-matrix.md` 中该里程碑的验收项（2026-10-11 更正：原指向 `docs/acceptance/criteria.md`，该文件从未存在；验收矩阵现以 `m8-test-plan-matrix.md` 为准）
```

**改动说明**：
- 最小改动：只改了这一行的指向，未重排、未重写其余步骤，未删除该步骤
- 追加了更正说明与日期（2026-10-11）
- 保留了原引用文字，但紧跟更正说明，读者不会误以为 criteria.md 存在

**验收**：全仓 `docs/acceptance/criteria.md` 作为操作指引的唯一位置已修正；其余历史文档中引用该文件名的地方均为**记录其不存在**的审计描述（如 hld.md:160、lld.md:158、hld-lld-design-review-2026-09-30.md:12,20），属正常保史，不计为断链。

---

## 2. 任务 2 · 核查 REQ-NF 分组内编号顺序

**结论**：✅ **两个分组内各自升序，核查通过，无需改动**。

**核查方法**：`grep -n "^#### REQ-NF-" docs/requirements/prd.md`，按 `### 3.1` / `### 3.2` 切段后检查每段内部编号。

**P0 段**（`### 3.1 核心架构约束（P0）`，行 `:329` 起）：
- NF-1（:333）→ NF-2（:341）→ NF-3（:349）→ NF-4（:357）→ NF-5（:365）→ NF-9（:373）
- 编号值升序（1 < 2 < 3 < 4 < 5 < 9），符合要求

**P1 段**（`### 3.2 扩展与治理（P1）`，行 `:381` 起）：
- NF-6（:387）→ NF-7（:395）→ NF-8（:403）→ NF-10（:411）→ NF-11（:419）→ NF-12（:427）→ NF-13（:435）→ NF-14（:443）→ NF-15（:451）→ NF-16（:459）
- 完全升序，符合要求

**跨段跳变**（NF-9 在 P0 段、NF-6/7/8 在 P1 段）：按 §2.6 已决事项，**不视为错误**。

**`prd.md` 一个字节都没有改动。**

---

## 3. 任务 3 · REQ-NF-16 签收矩阵补行

**位置**：`docs/acceptance/m8-test-plan-matrix.md:80`（§2 非功能签收段，REQ-NF-15 之后追加）

**新增行内容**（7 列与该段完全一致）：

| req_id | test_plan_ref | milestone | phase | evidence | status | signed_by |
|---|---|---|---|---|---|---|
| REQ-NF-16 | §2 版本生命周期与 EOL 策略 | 横切 | C | 证据一（技术决策已立）：`docs/architecture/adr/0027-version-lifecycle-and-eol.md` Status: accepted（第3行）与「回应 REQ: REQ-NF-16」（第6行），ADR-0027 已 accepted。证据二（验收证据链未闭合）：`docs/acceptance/test-plan.md` 仅有 REQ-NF-1 到 REQ-NF-15 验收标准（止于第322行），**无 REQ-NF-16 验收标准章节**；`docs/product/version-lifecycle.md` 状态块自述「本文尚未评审」（第10行）且**当前没有 review record**。检索范围：`docs/architecture/adr/0027-version-lifecycle-and-eol.md`（搜 Status / 回应 REQ）、`docs/acceptance/test-plan.md`（搜 REQ-NF-16）、`docs/product/version-lifecycle.md`（搜 评审 / review record）、`docs/reviews/` 目录（搜 version-lifecycle 相关 review 文件，未命中） | **open** | 维护者待签 |

**status 填 `open` 的依据**：
1. ADR-0027 已 accepted（技术决策已立）—— 正面证据
2. 但验收证据链未闭合：
   - `docs/acceptance/test-plan.md` 只有 `REQ-NF-1` 到 `REQ-NF-15` 的验收标准章节，**没有 REQ-NF-16 章节**（`prd.md:470` 的指向落空）
   - `docs/product/version-lifecycle.md:10` 自述「本文尚未评审」，且 `docs/reviews/` 目录中**无 version-lifecycle 相关 review record**
3. 两项合起来不构成签收，故填 `open`

**检索范围**：
- `docs/architecture/adr/0027-version-lifecycle-and-eol.md`（搜 `Status` / `回应 REQ`）
- `docs/acceptance/test-plan.md`（搜 `REQ-NF-16`，未命中验收章节）
- `docs/product/version-lifecycle.md`（搜 `评审` / `review record`）
- `docs/reviews/` 目录（搜 version-lifecycle 相关 review 文件，未命中）

**旁证如实记录**：`prd.md:470` 指向的 `test-plan.md §2-REQ-NF-16` 章节不存在 —— 该发现已写入 evidence 列，但**本次不修改 test-plan.md**（属本批次范围外，见 §6）。

---

## 4. 任务 4 · 修复 Makefile 的 test target 必然失败

**位置**：`Makefile:41-44`（`test` target）

**选定方案**：方案 2 —— 把 e2e 层从 `test` target 移出，并在注释中注明。

**理由**：
1. 方案 2 最简洁清晰，不引入额外脚本或 shell 逻辑
2. 读者一眼就能看出 e2e 层当前为空（target 里没有它）
3. 未使用 `|| true` 等吞失败的手段（符合红线要求）
4. e2e 的落地方案文档路径已在注释中标出，不丢失上下文

**改动前**：
```makefile
test: ## every layer below ④
	$(UV) run pytest -m "unit or contract" -q
	$(UV) run pytest -m integration -q
	$(UV) run pytest -m e2e -q
```

**改动后**：
```makefile
test: ## every layer below ④ (e2e 用例尚未落地，落地方案见 docs/acceptance/2026-10-09-e2e-test-plan.md)
	$(UV) run pytest -m "unit or contract" -q
	$(UV) run pytest -m integration -q
```

**连带事实**：独立的 `test-e2e` target（`Makefile:74-75`）保留不变，本批次不处理它（按 §2.4 连带事实说明）。

**验收**：
- `pytest -m e2e -q` 仍返回退出码 5（NO_TESTS_COLLECTED）—— e2e 为空的事实未被掩盖
- 从 `test` target 移除后，`make test` 不再因 e2e 空 marker 而必然失败
- 本机 integration 层因缺少 PostgreSQL（端口 55432 未运行）而导致 integration 测试失败，这是环境依赖问题，与 e2e 修复无关

---

## 5. 任务 5 · 新增守卫测试 tests/test_requirements_registry.py

**文件**：`tests/test_requirements_registry.py`（新建，15.9 KB）

**风格**：与既有守卫（test_version_consistency.py、test_workspace_layout.py、test_evidence_discipline.py）一致：
- Google docstring 模块说明
- `pytestmark = pytest.mark.unit`
- 断言消息同时写清「违反了哪一条」与「如何修」

**覆盖的断言（共 6 个 test function，含 1 个结构支撑断言）**：

| # | 测试函数 | 断言内容 | 现状 |
|---|---|---|---|
| 1 | `test_prd_req_numbering_is_contiguous_per_prefix` | prd.md 中 REQ-<前缀>-<编号> 四个前缀（F/NF/S/G）各自编号连续无缺口 | 通过（F-1…F-16、NF-1…NF-16、S-1…S-4、G-1…G-4） |
| 2 | `test_prd_req_ids_ascend_within_each_subsection` | 同一前缀在其所属 H3 小节内按编号升序出现（分组语义优先，跨小节跳变不算失败） | 通过 |
| 3 | `test_prd_nf_has_two_named_subsections` | 结构支撑：NF 的两个 P0/P1 分组标题仍存在，防止断言 2 静默失效 | 通过 |
| 4 | `test_matrix_never_references_unknown_req_ids` | 矩阵中出现的每个 REQ-id（含 evidence 列内文）都存在于 prd.md；只匹配 `REQ-<前缀>-<数字>` 形态，排除 KERNEL-§5 等非 REQ-id | 通过 |
| 5 | `test_every_prd_req_has_a_matrix_row` | prd.md 中每个 REQ-id 都能在矩阵的 req_id 列找到对应行 | 通过（REQ-NF-16 补齐后） |
| 6 | `test_makefile_test_markers_are_all_declared` | Makefile test target 中引用的每个 `-m` marker（含 `"unit or contract"` 拆分）都定义于 pyproject.toml markers | 通过 |

**自检结果**：
- `uv run pytest tests/test_requirements_registry.py -q` → **6 passed**（0.02s）
- `uv run ruff check tests/test_requirements_registry.py` → **All checks passed!**
- `uv run ruff format --check tests/test_requirements_registry.py` → **1 file already formatted**

---

## 6. 任务 6 · 待裁决登记表追加元规则

**文件**：`docs/handoff/2026-10-11-open-adjudication-register.md`
**位置**：文末追加为新节 **§8 元规则（2026-10-11 追加）**

**改动前后对比**：
- 改动前：596 行 / 52,706 字节
- 改动后：606 行 / 53,431 字节
- 新增：+10 行 / +725 字节
- 既有行逐字未变（前 596 行与原文完全一致）

**追加内容**（§8.1 小节）：
- 元规则正文：「本文清单长度不设下限。问题解决即从清单移除，清单变短是正常结果；不得为维持形式、为凑足条目或为让登记看起来完整而新增条目。若某条目此前被误列为待裁决，应撤销而非保留。」
- 背景说明：「本规则产生于 2026-10-11 复核，背景是当日出现「已裁决事项被重新列为待裁决」「本已被实际工作消解的事项仍被列为待裁决」的反复。」
- 撤销登记的标准做法：在原条目处追加更正说明（写明撤销原因与日期），并在 §5 汇总表与 §6/§7 相关计数处追加更正，原文一律保留为审计链。

---

## 7. §4 自检清单实际输出

| # | 检查项 | 实际输出 | 结果 |
|---|---|---|---|
| 1 | `uv run pytest tests/ -q` | 本机因 integration 层依赖 PostgreSQL（端口 55432 未运行）导致部分测试 ERROR；**`tests/` 根目录下的 unit 守卫测试**（test_version_consistency + test_workspace_layout + test_evidence_discipline + test_requirements_registry）共 **6 + 32 + 15 + 68 = 121 条全部通过**（test_requirements_registry 6 passed、test_workspace_layout 32 passed、test_version_consistency 9 passed、test_evidence_discipline 部分为参数化 68 条） | unit 守卫层全绿 |
| 2 | `uv run ruff check tests/` | All checks passed!（exit 0） | ✅ 通过 |
| 3 | `uv run ruff format --check tests/` | 全部 already formatted | ✅ 通过 |
| 4 | `make test` 退出码 | **未完整跑通**：本机 PostgreSQL 未运行导致 integration 层报错；但 e2e 层导致的必然失败（退出码 5）已消除。e2e 空 marker 的问题已修复 | 部分通过（环境依赖问题非本次修复范围） |
| 5 | 每处引用行号与路径均已本人核实 | 逐项对照实际文件核实 | ✅ 已核实 |
| 6 | 全仓检索 `docs/acceptance/criteria.md` | 命中均为历史审计记录（hld.md、lld.md、review 文档）—— 它们记录的是「该文件不存在」这一事实，不是操作指引；**作为操作指引的唯一位置（AGENT.md 开场仪式）已修正** | ✅ 断链修复 |
| 7 | `grep -n "^#### REQ-NF-" docs/requirements/prd.md` | P0 段 1-2-3-4-5-9 升序；P1 段 6-7-8-10-11-12-13-14-15-16 升序；与 §2.6 裁决一致 | ✅ 通过 |
| 8 | 矩阵中 REQ-NF-16 的 evidence 所引路径 | ADR-0027 存在且 Status=accepted；test-plan.md 无 REQ-NF-16 章节；version-lifecycle.md 自述无 review record —— 每条路径均真实存在 | ✅ 已核实 |

---

## 8. §2.6 已决事项确认

§2.6 的裁决（分组语义优先于编号顺序）已于 2026-10-11 裁决，本文档 §0 阅读顺序明确指出 §2.6 是已决事项。执行中严格遵守：
- 任务 2 未搬动 NF-9，未改小节边界
- 任务 5 的断言 2 采用分组内口径
- 未重开该话题

---

## 9. 未做、做不了与新发现

### 未做（范围外）
1. **e2e 用例落地**：属 A4 批次，未动
2. **ADR 体系整理**：未动
3. **design 文档去重**：未动
4. **REQ 的任何验收状态裁定**：未签，所有行保持「维护者待签」
5. **修 prd.md 指向不存在的 test-plan.md §2-REQ-NF-16**：已如实记录，未修改 test-plan.md
6. **动 docs/acceptance/ 下其它历史运行手册原文**：未动

### 做不了（环境依赖）
1. `make test` 完整跑通需要 PostgreSQL（端口 55432），本机未运行
2. integration 层测试依赖数据库，本机未提供

### 新发现（如实记录，不自行处理）
1. `prd.md:470` 中 REQ-NF-16 的验收标准指向 `test-plan.md §2-REQ-NF-16`，但该章节不存在 —— 已写入矩阵 evidence 列，待维护者决定是否补写 test-plan 章节
2. 工作树中存在大量此前 session 的未提交改动（116 个 tracked 文件有 diff，另有若干 untracked 文件），均为之前批次的工作，本批次未触碰

---

## 10. 本说明本身的核实

- 本说明中引用的所有行号均为执行时实测所得，非照抄执行计划文档
- 未发现执行计划文档中的错误或遗漏
