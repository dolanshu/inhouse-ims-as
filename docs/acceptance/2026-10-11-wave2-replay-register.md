# Wave 2 回放对拍用例登记（A4-3「独立 issue」仓内载体）

> **落盘日期：2026-10-11。状态：已落盘，待维护者评审。**
>
> **本文件是 A4-3 裁决所指「独立 issue」的仓内载体；本项目无外部 issue 跟踪，仓内文档即追踪系统。**
> 2026-10-11 维护者裁决：G2 / A4-3 所称「后置到独立 issue」以**仓内登记 doc**（即本文件）作为载体，
> 不再另行创建外部 issue。裁决出处见 §1。
>
> **当前状态：载体已建，用例未实现，待 A4 e2e 批次 Wave 1 落地后启动。**
>
> **本文件不签收 REQ-F-1**：REQ-F-1（14 条 B2BUA 全文回放）全文状态**仍 open**；本文件只是追踪载体，
> 不是实现、不是验收证据。本文件同样不签收 REQ-F-2 / REQ-F-4，不签收任何里程碑，不构成外部验收通过。

---

## 1. 背景与裁决出处

Wave 2（14 条逐条消息回放对拍）在 e2e 分波计划中被明确后置，又经 2026-10-10 裁决记为
「后置到独立 issue、本迭代不创建」；2026-10-11 维护者裁决以本仓内文件作为该 issue 的载体。

| 出处 | 位置（2026-10-11 逐行核实） | 原文要点 |
|---|---|---|
| e2e 分波计划 | [`2026-10-09-e2e-test-plan.md`](2026-10-09-e2e-test-plan.md) 「Wave 2 — REQ-F-1 形状（仍无控制台）」节（`:66-74`） | Wave 2 工作定义与完成标准（见 §3 摘录） |
| 同上 | 同文件 Wave 1 节「**明确不做（Wave 1）：14 条逐条 header 对拍、控制台、kind、容量数字。**」（`:64`） | 14 条逐条对拍不属于 Wave 1 |
| 2026-10-10 裁决 | [`../handoff/2026-10-10-unfinished-assessment-and-next-plan.md`](../handoff/2026-10-10-unfinished-assessment-and-next-plan.md) §0-A.6 裁决记录表 **G2 / A4-3** 行（`:56`） | 「Wave 2 的 14 条回放用例后置到独立 issue；本迭代仅登记为 gap；本任务**不创建 issue**。」 |
| 决策记录抄录 | [`../plan.md`](../plan.md) §0「产品决策记录」表 G2 / A4-3 行（`:39`） | 「Wave 2 回放用例后置到独立 issue；本迭代按 gap 记录」 |
| 载体裁决 | 维护者 2026-10-11 裁决（登记于 [`../handoff/2026-10-11-open-adjudication-register.md`](../handoff/2026-10-11-open-adjudication-register.md) §2 P5 条目 2026-10-11 收尾轮追加段） | 以仓内 doc 代替外部 issue；本文件即该载体 |

---

## 2. 用例清单：14 条基准消息

基准实物已在仓内：[`../../testbed/contracts/sip-baseline/S1-basic-call/`](../../testbed/contracts/sip-baseline/S1-basic-call/)
（场景 S1 基本呼叫，sippy 基线，抓取日期 2026-09-28；序列说明见该目录 `README.md`）。
下表文件名逐字录自该目录（2026-10-11 Glob 实测，共 14 个 `.txt`，另加 `README.md`），按 `01 → 14` 排序；
方向（`in` = 进入 AS 的入腿、`out` = AS 发出的出腿）、对端（`trunk` / `core`）与消息类型均可从文件名直接读出，
本表不编造消息文件内部细节。

| # | 文件名（逐字） | 方向 | 对端 | 消息类型 | 序列中的位置（据该目录 README） |
|---|---|---|---|---|---|
| 01 | `01-in-invite-trunk.txt` | 入腿（trunk→AS） | trunk | INVITE | 呼叫起始 |
| 02 | `02-out-100-trunk.txt` | 出腿（AS→trunk） | trunk | 100 Trying | 入腿 INVITE 的临时响应 |
| 03 | `03-out-invite-core.txt` | 出腿（AS→core） | core | INVITE | B2BUA 翻腿（新 Call-ID） |
| 04 | `04-in-100-core.txt` | 入腿（core→AS） | core | 100 Trying | 出腿 INVITE 的临时响应 |
| 05 | `05-in-180-core.txt` | 入腿（core→AS） | core | 180 Ringing | 被叫振铃 |
| 06 | `06-out-180-trunk.txt` | 出腿（AS→trunk） | trunk | 180 Ringing | 振铃回送主叫 |
| 07 | `07-in-200-core.txt` | 入腿（core→AS） | core | 200 OK | 被叫应答 |
| 08 | `08-out-ack-core.txt` | 出腿（AS→core） | core | ACK | 确认出腿应答 |
| 09 | `09-out-200-trunk.txt` | 出腿（AS→trunk） | trunk | 200 OK | 应答回送主叫 |
| 10 | `10-in-ack-trunk.txt` | 入腿（trunk→AS） | trunk | ACK | 呼叫建立完成 |
| 11 | `11-in-bye-core.txt` | 入腿（core→AS） | core | BYE | 释放发起（core 侧先挂） |
| 12 | `12-out-200-core.txt` | 出腿（AS→core） | core | 200 OK | BYE 响应（core 侧） |
| 13 | `13-out-bye-trunk.txt` | 出腿（AS→trunk） | trunk | BYE | 释放翻腿到 trunk |
| 14 | `14-in-200-trunk.txt` | 入腿（trunk→AS） | trunk | 200 OK | 释放完成（终态） |

