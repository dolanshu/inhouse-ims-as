# M8 批次 3「kind/sim 证据」完成交接（2026-10-12）

## 0. 本文性质与边界

- 本文是 [`2026-10-12-m8-batch3-prompt.md`](2026-10-12-m8-batch3-prompt.md) 的完成交接，配套评审记录
  [`../reviews/m8-batch3-kind-sim-evidence-review-2026-10-12.md`](../reviews/m8-batch3-kind-sim-evidence-review-2026-10-12.md)。
- **不签收任何 REQ、不改变 `docs/acceptance/m8-test-plan-matrix.md` 状态、不改 report.md；不构成容量/SLA/RPO/RTO 承诺。**
- 环境：`dev-win03ib7niepf0`；工具 `tools/bin`（kind 0.24.0 / kubectl 1.31.4 / helm 3.16.4）。
- **未执行任何 git 写操作**；所有改动留在工作树，提交切分由维护者决定。

## 1. 完成清单（7/7）与证据三元组

| 项 | 结论 | 证据（三元组） |
|---|---|---|
| F-15 真 AS 全栈（含 NF-10） | 已验证（PASS） | (已验证, docs/acceptance/artifacts/m5/2026-10-12/PASS-f15-distribution-lifecycle-rollback-2026-10-12.txt, 2026-10-12) |
| NF-2 双 Deployment 隔离 | 已验证（PASS） | (已验证, docs/acceptance/artifacts/m5/2026-10-12/PASS-nf2-deployment-isolation-2026-10-12.txt, 2026-10-12) |
| NF-9 命名空间隔离 | 已验证（PASS） | (已验证, docs/acceptance/artifacts/m5/2026-10-12/PASS-nf9-namespace-isolation-2026-10-12.txt, 2026-10-12) |
| NF-4 滚动零丢失 | **失败已登记（FAILCLOSED，不是通过证据）** | (失败已登记, docs/acceptance/artifacts/m5/2026-10-12/FAILCLOSED-nf4-rolling-restart-inflight-loss-2026-10-12.txt, 2026-10-12) |
| NF-5 UDP/TCP/TLS 一致性 | 已验证（PASS） | (已验证, docs/acceptance/artifacts/m5/2026-10-12/PASS-nf5-simulator-transport-consistency-2026-10-12.txt, 2026-10-12) |
| 2.5 备份恢复演练 | 已验证（PASS，耗时为量级非承诺） | (已验证, docs/acceptance/artifacts/m5/2026-10-12/PASS-backup-restore-drill-bundled-pg-2026-10-12.txt, 2026-10-12) |
| P0 缺陷修复（取证中发现） | 已验证（PASS） | (已验证, docs/acceptance/artifacts/m5/2026-10-12/PASS-config-service-auth-distribution-409-fix-2026-10-12.txt, 2026-10-12) |

索引已更新：docs/acceptance/artifacts/m5/README.md（+7 行，FAILCLOSED 行标注「**不是通过证据**」）。

## 2. 关键结果摘要

- **F-15/NF-10**：两批健康→自动 applied（order_rev=5）→显式 apply 幂等 200；末批不健康→自动 rolled_back（rolled_back_to=1, health check failed）；首批后手动 rollback（rolled_back_to=2）。fleet-a 集群内真实收到 notify；「只通知首批」为设计行为。fleet 为协议 stub（AS 无 notify/bundle 接收端）。
- **NF-2**：删 translation 并重建窗口 anti-fraud 42/42 ×200，身份不变。
- **NF-9**：ns-A 停 PG+删两个 AS Deployment 期间 ns-B 58/58 ×200、7 Pod 身份不变；ns-A helm 恢复。
- **NF-4**：350 呼/轮 ×2 轮，分别 347/346 建立；timeout_invite 3/4、bye_sip_481 6/7、timeout_bye 4/3、unresolved 10/10。根因：单副本 headless 切换窗口 + DUM 对话态仅在进程内存。**待维护者裁决**。
- **NF-5**：UDP/TCP/TLS 三轮均 200×9、404×3、603×3，unresolved=0；TLS 为测试 CA。
- **2.5**：pg_dump 0.259s / cp 0.143s / drop+create 1.123s / pg_restore 0.704s（rc=0，stderr 0）/ config-service 重启 5.252s；12 项计数+三角色一致；审计 append-only 8 项守卫按拒；登录 200、rules rows=2、审计续写。
- **P0**：auth 模式分发必 409，删冗余 idle 检查（净 -10 行）+ 2 个端到端回归。

## 3. 代码/文件改动清单（均未提交）

