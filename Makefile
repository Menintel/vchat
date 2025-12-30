# Makefile for VChat monorepo

.PHONY: install dev dev-web dev-api backend-venv backend-run format lint start livekit

install:
	pnpm install

dev:
	pnpm --filter ./apps/web dev

dev-web:
	pnpm --filter ./apps/web dev

dev-api:
	cd apps/backend && uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

build:
	pnpm --filter ./apps/web build

preview:
	pnpm --filter ./apps/web preview

typecheck:
	pnpm --filter ./apps/web vue-tsc --noEmit

backend-venv:
	python -m venv .venv
	@echo "Activate the venv:"
	@echo "  Windows: .\\.venv\\Scripts\\activate"
	@echo "  Unix: source .venv/bin/activate"
	@echo "Then run: pip install -r apps/backend/requirements.txt"

format:
	pnpm -w -r run format

lint:
	pnpm -w -r run lint

livekit:
	docker compose -f infra/livekit/docker-compose.yml up

# Run frontend
start:
	$(MAKE) dev
