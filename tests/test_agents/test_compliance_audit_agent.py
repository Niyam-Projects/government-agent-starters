"""Tests for ComplianceAuditAgent (Compliance/Security/Accessibility Audit Loop)."""

from agents.compliance_audit_agent.agent import (
    DEFAULT_REVIEW_DOMAINS,
    OUTPUT_SECTIONS,
    SEVERITY_LEVELS,
    ComplianceAuditAgent,
)

from niyam.sdk import AgentInput
from niyam.testing import MockBackend


def test_validates_missing_artifact():
    agent = ComplianceAuditAgent()
    result = agent.run(AgentInput(payload={}))
    assert result.status == "validation_error"
    assert any("artifact" in e for e in result.errors)


def test_framework_is_optional_and_defaults_to_multi_domain():
    agent = ComplianceAuditAgent()
    result = agent.run(
        AgentInput(payload={"artifact": "print('hello')"}),
        MockBackend(),
    )
    assert result.status == "success"
    assert result.result["framework"] == "multi-domain"
    assert result.result["artifact_type"] == "mixed"


def test_runs_with_valid_input_and_populates_defaults():
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
    assert "audit_report" in result.result
    assert result.result["framework"] == "NIST 800-53"
    assert result.result["review_mode"] == "initial"
    assert result.result["domains_reviewed"] == list(DEFAULT_REVIEW_DOMAINS)
    assert result.result["severity_legend"] == list(SEVERITY_LEVELS)
    assert result.result["output_sections"] == list(OUTPUT_SECTIONS)
    assert result.result["confidence_labels"] == ["confirmed", "human_validation_required"]


def test_custom_review_domains_are_respected():
    agent = ComplianceAuditAgent()
    custom = ["secure_coding", "accessibility_508"]
    result = agent.run(
        AgentInput(
            payload={
                "artifact": "<button>ok</button>",
                "artifact_type": "ui",
                "review_domains": custom,
            }
        ),
        MockBackend(),
    )
    assert result.status == "success"
    assert result.result["domains_reviewed"] == custom
    assert result.result["artifact_type"] == "ui"


def test_review_domains_must_be_list():
    agent = ComplianceAuditAgent()
    result = agent.run(
        AgentInput(
            payload={
                "artifact": "x",
                "review_domains": "secure_coding",
            }
        )
    )
    assert result.status == "validation_error"
    assert any("review_domains" in e for e in result.errors)


def test_controls_must_be_list():
    agent = ComplianceAuditAgent()
    result = agent.run(
        AgentInput(
            payload={
                "artifact": "x",
                "controls": "AC-3",
            }
        )
    )
    assert result.status == "validation_error"
    assert any("controls" in e for e in result.errors)


def test_recheck_requires_both_previous_and_remediated():
    agent = ComplianceAuditAgent()
    result = agent.run(
        AgentInput(
            payload={
                "artifact": "x",
                "previous_findings": "SEC-001 SQL injection",
            }
        )
    )
    assert result.status == "validation_error"
    assert any("Re-check mode" in e for e in result.errors)


def test_recheck_mode_triggered_when_both_provided():
    agent = ComplianceAuditAgent()
    result = agent.run(
        AgentInput(
            payload={
                "artifact": "original",
                "previous_findings": "SEC-001 SQL injection in get_user",
                "remediated_artifact": "parameterized query now in use",
            }
        ),
        MockBackend(),
    )
    assert result.status == "success"
    assert result.result["review_mode"] == "recheck"
