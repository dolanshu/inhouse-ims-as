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

# `docs/plan.md` M8 行回写草案（M8 批次 6 / E-3，2026-10-12）

## 0. 性质

本文是回写**草案**；`docs/plan.md` **一字未改**。本草案须经维护者确认后，方可由维护者或授权 agent 执行。本批次未执行任何 git 写操作。执行环境：`dev-win03ib7niepf0`。

## 1. 建议一：§0「当前进行中的步骤」单元格

建议在该单元格末尾追加以下完整文本，不改既有内容：

> **2026-10-13 追加**：M8 内部版收尾已由批次 1–6 完成（function 完整 + 模拟器证据 + 可重复构建工件；矩阵终态 pass 27 / defer 4 / blocked 9 / n-a 9 / open 0 / fail 0，口径均为「工程证据接受」）；**M8 退出签字仍未签**，仍排在外部硬依赖（S-2 / S-3、NF-1、ADR-0008 演练、D12/O5-HA）闭环之后。内部版收尾评审见 [`../reviews/m8-internal-release-exit-review-2026-10-12.md`](../reviews/m8-internal-release-exit-review-2026-10-12.md)。

## 2. 建议二：§0「产品决策记录」表

建议新增一行（追加，不改既有行）：

| 日期 | 决策 | 方向 | 依据 |
|---|---|---|---|
| 2026-10-13 | **M8 内部版收尾完成（不是 M8 退出签字）** | 批次 1–6 全部落地（发布与打包 / SIP 对拍 / kind-sim 证据 / 签收与评审 / 性能与容量 / 文档与报告）；矩阵终态 pass 27 / defer 4 / blocked 9 / n-a 9 / open 0 / fail 0（口径 = 工程证据接受）；VERSION 维持 `0.2.0` 不 bump、CHANGELOG 在 `[0.2.0]` 节内追加 internal build 条目、镜像 tag `as-platform:0.2.0-internal-<date>`、chart 不同步；**M8 不签**。**不得据本行推出**：M8 已签收 / 已发版 / O1 对外值已填 | [`report.md`](report.md) §0.10（批次 6 / E-1）；[`../reviews/m8-exit-review-2026-10-06.md`](../reviews/m8-exit-review-2026-10-06.md) §3.2（批次 6 / E-5）；[`../reviews/m8-internal-release-exit-review-2026-10-12.md`](../reviews/m8-internal-release-exit-review-2026-10-12.md)；`m8-test-plan-matrix.md`「M8 批次4 终态化代签（2026-10-13）」节；`(已验证, docs/acceptance/artifacts/m5/2026-10-12/PASS-e6-packaging-recheck-2026-10-12.txt, 2026-10-12)` |

## 3. 建议三：§4 里程碑表 M8 行「状态」列

| 原文 | 建议值 |
|---|---|
| **RC 产物就绪；退出签字仍搁置（2026-10-07）**。M7.1 已工程关门。仍待 Close 前限制解除后再 revisit …。原状态：RC就绪、待维护者退出签字（2026-10-06） | **内部版收尾完成（2026-10-13）**：function 完整 + 模拟器证据 + 可重复构建工件；矩阵终态 **pass 27 / defer 4 / blocked 9 / n-a 9 / open 0 / fail 0**（签字口径一律「工程证据接受」，非 REQ 级验收）。**M8 退出签字仍未签** —— 排在外部硬依赖（S-2 / S-3、NF-1、ADR-0008 演练、D12/O5-HA）闭环之后。**原状态：RC 产物就绪；退出签字仍搁置（2026-10-07）** |

依据：`(已验证, docs/acceptance/m8-test-plan-matrix.md「M8 批次4 终态化代签（2026-10-13）」节, 2026-10-13)`；`(已验证, docs/acceptance/artifacts/m5/2026-10-12/PASS-e6-packaging-recheck-2026-10-12.txt, 2026-10-12)`；内部版收尾评审 [`../reviews/m8-internal-release-exit-review-2026-10-12.md`](../reviews/m8-internal-release-exit-review-2026-10-12.md)。

## 4. 边界

1. 本草案不改 `docs/plan.md` 任何一行。
2. M8 行最终表述由维护者确认。
3. 本草案不签 M8，不签任何 REQ，也不宣称 M8 全绿。
4. 内部版本不是发行版；未 tag，O1 对外承诺值仍不填。
5. 本批次未执行任何 git 写操作；commit 拆分由维护者决定。
6. 执行环境固定为 `dev-win03ib7niepf0`。

> **2026-10-13 状态**：本草案已由维护者采纳并授权执行，M8 行按**路径 C** 调整（M8 退出签字 + 书面接受外部硬依赖风险），回写已落到 `docs/plan.md`。本草案保留为档案。
