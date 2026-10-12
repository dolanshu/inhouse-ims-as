# M8 内部版本收尾 — Handoff（2026-10-12）

## 0. 本 handoff 用途

本 session 完成了批次 1「发布与打包」。新 session 从批次 2「SIP 对拍」开始接续。本文档是新 session 的唯一执行入口——读完即可继续，不需回看本 session 对话。

## 1. 当前状态

- **本版定位**：内部版本（function 完整 + 模拟器证据 + 可重复构建的发布工件），**不是 M8 退出签字**。
- **已完成**：批次 1「发布与打包」六项全部完成并通过验证。
- **待执行**：批次 2 → 3 → 5 → 4 → 6（按依赖顺序）。
- **分支**：master（未提交任何改动）。

## 2. 批次 1 完成项（已落盘，未提交）

### 2.1 改动文件

| 文件 | 改动 |
|---|---|
| deploy/docker/Dockerfile | 两阶段→三阶段（resip-builder/py-builder/runtime）：从 vendor 源码构建 reSIProcate 共享库 + 三个 native 扩展（_resip_runtime/_resip_two_leg/_resip_recovery）；runtime ENV: AS_ENABLE_SIP_RUNTIME=1, AS_RESIP_*_BUILD=/app/native, LD_LIBRARY_PATH=/app/lib；EXPOSE 修正为 5060/udp 5060/tcp 5061/tcp |
| platform/src/as_platform/__main__.py | main() 接入 SipStackService.from_env()+start()；drain 时 stop()；fail-closed: 扩展缺失 → except → exit 2；未设 env 时向后兼容 |
| platform/README.md | 环境变量表从 10 行补全到 30+ 行（AS_SIP_*/AS_TLS_*/AS_PEER_*/AS_RECOVERY_*），标注 Helm 接入状态与 values 对应键 |
| CHANGELOG.md | [0.2.0] 节追加 Internal build (2026-10-12) 子节，标注「内部版本，不是发行版」 |
| .dockerignore | 豁免 vendor 源码头文件 |
| docs/acceptance/artifacts/m5/2026-10-12/PASS-docker-build-digest-2026-10-12.txt | 镜像构建证据：image ID sha256:8f2e1b9465d96a8cb7b9cab286e687a52621f136b570f521df15f6f9112da7c8，native listener 确认监听 UDP 5060 |
| docs/acceptance/artifacts/m5/2026-10-12/PASS-desensitization-check-2026-10-12.txt | 脱敏复检：镜像内无密钥/证书/抓包/含口令日志 |
| docs/reviews/m8-batch1-release-packaging-review-2026-10-12.md | 批次 1 review record（无 gap，待维护者评审，未签） |

### 2.2 验证结果

- make gate: 1104 passed / 2 skipped / 214 deselected (exit 0)
- tests/test_evidence_discipline.py + tests/test_version_consistency.py: 94 passed
- 镜像构建 exit 0，RESIP_RUNTIME_LISTENING 确认 UDP 5060 监听
- 脱敏复检：无敏感文件

### 2.3 遗留未提交改动（非本批次引入，是之前会话遗留）

工作树中以下文件也有未提交改动，**不是批次 1 引入的**，新 session 需注意：
- docs/acceptance/m8-test-plan-matrix.md
- docs/handoff/2026-10-12-m8-scope-revision-internal-release-plan.md
- docs/plan.md
- docs/reviews/m8-scope-revision-internal-release-plan-review-2026-10-12.md（新建）

## 3. 待执行批次（按依赖顺序）

### 批次 2「SIP 对拍」（下一个）

**执行顺序（出自 ../handoff/2026-10-09-sip-native-testing-plan.md §4-D，不得重排）**：

1. **S8 基线补采**：M2 probe 补采 Route / Record-Route 基线（基线缺这两个头，2 条既有 skip 的根因）。补采前不排 S8 实现，REQ-F-5 按 N4 停止线不签 pass。补采完成后建议插在 P3 之后。
2. **P1 S5**：两腿归一化序列对拍。F-2 已于 2026-10-12 N3 代签 pass，此处为 coverage 扩展（不改行状态）。复用 testbed/e2e/ 框架。
3. **P2 S7a**：SDP 透传 corpus 扩充（兼 F-4 更广 corpus）。补带 media 描述 / 多 m-line 的 SDP 变体。推进 F-4。
4. **P3 S6**：多规则优先级 + 无匹配组合。F-3 已于 N3 代签 pass，此处为 coverage 扩展。与 S2（404 已绿）共用仿真链。
5. **P4 S10**：非 2xx（486/480/408）透传。依赖先扩 testbed 对端 UAS（当前只返 200）。推进 F-10。
6. **P5 S9**：in-dialog 路由。依赖 M7.3 context restoration 工程切片（已在位）。推进 F-9。
7. **P6 S11**：CANCEL 与最终响应竞态。竞态两分支确定性证明成本最高、flaky 风险最大；允许以 gap 登记收尾。推进 F-11。

**其余关联**：
- F-8（CANCEL 三分支）随 S4 cancel harness 与 S11 的对拍推进。
- F-16（翻译决策链）的轨迹联动部分依赖 F-13 —— F-13 已裁定 delay v1.1，故 F-16 只签非轨迹部分并写明理由。

### 批次 3「kind/sim 证据」

可与批次 2 部分并行；F-15 真 AS 依赖批次 1 的镜像（已就绪）。取证行：NF-2、NF-4、NF-9、NF-5、F-15/5.4-F-15真AS、NF-10、2.5 备份恢复（kind bundled PG 备份/恢复/重建演练 + runbook 走查 + 实测耗时）。

