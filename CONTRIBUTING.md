# Contributing to Niyam Agent Starters

Thank you for your interest in contributing. This repository uses an **open core** model — the agent SDK, starter agents, testing utilities, and local runner are open source. The Niyam AIOL, which provides production security and operations, is closed source.

This means the contribution surface is well-defined: **you contribute agents and SDK improvements, and the AIOL team handles the rest.**

## What You Can Contribute

| Area | Examples |
|------|----------|
| **New agents** (primary path) | Domain-specific agents for government/enterprise patterns |
| **Agent improvements** | Better prompts, validation, output structure |
| **SDK improvements** | `AgentBase`, `AgentInput`, `AgentOutput` enhancements (coordinated) |
| **Testing utilities** | New mock implementations, test helpers |
| **Local runner** | Developer experience improvements |
| **Documentation** | Guides, examples, architecture docs |
| **Bug fixes** | For any open-source component |
| **Test coverage** | More tests for agents and SDK |

## What Lives in the Niyam AIOL (Not Here)

- Security layer
- Production model backends
- Enterprise integrations
- Workflow/orchestration engine
- Production infrastructure (deployment, Web UI, observability)

## Getting Started

1. **Fork** the repository and clone your fork locally.
2. **Set up** your development environment:

   ```bash
   pip install uv
   uv pip install -e ".[dev]"
   pre-commit install
   ```

3. **Create a branch** for your work:

   ```bash
   git checkout -b feature/your-feature-name
   ```

## Development Workflow

### Running Tests

```bash
make test           # all tests
make test-fast      # skip slow/integration tests
make test-cov       # with coverage report
```

### Code Quality

```bash
make lint           # run ruff linter
make format         # auto-format with ruff
make typecheck      # run mypy
make audit          # dependency vulnerability audit
make check          # all of the above
```

Pre-commit hooks run automatically on `git commit`.

## Open-Source Submission Hygiene

Before opening a PR, make sure your contribution is safe to publish in a public repository.

Do not submit:

- Secrets, tokens, keys, certificates, `.env` files, or copied production config.
- Internal-only URLs, ticket links, architecture diagrams, screenshots, or runbooks.
- Customer, partner, agency, or employee data unless it is already public and necessary.
- Classified, CUI, export-controlled, PII, or other regulated/sensitive data.
- Prompt examples or model outputs copied from non-public systems without approval.

When examples are useful, sanitize them aggressively:

- Replace real names, IDs, hostnames, account numbers, and URLs with obvious placeholders.
- Keep sample payloads minimal and fictional.
- Prefer synthetic examples over redacted production artifacts.

## Adding a New Agent

This is the primary contribution path. See [docs/adding-agents.md](docs/adding-agents.md) for the full guide.

In short:

1. `cp -r templates/new_agent agents/my_agent`
2. Implement your agent in `agent.py` (extend `AgentBase`, implement `_run()`)
3. Write a prompt template in `prompt.md`
4. Add config, examples, README
5. Add tests in `tests/test_agents/`
6. Verify: `niyam run my_agent --payload '{"input_text": "test"}'`

### Agent Rules

- Agents must **only import from `niyam.sdk`** — never from `niyam.runner` or `niyam.testing` in production code.
- Use `model_backend.generate(prompt)` — never instantiate backends directly.
- Do not log or print sensitive payload fields.
- Return a `dict` from `_run()` — the framework wraps it in `AgentOutput`.
- Keep all prompts in `prompt.md` as Jinja2 templates.
- Keep config in `config.yaml` (YAML, not Python).
- Include `examples/input.json` and `examples/output.json`.

## Code Standards

- All Python code targets **Python 3.11+**.
- Use **type hints** for all function signatures.
- Follow the existing code style (enforced by ruff).
- Keep modules focused and small.
- Prefer composition over inheritance.

## Commit Messages

Use clear, descriptive commit messages:

```
Add compliance_audit_agent with NIST 800-53 support

- Implement ComplianceAuditAgent with gap analysis output
- Add prompt template for framework evaluation
- Include example input/output for NIST 800-53
```

## Pull Requests

- One logical change per PR.
- Include a clear description of **what** and **why**.
- Reference any related issues.
- Ensure all checks pass (`make check && make audit && make test`).
- Update documentation if your change affects user-facing behavior.
- Double-check that examples, screenshots, prompts, and fixtures do not expose non-public information.

## Reporting Issues

Use [GitHub Issues](https://github.com/Niyam-Projects/government-agent-starters/issues) with the provided templates.

## Security

If you discover a security vulnerability, **do not** open a public issue. See [SECURITY.md](SECURITY.md).

## Code of Conduct

All contributors must follow our [Code of Conduct](CODE_OF_CONDUCT.md).

## License

By contributing, you agree that your contributions will be licensed under the [Apache License 2.0](LICENSE).
