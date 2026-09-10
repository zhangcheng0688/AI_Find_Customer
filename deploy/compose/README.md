# deploy/compose

核心中间件：**Postgres 16 · Redis 7 · MinIO**。

## 端口

| 服务 | 端口 | 说明 |
|------|------|------|
| Postgres | 5432 | 用户/库 `factory` / 密码见 `.env` |
| Redis | 6379 | 限流/幂等预留 |
| MinIO API | 9000 | 文档对象存储 |
| MinIO Console | 9001 | 账号 `factory` |
| API（profile `app`） | 8080 | 产品壳 + Mission |
| Gateway（profile `app`） | 8081 | `POST /dev/ingest` |
| Console（profile `app`） | 5173 | 任务台 |

## 启动

```bash
cp deploy/compose/.env.example deploy/compose/.env
docker compose -f deploy/compose/docker-compose.yml --env-file deploy/compose/.env up -d
docker compose -f deploy/compose/docker-compose.yml ps
```

无 Docker 时：API 自动用 SQLite（`apps/api/data/api.db`），仍可跑通 Day 1–3。

应用容器：

```bash
docker compose -f deploy/compose/docker-compose.yml --env-file deploy/compose/.env --profile app up -d --build
```

## Coze Studio / RAGFlow / Activepieces

**不阻塞 P0。** 三者镜像重、版本组合多，默认不随 `up -d` 启动。

| 引擎 | 7 天策略 | 后续 |
|------|----------|------|
| Coze Studio | 先走 API 内 mock orchestrator | 按其官方 compose 单独拉起，壳映射 workspace |
| RAGFlow | mock 引用 | 官方镜像 + 租户 dataset 前缀 |
| Activepieces | 催办先用 API 内置 chaser | 只准 MIT 核心，**禁用 `packages/ee`** |

P1 再启引擎时开 issue 钉版本，不要把未验证的巨型 stack 写进默认 compose。
