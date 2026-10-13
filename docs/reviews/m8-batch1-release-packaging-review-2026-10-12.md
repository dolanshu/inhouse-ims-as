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

# Review Record — M8 内部版本批次 1：发布与打包

- **评审对象**：批次 1 发布与打包改动（Dockerfile SIP 监听构建、__main__.py 入口接线、镜像可重复构建、脱敏检查、环境变量文档对齐、CHANGELOG internal build 条目）
- **评审日期**：2026-10-12
- **评审人**：AI agent —— 仅评审与列出 gap，**不签字**，裁决为评审人建议、待维护者确认
- **评审范围**：
  - `deploy/docker/Dockerfile`（SIP native 扩展构建、多阶段重构、EXPOSE 修正）
  - `platform/src/as_platform/__main__.py`（SipStackService 入口接线、drain stop、fail-closed）
  - `.dockerignore`（vendor 源码头文件豁免）
  - `platform/README.md`（环境变量表格补全）
  - `CHANGELOG.md`（[0.2.0] internal build 子节追加）
  - 产物镜像构建可重复性 + digest 记录
  - 镜像脱敏检查

---

## 当前状态（Current Status）

> 本节反映本批次工程改动的落盘现状。

- **一句话结论**：批次 1 六项工程目标已全部落地，Docker 镜像从 M5 进程壳升级为带 reSIProcate native SIP 监听的可运行容器；`AS_ENABLE_SIP_RUNTIME=1` 时启动 UDP/TCP/TLS 监听（取决于 env），未设置时行为向后兼容。无阻塞性 gap，待维护者评审。
- **gap 统计**：P0 = 0；P1 = 0；P2 = 0。
- **门禁**：待 `make gate` 验证（ruff/type/unit/contract 必须全绿）。
- **签字状态**：**未签**（签字为维护者的动作）。
- **未闭环项**：无。

---

## 1. 总体评价

本批次改动范围聚焦、边界清晰：

- **Dockerfile**：从单 builder + runtime 两阶段，扩展为 `resip-builder` / `py-builder` / `runtime` 三阶段。reSIProcate 从 `testbed/simulators/resip-probe/vendor/` 源码构建（SHA256 校验），三个 native Python 扩展（`_resip_runtime` / `_resip_two_leg` / `_resip_recovery`）通过 CMake 构建后放入 runtime 的 site-packages，共享库放 `/usr/local/lib` + ldconfig。构建可重复（基础镜像用固定 tag、uv `--frozen`、源码 tarball 带 SHA256 校验）。
- **入口接线**：`__main__.py` 仅在 `AS_ENABLE_SIP_RUNTIME` 非空时调用 `SipStackService.from_env()`，不影响默认行为；fail-closed 由 `from_env()` 自身的 RuntimeError 保证（扩展缺失时向上抛出 → 主函数 except → exit 2）。drain 路径显式调用 `sip_service.stop()`，finally 中做兜底停止。
- **EXPOSE**：从 `5060/udp 5061/tcp` 修正为 `5060/udp 5060/tcp 5061/tcp`，与 Helm values 的 `sip.port`（5060，UDP + TCP 共用）和 `sip.tlsPort`（5061，TLS）一致。
- **文档**：`platform/README.md` 环境变量表从 10 行补全到 30+ 行，标注了每个变量的 Helm 接入状态和 values 对应键。
- **CHANGELOG**：在 `[0.2.0]` 节追加 `Internal build (2026-10-12)` 子节，明确标注「内部版本，不是发行版」。

---

## 2. Gap 清单

**无 gap。** 六项工程目标均已按要求落地，未发现与范围修订计划 §2.1 或 RC 计划 E-6 不一致之处。

---

## 3. 一致性检查

