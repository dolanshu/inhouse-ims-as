# M5 committable evidence (redacted)

Sanitized M5.1 transcripts. Raw kind runs may still land under gitignored `artifacts/m5/<date>/`.

## 文件名即结论（2026-10-11 起）

本目录内证据文件强制前缀 `PASS-` / `FAIL-` / `FAILCLOSED-`，格式为 `<结论>-<被验项>-<日期>.txt`
（`-sample` 后缀表示该次运行的尾部摘要）。依据见
[`../../handoff/2026-10-11-open-adjudication-register.md`](../../handoff/2026-10-11-open-adjudication-register.md) §7.4 第 1 层。

三个前缀不可互换，**一律以文件名为准**：

| 前缀 | 含义 | 是不是通过证据 |
|---|---|---|
| `PASS-` | 被采集命令 **exit 0** | 是 |
| `FAIL-` | 被采集命令**跑了但非零退出** | **不是** |
| `FAILCLOSED-` | 显式拒绝而非猜测（如 `M5_STRICT=1` 而无集群，`exit=1`） | **不是** |

> **`FAIL-` 是 2026-10-11 新增的前缀。** 此前 `deploy/kind/m5-record-artifacts.sh` 用
> `make X 2>&1 | strip_ansi > file` 采集，管道退出码取自 `strip_ansi`（恒为 0）而不是 `make`，
> 于是失败的运行被写成了 `PASS-` 文件 —— 在「文件名即结论」之下，这等于凭空造出一份绿证据。
> 该脚本现已按 `PIPESTATUS[0]` 分流：失败落 `FAIL-`、脚本最终非零退出、文件头写明真实退出码。

> **本目录内 `Fail` / `ERROR` 字样属正常语义，不得据此判定文件失败；一律以文件名前缀为准。**

## 索引表

| Path | 结论 | Meaning |
|---|---|---|
| `2026-10-05/PASS-gate-2026-10-05.txt` | 通过 | full `make gate` (must end in pytest passed)。**含 SKIPPED 项**，见下方「三件容易被误读的事」第 3 条 |
| `2026-10-05/PASS-gate-sample-2026-10-05.txt` | 通过 | last lines of that run（同样含 SKIPPED 项） |
| `2026-10-05/PASS-chart-check-2026-10-05.txt` | 通过 | `make chart-check`，末行 `chart-check: OK`；含 `[INFO] Fail:` 行属预期断言，见下方第 2 条 |
| `2026-10-05/PASS-chart-check-sample-2026-10-05.txt` | 通过 | 同上运行的内容副本 |
| `2026-10-05/PASS-alert-check-2026-10-05.txt` | 通过 | `promtool check rules` → `SUCCESS: 5 rules found`（**仅覆盖当时的原 5 条规则**） |
| `2026-10-05/PASS-alert-check-sample-2026-10-05.txt` | 通过 | 同上运行的内容副本 |
| `2026-10-05/FAILCLOSED-m5-strict-context-2026-10-05.txt` | **不是通过证据** | `M5_STRICT=1` with no `kind-as-m5`（**exit=1**），fail-closed 路径记录 |
| `2026-10-11/PASS-alert-check-full-2026-10-11.txt` | 通过 | Docker 运行 `promtool check rules` → `SUCCESS: 10 rules found`（**覆盖全部 3 组 10 条规则**：as.call-path 5 + as.runtime 3 + as.platform 2）；镜像 `prom/prometheus:v2.45.0`，host `WIN-03IB7NIEPF0` |
| `2026-10-11/PASS-gate-2026-10-11.txt` | 通过 | 本机（`dev-win03ib7niepf0`）`make gate`（ruff format --check / ruff check / mypy / pytest unit+contract）→ `1037 passed, 10 skipped, 206 deselected`。**含 SKIPPED 项**，引用时必须一并说明 skip 构成，见下方第 3 条 |
| `2026-10-11/PASS-gate-sample-2026-10-11.txt` | 通过 | 同上运行的尾部摘要（同样含 SKIPPED 项） |
| `2026-10-11/PASS-chart-check-2026-10-11.txt` | 通过 | 本机 `make chart-check`，末行 `chart-check: OK`、`1 chart(s) linted, 0 chart(s) failed`；语义与 2026-10-05 行相同（`[INFO] Fail:` 属预期断言，见下方第 2 条）；helm 3.16.4（`tools/bin/`，infra bootstrap 后首次本机产出） |
| `2026-10-11/PASS-chart-check-sample-2026-10-11.txt` | 通过 | 同上运行的内容副本 |
| `2026-10-11/PASS-alert-check-2026-10-11.txt` | 通过 | **本地** promtool **2.55.1**（`tools/bin/`，与 2026-10-05 证据**同版本**）`check rules` → `SUCCESS: 10 rules found`（**覆盖全部 3 组 10 条规则**：as.call-path 5 + as.runtime 3 + as.platform 2）；二进制溯源为官方镜像提取（非 release tarball，安装当日 GitHub 不可达），见 [`../../../handoff/2026-10-11-local-infra-bootstrap-execution-record.md`](../../../handoff/2026-10-11-local-infra-bootstrap-execution-record.md) |
| `2026-10-11/PASS-alert-check-sample-2026-10-11.txt` | 通过 | 同上运行的内容副本 |
| `2026-10-11/FAILCLOSED-m5-strict-context-2026-10-11.txt` | **不是通过证据** | `M5_STRICT=1` context 检查：本次 `kind-as-m5` context 在位、检查本身 `exit=0`，但按采集脚本设计该文件**一律**记 `FAILCLOSED`、永不作为通过证据引用（与 2026-10-05 行的 `exit=1` 失败路径不同，二者都不是通过证据） |
| `2026-10-11/FAIL-m5-verify-strict-2026-10-11.txt` | **不是通过证据** | `M5_STRICT=1 bash deploy/kind/m5-verify.sh` **exit=1**：新建 `as-m5` 集群只有空控制面（`No resources found in as-m5 namespace.`，产品 AS pod 未部署），jsonpath 断言越界。**如实失败** —— 印证「工具与集群就位 ≠ 集群级产品验证通过」 |
| `2026-10-11/FAIL-m5-verify-strict-sample-2026-10-11.txt` | **不是通过证据** | 同上运行的尾部摘要 |
| `README.md` | — | this index |

