# Security Architecture

Security is the **primary reason** the Niyam AI Orchestration Layer (AIOL) is closed source. Government and enterprise deployments demand security controls that are hardened, audited, and not publicly exposed. The open-source agent SDK provides baseline code hygiene — production security enforcement happens inside the AIOL.

## Security Boundary: Open vs. Closed

```
┌─────────────────────────────────────────────────────────────────────┐
│                    OPEN SOURCE (this repo)                           │
│                                                                     │
│  Security scope: agent-level input validation and code hygiene      │
│                                                                     │
│  ✓ Pydantic input validation on AgentInput                          │
│  ✓ Structured AgentOutput envelope for consistent handling          │
│  ✓ No tracked secrets or local env files in the repo               │
│  ✓ Non-root Docker container                                        │
│  ✓ Version-bounded dependencies and CI vulnerability scanning       │
│  ✓ Zero network calls in local runner (fully air-gapped)            │
│                                                                     │
│  ✗ No auth — anyone can run any agent locally                       │
│  ✗ No encryption — no data-at-rest or data-in-transit protection    │
│  ✗ No audit trail — output goes to stdout or a local file           │
│  ✗ No prompt security — no injection detection or guardrails        │
│  ✗ No data classification — no CUI/PII handling controls            │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│                 NIYAM AIOL (closed source)                           │
│                                                                     │
│  Security scope: full operational security for production systems    │
│                                                                     │
│  · Identity and access control                                      │
│  · Prompt security and output guardrails                             │
│  · Data protection and encryption                                    │
│  · Audit and compliance                                              │
│  · Network and infrastructure hardening                              │
│  · Secrets and credential management                                 │
│                                                                     │
│  Details of the security implementation are not published.           │
└─────────────────────────────────────────────────────────────────────┘
```

## Why Security Is Closed Source

1. **Security implementations are attack surfaces.** Publishing detection logic, guardrail rules, or audit internals gives adversaries a roadmap. Keeping them closed is a deliberate security posture.
2. **Government and enterprise deployments require hardened, non-inspectable controls** that vary per agency, classification level, and authorization boundary.
3. **Compliance evidence and audit mechanisms** are tightly coupled to customer environments and cannot be safely generalized in a public repo.
4. **Credential and secrets management** involves flows that must remain opaque.

## What the Open-Source Repo Provides

The agent SDK enforces baseline security hygiene that is safe to publish:

### Input Validation

Every agent receives input through `AgentInput` (a Pydantic model). Agents implement `validate_input()` to enforce domain-specific constraints before any model call is made. The AIOL applies additional validation at runtime.

### Structured Output Envelope

All agent output flows through `AgentOutput` — a fixed schema with `agent_name`, `status`, `result`, `errors`, and `timestamp`. This gives the AIOL and local tooling a consistent surface to work with, but agent authors must still avoid putting sensitive or unnecessary raw data into `result`.

### No Secrets in Code

- `.env` files are excluded via `.gitignore`.
- `.env.example` contains local runner settings only and no credentials.
- Pre-commit runs `detect-private-key` to catch accidental private-key commits.
- The local runner requires zero credentials (mock backend only).

### Minimal Attack Surface

- The local runner makes **zero network calls**.
- Dependencies are minimal and constrained to reviewed version ranges.
- The Docker image runs as a non-root user.
- CI scans dependencies for known CVEs.

## What the AIOL Provides

The AIOL includes a comprehensive security layer purpose-built for government and enterprise AI workloads. The following describes the *categories* of security capability — not their implementation.

| Category | Scope |
|---|---|
| **Identity & access control** | Authentication, authorization, and policy enforcement across agents, models, and data sources |
| **Prompt security** | Protection against adversarial inputs and enforcement of output safety policies |
| **Data protection** | Encryption, classification, and lifecycle management for data at rest and in transit |
| **Audit & compliance** | Comprehensive audit trail with compliance-aligned reporting |
| **Secrets & credential management** | Secure handling of API keys, service credentials, and managed identities |
| **Infrastructure hardening** | Network controls, container security, and runtime threat protection |

> Implementation details, algorithms, specific tooling, and architecture of the AIOL security layer are not documented in this public repository.

## NIST 800-53 Relevance

The combined open-source SDK + AIOL is designed with the following NIST 800-53 control families in mind:

| Control Family | Open-Source SDK | AIOL |
|---|---|---|
| **AC** (Access Control) | Minimal dependencies | Authorization and policy enforcement |
| **AU** (Audit & Accountability) | `AgentOutput` schema | Comprehensive audit capabilities |
| **CM** (Configuration Management) | Minimal local runner | Production configuration controls |
| **IA** (Identification & Authentication) | — | Identity and authentication services |
| **SC** (System & Communications Protection) | `.env` for local secrets | Encryption and communication protection |
| **SI** (System & Information Integrity) | Pydantic input validation | Additional integrity controls |

This mapping is illustrative. Organizations must perform their own assessments as part of their Authorization to Operate (ATO) process. The AIOL team can provide compliance documentation under NDA.

## Secure Development Practices (Open-Source Repo)

### For Agent Authors

- Validate all inputs in `validate_input()` — do not trust payload contents.
- Do not make direct network calls — use the `Connector` protocol.
- Do not log or print sensitive payload fields.
- Do not hardcode model names, API endpoints, or credentials.
- Use `AgentOutput` as the sole return channel — do not write to files directly.

### For Contributors

- All dependencies must be reviewed for known vulnerabilities before merging.
- Pre-commit hooks must pass (includes `detect-private-key`).
- No `.env` files, credentials, internal URLs, or non-public artifacts in any commit.
- Security vulnerabilities must be reported privately per [SECURITY.md](../SECURITY.md).

### Data Handling

- Do not process classified, CUI, or PII data with the local runner.
- The local runner has no encryption, no access control, and no audit trail.
- For data requiring protection, deploy agents through the AIOL.
- Agent outputs may contain AI-generated content — always review before use in any decision process.
