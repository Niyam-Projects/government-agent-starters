"""Example: run an agent programmatically with the mock backend.

Usage:
    python examples/run_agent_example.py
"""

from niyam.runner.discovery import AgentRegistry
from niyam.sdk import AgentInput
from niyam.testing import MockBackend


def main() -> None:
    AgentRegistry.discover()

    print("=== Available Agents ===")
    for agent_meta in AgentRegistry.list_agents():
        print(f"  {agent_meta['name']} v{agent_meta['version']}: {agent_meta['description']}")

    print("\n=== Running requirements_architect_agent ===")
    agent_cls = AgentRegistry.get("requirements_architect_agent")
    if agent_cls is None:
        print("Agent not found!")
        return

    agent = agent_cls()
    backend = MockBackend()

    agent_input = AgentInput(
        payload={
            "requirements_text": (
                "The system must support single sign-on via SAML 2.0. "
                "All API endpoints must enforce rate limiting. "
                "Data exports must be available in JSON and CSV formats."
            ),
            "context": "Internal tool for agency staff.",
        }
    )

    result = agent.run(agent_input, backend)
    print(f"  Status: {result.status}")
    print(f"  Result keys: {list(result.result.keys())}")
    print(f"  Timestamp: {result.timestamp}")


if __name__ == "__main__":
    main()
