# Niyam AIOL Integration

This document describes how agents built with the open-source SDK integrate with the closed-source **Niyam AI Orchestration Layer (AIOL)**.

## The Contract

The integration boundary is the `niyam.sdk` module. Agents depend **only** on:

```python
from niyam.sdk import AgentBase, AgentInput, AgentOutput
```

The AIOL provides implementations of the `ModelBackend` and `Connector` protocols defined in `niyam.sdk.protocols`. Agents never import these implementations directly — they receive them via dependency injection at runtime.

## How the AIOL Loads Agents

```
1. AIOL scans agents/ directory (or a configured agent registry)
2. Imports each agent module, discovers subclasses of AgentBase
3. Registers them by their `name` attribute
4. At execution time:
   a. AIOL enforces security policies
   b. AIOL selects the appropriate ModelBackend and Connector
   c. AIOL calls agent.run(agent_input, model_backend)
   d. AIOL captures the AgentOutput
```

## What the AIOL Provides

The AIOL injects production implementations at runtime. Agents interact with them through the same `ModelBackend` and `Connector` interfaces used locally with mocks.

| Category | What agents get |
|---|---|
| **Security** | Access control, prompt safety, data protection, audit — enforced transparently |
| **Model backends** | Production model inference with orchestration and management |
| **Connectors** | Enterprise data source integrations with credential management |
| **Workflows** | Multi-agent chaining and orchestration |
| **Observability** | Logging, metrics, and monitoring |
| **Deployment** | Environment management and production runtime |

> Specific implementations, supported providers, and architecture details are available under NDA from the Niyam team.

## Agent Author Requirements

To ensure your agent works on the AIOL:

1. **Extend `AgentBase`** — this is the only required base class.
2. **Set `name` as a class attribute** — must match the directory name.
3. **Implement `_run()`** — receives `AgentInput` and a `ModelBackend`.
4. **Use `model_backend.generate(prompt)`** — never import or instantiate backends directly.
5. **Return a `dict`** from `_run()` — the framework wraps it in `AgentOutput`.
6. **Validate input** via `validate_input()` — return a list of error strings.
7. **Keep prompts in `prompt.md`** — the AIOL indexes these for management.
8. **Keep config in `config.yaml`** — the AIOL can override values per environment.

## What NOT to Do

- Do not import from `niyam.runner` — that's the local dev runner, not the AIOL.
- Do not import from `niyam.testing` in production code — those are mock implementations.
- Do not make network calls directly — use the `Connector` protocol.
- Do not hardcode model names — the AIOL manages model selection.
- Do not write to the filesystem — use `AgentOutput` as the sole return channel.
- Do not log sensitive data — the AIOL handles audit logging.

## Local Development vs. AIOL

| Aspect | Local (this repo) | Niyam AIOL |
|--------|-------------------|------------|
| Security | None | Production security controls |
| Model backend | `MockBackend` (offline) | Production model backends |
| Connectors | `MockConnector` (sample data) | Enterprise integrations |
| Agent discovery | Filesystem scan | Managed registry |
| Execution | Single agent, CLI | Workflows, chaining, scheduling |
| Output | JSON to stdout/file | Secured, audited output |
| Auth | None | Production access control |

## Testing Against the AIOL

The AIOL provides a compatibility test suite for validating agents:

```bash
# Run from the AIOL (not available in this repo)
niyam-aiol test-agent agents/my_agent/
```

For local development, the open-source test suite with `MockBackend` is sufficient to validate your agent's logic, input validation, and output structure.
