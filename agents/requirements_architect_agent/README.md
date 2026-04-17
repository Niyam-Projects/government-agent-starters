# Requirements Architect Agent

Converts mission needs, policy constraints, legacy documentation, tickets, and
codebase context into an **implementation-ready technical architecture
package** for U.S. government software delivery teams.

> When run through the open-source `niyam` CLI, this agent uses the offline
> `MockBackend`. Local runs validate prompt wiring and output shape, but do
> not perform real model-backed analysis. Deploy on the Niyam AIOL for
> production inference.

## Mission

1. Extract functional and non-functional requirements from mixed artifacts.
2. Identify missing requirements, ambiguities, assumptions, and risks.
3. Propose a target architecture aligned to secure government delivery.
4. Produce traceable mapping: mission need → requirement → architecture
   decision → backlog.
5. Recommend where AI / ML / LLM fits and where traditional engineering is
   better.

## Input

| Field               | Type    | Required                                       | Description                                                                                   |
|---------------------|---------|------------------------------------------------|-----------------------------------------------------------------------------------------------|
| `requirements_text` | string  | at least one of `requirements_text` / `artifacts` | Raw requirements / mission-need text.                                                       |
| `artifacts`         | list    | at least one of `requirements_text` / `artifacts` | Mixed artifacts: SOWs, CONOPS, Jira/Xray tickets, ICDs, source code, runbooks, policy memos. |
| `context`           | string  | no                                             | Additional environment or program context (e.g., FedRAMP target, zero-trust posture).         |

Each `artifact` entry has: `type` (see `config.yaml: artifact_types`), `name`,
and optional `content`.

## Output

| Field                  | Type   | Description                                                                                  |
|------------------------|--------|----------------------------------------------------------------------------------------------|
| `architecture_package` | string | Reviewer-ready markdown document with sections **A–J** (see below).                          |
| `input_length`         | int    | Character count of `requirements_text`.                                                      |
| `artifact_count`       | int    | Number of artifacts supplied.                                                                |
| `model_used`           | string | Name of the model backend used.                                                              |

### Sections produced (A–J)

- **A.** Executive Summary
- **B.** Mission Problem Statement
- **C.** Requirements Inventory
- **D.** Current-State Assessment
- **E.** Target-State Architecture
- **F.** Risks / Unknowns / Government Decisions
- **G.** AI Suitability Analysis
- **H.** Backlog with Priorities
- **I.** Traceability Matrix
- **J.** Recommended First Sprint

## Operating Rules (enforced by the prompt)

- Assume federal, regulated, zero-trust, audit-sensitive environments.
- Favor explainability, maintainability, interoperability, modularity.
- Do not assume unrestricted internet access.
- Do not invent agency policy — flag as **Government Decision Required**.
- Classify every item as must-have / enhancement / deferred / risk-or-blocker.

## Example

```bash
niyam run requirements_architect_agent \
  --input agents/requirements_architect_agent/examples/input.json
```

See `examples/input.json` and `examples/output.json` for a federal compliance
management platform walkthrough.

## Extending

- Edit `prompt.md` to adjust analysis depth or section content.
- Edit `config.yaml` to change categories, artifact types, or roadmap
  horizons.
- Integrate a real backend through the Niyam AIOL when you need live model
  inference beyond the local mock runner.
