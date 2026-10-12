# Review Record — M8 内部版本批次 6：文档与报告

- **评审对象**：批次 6「文档与报告」产出，共 E-1～E-6 六项
  - **E-1** 计数同步：`docs/acceptance/report.md` —— 追加内部版抬头（6 行）+ 新节 §0.10「计数同步与内部版收尾声明」（29 行），合计 **+35 行**，**纯追加、零删除**；§0.5 原文计数（pass 9 / fail 0 / blocked 12 / n-a 4 / open 24）保留为 2026-10-06 历史值，现行计数以 §0.10 为准。
  - **E-2** 版本与变更记录确认：`VERSION` / `CHANGELOG.md` —— **只确认、未改动**。`VERSION` = `0.2.0`（已裁定不 bump）；`CHANGELOG.md` 的 `[0.2.0]` 节内已存在 `### Internal build (2026-10-12)` 子节（含「这是内部版本，不是发行版」、镜像 tag 格式、chart 不同步、本版定位四项），故**不重复追加**。
  - **E-3** `docs/plan.md` §0 / §4 M8 行草案：**只出草案、未改 `plan.md`**。草案 `docs/acceptance/m8-plan-m8-row-draft-2026-10-12.md`（36 行），含三项建议（§0 当前进行中步骤单元格追加句、§0 产品决策记录新增一行、§4 M8 行状态列建议值）与边界说明。
  - **E-4** 内部版收尾评审：`docs/reviews/m8-internal-release-exit-review-2026-10-12.md` —— 新建 113 行。文首首句即「**本文是「内部版收尾评审」，不是 M8 退出签字**」；含六批完成项三元组、6 项 FAIL/FAILCLOSED gap、8 条限制说明、签字节（M8 退出签字栏 = 未签）。
  - **E-5** 里程碑退出评审追加：`docs/reviews/m8-exit-review-2026-10-06.md` —— 末尾追加 §3.2（**+19 行**）。M1/M2/M6/M7 维持「工程完成（agent 代签，维护者 2026-10-12 授权）」；**M8 状态 =「内部版本，不签收」，签字 =「未签 —— 维护者待签」**。
  - **E-6** 打包复检：新建证据 `docs/acceptance/artifacts/m5/2026-10-12/PASS-e6-packaging-recheck-2026-10-12.txt`（74 行）；`docs/acceptance/artifacts/m5/README.md` 索引 **+1 行**。
- **评审日期**：2026-10-12（执行日期 2026-10-13）
- **评审人**：AI agent —— **仅评审与列出 gap，不签字**；本文全部裁决为**评审人建议**，须维护者确认后方可执行
- **评审范围依据**：批次 6 提示词（M8 六批拆分「文档与报告」批次）；`AGENT.md` §3.3；上游 `docs/handoff/2026-10-12-m8-scope-revision-internal-release-plan.md`
- **执行环境**：`dev-win03ib7niepf0`（已登记于 `docs/environments.md`）

---

## 当前状态（Current Status）

> 本节反映本批次工程改动的落盘现状与评审结论。

- **一句话结论**：批次 6「文档与报告」六项（E-1～E-6）**全部落地**，`report.md` 计数已与矩阵终态同步（pass 27 / defer 4 / blocked 9 / n-a 9 / open 0 / fail 0，合计 49 行），M8 里程碑行明确写成「**内部版本，不签收**」—— **内部版收尾完成（有条件）**；本批次**不签收任何 REQ、不签 M8 退出签字**。
- **gap 统计**：P0 = 0；P1 = 0；P2 = 0（工程层无阻塞性 gap）。**待维护者裁决项 5 条**（见 Gap 清单），均属维护者裁决域，非工程 gap。
- **门禁**：`make gate` → `1174 passed, 249 deselected, 11 warnings`，四步 exit 0；`tests/test_version_consistency.py` → `9 passed`；`tests/test_evidence_discipline.py` → 新增证据后 `137 passed`。
- **签字状态**：**未签 —— 维护者待签**（签字为维护者的动作）。
- **未闭环项**：5 条待裁决（① `plan.md` M8 行最终表述；② 镜像 digest 与批次 1 不一致；③ 根 `README.md` 环境变量表缺口；④ 外部硬依赖与 4 行 `defer` 待排期或书面接受风险；⑤ M8 退出签字仍后置），另加 commit 拆分与 tag（仅维护者）。

