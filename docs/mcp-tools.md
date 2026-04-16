# Declaring MCP tools

Starter agents can declare the MCP tools they need in `config.yaml`:

```yaml
mcp_tools:
  - server: jira
    tool: jira_search
    required: true
  - server: jira
    tool: jira_create_issue
```

The AIOL reads these references, validates the corresponding MCP server is
configured in its mesh, and injects the tools into the orchestrator's
toolbox at runtime. If `required: true` and the tool is missing, the AIOL
fails fast on load.

The SDK itself stays dependency-free — no `fastmcp` import on the starters
side. See `niyam.sdk.mcp.MCPToolRef` for the full schema.

For the runtime side (server config, transports, JIRA wiring), see the
`niyam-aiol` repo's `docs/mcp-mesh.md`.
