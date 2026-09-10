# License 合规清单

权威需求见 [`PRD与技术栈.md`](./PRD与技术栈.md) v1.1。商务决策前请法务按各上游仓库**默认分支**复核。

## 原则

- 底座优先 **Apache 2.0 / MIT**。
- 产品壳（租户 / 白标 / 配额 / Bot / 模板 / 审计 / **任务引擎**）自研、可开源交付。
- 保留上游 NOTICE；不冒用 Coze / 字节等商标。

## 允许（一期默认路径）

| 组件 | 协议 | 用途 | 约束 |
|------|------|------|------|
| Coze Studio | Apache 2.0 | 编排底座（Agent / 可视化工作流） | 开源版缺完整企业多租户/SSO/集群 → 能力放产品壳 |
| RAGFlow | Apache 2.0 | 知识底座 | 按租户隔离 dataset / 前缀 |
| Activepieces | MIT **核心** | 定时 / Webhook / 同步 | **禁止**引入或依赖 `packages/ee` 及任何 EE 专有包 |
| PostgreSQL / Redis / MinIO | OSI 许可 | 数据 / 缓存 / 对象存储 | — |
| Gin | MIT | `apps/api` HTTP | 已锁定，见根 README |

## 禁止（不可作为可白标多租户内核）

| 组件 | 原因 |
|------|------|
| **Dify** | 禁对外多租户；前端禁去 Logo |
| **n8n** | Sustainable Use：禁白标 / 有偿转售托管 |
| **FastGPT** | 类 Dify 附加条款 |
| **MaxKB** | GPL-3.0，闭源白标 / 分发风险高 |

引入上述组件作为「工厂内核」视为 **P0 合规事故**。

## 明确不替代

| 组件 | 本项目定位 |
|------|------------|
| OpenClaw 等个人 Agent 运行时 | 可选通道参考；**不替代** Coze（编排）或自研任务引擎（主动长程） |
| Bisheng | Apache 2.0，仅私有化 / 信创备选线，**不进** SaaS 一期默认路径 |

## Activepieces EE 红线

- 只使用社区版 MIT 核心。
- 不得复制、依赖、或「悄悄打开」`packages/ee`。
- 催办 / 升级等组织级长程能力以 **壳内任务引擎** 为准，Activepieces 只做触发与同步。
