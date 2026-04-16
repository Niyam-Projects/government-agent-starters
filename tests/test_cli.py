"""Tests for the local runner CLI."""

from typer.testing import CliRunner

from niyam.runner.cli import app

runner = CliRunner()


def test_version_flag():
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    assert "niyam" in result.stdout


def test_list_agents():
    result = runner.invoke(app, ["list-agents"])
    assert result.exit_code == 0


def test_info():
    result = runner.invoke(app, ["info"])
    assert result.exit_code == 0
    assert "log_level" in result.stdout


def test_run_unknown_agent():
    result = runner.invoke(app, ["run", "nonexistent_agent"])
    assert result.exit_code == 1
    assert "not found" in result.stdout


def test_run_agent_with_inline_payload():
    result = runner.invoke(
        app,
        [
            "run",
            "requirements_architect_agent",
            "--payload",
            '{"requirements_text": "The system must support SSO."}',
        ],
    )
    assert result.exit_code == 0
    assert "success" in result.stdout


def test_run_agent_validation_error():
    result = runner.invoke(
        app,
        [
            "run",
            "requirements_architect_agent",
            "--payload",
            "{}",
        ],
    )
    assert result.exit_code == 1
    assert "validation_error" in result.stdout
