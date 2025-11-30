from dotenv import load_dotenv

from foggy.graph.edges import maybe_exit_human_node, maybe_route_to_tools
from foggy.graph.models import PlanState
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode
from foggy.graph.nodes import (
    welcome_message_node,
    human_goal_node,
    todo_list_generator_node,
    human_node,
    planner_node
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
    save_learning_plan,
]

tool_node = ToolNode(AUTO_TOOLS)

foggy_planner_graph_builder = StateGraph(PlanState)

foggy_planner_graph_builder.add_node("welcome_message_node", welcome_message_node)
foggy_planner_graph_builder.add_node("human_goal_node", human_goal_node)
foggy_planner_graph_builder.add_node("todo_list_generator_node", todo_list_generator_node)
foggy_planner_graph_builder.add_node("planner_node", planner_node)
foggy_planner_graph_builder.add_node("human_node", human_node)
foggy_planner_graph_builder.add_node("tool_node", tool_node)
# foggy_planner_graph_builder.add_node("write_plan_node", write_plan_node)

foggy_planner_graph_builder.add_conditional_edges("planner_node", maybe_route_to_tools)
foggy_planner_graph_builder.add_conditional_edges("human_node", maybe_exit_human_node)

foggy_planner_graph_builder.add_edge(START, "welcome_message_node")
foggy_planner_graph_builder.add_edge("welcome_message_node", "human_goal_node")
foggy_planner_graph_builder.add_edge("human_goal_node", "todo_list_generator_node")

foggy_planner_graph_builder.add_edge("todo_list_generator_node", "planner_node")
foggy_planner_graph_builder.add_edge("tool_node", "planner_node")
# foggy_planner_graph_builder.add_edge("write_plan_node", "planner_node")

# Build the graph
foggy_planner_graph = foggy_planner_graph_builder.compile()


def save_graph_diagram(output_path: str = "docs/foggy_planner_graph.png") -> str:
    """Save the graph visualization as a Mermaid diagram.

    Args:
        output_path: Path where to save the diagram (default: docs/foggy_planner_graph.png)

    Returns:
        Path to the saved diagram file
    """
    from pathlib import Path

    # Ensure the directory exists
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    # Generate and save the Mermaid PNG
    try:
        png_data = foggy_planner_graph.get_graph().draw_mermaid_png()
        with open(output_file, "wb") as f:
            f.write(png_data)
        return str(output_file)
    except Exception:
        # If PNG generation fails, save as Mermaid text
        mermaid_text = foggy_planner_graph.get_graph().draw_mermaid()
        text_file = output_file.with_suffix('.mmd')
        with open(text_file, "w") as f:
            f.write(mermaid_text)
        return str(text_file)