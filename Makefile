.PHONY: install format lint clean test pytest mypy

install:
	uv sync
	pre-commit install

lint:
	uv run ruff check ./src/*
	uv run pyupgrade --py313-plus $(find . -name '*.py' -not -path './.venv/*')

mypy:
	uv run mypy ./src/*

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

test:
	uv run pytest

pytest:
	uv run pytest
