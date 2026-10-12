# M8 批次 6「文档与报告」— 新 Session 提示词

## 开场仪式
1. 读 AGENT.md、docs/README.md、docs/plan.md（M8 节）、docs/acceptance/m8-test-plan-matrix.md
2. `git status` 核对工作树
3. 确认批次 1~5 的证据与评审文档已落盘

## 当前状态
- 已完成：批次 1（发布与打包）、批次 2（SIP 对拍）、批次 3（kind/sim 证据）、批次 4（签收与评审）、批次 5（性能与容量）
- 分支 master，所有改动未提交（不许提交）
- 本批次是最后一批，依赖前序全部产出
- 环境名：dev-win03ib7niepf0

## 已裁定事项（不要重新问、不要改）
- **VERSION 不 bump**：维持 0.2.0
- **CHANGELOG**：在 0.2.0 节内追加 internal build 条目（批次 1 已做）
- **镜像 tag**：as-platform:0.2.0-internal-<date>，chart 不同步
- **M8 不签**：里程碑签字表中 M8 行留空，M1/M2/M6/M7 工程完成已代签

## 工作范围（E-1 ~ E-6）
### E-1：report.md 升为 M8 RC 报告
- docs/acceptance/report.md §0.5 计数同步为矩阵现行值
- 计数取值以批次 4 终态化草案为准（pass / open / blocked / n-a / fail）
- 报告抬头明确「内部版本，不是 M8 退出签字」

### E-2：VERSION / CHANGELOG
- VERSION 维持 0.2.0（已裁定，不改）
- CHANGELOG 确认 0.2.0 节内有 internal build (2026-10-12) 条目
- 如已就位则只做确认，不重复追加

### E-3：plan.md §0 / §4 M8 行回写
- 按本版实际收尾状态回写 M8 行
- M8 行最终表述由维护者确认——agent 先出草案，不直接改 plan.md

### E-4：内部版退出评审文档
- 新建 docs/reviews/m8-internal-release-exit-review-2026-10-12.md
- 内容：本版完成项、证据清单、已知 gap（FAILCLOSED 项）、限制说明
- **明确不是 M8 退出签字**

### E-5：里程碑签字表
- M1 / M2 / M6 / M7「工程完成」已由维护者授权代签（保持）
- **M8 不签**——签字表 M8 行标注「内部版本，不签收」

### E-6：打包复检
- 跑 tests/test_version_consistency.py（全绿）
- 镜像与 Helm 可重复构建（重新构建一次，digest 与批次 1 一致或记录新 digest）
- 脱敏复检：镜像内无密钥/证书/抓包/含口令日志
- README 与 runbook 与 AS_SIP_*/AS_TLS_* 实现一致（逐条核对环境变量）
- 证据：PASS-e6-packaging-recheck-2026-10-12.txt

## 硬纪律
- 主 agent 不写文件，派 writing subagent（general_purpose_task），一个工作树同时只一个
- 不执行任何 git 写操作
- 不签任何 REQ、不签 M8 里程碑
- 证据四层：PASS-/FAILCLOSED- 前缀 → docs/acceptance/artifacts/m5/2026-10-12/；环境名 dev-win03ib7niepf0；三元组
- 写文档一律「原文保留不改，追加更正」
- plan.md M8 行回写先出草案，等维护者确认

## 关键文件
- 执行依据：docs/handoff/2026-10-12-m8-scope-revision-internal-release-plan.md §2.6
- 报告：docs/acceptance/report.md
- 版本：VERSION、CHANGELOG.md
- 计划：docs/plan.md
- 矩阵：docs/acceptance/m8-test-plan-matrix.md
- 批次 4 终态草案：docs/acceptance/m8-matrix-finalization-draft-2026-10-12.md
- 版本一致性测试：tests/test_version_consistency.py
- Dockerfile：deploy/docker/Dockerfile
- Helm：deploy/helm/

## 收尾
- E-1~E-6 全部完成
- `make gate` 全绿 + `tests/test_version_consistency.py` + `tests/test_evidence_discipline.py` 全绿
- `git status` 核对全部改动
- 写 review record：docs/reviews/m8-batch6-docs-report-review-2026-10-12.md
- 写最终 handoff：docs/handoff/2026-10-12-m8-batch6-complete-handoff.md
- handoff 中明确：所有改动未提交，由维护者决定 commit 拆分

## 注意
- 本批次不改代码，只更新文档与报告
- 如发现前序批次证据缺失，登记 FAILCLOSED- 并在 handoff 中标注，不自行补做
- 内部版退出评审不等于 M8 退出签字，措辞必须严格区分
