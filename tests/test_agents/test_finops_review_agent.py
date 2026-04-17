"""Tests for FinOpsReviewAgent."""

from agents.finops_review_agent.agent import FinOpsReviewAgent

from niyam.sdk import AgentInput
from niyam.testing import MockBackend


def test_validates_missing_spend_data():
    agent = FinOpsReviewAgent()
    result = agent.run(AgentInput(payload={}))
    assert result.status == "validation_error"
    assert any("spend_data" in e for e in result.errors)


def test_runs_with_valid_input():
    agent = FinOpsReviewAgent()
    result = agent.run(
        AgentInput(
            payload={
                "spend_data": "Total monthly: $47,230. EC2: $18,400.",
                "period": "monthly",
                "cloud_provider": "aws",
            }
        ),
        MockBackend(),
    )
    assert result.status == "success"
    assert "finops_analysis" in result.result
    assert result.result["period"] == "monthly"
    assert result.result["cloud_provider"] == "aws"


def test_defaults_period_and_provider():
    agent = FinOpsReviewAgent()
    result = agent.run(
        AgentInput(payload={"spend_data": "Total: $10,000"}),
        MockBackend(),
    )
    assert result.result["period"] == "monthly"
    assert result.result["cloud_provider"] == "generic"
