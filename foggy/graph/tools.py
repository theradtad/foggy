"""Tools for Foggy LangGraph implementation.

This module contains all tools used by the LangGraph nodes including
web search, todo operations, and file management.
"""

import os

from typing import List, Dict, Any
from pathlib import Path
import re
import click
from langchain.tools import tool, ToolRuntime
from langgraph.types import Command
from langchain.messages import ToolMessage

from langchain_tavily import TavilySearch
from foggy.graph.models import Task

@tool
def web_search(query: str) -> List[Dict[str, Any]]:
    """Perform web search for the given query.
    """
    try:
        click.echo(click.style(f"\n🔍 Tool: web_search", fg="yellow", bold=True))
        click.echo(click.style(f"   Query: {query}", fg="yellow"))
        os.getenv("TAVILY_API_KEY")  # Ensure API key is set
        web_search = TavilySearch(max_results=3, topic="general")
        results = web_search.run(query)
        
        return_res = []
        for result in results["results"]:
            return_res.append({
                "title": result.get("title", ""),
                "content": result.get("snippet", ""),
                "url": result.get("link", "")
            })
        
        return return_res
    except Exception as e:
        print(f"Web search failed: {e}")
        return []

@tool
def create_todo(task_name: str, runtime: ToolRuntime) -> Command:
    """Create a new todo task with isFinished set to False.
    """
    click.echo(click.style(f"\n📝 Tool: create_todo", fg="yellow", bold=True))
    click.echo(click.style(f"   Task: {task_name}", fg="yellow"))

    # Read current todo list from state
    todo_list = runtime.state.get("todo", [])

    # Create new todo
    new_todo = Task(name=task_name, isFinished=False)
    updated_todos = todo_list + [new_todo]

    # Create command to update state
    return Command(update={
        "todo": updated_todos,
        "messages": runtime.state.get("messages", []) + [ToolMessage(content=f"Added todo: {task_name}", tool_call_id=runtime.tool_call_id)]
    })

@tool
def update_todo_status(task_name: str, is_finished: bool, runtime: ToolRuntime) -> Command:
    """Update the status of the task with the given name.

    Args:
        task_name: The name of the task to update
        is_finished: Whether the task is completed
        runtime: LangGraph tool runtime for state management

    Returns:
        Command to update the state with the modified todo list
    """
    click.echo(click.style(f"\n✏️ Tool: update_todo_status", fg="yellow", bold=True))
    click.echo(click.style(f"   Task: {task_name}", fg="yellow"))
    click.echo(click.style(f"   Status: {'Completed' if is_finished else 'Incomplete'}", fg="yellow"))

    # Read current todo list from state
    todo_list = runtime.state.get("todo", [])

    # Find and update the task
    updated_todos = []
    found = False
    for todo in todo_list:
        if todo.name == task_name:
            updated_todos.append(Task(name=todo.name, isFinished=is_finished))
            found = True
        else:
            updated_todos.append(todo)

    if not found:
        return Command(update={
            "messages": runtime.state.get("messages", []) + [ToolMessage(content=f"Task '{task_name}' not found.", tool_call_id=runtime.tool_call_id)]
        })

    # Create command to update state
    status_text = "completed" if is_finished else "marked as incomplete"
    return Command(update={
        "todo": updated_todos,
        "messages": runtime.state.get("messages", []) + [
            ToolMessage(content=f"Task '{task_name}' {status_text}.", tool_call_id=runtime.tool_call_id)
        ]
    })

@tool
def get_pending_todos(runtime: ToolRuntime) -> List[Task]:
    """Get list of pending (unfinished) todos from state.
    """
    click.echo(click.style(f"\n📋 Tool: get_pending_todos", fg="yellow", bold=True))

    todo_list = runtime.state.get("todo", [])
    pending_todos = [todo for todo in todo_list if not todo.isFinished]

    return pending_todos

@tool
def read_todo(runtime: ToolRuntime) -> List[Task]:
    """Read the complete todo list from state.

    Args:
        runtime: LangGraph tool runtime for state access

    Returns:
        List of all todos in the current state
    """
    click.echo(click.style(f"\n📖 Tool: read_todo", fg="yellow", bold=True))

    return runtime.state.get("todo", [])

@tool
def save_learning_plan(title: str, content: str, user_goal_name: str) -> str:
    """Save learning plan to json file in learning_plans folder.
    """
    click.echo(click.style(f"\n💾 Tool: save_learning_plan", fg="yellow", bold=True))
    return "Request to save learning plan received. Processing..."

@tool
def should_continue_planning(runtime: ToolRuntime) -> bool:
    """Determine if planning should continue based on current state.
    """
    click.echo(click.style(f"\n🔄 Tool: should_continue_planning", fg="yellow", bold=True))

    todo_list = runtime.state.get("todo", [])
    pending_todos = [todo for todo in todo_list if not todo.isFinished]
    finished = runtime.state.get("finished", False)

    # Continue if there are pending todos and planning is not finished
    return len(pending_todos) > 0 and not finished
