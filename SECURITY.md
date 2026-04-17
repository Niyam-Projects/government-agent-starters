# Security Policy

## Reporting a Vulnerability

If you discover a security vulnerability in this project, we appreciate your help in disclosing it responsibly.

**Please do NOT open a public GitHub issue or pull request for security vulnerabilities.**

Instead, prefer the repository's private vulnerability reporting flow:

- GitHub private reporting: `https://github.com/Niyam-Projects/government-agent-starters/security/advisories/new`

If private reporting is unavailable in your environment, contact the repository maintainers through the repository owner's public contact channel and clearly label the report as a security issue. Include:

1. A description of the vulnerability.
2. Steps to reproduce the issue.
3. Any relevant logs, screenshots, or proof-of-concept code.
4. Your assessment of the severity and impact.

## Response Goals

- **Acknowledgment goal**: within 48 hours of receipt.
- **Initial assessment goal**: within 5 business days.
- **Resolution goal**: within 30 days for critical issues, 90 days for others.

## Scope

This security policy covers:

- The `niyam-agent-starters` codebase and its dependencies.
- The local CLI tool shipped in this repository.
- Agent prompt templates, examples, and configuration files.

This policy does **not** cover:

- Vulnerabilities in third-party dependencies (report these upstream).
- Issues in user-deployed infrastructure.
- Social engineering attacks.

## Security Design Principles

This project follows these security principles:

1. **Local-first**: agents run locally by default with no external network calls.
2. **No secrets in code**: credentials belong in local environment files or secret stores, not tracked files.
3. **Minimal dependencies**: only well-maintained, audited packages.
4. **Input validation**: all agent inputs are validated before processing.
5. **Inspectable output**: agent executions produce structured output for review during development.
6. **Least privilege**: the Docker container runs as a non-root user.

## Supported Versions

| Version | Supported |
|---------|-----------|
| 0.1.x   | Yes       |

## Acknowledgments

We gratefully acknowledge security researchers who responsibly disclose vulnerabilities. With your permission, we will credit you in release notes.
