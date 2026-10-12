# M8 批次 5「性能与容量（kind）」评审记录（2026-10-12）

## 当前状态（Current Status）

批次 5 四项工程目标全部落地：3 项 PASS（NF-15 多副本测量、O1 loopback 1280 内部复测、HPA 阈值填写）+ 1 项 FAILCLOSED（performance 层门禁终态，已登记，待维护者裁决）。未签收任何 REQ，矩阵 NF-15 行维持 open，report.md 计数未动。`make gate` 全绿（1150 passed, 227 deselected），证据纪律测试 127 passed，`make chart-check` OK。容量类告警未新增，ne-datasheet 容量取值与 4.1 正式报告维持阻塞。唯一待维护者事项 = performance 层门禁终态（B5-04）。

**2026-10-13 维护者追加裁决：批次 5 判定 pass。** 此为批次层面的工程接受（3 项 PASS 工程目标 + 1 项 FAILCLOSED 如实登记），**不是 REQ-NF-15 签收**，矩阵 NF-15 行维持 open，report.md 计数不动。维护者同时指示：测量证据须配通俗说明（已追加至两份测量证据末尾），并登记下一 release 增强方向——关闭 accept_all_invites、搭建真实下游 UAS、对完整 B2BUA 两腿路径做真实 socket 压测（见 B5-08/B5-09）。B5-04（performance 层门禁终态）不在本次 pass 覆盖范围内，仍待 M8 总审裁决。

## 1. 评审对象

- 取证范围：`docs/handoff/2026-10-12-m8-batch5-prompt.md` 的四项取证范围（NF-15 kind 多副本测量、O1 loopback 1280 内部复测、HPA 阈值填写、performance 层门禁终态登记）。
- 全部产出：4 个证据文件（见 §4）、`deploy/helm/values-onprem.example.yaml` 改动（+37 行 autoscaling 段）、证据索引 `docs/acceptance/artifacts/m5/README.md`（+4 行）。
- 执行依据：`docs/handoff/2026-10-12-m8-scope-revision-internal-release-plan.md` §2.5。
- 执行环境：dev-win03ib7niepf0，集群 kind-as-m5，命名空间 nf15-perf。

## 2. 评审日期与评审人

- 评审日期：2026-10-12。
- 评审人：AI agent 工程自审（AGENT.md §3.3）；维护者签字另列（见文末）。

## 3. 评审结论

**有条件通过。** 四项工程目标与证据三元组齐备，门禁全绿（`make gate` exit 0、证据纪律 127 passed、chart-check OK）。通过条件：

1. B5-04（performance 层门禁终态）待维护者裁决，agent 未实现阻塞层、未代为接受风险；
2. 提交切分由维护者决定，本批次未执行任何 git 写操作。

## 4. 证据三元组清单

| 项 | 三元组（结论, 证据, 日期） |
| --- | --- |
| NF-15 多副本测量 | (已验证, docs/acceptance/artifacts/m5/2026-10-12/PASS-nf15-multi-replica-measurement-2026-10-12.txt, 2026-10-12) |
| O1 loopback 1280（内部） | (已验证, docs/acceptance/artifacts/m5/2026-10-12/PASS-o1-loopback-cps-1280-2026-10-12.txt, 2026-10-12) |
| HPA 阈值填写 | (已验证, docs/acceptance/artifacts/m5/2026-10-12/PASS-hpa-threshold-filled-2026-10-12.txt, 2026-10-12) |
| performance 门禁终态 | (失败已登记-待裁决, docs/acceptance/artifacts/m5/2026-10-12/FAILCLOSED-performance-gate-terminal-state-2026-10-12.txt, 2026-10-12) |

## 5. 关键结果复核

- 现场：kind-as-m5 集群新增命名空间 nf15-perf；helm release `nf15`（anti-fraud 2 副本，requests 200m/256Mi，bundled PG/Redis + config-service）+ 临时 `sut-direct` Deployment（2/4 副本，podIP 广播绕过 Service）+ as-load-gen Pod；档位模型 accept-all / UDP / hold=0 / 每档 15s。
- NF-15 2 副本五档（20/80/320/640/1280 CPS）全部零失败：established=300/1200/4800/9600/19200，unresolved=0。
- per-pod CPU（以 200m request 为分母）：~160 CPS/Pod 约 50% request、~320 CPS/Pod 约 105%、~640 CPS/Pod 约 214%；内存最高档约 59%。
- 建立时延 p95：从 8.3ms（80 CPS）到 29-36ms（1280 CPS）。
- 4 副本@1280：经 podIP 直连完全均衡（各 14400 UDP 报文），资源占用线性一致。
- O1 loopback 1280：19200/19200 established，unresolved=0，p95 12.79ms。
- HPA 示例：enabled / minReplicas 2 / maxReplicas 4 / CPU 70 / MEM 70；默认 values.yaml 与 hpa.yaml 守卫零改动；example 渲染 2 HPA、默认渲染 0 HPA，两条守卫实测有效，chart-check OK。
- 架构发现：ClusterIP UDP 短流经 conntrack 钉选单端点（2400 呼叫仅约 10 个不同客户端源端口），SIP UDP 多副本均衡不能依赖 ClusterIP 随机分发。

