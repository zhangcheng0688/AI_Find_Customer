# Agent 工厂 — 文档索引

可白标的 **组织级 Agent 工厂**（SaaS 多租户优先）。

**架构一句话：** 编排大脑 = Coze Studio；主动与长程 = 自研任务引擎 + Activepieces（MIT 核心）；知识 = RAGFlow；入口 = 企微/飞书 + `channel-gateway`。

**API 已锁定：** Go + Gin（理由见仓库根 `README.md`）。

## 本地怎么跑

P0 当前只完成目录与文档（Prompt-0）。中间件 Compose 在 **P0-2 / Prompt-1**，尚未落文件。

预期顺序（Prompt-1 之后）：

1. `docker compose -f deploy/compose/docker-compose.yml up -d` — Postgres / Redis / MinIO
2. 启动 `apps/api`
3. 启动 `apps/channel-gateway`
4. 启动 `apps/console`

端口与 `.env.example` 以 Prompt-1 交付为准。

## 文档

| 文件 | 说明 |
|------|------|
| [项目简报.md](./项目简报.md) | 给 Agent 的长期上下文 |
| [PRD与技术栈.md](./PRD与技术栈.md) | 权威 PRD v1.1 |
| [P0任务清单.md](./P0任务清单.md) | P0 完成标准 |
| [license-compliance.md](./license-compliance.md) | 允许 / 禁止依赖 |
| [wecom-setup.md](./wecom-setup.md) | 企微（P1，本文仅占位） |
| [runbook.md](./runbook.md) | 运行手册（后续填充） |

## License 红线

禁止 Dify / n8n / FastGPT / MaxKB 作为可白标多租户内核。Activepieces **禁用** `packages/ee`。
