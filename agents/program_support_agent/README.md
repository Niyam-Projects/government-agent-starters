# Program Support Agent

Generates program management artifacts — status reports, risk registers, milestone summaries, and stakeholder communications — from structured project data.

> When run through the open-source `niyam` CLI, this agent uses the offline `MockBackend`. Local runs validate prompt wiring and output shape, but they do not generate polished production-ready artifacts.

## Use Case

Government programs require frequent, structured reporting across multiple audiences. This agent accelerates the creation of routine program artifacts, allowing program managers to focus on decision-making rather than document formatting.

## Input

| Field           | Type   | Required | Description                                         |
|-----------------|--------|----------|-----------------------------------------------------|
| `project_data`  | string | yes      | Structured or unstructured project status data      |
| `artifact_type` | string | yes      | Type of artifact to generate (see config.yaml)      |
| `audience`      | string | no       | Target audience (default: "stakeholders")           |

## Output

| Field                | Type   | Description                          |
|----------------------|--------|--------------------------------------|
| `generated_artifact` | string | Model-generated program artifact     |
| `artifact_type`      | string | Type of artifact that was generated  |
| `model_used`         | string | Name of the model backend used       |

## Example

```bash
niyam run program_support_agent \
  --input agents/program_support_agent/examples/input.json
```

## Extending

- Edit `prompt.md` to customize artifact formats.
- Add new artifact types in `config.yaml`.
- Connect to project management tools via custom connectors.
