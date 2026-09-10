#!/usr/bin/env bash
set -euo pipefail
API="${API_BASE_URL:-http://localhost:8080}"
TENANT="${DEV_TENANT_ID:-dev-tenant}"

echo "== health =="
curl -sfS "${API}/health"
echo

echo "== create mission =="
CREATE=$(curl -sfS -X POST "${API}/tenants/${TENANT}/missions" \
  -H "X-Tenant-Id: ${TENANT}" -H "Content-Type: application/json" \
  -d '{"bot_id":"bot-quote","type":"inquiry","status":"open","assignee":"sales-owner"}')
echo "${CREATE}"
ID=$(python3 -c "import json,sys; print(json.loads(sys.argv[1])['data']['mission']['id'])" "${CREATE}")
echo "id=${ID}"

echo "== open -> running =="
curl -sfS -X PATCH "${API}/tenants/${TENANT}/missions/${ID}/status" \
  -H "X-Tenant-Id: ${TENANT}" -H "Content-Type: application/json" \
  -d '{"status":"running"}'
echo
echo "== running -> waiting =="
curl -sfS -X PATCH "${API}/tenants/${TENANT}/missions/${ID}/status" \
  -H "X-Tenant-Id: ${TENANT}" -H "Content-Type: application/json" \
  -d '{"status":"waiting"}'
echo
echo "== list =="
curl -sfS "${API}/tenants/${TENANT}/missions" -H "X-Tenant-Id: ${TENANT}"
echo
echo "== cancel =="
curl -sfS -X POST "${API}/tenants/${TENANT}/missions/${ID}/cancel" \
  -H "X-Tenant-Id: ${TENANT}" -H "Content-Type: application/json" \
  -d '{"reason":"smoke"}'
echo
echo "smoke-mission OK"
