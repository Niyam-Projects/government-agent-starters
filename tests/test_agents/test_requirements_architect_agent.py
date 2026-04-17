"""Tests for RequirementsArchitectAgent."""

from agents.requirements_architect_agent.agent import RequirementsArchitectAgent

from niyam.sdk import AgentInput
from niyam.testing import MockBackend


def test_validates_missing_inputs():
    agent = RequirementsArchitectAgent()
    result = agent.run(AgentInput(payload={}))
    assert result.status == "validation_error"
    assert any("requirements_text" in e or "artifacts" in e for e in result.errors)


def test_rejects_non_list_artifacts():
    agent = RequirementsArchitectAgent()
    result = agent.run(AgentInput(payload={"requirements_text": "x", "artifacts": "not-a-list"}))
    assert result.status == "validation_error"
    assert any("'artifacts' must be a list" in e for e in result.errors)


def test_runs_with_requirements_text():
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
    assert "architecture_package" in result.result
    assert result.result["input_length"] > 0
    assert result.result["artifact_count"] == 0
    assert result.result["model_used"] == "MockBackend"


def test_runs_with_artifacts_only():
    agent = RequirementsArchitectAgent()
    result = agent.run(
        AgentInput(
            payload={
                "artifacts": [
                    {
                        "type": "statement_of_work",
                        "name": "SOW-1",
                        "content": "Deliver a secure portal.",
                    }
                ]
            }
        ),
        MockBackend(),
    )
    assert result.status == "success"
    assert result.result["artifact_count"] == 1
    assert result.result["input_length"] == 0


def test_works_without_context():
    agent = RequirementsArchitectAgent()
    result = agent.run(
        AgentInput(payload={"requirements_text": "Must support MFA."}),
        MockBackend(),
    )
    assert result.status == "success"
