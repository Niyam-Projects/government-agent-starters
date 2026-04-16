"""Tests for ComplianceAuditAgent."""

from agents.compliance_audit_agent.agent import ComplianceAuditAgent

from niyam.sdk import AgentInput
from niyam.testing import MockBackend


def test_validates_missing_artifact():
    agent = ComplianceAuditAgent()
    result = agent.run(AgentInput(payload={"framework": "NIST 800-53"}))
    assert result.status == "validation_error"
    assert any("artifact" in e for e in result.errors)


def test_validates_missing_framework():
    agent = ComplianceAuditAgent()
    result = agent.run(AgentInput(payload={"artifact": "SSP excerpt"}))
    assert result.status == "validation_error"
    assert any("framework" in e for e in result.errors)


def test_runs_with_valid_input():
    agent = ComplianceAuditAgent()
    result = agent.run(
        AgentInput(
            payload={
                "artifact": "All data is encrypted at rest using AES-256.",
                "framework": "NIST 800-53",
                "controls": ["SC-28"],
            }
        ),
        MockBackend(),
    )
    assert result.status == "success"
    assert "compliance_analysis" in result.result
    assert result.result["framework"] == "NIST 800-53"
