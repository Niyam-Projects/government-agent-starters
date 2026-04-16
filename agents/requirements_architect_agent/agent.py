"""Requirements Architect Agent implementation.

Converts mission needs, policy constraints, legacy documentation, tickets,
and codebase context into an implementation-ready technical architecture
package for U.S. government software delivery teams.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from jinja2 import Template

from niyam.sdk import AgentBase, AgentInput


class RequirementsArchitectAgent(AgentBase):
    name = "requirements_architect_agent"
    version = "0.2.0"
    description = (
        "Converts mission needs and mixed artifacts into a traceable, "
        "implementation-ready technical architecture package."
    )

    def __init__(self, config_path: Path | None = None) -> None:
        super().__init__(config_path)
        prompt_path = Path(__file__).parent / "prompt.md"
        if prompt_path.exists():
            self.prompt_template = prompt_path.read_text()

    def validate_input(self, agent_input: AgentInput) -> list[str]:
        errors: list[str] = []
        payload = agent_input.payload
        if not payload.get("requirements_text") and not payload.get("artifacts"):
            errors.append(
                "At least one of 'requirements_text' or 'artifacts' is required in payload."
            )
        artifacts = payload.get("artifacts")
        if artifacts is not None and not isinstance(artifacts, list):
            errors.append("'artifacts' must be a list when provided.")
        return errors

    def _run(self, agent_input: AgentInput, model_backend: Any) -> dict[str, Any]:
        payload = agent_input.payload
        artifacts = payload.get("artifacts") or []

        template = Template(self.prompt_template)
        prompt = template.render(
            requirements_text=payload.get("requirements_text", ""),
            context=payload.get("context", ""),
            artifacts=artifacts,
        )

        response = model_backend.generate(prompt)

        return {
            "architecture_package": response,
            "input_length": len(payload.get("requirements_text", "")),
            "artifact_count": len(artifacts),
            "model_used": type(model_backend).__name__,
        }
