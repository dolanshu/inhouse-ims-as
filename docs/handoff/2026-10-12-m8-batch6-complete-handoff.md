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

# M8 批次 6「文档与报告」完成交接（2026-10-12）

## 0. 本文性质与边界

本文为 M8 批次 6 完成交接。批次 6 是 M8 六批拆分中的**最后一批**，依赖批次 1–5 的产出；配套评审记录：`docs/reviews/m8-batch6-docs-report-review-2026-10-12.md`。

- **本版定位**：内部版本 —— function 完整 + 模拟器证据 + 可重复构建工件。**不是 M8 退出签字**，不构成发版。
- **本批次不签收任何 REQ**、不改矩阵状态（矩阵终态由批次 4 代签节落地）、**不改 `docs/plan.md`**、不改 `VERSION` / `CHANGELOG.md`。
- **不宣称 M8 全绿、不宣称已发版**；「内部版收尾完成」≠「M8 退出签字」。
- **执行环境**：`dev-win03ib7niepf0`（已登记于 `docs/environments.md`）。
- **未执行任何 git 写操作**，全部改动留工作树，由维护者切分提交。

## 1. 完成清单（6/6）与三元组

| 项 | 落点文件 | 三元组（结论, 证据, 日期） |
|---|---|---|
| **E-1** 计数同步 | `docs/acceptance/report.md` +35 行（内部版抬头 6 行 + §0.10「计数同步与内部版收尾声明」29 行） | (已验证, `docs/acceptance/report.md` §0.10, 2026-10-13) |
| **E-2** 版本与变更记录 | `VERSION` = `0.2.0`；`CHANGELOG.md` `[0.2.0]` 节内已有 `### Internal build (2026-10-12)` 子节 | (已确认、**未改动**, `VERSION` / `CHANGELOG.md`, 2026-10-12) |
| **E-3** `plan.md` §0 / §4 M8 行 | `docs/acceptance/m8-plan-m8-row-draft-2026-10-12.md`（36 行） | (**只出草案**、`docs/plan.md` 未改, `docs/acceptance/m8-plan-m8-row-draft-2026-10-12.md`, 2026-10-12) |
| **E-4** 内部版收尾评审 | `docs/reviews/m8-internal-release-exit-review-2026-10-12.md`（113 行） | (已验证, `docs/reviews/m8-internal-release-exit-review-2026-10-12.md`, 2026-10-12) |
| **E-5** 里程碑退出评审追加 | `docs/reviews/m8-exit-review-2026-10-06.md` §3.2（+19 行） | (已验证, `docs/reviews/m8-exit-review-2026-10-06.md` §3.2, 2026-10-12) |
| **E-6** 打包复检 | `docs/acceptance/artifacts/m5/2026-10-12/PASS-e6-packaging-recheck-2026-10-12.txt`（74 行）+ 索引 +1 行 | (已验证, `docs/acceptance/artifacts/m5/2026-10-12/PASS-e6-packaging-recheck-2026-10-12.txt`, 2026-10-12) |

- E-2 说明：`VERSION` 已裁定不 bump，维持 `0.2.0`；`CHANGELOG.md` 的 internal build 子节已存在（含「这是内部版本，不是发行版」、镜像 tag 格式、chart 不同步、本版定位四项），**不重复追加**。
- E-3 说明：草案含三项建议（§0 当前进行中步骤单元格追加句、§0 产品决策记录新增一行、§4 M8 行状态列建议值）与边界；**`docs/plan.md` 未被改动**，最终表述由维护者确认。

## 2. 关键结果摘要

