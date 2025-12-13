.PHONY: install install-dev ruff run

install:
	uv sync --no-dev

install-dev:
	uv sync

ruff:
	uvx ruff check --select I --fix
	uvx ruff format

run:
	uv run ./src/toddle_ops/main.py