| 文件 | 改动 | 来源 |
|---|---|---|
| services/config-service/src/as_config_service/api.py | 删 require_idle_distribution_connection 及 4 处调用（-10 行） | 本批 P0 修复 |
| services/config-service/tests/test_postgres_auth_api_integration.py | +212 行（PgHarness 扩 store；2 个真实 PG/HTTPS/CSRF 分发回归） | 本批 P0 修复 |
| testbed/sim-platform/Dockerfile.product | bullseye→bookworm（OpenSSL 3 事实注释） | 本批 NF-5 取证前置 |
| testbed/e2e/test_s1_replay_contract.py | ruff format 纯格式塌行 | 本批门禁修复（批次2 提交带入的不合规） |
| platform/tests/test_req_f6_f7_rule_priority_integration.py | except socket.timeout → TimeoutError（等价） | 同上 |
| platform/tests/test_req_f11_cancel_race_integration.py | 去无占位符 f-string 前缀（F541） | 同上 |
| docs/acceptance/artifacts/m5/2026-10-12/*.txt（7 份新证据） | 见 §1 | 本批 |
| docs/acceptance/artifacts/m5/README.md | +7 行索引 | 本批 |
| docs/reviews/m8-batch3-kind-sim-evidence-review-2026-10-12.md | 新增 | 本批 |
| docs/handoff/2026-10-12-m8-batch3-complete-handoff.md | 本文件 | 本批 |

非本批、本批未触碰：`.dockerignore`（批次 1 遗留修改）、`docs/handoff/2026-10-12-m8-batch5-prompt.md`（未跟踪，维护者预置的下一批提示词）、`docs/intro.md`（未跟踪，来源不明）。

## 4. 验证结果

- `make gate`（2026-10-12 本机，exit 0）：ruff format 546 files already formatted；ruff check All checks passed；mypy Success 90 files；pytest `-m "unit or contract"` **1140 passed, 227 deselected, 11 warnings**。
- `uv run pytest tests/test_evidence_discipline.py -q`：**117 passed**。
- config-service 全量（compose PG12.22 :55432，AS_PG_TEST_DSN 指定，凭据不入库）：**629 passed, 3 skipped**（wal_level=replica / PG 版本环境限制）。
- 原始取证记录留存于执行机临时目录（不入库）：/tmp/m8b3/（f15-run4.log、nf2-redrill.log、nf9-redrill.log、nf4.log、nf4-run2.log、nf5.log、drill2/、gate3.log 等）。

## 5. 集群现场状态

- **kind-as-m5**：ns `as-m5` release `as`（revision 4+，helm upgrade 恢复后全栈 Running，migrate Completed；fleet-a/fleet-b 协议 stub 保留）；ns `as-m5b` release `asb` 独立全栈保留。清理方式：`kubectl --context kind-as-m5 delete deploy fleet-a fleet-b -n as-m5`；整个第二全栈可 `helm --kube-context kind-as-m5 -n as-m5b uninstall asb`。
- **kind-as-m71**：ims-sim（scscf/ssbc-north/ssbc-south/uas/call-load）与 as-sut（bookworm 基底色 as-sut:dev，单架构 postgres:12.22 / redis 转存镜像，Calico v3.28.2 本地 -kind 镜像）全部 Running/migrate Completed。call-load UI 经 `kubectl -n ims-sim port-forward svc/ims-sim-ui 8088:8088` 访问。
- 本地 compose：as-m4b8-dev-postgres-1（PG12.22 :55432）、as-redis-test :6379、as-pg15-test :55434 仍在运行。

## 6. 待维护者事项

1. **B3-02 NF-4 裁决**：FAILCLOSED 是否立项（StateStore/S-SBC 透明桥、多副本对话归属、或维护窗口操作口径）；裁决前矩阵维持 blocked。
2. **B3-04**：config-service 单连接 PG 重启后不自动重连（500→重启恢复）是否立项。
3. **工作树处置**：§3 改动如何切分提交（含批次 2 提交带入的 3 处 lint/格式修复、批次 1 遗留 .dockerignore、两个未跟踪 docs 文件）。
4. 评审记录 Adjudication 13 行中 B3-01/02/04 标「待维护者确认/待裁决」，请逐行给最终裁决。
5. `docs/handoff/2026-10-12-m8-batch5-prompt.md` 已在工作树中，下一批启动前请确认其内容。

## 7. 纪律执行声明

- 主 agent 未直接写任何文件；全部文件改动经 general-purpose writing subagent 落盘并以 git status/diff 逐项核对；同一工作树同时仅一个 writing subagent。
- 无 git add/commit/tag/push/branch；无 REQ 签收、无矩阵/report 计数改动；证据文件无凭据/token/cookie；FAILCLOSED 已在 m5 README 索引标注「不是通过证据」。

## 8. 2026-10-12 维护者追加裁决：NF-4 签收 pass（接受实测呼损）

- 裁决（原话要点）：当前 release 接受该呼损程度；NF-4 mark pass；呼损在今后 release 通过 feature 做 enhancement。
- 口径：滚动升级行为已实测验证 + 在途呼损范围（UDP 两轮：受影响 13/14 呼、unresolved 各 10）被接受 = pass；**不是零丢失已达成**。
- 已落盘：PASS-nf4-rolling-upgrade-accepted-loss-2026-10-12.txt（含完整机理与候选增强方向）；FAILCLOSED 原始记录追加裁决指针、保留不改事实；m5 README 索引两行；矩阵 REQ-NF-4 行转 pass + 文末追加裁定节（pass 16→17、blocked 7→6）；plan.md §0 决策行；review record B3-02 关闭。
- 「滚动零呼损」为今后 release 增强 feature，本版不立项（与 FM、呼叫轨迹同流程）。
- 本节追加后未执行任何 git 写操作。
