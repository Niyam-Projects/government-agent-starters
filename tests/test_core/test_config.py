"""Tests for RunnerConfig."""

from pathlib import Path

from niyam.runner.config import RunnerConfig


def test_default_config():
    config = RunnerConfig()
    assert config.log_level == "INFO"


def test_config_output_dir_is_path():
    config = RunnerConfig()
    assert isinstance(config.output_dir, Path)


def test_config_from_env(monkeypatch):
    monkeypatch.setenv("NIYAM_LOG_LEVEL", "DEBUG")
    config = RunnerConfig()
    assert config.log_level == "DEBUG"
