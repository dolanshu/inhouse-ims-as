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

# ADR 注册表（ADR register）

`3rdparty-as` 的架构决策记录（architecture decision records）。它们记录的设计是
[`../新系统整体架构.md`](../新系统整体架构.md)；下表把该文档 §0 账本中的每一项已确认决策，映射到
承载其背景、后果与已接受缺口的 ADR。

**状态图例** —— `skeleton`：决策已确认但 ADR 还没写；`draft`：写了，未评审；
`accepted`：评审过且有约束力；`superseded-in-part`：部分前提被新 ADR 推翻，框架仍有效。

ADR 与它所授权的改动**一起**写，不事后、不最后批量补。没有 ADR 的决策，是要被重新争论的决策。

## 注册表

| ADR | 决策 | §0 | 状态 |
|---|---|---|---|
| [0000](0000-adr-template.md) | 下面每个 ADR 使用的模板 | — | accepted |
| [0001](0001-monorepo-uv-workspace.md) | 单一 monorepo + uv workspace；POC 与 `as_platform` 并入 | 3 | accepted ✓ |
| [0002](0002-per-usecase-process-state-redis.md) | 运行时模型：一个用例一个进程，状态外置到 Redis | 2 | accepted ✓ |
| [0003](0003-s-sbc-transparent-bridge.md) | 单一 ISC 接入语义 —— S-SBC 是透明桥接，不是第二种业务语义 | 10 | accepted ✓ |
| [0004](0004-media-seam.md) | 不做媒体；保留一个媒体 seam 并写明触发条件 | 11 | accepted ✓ |
| [0005](0005-observability-otel.md) | OTel 三信号，后端中立，导出绝不能阻塞呼叫路径；呼叫轨迹保留独立查询通道 | 12 | accepted ✓ |
| [0006](0006-config-governance.md) | 配置治理：PostgreSQL 版本库 + 变更单状态机，而非 GitOps | 13 | accepted ✓ |
| [0007](0007-data-plane-split.md) | 数据面拆分：Redis 存运行态，PostgreSQL 存治理态 | 14 | accepted ✓ |
| [0008](0008-redundancy.md) | 冗余：站点内 N+1 零单点；跨站点 1+1 温备，非双活 | 7 | accepted ✓ |
| [0009](0009-issu-draining.md) | ISSU 是 draining，不是在途状态迁移 | §6.2 | accepted ✓ |
| [0010](0010-autoscaling-hpa-downscale-guard.md) | 扩缩容：自定义指标 HPA + 缩容保护控制器 | 15 | accepted ✓ |
| 0011 | ~~SIP 栈：双栈，`sippy` 保生产，`go-b2bua` 试点~~ **栈前提被 ADR-0019 推翻**：sippy 退出生产栈；双栈并行框架仍有效 | 8 | superseded-in-part |
| [0012](0012-cross-implementation-parity.md) | 语言无关契约 + 跨实现对拍作为转正门槛 | 9 | accepted ✓ |
| [0013](0013-helm-only-production.md) | Helm 是唯一生产形态；compose 仅作开发环境 | 6 | accepted ✓ |
| [0014](0014-three-layer-testbed.md) | 三层 testbed；真实 socket 压测；不是 v1 交付物（**REQ:** [REQ-NF-15](../../requirements/req-nf-15-testbed-performance.md)） | 16 | accepted ✓ |
| [0015](0015-engineering-discipline.md) | 研发模式：分层 TDD、ADR 制度化、四层测试门禁 | 17 | accepted ✓ |
| [0016](0016-in-boundary-security.md) | 边界内安全：对端白名单、端到端 TLS、控制台鉴权、全量审计。不做 LI、不做计费 | 18 | accepted ✓ |
| [0017](0017-no-cdr.md) | 不做 CDR：不采集、不投递、不归档 —— 由呼叫轨迹替代 | 4 | accepted ✓ |
| [0018](0018-release-versioning.md) | 一个产品 release 版本，独立的组件接口版本 | §11.3 | accepted ✓ |
| [0019](0019-sip-stack-selection.md) | 生产 SIP 协议栈选型（推翻 0011 的栈前提；选定 reSIProcate；go-b2bua / libre 为备选；rsipstack 因 Rust 不在团队技术栈内被否决） | 8 | **accepted** |
| [0020](0020-feature-capability-gating.md) | Feature 能力门控：分层（部署级总开关 + 运行态细粒度覆盖），复用配置治理变更链路 | 19 | accepted ✓ |
| [0021](0021-runtime-override-granularity.md) | 运行态覆盖的判定粒度与 schema：号段 + 稳定哈希百分比，判定幂等（裁决未决项 D7） | — | accepted ✓ |
| [0022](0022-resiprocate-b2bua-control.md) | reSIProcate DUM 协议机制之上的产品 `CallController`；语言桥接与状态恢复仍为阻塞项 | 8 | **accepted**（2026-10-05 修正案；D10/REQ-NF-1 仍 open） |
| [0023](0023-redis-call-state-checkpoint.md) | 呼叫恢复方向：Redis 应用层必要状态 checkpoint；不序列化完整 DUM / `SipStack`（D10 仍未通过） | 2 | proposed |
| [0024](0024-console-password-sessions.md) | 控制台角色 + 密码认证与可撤销会话；M4b-6a/6b 工程切片；2026-10-03 维护者签核 accepted | 18 | accepted ✓ |
| [0025](0025-managed-rule-runtime-bundle.md) | 管理面 `ManagedRule` → 内部 API `ConfigBundle`/`RuleDTO` 无损编译契约（v1：被叫 + 前缀子集） | 13 | draft |
| [0026](0026-in-cluster-state-stores-proposal.md) | 集群内专用 PG/Redis（非 IMS）；单 chart 合并交付；部分修订 ADR-0013 state 渲染 | 14 / D12 | accepted ✓ |
| [0027](0027-version-lifecycle-and-eol.md) | 版本生命周期与 EOL 策略：minor 版本支持 ≥ 12 个月，EOL 提前 6 个月通知，不定义 LTS | — | accepted ✓ |

