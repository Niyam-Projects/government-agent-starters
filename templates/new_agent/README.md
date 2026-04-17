# New Agent

<!-- TODO: Replace with your agent's description -->

Short description of what this agent does.

## Use Case

Explain the problem this agent solves and who benefits from it.

## Input

| Field        | Type   | Required | Description              |
|--------------|--------|----------|--------------------------|
| `input_text` | string | yes      | Text input to analyze    |

## Output

| Field    | Type   | Description                     |
|----------|--------|---------------------------------|
| `result` | string | Model-generated analysis        |

## Example

```bash
niyam run new_agent --input agents/new_agent/examples/input.json
```

## Extending

- Edit `prompt.md` to customize the analysis.
- Edit `config.yaml` for agent-specific settings.
