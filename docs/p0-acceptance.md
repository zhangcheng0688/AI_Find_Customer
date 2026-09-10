# P0 验收

对照 [`P0任务清单.md`](./P0任务清单.md)。日期：2026-09-10。

## 清单

| 项 | 状态 | 说明 |
|----|------|------|
| P0-1 仓库骨架 | 完成 | `apps/` `deploy/compose` `templates/` `docs/` + License 红线 |
| P0-2 Compose | 完成（文件） | Postgres/Redis/MinIO + 健康检查；本环境无 Docker daemon，未在此机 `compose up` |
| P0-3 Mission API | 完成 | `go test ./...` 通过；`scripts/smoke-mission.sh` 通过 |
| P0-4 渠道网关 | 完成 | `scripts/smoke-ingest.sh` 通过；同 `externalMsgId` 返回 `idempotent: true` |
| P0-5 控制台 | 完成 | `apps/console` `npm run build` 通过；dev 登录写死 |

## 本机 smoke（SQLite，无 Docker）

```
make factory-test     # ok  httpapi + mission
curl /health          # {"ok":true,"data":{"service":"api","db":"ok","tenant":"dev-tenant"}}
scripts/smoke-mission.sh  # create → running → waiting → cancel
scripts/smoke-ingest.sh   # 建任务 + 幂等
```

## 启动顺序

1. 中间件（可选）：`make factory-middleware`
2. `make factory-api`
3. `make factory-gateway`
4. `make factory-console`

下一步 P1 环境变量见 [`p1-ready.md`](./p1-ready.md)。7 天总计划见 [`7day-launch-plan.md`](./7day-launch-plan.md)。
