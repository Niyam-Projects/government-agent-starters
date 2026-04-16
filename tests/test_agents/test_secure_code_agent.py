"""Tests for SecureCodeAgent."""

from agents.secure_code_agent.agent import SecureCodeAgent

from niyam.sdk import AgentInput
from niyam.testing import MockBackend


def test_validates_missing_source_code():
    agent = SecureCodeAgent()
    result = agent.run(AgentInput(payload={}))
    assert result.status == "validation_error"
    assert any("source_code" in e for e in result.errors)


def test_runs_with_valid_input():
    agent = SecureCodeAgent()
    result = agent.run(
        AgentInput(
            payload={
                "source_code": "import os\nos.system(input())",
                "language": "python",
            }
        ),
        MockBackend(),
    )
    assert result.status == "success"
    assert "security_review" in result.result
    assert result.result["lines_reviewed"] == 2
    assert result.result["language"] == "python"


def test_defaults_to_python():
    agent = SecureCodeAgent()
    result = agent.run(
        AgentInput(payload={"source_code": "print('hello')"}),
        MockBackend(),
    )
    assert result.result["language"] == "python"
