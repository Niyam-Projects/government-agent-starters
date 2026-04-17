#!/usr/bin/env bash
# Run all quality checks.
# Usage: bash scripts/lint.sh

set -euo pipefail

echo "==> Ruff lint..."
ruff check src agents tests

echo "==> Ruff format check..."
ruff format --check src agents tests

echo "==> Mypy..."
mypy src/niyam agents

echo "==> All checks passed."
