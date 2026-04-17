#!/usr/bin/env bash
# Quick setup script for new contributors.
# Usage: bash scripts/setup.sh

set -euo pipefail

echo "==> Niyam Agent Starters — Setup"

# Check Python version
if ! command -v python3 &>/dev/null; then
    echo "ERROR: python3 is required. Install Python 3.11+ first."
    exit 1
fi

PYTHON_VERSION=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
echo "    Python version: $PYTHON_VERSION"

# Install uv if not present
if ! command -v uv &>/dev/null; then
    echo "==> Installing uv..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    export PATH="$HOME/.cargo/bin:$PATH"
fi

echo "    uv version: $(uv --version)"

# Install dependencies
echo "==> Installing dependencies..."
uv pip install -e ".[dev]"

# Set up pre-commit hooks
echo "==> Installing pre-commit hooks..."
pre-commit install

# Copy .env if it doesn't exist
if [ ! -f .env ]; then
    echo "==> Copying .env.example → .env"
    cp .env.example .env
fi

echo ""
echo "==> Setup complete!"
echo ""
echo "    This is the local development runner (mock backend only)."
echo "    For production security and model inference, deploy agents via the Niyam AIOL."
echo ""
echo "    Try these commands:"
echo "      niyam list-agents"
echo "      niyam run requirements_architect_agent --input agents/requirements_architect_agent/examples/input.json"
echo "      make test"
echo ""
