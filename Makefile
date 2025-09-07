.PHONY: install format lint clean

install:
	uv sync
	pre-commit install

lint:
	uv run ruff check ./src/*
	poetry run pyupgrade --py311-plus $(find . -name '*.py' -not -path './.venv/*')

mypy:
	uv run mypy ./src/*

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

tests:
	uv run pytest
