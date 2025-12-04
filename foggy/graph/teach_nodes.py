"""LangGraph nodes for Foggy Teach Mode workflow.

This module contains all node implementations for the teach mode workflow.
Each node receives TeachState and returns updated state.

Version: 1.0.0
"""

import json
from pathlib import Path
from typing import Literal

import click
from langchain_core.messages import SystemMessage

from foggy.graph.models import TeachState, SectionInfo, SubsectionStatus


def load_next_section_node(state: TeachState) -> TeachState:
    """Load next incomplete section from learning plan.

    This is the entry point for Teach mode. It reads the plan from the
    learning_plans folder and initializes the current section to be taught.

    Args:
        state: Current TeachState

    Returns:
        Updated TeachState with current section info and loaded plan
    """
    learning_plan = state.get("learning_plan")

    # If plan not loaded yet, load from file
    if not learning_plan:
        plan_path = Path("learning_plans/learning_plan.json")
        if not plan_path.exists():
            click.echo(
                click.style(
                    "❌ Error: No learning plan found. Please run 'foggy plan' first.",
                    fg="red",
                )
            )
            error_message = SystemMessage(
                content="Error: No learning plan found. Please run 'foggy plan' first."
            )
            return {
                "messages": [error_message],
                "learning_plan": state.get("learning_plan", {}),
                "goal": state.get("goal", ""),
                "current_section": None,
                "current_subsection": None,
                "completed_sections": state.get("completed_sections", []),
                "completed_subsections": state.get("completed_subsections", []),
            }

        try:
            with open(plan_path, "r", encoding="utf-8") as f:
                learning_plan = json.load(f)
        except Exception as e:
            click.echo(
                click.style(f"❌ Error loading plan: {str(e)}", fg="red")
            )
            error_message = SystemMessage(
                content=f"Error loading learning plan: {str(e)}"
            )
            return {
                "messages": [error_message],
                "learning_plan": state.get("learning_plan", {}),
                "goal": state.get("goal", ""),
                "current_section": None,
                "current_subsection": None,
                "completed_sections": state.get("completed_sections", []),
                "completed_subsections": state.get("completed_subsections", []),
            }

    completed_sections = state.get("completed_sections", [])

    # Find next incomplete section
    for section_data in learning_plan.get("sections", []):
        section_id = section_data["id"]

        if section_id not in completed_sections:
            # Create SubsectionStatus objects
            subsections = [
                SubsectionStatus(
                    id=sub["id"],
                    name=sub["name"],
                    description=sub["description"],
                    concepts=sub.get("concepts", []),
                    isCompleted=sub.get("isCompleted", False),
                )
                for sub in section_data.get("subsections", [])
            ]

            # Create SectionInfo object
            current_section = SectionInfo(
                id=section_id,
                name=section_data["name"],
                description=section_data["description"],
                subsections=subsections,
            )

            click.echo(
                click.style(
                    f"\n📚 Starting section: {current_section.name}", fg="cyan", bold=True
                )
            )
            click.echo(f"   {current_section.description}\n")

            start_message = SystemMessage(
                content=f"Starting section: {current_section.name}"
            )

            return {
                "messages": [start_message],
                "learning_plan": learning_plan,
                "goal": learning_plan.get("goal", ""),
                "current_section": current_section,
                "current_subsection": None,  # Will be set by orchestrator
                "completed_sections": state.get("completed_sections", []),
                "completed_subsections": state.get("completed_subsections", []),
            }

    # All sections complete
    click.echo(
        click.style(
            "\n🎉 Congratulations! You've completed all sections of your learning plan!",
            fg="green",
            bold=True,
        )
    )
    completion_message = SystemMessage(
        content="🎉 Congratulations! You've completed all sections of your learning plan!"
    )

    return {
        "messages": [completion_message],
        "learning_plan": learning_plan,
        "goal": state.get("goal", ""),
        "current_section": None,
        "current_subsection": None,
        "completed_sections": state.get("completed_sections", []),
        "completed_subsections": state.get("completed_subsections", []),
    }


def route_after_load(state: TeachState) -> Literal["setup_env", "finish"]:
    """Route after loading section.

    Args:
        state: Current TeachState

    Returns:
        Next node to execute: "setup_env" if section loaded, "finish" if all complete
    """
    current_section = state.get("current_section")

    if current_section:
        return "setup_env"
    else:
        return "finish"
