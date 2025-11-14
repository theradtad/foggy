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
from typing import NoReturn

from foggy.conversation.dummy import DummyConversation


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
    click.echo("This is where personalized learning paths are created.")

    # Start dummy conversation
    conversation = DummyConversation()
    conversation.start_interactive("Planning")


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
