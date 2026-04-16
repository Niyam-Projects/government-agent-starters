"""Secure Code Generation & Refactor Agent implementation.

Generates new code and refactors existing code with explicit security,
testability, and compliance considerations. Produces a structured reviewer
package (plan, code, tests, security notes, rollback, checklist).
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from jinja2 import Template

from niyam.sdk import AgentBase, AgentInput


_VALID_MODES = {"generate", "refactor"}


class SecureCodeAgent(AgentBase):
    name = "secure_code_agent"
    version = "0.2.0"
    description = (
        "Generates and refactors production-grade code with explicit "
        "security, testability, and compliance considerations."
    )

    def __init__(self, config_path: Path | None = None) -> None:
        super().__init__(config_path)
        prompt_path = Path(__file__).parent / "prompt.md"
        if prompt_path.exists():
            self.prompt_template = prompt_path.read_text()

    def validate_input(self, agent_input: AgentInput) -> list[str]:
        errors: list[str] = []
        payload = agent_input.payload

        if not payload.get("task_description"):
            errors.append("'task_description' is required in payload.")

        mode = payload.get("mode", "generate")
        if mode not in _VALID_MODES:
            errors.append(
                f"'mode' must be one of {sorted(_VALID_MODES)}; got '{mode}'."
            )

        if mode == "refactor" and not payload.get("existing_code"):
            errors.append(
                "'existing_code' is required in payload when mode='refactor'."
            )

        constraints = payload.get("constraints")
        if constraints is not None and not isinstance(constraints, list):
            errors.append("'constraints' must be a list of strings if provided.")

        focus_areas = payload.get("focus_areas")
        if focus_areas is not None and not isinstance(focus_areas, list):
            errors.append("'focus_areas' must be a list of strings if provided.")

        return errors

    def _run(self, agent_input: AgentInput, model_backend: Any) -> dict[str, Any]:
        payload = agent_input.payload
        mode = payload.get("mode", "generate")
        language = payload.get("language", "python")
        existing_code = payload.get("existing_code", "")

        template = Template(self.prompt_template)
        prompt = template.render(
            mode=mode,
            task_description=payload["task_description"],
            requirements=payload.get("requirements", ""),
            existing_code=existing_code,
            language=language,
            stack_context=payload.get("stack_context", ""),
            constraints=payload.get("constraints", []),
            focus_areas=payload.get("focus_areas", []),
        )

        response = model_backend.generate(prompt)

        return {
            "generation_result": response,
            "mode": mode,
            "language": language,
            "existing_lines": (
                existing_code.count("\n") + 1 if existing_code else 0
            ),
            "model_used": type(model_backend).__name__,
        }
