# M8 矩阵 open 行终态化草案（2026-10-12）

## §0 本文性质与边界

- **本文是草案**，等维护者批。**不直接改** `docs/acceptance/m8-test-plan-matrix.md` —— 矩阵正文各行与「状态统计」一字未改；本文批准后由维护者或授权 agent 执行矩阵改写。
- **本批次不签收任何 REQ、不改 `docs/acceptance/report.md` 计数、不代签。** 本文所有 `pass` 建议行一律标注「**待维护者 M8 退出评审确认**」，禁止读作「已签收 / 已通过 / REQ 级验收通过」。
- **口径来源**：`docs/handoff/2026-10-12-m8-scope-revision-internal-release-plan.md` §2.4（每行给出 pass / n-a / defer 之一，必带理由；pass 须有本版新证据）。
- **N3 / N4 纪律延续**：「工程证据接受」≠ REQ 级验收通过 ≠ 里程碑签收。M5 REQ 级仍是不通过、M8 仍是「RC 就绪、待退出签字」。
- **执行环境**：`dev-win03ib7niepf0`（已登记于 `docs/environments.md`）。本版日期 **2026-10-12**。
- **未执行任何 git 写操作**（无 add / commit / tag / push / branch / 改 remote）。

---

## §1 逐行建议终态（17 行）

