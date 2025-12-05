"""LangGraph module for Foggy CLI.

This module contains all LangGraph-related components including:
- State models (PlanState, Task, TeachState)
- Tools (web_search, create_todo, save_learning_plan, etc.)
- Nodes (welcome_message_node, planner_node, teach nodes, etc.)
- Graphs (foggy_planner_graph, foggy_teach_graph)
"""

from foggy.graph.models import PlanState, Task, TeachState
from foggy.graph.tools import (
    web_search,
    create_todo,
    update_todo_status,
    read_todo,
    get_pending_todos,
    save_learning_plan,
    should_continue_planning,
    read_file_tool,
    write_file_tool,
)
from foggy.graph.nodes import (
    welcome_message_node,
    human_goal_node,
    todo_list_generator_node,
    human_node,
    planner_node,
    structure_learning_plan_node,
    ALL_TOOLS,
)
from foggy.graph.graph import foggy_planner_graph, save_graph_diagram
from foggy.graph.teach_graph import foggy_teach_graph, save_teach_graph_diagram

__all__ = [
    # Models
    "PlanState",
    "Task",
    "TeachState",
    # Tools
    "web_search",
    "create_todo",
    "update_todo_status",
    "read_todo",
    "get_pending_todos",
    "save_learning_plan",
    "should_continue_planning",
    "read_file_tool",
    "write_file_tool",
    # Nodes
    "welcome_message_node",
    "human_goal_node",
    "todo_list_generator_node",
    "human_node",
    "planner_node",
    "structure_learning_plan_node",
    "ALL_TOOLS",
    # Graph
    "foggy_planner_graph",
    "save_graph_diagram",
    "foggy_teach_graph",
    "save_teach_graph_diagram",
]
