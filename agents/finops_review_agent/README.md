# FinOps Review Agent

Analyzes cloud spending data and produces optimization recommendations aligned with FinOps Foundation best practices.

> When run through the open-source `niyam` CLI, this agent uses the offline `MockBackend`. Local runs validate prompt wiring and output shape, but they do not perform real spend analysis.

## Use Case

Cloud cost management is a critical concern for government programs operating under fixed budgets. This agent analyzes spending data and produces actionable recommendations for rightsizing, reserved capacity, and waste elimination.

## Input

| Field            | Type   | Required | Description                                    |
|------------------|--------|----------|------------------------------------------------|
| `spend_data`     | string | yes      | Cloud spending data (structured or narrative)  |
| `period`         | string | no       | Reporting period (default: "monthly")          |
| `cloud_provider` | string | no       | Cloud provider (default: "generic")            |

## Output

| Field             | Type   | Description                              |
|-------------------|--------|------------------------------------------|
| `finops_analysis` | string | Model-generated cost analysis            |
| `period`          | string | Period that was analyzed                  |
| `cloud_provider`  | string | Cloud provider context                   |
| `model_used`      | string | Name of the model backend used           |

## Example

```bash
niyam run finops_review_agent \
  --input agents/finops_review_agent/examples/input.json
```

## Extending

- Edit `prompt.md` to adjust analysis criteria.
- Add provider-specific optimization rules in `config.yaml`.
- Connect to cloud billing APIs via custom connectors.