- **report.md 计数同步**：现行值 **pass 27 / defer 4 / blocked 9 / n-a 9 / open 0 / fail 0，合计 49 行**（取值依据 = `docs/acceptance/m8-test-plan-matrix.md`「M8 批次4 终态化代签（2026-10-13）」节第四节）。§0.5 原文的 2026-10-06 历史值（pass 9 / fail 0 / blocked 12 / n-a 4 / open 24）**保留不改**，以「原文保留、追加更正」方式处理。全部 `pass` 口径为「**工程证据接受**」，为 agent 代签（维护者授权），**不是维护者亲签**。
- **M8 行不签收**：`docs/reviews/m8-exit-review-2026-10-06.md` §3.2 中 **M8 状态 =「内部版本，不签收」，签字 =「未签 —— 维护者待签」**；M1/M2/M6/M7 维持「工程完成（agent 代签，维护者 2026-10-12 授权）」。
- **E-6 八项实测**：版本一致性、证据纪律守卫、`make gate`、镜像重建、脱敏复检、SIP 监听运行时、Helm 可重复渲染、环境变量逐条核对 —— **六项通过 + 一项偏差**（镜像 digest 与批次 1 不一致，已按计划记录新 digest `sha256:63ba8f4df78d5853e70451cc0e2a12e691f2c38facc800e2135d71c7018ecfdb`；差异在 manifest 层：buildx v0.31.1 本次产出带 attestation 的 manifest list，`{{.Id}}` 取 manifest list digest；各层 CACHED 说明层内容未变。**不宣称内容变化，也不宣称与批次 1 逐字节一致**）。
- **环境变量 16 个逐条核对无漂移**：实现侧 `platform/src/as_platform/`（`runtime/transport_env.py` 为主入口）读取 `AS_SIP_*` / `AS_TLS_*` / `AS_PEER_*` 共 16 个；覆盖度 `platform/README.md` 16/16、`docs/operations/runbook-l2.md` 3/16、`docs/delivery/install-guide.md` 1/16、根 `README.md` 0/16。反向核对中文档出现的 `AS_SIP_NEXT_HOP` / `_PORT` / `_TLS_PORT` 不在 `platform/src`，但实现于 `apps/translation/src/as_translation/outbound.py:44/:48/:50`，**不是漂移、不是错名**。根 `README.md` 缺 env 表为既有文档缺口（非阻塞，`report.md` §0.7 已登记），本批次不补。

## 3. 改动文件清单（本批次 8 个文件，对应 E-1~E-6 六项；均未提交）

| 文件 | 改动 |
|---|---|
| `docs/acceptance/artifacts/m5/2026-10-12/PASS-e6-packaging-recheck-2026-10-12.txt` | **新增** 74 行证据（E-6） |
| `docs/reviews/m8-internal-release-exit-review-2026-10-12.md` | **新增** 113 行（E-4） |
| `docs/acceptance/m8-plan-m8-row-draft-2026-10-12.md` | **新增** 36 行草案（E-3；`docs/plan.md` **未改**） |
| `docs/reviews/m8-batch6-docs-report-review-2026-10-12.md` | **新增** 评审记录 |
| `docs/handoff/2026-10-12-m8-batch6-complete-handoff.md` | **新增** 本交接 |
| `docs/acceptance/report.md` | **追加 +35 行**（抬头 6 + §0.10 二十九），纯追加零删除（E-1） |
| `docs/reviews/m8-exit-review-2026-10-06.md` | **追加 +19 行**（§3.2）（E-5） |
| `docs/acceptance/artifacts/m5/README.md` | **追加 +1 行**索引（E-6 证据登记） |

**非本批次、勿混入本批次提交**（本批次 agent 未触碰以下四项）：

- `.dockerignore` —— 批次 1 遗留改动。
- `.gitignore` 与 `docs/intro.md` —— 维护者自身改动。
- `.codebuddy/teams/...` —— IDE 未跟踪目录。

**观察项**：上述本批次文件在核对时处于**已暂存（staged）**状态（`git status --short` 显示为 `A` / `M` 且位于第一列）。本批次 agent **未执行任何 git 写操作**，该暂存态**不是本批次产生**（同工作树内另有维护者的并发改动）。提交拆分由维护者决定。

## 4. 验证结果

执行环境 `dev-win03ib7niepf0`。

| 项 | 命令 | 结果 |
|---|---|---|
| 门禁 | `make gate` | `1174 passed, 249 deselected, 11 warnings`，四步 exit 0 |
| 版本一致性守卫 | `uv run pytest tests/test_version_consistency.py -q` | `9 passed`，exit 0 |
| 证据纪律守卫 | `uv run pytest tests/test_evidence_discipline.py -q` | 新增证据后 `137 passed`（执行 E-6 时为 `135 passed`；+2 来自新增证据使根守卫参数化用例增加，属预期） |
| Helm 可重复渲染 | `make chart-check`（`tools/bin/helm` 3.16.4） | `chart-check: OK` |
| 镜像重建 | `docker build -t as-platform:0.2.0-internal-20261012 -f deploy/docker/Dockerfile .` | exit 0（全部步骤 CACHED，2.5s） |
| 脱敏复检 | 镜像内 `find /app` + `grep -ri password\|passwd\|secret` | 无敏感文件、无含口令日志 → PASS |
| SIP 监听运行时 | `docker run --rm -e AS_SIP_ACCEPT_ALL_INVITES=1 -e AS_SIP_UDP_PORT=5060 …` | `RESIP_RUNTIME_LISTENING address=127.0.0.1 advertised=127.0.0.1 udp_port=5060` |

