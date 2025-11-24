from dotenv import load_dotenv
# from IPython.display import Image, display

from edges import maybe_exit_human_node, maybe_route_to_tools
from foggy.graph.models import PlanState
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode
from foggy.graph.nodes import (
    welcome_message_node,
    human_goal_node,
    todo_list_generator_node,
    human_node,
    planner_node,
    write_plan_node
)

from foggy.graph.tools import (
    web_search,
    create_todo,
    update_todo_status,
    read_todo,
    get_pending_todos,
    save_learning_plan,
)

# Load environment variables
load_dotenv()

# Define all available tools
AUTO_TOOLS = [
    web_search,
    create_todo,
    update_todo_status,
    read_todo,
    get_pending_todos,
]

tool_node = ToolNode(AUTO_TOOLS)

foggy_planner_graph_builder = StateGraph(PlanState)

foggy_planner_graph_builder.add_node("welcome_message_node", welcome_message_node)
foggy_planner_graph_builder.add_node("human_goal_node", human_goal_node)
foggy_planner_graph_builder.add_node("todo_list_generator_node", todo_list_generator_node)
foggy_planner_graph_builder.add_node("planner_node", planner_node)
foggy_planner_graph_builder.add_node("human_node", human_node)
foggy_planner_graph_builder.add_node("tool_node", tool_node)
foggy_planner_graph_builder.add_node("write_plan_node", write_plan_node)

foggy_planner_graph_builder.add_conditional_edges("planner_node", maybe_route_to_tools)
foggy_planner_graph_builder.add_conditional_edges("human_node", maybe_exit_human_node)

foggy_planner_graph_builder.add_edge(START, "welcome_message_node")
foggy_planner_graph_builder.add_edge("welcome_message_node", "human_goal_node")
foggy_planner_graph_builder.add_edge("human_goal_node", "todo_list_generator_node")
foggy_planner_graph_builder.add_edge("todo_list_generator_node", "planner_node")
foggy_planner_graph_builder.add_edge("tool_node", "planner_node")
foggy_planner_graph_builder.add_edge("write_plan_node", "planner_node")

# foggy_planner_graph = foggy_planner_graph_builder.build()
# Image(foggy_planner_graph().draw_mermaid_png())