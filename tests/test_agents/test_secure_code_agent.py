"""Tests for SecureCodeAgent (code generation & refactor)."""

from agents.secure_code_agent.agent import SecureCodeAgent

from niyam.sdk import AgentInput
from niyam.testing import MockBackend


def test_validates_missing_task_description():
    agent = SecureCodeAgent()
    result = agent.run(AgentInput(payload={}))
    assert result.status == "validation_error"
    assert any("task_description" in e for e in result.errors)


def test_validates_invalid_mode():
    agent = SecureCodeAgent()
    result = agent.run(
        AgentInput(
            payload={
                "task_description": "Do a thing.",
                "mode": "invent",
            }
        )
    )
    assert result.status == "validation_error"
    assert any("mode" in e for e in result.errors)


def test_refactor_requires_existing_code():
    agent = SecureCodeAgent()
    result = agent.run(
        AgentInput(
            payload={
                "task_description": "Refactor the login handler.",
                "mode": "refactor",
            }
        )
    )
    assert result.status == "validation_error"
    assert any("existing_code" in e for e in result.errors)


def test_validates_constraints_type():
    agent = SecureCodeAgent()
    result = agent.run(
        AgentInput(
            payload={
                "task_description": "Add a feature.",
                "constraints": "no new deps",
            }
        )
    )
    assert result.status == "validation_error"
    assert any("constraints" in e for e in result.errors)


def test_generate_mode_runs_with_minimal_input():
    agent = SecureCodeAgent()
    result = agent.run(
        AgentInput(payload={"task_description": "Create a hello endpoint."}),
        MockBackend(),
    )
    assert result.status == "success"
    assert result.result["mode"] == "generate"
    assert result.result["language"] == "python"
    assert result.result["existing_lines"] == 0
    assert "generation_result" in result.result


def test_refactor_mode_counts_existing_lines():
    agent = SecureCodeAgent()
    result = agent.run(
        AgentInput(
            payload={
                "task_description": "Refactor to use parameterized SQL.",
                "mode": "refactor",
                "language": "python",
                "existing_code": "a = 1\nb = 2\nc = 3",
            }
        ),
        MockBackend(),
    )
    assert result.status == "success"
    assert result.result["mode"] == "refactor"
    assert result.result["existing_lines"] == 3
    assert "generation_result" in result.result


def test_defaults_to_python_language():
    agent = SecureCodeAgent()
    result = agent.run(
        AgentInput(payload={"task_description": "Create a utility module."}),
        MockBackend(),
    )
    assert result.result["language"] == "python"
