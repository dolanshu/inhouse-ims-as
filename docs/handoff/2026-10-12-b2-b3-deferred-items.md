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

# B2 / B3 延后项登记（requirement + ADR 起草，下个 phase 实现）

> **落盘日期：2026-10-12。状态：已登记，未起草，未实现。**
>
> **维护者 2026-10-12 决定**：B2 / B3 的 requirement 与 ADR 起草**属大工程，本轮不做**，
> **单独留 item，后续做**；**功能实现放在下个 phase，当前不做**。
>
> **本文件是这两个 item 的仓内追踪载体**（本项目无外部 issue 跟踪，仓内文档即追踪系统 ——
> 与 A4-3「独立 issue」以 [`../acceptance/2026-10-11-wave2-replay-register.md`](../acceptance/2026-10-11-wave2-replay-register.md)
> 为载体的裁决口径一致）。
>
> **本文件不签收任何 REQ，不启动任何实现，不构成对外承诺。**

---

## 0. 先说清 B2 / B3 到底处于什么状态

这两项常被误读为「还没裁决」。**不是**——**取值早已裁决完毕**，缺的是**工程落地**：

| 项 | 已裁决的取值 | 裁决出处 | 当前状态 |
|---|---|---|---|
| **B2** | O4＝默认保留 **10 天**、部署可配；D5＝**in-cluster PostgreSQL**；Redis 继续用于 runtime checkpoint | §0-A.6 **G6 / B2 + D5**（2026-10-10 裁决，2026-10-11 同步到 `plan.md` §5） | **取值已裁**，轨迹存储 / 查询 / 删除**实现未落** |
| **B3** | O5＝**站点内 N+1 + 跨站 1+1 warm standby**；D3＝**Redis primary/replica + Sentinel**（ADR-0008） | §0-A.6 **G7 / B3 + D3**（2026-10-10 裁决） | **取值已裁**，Sentinel **实现未落**；**RPO / RTO 数值仍未裁** |

**因此本 item 的内容是「把已裁的取值变成可实现的工程」，不是「再来一次裁决」。**

---

## 1. Item B2 · 呼叫轨迹保留与存储

### 1.1 要交付什么

| # | 交付物 | 说明 |
|---|---|---|
| 1 | **requirement** | 轨迹存储 / 查询 / 删除三条能力的需求条目；含保留期语义（**清理触发点**与**时间起算口径**——裁决时明确标注为「实现细节待定义」） |
| 2 | **ADR** | D5 已定为 in-cluster PostgreSQL，但「in-cluster」的部署形态（StatefulSet？已有 `deploy/compose` 的 PG 还是 chart 内新起？）、备份策略、与 ADR-0026（D12 集群内 PG/Redis）的关系，都需一条 ADR 定夺 |
| 3 | 实现（**下个 phase**） | 存储 / 查询 / 删除 + 清理触发 |

### 1.2 已知的前置事实（起草时要用）

- `docs/product/security-privacy.md` §2 / §3.1 与 `docs/operations/backup-restore.md` §1 的「待 D5 裁决」表述，
  已于 2026-10-11 按追加方式同步为「取值已裁、实现未落」（register §2 P3）。
- `security-privacy.md` §4.1 记录的「**chart 无备份 Job**」这一事实**未变** —— 备份恢复方案因此仍未闭合。
  起草 ADR 时必须处理这一点，否则 ADR 会与仓库事实冲突。
- 裁决原文写明「**实现未落**」，且「不得标为已解决」。

### 1.3 阻塞的下游（起草完成后可解锁）

- `docs/product/security-privacy.md` 的 PDPO 保留期限与存储方案（当前写不出「系统按 10 天清理」）
- `docs/product/ne-datasheet.md` 若有相关表述
- 包装交付物中任何依赖「轨迹可查询」的描述

---

## 2. Item B3 · Redis HA 与容灾

### 2.1 要交付什么

| # | 交付物 | 说明 |
|---|---|---|
| 1 | **requirement** | 容灾能力需求；含 **RPO / RTO 数值**——**裁决明确未裁此值**，requirement 阶段必须补上，否则无法验收 |
| 2 | **ADR** | D3 已选 Redis primary/replica + Sentinel（ADR-0008），但 ADR-0008 是否覆盖 **Sentinel 的具体拓扑**（几个 Sentinel、quorum、与 K8s 调度的关系）需确认；若不足，需新 ADR 或修订 |
| 3 | 实现（**下个 phase**） | Sentinel 部署与故障切换验证 |

