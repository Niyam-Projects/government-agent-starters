"""Mock implementations for local agent development and testing.

These are the ONLY backend/connector implementations shipped in the
open-source repository.  They work fully offline with deterministic output
so agent authors can develop and test without any external services.
"""

from niyam.testing.backends import MockBackend
from niyam.testing.connectors import FileConnector, MockConnector

__all__ = [
    "FileConnector",
    "MockBackend",
    "MockConnector",
]
