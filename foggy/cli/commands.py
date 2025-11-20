"""CLI command definitions for the Foggy application.

This module defines all Click commands and command groups for the Foggy
CLI interface. Each command provides access to different aspects of the
tutoring system.

Commands:
    plan: Generate learning plans and paths
    teach: Access teaching interactions
    evaluate: Assess learning progress
"""

import click
import os
from typing import NoReturn

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain.agents import create_agent
from langchain.agents.middleware import TodoListMiddleware

from foggy.conversation.dummy import DummyConversation
from foggy.prompts import PLANNING_SYSTEM_PROMPT, PLANNING_EXAMPLE_GOAL, PLANNING_EXAMPLE_PLAN, PLANNING_EXAMPLE_TODO_LIST
from foggy.tools import get_planning_tools

# Load environment variables
load_dotenv()


@click.group()
@click.version_option(version="0.1.0", prog_name="foggy")
def cli_group() -> NoReturn:
    """Foggy - Your Personalized Coding Tutor.

    An AI-powered learning system that adapts to your individual learning needs
    through structured, project-based learning approaches.
    """
    pass


@cli_group.command()
def plan() -> None:
    """Generate personalized learning plans and study paths.

    This command initiates the planning phase where Foggy analyzes your
    learning goals, current knowledge, and creates customized learning
    journeys tailored to your needs.
    """
    click.echo("🎯 Welcome to Foggy's Planning Module!")
    goal = click.prompt("What is your learning goal? (e.g., 'Learn React', 'Master Python classes')")

    # Get API key and model from environment
    api_key: str = os.getenv('GOOGLE_API_KEY')
    model_name: str = os.getenv('GEMINI_MODEL', 'gemini-2.5-flash')

    if not api_key:
        click.echo("❌ Error: GOOGLE_API_KEY not found in environment variables.")
        click.echo("Please set your Google API key in the .env file.")
        return

    # Initialize the LLM
    llm: ChatGoogleGenerativeAI = ChatGoogleGenerativeAI(
        model=model_name,
        google_api_key=api_key,
        temperature=0.7
    )

    # Prepare the input with one-shot example
    planning_prompt: str = f"""
    Here is an example of a todo list for creating a learning plan:
    Example Todo List: {PLANNING_EXAMPLE_TODO_LIST.strip()}

    Here is an example of how to create a learning plan:

    Example Goal: {PLANNING_EXAMPLE_GOAL.strip()}

    Example Response:
    {PLANNING_EXAMPLE_PLAN.strip()}

    """

    SYS_PROMPT: str = PLANNING_SYSTEM_PROMPT + planning_prompt

    # Create the planning agent with system prompt
    agent = create_agent(llm, tools=get_planning_tools(), system_prompt=SYS_PROMPT)

    config: dict = {"configurable": {"thread_id": "planning_thread"}}

    inference_prompt: str = f"""
    Now, create a comprehensive learning plan for: "{goal}"
    """

    try:
        # Invoke the agent
        result = agent.invoke(
            {"messages": [HumanMessage(content=inference_prompt)]},
            config=config
        )

        # Extract the final message content
        final_message = result['messages'][-1]
        plan_content = final_message.content

        # Display the generated plan
        click.echo("\n" + "="*60)
        click.echo("🎯 GENERATED LEARNING PLAN")
        click.echo("="*60)
        click.echo(plan_content)
        click.echo("="*60 + "\n")

        click.echo("✅ Plan generated successfully! You can now use 'foggy teach' to start learning.")

    except Exception as e:
        click.echo(f"❌ Error generating plan: {str(e)}")
        click.echo("Please check your API key and internet connection.")


@cli_group.command()
def teach() -> None:
    """Access interactive teaching sessions and lessons.

    This command starts teaching interactions where Foggy provides
    hands-on learning experiences, code examples, and guided practice
    sessions adapted to your learning style.
    """
    click.echo("📚 Welcome to Foggy's Teaching Module!")
    click.echo("Let's start learning through examples and projects.")

    # Start dummy conversation
    conversation = DummyConversation()
    conversation.start_interactive("Teaching")


@cli_group.command()
def evaluate() -> None:
    """Assess your learning progress and provide feedback.

    This command begins assessment sessions where Foggy evaluates
    your understanding, identifies knowledge gaps, and provides
    constructive feedback to guide your learning journey.
    """
    click.echo("📊 Welcome to Foggy's Evaluation Module!")
    click.echo("Let's assess your progress and identify areas for growth.")

    # Start dummy conversation
    conversation = DummyConversation()
    conversation.start_interactive("Evaluation")