| req_id | 原状态 | 建议终态 | 理由（含边界） | 证据（三元组） |
|---|---|---|---|---|
| **F-4** | open | **pass**（工程证据接受，**待维护者 M8 退出评审确认**） | `PASS-s7a-sdp-corpus-expansion-2026-10-12.txt`：SDP 透传语料由 3 例扩到 5 例（新增 multi-m-line 318B、rich-audio 302B），5 passed，断言为字节恒等。矩阵该行原先挂的两个条件（「M8 review」+「更广 corpus」）均已满足。**边界**：语料为 testbed corpus，非线上话务；`docs/plan.md` §5.2 **D11**（SDP 原始 body 字节恒等的线上证明）仍是独立跟踪项，本行口径未包含它 | `(已验证, docs/acceptance/artifacts/m5/2026-10-12/PASS-s7a-sdp-corpus-expansion-2026-10-12.txt, 2026-10-12)` |
| **F-5** | open | **defer** | `PASS-s8-baseline-recapture-2026-10-12.txt` 消除了该行原先的 2 条 skip（12 passed、0 skipped），但同一文件「out of scope」节原文写明：trunk 侧 200 OK 的 **Record-Route 产品 AS 至今不转发**，属 **S8 实现范围**而非基线补采；矩阵该行另要求「产品真实路径行为验收另指 O3」。缺的是**实现立项**，不是外部环境 —— 按「补采前不排 S8 实现」的既有口径，不签 pass。提请注意该证据文件自述「REQ-F-5 matrix status not signed off」 | `(已验证, docs/acceptance/artifacts/m5/2026-10-12/PASS-s8-baseline-recapture-2026-10-12.txt, 2026-10-12)`；该文件自述「REQ-F-5 matrix status not signed off」，**不作为 pass 依据** |
| **F-8** | open | **defer** | 本版**无**针对 CANCEL 三分支的新实测证据；现有覆盖仅为 2026-10-06 `make gate` 的既有用例与 `docs/reviews/m8-phase-a-f6-f8-note-2026-10-06.md` 的 N2 #3（接受「字段契约已落地」，**C++→Python JSON 回调 defer post-RC**）。按 §2.4「pass 须有本版新证据」，不予 pass | **无本版新证据 —— 不构成三元组**；既有指针 `docs/reviews/m8-phase-a-f6-f8-note-2026-10-06.md`（N2 #3） |
| **F-9** | open | **defer** | BYE 分支已通（`PASS-s9-in-dialog-bye-routing-2026-10-12.txt`，`test_in_dialog_bye_is_forwarded_to_peer` PASSED + 回归 9 passed）；但 **re-INVITE / UPDATE 未实现**（`FAILCLOSED-s9-reinvite-update-not-implemented-2026-10-12.txt`：产品侧 `onOffer` L1219-1231 仅 harness 模式、无 `onUpdate` 覆写），该文件自述「待维护者决定是否立项」。属**部分覆盖**，不签全行 | `(已验证-仅 BYE 分支, docs/acceptance/artifacts/m5/2026-10-12/PASS-s9-in-dialog-bye-routing-2026-10-12.txt, 2026-10-12)`；`(能力缺失已登记, docs/acceptance/artifacts/m5/2026-10-12/FAILCLOSED-s9-reinvite-update-not-implemented-2026-10-12.txt, 2026-10-12)` |
| **F-10** | open | **pass**（工程证据接受，**待维护者 M8 退出评审确认**） | `PASS-s10-non-2xx-passthrough-2026-10-12.txt`：486 / 480 / 408 三码参数化全部 PASSED + 回归 12 passed；非 2xx 透传不改码。**边界**：未覆盖「有 early media 后转非 2xx」等变体 | `(已验证, docs/acceptance/artifacts/m5/2026-10-12/PASS-s10-non-2xx-passthrough-2026-10-12.txt, 2026-10-12)` |
| **F-11** | open | **defer** | 分支①已通（`PASS-s11-cancel-race-branch1-2026-10-12.txt`，`test_cancel_before_downstream_final_is_forwarded` PASSED）；但「**CANCEL 先于任何下游响应**」为已登记 gap（`FAILCLOSED-s11-cancel-before-any-downstream-response-2026-10-12.txt`：native `runtime_module.cxx` L1143-1162 守卫 `mOutboundDialogSet != nullptr`，此时该对话集尚未建立）。是否立项修复待维护者裁决，属实现缺口而非外部环境 | `(已验证-仅分支①, docs/acceptance/artifacts/m5/2026-10-12/PASS-s11-cancel-race-branch1-2026-10-12.txt, 2026-10-12)`；`(能力缺失已登记, docs/acceptance/artifacts/m5/2026-10-12/FAILCLOSED-s11-cancel-before-any-downstream-response-2026-10-12.txt, 2026-10-12)` |
| **F-16** | open | **defer** | 本版无本行新证据。维护者 2026-10-12 已裁定「F-16 轨迹联动部分只签非轨迹部分」，而轨迹联动随 F-13 转 v1.1；**非轨迹部分（decide 翻译用例）** 仅有 `make gate` 内既有覆盖（矩阵正文 L59 evidence 栏），无本版留档证据。**可转 pass 的条件**：若维护者接受以「2026-10-12 `make gate` 1174 passed + 矩阵 L59 既有 decide 覆盖」为工程证据，则非轨迹部分可转 pass（轨迹联动部分仍随 F-13 保持不验收、永不记 pass） | **无本版留档证据 —— 不构成三元组**；可转 pass 条件所指证据为 2026-10-12 `make gate` 运行记录与矩阵正文 L59 既有 evidence 栏 |
| **NF-2** | open | **pass**（工程证据接受，**待维护者 M8 退出评审确认**） | `PASS-nf2-deployment-isolation-2026-10-12.txt`：kind-as-m5 / ns as-m5 上，删除并重建 translation Pod 期间 anti-fraud `/health/live` + `/ready` 42/42 = 200，其 Pod UID / startTime / restartCount 全程不变。**边界**：覆盖 Pod / Deployment 级故障隔离，**不含节点级故障与网络分区** | `(已验证, docs/acceptance/artifacts/m5/2026-10-12/PASS-nf2-deployment-isolation-2026-10-12.txt, 2026-10-12)` |
| **NF-5** | open | **pass**（工程证据接受，**待维护者 M8 退出评审确认**） | `PASS-nf5-simulator-transport-consistency-2026-10-12.txt`：M7.1 仿真 S-SBC 上 UDP / TCP / TLS 三轮判决分布逐桶相同（15 呼：200×9 / 404×3 / 603×3，unresolved = 0），换传输协议不改变判决。**边界**：TLS 为**测试 CA**，非运营商 PKI；本证据不签收 REQ-S-2 / REQ-S-3 | `(已验证, docs/acceptance/artifacts/m5/2026-10-12/PASS-nf5-simulator-transport-consistency-2026-10-12.txt, 2026-10-12)` |
| **NF-9** | open | **pass**（工程证据接受，**待维护者 M8 退出评审确认**） | `PASS-nf9-namespace-isolation-2026-10-12.txt`：ns-A 停 bundled PostgreSQL + 删除两个 AS Deployment 期间，独立 ns-B（release `asb`）58/58 = 200，其 7 个 Pod 身份前后逐项不变。**边界**：两个命名空间**共享同一 kind 节点**，本证据不含节点宕机场景 | `(已验证, docs/acceptance/artifacts/m5/2026-10-12/PASS-nf9-namespace-isolation-2026-10-12.txt, 2026-10-12)` |
| **NF-10** | open | **pass**（工程证据接受，**待维护者 M8 退出评审确认**） | `PASS-f15-distribution-lifecycle-rollback-2026-10-12.txt`：控制面「草稿 → 审批 → 分发 → 回滚 → 审计」全链在真栈验证（末批健康 → 自动 applied + 幂等 apply；末批不健康 → 自动 rolled_back；手动 rollback 到 rev 2）+ config-service 套件在 `make gate` 内 + 代码无 git / GitOps 配置加载逻辑。**边界**：fleet-a / fleet-b 为**协议 stub**（产品 AS 无 notify / bundle 接收端），本证据**不证明 AS 进程消费 bundle**；bundled PG / Redis 为单副本，不覆盖生产 HA（D12 / O5） | `(已验证, docs/acceptance/artifacts/m5/2026-10-12/PASS-f15-distribution-lifecycle-rollback-2026-10-12.txt, 2026-10-12)` |
| **NF-13** | open | **defer** | 工程切片已在位（`platform/tests/test_resip_runtime_log_contract.py` 13 passed + decide / 遥测内核在 `make gate` 内）；但 **live 采集（Prometheus / Grafana + span 链）待环境**，且 **X1（抓取接线：`prometheus.io/scrape` annotation vs ServiceMonitor / PodMonitor）已由维护者 2026-10-12 裁定后置下一 release**，需运营商 monitoring-integration 标准输入（见 `docs/plan.md` §0 决策记录 2026-10-12 行）。依赖外部环境，按 §2.4 转 defer，不强行补测 | **本版无 live 采集新证据 —— 不构成三元组**；工程切片指针 `docs/plan.md` §0 决策记录（X1 后置） |
| **NF-14** | open | **defer** | 告警规则语法校验已过（promtool 3 组 10 条 `SUCCESS: 10 rules found`，见 `docs/acceptance/artifacts/m5/2026-10-11/PASS-alert-check-full-2026-10-11.txt`），但**语法校验 ≠ 真实触发**；Alertmanager 真实触发与通知通道待环境（通知通道为 M2 冻结事项延续）。依赖外部环境，不强行补测 | `(已验证-仅语法校验, docs/acceptance/artifacts/m5/2026-10-11/PASS-alert-check-full-2026-10-11.txt, 2026-10-11)`；真实触发**无本版证据** |
| **NF-15** | open | **defer** | harness 已落地并有实测（`PASS-nf15-multi-replica-measurement-2026-10-12.txt`、`PASS-o1-loopback-cps-1280-2026-10-12.txt`（**仅限内部**）、`PASS-hpa-threshold-filled-2026-10-12.txt`），但本版**明确未测饱和点**（PASS-nf15 自述「不是饱和点测量」），且 `performance` 层门禁终态（批次 5 **B5-04**）待维护者裁决。**可转 pass 的条件**：若维护者把本行口径收窄为「harness 落地 + 多副本实测」，本行可转 pass。四份证据文件本身均自述「不签收 REQ-NF-15」 / 「不计入通过清单」 | `(已验证-非饱和点, docs/acceptance/artifacts/m5/2026-10-12/PASS-nf15-multi-replica-measurement-2026-10-12.txt, 2026-10-12)`；`(已验证-仅限内部, docs/acceptance/artifacts/m5/2026-10-12/PASS-o1-loopback-cps-1280-2026-10-12.txt, 2026-10-12)`；`(已验证, docs/acceptance/artifacts/m5/2026-10-12/PASS-hpa-threshold-filled-2026-10-12.txt, 2026-10-12)`；`(门禁终态待裁决, docs/acceptance/artifacts/m5/2026-10-12/FAILCLOSED-performance-gate-terminal-state-2026-10-12.txt, 2026-10-12)` |
| **S-1** | open | **defer** | **两分结论。** ① 拒绝场景补测**通过**：本批次新增 `platform/tests/test_req_s1_whitelist_rejection.py`（9 条 unit，进 `make gate`），驱动真实 `ResipRuntimeListener._on_invite`，钉住白名单未命中 / 空策略（fail-closed）/ 证书不匹配 / 端点端口不符 / CIDR 外 / 明文 UDP-when-TLS-required 六路返回 **403**，并以 `received_at` 探针正向断言 `decide()` 未执行；补测中如实发现 `authorize_peer` 的地址与证书两维度是 **OR**（地址命中即放行、不要求对端证书），已钉住并注明**不构成 mTLS 强校验背书**。② 「白名单变更经审批后生效」**能力不存在**：`FAILCLOSED-s1-whitelist-change-approval-not-wired-2026-10-12.txt` 取证 —— `ConfigBundle`（`platform/src/as_platform/api/contract.py:71`，字段 :89-91）只有 version / rules / toggles；唯一可审批提案 `ManagedRuleChange`（`services/config-service/src/as_config_service/change_order.py:68`）只管规则；`platform/src` 内 `gate.install` / `install_with_overlap` **无产品调用点**；`load_transport_seam_from_env` 仅在 `sip_stack_service.py:126` / `:156` 构造时读一次（= 改 Helm values + 重启 Pod）。**且矩阵正文 L86 现有描述「白名单变更走审批（F-14 联动）」与代码事实冲突**（本草案只登记冲突，不改矩阵）。→ defer，待维护者二选一裁决：① 纳入变更单（属 v1.1 新 feature，本版不立项）；② 修订矩阵 L86 该说法。**若选②，本行可凭①的证据转 pass** | `(已验证-仅拒绝场景, docs/acceptance/artifacts/m5/2026-10-12/PASS-s1-whitelist-rejection-2026-10-12.txt, 2026-10-12)`；`(能力不存在已登记, docs/acceptance/artifacts/m5/2026-10-12/FAILCLOSED-s1-whitelist-change-approval-not-wired-2026-10-12.txt, 2026-10-12)` |
| **S-4** | open | **pass**（工程证据接受，**待维护者 M8 退出评审确认**） | 两份本批次新证据。① `PASS-s4-audit-append-only-2026-10-12.txt` —— 真 PostgreSQL（内部 compose，`127.0.0.1:55432`，DSN 口令已遮蔽）复跑 `test_postgres_audit_store_integration.py` **35 passed / 3 skipped**（3 条 skip 全为 `wal_level=replica` 的 PUBLICATION 门槛，**不含任何不可篡改守卫**）+ 新增 unit `services/config-service/tests/test_req_s4_audit_immutability.py` 7 条结构断言（行级 `BEFORE UPDATE OR DELETE` tgtype 27、语句级 `BEFORE TRUNCATE` tgtype 34、guard 体 `ERRCODE '23514'`、store 无 mutation API 且公开名字全集封闭）。② `PASS-s4-rbac-permission-matrix-2026-10-12.txt` —— 新增 `services/config-service/tests/test_req_s4_rbac_api_matrix_integration.py` **22 条**：`test_http_boundary_enforces_the_role_permission_matrix` 把角色 × 操作矩阵从内核纯函数推进到 **HTTP 边界 20 格**（read 全 200；submit 仅 viewer 403；approve / rollback 的 viewer + operator 403；manage_users 仅 admin 200），每条 403 精确断言权限拒绝 detail 以排除 CSRF / 404 / 双人原则冒充的假绿；`test_denied_write_at_the_http_boundary_persists_a_denied_audit_row` 断言越权落 **DENIED 审计行**（actor / outcome / action / resource 直连 DB 复核）；双人原则单列一条。既有覆盖另有 console 内核矩阵（`services/console/tests/test_access.py::test_role_permission_matrix`）。**边界（写全）**：结构断言 ≠ 数据库端实测（后者由真 PG integration 覆盖）；每条权限只取**一个代表性端点**，共用同一 `require_*_permission` 的其余端点未逐端点枚举；越权落痕只验 submit × viewer 一格 + 双人原则一格；**不含**外部 IAM / SSO 与运营商 PKI | `(已验证, docs/acceptance/artifacts/m5/2026-10-12/PASS-s4-audit-append-only-2026-10-12.txt, 2026-10-12)`；`(已验证, docs/acceptance/artifacts/m5/2026-10-12/PASS-s4-rbac-permission-matrix-2026-10-12.txt, 2026-10-12)` |
| **D12/O5-HA** | open | **defer** | 生产 Redis / PostgreSQL HA 属 2026-10-07 起登记的 **restriction**（Close 前无客户生产拓扑）；ADR-0026 已 accepted、Helm `stateStores` 骨架在位，但 **kind bundled state 不是本条**。依赖客户集群，本版不验收、不签 pass | **本版无客户生产拓扑证据 —— 不构成三元组**；restriction 指针 `docs/acceptance/m8-environment-evidence.md`（D12 / O5） |

