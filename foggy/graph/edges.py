from foggy.graph.models import PlanState
from langgraph.graph import END
from typing import Literal
import click


def maybe_exit_human_node(state: PlanState) -> Literal["planner_node", "__end__"]:
    """Decide whether to exit the human_node based on the current state.

    Args:
        state: Current PlanState

    Returns:
        Either "planner_node" to continue or END to finish
    """
    if state.get("finished", False):
        click.echo(click.style("\n🚪 Edge: Exiting workflow (finished=True)", fg="cyan", bold=True))
        return END
    click.echo(click.style("\n➡️ Edge: Routing to planner_node", fg="cyan", bold=True))
    return "planner_node"


def maybe_route_to_tools(state: PlanState) -> Literal["tool_node", "structure_learning_plan_node", "human_node", "__end__"]:
    """Decide whether to route to tool_node, structure_learning_plan_node, or human_node.

    Args:
        state: Current PlanState

    Returns:
        One of: "tool_node", "structure_learning_plan_node", "human_node", or END
    """
    if state.get("finished", False):
        click.echo(click.style("\n🚪 Edge: Exiting workflow (finished=True)", fg="cyan", bold=True))
        return END

    msgs = state.get("messages", [])
    if msgs and hasattr(msgs[-1], "tool_calls") and msgs[-1].tool_calls:
        # Check if save_learning_plan is in the tool calls
        for tool_call in msgs[-1].tool_calls:
            if tool_call.get("name") == "save_learning_plan":
                click.echo(click.style("\n➡️ Edge: Routing to structure_learning_plan_node (save_learning_plan detected)", fg="cyan", bold=True))
                return "structure_learning_plan_node"

        # Otherwise route to regular tool node
        click.echo(click.style("\n➡️ Edge: Routing to tool_node (tool calls detected)", fg="cyan", bold=True))
        return "tool_node"
    else:
        click.echo(click.style("\n➡️ Edge: Routing to human_node (no tool calls)", fg="cyan", bold=True))
        return "human_node"
    