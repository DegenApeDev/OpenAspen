.PHONY: install test lint format clean docs run-example run-server help

help:
	@echo "OpenAspen Development Commands"
	@echo "=============================="
	@echo "install       Install dependencies with Poetry"
	@echo "test          Run test suite with coverage"
	@echo "lint          Run linters (ruff, mypy)"
	@echo "format        Format code with black and ruff"
	@echo "clean         Remove build artifacts and cache"
	@echo "docs          Build documentation"
	@echo "run-example   Run basic example"
	@echo "run-server    Start API server"
	@echo "pre-commit    Install pre-commit hooks"

install:
	poetry install

test:
	poetry run pytest --cov=openaspen --cov-report=term-missing --cov-report=html

test-fast:
	poetry run pytest -x

lint:
	poetry run ruff check openaspen tests
	poetry run mypy openaspen

format:
	poetry run black openaspen tests examples
	poetry run ruff check --fix openaspen tests

clean:
	rm -rf .pytest_cache
	rm -rf .mypy_cache
	rm -rf .ruff_cache
	rm -rf htmlcov
	rm -rf dist
	rm -rf build
	rm -rf *.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf chroma_db

docs:
	@echo "Documentation available in docs/"
	@echo "README.md - Main documentation"
	@echo "docs/ARCHITECTURE.md - Architecture guide"
	@echo "docs/QUICKSTART.md - Quick start guide"

run-example:
	poetry run python examples/basic_tree.py

run-server:
	poetry run python examples/server_example.py

pre-commit:
	poetry run pre-commit install

publish:
	poetry build
	poetry publish

dev:
	poetry install
	poetry run pre-commit install
	@echo "Development environment ready!"
