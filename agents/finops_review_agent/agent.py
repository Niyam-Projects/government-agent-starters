"""FinOps, Cloud Optimization, and Architecture Review Agent.

Analyzes cloud environments, proposed solution changes, and architecture
decisions to identify cost optimization opportunities, technical risk,
maintainability concerns, and mission fit. Produces a decision-ready memo
for government program leadership.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from jinja2 import Template

from niyam.sdk import AgentBase, AgentInput


class FinOpsReviewAgent(AgentBase):
    name = "finops_review_agent"
    version = "0.2.0"
    description = (
        "Reviews cloud spend, architecture changes, and AI right-sizing; "
        "produces a decision-ready optimization memo."
    )

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
        payload = agent_input.payload
        template = Template(self.prompt_template)
        prompt = template.render(
            spend_data=payload["spend_data"],
            period=payload.get("period", "monthly"),
            cloud_provider=payload.get("cloud_provider", "generic"),
            architecture_summary=payload.get("architecture_summary"),
            proposed_change=payload.get("proposed_change"),
            ai_usage=payload.get("ai_usage"),
            mission_context=payload.get("mission_context"),
            telemetry_gaps=payload.get("telemetry_gaps"),
        )

        response = model_backend.generate(prompt)

        return {
            "finops_analysis": response,
            "period": payload.get("period", "monthly"),
            "cloud_provider": payload.get("cloud_provider", "generic"),
            "review_scope": {
                "spend_data_provided": bool(payload.get("spend_data")),
                "architecture_provided": bool(payload.get("architecture_summary")),
                "proposed_change_provided": bool(payload.get("proposed_change")),
                "ai_usage_provided": bool(payload.get("ai_usage")),
                "mission_context_provided": bool(payload.get("mission_context")),
                "telemetry_gaps_declared": bool(payload.get("telemetry_gaps")),
            },
            "model_used": type(model_backend).__name__,
        }
