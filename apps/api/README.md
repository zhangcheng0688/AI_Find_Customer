# apps/api

Go + Gin 产品壳，含 **Mission 任务引擎** 与演示用催办 ticker。

```bash
cd apps/api
go test ./...
go run ./cmd/server
```

- 未设置 `DATABASE_URL` 时用 SQLite：`data/api.db`
- 健康检查：`GET http://localhost:8080/health`
- 租户头：`X-Tenant-Id` 必须与路径 `:tenantId` 一致
- 默认 seed：`dev-tenant`

演示催办：`DEMO_CHASE_AFTER=30s`（生产改为 `24h`）。
