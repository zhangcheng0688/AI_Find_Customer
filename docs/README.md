# Agent 工厂 — 文档索引

**你的白标 Agent：** 扣子 Coze Studio + RAGFlow + 自研 UI。口径：[`北极星.md`](./北极星.md)。

**不是电缆项目。** PRD v1.1 只作 License / 引擎约束。

**API 已锁定：** Go + Gin（理由见仓库根 `README.md`）。

## 本地怎么跑

无 Docker（SQLite 演示）：

```bash
make factory-test
make factory-api          # :8080
make factory-gateway      # :8081
make factory-console      # :5173
```

有 Docker：

```bash
cp deploy/compose/.env.example deploy/compose/.env
make factory-middleware   # Postgres 5432 / Redis 6379 / MinIO 9000
# 然后 DATABASE_URL=postgres://factory:factory@127.0.0.1:5432/factory?sslmode=disable make factory-api
```

7 天计划：[`7day-launch-plan.md`](./7day-launch-plan.md)。端口见 [`../deploy/compose/README.md`](../deploy/compose/README.md)。

## 文档

| 文件 | 说明 |
|------|------|
| [项目简报.md](./项目简报.md) | 给 Agent 的长期上下文 |
| [PRD与技术栈.md](./PRD与技术栈.md) | 权威 PRD v1.1 |
| [P0任务清单.md](./P0任务清单.md) | P0 完成标准 |
| [北极星.md](./北极星.md) | 产品定义（扣子 + RAGFlow + 自研 UI） |
| [7day-launch-plan.md](./7day-launch-plan.md) | 7 天上线（纠正版） |
| [p1-ready.md](./p1-ready.md) | 真企微 / Coze / RAGFlow 环境变量 |
| [p0-acceptance.md](./p0-acceptance.md) | P0 验收记录 |
| [runbook.md](./runbook.md) | 运行手册（后续填充） |

## License 红线

禁止 Dify / n8n / FastGPT / MaxKB 作为可白标多租户内核。Activepieces **禁用** `packages/ee`。
