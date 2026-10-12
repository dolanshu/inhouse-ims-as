# M8 批次 3「kind/sim 证据」评审记录（2026-10-12）

> **落盘日期：2026-10-12。** 本文件是
> [`../handoff/2026-10-12-m8-batch3-prompt.md`](../handoff/2026-10-12-m8-batch3-prompt.md)
> 7 项取证（F-15、NF-2、NF-9、NF-10、NF-4、NF-5、2.5 备份恢复）的评审载体。
> **agent 依据实测证据提出裁决建议，不代替维护者最终判断；本文件不签收任何 REQ、不改变
> `docs/acceptance/m8-test-plan-matrix.md` 状态、不改变 report.md 计数。**
> 环境一律为 `dev-win03ib7niepf0`。

## 当前状态（Current Status）

- **取证完成度：7/7 项全部执行完毕**（2026-10-12）。F-15/NF-10、NF-2、NF-9、NF-5、2.5 备份恢复为 **PASS（5 份证据）**；NF-4 为 **FAILCLOSED（1 份，不是通过证据）**；取证中发现并修复 **1 个 P0 产品缺陷**（1 份 PASS 证据 + 代码改动）。
- **P0 缺陷（auth 模式分发生命周期必 409）：已修复、已验证关闭**（真集群行为 + 629 passed）。
- **NF-4：维护者 2026-10-12 已裁决并签收 pass**（口径=滚动行为已实测验证 + 在途呼损范围被当前 release 接受；**非零丢失已达成**）；严格滚动零呼损登记为今后 release 的增强 feature（本版不立项）。证据 PASS-nf4-rolling-upgrade-accepted-loss-2026-10-12.txt；矩阵 REQ-NF-4 已更新 pass（16→17）、blocked 7→6。
- **门禁：`make gate` 全绿**（2026-10-12 本机）：ruff format 546 files already formatted；ruff check All checks passed；mypy Success: no issues found in 90 source files；pytest `-m "unit or contract"` **1140 passed, 227 deselected, 11 warnings**。证据纪律测试 117 passed。
- **config-service 全量（含 integration，compose PG12.22）：629 passed, 3 skipped**（skip 为 wal_level=replica / PG 版本环境限制）。
- **未签收任何 REQ；矩阵、report.md 未改；无任何 git 写操作。**
- **遗留待维护者事项**：config-service 单连接不自动重连是否立项（B3-04）、工作树处置（提交切分由维护者决定）。

## 1. 评审范围与方法

| 项 | 矩阵行 | 拓扑 | 证据文件 |
|---|---|---|---|
| F-15 真 AS 全栈（分发/健康/自动回滚/手动回滚） | REQ-F-15 / 5.4-F-15 | kind-as-m5 / ns as-m5 / release `as`（bundled PG12.22 + Redis7） | PASS-f15-distribution-lifecycle-rollback-2026-10-12.txt |
| NF-10 灰度分发/回滚 | REQ-NF-10 | 随 F-15 | 同上 |
| NF-2 双 Deployment 隔离 | REQ-NF-2 | kind-as-m5 / ns as-m5 | PASS-nf2-deployment-isolation-2026-10-12.txt |
| NF-9 命名空间隔离 | REQ-NF-9 | kind-as-m5：ns as-m5（release `as`）+ ns as-m5b（release `asb`） | PASS-nf9-namespace-isolation-2026-10-12.txt |
| NF-4 滚动升级零丢失 | REQ-NF-4 | kind-as-m71 / ns as-sut（产品 AS 单副本、headless） | FAILCLOSED-nf4-rolling-restart-inflight-loss-2026-10-12.txt（**不是通过证据**） |
| NF-5 仿真器中立（UDP/TCP/TLS） | REQ-NF-5 | kind-as-m71：ims-sim + as-sut | PASS-nf5-simulator-transport-consistency-2026-10-12.txt |
| 2.5 备份恢复演练 | 产品化计划 §2.5 / backup-restore.md §2/§4/§5 | kind-as-m5 bundled PG | PASS-backup-restore-drill-bundled-pg-2026-10-12.txt |
| P0 缺陷修复（取证中发现） | — | as-m5 实测 + compose PG 集成测试 | PASS-config-service-auth-distribution-409-fix-2026-10-12.txt |

