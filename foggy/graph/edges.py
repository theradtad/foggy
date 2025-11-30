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
    click.echo("Deciding whether to exit human_node...")
    if state.finished:
        return END
    return "planner_node"


def maybe_route_to_tools(state: PlanState) -> Literal["tool_node", "write_plan_node", "human_node", "__end__"]:
    """Decide whether to route to tool_node or write_plan_node based on the current state.

    Args:
        state: Current PlanState

    Returns:
        One of: "tool_node", "write_plan_node", "human_node", or END
    """
    click.echo("Deciding whether to route to tool_node or write_plan_node or exit...")
    try:
        if state.finished:
            return END

        click.echo(f"State messages: {state.messages}")
        click.echo("------------------------------------------------------")
        msg = state.messages[-1] if state.messages else None
        click.echo(f"Last message: {msg}")
        click.echo(type(msg))
        tools_list = ["web_search", "create_todo", "update_todo_status", "read_todo", "get_pending_todos"]

        if msg and hasattr(msg, "tool_calls") and len(msg.tool_calls) > 0:
            # Check if any tool call is in the auto tools list
            # tool_calls is a list of dicts with 'name', 'args', 'id', 'type'
            for call in msg.tool_calls:
                click.echo(f"Tool call: {call}")
            # If we get here, none of the tool calls are in the auto tools list
            # So it must be save_learning_plan
            return "write_plan_node"
        else:
            # No tool calls, go back to human for feedback
            return "human_node"
    except Exception as e:
        click.echo(f"Error in maybe_route_to_tools: {e}")
        click.echo(f"State type: {type(state)}")
        click.echo(f"State: {state}")
        raise

    