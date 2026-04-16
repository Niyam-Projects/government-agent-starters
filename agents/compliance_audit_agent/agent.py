"""Compliance, Security, and Accessibility Audit Loop Agent.

Reviews code, configurations, UI artifacts, CI/CD pipelines, and related
technical artifacts for security, accessibility, and deployment readiness
before promotion. Produces severity-categorized findings in the program's
A-H audit report format, preserves evidence references, and supports
re-review of remediated artifacts (the "loop" in the name).
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from jinja2 import Template

from niyam.sdk import AgentBase, AgentInput

DEFAULT_REVIEW_DOMAINS: tuple[str, ...] = (
    "secure_coding",
    "authn_authz",
    "secrets_handling",
    "logging_and_sensitive_data",
    "dependency_risk",
    "api_hardening",
    "accessibility_508",
    "operational_readiness",
)

SEVERITY_LEVELS: tuple[str, ...] = (
    "critical",
    "high",
    "moderate",
    "low",
    "informational",
)

OUTPUT_SECTIONS: tuple[str, ...] = (
    "A. Overall Release Readiness Status",
    "B. Security Findings",
    "C. Accessibility Findings",
    "D. Operational / Logging / Monitoring Findings",
    "E. Remediation Recommendations",
    "F. Evidence Artifacts to Retain",
    "G. Human Validation Required",
    "H. Final Go / No-Go Recommendation",
)


class ComplianceAuditAgent(AgentBase):
    name = "compliance_audit_agent"
    version = "0.2.0"
    description = (
        "Reviews code, configs, UI, and pipelines for security, accessibility, "
        "and release readiness; produces severity-ranked A-H findings and "
        "supports re-review of remediated artifacts."
    )

    def __init__(self, config_path: Path | None = None) -> None:
        super().__init__(config_path)
        prompt_path = Path(__file__).parent / "prompt.md"
        if prompt_path.exists():
            self.prompt_template = prompt_path.read_text()

    def validate_input(self, agent_input: AgentInput) -> list[str]:
        errors: list[str] = []
        payload = agent_input.payload

        if not payload.get("artifact"):
            errors.append("'artifact' is required in payload.")

        previous = payload.get("previous_findings")
        remediated = payload.get("remediated_artifact")
        if bool(previous) != bool(remediated):
            errors.append(
                "Re-check mode requires both 'previous_findings' and "
                "'remediated_artifact' to be provided together."
            )

        domains = payload.get("review_domains")
        if domains is not None and not isinstance(domains, list):
            errors.append("'review_domains' must be a list of strings when provided.")

        controls = payload.get("controls")
        if controls is not None and not isinstance(controls, list):
            errors.append("'controls' must be a list of strings when provided.")

        return errors

    def _run(self, agent_input: AgentInput, model_backend: Any) -> dict[str, Any]:
        payload = agent_input.payload
        review_domains = payload.get("review_domains") or list(DEFAULT_REVIEW_DOMAINS)
        review_mode = (
            "recheck"
            if payload.get("previous_findings") and payload.get("remediated_artifact")
            else "initial"
        )
        framework = payload.get("framework", "multi-domain")
        artifact_type = payload.get("artifact_type", "mixed")

        template = Template(self.prompt_template)
        prompt = template.render(
            artifact=payload["artifact"],
            artifact_type=artifact_type,
            language=payload.get("language"),
            framework=framework,
            controls=payload.get("controls", []),
            review_domains=review_domains,
            severity_levels=list(SEVERITY_LEVELS),
            output_sections=list(OUTPUT_SECTIONS),
            review_mode=review_mode,
            previous_findings=payload.get("previous_findings", ""),
            remediated_artifact=payload.get("remediated_artifact", ""),
        )

        response = model_backend.generate(prompt)

        return {
            "audit_report": response,
            "review_mode": review_mode,
            "framework": framework,
            "artifact_type": artifact_type,
            "domains_reviewed": review_domains,
            "severity_legend": list(SEVERITY_LEVELS),
            "output_sections": list(OUTPUT_SECTIONS),
            "confidence_labels": ["confirmed", "human_validation_required"],
            "model_used": type(model_backend).__name__,
        }
