"""Slim local CLI for agent development.

This is a minimal runner for developing and testing agents locally with
the mock backend.  It is NOT the production CLI — the Niyam AIOL provides
production security and operations.

For local agent development this is all you need.
"""

from __future__ import annotations

import json
import logging
import sys
from pathlib import Path
from typing import Annotated

import typer
from rich.console import Console
from rich.table import Table

from niyam import __version__
from niyam.runner.config import get_config
from niyam.runner.discovery import AgentRegistry
from niyam.sdk.agent import AgentInput
from niyam.testing.backends import MockBackend

app = typer.Typer(
    name="niyam",
    help=(
        "Niyam Agent Starters — local development runner.\n\n"
        "This CLI uses the mock backend for offline agent development. "
        "For production security and operations, deploy via the Niyam AIOL."
    ),
    add_completion=False,
)
console = Console()


def _configure_logging() -> None:
    level = get_config().log_level.upper()
    logging.basicConfig(
        level=getattr(logging, level, logging.INFO),
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    version: Annotated[
        bool | None,
        typer.Option("--version", "-V", help="Show version and exit.", is_eager=True),
    ] = None,
) -> None:
    """Niyam Agent Starters — local development runner."""
    if version:
        console.print(f"niyam {__version__}")
        raise typer.Exit
    if ctx.invoked_subcommand is None:
        console.print(ctx.get_help())
        raise typer.Exit


@app.command()
def list_agents() -> None:  # noqa: A001
    """List all available agents."""
    _configure_logging()
    agents = AgentRegistry.list_agents()
    if not agents:
        console.print("[yellow]No agents found.[/yellow]")
        raise typer.Exit

    table = Table(title="Available Agents")
    table.add_column("Name", style="cyan")
    table.add_column("Version")
    table.add_column("Description")
    for a in agents:
        table.add_row(a["name"], a["version"], a["description"])
    console.print(table)


@app.command()
def run(
    agent_name: Annotated[str, typer.Argument(help="Agent name to execute.")],
    input_file: Annotated[
        Path | None,
        typer.Option("--input", "-i", help="Path to JSON input file."),
    ] = None,
    payload: Annotated[
        str | None,
        typer.Option("--payload", "-p", help="Inline JSON payload."),
    ] = None,
    output_file: Annotated[
        Path | None,
        typer.Option("--output", "-o", help="Write output to file."),
    ] = None,
) -> None:
    """Run an agent locally with the mock backend."""
    _configure_logging()

    agent_cls = AgentRegistry.get(agent_name)
    if agent_cls is None:
        console.print(f"[red]Agent '{agent_name}' not found.[/red]")
        console.print("Run [cyan]niyam list-agents[/cyan] to see available agents.")
        raise typer.Exit(code=1)

    raw_payload: dict = {}
    if input_file:
        raw_payload = json.loads(input_file.read_text())
    elif payload:
        raw_payload = json.loads(payload)

    agent_input = AgentInput(payload=raw_payload)
    backend = MockBackend()

    config_path = Path("agents") / agent_name / "config.yaml"
    agent = agent_cls(config_path=config_path if config_path.exists() else None)

    console.print(f"[bold]Running agent:[/bold] {agent_name}  [dim](mock backend)[/dim]")
    result = agent.run(agent_input, backend)

    output_json = result.model_dump_json(indent=2)

    if output_file:
        output_file.parent.mkdir(parents=True, exist_ok=True)
        output_file.write_text(output_json)
        console.print(f"[green]Output written to {output_file}[/green]")
    else:
        console.print_json(output_json)

    if result.status != "success":
        sys.exit(1)


@app.command()
def info() -> None:
    """Show local runner configuration."""
    _configure_logging()
    config = get_config()
    table = Table(title="Local Runner Configuration")
    table.add_column("Setting", style="cyan")
    table.add_column("Value")
    for field_name in type(config).model_fields:
        table.add_row(field_name, str(getattr(config, field_name)))
    console.print(table)
    console.print(
        "\n[dim]This is the local development runner. "
        "For production security and operations, deploy via the Niyam AIOL.[/dim]"
    )
