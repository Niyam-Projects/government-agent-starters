"""Shared test fixtures."""

from __future__ import annotations

import pytest

from niyam.sdk import AgentInput
from niyam.testing import MockBackend


@pytest.fixture
def mock_backend() -> MockBackend:
    """Return a MockBackend instance."""
    return MockBackend()


@pytest.fixture
def empty_input() -> AgentInput:
    """Return an empty AgentInput."""
    return AgentInput()


@pytest.fixture
def sample_input() -> AgentInput:
    """Return an AgentInput with sample payload data."""
    return AgentInput(
        payload={"text": "Sample input for testing."},
        metadata={"source": "test"},
    )
