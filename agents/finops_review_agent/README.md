# FinOps, Cloud Optimization & Architecture Review Agent

Reviews cloud environments, proposed architecture changes, and AI/LLM usage
for a government IT program. Produces a decision-ready memo identifying
cost optimization opportunities, technical risk, maintainability concerns,
and mission fit.

> When run through the open-source `niyam` CLI, this agent uses the offline
> `MockBackend`. Local runs validate prompt wiring and output shape, but
> they do not perform real spend or architecture analysis. Production runs
> on the Niyam AIOL inject a live model backend and enterprise connectors.

## Mission

Analyze cloud environments, proposed solution changes, and architecture
decisions to identify cost optimization opportunities, technical risk,
maintainability concerns, and mission fit. The agent covers five review
steps:

1. Review cloud usage, sizing, service selection, and deployment patterns.
2. Detect underutilization, duplication, waste, and unnecessary complexity.
3. Evaluate proposed architecture changes or change requests.
4. Assess whether an AI/LLM solution is right-sized for the problem.
5. Produce actionable recommendations for cost savings, avoidance, and
   implementation sequencing.

## Guiding Principles

- Optimize for mission value, not just lowest cost.
- Explain tradeoffs between speed, cost, security, and maintainability.
- Identify when a simpler non-AI solution is more appropriate.
- Explicitly call out assumptions and telemetry gaps.
- Never fabricate pricing or utilization data.

## Input

| Field                  | Type   | Required | Description                                                              |
|------------------------|--------|----------|--------------------------------------------------------------------------|
| `spend_data`           | string | yes      | Cloud spending data (structured or narrative).                           |
| `period`               | string | no       | Reporting period. Default `"monthly"`.                                   |
| `cloud_provider`       | string | no       | Cloud provider. Default `"generic"`.                                     |
| `architecture_summary` | string | no       | Current architecture description.                                        |
| `proposed_change`      | string | no       | Proposed architecture change or change request.                          |
| `ai_usage`             | string | no       | AI / ML / LLM components, models, traffic, and purposes.                 |
| `mission_context`      | string | no       | Program mission, users, and constraints.                                 |
| `telemetry_gaps`       | string | no       | Known gaps in billing, utilization, or architectural telemetry.          |

`spend_data` remains required to preserve the baseline FinOps review
behavior. All other fields are optional and, when provided, broaden the
review to cover architecture quality and AI right-sizing.

## Output

The `finops_analysis` field contains the decision-ready memo as a JSON
string. The memo uses the A–H structure:

| Section                      | Key                          |
|------------------------------|------------------------------|
| A. Executive Summary         | `executive_summary`          |
| B. Current State / Change    | `current_state`              |
| C. Cost Drivers              | `cost_drivers`               |
| D. Risks and Constraints     | `risks_and_constraints`      |
| E. Optimization Opportunities| `optimization_opportunities` |
| F. AI Suitability / Right-Size | `ai_suitability`           |
| G. Recommended Actions       | `recommendations`            |
| H. Evidence Needed           | `evidence_needed`            |

Each `recommendations` entry includes an `action` of `keep`, `optimize`,
`replace`, or `defer`, plus `estimated_savings`, `effort`, `priority`,
`sequence`, and `assumptions`.

Top-level wrapper fields returned by the agent:

| Field             | Type   | Description                                                         |
|-------------------|--------|---------------------------------------------------------------------|
| `finops_analysis` | string | Decision-ready memo (JSON per format above).                        |
| `period`          | string | Period that was analyzed.                                           |
| `cloud_provider`  | string | Cloud provider context.                                             |
| `review_scope`    | object | Booleans indicating which input sections were supplied.             |
| `model_used`      | string | Name of the model backend class used at runtime.                    |

## Example

```bash
niyam run finops_review_agent \
  --input agents/finops_review_agent/examples/input.json
```

## Extending

- Edit `prompt.md` to adjust review steps or memo sections.
- Add provider-specific optimization rules, AI right-sizing checks, or
  architecture dimensions in `config.yaml`.
- Connect to cloud billing APIs, CMDB, or architecture repositories via
  AIOL-provided connectors in production (mock-only in this repo).
