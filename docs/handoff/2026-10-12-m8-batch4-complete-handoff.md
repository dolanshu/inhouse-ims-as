# M8 批次 4「签收与评审」完成交接（2026-10-12）

## 0. 本文性质与边界

本文为 M8 批次 4 完成交接，配套评审记录：`docs/reviews/m8-batch4-signoff-review-2026-10-12.md`；配套矩阵终态化草案：`docs/acceptance/m8-matrix-finalization-draft-2026-10-12.md`。

- **不签收任何 REQ，不改变矩阵状态，不改 `report.md` 计数** —— 7 个 pass 建议一律标注「待维护者 M8 退出评审确认」。
- 「工程证据接受」≠ REQ 级验收通过 ≠ 里程碑签收；M5 REQ 级仍是不通过、M8 仍是「RC 就绪、待退出签字」。
- 执行环境：`dev-win03ib7niepf0`（审计复测用内部 compose PostgreSQL，容器 `as-m4b8-dev-postgres-1`，DSN `127.0.0.1:55432`，口令已遮蔽）。
- 未执行任何 git 写操作，全部改动留工作树，由维护者切分提交。

## 1. 完成清单与三元组

| 项 | 三元组（结论, 证据, 日期） |
| --- | --- |
| S-1 白名单拒绝场景补测（9 条 unit） | (已验证-仅拒绝场景, docs/acceptance/artifacts/m5/2026-10-12/PASS-s1-whitelist-rejection-2026-10-12.txt, 2026-10-12) |
| S-1「白名单变更经审批后生效」取证 | (能力不存在已登记, docs/acceptance/artifacts/m5/2026-10-12/FAILCLOSED-s1-whitelist-change-approval-not-wired-2026-10-12.txt, 2026-10-12) |
| S-4 审计 append-only（真 PG 复跑 + 7 条结构断言 unit） | (已验证, docs/acceptance/artifacts/m5/2026-10-12/PASS-s4-audit-append-only-2026-10-12.txt, 2026-10-12) |
| S-4 RBAC 权限矩阵（22 条 HTTP 边界 integration） | (已验证, docs/acceptance/artifacts/m5/2026-10-12/PASS-s4-rbac-permission-matrix-2026-10-12.txt, 2026-10-12) |
| 矩阵 17 个 open 行逐行终态化草案（7 pass / 10 defer，均待维护者确认） | (草案-待批, docs/acceptance/m8-matrix-finalization-draft-2026-10-12.md, 2026-10-12) |

## 2. 关键结果摘要

