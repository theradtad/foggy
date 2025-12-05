"""Teach mode LangGraph workflow.

This module defines the teach mode graph for Foggy, which guides users through
interactive learning sessions based on their generated learning plan.

Version: 1.0.0 - Basic Setup Flow
"""

from langgraph.graph import StateGraph, START, END

from foggy.graph.models import TeachState
from foggy.graph.teach_nodes import (
    load_next_section_node,
    setup_env_node,
)
from foggy.graph.teach_edges import route_after_load


def create_teach_graph() -> StateGraph:
    """Create the teach mode LangGraph workflow.

    Basic flow (v1.0.0):
    START → Load Section → Setup Env → END

    This initial implementation focuses on:
    1. Loading the first incomplete section from learning_plan.json
    2. Generating setup.md with environment setup instructions

    Future iterations will add:
    - Orchestrator for managing subsections
    - Worker nodes for teaching content
    - Human feedback loops
    - Memory compaction
    - Progress tracking

    Returns:
        Compiled StateGraph ready for execution
    """
    # Create graph with TeachState
    workflow_builder = StateGraph(TeachState)

    # Add nodes
    workflow_builder.add_node("load_section", load_next_section_node)
    workflow_builder.add_node("setup_env", setup_env_node)

    workflow_builder.add_edge(START, "load_section")
    workflow_builder.add_edge("setup_env", END)

    workflow_builder.add_conditional_edges("load_section", route_after_load)

    return workflow_builder.compile()



# Create singleton instance
foggy_teach_graph = create_teach_graph()


def save_teach_graph_diagram(output_path: str = "docs/teach-graph-diagram.png") -> None:
    """Save teach graph visualization to file.

    Args:
        output_path: Path to save the diagram (default: docs/teach-graph-diagram.png)
    """
    from pathlib import Path

    try:
        # Get the graph
        graph = create_teach_graph()

        # Create output directory if needed
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)

        # Generate and save PNG
        png_data = graph.get_graph().draw_mermaid_png()

        with open(output_file, "wb") as f:
            f.write(png_data)

        print(f"✓ Teach graph diagram saved to: {output_path}")

    except Exception as e:
        print(f"✗ Could not generate teach graph diagram: {e}")
        print("\nMermaid diagram text:")
        try:
            print(graph.get_graph().draw_mermaid())
        except Exception:
            print("Could not generate mermaid text either")
