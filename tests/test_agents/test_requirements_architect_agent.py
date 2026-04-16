"""Tests for RequirementsArchitectAgent."""

from agents.requirements_architect_agent.agent import RequirementsArchitectAgent

from niyam.sdk import AgentInput
from niyam.testing import MockBackend


def test_validates_missing_requirements_text():
    agent = RequirementsArchitectAgent()
    result = agent.run(AgentInput(payload={}))
    assert result.status == "validation_error"
    assert any("requirements_text" in e for e in result.errors)


def test_runs_with_valid_input():
    agent = RequirementsArchitectAgent()
    result = agent.run(
        AgentInput(
            payload={
                "requirements_text": "The system must support SSO.",
                "context": "Enterprise application",
            }
        ),
        MockBackend(),
    )
    assert result.status == "success"
    assert "structured_requirements" in result.result
    assert result.result["input_length"] > 0
    assert result.result["model_used"] == "MockBackend"


def test_works_without_context():
    agent = RequirementsArchitectAgent()
    result = agent.run(
        AgentInput(payload={"requirements_text": "Must support MFA."}),
        MockBackend(),
    )
    assert result.status == "success"
