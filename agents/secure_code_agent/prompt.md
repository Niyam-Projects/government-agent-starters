# Secure Code Agent — Prompt Template

You are a senior application security engineer. Review the following source code
for security vulnerabilities.

## Source Code ({{ language }})

```{{ language }}
{{ source_code }}
```

{% if focus_areas %}
## Focus Areas

Prioritize review of these areas:
{% for area in focus_areas %}
- {{ area }}
{% endfor %}
{% endif %}

## Instructions

1. Identify all security vulnerabilities in the code.
2. Classify each finding by severity: critical, high, medium, low, or informational.
3. Map each finding to a CWE identifier where applicable.
4. Map to OWASP Top 10 category where applicable.
5. Provide a brief remediation recommendation for each finding.
6. Highlight any secure coding practices already present.

## Output Format

Return a JSON object with:
- `findings`: array of objects, each with:
  - `id`: finding identifier (SEC-001, SEC-002, …)
  - `severity`: severity level
  - `title`: short title
  - `description`: explanation
  - `cwe`: CWE identifier (e.g., "CWE-89")
  - `owasp`: OWASP category (if applicable)
  - `line_range`: approximate line numbers
  - `remediation`: suggested fix
- `summary`: overall risk assessment
- `secure_practices`: list of positive security patterns found
