"""Agent discovery for the local runner.

Scans the ``agents/`` directory and imports each agent module, registering
any subclass of ``AgentBase``.  This is the local-dev equivalent of the
platform's agent registry — intentionally simple.
"""

from __future__ import annotations

import importlib
import logging
from pathlib import Path
from typing import Any

from niyam.sdk.agent import AgentBase

logger = logging.getLogger(__name__)

AGENTS_DIR = Path(__file__).resolve().parents[3] / "agents"


class AgentRegistry:
    """Discovers and retrieves agents from the local ``agents/`` directory."""

    _agents: dict[str, type[AgentBase]] = {}

    @classmethod
    def discover(cls) -> None:
        """Walk ``agents/`` and register every ``AgentBase`` subclass."""
        cls._agents.clear()
        if not AGENTS_DIR.is_dir():
            logger.warning("Agents directory not found: %s", AGENTS_DIR)
            return

        for agent_dir in sorted(AGENTS_DIR.iterdir()):
            if not agent_dir.is_dir() or agent_dir.name.startswith(("_", ".")):
                continue
            module_path = agent_dir / "agent.py"
            if not module_path.exists():
                continue
            module_name = f"agents.{agent_dir.name}.agent"
            try:
                mod = importlib.import_module(module_name)
                for attr in dir(mod):
                    obj = getattr(mod, attr)
                    if (
                        isinstance(obj, type)
                        and issubclass(obj, AgentBase)
                        and obj is not AgentBase
                    ):
                        cls._agents[obj.name] = obj
                        logger.debug("Registered agent: %s", obj.name)
            except Exception:
                logger.exception("Failed to load agent from %s", module_path)

    @classmethod
    def list_agents(cls) -> list[dict[str, Any]]:
        """Return metadata for all discovered agents."""
        if not cls._agents:
            cls.discover()
        return [
            {"name": a.name, "version": a.version, "description": a.description}
            for a in cls._agents.values()
        ]

    @classmethod
    def get(cls, name: str) -> type[AgentBase] | None:
        """Return the agent class registered under *name*."""
        if not cls._agents:
            cls.discover()
        return cls._agents.get(name)
