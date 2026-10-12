<!-- 
原始笔记（元信息）：
本文档目的为介绍本项目，为制作PPD提供参考。
参考文档：
AGENT.md
product-packaging-plan.md
README.md

突出与POC repo的区别
POC 路径：/home/shudong/project/3rtparty_AS_POC
突出正式/商业版的特点

完成度与restriction
verion 1.1 - 未来展望
当前项目提供的两种AS为范例，项目的目的为提供一个可扩展的AS框架，用于构建各种类型的AS。  -- 联网查询可能的AS 种类。

不要在本文中提及项目开发过程中的具体phase, M1/M2/..., 本文应该是一个general introduction。

注意，本文内容不是生成PPT的提示词，而是用于指导PPT制作的参考材料。
-->

# In-house IMS Application Server 项目介绍

> 本文档为项目介绍参考材料，用于指导 PPT 制作。产品名称为文档暂用名，正式命名待决策。

---

## 一、项目概述

### 1.1 产品定位

**产品名称**：In-house IMS Application Server（文档暂用名）

**网络角色**：3GPP Third-Party AS（第三方应用服务器）

**核心定位**：产品化的第三方 IMS 应用服务器，采用单租户、on-premises（本地部署）模式，部署在运营商 IMS 核心网之外。

### 1.2 网络拓扑与部署

```
┌─────────────────────────────────────────────────────────────────┐
│                    运营商 IMS 核心网（信任域）                      │
│  UE → P-CSCF → S-CSCF（按 iFC 触发）←→ HSS（iFC 签约）          │
└────────────────────┬────────────────────────────────────────────┘
                     │ ISC 触发
                     ▼
┌─────────────────────────────────────────────────────────────────┐
│                    运营商边界（非交付范围）                         │
│                      S-SBC（透明桥接）                            │
└────────────────────┬────────────────────────────────────────────┘
                     │ SIP trunk（UDP/TLS）
                     ▼
┌─────────────────────────────────────────────────────────────────┐
│                    网外 · 本项目交付边界                            │
│              第三方 AS（In-house IMS AS）                         │
│         • 单租户 on-premises 部署                                 │
│         • 多业务承载平台                                          │
│         • 一用例一进程                                            │
└─────────────────────────────────────────────────────────────────┘
```

**部署特点**：
- 部署在运营商 IMS 网络之外
- 由 S-CSCF 经运营商 S-SBC 触发
- S-SBC 做透明桥接，对两侧均透明
- 运行态与治理态数据全部留在客户机房，不出客户边界

### 1.3 多业务承载平台

本系统是一个**多业务承载平台**：
- 每个业务用例是独立进程
- 业务引擎可插拔
- 新增业务不需要改动 IMS 核心网
- S-CSCF 按 HSS 里的 iFC 签约触发 ISC
- 核心网侧只看到标准 ISC 触发
- 业务逻辑跑在独立进程中，不被核心网厂商的业务版本绑定

---

## 二、与 POC 的区别

### 2.1 POC 与产品的本质差异

| 维度 | POC（概念验证） | 本产品（生产级） |
|------|----------------|-----------------|
| **定位** | 在另一套非目标下验证概念 | 产品本身，面向生产部署 |
| **代码来源** | 原型代码 | 全新 git 历史，不导入 POC 历史 |
| **代码采纳** | — | 每个 POC 文件经过甄别：adopt / rewrite / baseline-reference / discard |
| **架构** | 单体原型 | 产品级分层架构（信令面/内核/控制面/数据面/横切/测试平台） |
| **决策机制** | 硬编码 | 决策缝（decide() 纯函数）、StateStore seam、Transport seam |
| **文档体系** | 基础文档 | 完整 ADR 体系（26+ 篇架构决策记录） |
| **测试** | 基础测试 | 四层测试门禁（unit/contract/integration/e2e） |
| **交付形态** | 手动部署 | 单租户 on-premises，Helm 部署 |
| **运维能力** | 基础日志 | 完整可观测性、告警、Runbook |

### 2.2 产品级架构特点

**分层架构**：
1. **信令面（apps/）**：一用例一进程，承载呼叫与业务判决，无状态
2. **内核（platform/）**：进程壳、B2BUA 状态机、decide() 决策缝、Transport/StateStore seam
3. **控制面（services/）**：规则版本库与变更单、运维控制台
4. **数据面**：Redis（运行态）+ PostgreSQL（治理态）
5. **横切能力**：可观测性、安全、运维
6. **测试平台（testbed/）**：契约用例集、仿真网元、真实 socket 压测（研发资产）

