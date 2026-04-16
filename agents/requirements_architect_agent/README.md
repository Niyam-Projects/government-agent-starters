# Requirements Architect Agent

Analyzes unstructured requirements text and produces structured, prioritized requirements with traceability metadata.

> When run through the open-source `niyam` CLI, this agent uses the offline `MockBackend`. Local runs validate prompt wiring and output shape, but they do not perform real model-backed requirements analysis.

## Use Case

Government and enterprise projects often begin with loosely written requirements documents. This agent transforms free-text requirements into structured, categorized artifacts suitable for tracking, traceability, and compliance review.

## Input

| Field               | Type   | Required | Description                        |
|---------------------|--------|----------|------------------------------------|
| `requirements_text` | string | yes      | Raw requirements text to analyze   |
| `context`           | string | no       | Additional project context         |

## Output

| Field                       | Type   | Description                              |
|-----------------------------|--------|------------------------------------------|
| `structured_requirements`   | string | Model-generated structured analysis      |
| `input_length`              | int    | Character count of input text            |
| `model_used`                | string | Name of the model backend used           |

## Example

```bash
niyam run requirements_architect_agent \
  --input agents/requirements_architect_agent/examples/input.json
```

## Extending

- Edit `prompt.md` to adjust the analysis strategy.
- Edit `config.yaml` to change categories or priority levels.
- Integrate a real backend through the Niyam AIOL when you need live model inference beyond the local mock runner.