方法：全部为真实 kind 集群 + 真实 helm release + 真实 SIP（M7.1 仿真 S-SBC，native reSIProcate 运行时）取证；每项保留命令输出原文入证据文件；失败项如实落 FAILCLOSED，不强行通过。

## 2. 各项评审结论

### 2.1 F-15 + NF-10：PASS（控制面行为已验证）

- CO-1 两批健康：distribution 201 start（仅首批通知）→ 首批健康 in_progress → 末批健康 completed 且变更单自动 applied（order_rev=5）；显式 apply 以 r1-1 幂等重放 200。
- CO-2 末批置 unhealthy：自动 rolled_back（rolled_back_to=1, reason="health check failed"），变更单 rolled_back，状态持久化。
- CO-3 首批后手动 rollback：rolled_back（rolled_back_to=2, reason="batch3 manual evidence drill"）。
- fleet-a 集群内真实收到全部 notify（change_id/version/bundle_version 与 API 一致）；fleet-b 仅 selftest —— 「只通知首批」为设计行为（test_fleet_api 钉死）。
- **边界**：产品 AS 无 notify/bundle 接收端（lld 事实），fleet-a/fleet-b 是协议 stub；证据证明 config-service 控制面，不证明 AS 消费 bundle；bundled 单副本不覆盖生产 HA。

### 2.2 NF-2：PASS

删除 translation Pod 并由 Deployment 重建的全窗口，anti-fraud 的 /health/live + /health/ready 42/42 为 200，anti-fraud Pod 名字/UID/startTime/restartCount 全程不变，translation 取得新 UID。

### 2.3 NF-9：PASS（附 1 个观察项）

ns-A 停 PostgreSQL 进程 + 删除 translation/anti-fraud 两个 Deployment 期间，独立 ns-B 全栈 58/58 探测 200，ns-B 7 个 Pod 身份（UID/startTime/restartCount）演练前后逐项不变；ns-A 经 helm upgrade 完整恢复。
观察项：PG 恢复后 config-service 单条共享连接不自动重连（登录 500），重启 Deployment 后恢复（实测 5.25s）。本批不改，列 Adjudication B3-04。

### 2.4 NF-4：实测在途呼损 → 2026-10-12 维护者裁决接受、签收 pass（零呼损滚动列今后 release feature）

- 拓扑：产品 AS 单副本（values-product-as.yaml `replicaCount: null` → 默认 1；注释说明第二进程会绑定同一组 SIP 端口），headless Service，RollingUpdate 25%/25%，preStop sleep 5 + terminationGracePeriodSeconds=300。
- 话务：UDP，全成功场景 T1/T5/F1，5cps×70s=350 呼/轮，第 12s rollout restart。
- 第 1 轮（20:47:37）：347/350 建立；timeout_invite 3、bye_sip_481 6、timeout_bye 4；unresolved 10。
- 第 2 轮（20:51:15，独立复现）：346/350；timeout_invite 4、bye_sip_481 7、timeout_bye 3；unresolved 10。
- 根因：① headless 单副本切换窗口存在 INVITE 无应答路径（UDP，对端按 Pod IP 寻址）；② 对话状态只在旧进程内存（reSIProcate DUM 无 serialize/deserialize API），切换后 BYE 到新进程 → 481/超时。与已登记 native gap（M2 拟以 S-SBC 透明桥 + StateStore 弥补）同源。preStop/grace 不等于在途对话迁移。
- **处理**：本批不改产品代码、不改 chart 默认值；FAILCLOSED 登记；矩阵维持 blocked；是否立项待维护者裁决（B3-02）。