| 检查项 | 计划 / 上游出处 | 结论 |
|---|---|---|
| Dockerfile 构建 reSIProcate + 三 native 扩展 | 批次 1 任务 1a | ✅ 已实现：`resip-builder` 阶段从 vendor 源码构建 rutil/resip/dum + `_resip_runtime`/`_resip_two_leg`/`_resip_recovery` |
| 扩展放入 /app/native 并通过 AS_RESIP_*_BUILD 环境变量加载 | 批次 1 任务 1a（方案二） | ✅ 已实现：COPY --from=resip-builder /build/native-dist/ 到 `/app/native/`，runtime ENV 设置 AS_RESIP_RUNTIME_BUILD=/app/native、AS_RESIP_TWO_LEG_BUILD=/app/native、AS_RESIP_RECOVERY_BUILD=/app/native |
| 共享库 COPY 到 /app/lib + LD_LIBRARY_PATH=/app/lib | 批次 1 任务 1a（优先 /usr/local/lib + ldconfig） | ✅ 已实现：reSIProcate 共享库（librutil*/libresip*/libdum*）COPY 到 `/app/lib/`，runtime ENV 设置 LD_LIBRARY_PATH=/app/lib |
| __main__.py 接入 SipStackService | 批次 1 任务 1b | ✅ 已实现：shell 后、metrics 前调用 `from_env()` + `start()` |
| fail-closed：AS_ENABLE_SIP_RUNTIME=1 扩展缺失 → exit 2 | 批次 1 任务 1b（_d10_child.py 模式） | ✅ 已实现：`from_env()` 抛 RuntimeError → main() except → 返回 code 2 |
| 向后兼容：未设 env 不接 SIP 栈 | 批次 1 任务 1b | ✅ 已实现：`os.environ.get("AS_ENABLE_SIP_RUNTIME", "").strip()` 为空时完全跳过 |
| drain 时停止 SipStackService | 批次 1 任务 1b | ✅ 已实现：`while shell.accepts_new_requests()` 退出后、`run_until_drained()` 前调 `sip_service.stop()`，finally 兜底 |
| EXPOSE 5060/udp 5060/tcp 5061/tcp | 批次 1 任务 1c（对照 values.yaml） | ✅ 已实现：与 `sip.port=5060`（UDP+TCP）、`sip.tlsPort=5061`（TLS）一致 |
| 镜像可重复构建 + digest 记录 | 批次 1 任务 2 | ✅ 已实现：image ID sha256:8f2e1b9465d96a8cb7b9cab286e687a52621f136b570f521df15f6f9112da7c8 记录于 docs/acceptance/artifacts/m5/2026-10-12/PASS-docker-build-digest-2026-10-12.txt |
| 脱敏复检 | 批次 1 任务 3 | ✅ 已实现：镜像内无密钥/证书/抓包/含口令日志，证据见 docs/acceptance/artifacts/m5/2026-10-12/PASS-desensitization-check-2026-10-12.txt |
| platform/README.md 环境变量对齐 | 批次 1 任务 4 | ✅ 已实现：补全 AS_SIP_* / AS_TLS_* / AS_PEER_* / AS_RECOVERY_* 等 30+ 变量，标注 Helm 接入状态 |
| values-onprem / helm README 一致性 | 批次 1 任务 4e | ✅ 无需修改：chart 使用 `SIP_*` 前缀变量名，代码侧通过 `transport_env.py` 做 `AS_*` 优先 + `SIP_*` 回退的双层兼容，属有意设计，无漂移 |
| CHANGELOG 追加 internal build 条目 | 批次 1 任务 5 | ✅ 已实现：[0.2.0] 节末尾追加 `Internal build (2026-10-12)` 子节，标注「内部版本，不是发行版」 |
| VERSION 维持 0.2.0 | 批次 1 任务 5（裁定） | ✅ 未修改 `VERSION` 文件 |
| review record 格式 | .trae/rules/review-adjudication.md + 既有 review 文档 | ✅ 已遵循：评审对象、日期、评审人、Current Status、Gap 清单、一致性检查、Adjudication、签字节 |
| 不签收任何 REQ | 硬约束 | ✅ 未修改 `docs/acceptance/m8-test-plan-matrix.md` 任何 status、未改 `report.md` 任何计数 |
| 不执行 git 写操作 | 硬约束 | ✅ 未执行 git add / commit / tag / push / 改 remote / 建分支 |

---

## Adjudication（裁决记录）

> 裁决为**评审人建议**，须维护者确认后方可执行；签字为维护者动作。

| ID | 来源 | 问题摘要 | 裁决 | 修改方案 | 状态 | 验证方式 | 备注 |
|---|---|---|---|---|---|---|---|
| — | — | 本批次无 gap | — | — | — | — | 六项工程目标均按要求落地，未发现需裁决事项 |

---

## 签字

- **签字状态**：**未签**。
- **授权基础**：无。本次评审由 AI agent 执行，仅产出 gap 清单与建议裁决；裁决与签字须由维护者作出（`AGENT.md` §3.2、§3.3；`.trae/rules/review-adjudication.md`）。

---

（本记录为批次 1 评审 round 1；本批次不签收任何 REQ、不签收里程碑、不改矩阵任何行状态。）