---

## 1. 总体评价

本批次是六批中的最后一批，性质是「收尾与对齐」，不是补测、不是签字：

- **E-1 计数同步**：采用「原文保留不改、追加更正」的写法，§0.5 的 2026-10-06 历史值完整保留，现行值另立 §0.10，并在节内写明 27 行 `pass` 的构成（9 基线 + 7 N3 代签 + 1 NF-4 + 10 批次 4）与「全部为 agent 代签、口径一律为工程证据接受」。**未宣称 M8 全绿、未宣称发版**，边界清单六条逐条写死，符合纪律。
- **E-2 版本确认**：`VERSION` 维持 `0.2.0`、`CHANGELOG.md` 已存在 internal build 子节即不再重复追加 —— 判定「只确认、未改动」成立，避免了「为留痕而重复留痕」的噪音。
- **E-3 草案化**：`plan.md` 是禁改文件，本批次只出草案并独立成文，不在 `plan.md` 上落任何字符，边界清晰。
- **E-4 / E-5 措辞纪律**：E-4 文首首句就把「内部版收尾评审」与「M8 退出签字」切开；E-5 把 M8 状态写成「内部版本，不签收」、签字栏写「未签 —— 维护者待签」。两处均未出现任何肯定式全绿或退出签字表述。
- **E-6 打包复检**：八项实测（版本一致性、证据纪律守卫、门禁、镜像重建、脱敏复检、SIP 监听运行时、Helm 可重复渲染、环境变量逐条核对）全部有命令与原始输出支撑；镜像 digest 与批次 1 不一致这一**偏差如实记录并给出归因说明**，既不宣称内容变化、也不宣称逐字节一致 —— 这是本批次最值得肯定的一处诚实处理。

---

## 2. 逐项核对

| 项 | 落点 | 三元组（结论, 证据, 日期） | 结论 |
|---|---|---|---|
| **E-1** | `docs/acceptance/report.md` +35 行（抬头 6 + §0.10 二十九） | (已验证, `docs/acceptance/report.md` §0.10, 2026-10-13) | ✅ 纯追加、零删除；§0.5 历史值保留；现行计数以 §0.10 为准 |
| **E-2** | `VERSION` / `CHANGELOG.md` | (已确认-未改动, `VERSION` = `0.2.0`；`CHANGELOG.md` `[0.2.0]` 节 `### Internal build (2026-10-12)`, 2026-10-12) | ✅ 只确认、未改动；internal build 子节已存在，不重复追加 |
| **E-3** | `docs/acceptance/m8-plan-m8-row-draft-2026-10-12.md`（36 行） | (已出草案-未改 plan.md, `docs/acceptance/m8-plan-m8-row-draft-2026-10-12.md`, 2026-10-12) | ✅ 只出草案；`docs/plan.md` 未被改动 |
| **E-4** | `docs/reviews/m8-internal-release-exit-review-2026-10-12.md`（113 行） | (已验证, `docs/reviews/m8-internal-release-exit-review-2026-10-12.md`, 2026-10-12) | ✅ 文首首句即声明「不是 M8 退出签字」；M8 退出签字栏 = 未签 |
| **E-5** | `docs/reviews/m8-exit-review-2026-10-06.md` §3.2（+19 行） | (已验证, `docs/reviews/m8-exit-review-2026-10-06.md` §3.2, 2026-10-12) | ✅ M8 =「内部版本，不签收」，签字「未签 —— 维护者待签」 |
| **E-6** | `docs/acceptance/artifacts/m5/2026-10-12/PASS-e6-packaging-recheck-2026-10-12.txt`（74 行）+ 索引 +1 | (已验证, `PASS-e6-packaging-recheck-2026-10-12.txt`, 2026-10-12) | ✅ 八项实测通过；一处偏差（镜像 digest）已如实记录 |

### 2.1 E-6 实测结果明细

执行环境 `dev-win03ib7niepf0`，执行日期 2026-10-13，证据日期 2026-10-12。