**维护者裁决（2026-10-12）**：当前 release 接受该呼损级别，NF-4 mark pass，呼损在今后 release 通过 feature enhancement。验收口径为「实测行为已验证 + 损失范围接受」，不是零丢失已达成。

**切换时序（k8s 事件实测为 surge 顺序）**：t≈0 新 Pod 创建、旧 Pod 仍在端点；t≈1-3s 新 Pod readiness 通过前 headless DNS 同时返回旧+新 A 记录，S-SBC 逐消息 getaddrinfo 无缓存，INVITE 被分到旧/新 Pod；t≈3s 旧 Pod Terminating——端点摘除与 preStop sleep 5 并行无先后保证，且 sleep 不透明、进程不置 not-ready/不 drain；t≈3-8s 旧进程持有在途对话但已不在 DNS；t≈8s+ SIGTERM 退出。

**两类损失机理**：① timeout_invite（3/4）= UDP 切换窗口 INVITE 到已摘端点的旧 IP，无 ICMP 反馈、6s 无终态；新 Pod 对 INVITE 来者不拒，故无 5xx，全为静默超时。② 在途对话 unresolved（每轮恰好 10）= 对话态只在旧进程 DUM 内存，BYE 按 headless 名路由到新进程得 481，或命中已退出的旧 IP 超时；很多 BYE 失败时旧进程仍活在 preStop 内，但已移出 DNS 且对话不粘实例。

**结构性佐证**：5cps×hold 2s ≈ 稳态 10 并发，两轮 unresolved 各 10 = 切换时刻一窗在途对话整体受损，非随机丢包。

**今后 release 增强 feature 的候选方向（本版不立项、不预选）**：A 进程级 drain（preStop 触发 not-ready/拒新单 + sleep≥最长呼叫时长）；B S-SBC 透明桥 + StateStore 对话态外部化（M2 既定路线，覆盖长呼叫）；C Contact/Record-Route 实例粘性；D 维护窗口/先静默话务的运维口径。完整分析见 PASS-nf4-rolling-upgrade-accepted-loss-2026-10-12.txt。

### 2.5 NF-5：PASS（附 PKI 边界）

UDP/TCP/TLS 各 15 呼（T1/T4/T5/F1/F2），三轮判决分布逐桶相同：200×9 / 404×3 / 603×3，unresolved=0，无传输级错误。TLS 使用测试 CA（非运营商 PKI），不签收 REQ-S-2/S-3；呼数/时延是本轮运行值，非容量承诺。

### 2.6 2.5 备份恢复：PASS（耗时为量级，非承诺）

真 DROP（terminate+DROP，PG12 不支持 WITH FORCE）后 pg_restore rc=0、stderr 0 字节；12 项计数 + 三角色前后一致，两 schema 恢复；审计 append-only 8 项守卫按拒（UPDATE/DELETE/TRUNCATE/change_orders_events/大写 outcome CHECK/id 列/插入后篡改回滚）；控制台登录 200、managed-rules 200 rows=2、审计续写。实测：dump 0.259s、cp 0.143s、drop+create 1.123s、restore 0.704s、config-service 重启 5.252s —— **仅描述本次 lab 小数据集，不预设 RPO/RTO**；客户演练仍以 backup-restore.md §5 模板为准。

### 2.7 P0 缺陷：auth 模式分发生命周期必 409（已修复关闭）

- 症状：真集群 HTTPS 登录 + CSRF 后 distribution start 稳定 409 "distribution connection is not idle"，reports/apply/rollback 同受影响；无 auth 路径不触发，故此前测试未暴露。
- 根因：单条共享 psycopg 连接被 auth 路由依赖（resolve_session/verify_csrf）的 SELECT 置入 INTRANS，内部 require_idle_distribution_connection 必失败；入口中间件 serialize_api_request 已有 IDLE 检查 + 出口 rollback，内部检查重复且层级错误。
- 修复：删该函数与 4 处调用（净 -10 行）；新增 2 个真实 PG + HTTPS 登录 + CSRF 端到端回归（start→reports→自动 applied→幂等 apply；手动 rollback）。
- 验证：目标文件 19 passed（含 2 新增）；config-service 全量 629 passed/3 skipped；修复后真集群 F-15 全链路 200/201。

