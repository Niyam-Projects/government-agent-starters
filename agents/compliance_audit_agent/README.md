# Compliance, Security, and Accessibility Audit Loop Agent

Reviews code, configurations, UI implementations, CI/CD pipelines, and other
technical artifacts for security, accessibility, and deployment readiness
before promotion. Produces severity-categorized findings in the program's
A–H audit report format, preserves evidence references, and supports
re-review of remediated artifacts (the "loop").

> When run through the open-source `niyam` CLI, this agent uses the offline
> `MockBackend`. Local runs validate prompt wiring and output shape — they do
> not perform a real audit. Production assessments run via the Niyam AIOL.

## Mission

Review artifacts across eight domains before release:

1. Secure coding weaknesses
2. Authentication / authorization concerns
3. Secrets handling
4. Logging and sensitive-data exposure
5. Dependency risk
6. API / interface hardening
7. Accessibility and Section 508 concerns for UI/UX
8. Operational readiness and auditability

Findings are categorized by severity (`critical`, `high`, `moderate`, `low`,
`informational`) and tagged with a confidence label (`confirmed` or
`human_validation_required`).

## Input

| Field | Type | Required | Description |
|---|---|---|---|
| `artifact` | string | yes | The artifact under review (source code, config, CI YAML, UI markup, docs). |
| `artifact_type` | string | no | One of `source_code`, `config`, `ci_pipeline`, `ui`, `documentation`, `mixed`. Defaults to `mixed`. |
| `language` | string | no | Language hint when `artifact_type` is `source_code`. |
| `framework` | string | no | Framework lens (e.g., `NIST 800-53`, `FedRAMP`, `Section 508`). Defaults to `multi-domain`. |
| `controls` | string[] | no | Specific framework controls to consider. |
| `review_domains` | string[] | no | Subset of the eight mission domains. Defaults to all eight. |
| `previous_findings` | string | no | Prior audit findings — required (together with `remediated_artifact`) to trigger re-check mode. |
| `remediated_artifact` | string | no | Revised artifact to re-review against `previous_findings`. |

If exactly one of `previous_findings` or `remediated_artifact` is provided,
validation fails — re-check mode requires both.

## Output

| Field | Type | Description |
|---|---|---|
| `audit_report` | string | Markdown report with sections A–H. |
| `review_mode` | string | `initial` or `recheck`. |
| `framework` | string | Framework lens used for the review. |
| `artifact_type` | string | Echoed artifact type. |
| `domains_reviewed` | string[] | Domains actually covered this run. |
| `severity_legend` | string[] | The severity scale used. |
| `output_sections` | string[] | The A–H section titles the report is expected to contain. |
| `confidence_labels` | string[] | Allowed confidence values for findings. |
| `model_used` | string | Backend class name (`MockBackend` locally). |

The `audit_report` is Markdown with these sections, in order:

```
A. Overall Release Readiness Status
B. Security Findings
C. Accessibility Findings
D. Operational / Logging / Monitoring Findings
E. Remediation Recommendations
F. Evidence Artifacts to Retain
G. Human Validation Required
H. Final Go / No-Go Recommendation
```

Each finding in sections B–D includes: `id`, `severity`, `confidence`,
`location`, `description`, `impact`, `remediation`, and `references`
(CWE / OWASP / WCAG / Section 508 / NIST).

## Example

```bash
niyam run compliance_audit_agent \
  --input agents/compliance_audit_agent/examples/input.json
```

## Re-check (Loop) Mode

Pass the prior audit's findings and the revised artifact to request a
comparison pass:

```json
{
  "artifact": "<original artifact>",
  "previous_findings": "<prior A-H report or finding list>",
  "remediated_artifact": "<revised artifact>"
}
```

The model compares each prior finding and records a disposition of
`resolved`, `partially_resolved`, `unchanged`, or `regressed`, and flags any
new issues introduced by the remediation.

## Extending

- Add or remove severity levels in `config.yaml` (update `prompt.md` to
  match).
- Add framework-specific guidance in `prompt.md`.
- Chain with `secure_code_agent` for deeper code-level findings that feed
  this agent's security section as input evidence.

## Roadmap — AIOL Integration Enhancements

The following enhancements apply when this agent is loaded by the Niyam
AIOL runtime. They are documented here so prompt authors can align their
edits with the production surface.

### Deterministic SAST / SCA via FastMCP (Section B. Security Findings)

LLM-only vulnerability reasoning is non-deterministic and falls short of
FedRAMP / DoD baselines, which mandate official SAST / SCA tooling.

- **`sonarqube-mcp` server** — a FastMCP server that authenticates to an
  agency's SonarQube / SonarCloud instance and exposes tools for Quality
  Gate status, Security Hotspots, and rule violations for a given file
  or PR ref.
- **Prompt wiring** — the `prompt.md` should instruct this agent to
  invoke `sonarqube_fetch_findings` against the artifact's git ref
  **before** synthesizing Section B, so security findings are anchored
  to the agency's deterministic Quality Gate rather than model inference.

### Dynamic accessibility testing (Section C. Accessibility Findings)

This agent is stateless and cannot render a DOM from static artifacts.
To close that gap:

- **`axe-playwright-mcp` server** — a FastMCP microservice that accepts
  HTML, spins up a headless Playwright instance, runs `axe-core` against
  the rendered DOM, and returns structured JSON violations.
- **Prompt wiring** — mandate an invocation of `run_axe_core` against
  any UI artifact before finalizing Section C, so Section 508 findings
  reflect runtime DOM behavior rather than static string analysis.

### Loop bounding & financial guardrails

When this agent is chained with `secure_code_agent` in a revise / re-audit
loop, the ADK orchestrator must enforce:

- **`MAX_REVISIONS` circuit breaker** (e.g., 3–5 iterations) before the
  orchestrator raises `human_escalation_required`. This prevents
  compliance / code agents from ping-ponging indefinitely on a logic
  disagreement.
- **Global token / rate budget** in the AIOL middleware so a single
  session cannot exhaust inference tokens or hammer MCP connectors.

These are orchestrator- and prompt-level concerns — portable across
clouds and vendor model backends.
