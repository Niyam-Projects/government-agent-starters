.DEFAULT_GOAL := help
SHELL := /bin/bash

# ---------------------------------------------------------------------------
# Variables
# ---------------------------------------------------------------------------
PYTHON   ?= python3
UV       ?= uv
SRC_DIRS := src agents tests

# ---------------------------------------------------------------------------
# Help
# ---------------------------------------------------------------------------
.PHONY: help
help: ## Show this help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

# ---------------------------------------------------------------------------
# Setup
# ---------------------------------------------------------------------------
.PHONY: install
install: ## Install project and dev dependencies with uv
	$(UV) pip install -e ".[dev]"

.PHONY: install-hooks
install-hooks: ## Install pre-commit hooks
	pre-commit install

.PHONY: setup
setup: install install-hooks ## Full local setup (install + hooks)
	@echo "✓ Setup complete. Copy .env.example → .env if needed."

# ---------------------------------------------------------------------------
# Quality
# ---------------------------------------------------------------------------
.PHONY: lint
lint: ## Run ruff linter
	$(UV) run ruff check $(SRC_DIRS)

.PHONY: format
format: ## Run ruff formatter
	$(UV) run ruff format $(SRC_DIRS)

.PHONY: format-check
format-check: ## Check formatting without changes
	$(UV) run ruff format --check $(SRC_DIRS)

.PHONY: typecheck
typecheck: ## Run mypy type checking
	$(UV) run mypy src/niyam agents

.PHONY: check
check: lint format-check typecheck ## Run all quality checks

.PHONY: audit
audit: ## Run a dependency vulnerability audit
	XDG_CACHE_HOME=$(CURDIR)/.cache $(UV) run --with pip-audit pip-audit

# ---------------------------------------------------------------------------
# Test
# ---------------------------------------------------------------------------
.PHONY: test
test: ## Run tests
	$(UV) run pytest

.PHONY: test-cov
test-cov: ## Run tests with coverage
	$(UV) run pytest --cov=niyam --cov=agents --cov-report=term-missing --cov-report=html

.PHONY: test-fast
test-fast: ## Run tests excluding slow/integration
	$(UV) run pytest -m "not slow and not integration"

# ---------------------------------------------------------------------------
# Run (local runner — mock backend only)
# ---------------------------------------------------------------------------
.PHONY: cli
cli: ## Run the local CLI (pass ARGS= for commands, e.g. make cli ARGS="list-agents")
	$(UV) run niyam $(ARGS)

# ---------------------------------------------------------------------------
# Docker
# ---------------------------------------------------------------------------
.PHONY: docker-build
docker-build: ## Build Docker image
	docker build -t niyam-agent-starters:local .

.PHONY: docker-run
docker-run: ## Run CLI inside Docker (pass ARGS= for commands)
	docker run --rm --env-file .env niyam-agent-starters:local $(ARGS)

# ---------------------------------------------------------------------------
# Maintenance
# ---------------------------------------------------------------------------
.PHONY: clean
clean: ## Remove build artifacts and caches
	rm -rf dist build *.egg-info .pytest_cache .mypy_cache .ruff_cache htmlcov .coverage outputs
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
