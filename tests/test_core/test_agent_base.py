"""Tests for the AgentBase class (SDK contract)."""

from __future__ import annotations

import importlib.util
import sys
from typing import Any

from niyam.sdk import AgentBase, AgentInput, AgentOutput
from niyam.testing import MockBackend


class _StubAgent(AgentBase):
    name = "stub_agent"
    version = "0.1.0"
    description = "Test stub"

    def _run(self, agent_input: AgentInput, model_backend: Any) -> dict[str, Any]:
        return {"echo": agent_input.payload.get("text", "")}


class _FailingAgent(AgentBase):
    name = "failing_agent"
    version = "0.1.0"
    description = "Always fails"

    def _run(self, agent_input: AgentInput, model_backend: Any) -> dict[str, Any]:
        msg = "Something went wrong"
        raise RuntimeError(msg)


class _ValidatingAgent(AgentBase):
    name = "validating_agent"
    version = "0.1.0"
    description = "Validates input"

    def validate_input(self, agent_input: AgentInput) -> list[str]:
        if not agent_input.payload.get("required_field"):
            return ["'required_field' is required"]
        return []

    def _run(self, agent_input: AgentInput, model_backend: Any) -> dict[str, Any]:
        return {"ok": True}


def test_agent_output_structure():
    agent = _StubAgent()
    result = agent.run(AgentInput(payload={"text": "hello"}), MockBackend())
    assert isinstance(result, AgentOutput)
    assert result.agent_name == "stub_agent"
    assert result.status == "success"
    assert result.result == {"echo": "hello"}
    assert result.errors == []
    assert result.timestamp


def test_agent_error_handling():
    agent = _FailingAgent()
    result = agent.run(AgentInput(), MockBackend())
    assert result.status == "error"
    assert len(result.errors) == 1
    assert "Something went wrong" in result.errors[0]


def test_agent_validation():
    agent = _ValidatingAgent()
    result = agent.run(AgentInput(payload={}), MockBackend())
    assert result.status == "validation_error"
    assert "'required_field' is required" in result.errors


def test_agent_validation_passes():
    agent = _ValidatingAgent()
    result = agent.run(AgentInput(payload={"required_field": "present"}), MockBackend())
    assert result.status == "success"


def test_agent_input_defaults():
    inp = AgentInput()
    assert inp.payload == {}
    assert inp.metadata == {}


def test_agent_output_serialization():
    output = AgentOutput(agent_name="test", result={"key": "value"})
    data = output.model_dump()
    assert data["agent_name"] == "test"
    assert data["status"] == "success"
    json_str = output.model_dump_json()
    assert "test" in json_str


def test_agent_base_loads_prompt_from_subclass_directory(tmp_path):
    prompt_path = tmp_path / "prompt.md"
    prompt_path.write_text("Prompt from subclass directory")

    module_path = tmp_path / "temp_agent.py"
    module_path.write_text(
        """
from __future__ import annotations

from typing import Any

from niyam.sdk import AgentBase, AgentInput


class TempAgent(AgentBase):
    name = "temp_agent"

    def _run(self, agent_input: AgentInput, model_backend: Any) -> dict[str, Any]:
        return {"prompt": self.prompt_template}
"""
    )

    spec = importlib.util.spec_from_file_location("temp_agent_module", module_path)
    assert spec is not None
    assert spec.loader is not None

    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    try:
        spec.loader.exec_module(module)
        agent = module.TempAgent()
        assert agent.prompt_template == "Prompt from subclass directory"
    finally:
        sys.modules.pop(spec.name, None)