- **S-1 拒绝场景补测通过**：新增 `platform/tests/test_req_s1_whitelist_rejection.py`（9 条 unit，进 `make gate`），驱动真实 `ResipRuntimeListener._on_invite`，钉住白名单未命中 / 空策略（fail-closed）/ 证书不匹配 / 端点端口不符 / CIDR 外 / 明文 UDP-when-TLS-required 六路返回 **403**，并以 `received_at` 探针正向断言 `decide()` 未执行。补测中**如实发现** `authorize_peer` 的地址与证书两维度是 **OR**（地址命中即放行、不要求对端证书），已钉住并注明**不构成 mTLS 强校验背书**（提为 D4-02）。
- **S-1「变更经审批后生效」能力不存在**：FAILCLOSED 取证 —— `ConfigBundle`（`platform/src/as_platform/api/contract.py:71`，字段 :89-91）只有 version/rules/toggles；唯一可审批提案 `ManagedRuleChange`（`services/config-service/src/as_config_service/change_order.py:68`）只管规则；`platform/src` 内 `gate.install` / `install_with_overlap` **无产品调用点**；`load_transport_seam_from_env` 仅在 `sip_stack_service.py:126`/`:156` 构造时读一次（= 改 Helm values + 重启 Pod）。**并且矩阵正文 L86「白名单变更走审批（F-14 联动）」与代码事实冲突**，只登记、不改矩阵（提为 D4-01）。agent **未实现**该能力。
- **S-4 审计 append-only**：真 PostgreSQL（内部 compose）复跑 `test_postgres_audit_store_integration.py` → **35 passed / 3 skipped**（3 条 skip 全为 `wal_level=replica` 的 PUBLICATION 门槛，**不含**任何不可篡改守卫）+ 新增 `test_req_s4_audit_immutability.py` 7 条结构断言（行级 `BEFORE UPDATE OR DELETE` tgtype 27、语句级 `BEFORE TRUNCATE` tgtype 34、guard 体 `ERRCODE '23514'`、store 无 mutation API 且公开名字全集封闭）。**结构断言 ≠ 数据库端实测**，后者由真 PG integration 覆盖。
- **S-4 RBAC 权限矩阵**：新增 `test_req_s4_rbac_api_matrix_integration.py` 22 条，把矩阵从内核纯函数推进到 **HTTP 边界 20 格**（read 全 200；submit 仅 viewer 403；approve / rollback 的 viewer+operator 403；manage_users 仅 admin 200），每条 403 精确断言权限拒绝 detail 以排除 CSRF / 404 / 双人原则冒充的假绿；另验证越权落 **DENIED 审计行**（直连 DB 复核）与双人原则单列。边界：每条权限只取一个代表性端点、越权落痕只验两格、不含外部 IAM / SSO 与运营商 PKI。
- **矩阵终态化草案**：17 行逐行给建议终态与理由 —— **7 行 pass**（F-4、F-10、NF-2、NF-5、NF-9、NF-10、S-4）**全部待维护者 M8 退出评审确认**；**10 行 defer**（F-5、F-8、F-9、F-11、F-16、NF-13、NF-14、NF-15、S-1、D12/O5-HA）。若全盘采纳：pass 17 → 24、defer 0 → 10、open 17 → 0，blocked 6 / n-a 9 / fail 0 不变。`defer` 为本草案**新增**状态词，须维护者确认后方可使用（D4-03）。

## 3. 改动文件清单（均已落盘、均未提交）

| 文件 | 改动 |
| --- | --- |
| `platform/tests/test_req_s1_whitelist_rejection.py` | 新增，9 条 unit（S-1 拒绝场景） |
| `services/config-service/tests/test_req_s4_audit_immutability.py` | 新增，7 条 unit（审计不可篡改结构断言） |
| `services/config-service/tests/test_req_s4_rbac_api_matrix_integration.py` | 新增，22 条 integration（RBAC 权限矩阵 HTTP 边界，真 PG） |
| `docs/acceptance/artifacts/m5/2026-10-12/PASS-s1-whitelist-rejection-2026-10-12.txt` | 新增证据 |
| `docs/acceptance/artifacts/m5/2026-10-12/FAILCLOSED-s1-whitelist-change-approval-not-wired-2026-10-12.txt` | 新增证据（**不是通过证据**） |
| `docs/acceptance/artifacts/m5/2026-10-12/PASS-s4-audit-append-only-2026-10-12.txt` | 新增证据 |
| `docs/acceptance/artifacts/m5/2026-10-12/PASS-s4-rbac-permission-matrix-2026-10-12.txt` | 新增证据 |
| `docs/acceptance/artifacts/m5/README.md` | 索引表 +6 行（批次 5 的 4 行 + S-1 两行 + S-4 两行）；FAILCLOSED 行同行含「不是通过证据」 |
| `docs/acceptance/m8-matrix-finalization-draft-2026-10-12.md` | 新增矩阵终态化草案 |
| `docs/reviews/m8-batch4-signoff-review-2026-10-12.md` | 新增评审记录 |
| `docs/handoff/2026-10-12-m8-batch4-complete-handoff.md` | 新增本交接 |