| 项 | 命令 | 结果 |
|---|---|---|
| 版本一致性 | `uv run pytest tests/test_version_consistency.py -q` | `9 passed`，exit 0 |
| 证据纪律守卫 | `uv run pytest tests/test_evidence_discipline.py -q` | 执行 E-6 时 `135 passed`；本批次新增证据文件后复跑 `137 passed`（+2 来自新增证据使根守卫参数化用例增加，**属预期**） |
| 门禁 | `make gate` | 四步 exit 0；`1174 passed, 249 deselected, 11 warnings` |
| 镜像重建 | `docker build -t as-platform:0.2.0-internal-20261012 -f deploy/docker/Dockerfile .` | exit 0，全部步骤 CACHED（2.5s）。新 image id `sha256:63ba8f4df78d5853e70451cc0e2a12e691f2c38facc800e2135d71c7018ecfdb`；批次 1 记录 `sha256:8f2e1b9465d96a8cb7b9cab286e687a52621f136b570f521df15f6f9112da7c8` —— **不一致，已按计划记录新 digest**。差异发生在 manifest 层（buildx v0.31.1 本次产出带 attestation 的 manifest list，`{{.Id}}` 取 manifest list digest）；各层 CACHED 说明层内容未变。**不宣称内容变化，也不宣称与批次 1 逐字节一致** |
| 脱敏复检 | 镜像内 `find /app` 查 `*.pem/*.key/*.pcap/*.pcapng/*.crt/*.p12/*.jks` + `grep -ri password\|passwd\|secret /app --include='*.log'` | 无敏感文件、无含口令日志 → **PASS** |
| SIP 监听运行时 | `docker run --rm -e AS_SIP_ACCEPT_ALL_INVITES=1 -e AS_SIP_UDP_PORT=5060 as-platform:0.2.0-internal-20261012` | `RESIP_RUNTIME_LISTENING address=127.0.0.1 advertised=127.0.0.1 udp_port=5060` |
| Helm 可重复渲染 | `make chart-check`（`tools/bin/helm` 3.16.4） | `chart-check: OK` |
| 环境变量逐条核对 | 实现侧 `platform/src/as_platform/`（`runtime/transport_env.py` 为主入口） | 读取 `AS_SIP_*` / `AS_TLS_*` / `AS_PEER_*` 共 **16 个**，见下表 |

> **计数自增说明**：根守卫按证据文件参数化。执行 E-6 时 `make gate` = `1174 passed` / `tests/test_evidence_discipline.py` = `135 passed`；新增本批次证据后收尾复跑为 `1176 passed` / `137 passed`。证据文件内保留执行时快照。

**实现侧读取的 16 个环境变量**：`AS_PEER_ALLOWED_ADDRESSES`、`AS_PEER_ALLOWED_CERT_FINGERPRINTS`、`AS_SIP_ACCEPT_ALL_INVITES`、`AS_SIP_ADVERTISED_ADDRESS`、`AS_SIP_BIND_ADDRESS`、`AS_SIP_DISABLE_UDP`、`AS_SIP_ENABLE_TCP`、`AS_SIP_ROUTE_HOOK`、`AS_SIP_TCP_PORT`、`AS_SIP_TLS_PORT`、`AS_SIP_UDP_PORT`、`AS_TLS_CA_PATH`、`AS_TLS_CERT_PATH`、`AS_TLS_ENABLE`、`AS_TLS_KEY_PATH`、`AS_TLS_REQUIRE_CLIENT_CERT`。

**文档覆盖度**：`platform/README.md` **16/16**；`docs/operations/runbook-l2.md` 3/16（子集引用）；`docs/delivery/install-guide.md` 1/16；根 `README.md` **0/16**（无环境变量表）。

**反向核对**：文档出现的 `AS_SIP_NEXT_HOP` / `_PORT` / `_TLS_PORT` 不在 `platform/src`，但实现于 `apps/translation/src/as_translation/outbound.py:44/:48/:50`，**不是漂移、不是错名**。

**结论**：**未发现错名 / typo / 漂移**；根 `README.md` 缺 env 表为**既有文档缺口**（非阻塞，`report.md` §0.7 已登记），本批次不补。

### 2.2 矩阵现行计数

唯一取值依据 = `docs/acceptance/m8-test-plan-matrix.md`「M8 批次4 终态化代签（2026-10-13）」节第四节。

| 桶 | 现行值 |
|---|---:|
| pass | **27** |
| defer | **4** |
| blocked | **9** |
| n-a | **9** |
| open | **0** |
| fail | **0** |
| **合计** | **49** |

