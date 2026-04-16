"""Niyam Agent SDK — public contracts for building agents.

This module defines the interface boundary between open-source agents and
the Niyam AIOL.  Everything in ``niyam.sdk`` is the stable public API
that agent authors depend on.
"""

from niyam.sdk.agent import AgentBase, AgentInput, AgentOutput
from niyam.sdk.protocols import Connector, ModelBackend

__all__ = [
    "AgentBase",
    "AgentInput",
    "AgentOutput",
    "Connector",
    "ModelBackend",
]
