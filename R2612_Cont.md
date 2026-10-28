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

# R2612 后续规划（不含外部硬依赖）

> **上下文**：M8 internal release 已于 2026-10-13 关闭（path C，外部硬依赖风险已书面接受），VERSION `0.2.0`，未 bump、未 tag。
> 本文档汇总 M8 之后、**不含外部硬依赖部分**（运营商 PKI / 客户 K8s / 双站点 / 外部监控输入 / X1 scrape wiring / 真实集群引流演练）的全部剩余项。
> 外部硬依赖类（`next-release-v1.1-plan.md` §2）不进本文档，启动条件 = 维护者裁决 + 外部资源到位。
> 本文档**不做启动授权**、**不做里程碑签署**、**不 git commit**。

---

## 0. 当前状态快照

| 维度 | 事实 |
|---|---|
| 里程碑 | M0→M1→M2→M3→M4a→M4b→M5→M6→M7→M7.1→**M8 exit 已签署（2026-10-13，path C）** |
| VERSION | `0.2.0`（未 bump、未 tag） |
| M8 验收矩阵终态 | pass 27 / defer 4 / blocked 9 / n-a 9 / open 0 / fail 0 |
| 工程闸门 | `make gate` ≈ 1100 passed / 2 skipped；e2e 8 passed；集成层 200 passed（PG 12.22） |
| 代码构件 | apps×2（translation / anti-fraud）、services×2（console / config-service）、testbed×2（simulators / load）、platform（workspace root 包） |
| 部署产物 | Helm chart `0.2.0`、`kubeVersion >=1.23.0-0`、alert rules 10 条、values-onprem.example |
| ADR | 0001–0027 |
| 产品定位 | 第三方 IMS AS、单租户、机房内部署、xxCarrier 内部 review 导向 |
| 文档归口 | 所有剩余项完整归口于 `docs/next-release-v1.1-plan.md`；本文档是面向 R2612 分支的**执行视角摘要** |

---

## 第一类：v1.1 新特性（每项必须完整走完 requirement → ADR → HLD/LLD → contract → code+tests → acceptance → review record 文档链）

> 排序：按交付价值 + 技术可做性 + 是否为已知 POC 基线倒退来排，排在前面的优先级更高。

### 1. Call-ID 消息追踪（REQ-F-13 / NF-7）

**是什么**：给运维一个入口，输入通话 ID，把那通电话的所有 SIP 信令（INVITE / 200 OK / BYE 等）按时间顺序拉出来看。类似邮件客户端"查看某封邮件的完整收发记录"。

**现在怎么样**：完全没有实现。POC 原型里 `observability/tracing.py` 被 triage 为"产品能力保留"，但产品版落地时遗漏了——是一个明确的功能倒退。值已裁决：默认保留 10 天、可配置，存在集群内 PostgreSQL。

**为什么要做**：ADR-0017 明确说"不做 CDR，用 Call-ID 追踪替代"。投诉溯源、反欺诈证据链、排障都要靠这个。没有它交付就缺了最基本的一条证据链。

---

### 2. 通话中途业务触发（re-INVITE / UPDATE 处理，REQ-F-9）

**是什么**：通话已接通后，网络发来"中途请求"——加媒体、切编码、转给别人。AS 要识别、查规则、做决策。类似一通电话突然被要求"三方通话"。

**现在怎么样**：BYE（挂机）这一种中途请求已通，re-INVITE / UPDATE / PRACK 三种完全没实现。

**为什么要做**：运营商 IMS 的常规能力，没有它业务系统没法在通话中途挂逻辑（余额提醒、VIP 坐席、加密协商等）。

---

### 3. trunk 侧 Record-Route 头转发（REQ-F-5）

**是什么**：SIP Record-Route 头让后续消息知道回程路径。下游网元回复里带了这个头，我们要原样透传给上一跳。

**现在怎么样**：我们消费入腿 Route 头做路由决策，但下游回复里的 Record-Route 没往上游转。baseline 抓包里根本没有 Record-Route 头，所以这个问题被推迟——先重抓 baseline 再修。

