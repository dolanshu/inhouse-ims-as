# M8 批次 5「性能与容量（kind）」完成交接（2026-10-12）

## 0. 本文性质与边界

本文为 M8 批次 5 完成交接，配套评审记录：`docs/reviews/m8-batch5-performance-capacity-review-2026-10-12.md`。

- 不签收任何 REQ，不改变矩阵状态，不改 report.md 计数。
- 不构成容量/SLA 承诺；内部工程目标值不得写入对外材料。
- 执行环境：dev-win03ib7niepf0（集群 kind-as-m5）。
- 未执行任何 git 写操作，全部改动留工作树，由维护者切分提交。

## 1. 完成清单（4/4）与三元组

| 项 | 三元组（结论, 证据, 日期） |
| --- | --- |
| NF-15 多副本测量 | (已验证, docs/acceptance/artifacts/m5/2026-10-12/PASS-nf15-multi-replica-measurement-2026-10-12.txt, 2026-10-12) |
| O1 loopback 1280（内部） | (已验证, docs/acceptance/artifacts/m5/2026-10-12/PASS-o1-loopback-cps-1280-2026-10-12.txt, 2026-10-12) |
| HPA 阈值填写 | (已验证, docs/acceptance/artifacts/m5/2026-10-12/PASS-hpa-threshold-filled-2026-10-12.txt, 2026-10-12) |
| performance 门禁终态 | (失败已登记-待裁决, docs/acceptance/artifacts/m5/2026-10-12/FAILCLOSED-performance-gate-terminal-state-2026-10-12.txt, 2026-10-12) |

## 2. 关键结果摘要

- **NF-15**：2 副本五档（20/80/320/640/1280 CPS × 15s，hold=0，accept-all UDP）全零失败。per-pod 资源（requests 200m/256Mi 为分母）：CPU 约 2%/11%/50%/105%/214%，内存约 7%/8%/14%/26%/59%；建立时延 p95 52.7/8.3/7.7/4.4/29-36ms（首档为冷启动）。4 副本@1280 经 podIP 直连完全均衡、资源线性。架构发现：ClusterIP UDP 短流经 conntrack 端点钉选，多副本均衡不能走 ClusterIP 路径。
- **O1**：loopback 1280 CPS，19200/19200 established，零 unresolved，p95 12.79ms（内部复测）。
- **HPA**：`deploy/helm/values-onprem.example.yaml` +37 行 autoscaling 段（enabled，minReplicas 2 / maxReplicas 4，CPU/MEM 各 70，customMetric null），逐字标注「kind 实测、非对外承诺、上线前须目标环境复测」；默认 values.yaml 与 hpa.yaml 零改动；渲染 2 HPA（example）/ 0 HPA（默认），两条守卫实测有效，chart-check OK。
- **performance 门禁**：FAILCLOSED 已登记，待维护者就 (a) 实现 `make gate` 阻塞层 / (b) M8 总审书面接受风险 作出裁决。

## 3. 改动文件清单（均未提交）

| 文件 | 改动 |
| --- | --- |
| deploy/helm/values-onprem.example.yaml | +37 行 autoscaling 段（本批次唯一代码/配置改动） |
| docs/acceptance/artifacts/m5/2026-10-12/PASS-nf15-multi-replica-measurement-2026-10-12.txt | 新增证据 |
| docs/acceptance/artifacts/m5/2026-10-12/PASS-o1-loopback-cps-1280-2026-10-12.txt | 新增证据 |
| docs/acceptance/artifacts/m5/2026-10-12/PASS-hpa-threshold-filled-2026-10-12.txt | 新增证据 |
| docs/acceptance/artifacts/m5/2026-10-12/FAILCLOSED-performance-gate-terminal-state-2026-10-12.txt | 新增证据 |
| docs/acceptance/artifacts/m5/README.md | +4 行索引（FAILCLOSED 行标注「不是通过证据」） |
| docs/reviews/m8-batch5-performance-capacity-review-2026-10-12.md | 新增评审记录 |
| docs/handoff/2026-10-12-m8-batch5-complete-handoff.md | 新增本交接 |

非本批次遗留（勿混入本批次提交）：`.dockerignore` modified（批次 1 遗留）；`docs/handoff/2026-10-12-m8-batch4-prompt.md`、`docs/handoff/2026-10-12-m8-batch6-prompt.md` 为维护者新增、未跟踪。测量期间维护者已提交 004904b "m8 batch3 done"；本批次未做任何 git 写操作。

## 4. 验证结果

`make gate`（2026-10-12，dev-win03ib7niepf0，exit 0）：

- 550 files already formatted；
- ruff：All checks passed；
- mypy：Success, 90 files；
- pytest：1150 passed, 227 deselected, 11 warnings；
- tests/test_evidence_discipline.py：127 passed。

`make chart-check`：chart-check: OK。helm 两条守卫的原始报错逐字记录于 PASS-hpa-threshold-filled-2026-10-12.txt 证据文件。

