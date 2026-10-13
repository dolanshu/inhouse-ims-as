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

# `platform/` — 内核（layer ②）

每个 AS 实例都构建于其上的共享壳。它包含对所有用例共同的东西，不含任何属于某一个用例的东西：

| 关注点 | 为什么住在这里 |
|---|---|
| 进程壳（`main`、`bootstrap`） | 启动、自检、关闭一个 AS 进程的统一方式 |
| B2BUA 状态机（`call_controller`） | 每个用例都需要的 RFC 3261 腿处理 |
| `decide()` seam | 用例注入其业务判决的唯一点 |
| `Transport` seam | 今天 UDP，生产里到 S-SBC 的 TLS（ADR-0016） |
| `StateStore` seam | 今天内存，生产里 Redis（ADR-0002） |
| 可观测性原语 | 每个进程统一的、基于 OTel 的信号模型 |

## 硬性规则

**这个包绝不能 import `apps/*`、`services/*` 或 `testbed/*`。**
依赖方向是单向的，由 `tests/test_library_independence.py` 断言，而非由目录布局保证。

## 状态

仅有骨架。代码通过 `docs/migration/triage.md` 里的甄别驱动迁移进来；绝不整块照搬。

## 进程壳环境变量（SIP / D10 工程）

> 下表中「Helm」列标注该变量是否已由 `deploy/helm/` chart 注入：
> - ✅ Helm：已通过 values.yaml → ConfigMap / Secret → env/envFrom 注入
> - ⚙️ pure env：仅代码读取，需通过 `runtime.extraEnv` 或外部环境注入
> - 「Helm 对应键」列出 values.yaml 中驱动该变量的键（若 Helm 通过其他变量名如 `SIP_*` 间接驱动，则标注其映射关系）