**关键设计决策**：
- **决策缝（decide()）**：纯函数判决缝，模块内无 socket、无时钟、无全局状态，可强制 TDD
- **Transport seam**：对端准入与传输策略可替换
- **StateStore seam**：运行态存储可替换
- **一用例一进程**：一个 Deployment / 一个故障域 / 一个灰度单元
- **ISSU draining**：摘流 → draining → 归零才退出，不做在途呼叫迁移

### 2.3 工程体系差异

**ADR 体系**：
- 26+ 篇架构决策记录
- 每个决策都有明确的上下文、决策、后果
- 决策与代码一起演进，不事后补

**测试门禁**：
- `make gate` = ruff format → ruff check → mypy → pytest（unit+contract）
- 四层测试：unit → integration → e2e → performance
- 1100+ 测试用例通过

**文档链贯通**：
需求（Requirement）→ 架构决策（ADR）→ 高层设计（HLD）→ 低层设计（LLD）→ 接口契约 → 代码 + 测试 → 验收项

---

## 三、商业版/产品级特点

### 3.1 产品化包装

**规范符合性**：
- 3GPP 规范符合性矩阵（TS 24.229、RFC 3261 等）
- 逐项标注符合性状态（Fully / Partial / N/A / open）
- 每个判定都有文件/行号或契约场景号作为证据

**网元档案（NE Datasheet）**：
- 容量模型与测量方法
- KPI 定义与门限
- 告警清单
- 依赖关系图
- 资源规格
- 部署形态

**故障定界手册**：
- AS / S-CSCF / HSS / 计费域四方故障归属判断流程
- SIP/Diameter 抓包对齐方法
- "5 分钟自证清白"检查表
- 常见故障剧本

**责任边界矩阵（RACI）**：
- 明确各方责任边界
- 接口抓包责任方
- 多厂商协作定责

### 3.2 运维能力

**可观测性**：
- Prometheus 指标（as_* 系列）
- OTel 导出
- 按 Call-ID 的呼叫轨迹
- Grafana 看板模板

**告警与响应**：
- 告警规则（SIP 5xx 飙升、ISC 超时、会话泄漏等）
- 告警-动作对照表
- 告警级别（P1/P2/P3）
- 升级路径

**运维手册**：
- L1/NOC Runbook
- L2/二线 Runbook
- 摘流回退 Playbook
- 备份恢复方案

### 3.3 交付能力

**预检环境**：
- 一键校验 K8s 版本与 API
- 节点资源检查
- 依赖服务验证
- Helm、RBAC、chart 渲染校验

**离线安装包**：
- 支持 air-gapped 环境
- 运营商机房无外网场景

**Helm 部署**：
- 生产唯一交付形态
- 每个业务用例渲染为独立 Deployment
- 标准 Deployment / ConfigMap / Secret

### 3.4 安全合规

**边界安全**：
- 白名单 + mTLS + 鉴权审计
- 对端按白名单校验
- S-SBC 端到端终止 TLS

**配置治理**：
- 变更单 → 审批 → 写库 → 灰度分发
- 版本存为 PostgreSQL 中的行
- 藏在变更单状态机之后
- 不走 GitOps（不要求运维人员学 Git）

**合规说明**：
- PDPO 合规说明
- 数据留港
- 审计日志

### 3.5 高可用

**ISSU draining**：
- 摘流 → draining → 归零才退出
- 不做在途呼叫迁移
- 严格零呼损滚动升级

**数据存储**：
- Redis Sentinel（运行态）
- PostgreSQL（治理态）
- 冗余部署

### 3.6 明确不做的事

| 不做的事 | 原因 |
|---------|------|
| 不做媒体 | 无 RTP、转码、DTMF、MRF、媒体锚定 |
| 不做 CDR | 不采集、不投递、不归档、不批价 |
| 不做合法监听（LI） | IRI 属于网内网元，第三方 AS 介入引入跨法域暴露 |
| 不做 Diameter Sh | 数据来自自有数据面 |
| 不做多租户 | 单租户 on-premises，运营商交付形态决定 |
| 配置不走 GitOps | 变更单 → 审批 → 写库 → 灰度分发 |
| 不写 Operator（CRD） | 用 Helm + 标准资源 |
| 不发布容量数字 | 容量目标未裁决，不公布 CPS 或并发数字 |

---

## 四、当前提供的两种 AS 范例

