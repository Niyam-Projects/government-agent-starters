"""Tests for the AgentRegistry (local runner discovery)."""

from niyam.runner.discovery import AgentRegistry


def test_discover_finds_agents():
    AgentRegistry.discover()
    agents = AgentRegistry.list_agents()
    assert len(agents) >= 5
    names = {a["name"] for a in agents}
    assert "requirements_architect_agent" in names
    assert "secure_code_agent" in names
    assert "compliance_audit_agent" in names
    assert "program_support_agent" in names
    assert "finops_review_agent" in names


def test_get_returns_agent_class():
    AgentRegistry.discover()
    cls = AgentRegistry.get("requirements_architect_agent")
    assert cls is not None
    assert cls.name == "requirements_architect_agent"


def test_get_returns_none_for_unknown():
    AgentRegistry.discover()
    cls = AgentRegistry.get("nonexistent_agent")
    assert cls is None