## 6. 问题清单（gap）

- **B5-01 ClusterIP UDP 端点钉选**：架构发现，真实部署需每副本独立可达设计；本批次不立项，建议在目标环境设计阶段处理。
- **B5-02 测量模型局限**：accept-all / hold=0 / 单节点 kind，非业务判决路径、非 S-SBC、非饱和点；维护者已定口径为数值象征性、架构探索；不发布对外数字。
- **B5-03 4 副本档时延偏高（p95 79-88ms）**：根因为负载侧单 Pod 512 线程竞争，SUT 零失败；干净时延曲线以 2 副本为准。
- **B5-04 performance 层门禁终态**：(a) `make gate` 增加阻塞层，或 (b) M8 总审书面接受风险——待维护者裁决，agent 未实现、未代接受。
- **B5-05 20 CPS 首档 p50≈52ms**：冷启动预热，已在证据中说明，非退化。
- **B5-06 onprem 示例启用 HPA 但未给 useCases[].resources 数值**：注释已强制要求先在目标环境测量中配平 requests；示例文件保持象征性，不新增容量数字。
- **B5-07 原始数据存执行机 /tmp/m8b5/ 不入库**：沿用批次 3 惯例；关键配置与全部派生数字已逐字写入证据文件。

## 7. 边界与不宣称

- 不宣称 M8 全绿，不构成 M8 退出签字。
- 不签收 REQ-NF-15，矩阵 NF-15 行维持 open。
- 无对外容量数字；内部工程目标值不得写入对外材料。
- 容量类告警未新增；ne-datasheet 容量取值与 4.1 正式报告维持阻塞。
- 未执行任何 git 写操作（无 add/commit/tag/push/branch）。

## Adjudication

| ID | 来源 | 问题摘要 | 裁决 | 修改方案 | 状态 | 验证方式 | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| B5-01 | 本批评测 NF-15 | ClusterIP UDP 短流 conntrack 钉选单端点，多副本均衡不成立于该路径 | 接受（架构发现登记，不立项） | 证据文件记录机理与含义；目标环境设计采用每副本独立可达 | 已关闭 | 行为观察（per-pod UDP 计数 57604 vs 4 + conntrack 源端口采样） | 今后 release 目标环境设计输入 |
| B5-02 | 本批评测 NF-15/O1 | accept-all/hold=0/单节点 kind 模型局限 | 接受（维护者已定象征性口径） | 证据文件边界节写明，对外材料不引用 | 已关闭 | 文档更新 | AGENT.md §2 |
| B5-03 | 本批评测 NF-15 | 4 副本档时延受负载发生器线程竞争污染 | 部分接受 | 证据文件标注污染来源，时延结论以 2 副本曲线为准 | 已修改 | 行为观察 + 文档更新 | 如需可后续独立负载 Pod 复跑 |
| B5-04 | RC 计划 A-6 / scope §2.5 | performance 层是否进 make gate 阻塞 | 待裁决 | 二选一：实现阻塞层 或 M8 总审书面接受风险 | 待修改 | 维护者确认 | FAILCLOSED-performance-gate-terminal-state-2026-10-12.txt |
| B5-05 | 本批评测 NF-15 | 首档冷启动时延异常 | 接受（测量假象） | 证据文件说明，不重跑 | 已关闭 | 文档更新 | — |
| B5-06 | 本批评测 HPA | 示例 HPA 无数值型 resources 配套 | 部分接受 | 注释强制「先测配 requests 再启用」；不新增数字 | 已修改 | helm template + chart-check + 文档更新 | 上线前目标环境复测 |
| B5-07 | 本批评测 取证纪律 | 原始数据仅 /tmp 不入库 | 接受（沿用批次 3 惯例） | 关键配置与派生数字逐字入证据 | 已关闭 | 文档更新 | /tmp/m8b5/ 保留至维护者清理 |
| B5-08 | 2026-10-13 维护者裁决 | 批次 5 整体判定 | 接受（批次 5 判定 pass；非 REQ-NF-15 签收，矩阵行维持 open） | 两份测量证据追加通俗说明节；B5-04 仍单列待 M8 总审 | 已关闭 | 维护者确认（2026-10-13 口头裁决，agent 落盘） | 批次层面工程接受；不宣称 M8 退出签字 |
| B5-09 | 2026-10-13 维护者裁决 | 容量测量改用真实两腿：关闭 accept_all_invites、真实下游 UAS、B2BUA 入腿+出腿真实 socket 压测 | 接受（列下一 release enhancement，本版不立项） | 本版仅在证据/评审/交接登记方向；实现走下一 release 新 feature 流程 | 已关闭 | 维护者确认（2026-10-13 口头裁决，agent 落盘） | 覆盖业务判决与转发路径；对应 accept-all 模型局限（B5-02） |

**签字：** 维护者 2026-10-13 判定批次 5 pass（B5-08/B5-09 已裁决；B5-04 仍待 M8 总审）；AI agent 工程自审已于 2026-10-12 完成，裁决落盘于 2026-10-13。

---

本评审不签收任何 REQ、不改变矩阵状态与 report.md 计数、不构成对外容量承诺；未执行 git 写操作。