**为什么要做**：运营商网络多层 AS 串联时，不转发会导致后续消息走错路。协议合规性缺陷。

---

### 4. CANCEL 竞态修复（REQ-F-11）

**是什么**：INVITE 刚发出去，上游紧接着发来 CANCEL。CANCEL 可能在任何时刻到达。目前只覆盖了"下游已经回复 100 Trying 之后才来的 CANCEL"这一种情况，另一种（任何下游回复都还没来就来 CANCEL）有 bug。

**现在怎么样**：分支①通了，分支②需要在 native C++ `runtime_module.cxx` L1143-1162 加 guard。

**为什么要做**：理论上的竞态漏洞——一旦出现就是"我们发了 CANCEL 但下游没收到，电话还是振铃了"这种诡异现象。

---

### 5. caller-ID + 正则规则匹配（REQ-F-12 四维 UI）

**是什么**：目前控制台规则只能按"被叫号码"和"被叫前缀"匹配。要加的能力：按主叫号码匹配、按主叫或被叫的正则表达式匹配。UI 上做成两个下拉框（选主叫/被叫）+ 输入框（填号码或正则）。

**现在怎么样**：M4 里程碑明确只做了 callee + prefix，caller-ID 和 regex 推到 v1.1。

**为什么要做**：真实运营里同一个被叫号段可能配不同规则（主叫 VIP 就接、主叫黑名单就拒），只靠 callee+prefix 不够灵活。

---

### 6. 零丢失滚动升级（NF-4 增强）

**是什么**：`kubectl rollout restart` 时正在通话的 100 通电话一个都不丢。

**现在怎么样**：当前版本**已经接受了有损失**——实测约 4% 在途通话掉了。原因是 reSIProcate 对话状态存在进程内存里，没有序列化/反序列化 API，老进程挂了新进程接不上。

**为什么要做**：增强特性，不阻塞当前版本。候选方向：进程级 drain 时间更长、S-SBC 透明桥 + Redis 存对话状态、实例 stick 同一 Pod、或维护窗口约定。排在前面几项之后。

---

### 7. CANCEL 三分支 real-stack parity + native JSON callback（REQ-F-8）

**是什么**：CANCEL 有三个处理分支，目前只在 testbed harness（模拟环境）里验证过，没在真实 reSIProcate 栈上逐个对照。native C++ 和 Python 层目前用 log 文本解析回传结果，要改成 JSON 结构化回调。

**现在怎么样**：完整三分支 real-stack comparison 还没跑；native→Python 还是 log 文本。

**为什么要做**：harness 验证≠真实栈验证。之前有过 harness 全绿但实际有 bug 的教训（`advertised=` 正则 bug）。

---

## 第二类：值已裁决、实现可立即落地（最快出代码）

> 这些项的值已经裁决好、阻塞外部条件已经去掉，差的就是写代码 / 跑测量 / 起草文档。

### 8. A3 Phase D：S5–S11 原生 SIP 场景补全

**是什么**：已有 S1–S4 四个 baseline 场景，S5–S11 七个场景（两腿归一化 / SDP 语料库 / 规则优先级 / 非 2xx 透传 / BYE 路由 / Record-Route 抓包 / CANCEL 竞态）还没实现对应 case。排期已定：P1 S5 → P2 S7a → P3 S6 → P4 S10 → P5 S9 → P6 S11。S8（Record-Route）单独阻塞，因为 baseline 里缺这两个头。

**现在怎么样**：排期表已写，一条 case 都没写。

**为什么要做**：补齐协议层测试覆盖，是 REQ-F-1 完整 14 条 parity 检查的一部分。

---

### 9. HPA 阈值测量批次

**是什么**：Helm chart 里 HPA 的 CPU/内存阈值目前留空，需要跑一次测量，把"单 Pod 跑满 CPS 1280 时 CPU 用了多少、内存用了多少"测出来，填进 `values-onprem.example.yaml`。

