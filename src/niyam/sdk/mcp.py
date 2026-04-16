"""Declarative contract for MCP-backed tools.

Starter agents remain dep-free: they *describe* what MCP tools they want,
the AIOL (or any runtime that implements the contract) wires them up.

Example (in an agent's config.yaml):

    mcp_tools:
      - server: jira
        tool: jira_search
        required: true
      - server: jira
        tool: jira_create_issue
"""

from __future__ import annotations

from pydantic import BaseModel, Field


class MCPToolRef(BaseModel):
    """Reference to a tool exposed by an MCP server."""

    server: str = Field(description="MCP server name (matches the mesh entry).")
    tool: str | None = Field(
        default=None,
        description="Unprefixed tool name. Omit to request all tools on the server.",
    )
    required: bool = Field(
        default=False,
        description="If True, the runtime must raise when the tool is unavailable.",
    )
    description: str = ""

    @property
    def qualified_name(self) -> str | None:
        """Full name as exposed by the mesh (``<server>_<tool>``)."""
        return f"{self.server}_{self.tool}" if self.tool else None


class MCPToolRequirements(BaseModel):
    """Collection wrapper — convenient for ``config.yaml`` parsing."""

    mcp_tools: list[MCPToolRef] = Field(default_factory=list)
