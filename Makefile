# Agent Factory local commands (does not replace AI Hunter scripts)

.PHONY: factory-test factory-api factory-gateway factory-console factory-smoke factory-middleware

factory-test:
	cd apps/api && go test ./...

factory-api:
	cd apps/api && go run ./cmd/server

factory-gateway:
	cd apps/channel-gateway && go run ./cmd/server

factory-console:
	cd apps/console && npm install && npm run dev

factory-smoke:
	bash scripts/smoke-mission.sh
	bash scripts/smoke-ingest.sh

factory-middleware:
	docker compose -f deploy/compose/docker-compose.yml --env-file deploy/compose/.env.example up -d