### 批次 5「性能与容量（kind）」

可与批次 3 并行；向批次 4 供 NF-15 证据。
- NF-15 多副本测量：kind 上多副本，记录 per-pod CPU/内存利用率。
- HPA 阈值填写：kind 实测后填 deploy/helm/values-onprem.example.yaml（注明「kind 实测、非对外承诺、上线前须目标环境复测」）；默认 values.yaml 保持 null。
- O1：内部工程目标 loopback CPS 1280 无失败（仅限内部，不写入对外材料）。
- 容量类告警仍不新增；ne-datasheet/4.1 正式报告维持阻塞。

### 批次 4「签收与评审」

依赖批次 2/3/5 产出证据。
- S-1（白名单）：评审现有证据 + 缺项补测。
- S-4（RBAC + 审计不可篡改）：评审 + 缺项补测；durable audit 已有工程切片。
- 矩阵 17 open 行逐行终态化：每行给出 pass/n-a/defer 之一，必带理由；pass 须有本版新证据。

### 批次 6「文档与报告」（最后）

- E-1: report.md 升为 M8 RC 报告，§0.5 计数同步为 pass 16 / open 17 / blocked 7 / n-a 9 / fail 0。
- E-2: VERSION 维持 0.2.0，CHANGELOG 已追加 internal build。
- E-3: plan.md §0/§4 M8 行回写。
- E-4: 内部版退出评审文档（明确不是 M8 退出签字）。
- E-5: 里程碑签字表（M1/M2/M6/M7 工程完成已代签；M8 不签）。
- E-6: 打包复检。

## 4. 已裁定六项（不要重新问）

1. F-13/NF-7 呼叫轨迹 = 重大漏项，delay 到 v1.1 作为 feature；本版不实现；F-16 只签非轨迹部分。
2. 内部版本不 bump：VERSION 维持 0.2.0，CHANGELOG 在 0.2.0 节内追加 internal build 条目，镜像 tag 用 as-platform:0.2.0-internal-<date>，chart 不再同步。
3. 2.5 备份恢复：本版做 kind 完整工程演练（bundled PG 备份/恢复/重建 + runbook 走查 + 实测耗时），明写不等于客户真实集群版。
4. NF-15 HPA 阈值：kind 多副本 + per-pod CPU/内存实测数据产出后，填 values-onprem.example.yaml（注明「kind 实测、非对外承诺、上线前须目标环境复测」）；默认 values.yaml 保持 null；ne-datasheet/容量告警/4.1 正式报告仍阻塞。
5. 批次 2/3 一次性全量授权。
6. 批次 1/4/6（及隐含批次 5）一并全量授权。→ 六个批次全部授权。

## 5. 硬纪律（违反即返工）

- 主 agent 只做规划/review/汇报，不直接写文件。所有写文件动作派 writing subagent（Task 工具 subagent_type=general_purpose_task）；一个工作树同时只允许一个 writing member。
- 不执行任何 git 写操作（不 add/commit/tag/push/改 remote/建分支）；commit 拆分由维护者决定。
- 不签收任何 REQ、不签收任何里程碑、不改矩阵任何行的 status、不改 report.md 计数。写文档一律「原文保留不改，追加更正」。
- 证据四层机制：文件名即结论（docs/acceptance/artifacts/** 强制 PASS- / FAILCLOSED- 前缀）；环境必须有名字（写 environments.md 里已登记的环境名 dev-win03ib7niepf0，禁匿名「本机」）；状态一律三元组 (结论, 证据文件, 日期)；守卫测试 tests/test_evidence_discipline.py。
- 不发明新编号；引用既有编号。
- 不发布任何对外容量数字；内部工程目标（loopback CPS 1280）仅限内部。

## 6. 环境信息

- 已登记环境：dev-win03ib7niepf0（host WIN-03IB7NIEPF0）
- 工具在 tools/bin（helm 3.16.4 / kubectl 1.31.4 / kind 0.24.0 / promtool 2.55.1，版本锁定于 tools/VERSIONS）
- 已有 kind 集群：as-m5（context kind-as-m5）、as-m71
- docker 可用
- 构建/测试命令见 Makefile（make gate / make gate-native / make chart-check / make test-integration-compose / make m2-platform-resip-build）

## 7. 新 session 开场仪式

新 session 第一个动作：

1. 读 AGENT.md、docs/README.md、docs/plan.md 当前里程碑、docs/acceptance/m8-test-plan-matrix.md
2. 读本 handoff 文档
3. git status 核对工作树现状
4. 从批次 2 第 1 项（S8 基线补采）开始

## 8. 关键指针

- 本批次唯一执行依据：docs/handoff/2026-10-12-m8-scope-revision-internal-release-plan.md
- SIP 对拍计划：docs/handoff/2026-10-09-sip-native-testing-plan.md §4-D
- 签收矩阵：docs/acceptance/m8-test-plan-matrix.md（现行 pass 16 / open 17 / blocked 7 / n-a 9 / fail 0；F-13/5.4-F-13/NF-7 已转 n-a）
- 评审记录：docs/reviews/m8-scope-revision-internal-release-plan-review-2026-10-12.md（G-1/G-2/G-3 已闭环）
- 环境登记：docs/environments.md
- 批次 1 review：docs/reviews/m8-batch1-release-packaging-review-2026-10-12.md

---

落盘日期：2026-10-12。本文档不签收任何 REQ、不签收里程碑、不改矩阵状态。
