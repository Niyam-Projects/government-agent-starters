# Program Support & Audit-Ready Artifact Agent

Transforms operational project data — tickets, sprint reports, status notes, risk registers, meeting notes, test results, and cost summaries — into accurate, concise, audit-ready program artifacts.

> When run through the open-source `niyam` CLI, this agent uses the offline `MockBackend`. Local runs validate prompt wiring and output shape, but they do not generate polished production-ready artifacts.

## Mission

Improve leadership visibility, execution discipline, and reviewer readiness across the program lifecycle: weekly status reporting, monthly program reviews, risk logs, action item trackers, milestone documentation, acquisition artifacts, governance board prep, audit response packages, and records and information management summaries.

## Operating Principles

- Accuracy over verbosity.
- Never invent status; missing data is clearly labeled.
- Differentiate facts, risks, decisions, and recommendations.
- Useful to technical leads, PMs, CORs, and executives.
- Traceable back to source inputs.
- Flags when human review is mandatory before release.

## Supported Artifacts

| ID | `artifact_type`               | Purpose                                          |
|----|-------------------------------|--------------------------------------------------|
| A  | `weekly_status_report`        | Weekly rollup for PMs and team leads             |
| B  | `monthly_pmr_brief`           | Monthly program management review                |
| C  | `risk_issue_register_update`  | New / changed / closed risks and issues          |
| D  | `decision_memo`               | Structured decision with options and rationale   |
| E  | `audit_evidence_index`        | Control-to-evidence mapping for audits           |
| F  | `meeting_summary`             | Discussion, decisions, action items with owners  |
| G  | `executive_one_pager`         | One-page executive snapshot                      |

## Supported Audiences

- `technical_team`
- `pmo`
- `executive_leadership`
- `audit_review_board`

## Input

| Field           | Type   | Required | Description                                                                 |
|-----------------|--------|----------|-----------------------------------------------------------------------------|
| `project_data`  | string | yes      | Structured or unstructured source inputs (tickets, notes, metrics, etc.)    |
| `artifact_type` | string | yes      | One of the supported artifact types above                                   |
| `audience`      | string | no       | Target audience (default: `pmo`)                                            |

## Output

| Field                | Type   | Description                          |
|----------------------|--------|--------------------------------------|
| `generated_artifact` | string | Model-generated program artifact     |
| `artifact_type`      | string | Type of artifact that was generated  |
| `model_used`         | string | Name of the model backend used       |

Every generated artifact begins with a **"What leadership needs to know"** section and ends with a **"Quality Check"** block listing missing evidence, unverifiable claims, and items requiring human review before release.

## Example

```bash
niyam run program_support_agent \
  --input agents/program_support_agent/examples/input.json
```

## Extending

- Edit `prompt.md` to customize artifact formats or add new ones.
- Add new artifact types and audiences in `config.yaml`.
- Connect to project management, ticketing, or document repositories via custom connectors.
