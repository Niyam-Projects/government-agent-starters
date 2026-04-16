"""Minimal configuration for the local runner.

Only what's needed for local development.  The Niyam AIOL has its own
configuration system for production environments.
"""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class RunnerConfig(BaseSettings):
    """Local runner settings — loaded from environment / ``.env``."""

    model_config = SettingsConfigDict(
        env_prefix="NIYAM_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    log_level: str = "INFO"
    output_dir: Path = Path("./outputs")


@lru_cache(maxsize=1)
def get_config() -> RunnerConfig:
    """Return a cached singleton config instance."""
    return RunnerConfig()
