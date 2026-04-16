# Deployment Guide

## Local Development (This Repo)

The local runner requires no external services. Clone, install, and run.

```bash
git clone https://github.com/Niyam-Projects/government-agent-starters.git
cd government-agent-starters
pip install uv
uv pip install -e ".[dev]"
cp .env.example .env
niyam list-agents
```

The local runner uses the `MockBackend` — all operations are offline and deterministic.

## Docker (Local)

```bash
# Build
docker build -t niyam-agent-starters:local .

# Run
docker run --rm niyam-agent-starters:local \
  run requirements_architect_agent \
  --payload '{"requirements_text": "The system must support MFA."}'
```

## VS Code Dev Container

Open the repository in VS Code and select **Reopen in Container**. The dev container includes Python 3.12, uv, and all development dependencies.

## Production Deployment

Production deployment is handled by the **Niyam AI Orchestration Layer (AIOL)** (closed source). The AIOL provides security enforcement, production model backends, enterprise integrations, and operational infrastructure.

### How Agents Move from Local to Production

```
Local Development          →  AIOL Staging               →  AIOL Production
─────────────────             ──────────────────           ────────────────────
MockBackend                   Production backends          Production backends
MockConnector                 Enterprise integrations      Enterprise integrations
No security                   Security enforced            Full security stack
CLI output                    Audit + monitoring           Full operational stack
```

The agent code is identical across all environments. Only the injected backends, connectors, and security policies change.

### Preparing Agents for the AIOL

1. Ensure your agent only imports from `niyam.sdk`.
2. Validate all inputs in `validate_input()`.
3. Return structured data from `_run()` (no side effects).
4. Keep prompt templates parameterized (no hardcoded values).
5. Do not log or print sensitive payload fields.
6. Test thoroughly with `MockBackend` — the interface is identical.
7. Document input/output contracts in the agent's README.

See [platform-integration.md](platform-integration.md) for the full integration contract.
