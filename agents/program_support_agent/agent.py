"""Program Support & Audit-Ready Artifact Agent implementation.

Transforms operational project data into audit-ready program artifacts:
weekly status reports, monthly PMR briefs, risk and issue register
updates, decision memos, audit evidence indexes, meeting summaries, and
executive one-pagers.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from jinja2 import Template

from niyam.sdk import AgentBase, AgentInput


class ProgramSupportAgent(AgentBase):
    name = "program_support_agent"
    version = "0.2.0"
    description = "Generates audit-ready program artifacts from operational project data."

    def __init__(self, config_path: Path | None = None) -> None:
        super().__init__(config_path)
        prompt_path = Path(__file__).parent / "prompt.md"
        if prompt_path.exists():
            self.prompt_template = prompt_path.read_text()

    def validate_input(self, agent_input: AgentInput) -> list[str]:
        errors: list[str] = []
        if not agent_input.payload.get("project_data"):
            errors.append("'project_data' is required in payload.")
        if not agent_input.payload.get("artifact_type"):
            errors.append("'artifact_type' is required in payload.")
        return errors

    def _run(self, agent_input: AgentInput, model_backend: Any) -> dict[str, Any]:
        template = Template(self.prompt_template)
        prompt = template.render(
            project_data=agent_input.payload["project_data"],
            artifact_type=agent_input.payload["artifact_type"],
            audience=agent_input.payload.get("audience", "pmo"),
        )

        response = model_backend.generate(prompt)

        return {
            "generated_artifact": response,
            "artifact_type": agent_input.payload["artifact_type"],
            "model_used": type(model_backend).__name__,
        }
