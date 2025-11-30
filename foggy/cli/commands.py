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

from foggy.graph import foggy_planner_graph, PlanState, save_graph_diagram

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
    # Check for required API keys
    api_key: str = os.getenv('GOOGLE_API_KEY')
    tavily_key: str = os.getenv('TAVILY_API_KEY')

    if not api_key:
        click.echo("❌ Error: GOOGLE_API_KEY not found in environment variables.")
        click.echo("Please set your Google API key in the .env file.")
        return

    if not tavily_key:
        click.echo("⚠️  Warning: TAVILY_API_KEY not found. Web search functionality will be limited.")

    try:
        save_graph_diagram()
        # Initialize empty state
        initial_state = PlanState(messages=[], todo=[], finished=False)
        # Run the planning graph
        final_state = foggy_planner_graph.invoke(initial_state)

        click.echo("\n✅ Planning completed successfully!")
        
        for todo in final_state.get("todo", []):
            status = "✔️" if todo.isFinished else "❌"
            click.echo(f"{status} {todo.name}")

        click.echo("Your personalized learning plan has been generated.")

    except KeyboardInterrupt:
        click.echo("\n\n⚠️  Planning interrupted by user.")
        click.echo("Your progress has been saved. Run 'foggy plan' again to continue.")
    except Exception as e:
        click.echo(f"\n❌ Error during planning: {str(e)}")
        click.echo("Please check your configuration and try again.")


@cli_group.command()
def teach() -> None:
    """Access interactive teaching sessions and lessons.

    This command starts teaching interactions where Foggy provides
    hands-on learning experiences, code examples, and guided practice
    sessions adapted to your learning style.
    """
    click.echo("📚 Welcome to Foggy's Teaching Module!")
    click.echo("Let's start learning through examples and projects.")


@cli_group.command()
def evaluate() -> None:
    """Assess your learning progress and provide feedback.

    This command begins assessment sessions where Foggy evaluates
    your understanding, identifies knowledge gaps, and provides
    constructive feedback to guide your learning journey.
    """
    click.echo("📊 Welcome to Foggy's Evaluation Module!")
    click.echo("Let's assess your progress and identify areas for growth.")