> **注记（2026-10-11，状态漂移修正）**：上表原把 **0023** 记为 `draft`，但
> [0023](0023-redis-call-state-checkpoint.md) 正文写 `Status: proposed` —— 注册表与正文不一致。
> **以正文为准**，本次只把注册表这一处改为 `proposed`，**未改动 ADR 正文、未改动任何其它注册项**。
> 0025 的 `draft` 与其正文一致，本次不动。
> 依据：[`../../handoff/2026-10-11-open-adjudication-register.md`](../../handoff/2026-10-11-open-adjudication-register.md)
> §1 S1 表「注册表与正文漂移」行。**本注记已落盘，待维护者评审。**

> **第二次全量复核（2026-10-11，S1 第二批）**：逐个打开 **0001–0027**（0000 模板除外）正文核对状态行，
> 结论：**25 个英文 `- **Status**:` 行与 0011 / 0019 两个中文「- **状态**：」行，取值与上方注册表全部一致**
> （0023=proposed、0025=draft、0011=superseded-in-part，其余 accepted；0024 行尾维护者签核注记不改变 accepted 取值）。
> **0011 ↔ 0019 双向可追溯**：[0011](0011-sip-stack-dual-path.md) 正文第 4 行写
> 「superseded-in-part by ADR-0019」，[0019](0019-sip-stack-selection.md) 正文第 7 行写
> 「取代 ADR-0011 确立的『生产栈 = sippy』前提」。
> **链接核查**：对 `docs/**` 内全部指向 `adr/00NN-*.md` 的 Markdown 链接做相对路径解析（共 206 条），
> **205 条有效、无 ADR-0028 及以上的越界引用**；发现 **1 条既有断链**：
> [`../../acceptance/m5-engineering-closure-2026-10-04.md`](../../acceptance/m5-engineering-closure-2026-10-04.md)
> 第 43 行链接写作 `architecture/adr/0026-in-cluster-state-stores-proposal.md`，
> 自 `docs/acceptance/` 解析应为 `../architecture/adr/...`（缺少 `../` 前缀）。
> 该文件是 2026-10-04 历史关门文档，按保史约定且不在本批授权改动路径内，**本次不修复、不删改其原文**，
> 仅在此登记，待维护者评审决定（修正方式：把该链接改为 `../architecture/adr/0026-in-cluster-state-stores-proposal.md`）。
> 本次复核**未改动任何 ADR 正文、未改动上方注册表表格**。**本注记已落盘，待维护者评审。**

## 规则

- **编号只追加。** 被取代的 ADR 保留编号并标为被新 ADR 取代；编号绝不重用或重排。
- **一个 ADR 一个决策。** "架构"不是决策。
- **ADR 必须写明它接受了什么。** 它明知故犯的缺口是记录的一部分；没有 consequences 节的 ADR 是宣传。
- **代码指向它的 ADR。** 一行不显而易见的代码带 `# See ADR-00NN`，审稿人能从代码一步走到理由。
- **推翻一个决策** 意味着写一个新的 ADR，并在同一次改动里更新
  [`../新系统整体架构.md`](../新系统整体架构.md)。

## 与 POC ADR 的关系

POC 在 `3rtparty_AS_POC/docs/architecture/adr/` 里带了 ADR-0001 … ADR-0016。它们**不**导入。
它们记录的是一个概念验证 —— 一个有着不同非目标的不同系统 —— 的决策。某条 POC 决策存活进产品时，
要在这里对着产品约束重新论证，POC 原文作为背景引用。没存活的，就干脆缺席，迁移甄别
（[`../../migration/triage.md`](../../migration/triage.md)）记录原因。