另：同目录 `README.md` 为场景与序列说明，不在 14 条消息计数内。

---

## 3. 对拍工作定义

工作定义全部来自 [`2026-10-09-e2e-test-plan.md`](2026-10-09-e2e-test-plan.md) Wave 2 节（`:66-74`），
本节只作概括与引用，**不改写其结论**：

1. **拓扑前提**：在 Wave 1 拓扑上，对**一通** T1（翻译接通）呼叫采集入 / 出腿关键消息
   （方法 + 最终响应码序列），与 `S1-basic-call` 基准做**归一化**对比（`:70`）。
2. **双腿 Call-ID**：断言 **C_in ≠ C_out**（REQ-F-2 子集）（`:71`）。
3. **SDP 逐字节**：SDP offer 入腿与出腿**逐字节**一致（REQ-F-4）；**若实现成本不可接受，则单列 follow-up**（`:72`）。
4. **完成标准（原文要点）**：`test-plan.md` 的 REQ-F-1 勾选只能改为
   「**自动化子集已覆盖 / 全文仍 open**」并链到具体用例名；**未对拍 14 条时不得打勾全文**（`:74`）。

Wave 1 节明写「**明确不做（Wave 1）：14 条逐条 header 对拍**」（`:64`），即本批用例不属于 Wave 1 范围。

---

## 4. 关联需求与现状

| 关联项 | 关系 | 现状口径 |
|---|---|---|
| **REQ-F-1** | 14 条 B2BUA 全文回放即本批用例本体 | **全文仍 open，本文件不签收。** 既有口径见 [`../product/compliance-matrix.md`](../product/compliance-matrix.md)：`:79`「14 条消息全文回放未签收」、`:117`「14 条全文未签收」、`:234` S1 行「Partial（14 条全文未签收）」、`:266`「REQ-F-1 的 14 条 B2BUA **未**由 harness 签收」（2026-10-11 检索核实） |
| **REQ-F-2** | Wave 2 对拍断言 C_in ≠ C_out，是 REQ-F-2（双腿独立 Call-ID）的子集 | 随 Wave 2 用例实现时覆盖；本文件不改变其签收状态 |
| **REQ-F-4** | SDP offer 入 / 出腿逐字节恒等 | e2e 计划允许在成本不可接受时**单列为 follow-up**；本文件不预判取舍 |
| 基准实物 | [`../../testbed/contracts/sip-baseline/S1-basic-call/`](../../testbed/contracts/sip-baseline/S1-basic-call/) 14 个消息文件 + README | 已在仓内、可追溯（§2 清单） |

**e2e 落地现状（2026-10-11 检索核实）：**

- `pytest.mark.e2e` 在全仓 `.py` 文件中**命中 0 处**——连 Wave 1 都尚未落地；
  与 [`2026-10-09-e2e-test-plan.md`](2026-10-09-e2e-test-plan.md) 文首「`pytest -m e2e` 当前 **0 条**」（`:4`）一致。
- **启动前提**：① A4 e2e 批次的 **Wave 1 先行落地**（`testbed/e2e/test_sip_first_edition.py`，
  裁决见 2026-10-10 handoff §0-A.6 G2 / A4-1 行 `:54`）；② 在**具备必需 native extension** 的环境运行
  （G2 / A4-2：缺 native 时 **fail** 不 skip，`:55`）。

---

## 5. 不做的事（本文件边界）

- **本文件不实现任何用例**：不新建 `testbed/e2e/` 测试文件、不写对拍 harness、不改任何产品 / 测试代码。
- **不补抓包**：基准以仓内既有 `S1-basic-call` 14 个文件为准；不新增抓包、不引用真实流量。
- **不签收**：不签收 REQ-F-1 / REQ-F-2 / REQ-F-4，不签收任何里程碑，不构成外部验收通过。
- **不替维护者排期**：用例实现属于 A4 e2e 批次，启动顺序以维护者授权为准。
- **未来实现时的回写约定**：新建 `testbed/e2e/` 测试文件实现对拍后，在本文件**追加**一节登记结果
  （实现日期、用例文件名、对拍范围、SDP 对拍是纳入还是单列 follow-up），并按 e2e 计划完成标准
  把 REQ-F-1 勾选改为「自动化子集已覆盖 / 全文仍 open」；14 条未全部对拍前**不得**勾选全文。
