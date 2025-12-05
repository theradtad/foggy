from foggy.graph.models import TeachState
from langgraph.graph import END
from typing import Literal
import click


def route_after_load(state: TeachState) -> Literal["setup_env", "__end__"]:
    """Route after loading section.

    Args:
        state: Current TeachState

    Returns:
        Next node to execute: "setup_env" if section loaded, "finish" if all complete
    """
    click.echo(click.style("\n➡️ Edge: Routing after load_section_node", fg="cyan", bold=True))
    current_section = state.get("current_section")

    if current_section:
        return "setup_env"
    else:
        return END