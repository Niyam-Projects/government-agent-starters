"""TODO: Agent implementation.

Replace this with a description of what your agent does.
"""

from __future__ import annotations

from typing import Any

from jinja2 import Template

from niyam.sdk import AgentBase, AgentInput


class NewAgent(AgentBase):
    # TODO: Update these class attributes
    name = "new_agent"
    version = "0.1.0"
    description = "TODO: Describe what this agent does."

    def validate_input(self, agent_input: AgentInput) -> list[str]:
        # TODO: Add input validation
        errors: list[str] = []
        if not agent_input.payload.get("input_text"):
            errors.append("'input_text' is required in payload.")
        return errors

    def _run(self, agent_input: AgentInput, model_backend: Any) -> dict[str, Any]:
        template = Template(self.prompt_template)
        prompt = template.render(**agent_input.payload)
        response = model_backend.generate(prompt)
        # TODO: Post-process the response as needed
        return {"result": response}
