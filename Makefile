# Makefile for VChat monorepo

.PHONY: install dev backend-venv backend-run format lint start

install:
	pnpm install

dev:
	pnpm --filter ./apps/frontend dev

build:
	pnpm --filter ./apps/frontend build

preview:
	pnpm --filter ./apps/frontend preview

backend-venv:
	python -m venv .venv
	@echo "Activate the venv:"
	@echo "  Windows: ".\\.venv\\Scripts\\activate"
	@echo "  Unix: source .venv/bin/activate"
	@echo "Then run: pip install -r apps/backend/requirements.txt"

backend-run:
	cd apps/backend && uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

format:
	pnpm -w -r run format

lint:
	pnpm -w -r run lint

# Run both (frontend + backend) in separate terminals; this command will run frontend here
start:
	$(MAKE) dev
