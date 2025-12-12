.PHONY: install install-dev ruff run docker-build docker-run docker-stop docker-logs docker-clean

install:
	uv sync --no-dev

install-dev:
	uv sync

ruff:
	uvx ruff check --select I --fix
	uvx ruff format

run:
	adk web src/toddle_ops/agents

# Docker commands
docker-build:
	docker compose build

docker-run:
	docker compose up -d

docker-stop:
	docker compose down

docker-logs:
	docker compose logs -f

docker-clean:
	docker compose down -v
	docker system prune -f

docker-rebuild:
	docker compose up -d --build
