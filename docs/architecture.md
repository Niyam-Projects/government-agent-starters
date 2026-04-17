# Architecture

## Open Core Model

This repository follows an **open core** architecture. The open-source component provides the agent SDK, starter agents, and a slim local runner. The closed-source **Niyam AI Orchestration Layer (AIOL)** provides the security and operation layers for production deployment.

```
┌───────────────────────────────────────┐
│        Open Source (this repo)         │
│                                       │
│  SDK Layer (niyam.sdk)                │
│  ├─ AgentBase, AgentInput, AgentOutput│
│  └─ ModelBackend, Connector protocols │
│                                       │
│  Agent Layer (agents/)                │
│  ├─ requirements_architect_agent      │
│  ├─ secure_code_agent                 │
│  ├─ compliance_audit_agent            │
│  ├─ program_support_agent             │
│  └─ finops_review_agent               │
│                                       │
│  Testing Layer (niyam.testing)        │
│  ├─ MockBackend                       │
│  ├─ MockConnector                     │
│  └─ FileConnector                     │
│                                       │
│  Local Runner (niyam.runner)          │
│  ├─ Slim CLI                          │
│  ├─ Agent discovery                   │
│  └─ Minimal config                    │
└───────────────┬───────────────────────┘
                │
        SDK contract boundary
        (agents only depend on niyam.sdk)
                │
┌───────────────▼───────────────────────┐
│  Niyam AIOL — AI Orchestration Layer  │
│            (closed source)             │
│                                       │
│  Security Layer                       │
│  ├─ Access control and policy         │
│  ├─ Prompt security and guardrails    │
│  ├─ Data protection and encryption    │
│  ├─ Audit and compliance              │
│  └─ Secrets and credential mgmt       │
│                                       │
│  Operation Layer                      │
│  ├─ Model orchestration               │
│  ├─ Enterprise integrations           │
│  ├─ Workflow engine                   │
│  ├─ Observability                     │
│  └─ Deployment management             │
│                                       │
│  Production Runtime                   │
│  ├─ Full CLI, API, and Web UI         │
│  └─ Environment management             │
└───────────────────────────────────────┘
```

## SDK Layer (`niyam.sdk`)

The SDK defines the **stable contract** between agents and the AIOL.

### `AgentBase`

Every agent extends this abstract base class:

- `name`, `version`, `description` — agent metadata.
- `validate_input(agent_input)` — optional input validation.
- `_run(agent_input, model_backend)` — core logic (abstract, must implement).
- `run(agent_input, model_backend)` — public entry point with error handling.

### `AgentInput` / `AgentOutput`

Pydantic models that enforce consistent data envelopes:

- `AgentInput`: `payload` (dict) + `metadata` (dict).
- `AgentOutput`: `agent_name`, `status`, `result`, `errors`, `timestamp`.

### `ModelBackend` / `Connector`

Abstract base classes defining the protocols that the AIOL implements:

- `ModelBackend.generate(prompt, **kwargs) -> str`
- `Connector.fetch(query, **kwargs) -> dict`

Agents call these methods without knowing the underlying implementation.

## Testing Layer (`niyam.testing`)

Mock implementations for offline development:

| Class | Purpose |
|-------|---------|
| `MockBackend` | Returns deterministic responses with prompt length metadata |
| `MockConnector` | Returns sample data from fixtures |
| `FileConnector` | Reads data from local JSON files |

These are the **only** backend/connector implementations in the open-source repo.

## Local Runner (`niyam.runner`)

A minimal, offline CLI for agent development:

- **Discovery**: scans `agents/` for `AgentBase` subclasses.
- **Execution**: runs agents with `MockBackend` only.
- **Config**: reads `NIYAM_LOG_LEVEL` and `NIYAM_OUTPUT_DIR` from `.env`.

The runner is intentionally limited. It has no model selection, no enterprise connectors, no workflow chaining. It exists solely to give agent authors a fast feedback loop.

## Design Decisions

### Why open core?

- **Security must be closed.** Publishing security implementations gives adversaries a roadmap. Government deployments require hardened, non-inspectable controls.
- Agents are the primary contribution surface — they don't need AIOL access.
- Clear interface boundary makes contributions well-scoped and reviewable.
- Enterprise IP stays protected.
- Adopters get value immediately from the SDK and starter agents.

### Why uv?

- 10–100x faster than pip for dependency resolution.
- Built by the Astral team (same as ruff) with strong ecosystem adoption.
- Simpler than Poetry for contributors.

### Why Pydantic for I/O contracts?

- Runtime validation of agent inputs and outputs.
- Automatic JSON serialization for audit trails.
- Type-safe field definitions with clear error messages.

### Why Jinja2 for prompts?

- Battle-tested template engine with clear syntax.
- Templates are plain text files — easy to version and review.
- No vendor lock-in on prompt format.

## Extension Points

| What | How | Where |
|------|-----|-------|
| Add a new agent | Extend `AgentBase`, implement `_run()` | `agents/` (open) |
| Add a security policy | Configure via AIOL security administration | AIOL Security Layer (closed) |
| Add a model backend | Implement `ModelBackend` protocol | AIOL Operation Layer (closed) |
| Add a connector | Implement `Connector` protocol | AIOL Operation Layer (closed) |
| Add a CLI command | Add to local runner for dev features | `niyam.runner.cli` (open) |
| Add a workflow | Chain agents via the orchestration engine | AIOL Operation Layer (closed) |
