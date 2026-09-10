#!/usr/bin/env bash
set -euo pipefail
GW="${GATEWAY_BASE_URL:-http://localhost:8081}"
TENANT="${DEV_TENANT_ID:-dev-tenant}"
MSG="smoke-${RANDOM}"

echo "== ingest =="
curl -sfS -X POST "${GW}/dev/ingest" -H "Content-Type: application/json" \
  -d "{\"tenantId\":\"${TENANT}\",\"botId\":\"demo-agent\",\"userId\":\"builder\",\"text\":\"你好，介绍一下你能做什么\",\"externalMsgId\":\"${MSG}\"}"
echo
echo "== ingest idempotent =="
curl -sfS -X POST "${GW}/dev/ingest" -H "Content-Type: application/json" \
  -d "{\"tenantId\":\"${TENANT}\",\"botId\":\"demo-agent\",\"userId\":\"builder\",\"text\":\"你好，介绍一下你能做什么\",\"externalMsgId\":\"${MSG}\"}"
echo
echo "smoke-ingest OK"