## 三件容易被误读的事

1. **`FAILCLOSED-m5-strict-context-2026-10-05.txt` 是 exit=1 的失败记录，不是通过证据。**
   它记录的是 `M5_STRICT=1` 且无 `kind-as-m5` 集群时的 **fail-closed 路径**（内容为
   `ERROR: kind-as-m5 context missing (M5_STRICT=1)` / `exit=1`）。它的价值在于证明「无集群时显式失败」
   这一行为存在，**不得**计入任何「已通过」清单。

2. **`PASS-chart-check-2026-10-05.txt` 中的 `[INFO] Fail: tls.enabled=true requires tls.secretName`
   是 chart-check 对 fail-closed 渲染的预期断言，属正常语义，不代表该文件失败。**
   同理适用于同行附近的 `sip.peerAllowlist must be non-empty (ADR-0016 fail-closed)` 与
   `[INFO] Chart.yaml: icon is recommended`；判定依据是末行 `chart-check: OK` 与
   `1 chart(s) linted, 0 chart(s) failed`。

3. **`PASS-gate-2026-10-05.txt` 含 SKIPPED 项；按既有纪律「skip 不是通过证据」。**
   该次运行为 `878 passed, 2 skipped, 145 deselected`，两条 SKIPPED 均来自
   `testbed/simulators/tests/test_derived_baseline.py:245` 与 `:279`
   （S1-basic-call 未构造 Route / Record-Route header，需专门的 M2 probe capture 才能断言）。
   **引用该文件时必须一并说明 skip 构成**，不得只写「gate 通过」。

## 引用规范

任何证据一律用三元组 `(结论, 证据文件, 日期)` 表述，例如
`(已验证, docs/acceptance/artifacts/m5/2026-10-05/PASS-chart-check-2026-10-05.txt, 2026-10-05)`；
环境名见 [`../../environments.md`](../../environments.md)（文档中禁止再出现匿名的「本机」）。

Do not store passwords, tokens, DSNs, or cookies.