**非本批次遗留（勿混入本批次提交）**：`.dockerignore`（批次 1）、`deploy/helm/values-onprem.example.yaml`（批次 5）、批次 5 的四份证据与其评审 / 交接、`docs/handoff/2026-10-12-m8-batch4-prompt.md` 与 `docs/handoff/2026-10-12-m8-batch6-prompt.md`（维护者新增、未跟踪）。

**未改动**：`docs/acceptance/m8-test-plan-matrix.md`、`docs/acceptance/report.md`、`docs/plan.md`、`docs/environments.md`、任何产品代码与既有测试。

## 4. 验证结果

环境 `dev-win03ib7niepf0`：

- `make gate` → **`1174 passed, 249 deselected, 11 warnings`，0 skipped**，exit 0。
- `uv run pytest tests/test_evidence_discipline.py -q` → **`135 passed`**，exit 0（补测前 127，+8 为新增 4 份证据各触发 2 条参数化守卫）。
- S-1 新增测试 → **9 passed**。
- S-4 unit → **7 passed**；S-4 integration → **22 passed**（真 PostgreSQL `127.0.0.1:55432`，容器 `as-m4b8-dev-postgres-1`）。
- 审计既有 integration 复跑 → **35 passed, 3 skipped**（3 条 skip 全为 `wal_level=replica` 的 PUBLICATION 门槛，不含任何不可篡改守卫）。

## 5. 待维护者事项

1. **D4-01**：S-1「白名单变更经审批后生效」二选一 —— ① 纳入变更单（属 v1.1 新 feature，本版不立项，该行维持 defer）；② 修订矩阵 L86「白名单变更走审批（F-14 联动）」这一与代码事实冲突的说法（选②则该行可凭拒绝场景补测证据转 pass）。
2. **D4-02**：白名单 `authorize_peer` 地址 / 证书 **OR** 语义是否收紧为 AND（当前地址命中即放行、不要求对端证书）。
3. **D4-03**：是否引入 `defer` 状态词 + 是否按草案 §3 改写矩阵计数（pass 17→24 / defer 0→10 / open 17→0）。
4. **D4-04**：F-16 非轨迹部分可否以「2026-10-12 `make gate` 1174 passed + 矩阵 L59 既有 decide 覆盖」为工程证据转 pass。
5. **D4-05**：NF-15 是否收窄口径为「harness 落地 + 多副本实测」转 pass，或随批次 5 **B5-04** 一并裁决。
6. **D4-06**：F-5（Record-Route 产品侧转发）、F-9（re-INVITE / UPDATE）、F-11（CANCEL 先于任何下游响应）三项是否 v1.1 立项（承接三份能力缺失登记文件，其中 F-9 / F-11 各有一份 FAILCLOSED）。
7. **D4-07**：7 个 pass 建议（F-4、F-10、NF-2、NF-5、NF-9、NF-10、S-4）在 M8 退出评审中逐行确认。
8. **工作树提交切分**：本批次（3 个新增测试 + 4 份证据 + 索引 +6 行 + 草案 / 评审 / 交接）为一组；批次 1 的 `.dockerignore`、批次 5 的 `values-onprem.example.yaml` 与其证据 / 评审 / 交接分别处理。
9. **批次 6 承接**：`report.md` §0.5 计数取值**以本草案为取值依据**（`docs/handoff/2026-10-12-m8-batch6-prompt.md` E-1）；草案未获批准前，批次 6 不得先行改写计数。

> **去向指针（2026-10-13 追加；上方九项待维护者事项原文一律保留不改）**：本节尚未闭合的几项去向为 ——
> **第 3 项**：`defer` 状态词是否长期沿用（该词已按本批次终态化代签落地并注明「本次新增」）→
> [`../next-release-v1.1-plan.md`](../next-release-v1.1-plan.md) **§5-4**；
> **第 6 项**：**F-5（Record-Route）/ F-9（re-INVITE / UPDATE）/ F-11（CANCEL 先于任何下游响应）的 v1.1 立项** →
> 同文档 **§3 第 1 / 3 / 4 行**（同列的 F-8 CANCEL 三分支为第 2 行）；
> **第 5 项**：NF-15 口径（随带 per-pod 利用率的测量批次一并裁决） → 同文档 **§4-9**；
> **第 8 项**：工作树提交切分 → 同文档 **§5-6**。
> 后续状态盘点、汇报、handoff、新 session 开场涉及本节遗留项一律**只引该指针**，不逐项展开、不再列入「待维护者动作」。

