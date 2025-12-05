"""LangGraph nodes for Foggy Teach Mode workflow.

This module contains all node implementations for the teach mode workflow.
Each node receives TeachState and returns updated state.

Version: 1.0.0
"""

import json
import os
from pathlib import Path
from typing import Literal

import click
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage, ToolMessage

from foggy.graph.models import TeachState, SectionInfo, SubsectionStatus
from foggy.graph.tools import read_file_tool, write_file_tool

# Load environment variables
load_dotenv()


def _get_llm() -> ChatGoogleGenerativeAI:
    """Get configured LLM instance.

    Returns:
        ChatGoogleGenerativeAI: Configured Gemini LLM instance
    """
    model_name = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
    return ChatGoogleGenerativeAI(
        model=model_name,
        google_api_key=os.getenv("GOOGLE_API_KEY"),
    )


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


def setup_env_node(state: TeachState) -> TeachState:
    """Generate setup instructions file for the current section.

    This node uses an agent to create a setup.md file with instructions
    for setting up the learning environment.

    Args:
        state: Current TeachState

    Returns:
        Updated TeachState with setup instructions created
    """
    if state.get("finished", False):
        click.echo(click.style("Exiting the setup node", fg="yellow"))
        return {
            "messages": state.get("messages", []),
            "learning_plan": state.get("learning_plan", {}),
            "goal": state.get("goal", ""),
            "current_section": state.get("current_section"),
            "current_subsection": state.get("current_subsection"),
            "completed_sections": state.get("completed_sections", []),
            "completed_subsections": state.get("completed_subsections", []),
            "isSetupFinished": True
        }


    current_section = state.get("current_section")

    # Early exit if no current section
    if not current_section:
        click.echo(click.style("⚠️  No section to set up", fg="yellow"))
        return {
            "messages": [SystemMessage(content="No section to set up")],
            "learning_plan": state.get("learning_plan", {}),
            "goal": state.get("goal", ""),
            "current_section": None,
            "current_subsection": None,
            "completed_sections": state.get("completed_sections", []),
            "completed_subsections": state.get("completed_subsections", []),
            "isSetupFinished": True
        }

    click.echo(click.style("\n🔧 Generating setup instructions...", fg="cyan", bold=True))
    click.echo(f"   Section: {current_section.name}")
    click.echo(f"   Description: {current_section.description}\n")

    SETUP_PROMPT = f"""
    You are an expert at creating clear and concise setup instructions for learning environments.
    Given a section details, generate step-by-step setup instructions that a student can follow to
    prepare their environment for learning.
    Provide the instructions in markdown format with appropriate headings and bullet points.

    Always check the existing setup.md file's contents and then update the file if necessary.
    If the existing setup.md is sufficient, do not make any changes.
    The existing setup file is present at the path: ./setup_instructions/setup.md.
    Use the read_file tool to read from existing files.
    Use the write_file tool to write to new files. This overwrites existing files.

    After the setup.md file is created or updated, inform the user that it has been updated.
    """

    setup_agent = create_agent(
        model=_get_llm(),
        tools=[read_file_tool, write_file_tool],
        system_prompt=SETUP_PROMPT
    )


    setup_generation_prompt = f"""
    Section Name: {current_section.name}
    Section Description: {current_section.description}
    Generate or update the setup.md file with clear setup instructions for this section.
    """

    click.echo(click.style("\n Foggy is generating your Setup Instructions...", fg="green"))
    response = setup_agent.invoke({"messages": [{"role": "user", "content": setup_generation_prompt.strip()}]})
    click.echo(click.style("✅ Setup Instructions are generated.", fg="green"))

    return {
        "messages": response["messages"],
        "learning_plan": state.get("learning_plan", {}),
        "goal": state.get("goal", ""),
        "current_section": None,
        "current_subsection": None,
        "completed_sections": state.get("completed_sections", []),
        "completed_subsections": state.get("completed_subsections", []),
        "isSetupFinished": True
    }