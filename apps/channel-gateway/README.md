# apps/channel-gateway

P0 用 `POST /dev/ingest` 模拟企微入站，不引入官方 SDK。

```bash
cd apps/channel-gateway
API_BASE_URL=http://localhost:8080 go run ./cmd/server
```

```bash
curl -sS -X POST http://localhost:8081/dev/ingest \
  -H 'Content-Type: application/json' \
  -d '{"tenantId":"dev-tenant","botId":"bot-quote","userId":"wx-user-1","text":"YJLV 3x95 报价","externalMsgId":"msg-001"}'
```

同一 `externalMsgId` 不会重复创建 Mission（API 侧幂等）。