---

## §2 状态词说明

`defer` 是本草案**新增**的状态词（矩阵现有状态词为 pass / fail / blocked / n-a / open），**须维护者确认后方可使用**。三者区别：

| 状态词 | 含义 | 是否可回转为 pass |
|---|---|---|
| **defer** | 本版**工程层已尽力**，缺的是**实现立项 / 外部环境 / 维护者裁决**之一；理由与缺项均已登记 | **可以** —— 条件满足（立项完成 / 环境到位 / 裁决作出）后可回转为 pass |
| **blocked** | **restriction** —— 本版**不能做**（如 2026-10-07 起 Close 前不联调真实运营商 S-SBC / 客户 K8s） | 本版不能靠工程层努力解除 |
| **n-a** | 永不验收、**永不记为 pass**（如 v1.1 范围项、非目标项，均附理由） | 否 —— 永不记 pass |

因此本文 10 行 `defer` 中：F-5 / F-9 / F-11 缺**实现立项**；NF-13 / NF-14 / NF-15 / D12/O5-HA 缺**外部环境或门禁裁决**；F-8 / F-16 缺**本版新证据**；S-1 缺**维护者二选一裁决**。

---

## §3 计数影响（若维护者全盘采纳）

- **现值**（矩阵追加节 2026-10-12 NF-4 裁定节登记值；矩阵正文「状态统计」原文未改）：
  **pass 17 / open 17 / blocked 6 / n-a 9 / fail 0**
