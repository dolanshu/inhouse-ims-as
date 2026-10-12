# M8 批次 5「性能与容量（kind）」— 新 Session 提示词

## 开场仪式
1. 读 AGENT.md、docs/README.md、docs/plan.md（M8 节）、docs/acceptance/m8-test-plan-matrix.md
2. `git status` 核对工作树
3. `export PATH="$PWD/tools/bin:$PATH"`

## 当前状态
- 已完成：批次 1（发布与打包）、批次 2（SIP 对拍）、批次 3（kind/sim 证据，若已完成）
- 分支 master，所有改动未提交（不许提交）
- kind 集群：as-m5（context kind-as-m5）
- 工具：tools/bin（kind 0.24.0 / kubectl 1.31.4 / helm 3.16.4）
- 负载 harness：testbed/load/（`uv run python -m as_load --cps --duration --hold --workers --timeout`）
- loopback 测量脚本：testbed/load/scripts/m6-o1-formal-report.sh
- 环境名：dev-win03ib7niepf0

## 取证范围（按顺序）
1. **NF-15 多副本测量**
   - kind 上部署多副本 AS（helm 设 replicaCount > 1）
   - 用 testbed/load harness 发 SIP 负载，记录 per-pod CPU/内存利用率
   - 测量多个 CPS 档位（如 20/40/80/160/320/640/1280）
   - 证据：PASS-nf15-multi-replica-measurement-2026-10-12.txt（含 per-pod CPU/内存、CPS 档位、建立时延 p50/p95/p99）

2. **O1 内部工程目标复测**
   - loopback CPS 1280 无失败（仅限内部，不写入对外材料）
   - 复用 m6-o1-formal-report.sh 或直接调 as_load
   - 证据：PASS-o1-loopback-cps-1280-2026-10-12.txt（internal only）

3. **HPA 阈值填写**
   - 基于 kind 实测数据，填 deploy/helm/values-onprem.example.yaml 的 autoscaling 段：
     - minReplicas / maxReplicas
     - targetCPUUtilizationPercentage / targetMemoryUtilizationPercentage
   - **默认 values.yaml 保持 null（不动）**
   - 示例内必须注明：「kind 实测、非对外承诺、上线前须目标环境复测」
   - 证据：PASS-hpa-threshold-filled-2026-10-12.txt（含 values-onprem diff + 实测依据）

4. **performance 层门禁终态**
   - 二选一：(a) 实现为 `make gate` 阻塞层，或 (b) M8 总审书面接受风险
   - **不自作实现、不自行接受风险** —— 需维护者裁决
   - 若无法在本批次决定，登记 FAILCLOSED- 说明待维护者裁决

## 硬纪律
- 主 agent 不写文件，派 writing subagent（general_purpose_task），一个工作树同时只一个
- 不执行任何 git 写操作（add/commit/tag/push/branch）
- 不签任何 REQ、不改矩阵状态、不改 report.md 计数
- **不发布任何对外容量数字**（AGENT.md §2）；内部工程目标值不得写入对外材料
- 证据四层：文件名 PASS-/FAILCLOSED- 前缀 → docs/acceptance/artifacts/m5/2026-10-12/；环境名 dev-win03ib7niepf0；三元组 (结论, 证据文件, 日期)；跑 tests/test_evidence_discipline.py
- 容量类告警仍不新增；ne-datasheet 容量取值、4.1 正式报告维持阻塞

## 关键文件
- 执行依据：docs/handoff/2026-10-12-m8-scope-revision-internal-release-plan.md §2.5
- 矩阵：docs/acceptance/m8-test-plan-matrix.md（NF-15 行）
- 负载 harness：testbed/load/ + testbed/load/scripts/m6-o1-formal-report.sh
- Helm HPA 模板：deploy/helm/templates/hpa.yaml（fail-fast：minReplicas/maxReplicas required、至少一个 target threshold）
- Helm values：deploy/helm/values.yaml（autoscaling 段全 null，**不动**）+ values-onprem.example.yaml（待填）
- O1 历史报告：docs/acceptance/m6-o1-measurement-report-2026-10-05.md

## 收尾
- 每项落 PASS-/FAILCLOSED- 证据文件
- 全部完成后：`make gate` 全绿 + `git status` 核对
- 写 review record：docs/reviews/m8-batch5-performance-capacity-review-2026-10-12.md
- 写 handoff：docs/handoff/2026-10-12-m8-batch5-complete-handoff.md

## 注意
- kind 资源有限，多副本测量时注意 CPU/内存限额，避免节点 OOM
- as_load 是 IPv4-only（testbed/load/README.md 当前限制 #5）
- CPS 1280 是 loopback 模型下限，不是饱和点、不是承诺值
- 如某 CPS 档位 kind 资源不够，记录实测最高档位即可，不强求 1280