**现在怎么样**：CPS 1280 饱和点已测到（2026-10-12），但那次没采 per-pod 资源数据，还不能填阈值。

**为什么要做**：HPA 空着就没法自动伸缩。把已裁决好的值落地。

---

### 10. M5D-1…M5D-6：六个已知工程债

> 每项都是一次 review 揪出来的"知道不对但先放着"，M5 赶里程碑推迟了，这次一起清。

| # | 问题 | 人话 |
|---|---|---|
| M5D-1 | 6 条 alert rule 引用不存在的 metrics，有个 `clamp_min` 算术写错 | 告警规则里有死代码，阈值写的 `> 0` 逻辑不对 |
| M5D-2 | scale-down guard 参数读进来只打 log，不参与决策 | 缩容保护功能是空壳 |
| M5D-3 | OTLP export 是 NoOp sink，发进去直接丢 | 遥测数据导出是假的 |
| M5D-4 | NetworkPolicy 只有入方向、源标签太宽 | 网络策略只管了入、出方向没管、源范围太松 |
| M5D-5 | Pod 没设 resources（BestEffort）、没设 startupProbe | AS Pod 资源没设上下限、启动时没健康检查 |
| M5D-6 | 跨站点切换演练没做 | ADR-0008 承诺的跨站点容灾验证没跑 |

**为什么要做**：都是"知道不对但先放着"的东西，一次改干净。

---

### 11. PG15 AmbiguousFunction 修复

**是什么**：config-service 集成测试在 PG 15.18 上有 SQL 报错，原因是 PG 14+ 把 `\|\|`（字符串拼接）操作符的类型推断改了。

**现在怎么样**：失败已诚实记录成 `FAIL-` 证据，没改任何代码。当前用 PG 12.22 跑是绿的，但 PG 12 已 EOL。

**为什么要做**：跟上 PG 新版本。改动很小，SQL 里加个显式 CAST。

---

### 12. B2 / B3 requirement + ADR 起草

**是什么**：B2（call trace 保留 + 存储）和 B3（Redis HA + 灾备）的值已经裁决好（O4=10 天可配置、O5=N+1 本地 + 1+1 异地、D5=集群内 PG、D3=Redis primary/replica + Sentinel），但 requirement 文档和 ADR 还没写。

**现在怎么样**：值都有了，起草 requirement → ADR → HLD/LLD 还没启动。四个启动条件可逐条确认（维护者授权、RPO/RTO 值、确认拓扑关系、是否合并成一个 requirement）。

**为什么要做**：这两个是 call trace 功能和生产 HA 的上游设计文档，不写就没法往下推进。

---

## 第三类：文档和卫生清理（不改产品代码，风险最低）

### 13. 五份 stale 文档同步

**是什么**：有五份文档里还写着旧值（`Chart.yaml` 还是 `0.0.0-skeleton`、O1 capacity 还写着"未裁决"），而实际 chart 已经 sync 到 `0.2.0`、O1 内部值已经裁决了。

**目标文件**：
- `docs/delivery/airgap-package.md`
- `docs/delivery/install-guide.md`
- `docs/operations/rollback-playbook.md`
- `docs/product/ne-datasheet.md`
- `docs/product/version-lifecycle.md`

**怎么做**：遵循"保留原文 + 追加 annotation"规则，不删旧文字，在旧文字旁边加括号注释"本值已变更为 XX，见 XXX"。

---

### 14. `defer` status word 确认

**是什么**：M8 batch 4 验收矩阵里新引入了状态词 `defer`（"本版本不做、已分配到 v1.1"），和 `blocked`（外部环境缺失）、`n-a`（永远不做）、`pass`（已验收）并列。这个词还没经过维护者正式确认是否长期保留。

**为什么要做**：长期保留的话后面的验收文档都要用；不保留就得换别的表述方式。

---

### 15. Performance 层 gate 终态二选一

