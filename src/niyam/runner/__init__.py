"""Slim local runner for agent development.

This is a minimal, local-only shell for developing and testing agents.
It is NOT the Niyam AIOL — it only supports mock backends and is designed
for rapid agent iteration on a developer's machine.

The Niyam AIOL provides production security and operations.
"""

from niyam.runner.config import RunnerConfig, get_config
from niyam.runner.discovery import AgentRegistry

__all__ = [
    "AgentRegistry",
    "RunnerConfig",
    "get_config",
]
