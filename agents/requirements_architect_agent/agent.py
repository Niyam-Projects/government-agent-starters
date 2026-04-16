"""Requirements Architect Agent implementation.

Analyzes unstructured requirements text and produces structured, prioritized
requirements with traceability metadata.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from jinja2 import Template

from niyam.sdk import AgentBase, AgentInput


class RequirementsArchitectAgent(AgentBase):
    name = "requirements_architect_agent"
    version = "0.1.0"
    description = "Analyzes and structures project requirements into traceable artifacts."

    def __init__(self, config_path: Path | None = None) -> None:
        super().__init__(config_path)
        prompt_path = Path(__file__).parent / "prompt.md"
        if prompt_path.exists():
            self.prompt_template = prompt_path.read_text()

    def validate_input(self, agent_input: AgentInput) -> list[str]:
        errors: list[str] = []
        if not agent_input.payload.get("requirements_text"):
            errors.append("'requirements_text' is required in payload.")
        return errors

    def _run(self, agent_input: AgentInput, model_backend: Any) -> dict[str, Any]:
        template = Template(self.prompt_template)
        prompt = template.render(
            requirements_text=agent_input.payload["requirements_text"],
            context=agent_input.payload.get("context", ""),
        )

        response = model_backend.generate(prompt)

        return {
            "structured_requirements": response,
            "input_length": len(agent_input.payload["requirements_text"]),
            "model_used": type(model_backend).__name__,
        }
