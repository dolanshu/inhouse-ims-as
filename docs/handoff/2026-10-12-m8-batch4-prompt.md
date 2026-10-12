# M8 批次 4「签收与评审」— 新 Session 提示词

## 开场仪式
1. 读 AGENT.md、docs/README.md、docs/plan.md（M8 节）、docs/acceptance/m8-test-plan-matrix.md
2. `git status` 核对工作树
3. 确认批次 2/3/5 的证据文件已落盘（docs/acceptance/artifacts/m5/2026-10-12/）

## 当前状态
- 已完成：批次 1（发布与打包）、批次 2（SIP 对拍）、批次 3（kind/sim 证据）、批次 5（性能与容量）
- 分支 master，所有改动未提交（不许提交）
- 本批次依赖前序批次产出的全部证据
- 环境名：dev-win03ib7niepf0

## 核心边界（最重要）
**本批次不代签任何 REQ。** 「工程证据接受」≠ REQ 级验收通过 ≠ 里程碑签收。
所有 pass 转态须由维护者在 M8 退出评审中确认；agent 只做：
1. 逐行评审证据是否充分
2. 缺项补测（仅限工程层，不碰外部环境）
3. 给出 pass/n-a/defer 建议 + 理由
4. 准备矩阵行的更新草案（不直接改矩阵，等维护者批）

## 工作范围
### 1. S-1（白名单）评审
- 评审现有证据：白名单逻辑（ingress.py allowlist/peer）+ 变更走审批（F-14 联动）
- 缺项补测：白名单拒绝场景、白名单变更经审批后生效
- 证据：PASS/FAILCLOSED-s1-whitelist-review-2026-10-12.txt

### 2. S-4（RBAC + 审计不可篡改）评审
- durable audit 工程切片已在位（PostgresAuditStore + owner trigger 阻止 mutation/truncate）
- 补其正式全绿所缺部分：审计 append-only 验证、RBAC 权限矩阵验证
- 证据：PASS/FAILCLOSED-s4-rbac-audit-review-2026-10-12.txt

### 3. 矩阵 open 行逐行终态化
对 docs/acceptance/m8-test-plan-matrix.md 中每个 `open` 行，给出建议终态：
- **pass**：须有本版新证据（三元组留档），附证据文件路径
- **n-a**：附理由（如 v1.1 范围、非目标项）
- **defer**：附理由（如依赖外部环境 X1、客户集群、运营商 PKI）

需评审的 open 行（以矩阵实际为准）：
- F-1 ~ F-16（基本呼叫、Call-ID、翻译、SDP、Route、404、阻止、CANCEL、in-dialog、非2xx、竞态、控制台、审批、决策链）
- NF-2、NF-5、NF-9、NF-10、NF-13、NF-14、NF-15
- S-1、S-4
- D12/O5-HA

**依赖外部环境的行（NF-13 live 采集、NF-14 真实告警触发等）按理由转 defer，提请维护者评审。**

### 4. 矩阵更新草案
- 产出矩阵更新草案文档（docs/acceptance/m8-matrix-finalization-draft-2026-10-12.md）
- 每行：原状态 → 建议终态 → 理由 → 证据文件
- **不直接改 m8-test-plan-matrix.md**，草案等维护者批后由维护者或授权 agent 执行

## 硬纪律
- 主 agent 不写文件，派 writing subagent（general_purpose_task），一个工作树同时只一个
- 不执行任何 git 写操作
- **不直接改矩阵状态、不改 report.md 计数**——只出草案
- 证据四层：PASS-/FAILCLOSED- 前缀 → docs/acceptance/artifacts/m5/2026-10-12/；环境名 dev-win03ib7niepf0；三元组
- 缺项补测只做工程层（unit/contract/integration），不碰外部环境（客户集群、运营商 PKI）
- 维护者未确认前，任何行不得从 open 转 pass

## 关键文件
- 矩阵：docs/acceptance/m8-test-plan-matrix.md
- 执行依据：docs/handoff/2026-10-12-m8-scope-revision-internal-release-plan.md §2.4
- 批次 2 证据：docs/acceptance/artifacts/m5/2026-10-12/PASS-s5~s11-*.txt
- 批次 3 证据：docs/acceptance/artifacts/m5/2026-10-12/PASS-nf*/f15*/2-5-*.txt
- 批次 5 证据：docs/acceptance/artifacts/m5/2026-10-12/PASS-nf15*/o1*/hpa*.txt
- 白名单实现：platform/src/as_platform/sip/ingress.py
- 审计实现：platform/src/as_platform/config/audit_store.py 等

## 收尾
- S-1/S-4 评审证据落盘
- 矩阵终态化草案落盘（docs/acceptance/m8-matrix-finalization-draft-2026-10-12.md）
- 全部完成后：`make gate` 全绿 + `git status` 核对
- 写 review record：docs/reviews/m8-batch4-signoff-review-2026-10-12.md
- 写 handoff：docs/handoff/2026-10-12-m8-batch4-complete-handoff.md

## 注意
- 本批次最核心的纪律是「不代签」——所有 pass 建议都要标注「待维护者 M8 退出评审确认」
- 如某行证据不足，宁可标 defer 也不要标 pass
- 依赖 X1（抓取接线）或外部环境的行一律 defer，不强行补测