### 2.2 已知的前置事实（起草时要用）

- D3 的**客户端接线**已于 2026-10-05 resolved（`m2-d3-sentinel-adjudication-2026-10-05.md`）；
  当前未决的**只剩 HA 拓扑**。
- 裁决明确「**不承诺机架 / AZ 级容错**」——requirement 不得写成机架级容灾。
- `docs/operations/backup-restore.md` 的 RPO / RTO 与 HA 章节，已于 2026-10-11 同步为「取值已裁、实现未落」。
- `plan.md` §5.2 D3 行与 §5.1 O5 行均带行内注记，起草时以那里为准。

### 2.3 阻塞的下游

- `docs/operations/backup-restore.md` 的 RPO / RTO 数值（当前为空）
- `docs/product/security-privacy.md` §4.1
- 任何对外材料中的可用性承诺

---

## 3. 为什么本轮不做（如实记录）

1. **属需求级工作**：按 `AGENT.md` §3，需走 requirement → ADR → HLD/LLD → 契约 → 代码+测试 → 验收项 + review record。
   requirement 与 ADR 的**起草**本身就需要先读全部相关正本（ADR-0008、ADR-0026、M2 D3 裁决、两份下游文档），
   不是一次指令可完成的。
2. **B2 与 B3 相互牵连**：轨迹存储选 in-cluster PostgreSQL，而 PG 的高可用形态又与 D12（ADR-0026）和
   B3 的容灾基线（跨站 1+1 warm standby）相关。分开起草会产生两份互相冲突的 ADR。
3. **维护者已明确**：本轮只留 item，功能下个 phase 实现。

---

## 4. 启动条件（下次开工前先确认）

- [ ] 维护者授权启动 requirement 起草
- [ ] **B3 的 RPO / RTO 数值**已有取值（否则 requirement 无处落验收标准）
- [ ] 确认 B2 的 PG 部署形态与 ADR-0026 的关系（修订还是新 ADR）
- [ ] 确认 B2 / B3 是否**合并**为一份「状态与持久化」requirement + ADR，还是分开

---

## 5. 后置到下一个 release（2026-10-12 晚些时候追加）

> **维护者 2026-10-12 决定**：B2 / B3 的 requirement 与 ADR 起草（**含 B3 的 RPO / RTO 取值**）
> **整体留到下一个 release**；本轮不启动，**以后不再单独提出**
> （与 [`2026-10-10-unfinished-assessment-and-next-plan.md`](2026-10-10-unfinished-assessment-and-next-plan.md)
> §12「已裁不做登记区」同口径：后续状态盘点一律只引指针，不逐项复述）。

- 本文 §0–§4 的全部内容**继续有效**，作为下一个 release 启动时的输入；
- §4 的四项启动条件**原样保留** —— 下一个 release 开工前先逐项确认，未确认不得启动；
- **RPO / RTO 数值的裁定一并后置** —— 它属对外可用性承诺，须维护者取值，不由 agent 代裁；
- **重启时机**：维护者在下一个 release 排期时明确；届时在本文**追加**重启记录，不改写本文。

> **去向指针（2026-10-13 追加；上方第 5 节原文一律保留不改）**：本文的后置登记统一收口于
> [`../next-release-v1.1-plan.md`](../next-release-v1.1-plan.md) —— **B2**（O4＝默认保留 10 天、部署可配，
> D5＝in-cluster PostgreSQL；轨迹存储 / 查询 / 删除实现未落）见 **§4-1**；**B3**（O5 / D3 取 Redis primary/replica + Sentinel，
> 实现未落）见 **§4-2**；**本文 §4 的四项启动条件**原样保留为该文档 **§4.3**，未确认不得启动；
> **RPO / RTO 取值**属对外可用性承诺、仍须维护者取值，登记为该文档 **§7-4**。
> 本文 §0–§4 的全部内容**继续有效**，作为下一个 release 启动时的输入；重启记录届时在该文档对应行**追加**，不改写本节。

---

**落盘日期：2026-10-12。状态：已登记，未起草，未实现。**
（关联：[`2026-10-10-unfinished-assessment-and-next-plan.md`](2026-10-10-unfinished-assessment-and-next-plan.md) §4 B2 / B3；
上游裁决：`docs/plan.md` §0 决策记录表 G6 / G7 行。
本文件不签收任何 REQ、不启动任何实现，不构成对外承诺。）
