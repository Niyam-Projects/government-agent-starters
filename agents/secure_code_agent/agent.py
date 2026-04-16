"""Secure Code Agent implementation.

Reviews source code for common security vulnerabilities and produces
findings aligned with CWE and OWASP classifications.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from jinja2 import Template

from niyam.sdk import AgentBase, AgentInput


class SecureCodeAgent(AgentBase):
    name = "secure_code_agent"
    version = "0.1.0"
    description = "Reviews code for security vulnerabilities (CWE/OWASP aligned)."

    def __init__(self, config_path: Path | None = None) -> None:
        super().__init__(config_path)
        prompt_path = Path(__file__).parent / "prompt.md"
        if prompt_path.exists():
            self.prompt_template = prompt_path.read_text()

    def validate_input(self, agent_input: AgentInput) -> list[str]:
        errors: list[str] = []
        if not agent_input.payload.get("source_code"):
            errors.append("'source_code' is required in payload.")
        return errors

    def _run(self, agent_input: AgentInput, model_backend: Any) -> dict[str, Any]:
        template = Template(self.prompt_template)
        prompt = template.render(
            source_code=agent_input.payload["source_code"],
            language=agent_input.payload.get("language", "python"),
            focus_areas=agent_input.payload.get("focus_areas", []),
        )

        response = model_backend.generate(prompt)

        return {
            "security_review": response,
            "lines_reviewed": agent_input.payload["source_code"].count("\n") + 1,
            "language": agent_input.payload.get("language", "python"),
            "model_used": type(model_backend).__name__,
        }
