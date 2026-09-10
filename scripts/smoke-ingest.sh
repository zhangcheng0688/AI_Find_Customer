#!/usr/bin/env bash
set -euo pipefail
GW="${GATEWAY_BASE_URL:-http://localhost:8081}"
TENANT="${DEV_TENANT_ID:-dev-tenant}"
MSG="smoke-${RANDOM}"

echo "== ingest =="
curl -sfS -X POST "${GW}/dev/ingest" -H "Content-Type: application/json" \
  -d "{\"tenantId\":\"${TENANT}\",\"botId\":\"bot-quote\",\"userId\":\"wx-1\",\"text\":\"YJLV 3x95 报价\",\"externalMsgId\":\"${MSG}\"}"
echo
echo "== ingest idempotent =="
curl -sfS -X POST "${GW}/dev/ingest" -H "Content-Type: application/json" \
  -d "{\"tenantId\":\"${TENANT}\",\"botId\":\"bot-quote\",\"userId\":\"wx-1\",\"text\":\"YJLV 3x95 报价\",\"externalMsgId\":\"${MSG}\"}"
echo
echo "smoke-ingest OK"
