"""Compliance Audit Agent implementation.

Evaluates project artifacts against compliance frameworks (NIST, FedRAMP,
SOC 2, etc.) and produces gap analyses.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from jinja2 import Template

from niyam.sdk import AgentBase, AgentInput


class ComplianceAuditAgent(AgentBase):
    name = "compliance_audit_agent"
    version = "0.1.0"
    description = "Evaluates artifacts against compliance frameworks and produces gap analyses."

    def __init__(self, config_path: Path | None = None) -> None:
        super().__init__(config_path)
        prompt_path = Path(__file__).parent / "prompt.md"
        if prompt_path.exists():
            self.prompt_template = prompt_path.read_text()

    def validate_input(self, agent_input: AgentInput) -> list[str]:
        errors: list[str] = []
        if not agent_input.payload.get("artifact"):
            errors.append("'artifact' is required in payload.")
        if not agent_input.payload.get("framework"):
            errors.append("'framework' is required in payload.")
        return errors

    def _run(self, agent_input: AgentInput, model_backend: Any) -> dict[str, Any]:
        template = Template(self.prompt_template)
        prompt = template.render(
            artifact=agent_input.payload["artifact"],
            framework=agent_input.payload["framework"],
            controls=agent_input.payload.get("controls", []),
        )

        response = model_backend.generate(prompt)

        return {
            "compliance_analysis": response,
            "framework": agent_input.payload["framework"],
            "model_used": type(model_backend).__name__,
        }
