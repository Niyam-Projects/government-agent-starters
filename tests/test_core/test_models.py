"""Tests for mock model backend."""

from niyam.testing import MockBackend


def test_mock_backend_returns_string():
    backend = MockBackend()
    result = backend.generate("test prompt")
    assert isinstance(result, str)
    assert "MockBackend" in result


def test_mock_backend_includes_prompt_length():
    backend = MockBackend()
    result = backend.generate("hello world")
    assert "11 chars" in result
