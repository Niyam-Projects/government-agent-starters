# Adding a New Agent

This guide walks through creating a new agent from scratch.

## 1. Create the Agent Directory

```bash
cp -r templates/new_agent agents/my_agent
```

Or create the structure manually:

```
agents/my_agent/
├── __init__.py
├── agent.py
├── config.yaml
├── prompt.md
├── README.md
└── examples/
    ├── input.json
    └── output.json
```

## 2. Implement the Agent

Edit `agents/my_agent/agent.py`:

```python
from __future__ import annotations

from typing import Any

from jinja2 import Template

from niyam.sdk import AgentBase, AgentInput


class MyAgent(AgentBase):
    name = "my_agent"
    version = "0.1.0"
    description = "Short description of what this agent does."

    def validate_input(self, agent_input: AgentInput) -> list[str]:
        errors: list[str] = []
        if not agent_input.payload.get("required_field"):
            errors.append("'required_field' is required in payload.")
        return errors

    def _run(self, agent_input: AgentInput, model_backend: Any) -> dict[str, Any]:
        template = Template(self.prompt_template)
        prompt = template.render(**agent_input.payload)
        response = model_backend.generate(prompt)
        return {"result": response}
```

### Key requirements:

- **Import only from `niyam.sdk`** — never from `niyam.runner` or `niyam.testing` in agent code.
- **Extend `AgentBase`** and set `name`, `version`, `description` as class attributes.
- **Implement `_run()`** — this is where your agent logic goes.
- **Optionally override `validate_input()`** to enforce input requirements.
- **Use the model backend** via `model_backend.generate(prompt)` — never instantiate backends directly.
- **Keep `prompt.md` next to `agent.py`** — `AgentBase` loads it automatically from the agent directory.

## 3. Write the Prompt Template

Edit `agents/my_agent/prompt.md`:

```markdown
# My Agent — Prompt Template

You are an expert in [domain]. Analyze the following input.

## Input

{{ required_field }}

## Instructions

1. Do the first thing.
2. Do the second thing.
3. Return structured output.

## Output Format

Return a JSON object with:
- `field_a`: description
- `field_b`: description
```

Prompt templates use [Jinja2](https://jinja.palletsprojects.com/) syntax. Variables from `agent_input.payload` are available in the template context.

## 4. Add Configuration

Edit `agents/my_agent/config.yaml`:

```yaml
agent:
  name: my_agent
  version: "0.1.0"
  max_input_tokens: 8192
  output_format: json

# Add agent-specific settings here
custom_setting: value
```

## 5. Add Examples

Create `agents/my_agent/examples/input.json`:

```json
{
  "required_field": "Sample input data for the agent."
}
```

Create `agents/my_agent/examples/output.json` with the expected output structure.

## 6. Update `__init__.py`

```python
from agents.my_agent.agent import MyAgent

__all__ = ["MyAgent"]
```

## 7. Write Tests

Create `tests/test_agents/test_my_agent.py`:

```python
from agents.my_agent.agent import MyAgent
from niyam.sdk import AgentInput
from niyam.testing import MockBackend


def test_my_agent_validates_required_field():
    agent = MyAgent()
    result = agent.run(AgentInput(payload={}))
    assert result.status == "validation_error"


def test_my_agent_runs_with_mock():
    agent = MyAgent()
    result = agent.run(
        AgentInput(payload={"required_field": "test data"}),
        MockBackend(),
    )
    assert result.status == "success"
    assert "result" in result.result
```

## 8. Write the README

Document your agent's purpose, input/output schema, and usage examples in `agents/my_agent/README.md`.

## 9. Test It

```bash
# Verify it's discovered
niyam list-agents

# Run with example input
niyam run my_agent --input agents/my_agent/examples/input.json

# Run tests
make test
```

## Checklist

- [ ] `agent.py` extends `AgentBase` and implements `_run()`
- [ ] `name` class attribute matches the directory name
- [ ] `prompt.md` contains a Jinja2 prompt template
- [ ] `config.yaml` has agent metadata
- [ ] `__init__.py` exports the agent class
- [ ] `examples/input.json` and `examples/output.json` are present
- [ ] `README.md` documents the agent
- [ ] Tests pass (`make test`)