### 2.8 取证工程侧处置（非产品功能）

- 产品镜像基底 bullseye→bookworm（native 扩展 2026-10-12 重编译后链接 libssl.so.3，bullseye 无此库）：仅改 testbed/sim-platform/Dockerfile.product。
- kind load 多架构 manifest list 失败：postgres:12.22 / redis:7-alpine / calico v3.28.2 三镜像以 `docker build --platform linux/amd64` 转存单架构后加载；calico 另 set image 到 `-kind` tag。属现场运维手段，无仓库文件改动。
- 批次 2 提交（090312c）带入 3 个 ruff 不合规（test_s1_replay_contract.py 格式、UP041、F541），本批为门禁全绿做纯格式/等价修复（Python 3.10 起 socket.timeout 即 TimeoutError 别名）。

## 3. 边界总述（本批不做/不证明）

1. 不签收任何 REQ；矩阵 F-15/5.4-F-15/NF-2/NF-4/NF-5/NF-9/NF-10 状态词维持原样（NF-4 仍 blocked）。
2. fleet stub 不是 AS bundle 接收端；kind 单节点不证明节点级容错；bundled 单副本不证明生产 HA（D12/O5）。
3. NF-5 的 TLS 为测试 CA；所有呼数/时延/备份耗时均非容量、SLA、RPO/RTO 承诺。
4. NF-4 损失不通过调参/换说法消化；FAILCLOSED 与根因如实入档。
5. 不含任何凭据/token/抓包；dump 文件留在临时目录不入库。

## Adjudication