### 4.1 号码翻译 AS（translation）

**业务场景**：
- 双腿 B2BUA
- 终结来自 S-SBC 的 trunk INVITE
- 应用翻译与路由决策
- 用新 Call-ID 发起新 INVITE 回去

**技术特点**：
- 决策模块是纯函数（decide()）
- 强制 TDD
- 规则版本化
- 状态外置到 Redis

**架构示意**：
```
S-SBC → INVITE（原 Call-ID）
         ↓
    号码翻译 AS
    ├─ 终结 INVITE
    ├─ 应用翻译规则
    ├─ 生成新 Call-ID
    └─ 发起新 INVITE → S-SBC
```

### 4.2 反诈 AS（anti-fraud）

**业务场景**：
- 单腿
- 甄别主叫
- 放通或应答 608 Rejected（RFC 8688）

**技术特点**：
- 判决函数 test-first
- 主叫甄别逻辑
- 速率限制
- 黑名单/白名单

**架构示意**：
```
S-SBC → INVITE
         ↓
    反诈 AS
    ├─ 甄别主叫
    ├─ 查询规则库
    └─ 判决：放通 / 608 Rejected
```

### 4.3 范例价值

这两种 AS 都是**可扩展框架的范例**：
- 一用例一进程
- decide() 纯函数决策缝
- 规则版本化
- 状态外置到 Redis
- 展示了如何基于平台快速接入新业务

---

## 五、可扩展的 AS 框架

### 5.1 平台定位

项目的目的是提供一个**可扩展的 AS 框架**，用于构建各种类型的 IMS Application Server。

**架构设计天然支持各类 AS 快速接入**：
- 一用例一进程：每个 AS 独立部署、独立故障域、独立灰度
- 可插拔业务引擎：业务逻辑与平台解耦
- 决策缝（decide()）：纯函数判决，可强制 TDD
- 状态外置：运行态在 Redis，治理态在 PostgreSQL

### 5.2 业界常见的 IMS AS 类型

基于 3GPP 标准与运营商实践，常见的 IMS Application Server 类型包括：

#### 号码与路由类
- **号码翻译/路由 AS**（Number Translation/Routing）
  - 号码携带（Number Portability）
  - 号段映射
  - 智能路由

#### 安全与防护类
- **反诈/防骚扰 AS**（Anti-fraud/Spam Protection）
  - 主叫甄别
  - 速率限制
  - 黑名单/白名单
  - 呼叫拦截

#### 语音增值类
- **彩铃/视频彩铃 AS**（Ring Back Tone/Video RBT）
  - 个性化回铃音
  - 企业品牌铃声
  - 视频彩铃

- **语音信箱 AS**（Voicemail）
  - 留言存储
  - 通知（短信/邮件）
  - 回放

- **会议桥 AS**（Conference Bridge）
  - 多方通话
  - 会议控制
  - 会议录音

#### 交互与导航类
- **IVR/自动总机 AS**（Interactive Voice Response）
  - 语音导航
  - DTMF 交互
  - 语音识别集成

#### 计费类
- **预付费计费 AS**（Prepaid Billing）
  - 实时计费
  - 余额查询
  - 在线充值

#### 企业应用类
- **点击拨号 AS**（Click-to-Dial）
  - Web 触发呼叫
  - API 集成

- **呼叫拦截/转接 AS**（Call Barring/Forwarding）
  - 条件呼叫转移
  - 黑名单拦截
  - 勿扰模式

- **VPN AS**（VoIP VPN）
  - 企业虚拟专网
  - 分机互拨
  - 跨地域组网

#### 合规与记录类
- **录音 AS**（Call Recording）
  - 合规录音
  - 按需录音
  - 录音存储与检索

- **通知/公告 AS**（Announcement/Notification）
  - 语音通知
  - 短信通知
  - 广播公告

#### 能力开放类
- **能力开放 AS**（Capability Exposure）
  - 北向 API 开放网络能力
  - 第三方应用集成
  - CPaaS 平台

### 5.3 平台优势

**快速接入**：
- 基于决策缝（decide()）模式，业务逻辑可快速开发
- 状态外置，业务进程无状态，易于扩缩容
- 规则版本化，支持灰度发布与回滚

**独立运维**：
- 每个 AS 独立部署，互不影响
- 独立故障域，故障不扩散
- 独立灰度单元，可单独升级

**不被绑定**：
- 不被核心网厂商的业务版本绑定
- 业务逻辑跑在独立进程中
- 可自主演进业务逻辑

