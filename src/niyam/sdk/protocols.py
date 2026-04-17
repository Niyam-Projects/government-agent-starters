"""Protocols that the Niyam AIOL implements.

These abstract interfaces define the contract between agents and the runtime.
The open-source repository provides *mock* implementations for local
development (see ``niyam.testing``).  The Niyam AIOL provides production
implementations.

Agent authors interact with these through ``model_backend.generate(prompt)``
and ``connector.fetch(query)`` — they never need to know which implementation
is backing them.
"""

from __future__ import annotations

import abc
from typing import Any


class ModelBackend(abc.ABC):
    """Interface every model backend must satisfy.

    Open-source: ``MockBackend`` (deterministic, offline).
    AIOL: Production model backends.
    """

    @abc.abstractmethod
    def generate(self, prompt: str, **kwargs: Any) -> str:
        """Send *prompt* to the model and return the completion text."""
        ...


class Connector(abc.ABC):
    """Interface for all data-source connectors.

    Open-source: ``MockConnector``, ``FileConnector`` (offline).
    AIOL: Production enterprise integrations.
    """

    @abc.abstractmethod
    def fetch(self, query: str, **kwargs: Any) -> dict[str, Any]:
        """Retrieve data matching *query*."""
        ...
