"""Custom tools for Foggy's agents.

This module defines specialized tools for different agents,
including search, file operations, and user interaction.
"""

import os
from typing import Type
import getpass

from langchain_tavily import TavilySearch
from langchain_community.tools.file_management import WriteFileTool
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field
import click


class AskUserInput(BaseModel):
    """Input for asking user a question."""

    question: str = Field(description="The question to ask the user")


class AskUserTool(BaseTool):
    """Tool to ask the user a question via CLI prompt."""

    name: str = "ask_user"
    description: str = "Ask the user a question and get their response. Use this for clarification or additional information needed for planning."
    args_schema: Type[BaseModel] = AskUserInput

    def _run(self, question: str) -> str:
        """Ask the user the question and return their response."""
        try:
            answer = click.prompt(f"\n🔍 {question}")
            return answer
        except (click.Abort, KeyboardInterrupt):
            return "User cancelled the input"


def get_planning_tools() -> list:
    """Get the list of tools for the planning agent.
    
    Lazily initializes tools to avoid import-time failures if API keys are missing.
    """
    tavily_api_key = os.getenv("TAVILY_API_KEY")
    
    if not tavily_api_key:
        try:
            tavily_api_key = getpass.getpass("Tavily API key (optional, press Enter to skip):\n")
            if tavily_api_key:
                os.environ["TAVILY_API_KEY"] = tavily_api_key
        except (EOFError, KeyboardInterrupt):
            tavily_api_key = None
    
    tools = []
    
    # Only add TavilySearch if we have an API key
    if tavily_api_key:
        try:
            tools.append(TavilySearch(max_results=3, api_key=tavily_api_key))
        except Exception as e:
            click.echo(f"⚠️  Warning: Could not initialize TavilySearch: {e}")
    
    tools.extend([
        WriteFileTool(),  # Write generated plans to files
        AskUserTool(),    # Ask user for clarification
    ])
    
    return tools


def get_planning_tools_descriptions() -> str:
    """Get description of available tools for planning agent."""
    descriptions = []
    for tool in get_planning_tools():
        descriptions.append(f"- {tool.name}: {tool.description}")
    return "\n".join(descriptions)
