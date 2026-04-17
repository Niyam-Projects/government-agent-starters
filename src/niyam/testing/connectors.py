"""Mock connectors for offline agent development."""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any

from niyam.sdk.protocols import Connector

logger = logging.getLogger(__name__)


class MockConnector(Connector):
    """Returns canned sample data — works fully offline.

    Optionally loads fixture data from a JSON file so agents can test
    against realistic payloads without hitting external services.
    """

    def __init__(self, sample_path: Path | None = None) -> None:
        self._data: dict[str, Any] = {}
        if sample_path and sample_path.exists():
            self._data = json.loads(sample_path.read_text())

    def fetch(self, query: str, **kwargs: Any) -> dict[str, Any]:
        logger.info("MockConnector: query=%s", query)
        return {
            "source": "mock",
            "query": query,
            "records": self._data.get("records", []),
            "total": self._data.get("total", 0),
        }


class FileConnector(Connector):
    """Read data from a local JSON file — useful for demos and examples."""

    def __init__(self, base_dir: Path | None = None) -> None:
        self.base_dir = base_dir or Path()

    def fetch(self, query: str, **kwargs: Any) -> dict[str, Any]:
        target = self.base_dir / query
        if not target.exists():
            return {"source": "file", "error": f"File not found: {target}"}
        return {"source": "file", "data": json.loads(target.read_text())}