口径：全部 `pass` 为「**工程证据接受**」，为 agent 代签（维护者授权），**不是维护者亲签**。

---

## 3. Gap 清单

**工程层无 gap。** P0 = 0 / P1 = 0 / P2 = 0。以下为**需维护者裁决的事项**，不是本批次的工程缺口：

| 编号 | 事项 | 性质 |
|---|---|---|
| ① | `plan.md` M8 行最终表述待确认（草案已出：`docs/acceptance/m8-plan-m8-row-draft-2026-10-12.md`） | 维护者裁决（文档表述） |
| ② | 镜像 digest 与批次 1 不一致（已记录新 digest `sha256:63ba8f4df78d…`，是否统一构建口径待定） | 维护者裁决（构建口径） |
| ③ | 根 `README.md` 环境变量表缺口 | 非阻塞；`report.md` §0.7 已登记 |
| ④ | 外部硬依赖（D-1 运营商 PKI + 外网 S-SBC、D-2 客户 K8s、ADR-0008 跨站点演练、D12/O5 生产 HA）与 4 行 `defer`（F-5 / F-8 / F-9 / F-11）仍待排期或书面接受风险 | 维护者裁决（排期 / 风险接受） |
| ⑤ | M8 退出签字仍后置 | 维护者动作（签字） |

---

## 4. 一致性检查

| 检查项 | 计划 / 上游出处 | 结论 |
|---|---|---|
| 禁改文件未动（`docs/plan.md`、`docs/acceptance/m8-test-plan-matrix.md`、`VERSION`、`CHANGELOG.md`） | 批次 6 提示词「硬纪律」 | ✅ 已执行：四者均未被本批次改动 |
| 三处追加式改动为纯新增（`+1` / `+35` / `+19`），零删除 | 批次 6 提示词 E-1 / E-5 / E-6 | ✅ 已执行：`git diff --cached --stat` 显示 README 索引 +1、`report.md` +35、`m8-exit-review-2026-10-06.md` +19，均为 insertions，无 deletions |
| 门禁与两项守卫全绿 | `AGENT.md` / `make gate` 定义 | ✅ 已执行：`make gate` 四步 exit 0（`1174 passed, 249 deselected, 11 warnings`）；`test_version_consistency.py` `9 passed`；`test_evidence_discipline.py` `137 passed` |
| 证据文件名前缀与四层机制一致 | `docs/acceptance/artifacts/m5/README.md`「文件名即结论」 | ✅ 一致：E-6 使用 `PASS-` 前缀，与实际通过结论一致 |
| 新增证据已在索引登记 | 同上 | ✅ 已执行：`docs/acceptance/artifacts/m5/README.md` +1 行 |
| 环境名不写匿名的「本机」 | `docs/environments.md` 规则 (2)；`tests/test_evidence_discipline.py` 规则 5 | ✅ 已执行：本文与 E-6 证据一律 `dev-win03ib7niepf0` |
| 不签收任何 REQ、不签 M8 | 批次 6 提示词「硬纪律」 | ✅ 已执行：全文未出现「已签收 / REQ 级验收通过 / M8 全绿 / 已发版」表述 |
| 不执行任何 git 写操作 | 同上 | ✅ 已执行：无 add / commit / tag / push / branch / 改 remote；全部改动留工作树 |
| review record 格式（五要素） | `AGENT.md` §3.3 | ✅ 已遵循：① 评审对象 ② 评审日期与评审人 ③ 评审结论 ④ 问题清单与对应修改 ⑤ 修改后的确认签字 |

---

## Adjudication（裁决记录）

> 裁决为**评审人建议**，须维护者确认后方可执行；签字为维护者动作。状态列一律「**待维护者确认**」。
> **本批次不作任何裁决、不代签。**

