"""Agent base class and data contracts.

These are the stable interfaces that every Niyam agent must implement.
The Niyam AIOL loads agents through these contracts — agent authors
never need to import anything outside ``niyam.sdk``.
"""

from __future__ import annotations

import abc
import inspect
import logging
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import yaml
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


class AgentInput(BaseModel):
    """Canonical input envelope for any agent invocation."""

    payload: dict[str, Any] = Field(default_factory=dict)
    metadata: dict[str, Any] = Field(default_factory=dict)


class AgentOutput(BaseModel):
    """Canonical output envelope returned by every agent."""

    agent_name: str
    status: str = "success"
    result: dict[str, Any] = Field(default_factory=dict)
    errors: list[str] = Field(default_factory=list)
    timestamp: str = Field(default_factory=lambda: datetime.now(UTC).isoformat())


class AgentBase(abc.ABC):
    """Abstract base that every agent must extend.

    Subclasses implement ``_run`` with their domain logic.  The public ``run``
    method handles validation, logging, and error wrapping.

    This class is the **stable contract** between open-source agents and the
    Niyam AIOL.  The AIOL discovers agents by looking for subclasses of
    ``AgentBase`` and wraps their execution with security and audit controls.
    """

    name: str = "base_agent"
    version: str = "0.1.0"
    description: str = ""

    def __init__(self, config_path: Path | None = None) -> None:
        self.config: dict[str, Any] = {}
        if config_path and config_path.exists():
            self.config = yaml.safe_load(config_path.read_text()) or {}
        self.prompt_template: str = ""
        self._load_prompt()

    def _load_prompt(self) -> None:
        """Load the prompt template from the agent's directory."""
        agent_file = Path(inspect.getfile(self.__class__)).resolve()
        agent_dir = agent_file.parent
        prompt_path = agent_dir / "prompt.md"
        if prompt_path.exists():
            self.prompt_template = prompt_path.read_text()

    def validate_input(self, agent_input: AgentInput) -> list[str]:
        """Return a list of validation errors (empty means valid)."""
        return []

    @abc.abstractmethod
    def _run(self, agent_input: AgentInput, model_backend: Any) -> dict[str, Any]:
        """Core agent logic — implemented by each agent."""
        ...

    def run(self, agent_input: AgentInput, model_backend: Any = None) -> AgentOutput:
        """Execute the agent with validation and error handling."""
        errors = self.validate_input(agent_input)
        if errors:
            return AgentOutput(
                agent_name=self.name,
                status="validation_error",
                errors=errors,
            )
        try:
            result = self._run(agent_input, model_backend)
            return AgentOutput(agent_name=self.name, result=result)
        except Exception as exc:  # noqa: BLE001
            logger.exception("Agent %s failed", self.name)
            return AgentOutput(
                agent_name=self.name,
                status="error",
                errors=[str(exc)],
            )