## 5. 集群与执行机现场（未清理，删除属不可逆动作）

kind-as-m5 新增命名空间 **nf15-perf**，内含：

- helm release `nf15`：anti-fraud 2 副本 + bundled PG/Redis + config-service；
- Deployment `sut-direct`：当前 4 副本（podIP 广播直连用）；
- Pod `as-load-gen`：`sleep infinity`，内含 /tmp/as_load 驱动。

清理命令（维护者决定时机）：

```
kubectl --context kind-as-m5 delete namespace nf15-perf
```

helm release 与临时 Deployment 均在该 ns 内，随 ns 删除即可，无需单独清理。

未触碰：kind-as-m5 既有 ns as-m5 / as-m5b（批次 3 现场）、kind-as-m71（批次 3 ims-sim/as-sut）、本地 compose 容器（as-m4b8-dev-postgres-1 等）。

原始测量数据：`/tmp/m8b5/`（nf15-2rep/、nf15-direct-2rep/、nf15-direct-4rep/、o1-loopback/、values 与清单快照、驱动脚本），保留至维护者清理。

## 6. 待维护者事项

1. **B5-04 裁决**：performance 层门禁终态——实现 `make gate` 阻塞层，或 M8 总审书面接受风险。
2. 评审记录 B5-01..B5-07 中 B5-04 的最终裁决与签字（其余 6 条已关闭/已修改）。
3. 工作树提交切分：values-onprem 示例 + 证据 + 索引 + 评审/交接为一组；`.dockerignore` 遗留分别处理。
4. nf15-perf 命名空间清理时机（见 §5 命令）。
5. NF-15 矩阵行维持 open；是否在批次 4「签收与评审」中按口径终态化由该批次决定，本批次不动。

> **去向指针（2026-10-13 追加；上方五项待维护者事项原文一律保留不改）**：本节尚未闭合的几项去向为 ——
> **第 5 项**：NF-15 矩阵行维持 `open`、是否终态化随测量批次一并裁决 →
> [`../next-release-v1.1-plan.md`](../next-release-v1.1-plan.md) **§5-5**；其本体（HPA 阈值已裁为填
> `values-onprem.example.yaml`、默认 `values.yaml` 保持 null，缺**带 per-pod CPU / 内存利用率**的测量批次；
> 2026-10-12 饱和点探测未记录资源数据）见同文档 **§4-9**；
> **第 3 / 4 项**：工作树提交切分、`nf15-perf` 命名空间清理时机 → 同文档 **§5-6**（以 `git status` 现场为准，不逐项固化）；
> **第 1 / 2 项**：B5-04 performance 层门禁终态的最终裁决与签字 —— 书面接受风险这一分支已于 2026-10-13 路径 C 行使，
> 是否仍需实现 `make gate` 阻塞层由维护者另行确认，其后如仍有遗留按同文档 **§9** 的启动前置另行排期。
> 后续状态盘点、汇报、handoff 涉及本节遗留项一律**只引该指针**，不逐项展开、不再列入「待维护者动作」。

## 7. 纪律执行声明

- 主 agent 未直接写任何仓库文件；全部仓库文件改动经 general-purpose writing subagent 落盘，并以 git status/diff 核对；同一工作树同时仅一个 writing subagent。
- /tmp 下仅操作脚本与原始测量数据。
- 无 git add/commit/tag/push/branch。
- 无 REQ 签收，无矩阵/report 计数改动。
- 证据文件无凭据/token/cookie。
- FAILCLOSED 已在索引标注「不是通过证据」；容量类告警未新增。

## 8. 2026-10-13 维护者追加裁决：批次 5 判 pass + 下一 release enhancement

- **批次 5 判定 pass**（维护者 2026-10-13）：批次层面工程接受；**不是 REQ-NF-15 签收**，矩阵 NF-15 行维持 open，report.md 计数不动，不构成 M8 退出签字。
- **通俗说明已追加**：两份测量证据（PASS-o1-loopback-cps-1280、PASS-nf15-multi-replica-measurement）末尾各追加「通俗说明」节——角色分工（as_load=UAC、AS=UAS）、一次呼叫 7 条报文与建立时延 4 报文窗口、accept-all 单腿的成因（resip_runtime.py 的 accept_all_invites 分支直接应答、不转发）、生产 B2BUA 两腿路径为何本次未覆盖、数字的确切含义与局限。
- **下一 release enhancement 方向**（B5-09）：关闭 accept_all_invites 开关，搭建真实下游 UAS，对「入腿 + 出腿」完整 B2BUA 两腿路径做真实 socket 压测，使容量测量覆盖业务判决与转发路径；本版不立项实现。
- **B5-04 未被本次 pass 覆盖**：performance 层门禁终态（(a) 阻塞层 或 (b) M8 总审书面接受风险）仍待 M8 总审裁决，FAILCLOSED 证据继续有效。
- 本次仅文档追加（2 份证据 + 本交接 + review record），未执行任何 git 写操作。