**是什么**：`make gate` 目前只跑 unit/contract（≈1100 测试），不跑 `performance` 层。M8 batch 5 记录了二选一：① 把 performance 变成 blocking layer（但性能测试不稳定、容易 flaky）；② 维护者书面接受"本版本不把 performance 放进 gate"。Path C（2026-10-13）只接受了外部硬依赖风险，没有单独裁决这一条。

**为什么要做**：不裁决就一直悬着，后面每个 PR 都会被问"为什么不跑 performance"。

---

### 16. 维护者签名 + 填值（必须维护者自己来）

| # | 事项 | 人话 |
|---|---|---|
| ① | M8 exit 签名块换成维护者自己的 | 目前是"agent 授权代理签名"，不是维护者自己签的 |
| ② | M1 exit 签名 | 同① |
| ③ | M6 milestone sign-off | "工程完成"≠"里程碑签署"，还差维护者一句同意 |
| ④ | RPO / RTO 值 | 外部可用性承诺，agent 不能编 |
| ⑤ | O1 对外 capacity 值 | CPS 1280 是内部目标，对外承诺多少得维护者定 |
| ⑥ | A4-4 gate 配置变更授权 | e2e 要不要放回 `make test`、kind e2e 要不要进 PR 必过，策略方向已有但执行授权要维护者给 |

---

### 17. 维护者还要裁决的五个二选一

| # | 问题 | A 选项 | B 选项 |
|---|---|---|---|
| ⑦ | config-service 单 PG 连接断线不自动重连要不要立项 | 立项加自动重连 | 接受现状（重启恢复） |
| ⑧ | whitelist 地址/证书 OR 语义要不要收紧成 AND | 收紧（地址+证书都匹配才放行） | 接受 OR（只要地址命中就放行） |
| ⑨ | whitelist 变更要不要纳入审批流程 | 纳入（走 ChangeOrder） | 不改代码，修正验收文档描述 |
| ⑩ | root `README.md` 环境变量表 0/16 覆盖率要不要补 | 补全表格 | 留给后面 |
| ⑪ | 未提交文件 commit 切分 + tag 时机 | 维护者自己决定 | 维护者自己决定 |

---

### 18. REQ-F-1 的 14 条 checkbox 勾上

**是什么**：`docs/acceptance/test-plan.md` 里 REQ-F-1（基本通话）下面有 14 个 header-by-header parity 检查项，每个前面有 `- [ ]`。目前 Wave 1 + Wave 2 覆盖了自动化子集，没勾任何一个 checkbox。

**为什么要做**：勾 checkbox 本身是形式，但代表"走完了从测试到正式验收的流程"。如果还剩没实现的项，就要诚实写进去。

---

## 建议的 R2612 启动顺序

```
Phase 0 — 维护者一次性把 Phase 16 + Phase 17 的 11 件事全部签完 / 填完
          ↓
Phase 1 — 文档卫生批次（Phase 13 + 14 + 15 + 18）
          不碰产品代码，一个 writing subagent 搞定
          ↓
Phase 2 — 值已裁决、实现可落地（Phase 8 + 9 + 10 + 11 + 12）
          Phase 12 是文档起草，其他四个是代码
          ↓
Phase 3 — v1.1 新特性逐个立项（Phase 1 → 2 → 3 → 4 → 5 → 6 → 7）
          每个都要走 requirement → ADR → design → contract → code → acceptance 完整文档链
```

---

## 与 `next-release-v1.1-plan.md` 的关系

- `next-release-v1.1-plan.md` 是**归口注册载体**：所有剩余项都在那里登记了来源和去向，是权威索引。
- 本文档是**R2612 分支的执行视角摘要**：把注册表里"我们自己能动手"的项抽出来、用人话解释清楚、排好优先级。
- 两者不冲突、不替代。启动任何一项前，`next-release-v1.1-plan.md` 里对应的行是权威登记，本文档只帮助理解。

---

Written to disk: 2026-10-28. Status: planning document only, not signed, not committed.