> **计数自增说明**：根守卫按证据文件参数化，新增证据会使计数自增。执行 E-6 时 `make gate` = `1174 passed, 249 deselected`、`tests/test_evidence_discipline.py` = `135 passed`；本批次新增 `PASS-e6-packaging-recheck-2026-10-12.txt` 后收尾复跑为 `make gate` = `1176 passed, 249 deselected`（exit 0）、`tests/test_evidence_discipline.py` = `137 passed`、`tests/test_version_consistency.py` = `9 passed`。证据文件内**保留执行时快照**，不回改数字。

## 5. 待维护者事项

1. **`docs/plan.md` §0 / §4 M8 行最终表述确认** —— 草案见 `docs/acceptance/m8-plan-m8-row-draft-2026-10-12.md`（本批次未改 `plan.md`）。
2. **外部硬依赖排期或书面接受风险** —— D-1（运营商 PKI + 外网 S-SBC）、D-2（客户 K8s）、ADR-0008 跨站点演练、D12/O5 生产 HA。
3. **4 行 `defer`（F-5 / F-8 / F-9 / F-11）与 F-13 / NF-7 呼叫轨迹的 v1.1 立项**。
4. **镜像 digest 口径** —— 是否统一 buildx 构建方式以复现批次 1 的 digest 形态（`sha256:8f2e1b9465d96a8cb7b9cab286e687a52621f136b570f521df15f6f9112da7c8`），或书面接受「以 manifest list digest 为准」的新口径。
   （**2026-10-13 已裁决：选②**，书面接受 manifest list digest 新口径，不重跑构建）
5. **根 `README.md` 环境变量表缺口是否补** —— 当前 0/16 覆盖，非阻塞，`report.md` §0.7 已登记。
6. **M8 退出签字仍后置** —— 本批次仅完成内部版收尾，未签 M8。
   （**2026-10-13 已按路径 C 处理**：M8 退出签字由维护者签收，含书面接受外部硬依赖风险；签字栏待其亲签，见 `docs/reviews/m8-exit-review-2026-10-06.md` §3.3）
7. **commit 拆分与 tag** —— 仅维护者执行（`AGENT.md` §10.4）；内部版本不打 tag。

> **去向指针（2026-10-13 追加；上方七项待维护者事项原文一律保留不改）**：本节尚未闭合的几项去向为 ——
> **第 1 项**：`docs/plan.md` §0 / §4 M8 行最终表述草案是否合并 →
> [`../next-release-v1.1-plan.md`](../next-release-v1.1-plan.md) **§5-3**（草案载体 = `docs/acceptance/m8-plan-m8-row-draft-2026-10-12.md`，待维护者确认表述后合并）；
> **第 2 项**：四项外部硬依赖（D-1 / D-2 / ADR-0008 演练 / D12-O5）的排期 —— 已按路径 C 书面接受风险、
> 保持 `blocked` 转下一 release → 同文档 **§2**（重启 = 维护者另行裁决 + 外部资源到位，后置 ≠ 取消）；
> **第 3 项**：4 行 `defer`（F-5 / F-8 / F-9 / F-11）与 F-13 / NF-7 呼叫轨迹的 v1.1 立项 → 同文档 **§3 第 1–5 行**；
> **第 6 项**：M8 退出签字栏现为 **agent 代签（维护者 2026-10-13 授权）**、**不是维护者亲签** → 同文档 **§7-1**；
> **第 7 项**：commit 拆分与 tag（仅维护者执行） → 同文档 **§5-6**。
> 后续状态盘点、汇报、handoff、新 session 开场涉及本节遗留项一律**只引该指针**，不逐项展开、不再列入「待维护者动作」。

## 6. 纪律执行声明

- 主 agent 未直接写任何仓库文件；本工作树同时只有一个 writing subagent，且两个 writer **串行**（前一个关闭后才启动这一个）。
- **未执行任何 git 写操作**（无 add / commit / tag / push / branch / 改 remote / stash）；全部改动留工作树。
- 不改代码、不改矩阵状态、不改 `docs/plan.md`、不改 `VERSION` / `CHANGELOG.md`。
- **不签收任何 REQ、不签 M8 里程碑签字**；不宣称 M8 全绿、不宣称已发版。
- 证据无凭据 / token / DSN / cookie；脱敏复检已确认镜像内无敏感文件与含口令日志。
- 三元组与环境名齐备：证据一律 `(结论, 证据文件, 日期)`，环境名一律 `dev-win03ib7niepf0`，未出现匿名的「本机」。
- 沿用既有编号体系（E-1~E-6、N2/N3/N4、D4-01…、B5-04、O1/O4/O5、D1~D12、G1–G8），未发明新编号。
