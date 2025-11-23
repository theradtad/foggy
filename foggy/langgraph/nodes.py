"""LangGraph nodes for Foggy CLI workflow.

This module contains all node implementations for the LangGraph-based
planning workflow. Each node receives state and returns updated state.

Version: 1.0.0
"""

import os

import click
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage, ToolMessage
from langgraph.prebuilt import ToolNode

from foggy.langgraph.models import PlanState
from foggy.langgraph.tools import (
    web_search,
    create_todo,
    update_todo_status,
    read_todo,
    get_pending_todos,
    save_learning_plan,
)
from foggy.prompts import PLANNING_SYSTEM_PROMPT

# Load environment variables
load_dotenv()

# Define all available tools
ALL_TOOLS = [
    web_search,
    create_todo,
    update_todo_status,
    read_todo,
    get_pending_todos,
    save_learning_plan,
]


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


def _get_llm_with_tools() -> ChatGoogleGenerativeAI:
    """Get configured LLM instance with tools bound.

    Returns:
        ChatGoogleGenerativeAI: Configured Gemini LLM with tools bound
    """
    llm = _get_llm()
    return llm.bind_tools(ALL_TOOLS)


def welcome_message_node(state: PlanState) -> PlanState:
    """Welcome message node - starting point of the graph.

    Displays a welcome message and asks the user to input their learning goal.

    Args:
        state: Current PlanState

    Returns:
        Updated PlanState with welcome message added to messages
    """
    welcome_text = """
Welcome to Foggy - Your AI-Powered Coding Tutor!

I'll help you create a personalized learning plan tailored to your goals.
Let's start by understanding what you want to learn.

Please enter your learning goal (or type 'q' to quit):
"""

    click.echo(click.style(welcome_text, fg="cyan"))

    # Add welcome message to state
    welcome_message = AIMessage(content=welcome_text.strip())

    return {
        "messages": [welcome_message],
        "todo": state.todo,
        "finished": state.finished,
    }


def human_goal_node(state: PlanState) -> PlanState:
    """Human Goal node - captures user's learning goal.

    Takes input from user regarding their goal. If user message is
    'q', 'quit', or 'exit', sets finished flag to True.

    Args:
        state: Current PlanState

    Returns:
        Updated PlanState with user goal message and possibly finished flag
    """
    user_input = click.prompt("", prompt_suffix="").strip()

    # Check for exit commands
    if user_input.lower() in ["q", "quit", "exit"]:
        click.echo(click.style("\nGoodbye! Happy learning!", fg="yellow"))
        return {
            "messages": [HumanMessage(content=user_input)],
            "todo": state.todo,
            "finished": True,
        }

    # Add user's goal as a human message
    goal_message = HumanMessage(content=f"My learning goal: {user_input}")

    return {
        "messages": [goal_message],
        "todo": state.todo,
        "finished": state.finished,
    }


def todo_list_generator_node(state: PlanState) -> PlanState:
    """AI TodoListGenerator node - generates task list from user's goal.

    Uses LLM with tools to create todos via create_todo tool calls.
    The LLM will use the create_todo tool to add tasks to the state.

    Args:
        state: Current PlanState

    Returns:
        Updated PlanState with AI response (may include tool calls for creating todos)
    """
    llm_with_tools = _get_llm_with_tools()

    # Get the user's goal from the last human message
    user_goal = ""
    for msg in reversed(state.messages):
        if isinstance(msg, HumanMessage):
            user_goal = msg.content
            break

    # Create prompt for todo generation
    todo_generation_prompt = f"""
Based on the user's learning goal, create a structured todo list for the planning process.

User's goal: {user_goal}

Use the create_todo tool to create exactly 4 todos:
1. Search for requirements and prerequisites for this learning goal
2. Ask the user about their current knowledge level on prerequisites
3. Generate a detailed plan covering concepts, examples, and projects
4. Save the final plan to a file

Call create_todo for each task.
"""

    # Generate todos using LLM with tools
    messages = [
        SystemMessage(content=PLANNING_SYSTEM_PROMPT),
        HumanMessage(content=todo_generation_prompt),
    ]

    response = llm_with_tools.invoke(messages)

    # Display response to user
    if response.content:
        click.echo(click.style("\n📋 Generating Todo List...", fg="green"))
        click.echo(response.content)

    return {
        "messages": [response],
        "todo": state.todo,
        "finished": state.finished,
    }