| 项 | 来源 | 问题摘要 | 裁决（建议） | 修改方案 | 状态 | 验证方式 |
|---|---|---|---|---|---|---|
| **①** | E-3 草案 | `docs/plan.md` §0 / §4 的 M8 行最终表述未定 | 建议维护者直接采用或修订 `docs/acceptance/m8-plan-m8-row-draft-2026-10-12.md` 的三项建议 | 由维护者或授权 agent 改 `plan.md`（本批次 agent 未改） | 待维护者确认 | 核对 `plan.md` §0 步骤单元格 / 产品决策记录 / §4 M8 状态列 |
| **②** | E-6 镜像重建 | 本次 image id `sha256:63ba8f4df78d…` 与批次 1 `sha256:8f2e1b9465d9…` 不一致；差异在 manifest 层（buildx v0.31.1 产带 attestation 的 manifest list） | 建议二选一：① 统一 buildx 构建口径以复现批次 1 的 digest 形态；② 书面接受「以 manifest list digest 为准」的新口径 | 若选①需重跑 `docker build` 并对比；若选②需在 E-6 证据与本文注明口径变更 | 待维护者确认 | 重跑 `docker build` 比对 `{{.Id}}`；或查 E-6 证据口径注记 |
| **③** | E-6 环境变量核对 | 根 `README.md` 无环境变量表（0/16 覆盖） | 建议补表，或书面接受该缺口（非阻塞，`report.md` §0.7 已登记） | 由维护者或授权 agent 补 `README.md` env 表；本批次不补 | 待维护者确认 | 核对根 `README.md` 是否出现 16 个变量的完整表 |
| **④** | 上游 D-1 / D-2 / ADR-0008 / D12-O5 与 4 行 `defer` | 外部硬依赖未排期；F-5 / F-8 / F-9 / F-11 定点 v1.1 但尚未立项 | 建议给出排期或书面接受风险；F-5 / F-8 / F-9 / F-11 走 v1.1 立项流程 | 排期登记或总审书面接受；立项走 requirement → ADR → design → review | 待维护者确认 | 查 v1.1 登记与总审风险接受记录 |
| **⑤** | E-4 / E-5 签字节 | M8 退出签字仍后置 | 建议由维护者在 M8 退出评审中单独签字；本批次仅完成内部版收尾 | 维护者签字（不可代签） | 待维护者确认 | 查 `m8-exit-review-2026-10-06.md` §3.2 M8 签字栏 |
| **（补充）commit 拆分** | 工作树现状 | 本批次 8 个文件与批次 1 遗留 `.dockerignore`、维护者自身改动（`.gitignore`、`docs/intro.md`）、IDE 未跟踪目录 `.codebuddy/teams/...` 混杂 | 建议按来源切分提交，勿混入本批次 | 由维护者执行 `git add` 范围选择并提交 | 维护者动作 | `git status --short` 逐项核对 |
| **（补充）tag** | `AGENT.md` §10.4 | 内部版本不打 tag | 保持不打 tag；tag 仅维护者执行 | 无 | 维护者动作 | `git tag -l` |

> 说明：commit 拆分与 tag 属于维护者动作而非评审裁决，列入本节仅为提醒，不构成裁决建议。
>
> **2026-10-13 维护者裁决（②）**：镜像 digest 口径**选② —— 书面接受新口径**，以 buildx v0.31.1 产出的 manifest list digest 为准（`sha256:63ba8f4df78d…`），**不重跑构建**去复现批次 1 的 `sha256:8f2e1b9465d…` 形态。E-6 证据内两个 digest 与「各层 CACHED、不宣称逐字节一致」的说明均为终态，不再改动。

---

## 签字

- **签字状态**：**未签 —— 维护者待签**。
- **评审人**：AI agent（仅评审与列出 gap，不签字）。
- **授权基础**：维护者已授权**执行** M8 六个批次（依据 `docs/handoff/2026-10-12-m8-scope-revision-internal-release-plan.md` §6 第 6 项；执行授权 ≠ 签字授权）。本批次不代签任何 REQ 或里程碑，签字仍为维护者动作。
- **评审结论**：**有条件通过** —— 批次 6「文档与报告」六项（E-1～E-6）**全部落地**，**内部版收尾完成（有条件）**；条件即上表 ①～⑤ 全部经维护者确认。
- **M8 退出签字栏**：**未签 —— 维护者待签**（内部版本，不签收）。
- **REQ**：**本批次不签收任何 REQ**。
- 执行环境 `dev-win03ib7niepf0`；本批次未执行任何 git 写操作；未改动 `docs/plan.md`、`docs/acceptance/m8-test-plan-matrix.md`、`VERSION`、`CHANGELOG.md`。

---

（本记录为批次 6「文档与报告」评审。本文不签收任何 REQ、不签 M8 里程碑签字、不宣称 M8 全绿、不宣称已发版；「内部版收尾完成」不等于「M8 退出签字」。）
