"""Tests for ProgramSupportAgent."""

from agents.program_support_agent.agent import ProgramSupportAgent

from niyam.sdk import AgentInput
from niyam.testing import MockBackend


def test_validates_missing_project_data():
    agent = ProgramSupportAgent()
    result = agent.run(AgentInput(payload={"artifact_type": "weekly_status_report"}))
    assert result.status == "validation_error"
    assert any("project_data" in e for e in result.errors)


def test_validates_missing_artifact_type():
    agent = ProgramSupportAgent()
    result = agent.run(AgentInput(payload={"project_data": "Sprint 14 complete."}))
    assert result.status == "validation_error"
    assert any("artifact_type" in e for e in result.errors)


def test_runs_with_valid_input():
    agent = ProgramSupportAgent()
    result = agent.run(
        AgentInput(
            payload={
                "project_data": "Sprint 14 complete. 3 of 5 items done.",
                "artifact_type": "weekly_status_report",
                "audience": "executive_leadership",
            }
        ),
        MockBackend(),
    )
    assert result.status == "success"
    assert "generated_artifact" in result.result
    assert result.result["artifact_type"] == "weekly_status_report"


def test_runs_decision_memo_for_audit_board():
    agent = ProgramSupportAgent()
    result = agent.run(
        AgentInput(
            payload={
                "project_data": "Decision: approve IAM timeline slip +1 week.",
                "artifact_type": "decision_memo",
                "audience": "audit_review_board",
            }
        ),
        MockBackend(),
    )
    assert result.status == "success"
    assert result.result["artifact_type"] == "decision_memo"