---

## 六、完成度与限制

### 6.1 当前状态

**产品版本**：0.2.0（Unreleased）

**工程门禁**：
- `make gate` 全绿
- ruff、mypy 干净
- 1100+ 测试通过

**生产 SIP 栈**：
- reSIProcate（ADR-0019）
- sippy 仅为 testbed 行为基线参考，不进入生产依赖

**两种 AS 范例**：
- 号码翻译 AS 决策模块已落地
- 反诈 AS 决策模块已落地

**产品化包装文档**：
- product/ 目录：一页纸、网元档案、规范符合性矩阵、责任边界矩阵等
- operations/ 目录：Runbook、故障定界手册、备份恢复方案等
- delivery/ 目录：安装指南、离线安装包、预检脚本等

### 6.2 已知限制与未完成项

**待验收项**：
- E1：reSIProcate 生产路径行为
- E4：TLS 证书热轮换
- E5：状态外置与恢复

**容量数字未裁决**：
- O1（容量目标）未裁决
- 不发布任何 CPS/并发数字
- M6 dev-host 测量仅供内部参考

**端到端路径**：
- e2e 端到端路径已初步落地（8 条测试）
- 真实运营商 S-SBC 与客户 K8s 环境的外部验证待进行

**testbed 定位**：
- testbed 仿真结果是研发资产
- 不充当现网证据
- v1 不把 testbed 作为交付物（ADR-0014）

### 6.3 当前不发布的内容

基于项目原则，以下内容在当前阶段**不发布**：
- 任何容量/性能数字（CPS、CAPS、BHCA、并发、吞吐、时延）
- 真实运营商环境验证结论
- 生产 ingress 验证结论
- 容量承诺数字

---

## 七、未来展望（v1.1 及以后）

### 7.1 运维能力增强

**长稳测试**：
- 7×24 长稳测试报告
- 稳定性验证

**API 版本兼容**：
- API 版本兼容策略
- 向后兼容保证

### 7.2 文档与白皮书

**产品白皮书**：
- 产品价值主张
- 架构优势
- 应用场景

**架构白皮书**：
- 技术架构详解
- 设计决策说明
- 最佳实践

### 7.3 平台能力开放

**多业务平台能力开放机制**：
- SDK 与开发工具
- 插件规范
- 新业务接入流程
- 第三方开发支持

### 7.4 功能增强

**呼叫轨迹查询**：
- 按 Call-ID 查 SIP 消息轨迹
- 投诉追溯与反诈举证

**严格零呼损滚动升级**：
- 在途呼叫迁移
- 无缝升级

**更多 AS 类型接入**：
- 基于平台快速接入新业务
- 丰富 AS 类型库

### 7.5 容量与性能

**容量裁决**：
- O1 容量目标裁决
- 真实 socket 压测
- 容量数字发布

**性能优化**：
- 持续性能优化
- 资源利用率提升

---

## 附录：关键术语

| 术语 | 说明 |
|------|------|
| **AS** | Application Server，应用服务器 |
| **IMS** | IP Multimedia Subsystem，IP 多媒体子系统 |
| **ISC** | IMS Service Control，IMS 业务控制接口 |
| **S-CSCF** | Serving Call Session Control Function，服务呼叫会话控制功能 |
| **S-SBC** | Session Border Controller，会话边界控制器 |
| **HSS** | Home Subscriber Server，归属用户服务器 |
| **iFC** | Initial Filter Criteria，初始过滤规则 |
| **B2BUA** | Back-to-Back User Agent，背靠背用户代理 |
| **TDD** | Test-Driven Development，测试驱动开发 |
| **ADR** | Architecture Decision Record，架构决策记录 |
| **ISSU** | In-Service Software Upgrade，在线软件升级 |
| **on-premises** | 本地部署，部署在客户机房 |

---

## 附录：参考文档

- `AGENT.md`：项目协作守则
- `README.md`：项目入口
- `docs/product-packaging-plan.md`：产品化包装计划
- `docs/architecture/新系统整体架构.md`：设计基线
- `docs/architecture/adr/`：架构决策记录（26+ 篇）
- `docs/requirements/prd.md`：产品需求文档
- `docs/plan.md`：里程碑与未决项
- `docs/product/`：产品文档目录
- `docs/operations/`：运维文档目录
- `docs/delivery/`：交付文档目录

---

**文档版本**：v1.0  
**最后更新**：2026-10-13  
**状态**：参考材料，用于指导 PPT 制作
