# Compliance Audit Agent

Evaluates project artifacts against compliance frameworks (NIST 800-53, FedRAMP, SOC 2, etc.) and produces structured gap analyses.

> When run through the open-source `niyam` CLI, this agent uses the offline `MockBackend`. Local runs validate prompt wiring and output shape, but they do not perform a real compliance assessment.

## Use Case

Government systems must demonstrate compliance against one or more security and governance frameworks. This agent accelerates the initial assessment by analyzing documentation, configurations, or architecture descriptions against a target framework.

## Input

| Field       | Type     | Required | Description                                |
|-------------|----------|----------|--------------------------------------------|
| `artifact`  | string   | yes      | Text of the artifact to evaluate           |
| `framework` | string   | yes      | Compliance framework (e.g., "NIST 800-53") |
| `controls`  | string[] | no       | Specific controls to focus on              |

## Output

| Field                 | Type   | Description                            |
|-----------------------|--------|----------------------------------------|
| `compliance_analysis` | string | Model-generated compliance assessment  |
| `framework`           | string | Framework evaluated against            |
| `model_used`          | string | Name of the model backend used         |

## Example

```bash
niyam run compliance_audit_agent \
  --input agents/compliance_audit_agent/examples/input.json
```

## Extending

- Edit `prompt.md` to add framework-specific evaluation criteria.
- Add custom control mappings in `config.yaml`.
- Chain with `secure_code_agent` for code-level compliance checks.
