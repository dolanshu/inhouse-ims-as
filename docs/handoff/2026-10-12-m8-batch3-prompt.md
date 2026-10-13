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

# M8 批次 3「kind/sim 证据」— 新 Session 提示词

## 开场仪式
1. 读 AGENT.md、docs/README.md、docs/plan.md（M8 节）、docs/acceptance/m8-test-plan-matrix.md
2. `git status` 核对工作树
3. `export PATH="$PWD/tools/bin:$PATH"`

## 当前状态
- 已完成：批次 1（发布与打包）、批次 2（SIP 对拍 S8/S5/S7a/S6/S10/S9/S11）
- 分支 master，所有改动未提交（不许提交）
- kind 集群：as-m5（context kind-as-m5）
- 工具：tools/bin（kind 0.24.0 / kubectl 1.31.4 / helm 3.16.4）
- 镜像：as-platform 已构建（带 native SIP 监听）
- 环境名：dev-win03ib7niepf0

## 取证范围（按顺序）
1. **F-15 真 AS 全栈**（最先，其他依赖它）
   - helm 部署到 kind（translation + antiFraud + config-service + bundled PG + Redis）
   - 验证：分发 → 健康 → 自动回滚 → 手动回滚
   - 参考 deploy/helm/values-onprem.example.yaml
2. **NF-2 双 Deployment 隔离**：kill translation Pod，antiFraud 不受影响
3. **NF-9 命名空间隔离**：ns-A 杀 PG/删 AS，ns-B 不受影响
4. **NF-10 灰度分发/回滚**：随 F-15 一并取证
5. **NF-4 滚动升级零丢失**：持续 SIP 话务下 helm rollout restart，验证不中断
6. **NF-5 换仿真器一致性**：M7.1 仿真 S-SBC（UDP/TCP/TLS）行为一致
7. **2.5 备份恢复演练**：kind bundled PG pg_dump → 删数据 → pg_restore → 校验审计链；记录实测耗时（RTO 量级，非承诺）；参考 docs/operations/backup-restore.md §2

## 硬纪律
- 主 agent 不写文件，派 writing subagent（general_purpose_task），一个工作树同时只一个
- 不执行任何 git 写操作（add/commit/tag/push/branch）
- 不签任何 REQ、不改矩阵状态、不改 report.md 计数
- 证据四层：文件名 PASS-/FAILCLOSED- 前缀 → docs/acceptance/artifacts/m5/2026-10-12/；环境名 dev-win03ib7niepf0；三元组 (结论, 证据文件, 日期)；跑 tests/test_evidence_discipline.py
- 不发明新编号，不发布对外容量数字

## 关键文件
- 执行依据：docs/handoff/2026-10-12-m8-scope-revision-internal-release-plan.md §2.3
- 矩阵：docs/acceptance/m8-test-plan-matrix.md
- Helm：deploy/helm/values-onprem.example.yaml
- 备份 runbook：docs/operations/backup-restore.md §2
- 状态存储：docs/acceptance/m5-state-stores-runbook.md
- SIP 仿真器：testbed/simulators/

## 收尾
- 每项落 PASS-/FAILCLOSED- 证据文件
- 全部完成后：`make gate` 全绿 + `git status` 核对
- 写 review record：docs/reviews/m8-batch3-kind-sim-evidence-review-2026-10-12.md
- 写 handoff：docs/handoff/2026-10-12-m8-batch3-complete-handoff.md

## 注意
- kind 集群只有 as-m5，部署前先 `kubectl get all -A` 看清现状
- 镜像需 `kind load docker-image as-platform:<tag> --name as-m5`
- 无法取证的行登记 FAILCLOSED- artifact，不强行通过
