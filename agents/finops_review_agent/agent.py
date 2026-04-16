"""FinOps Review Agent implementation.

Analyzes cloud spending data and produces optimization recommendations
aligned with FinOps Foundation practices.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from jinja2 import Template

from niyam.sdk import AgentBase, AgentInput


class FinOpsReviewAgent(AgentBase):
    name = "finops_review_agent"
    version = "0.1.0"
    description = "Analyzes cloud spend data and recommends cost optimizations."

    def __init__(self, config_path: Path | None = None) -> None:
        super().__init__(config_path)
        prompt_path = Path(__file__).parent / "prompt.md"
        if prompt_path.exists():
            self.prompt_template = prompt_path.read_text()

    def validate_input(self, agent_input: AgentInput) -> list[str]:
        errors: list[str] = []
        if not agent_input.payload.get("spend_data"):
            errors.append("'spend_data' is required in payload.")
        return errors

    def _run(self, agent_input: AgentInput, model_backend: Any) -> dict[str, Any]:
        template = Template(self.prompt_template)
        prompt = template.render(
            spend_data=agent_input.payload["spend_data"],
            period=agent_input.payload.get("period", "monthly"),
            cloud_provider=agent_input.payload.get("cloud_provider", "generic"),
        )

        response = model_backend.generate(prompt)

        return {
            "finops_analysis": response,
            "period": agent_input.payload.get("period", "monthly"),
            "cloud_provider": agent_input.payload.get("cloud_provider", "generic"),
            "model_used": type(model_backend).__name__,
        }
