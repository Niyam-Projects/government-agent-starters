from niyam.sdk.mcp import MCPToolRef, MCPToolRequirements


def test_qualified_name() -> None:
    ref = MCPToolRef(server="jira", tool="jira_search")
    assert ref.qualified_name == "jira_jira_search"


def test_qualified_name_none_when_no_tool() -> None:
    ref = MCPToolRef(server="jira")
    assert ref.qualified_name is None


def test_requirements_parse() -> None:
    data = {
        "mcp_tools": [
            {"server": "jira", "tool": "jira_search", "required": True},
            {"server": "github"},
        ]
    }
    reqs = MCPToolRequirements.model_validate(data)
    assert len(reqs.mcp_tools) == 2
    assert reqs.mcp_tools[0].required is True
    assert reqs.mcp_tools[1].tool is None