- **建议后**：
  - **pass：17 → 24**（+7：F-4、F-10、NF-2、NF-5、NF-9、NF-10、S-4）
  - **defer：0 → 10**（新增状态词：F-5、F-8、F-9、F-11、F-16、NF-13、NF-14、NF-15、S-1、D12/O5-HA）
  - **open：17 → 0**
  - blocked 6 / n-a 9 / fail 0 **不变**

> **本报告仅为草案推算** —— `docs/acceptance/report.md` §0.5 计数**一字未改**；矩阵正文各行与「状态统计」**一字未改**。计数改写须维护者批准本草案后进行（承接方见 `docs/handoff/2026-10-12-m8-batch6-prompt.md` E-1）。

---

## §4 待维护者裁决清单

| ID | 事项 | 选项 | 影响行 |
|---|---|---|---|
| **D4-01** | S-1「白名单变更经审批后生效」二选一 | ① 纳入变更单（属 **v1.1 新 feature**，本版不立项，本行维持 defer）；② 修订矩阵 L86「白名单变更走审批（F-14 联动）」这一与代码事实冲突的说法 —— 若选②，本行可凭拒绝场景补测证据转 pass | S-1 |
| **D4-02** | 白名单 `authorize_peer` 的**地址 / 证书 OR 语义**是否收紧为 AND | 当前：地址命中即放行、**不要求对端证书**。是否作为 mTLS 强校验缺口立项 | S-1（边界，不阻塞 D4-01） |
| **D4-03** | 是否引入 `defer` 状态词 + 是否按 §3 改写矩阵计数 | 引入 / 不引入（改挂 blocked 或维持 open） | 全表 10 行 |
| **D4-04** | F-16 **非轨迹部分**可否以 `make gate` 既有覆盖转 pass | 接受「2026-10-12 `make gate` 1174 passed + 矩阵 L59 既有 decide 覆盖」为工程证据 → 转 pass；否则维持 defer | F-16 |
| **D4-05** | NF-15 是否**收窄口径**转 pass | ① 口径收窄为「harness 落地 + 多副本实测」→ 转 pass；② 随批次 5 **B5-04**（performance 层门禁终态）一并裁决后决定 | NF-15 |
| **D4-06** | 三项实现缺口是否 **v1.1 立项** | F-5（Record-Route 产品侧转发）、F-9（re-INVITE / UPDATE）、F-11（CANCEL 先于任何下游响应）—— 承接三份 FAILCLOSED / 能力缺失登记文件（F-9、F-11 各一份） | F-5、F-9、F-11 |
| **D4-07** | 7 个 pass 建议在 **M8 退出评审**中逐行确认 | F-4、F-10、NF-2、NF-5、NF-9、NF-10、S-4 —— 逐行确认后方可计入矩阵 pass | 7 行 |

---

## §5 边界声明

1. **不改矩阵** —— `docs/acceptance/m8-test-plan-matrix.md` 正文各行与「状态统计」一字未改；本文为追加式草案。
2. **不改 `report.md` 计数** —— `docs/acceptance/report.md` §0.5 一字未改；§3 仅为推算。
3. **不签收任何 REQ、不代签** —— 全部 7 个 pass 建议均标注「待维护者 M8 退出评审确认」；「工程证据接受」≠ REQ 级验收通过 ≠ 里程碑签收。
4. **未执行任何 git 写操作**。
5. **依赖外部环境的行一律 defer，未强行补测**（NF-13 / NF-14 的 live 采集与真实触发、D12/O5-HA 的客户生产拓扑）。
6. **补测仅限工程层** —— 新增/复跑的是 unit / integration 用例与结构断言，不触碰客户集群、运营商 PKI、生产 HA。
7. 引用证据一律三元组；**无本版新证据的行如实写「不构成三元组」**，不拼凑证据。
