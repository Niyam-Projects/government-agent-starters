# Secure Code Agent

Generates and refactors production-grade code for a regulated government
software team. Produces a structured reviewer package that includes an
implementation plan, code changes, tests (happy / edge / negative),
security considerations, rollback notes, and a reviewer checklist.

> When run through the open-source `niyam` CLI, this agent uses the offline
> `MockBackend`. Local runs validate prompt wiring and output shape; real
> code generation happens on the closed-source AIOL runtime.

## Use Case

Converting approved requirements into secure, testable code — and
refactoring legacy code into clearer, modular components — is a recurring
need in government software delivery. This agent standardizes the output
so human reviewers receive a consistent, traceable package every time.

## Modes

- `generate` — produce new code from `task_description` and `requirements`.
- `refactor` — modify `existing_code` while documenting current behavior
  and preserving business logic.

## Input

| Field              | Type     | Required                          | Description                                                      |
|--------------------|----------|-----------------------------------|------------------------------------------------------------------|
| `task_description` | string   | yes                               | Plain-English description of the change.                         |
| `mode`             | string   | no (default `generate`)           | `generate` or `refactor`.                                        |
| `requirements`     | string   | no                                | Approved requirements or acceptance criteria.                    |
| `existing_code`    | string   | yes when `mode=refactor`          | Source code to refactor.                                         |
| `language`         | string   | no (default `python`)             | Programming language.                                            |
| `stack_context`    | string   | no                                | Agency-approved stack, frameworks, or patterns to follow.        |
| `constraints`      | string[] | no                                | Hard constraints (e.g., "no new dependencies", "FIPS crypto only"). |
| `focus_areas`      | string[] | no                                | Areas to emphasize (e.g., "authz", "input validation").          |

## Output

| Field                | Type   | Description                                                             |
|----------------------|--------|-------------------------------------------------------------------------|
| `generation_result`  | string | Model-generated JSON package (sections A–H plus helpers).               |
| `mode`               | string | Echoed mode (`generate` or `refactor`).                                 |
| `language`           | string | Echoed language.                                                        |
| `existing_lines`     | int    | Line count of `existing_code` (0 when not provided).                    |
| `model_used`         | string | Name of the model backend used.                                         |

### `generation_result` JSON shape

Sections A–H are always present; helpers appear when relevant:

- `change_summary` (A)
- `assumptions` (B)
- `implementation_plan` (C)
- `code_changes` (D)
- `test_coverage` (E)
- `security_considerations` (F)
- `rollback_notes` (G)
- `reviewer_checklist` (H)
- `legacy_behavior` — present when `mode=refactor`.
- `open_questions` — items requiring clarification.
- `options` — 2–3 option breakdown when ambiguity blocks a decision.

## Example

```bash
niyam run secure_code_agent \
  --input agents/secure_code_agent/examples/input.json
```

## Extending

- Edit `prompt.md` to adjust the mandatory output sections or principles.
- Add language-specific guidance in `config.yaml` (`supported_languages`).
- Chain downstream with `compliance_audit_agent` to evaluate generated
  code against NIST / FedRAMP controls.
- For ambiguous requirements, upstream with `requirements_architect_agent`
  before invoking this agent.

## Roadmap — AIOL Integration Enhancements

The following enhancements apply when this agent is loaded by the Niyam AIOL
runtime. They are documented here so contributors can align prompt edits and
schema changes with the production surface.

### Section 508 / WCAG 2.1 AA mandates for UI generation

When generating or refactoring UI code, the prompt should enforce:

- **Semantic HTML5** — `<button>` over `<div onClick>`; avoid non-semantic
  wrappers for interactive elements.
- **ARIA** — explicit `aria-label` / `aria-describedby` for all icon-only
  interactions; visible keyboard focus (`:focus-visible`, `tabindex`).
- **Contrast** — minimum 4.5:1 color contrast ratio for text.
- **Schema** — add a mandatory `accessibility_considerations: string[]`
  field to the generation output so the model documents its accessibility
  logic for every UI change.
- **Tests** — when generating unit / integration tests for frontend
  components, include `axe-core` (or `jest-axe`) assertions for zero
  accessibility violations.

### Continuous ATO (cATO) provenance & traceability

To preserve code-level explainability for ISSO reviews:

- **Trace ID in VCS** — the AIOL orchestrator injects the OpenTelemetry
  `Trace ID` as an immutable trailer in every agent-authored commit or PR
  (e.g., `AI-Trace-ID: <uuid>`), linking source code to its audit trace.
- **Requirements traceability** — extend the output schema with a
  `requirements_traceability` object mapping generated files / functions
  to parent epic / ticket IDs pulled via the JIRA FastMCP server.
- **Rationale comments** — for cyber / compliance-relevant configuration
  (encryption thresholds, RBAC, etc.), inject inline comments such as
  `# AI-Rationale: AES-256-GCM to fulfill FedRAMP SC-28 per JIRA-402`.

These are prompt- and schema-level changes — fully portable across
clouds — and do not require AIOL source access to prototype.
