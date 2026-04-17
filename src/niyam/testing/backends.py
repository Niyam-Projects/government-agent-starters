"""Mock model backend for offline agent development."""

from __future__ import annotations

from typing import Any

from niyam.sdk.protocols import ModelBackend


class MockBackend(ModelBackend):
    """Deterministic offline backend for testing and local development.

    Returns a fixed response that includes the prompt length so tests can
    assert the agent rendered its template correctly.

    This is the *only* model backend in the open-source repo.  Production
    backends are provided by the Niyam AIOL.
    """

    def generate(self, prompt: str, **kwargs: Any) -> str:
        return (
            f"[MockBackend] Received prompt ({len(prompt)} chars). "
            "This is a placeholder response for local development. "
            "Deploy on the Niyam AIOL for production model inference."
        )