## 6. 纪律执行声明

- 主 agent 未直接写任何仓库文件；全部仓库文件改动经 writing subagent 落盘，并以 `git status` / diff 核对；同一工作树同时仅一个 writing subagent。
- 无 git add / commit / tag / push / branch / 改 remote；未执行任何 git 写操作。
- 未改矩阵任何行状态与「状态统计」；未改 `report.md` §0.5 计数；未改任何产品代码与既有测试。
- 不签收任何 REQ、不签收里程碑；全部 pass 建议标注「待维护者 M8 退出评审确认」。
- 依赖外部环境的行（NF-13 / NF-14 的 live 采集与真实触发、D12/O5-HA 的客户生产拓扑）一律 defer，未强行补测；补测仅限工程层（unit / integration / 结构断言）。
- 证据文件无凭据 / token / cookie（审计 DSN 口令已遮蔽为 `***`）；环境名一律 `dev-win03ib7niepf0`，未出现匿名的「本机」。
- 新增 FAILCLOSED 证据已在索引 `docs/acceptance/artifacts/m5/README.md` 标注「不是通过证据」。

---

## 7. 代签执行结果（2026-10-13）

- **授权来源**：维护者 2026-10-13 原话「**接受建议，授权你代签**」。
- **落地范围**：**三项裁决**（B5-04 = **(b)** M8 总审书面接受风险；S-1 二选一 = **①** 修订矩阵 L86 描述；白名单地址 / 证书 **OR** = **本版接受**）与 **17 行终态** 已**全部落地**；落点 = `docs/acceptance/m8-test-plan-matrix.md` 的「M8 批次4 终态化代签（2026-10-13）」节（追加式，矩阵正文各行与「状态统计」原文未改）。
- **终态计数**：**pass 27 / defer 4 / blocked 9 / n-a 9 / open 0 / fail 0**（defer 为本次新增状态词：F-5 / F-8 / F-9 / F-11；三行 restriction 登记为 blocked：NF-13 / NF-14 / D12/O5-HA）。
- **本批次新增改动文件**（在本文 §3 清单基础上补）：
  | 文件 | 改动 |
  | --- | --- |
  | `docs/acceptance/m8-test-plan-matrix.md` | **追加一节**「M8 批次4 终态化代签（2026-10-13）」，正文与各「状态统计」段未改 |
  | `docs/handoff/2026-10-12-m8-batch4-complete-handoff.md` | 追加本文 §7 |
  | `docs/acceptance/m8-matrix-finalization-draft-2026-10-12.md` | 追加 §6「执行状态（2026-10-13）」，原文未改（草案转为存档） |
  | `docs/reviews/m8-batch4-signoff-review-2026-10-12.md` | 追加「裁决结果（2026-10-13，维护者已决并授权代签）」节，原文未改 |
- **`docs/acceptance/report.md` §0.5 计数未动**，归批次 6（**E-1**）按上述计数执行；`docs/plan.md` M8 行回写同样归批次 6（**E-3**）。
- **签字性质**：全部签字栏为「**agent 代签（维护者 2026-10-13 授权）**」，不是维护者亲签；**M8 里程碑仍未签**（内部版本、不签收）。
- **未执行任何 git 写操作**（无 add / commit / tag / push / branch / stash）；全部改动留工作树，由维护者切分提交。执行环境 `dev-win03ib7niepf0`。
