# Secure Code Agent

Reviews source code for security vulnerabilities, producing findings aligned with CWE and OWASP Top 10 classifications.

> When run through the open-source `niyam` CLI, this agent uses the offline `MockBackend`. Local runs validate prompt wiring and output shape, but they do not provide real security analysis.

## Use Case

Security review is a critical part of any government or enterprise software lifecycle. This agent automates initial code review to surface common vulnerabilities before human review, reducing turnaround time and improving coverage.

## Input

| Field          | Type     | Required | Description                                  |
|----------------|----------|----------|----------------------------------------------|
| `source_code`  | string   | yes      | Source code to review                        |
| `language`     | string   | no       | Programming language (default: python)       |
| `focus_areas`  | string[] | no       | Specific areas to prioritize                 |

## Output

| Field             | Type   | Description                                |
|-------------------|--------|--------------------------------------------|
| `security_review` | string | Model-generated security findings          |
| `lines_reviewed`  | int    | Number of lines in the input               |
| `language`        | string | Language that was reviewed                  |
| `model_used`      | string | Name of the model backend used             |

## Example

```bash
niyam run secure_code_agent \
  --input agents/secure_code_agent/examples/input.json
```

## Extending

- Edit `prompt.md` to adjust review criteria or output structure.
- Add language-specific review guidance in `config.yaml`.
- Chain with `compliance_audit_agent` for full compliance coverage.
