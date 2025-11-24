from models import PlanState
from langgraph.graph import END
from typing import Literal
import click


def maybe_exit_human_node(state:PlanState) -> Literal["planner_node", "__end__"]:
    """"
        Decide whether to exit the human_node based on the current state.
    """
    click.echo("Deciding whether to exit human_node...")
    if state.finished:
        return END
    return "planner_node"


def maybe_route_to_tools(state: PlanState) -> Literal["tool_node", "write_plan_node", "human_node", "__end__"]:
    """
        Decide whether to route to tool_node or write_plan_node based on the current state.
    """
    click.echo("Deciding whether to route to tool_node or write_plan_node or exit...")
    if state.finished:
        return END
    
    msg = state.messages[-1] if state.messages else []
    tools_list = ["web_search", "create_todo", "update_todo_status", "read_todo", "get_pending_todos"]

    if hasattr(msg, "tool_calls") and len(msg.tool_calls) > 0:
        if any (call["tool_name"] in tools_list for call in msg.tool_calls):
            return "tool_node"
        else:
            return "write_plan_node"
    
    else:
        return "human_node"

    