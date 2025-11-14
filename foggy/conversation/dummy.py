"""Dummy conversation implementation for simulating AI tutor interactions.

This module provides a DummyConversation class that simulates realistic
conversations with an AI tutor through random response generation and
interactive dialogue management.
"""

import random
import time
from typing import Dict, List, Optional

import click

from foggy.conversation.responses import get_greeting, get_random_response


class DummyConversation:
    """Dummy conversation handler that simulates AI tutor interactions.

    This class manages conversational state, simulates API-like delays,
    and provides realistic responses for different learning contexts.

    Attributes:
        context: The conversation context (e.g., "Planning", "Teaching", "Evaluation").
        history: List of conversation exchanges as (user_input, foggy_response) tuples.
        is_active: Boolean flag indicating if the conversation is currently active.
    """

    def __init__(self) -> None:
        """Initialize a new dummy conversation instance."""
        self.context: str = ""
        self.history: List[tuple[str, str]] = []
        self.is_active: bool = False

    def _simulate_api_call(self, user_input: str) -> str:
        """Simulate an AI API call with realistic response time and variability.

        Args:
            user_input: The user's input message to respond to.

        Returns:
            A randomly selected response appropriate for the conversation context.
        """
        # Simulate API processing time (0.5-2.0 seconds)
        delay = random.uniform(0.5, 2.0)
        time.sleep(delay)

        # Check for context-appropriate responses
        context_responses = {
            "Planning": "planning",
            "Teaching": "teaching",
            "Evaluation": "evaluation"
        }

        response_context = context_responses.get(self.context, "general")
        return get_random_response(response_context)

    def _display_response(self, response: str) -> None:
        """Display Foggy's response with appropriate formatting.

        Args:
            response: The response message to display.
        """
        click.echo("")  # Add spacing
        click.echo("🤖 Foggy: " + response)
        click.echo("")  # Add spacing

    def _is_exit_command(self, user_input: str) -> bool:
        """Check if the user input is an exit command.

        Args:
            user_input: The user's input to check.

        Returns:
            True if the input is an exit command, False otherwise.
        """
        return user_input.strip().lower() in ["/exit", "exit", "/quit", "quit"]

    def start_interactive(self, context: str) -> None:
        """Start an interactive conversation session.

        Args:
            context: The conversation context (e.g., "Planning", "Teaching", "Evaluation").
        """
        self.context = context
        self.is_active = True

        click.echo(f"\n🎯 Starting {context} Session")
        click.echo("=" * 50)

        # Display initial greeting
        greeting = get_greeting(context)
        self._display_response(greeting)

        try:
            while self.is_active:
                # Get user input
                user_input = click.prompt("You")

                if self._is_exit_command(user_input):
                    click.echo("\n👋 Thanks for chatting with Foggy! Goodbye!")
                    self.is_active = False
                    break

                # Show "thinking" indicator
                click.echo("🤖 Foggy is thinking...")

                # Simulate API call and get response
                response = self._simulate_api_call(user_input)

                # Store in conversation history
                self.history.append((user_input, response))

                # Display response
                self._display_response(response)

        except KeyboardInterrupt:
            click.echo("\n\n⚠️  Conversation interrupted. Thanks for using Foggy!")
        except Exception as e:
            click.echo(f"\n❌ An error occurred during the conversation: {e}", err=True)
        finally:
            self.is_active = False

    def get_conversation_history(self) -> List[tuple[str, str]]:
        """Get the complete conversation history.

        Returns:
            List of tuples containing (user_input, foggy_response) pairs.
        """
        return self.history.copy()

    def get_statistics(self) -> Dict[str, int]:
        """Get conversation statistics.

        Returns:
            Dictionary containing conversation metrics.
        """
        return {
            "total_exchanges": len(self.history),
            "context": self.context,
            "is_completed": not self.is_active
        }
