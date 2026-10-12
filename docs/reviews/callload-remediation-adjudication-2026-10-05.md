# callload 评审修复 — 裁决记录（2026-10-05）

> 输入：[`callload-m2-m6-m7-demo-branch-review-2026-10-05.md`](callload-m2-m6-m7-demo-branch-review-2026-10-05.md)  
> 计划：[`../handoff/2026-10-05-callload-review-response-plan.md`](../handoff/2026-10-05-callload-review-response-plan.md)  
> 验证：本机 `make gate`（964 passed, 2 skipped）；native 集成需 `make m2-platform-resip-build` + `make m2-platform-resip`。

| ID | 状态 | 证据 |
|----|------|------|
| F1 | 已修复 | `bind_address`/`advertised_address` 贯穿 C++ + `transport_env.py` |
| F7 | 已修复 | `AS_TLS_*` / `AS_PEER_*` + `SipStackService.from_env` |
| F10 | 已修复（内容） | 故事 C 话术 + `pre-m8-demo-review-plan.md` F10 对账段 |
| F9 | 部分修复 | `native_extensions.py` + 本地 `make m2-platform-resip-build`；**阻塞目标尚未成为必跑门禁** |
| F4 | 已修复 | `map_outbound_failure_to_inbound_status` + C++ `mapUpstreamFailureStatus` |
| F3 | 已修复（FORWARD 路径） | `buildUacLegDict` + `sip_stack_service` `uac_leg` |
| F2 | 已修复 | recovery BYE Contact + `Route` 回放 |
| F5 | 已修复 | fingerprint map 2048 上限淘汰 |
| F6 | 部分修复 | connection 注册上限 + dialog 终止注销；无 native transport close 回调 |
| F8 | 未闭合 | C++ 仍以 cout/cerr 为主；M8 前需 JSON 回调或宏契约 |
| F11 | 维护者 | 不纳入 agent 队列 |
| F12–F18 | 已修复 | 见各条目 CHANGELOG 0.2.0 |

**仍不构成**：M2/M6/M7 里程碑退出、REQ 全绿、客户 NF-1 正式签收。

---

## 合入 master（2026-10-06）

| 项 | 状态 |
|----|------|
| 工程修复（上表） | 已记录；F8 开放、F6 部分 |
| F9 阻塞门禁 | **未生效** — blocking 目标（`m2-native-smoke` / `m2-platform-resip`）尚未纳入必跑门禁 |
| 维护者 merge 清单 | [`../handoff/2026-10-06-callload-merge-to-master.md`](../handoff/2026-10-06-callload-merge-to-master.md) |
| 合入 master @ SHA | **`139d299`**（2026-10-06；squash） |

---

## 代签补记（2026-10-12；N2 第 3 项「须同步」之一）

> **授权来源**：维护者 **2026-10-12 明确授权由 agent 代签** M8 的 N2 九项书面裁决。
> N2 第 3 项（F8）的「须同步」列指向本文件的 **F6 行**，此处补记正式化结果。
> **本补记不是维护者亲签**；代签总记录见
> [`../handoff/2026-10-12-m8-n2-countersign-record.md`](../handoff/2026-10-12-m8-n2-countersign-record.md)。

**上表 F6 行的状态更新**：由「部分修复」**补充**为「**部分修复 + documented limitation 已接受**」。
签字：**agent 代签（维护者 2026-10-12 授权）**。

**依据（不新造结论）**：N2 第 4 项原文 —— F6 接受 documented limitation
（长连接无 dialog 终止时只靠 2048 指纹 LRU 与 4096 连接上限）；正式化记录见
[`m8-phase-a-f6-f8-note-2026-10-06.md`](m8-phase-a-f6-f8-note-2026-10-06.md) §5.1。

**边界**：**结论不是「已修复」** —— native transport-close 回调**仍然缺席**，
本补记不改变上表 F6 行的事实描述，只补「风险已接受」这一签字事实。
