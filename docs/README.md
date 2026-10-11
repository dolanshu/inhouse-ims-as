# 文档导航（Documentation map）

按读者角色阅读。全部是纯文本 —— Mermaid 或 ASCII 图，绝不放无法 diff 的渲染图片。

> `docs/` 下新增了三个面向不同读者的目录：**评审** [`product/`](#面向评审产品与评审文档)、**运维** [`operations/`](#运维与值守)、**交付** [`delivery/`](#交付形态)。它们都来自同一份包装计划：[`product-packaging-plan.md`](product-packaging-plan.md)。

## 决定要做什么

| 文档 | 是什么 |
|---|---|
| [`architecture/README.md`](architecture/README.md) | **架构入口。** 文档地图与优先级（**规范文档 = `hld.md` / `lld.md`**）、交付边界、证据分级、当前已知待确认项 |
| [`architecture/新系统整体架构.md`](architecture/新系统整体架构.md) | **设计基线。** 每一项已确认决策、其理由、未决清单与风险登记 |
| [`architecture/adr/`](architecture/adr/) | 决策记录；先看它的 README 里的注册表 |
| [`plan.md`](plan.md) | 交付计划：里程碑、顺序、退出标准 |
| [`environments.md`](environments.md) | **环境登记表。** 长期事实登记：每台机器的名字、hostname、具备/缺失工具、已产出的证据。引用环境必须用表中的名字。**数据由 `tools/env-probe.sh` 现场探测生成，不手工维护**（见「本机环境与工具」） |
| [`product-packaging-plan.md`](product-packaging-plan.md) | **产品化包装计划。** 四批交付物、`product/`·`operations/`·`delivery/` 三个新目录的由来与执行顺序 |
| [`migration/triage.md`](migration/triage.md) | 在采纳任何东西之前，POC 代码如何被甄别 |

## 构建它

| 文档 | 是什么 |
|---|---|
| [`../AGENT.md`](../AGENT.md) | **写代码之前先读。** 协作守则、分层、TDD 政策、门禁、git 规则 |
| [`../CONTRIBUTING.md`](../CONTRIBUTING.md) | 环境搭建、本地门禁、commit 与评审约定 |
| [`../README.md`](../README.md) | 定位、仓库导览、快速开始 |

## 面向评审：产品与评审文档

| 文档 | 是什么 |
|---|---|
| [`product/one-pager.md`](product/one-pager.md) | **产品一页纸。** 价值主张、架构大图、KPI 定义、三步部署 |
| [`product/ne-datasheet.md`](product/ne-datasheet.md) | **网元档案。** 接口清单、KPI 与告警、依赖关系、资源规格；容量数值受 O1 阻塞 |
| [`product/compliance-matrix.md`](product/compliance-matrix.md) | 3GPP / GSMA / RFC 规范符合性矩阵（Sh 与计费标 N/A 并保留理由） |
| [`product/responsibility-matrix.md`](product/responsibility-matrix.md) | 责任边界矩阵 RACI：AS 与 S-CSCF / HSS / 计费域 / 网管 / 安全各域 |
| [`product/version-lifecycle.md`](product/version-lifecycle.md) | 版本生命周期与 EOL 策略（REQ-NF-16 / ADR-0027） |
| [`product/security-privacy.md`](product/security-privacy.md) | 安全与隐私合规（PDPO）；保留期限待 O4、存储选型待 D5 |

## 运维与值守

| 文档 | 是什么 |
|---|---|
| [`operations/README.md`](operations/README.md) | 运维分册总览：读者分层、归集映射、尚未交付清单 |
| [`operations/runbook-l1.md`](operations/runbook-l1.md) | L1 运维手册：每日巡检、告警首响应、常见操作（NOC） |
| [`operations/runbook-l2.md`](operations/runbook-l2.md) | L2 运维手册：深度排障、信令与日志取证（二线） |
| [`operations/fault-demarcation.md`](operations/fault-demarcation.md) | 故障定界手册：AS / S-CSCF / HSS / 计费域四方定界 |
| [`operations/rollback-playbook.md`](operations/rollback-playbook.md) | 业务摘流 / 回退 + iFC 侧配合 |
| [`operations/backup-restore.md`](operations/backup-restore.md) | 备份恢复方案 + 演练记录模板（依赖真实集群环境） |
| [`operations/alert-response-matrix.md`](operations/alert-response-matrix.md) | 告警-动作对照表：级别、触发条件、处理动作、升级路径 |
| [`operations/grafana-dashboards/README.md`](operations/grafana-dashboards/README.md) | Grafana 看板模板（`overview.json` / `sip-signaling.json`）及其可用性前置条件 |

> `docs/acceptance/*-runbook.md` 是历史原件与审计追溯源，**不删除、不移动、不改写**；`operations/` 只做索引 + 链接 + 面向值班的操作正文。

> **评审 / 执行记录入口**：本轮产品化包装（`product/`、`operations/`、`delivery/` 三个目录）的**执行记录**见 [`reviews/product-packaging-execution-record-2026-10-10.md`](reviews/product-packaging-execution-record-2026-10-10.md)。⚠️ 该文件是**执行记录，不是维护者签字的 review record** —— 各分册要求的独立 review record（`AGENT.md` §3.3）仍待维护者评审；包装前的评审意见见 [`reviews/product-packaging-plan-review-2026-10-09.md`](reviews/product-packaging-plan-review-2026-10-09.md)。

## 交付形态

| 文档 | 是什么 |
|---|---|
| [`delivery/README.md`](delivery/README.md) | 交付目录总览：三步交付流程、前置条件、与权威文档的边界 |
| [`delivery/install-guide.md`](delivery/install-guide.md) | **安装部署指南。** 交付清单、镜像获取与同步、`helm install` 命令序列（Helm 参数以 [`../deploy/helm/README.md`](../deploy/helm/README.md) 为权威） |
| [`delivery/airgap-package.md`](delivery/airgap-package.md) | 离线安装包（air-gapped）制作与使用：联网侧、离线侧、校验和与供应链 |
| [`delivery/preflight.sh`](delivery/preflight.sh) | 部署前环境校验脚本：K8s / 资源 / 依赖服务 / Helm / RBAC / chart 渲染守卫 |

## 运行它

| 文档 | 是什么 |
|---|---|
| `acceptance/` | 逐条带证据的验收标准与历史 runbook 原件 —— 仍是历史证据的所在地 |
| [`../deploy/helm/README.md`](../deploy/helm/README.md) | **Helm chart 参数与渲染行为的唯一权威**（交付形态说明） |

## 本机环境与工具

> **环境信息不由人工维护。** 下面的脚本负责探测与安装，登记表 [`environments.md`](environments.md)
> 的数据行来自它们的输出。项目会部署到不同电脑，**环境差异是常态** —— 不要以任何一台机器的
> 工具清单去推断项目能力，也不要据「某台机器缺 X」改文档口径。

| 脚本 / 文档 | 是什么 |
|---|---|
| [`../tools/env-probe.sh`](../tools/env-probe.sh) | **环境探测（只读）。** 探测 hostname / OS / 架构 与 docker / uv / python3.10 / helm / kubectl / kind / promtool / make / git，区分「✅ 具备 / ❌ 缺失 / ⚠ 装了但不可用」三态。`--markdown` 输出可直接粘进 [`environments.md`](environments.md) 的表格行，`--json` 供机器读。不安装任何东西、不改系统状态、不需要 root，缺工具仍 exit 0 |
| [`../tools/bootstrap-infra.sh`](../tools/bootstrap-infra.sh) | **infra 工具安装（无 root、幂等）。** 把 helm / kubectl / kind / promtool 解压到 `tools/bin/`，版本锁定在 [`../tools/VERSIONS`](../tools/VERSIONS)；支持 `--dry-run`、`--only <tool>`、`--force`，装完自动调用 `env-probe.sh` 验证。**需要 root 的路径一律显式报错，绝不偷偷 sudo** |
| [`handoff/2026-10-11-local-infra-bootstrap-plan.md`](handoff/2026-10-11-local-infra-bootstrap-plan.md) | **本机补齐四件工具的执行计划**（前置条件核查、安装清单、版本固定、可证伪的验证步骤、回退、停止线）。执行者请从该文档开始，不要从本文开始 |

## 参考

| 文档 | 是什么 |
|---|---|
| `glossary.md` | IMS / SIP 术语表 —— **尚未创建**，随首个代码里程碑落地 |
| `specs/` | 规范性参考（RFC 3261、RFC 4566、RFC 8688、TS 24.229）与消息样例 —— **尚未创建** |