| 变量 | 说明 | Helm | Helm 对应键 / 备注 |
|------|------|------|--------------------|
| `AS_ENABLE_SIP_RUNTIME=1` | 启动 `SipStackService`（`ResipRuntimeListener` + 可选恢复） | ⚙️ pure env | 需通过 `runtime.extraEnv` 显式开启 |
| `AS_SIP_ACCEPT_ALL_INVITES=1` | 测试 harness：原生 DUM 完成 100/180/200 并触发 dialog-established 回调 | ⚙️ pure env | 仅开发/测试使用 |
| `AS_SIP_BIND_ADDRESS` | SIP 监听绑定地址（如 `0.0.0.0`）；缺省回退到 `SIP_LISTEN_ADDR` | ✅ Helm（间接） | `sip.listenAddr` → `SIP_LISTEN_ADDR`（代码中 `AS_SIP_BIND_ADDRESS` 优先于 `SIP_LISTEN_ADDR`） |
| `AS_SIP_ADVERTISED_ADDRESS` | SIP Contact/SDP 中通告的地址（bind 为 0.0.0.0 时必填） | ⚙️ pure env | 多网卡/外网场景需设置；当前 Helm 未独立暴露 |
| `AS_SIP_UDP_PORT` | UDP 监听端口；缺省回退到 `SIP_LISTEN_PORT` | ✅ Helm（间接） | `sip.port` → `SIP_LISTEN_PORT`（代码中 `AS_SIP_UDP_PORT` 优先） |
| `AS_SIP_TCP_PORT` | TCP 监听端口；缺省回退到 `SIP_LISTEN_PORT`（仅当 TCP 启用时有效） | ✅ Helm（间接） | `sip.port` → `SIP_LISTEN_PORT`（同时驱动 UDP 与 TCP） |
| `AS_SIP_TLS_PORT` | TLS 监听端口；缺省回退到 `SIP_TLS_LISTEN_PORT` | ✅ Helm（间接） | `sip.tlsPort` → `SIP_TLS_LISTEN_PORT` |
| `AS_SIP_ENABLE_TCP` | 是否启用 TCP 传输（默认 0 = 禁用；`SIP_LISTEN_PORT` 存在时也会自动启用） | ⚙️ pure env | Helm 通过 `sip.port` 隐式驱动（`SIP_LISTEN_PORT` 非空即启用 TCP） |
| `AS_SIP_DISABLE_UDP` | 是否禁用 UDP 传输（默认 0 = 启用） | ⚙️ pure env | 纯环境变量控制 |
| `AS_SIP_NEXT_HOP` | 出站 SIP 下一跳（S-SBC 南向地址）；用于 `AS_SIP_ROUTE_HOOK` 模块构建 Request-URI | ⚙️ pure env | 仅 translation/forward 用例需要；当前 Helm 未暴露 |
| `AS_SIP_NEXT_HOP_PORT` | 出站下一跳 UDP/TCP 端口（默认 5060） | ⚙️ pure env | 同上 |
| `AS_SIP_NEXT_HOP_TLS_PORT` | 出站下一跳 TLS 端口（默认 5061） | ⚙️ pure env | 同上 |
| `AS_SIP_ROUTE_HOOK` | 路由钩子模块名（如 `as_translation.outbound`）；由平台按名加载，决定 FORWARD/TRANSLATE 的出站 Request-URI | ⚙️ pure env | 每个用例需设置对应模块 |
| `AS_TLS_CERT_PATH` | TLS 证书路径；缺省回退到 `SIP_TLS_CERT_PATH` | ✅ Helm（间接） | `tls.secretName` 挂载到 `/etc/as/tls/` → `SIP_TLS_CERT_PATH` |
| `AS_TLS_KEY_PATH` | TLS 私钥路径；缺省回退到 `SIP_TLS_KEY_PATH` | ✅ Helm（间接） | 同上 |
| `AS_TLS_CA_PATH` | TLS CA 证书路径；缺省回退到 `SIP_TLS_CA_PATH` | ✅ Helm（间接） | 同上 |
| `AS_TLS_ENABLE` | 是否启用 TLS（默认 0；`SIP_TLS_ENABLED` 或证书路径存在时也会启用） | ✅ Helm（间接） | `tls.enabled` → `SIP_TLS_ENABLED` |
| `AS_TLS_REQUIRE_CLIENT_CERT` | 是否要求客户端证书（mTLS，默认 true）；缺省回退到 `SIP_TLS_REQUIRE_CLIENT_CERT` | ✅ Helm（间接） | `tls.requireClientCertificate` → `SIP_TLS_REQUIRE_CLIENT_CERT` |
| `AS_PEER_ALLOWED_ADDRESSES` | 对端白名单 IP/CIDR（逗号分隔）；缺省回退到 `SIP_PEER_ALLOWLIST` | ✅ Helm（间接） | `sip.peerAllowlist` → `SIP_PEER_ALLOWLIST` |
| `AS_PEER_ALLOWED_CERT_FINGERPRINTS` | 对端证书指纹白名单（逗号分隔） | ⚙️ pure env | 当前 Helm 未暴露；ADR-0016 白名单机制的第二层 |
| `AS_RECOVERY_CASE` | Checkpoint `case` 命名空间（默认 `translation`） | ⚙️ pure env | 纯环境变量控制 |
| `AS_RECOVERY_CALL_KEYS` | 逗号分隔的 call key；进程启动时经 `RecoveryCoordinator` 异步 restore | ⚙️ pure env | 故障恢复场景使用 |
| `AS_RECOVERY_NATIVE_ON_START` | 默认 `1`；为 `0` 时仅加载 checkpoint 到 `CallController` 而不起 RecoveryTU | ⚙️ pure env | 纯环境变量控制 |
| `AS_RECOVERY_CHECKPOINT_TTL_SECONDS` | Checkpoint TTL（默认 3600） | ⚙️ pure env | 纯环境变量控制 |
| `AS_RESIP_RECOVERY_CHECKPOINT_FILE` | **仅测试**：单文件 adapter 回退路径 | ⚙️ pure env | 测试专用 |
| `AS_REDIS_URL` | 可选；支持 `redis://` 与 `redis+sentinel://`；未配置 Redis 则 checkpoint 使用 `InMemoryStateStore`（开发） | ✅ Helm（间接） | `redis.url` / stateStores → `REDIS_URL`（代码中 `AS_REDIS_URL` 优先） |
| `AS_REDIS_SENTINEL_HOSTS` | 可选；与 `AS_REDIS_SENTINEL_MASTER` 成对使用（逗号分隔 `host:port`） | ✅ Helm（间接） | `redis.sentinel.addresses` → `REDIS_SENTINEL_HOSTS` |
| `AS_REDIS_SENTINEL_MASTER` | Sentinel 服务名（master set name） | ✅ Helm（间接） | `redis.sentinel.masters` 首个 → `REDIS_SENTINEL_MASTER_NAME` |
| `AS_RULESET_JSON` | 内联 JSON 规则列表或 `{"rules": [...]}`；用于加载决策规则 | ⚙️ pure env | 开发/测试场景；生产通过 ConfigBundle |
| `AS_CONFIG_BUNDLE_PATH` | ConfigBundle 格式 JSON 文件路径（含 rules 子集） | ⚙️ pure env | Helm 侧通过 `runtime.bundleConfigMap` 挂载到 `/etc/as/bundle/bundle.json` |
| `AS_HEALTH_PORT` | HTTP health/metrics 端口 | ✅ Helm | `health.port` |
| `AS_USE_CASE` | 用例名（用于 metrics 标签等） | ✅ Helm | `useCases[].name` |
| `AS_M5_PROBE_SIP_STATUS` | M5 探针：启动时注入一个 SIP 状态码计数（验证 metrics 接线） | ✅ Helm | `m5.probeSipStatusCode` |
