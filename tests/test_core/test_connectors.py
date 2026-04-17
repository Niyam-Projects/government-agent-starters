"""Tests for mock connectors."""

from niyam.testing import MockConnector


def test_mock_connector_returns_dict():
    connector = MockConnector()
    result = connector.fetch("test query")
    assert result["source"] == "mock"
    assert result["query"] == "test query"
    assert "records" in result