def human_node(state: PlanState) -> PlanState:
    """Human Node - generic node for user feedback.

    Takes feedback from the user at various stages of the planning process.
    This includes feedback on todos, knowledge on prerequisites, plan validation.

    Args:
        state: Current PlanState

    Returns:
        Updated PlanState with user feedback message
    """
    click.echo(click.style("\nPlease provide your feedback (or 'q' to quit):", fg="cyan"))
    user_input = click.prompt("", prompt_suffix="").strip()

    # Check for exit commands
    if user_input.lower() in ["q", "quit", "exit"]:
        click.echo(click.style("\nGoodbye! Happy learning!", fg="yellow"))
        return {
            "messages": [HumanMessage(content=user_input)],
            "todo": state.todo,
            "finished": True,
        }

    # Add user feedback as a human message
    feedback_message = HumanMessage(content=user_input)

    return {
        "messages": [feedback_message],
        "todo": state.todo,
        "finished": state.finished,
    }


def planner_node(state: PlanState) -> PlanState:
    """Planner Node - the brain of the agent (LLM).

    This is the main planning agent that processes messages and decides
    on next actions. It can call tools and generate responses.

    Args:
        state: Current PlanState

    Returns:
        Updated PlanState with AI response message (may include tool calls)
    """
    llm_with_tools = _get_llm_with_tools()

    # Build conversation context
    messages = [SystemMessage(content=PLANNING_SYSTEM_PROMPT)]

    # Add todo context
    if state.todo:
        todo_context = "\n\nCurrent Todo List:\n"
        for i, task in enumerate(state.todo, 1):
            status = "✓" if task.isFinished else "○"
            todo_context += f"{status} {i}. {task.name}\n"
        messages.append(SystemMessage(content=todo_context))

    # Add conversation history
    messages.extend(state.messages)

    # Get LLM response
    response = llm_with_tools.invoke(messages)

    # Display AI response to user (if there's content)
    if response.content:
        click.echo(click.style("\n🤖 Foggy:", fg="green"))
        click.echo(response.content)

    return {
        "messages": [response],
        "todo": state.todo,
        "finished": state.finished,
    }


def tool_node(state: PlanState) -> PlanState:
    """Tool Node - executes tool calls from the planner.

    Uses LangGraph's ToolNode to process any tool calls made by the planner node.

    Args:
        state: Current PlanState

    Returns:
        Updated PlanState with tool execution results
    """
    # Create ToolNode with all available tools
    tool_executor = ToolNode(ALL_TOOLS)

    # Execute tools - ToolNode handles the tool calls from the last message
    result = tool_executor.invoke({"messages": state.messages})

    return {
        "messages": result.get("messages", []),
        "todo": state.todo,
        "finished": state.finished,
    }


def write_plan_node(state: PlanState) -> PlanState:
    """Write Plan Node - saves the generated plan to a file.

    Processes save_learning_plan tool call and returns ToolMessage with result.

    Args:
        state: Current PlanState

    Returns:
        Updated PlanState with ToolMessage containing save result
    """
    # Get the last message which should contain tool calls
    last_message = state.messages[-1] if state.messages else None

    if not last_message or not hasattr(last_message, "tool_calls") or not last_message.tool_calls:
        error_message = AIMessage(content="No tool calls found to process.")
        return {
            "messages": [error_message],
            "todo": state.todo,
            "finished": state.finished,
        }

    # Process tool calls for save_learning_plan
    outbound_msgs = []

    for tool_call in last_message.tool_calls:
        if tool_call["name"] == "save_learning_plan":
            title = tool_call["args"].get("title", "Learning Plan")
            content = tool_call["args"].get("content", "")
            user_goal_name = tool_call["args"].get("user_goal_name", "learning_plan")

            try:
                file_path = save_learning_plan(
                    title=title,
                    content=content,
                    user_goal_name=user_goal_name
                )
                click.echo(click.style(f"\n✅ Plan saved to: {file_path}", fg="green"))

                # Return ToolMessage with result
                tool_message = ToolMessage(
                    content=f"Plan saved successfully to: {file_path}",
                    tool_call_id=tool_call["id"]
                )
                outbound_msgs.append(tool_message)

            except Exception as e:
                tool_message = ToolMessage(
                    content=f"Error saving plan: {str(e)}",
                    tool_call_id=tool_call["id"]
                )
                outbound_msgs.append(tool_message)

    if not outbound_msgs:
        error_message = AIMessage(content="No save_learning_plan tool calls found.")
        outbound_msgs.append(error_message)

    return {
        "messages": outbound_msgs,
        "todo": state.todo,
        "finished": state.finished,
    }