| ID | 来源 | 问题摘要 | 裁决 | 修改方案 | 状态 | 验证方式 | 备注 |
|---|---|---|---|---|---|---|---|
| B3-01 | F-15 取证 | auth 开启时分发 start/reports/apply/rollback 必 409（共享连接被 auth SELECT 置入 INTRANS + 冗余 idle 检查）—— P0 产品缺陷 | 接受 | 删 require_idle_distribution_connection 及 4 处调用（净 -10 行），新增 2 个真实 PG/HTTPS/CSRF 端到端回归测试 | 已验证 | 目标文件 19 passed；config-service 629 passed/3 skipped；修复后真集群 F-15 全链路 200/201 | 修复证据 PASS-config-service-auth-distribution-409-fix-2026-10-12.txt；待维护者确认 |
| B3-02 | NF-4 两轮话务 | 单副本 headless 拓扑下 rollout restart 在途损失：timeout_invite 3/4、bye_sip_481 6/7、timeout_bye 4/3、unresolved 10/10（受影响 3.7%/4.0%） | 接受 | 维护者 2026-10-12 裁决：当前 release 接受该呼损级别，REQ-NF-4 按「实测行为已验证+损失范围接受」签 pass（非零丢失已达成）；严格零呼损滚动列今后 release 增强 feature，本版不立项，启动走 requirement→ADR→design→review（候选方向 A 进程级 drain / B 透明桥+StateStore / C 实例粘性 / D 维护窗口） | 已关闭 | 维护者 2026-10-12 确认；PASS-nf4-rolling-upgrade-accepted-loss-2026-10-12.txt；矩阵 REQ-NF-4 行转 pass（pass 16→17、blocked 7→6） | 原始失败记录 FAILCLOSED-nf4-...txt 保留（不是通过证据）；仅 UDP 实测，不外推 TCP/TLS |
| B3-03 | F-15 notify 记录 | fleet-b 仅收到 selftest，被疑漏发 | 驳回（作为缺陷） | 无代码修改；证据文件如实标注「只通知首批」为设计行为、fleet 为协议 stub | 已关闭 | test_fleet_api 既有测试 + F-15 notify 原文 | 设计语义，非回归 |
| B3-04 | NF-9 / 备份演练 | PG 重启后 config-service 单条共享连接不自动重连（未重启前登录 500，重启 Deployment 后 200，实测 5.25s） | 部分接受 | 本批仅登记不改；建议后续评估连接重连/连接池 | 待修改 | 两次演练实测 500→重启后 200；PASS-nf9 / PASS-backup-restore | 运维观察项，是否立项待维护者 |
| B3-05 | NF-5 环境 | TLS 证书为测试 CA（自签） | 接受（作为边界） | 不签收 REQ-S-2/S-3，证据边界节标注「非运营商 PKI」 | 已关闭 | PASS-nf5 证据边界节 + UI pki_notice | — |
| B3-06 | as-sut 部署 | 产品镜像 bullseye 无法加载 native 扩展（libssl.so.3 缺失，CrashLoop） | 接受 | testbed/sim-platform/Dockerfile.product 基底升 bookworm（注释写明 OpenSSL 3 事实） | 已验证 | translation Pod 三端口 RESIP_RUNTIME_LISTENING + NF-5 三传输全 200 | 仅 testbed 产品镜像，发布镜像另行处置 |
| B3-07 | 镜像加载 | kind load 多架构 manifest list 报 content digest not found / ImagePullBackOff | 接受（运维手段） | postgres:12.22、redis:7-alpine、calico v3.28.2 转单架构（--platform linux/amd64）后加载；calico set image 到 -kind tag | 已验证 | 三个 kind 集群相关工作负载 Running/Completed | 无仓库文件改动；过程见 handoff |
| B3-08 | make gate | 批次 2 提交（090312c）带入 ruff 不合规：test_s1_replay_contract.py 格式、test_req_f6_f7 的 UP041、test_req_f11 的 F541 | 接受 | ruff format 单文件 + 两处等价小修（socket.timeout→TimeoutError；去无占位 f 前缀） | 已验证 | make gate 全绿（1140 passed） | Python 3.10 起二者同一对象；纯格式/等价 |
| B3-09 | 2.5 演练 | 备份/恢复实测秒级耗时是否可作 RTO/RTO 依据 | 驳回（作为承诺） | 证据仅写「本次实测量级，非承诺」；客户值仍由 backup-restore.md §5 演练方填写 | 已关闭 | PASS-backup-restore 证据边界节 | 不对外引用为 SLA |
| B3-10 | 备份演练首次 restore | PG12 不支持 DROP DATABASE WITH(FORCE)，首次 DROP 失败致 restore 落回旧库 | 接受（流程修正） | 改 pg_terminate_backend + 普通 DROP，先验证 tables_fresh_db=0 再 restore | 已验证 | 二次演练 restore rc=0、stderr 0 字节、计数一致 | runbook 命令本身不涉及该语法 |
| B3-11 | 收尾现场 | fleet-a/fleet-b 协议 stub 与 as-m5b 第二全栈是否清理 | 接受（保留） | 默认保留在 kind-as-m5，handoff 说明用途与清理方式 | 已关闭 | 本记录 + handoff 现场节 | 不落仓库（/tmp 驱动 + 集群内 YAML） |
| B3-12 | 工作树核对 | .dockerignore 为批次 1 遗留改动、docs/handoff/2026-10-12-m8-batch5-prompt.md 与 docs/intro.md 为非本批文件 | 驳回（并入本批提交） | 本批不动、不提交，交维护者处置 | 已关闭 | git status 已在 handoff 列示 | 提交切分由维护者决定 |
| B3-13 | 审计续写核对 | 失败/回滚的演练 INSERT 消耗序列值（id 空洞 94/95/96） | 驳回（作为问题） | 无修改；属 PostgreSQL 序列正常行为 | 已关闭 | PASS-backup-restore 证据注明 | — |
