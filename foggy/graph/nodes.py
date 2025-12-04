"""LangGraph nodes for Foggy CLI workflow.

This module contains all node implementations for the LangGraph-based
planning workflow. Each node receives state and returns updated state.

Version: 1.0.0
"""

import os

import click
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage, ToolMessage
from langgraph.prebuilt import ToolNode

from foggy.graph.models import PlanState, LearningPlan
from foggy.graph.tools import (
    web_search,
    create_todo,
    update_todo_status,
    read_todo,
    get_pending_todos,
    save_learning_plan,
    should_continue_planning
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
    should_continue_planning
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

def _get_llm_with_structured_plan_output() -> ChatGoogleGenerativeAI:
    llm = _get_llm()
    return llm.with_structured_output(LearningPlan, method="json_schema")


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
        "todo": state.get("todo", []),
        "finished": state.get("finished", False),
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
            "todo": state.get("todo", []),
            "finished": True,
        }

    # Add user's goal as a human message
    goal_message = HumanMessage(content=f"My learning goal: {user_input}")

    return {
        "messages": [goal_message],
        "todo": state.get("todo", []),
        "finished": state.get("finished", False),
    }


def todo_list_generator_node(state: PlanState) -> PlanState:
    """AI TodoListGenerator node - generates task list from user's goal.

    Uses agent with tools to create todos via create_todo tool calls.

    Args:
        state: Current PlanState

    Returns:
        Updated PlanState with AI response (may include tool calls for creating todos)
    """

    # Get the user's goal from the last human message
    msgs = state.get("messages", [])
    user_goal = None
    if len(msgs) > 0:
        user_goal = msgs[-1]

    if (not user_goal):
        click.echo(click.style("\n❌ Error: No learning goal provided.", fg="red"))
        return {
            "messages": [AIMessage(content="Error: No learning goal provided.")],
            "todo": state.get("todo", []),
            "finished": True,
        }
    
    # Create prompt for todo generation
    todo_generation_prompt = f"""
        Based on the user's learning goal, create a structured todo list for the planning process.

        User's goal: {user_goal}

        Use the create_todo tool to create todos. For example, the list of todos could be as follows:
        1. Search for requirements and prerequisites for this learning goal
        2. Ask the user about their current knowledge level on prerequisites
        3. Generate a detailed plan covering concepts, examples, and projects
        4. Save the final plan to a file

        Save the final plan would be the last step.
        Always create a todo to search the internet for requirements.
        Call create_todo for each task.

        Your response should ONLY contain tool calls to create_todo. Your goal is only to create the todo list.
        """

    todo_tools = [
        create_todo,
        read_todo,
        get_pending_todos,
    ]

    todo_agent = create_agent(
        model=_get_llm(),
        tools=todo_tools,
        system_prompt=PLANNING_SYSTEM_PROMPT,
        state_schema=PlanState
    )

    click.echo(click.style("\n Foggy is generating your Todo List...", fg="green"))
    response = todo_agent.invoke({"messages": [{"role": "user", "content": todo_generation_prompt.strip()}]})
    click.echo(click.style("✅ Todo List generation completed.", fg="green"))

    return {
        "messages": response["messages"],
        "todo": response.get("todo", state.get("todo", [])),
        "finished": response.get("finished", state.get("finished", False)),
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
    if state.get("todo", []):
        todo_context = "\n\nCurrent Todo List:\n"
        for i, task in enumerate(state.get("todo", []), 1):
            status = "✓" if task.isFinished else "○"
            todo_context += f"{status} {i}. {task.name}\n"
        messages.append(SystemMessage(content=todo_context))

    # Add conversation history
    messages.extend(state.get("messages", [])) 

    NEXT_STEP_PROMPT = """
    Based on the conversation so far, decide the next step. You can either:
    1. Ask the user for some input
    2. Provide a direct response to the user
    3. Call a tool to get more information or update the todo list
        If the todo list contains a step for searching the web, you MUST use the web_search tool to get relevant information.
        Always perform the web search first before proceeding with other steps.
    4. Mark a todo as completed using the update_todo_status tool
    5. Complete the todos one by one and in order.
    """
    
    messages.append(HumanMessage(content=NEXT_STEP_PROMPT))

    # Get LLM response
    response = llm_with_tools.invoke(messages)

    # click.echo(f"LLM Response: {response}")

    return {
        "messages": [response],
        "todo": state.get("todo", []),
        "finished": state.get("finished", False),
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
    msgs = state.get("messages", [])
    last_ai_message = None
    if len(msgs) > 0:
        last_ai_message = msgs[-1]
    
    ai_message_content = ""
    if last_ai_message and hasattr(last_ai_message, "content"):
        content = last_ai_message.content
        # Handle both string content and list of content chunks
        if isinstance(content, str):
            ai_message_content = content
        elif isinstance(content, list):
            for chunk in content:
                if isinstance(chunk, dict) and 'text' in chunk:
                    ai_message_content += chunk['text']
                elif hasattr(chunk, 'text'):
                    ai_message_content += chunk.text
                elif isinstance(chunk, str):
                    ai_message_content += chunk

    if ai_message_content:
        click.echo(click.style("\n🤖 Foggy:", fg="green", bold=True))
        click.echo(ai_message_content)
    click.echo(click.style("\nPlease provide your response (or 'q' to quit):", fg="cyan"))
    user_input = click.prompt("", prompt_suffix="").strip()

    # Check for exit commands
    if user_input.lower() in ["q", "quit", "exit"]:
        click.echo(click.style("\nGoodbye! Happy learning!", fg="yellow"))
        return {
            "messages": [HumanMessage(content=user_input)],
            "todo": state.get("todo", []),
            "finished": True,
        }

    # Add user feedback as a human message
    feedback_message = HumanMessage(content=user_input)

    return {
        "messages": [feedback_message],
        "todo": state.get("todo", []),
        "finished": state.get("finished", False),
    }

def structure_learning_plan_node(state: PlanState) -> PlanState:
    """Structure Learning Plan Node - converts plan text to structured JSON format.

    This node takes the conversation history where the plan was discussed,
    uses an LLM with structured output to extract sections, subsections,
    and concepts, then saves it as a structured JSON file.

    Args:
        state: Current PlanState

    Returns:
        Updated PlanState with ToolMessage containing save result
    """
    click.echo(click.style("\n🏗️ Structuring learning plan...", fg="cyan", bold=True))

    # Get the last message which should contain tool calls
    msgs = state.get("messages", [])
    last_message = None
    if len(msgs) > 0:
        last_message = msgs[-1]
    
    click.echo(click.style(f"\n The Last message is {last_message}", fg="yellow", bold=True))

    if not last_message or not hasattr(last_message, "tool_calls") or not last_message.tool_calls:
        error_message = ToolMessage(
            content="No tool calls found to process.",
            tool_call_id="error"
        )
        return {
            "messages": [error_message],
            "todo": state.get("todo", []),
            "finished": state.get("finished", False),
        }

    structure_model = _get_llm_with_structured_plan_output()

    msgs = [SystemMessage(content="""You are an expert at structuring learning plans.
Extract a well-organized learning plan from the conversation, creating logical sections and subsections.""")]

    # Prompt to extract structured plan
    structure_prompt = f"""Based on the conversation below, extract a structured learning plan.

Conversation:
{last_message}

Extract:
1. The main learning goal
2. Prerequisites needed (list of strings)
3. Sections with:
   - Unique id (e.g., "section_1", "section_2")
   - Name of the section
   - Description
   - Subsections with:
     - Unique id (e.g., "subsection_1_1", "subsection_1_2")
     - Name
     - Description
     - Key concepts (list of strings)
"""
    msgs.append(HumanMessage(content=structure_prompt))

    try:
        # Get structured output from model
        structured_plan: LearningPlan = structure_model.invoke(msgs)

        click.echo(click.style(f"✅ Plan structured successfully - Goal: {structured_plan.goal}", fg="green"))
        click.echo(click.style(f"   Sections: {len(structured_plan.sections)}", fg="green"))

        # Convert to JSON format matching the expected structure
        import json
        from datetime import datetime
        from pathlib import Path

        json_plan = {
            "goal": structured_plan.goal,
            "prerequisites": structured_plan.prerequisites,
            "sections": [],
            "metadata": {
                "created_at": datetime.now().isoformat(),
                "version": "1.0"
            }
        }

        # Add sections with subsections
        for section in structured_plan.sections:
            section_data = {
                "id": section.id,
                "name": section.name,
                "description": section.description,
                "subsections": []
            }

            for subsection in section.subsections:
                subsection_data = {
                    "id": subsection.id,
                    "name": subsection.name,
                    "description": subsection.description,
                    "concepts": subsection.concepts,
                    "isCompleted": False
                }
                section_data["subsections"].append(subsection_data)

            json_plan["sections"].append(section_data)

        # Save to file in learning_plans folder
        base_path = Path("./learning_plans")
        base_path.mkdir(parents=True, exist_ok=True)

        file_path = base_path / "learning_plan.json"

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(json_plan, f, indent=2, ensure_ascii=False)

        click.echo(click.style(f"✅ Plan saved to: {file_path.absolute()}", fg="green"))

        # Create tool message response for each tool call
        outbound_msgs = []
        for tool_call in last_message.tool_calls:
            if tool_call["name"] == "save_learning_plan":
                tool_message = ToolMessage(
                    content=f"Learning plan structured and saved successfully to: {file_path.absolute()}",
                    tool_call_id=tool_call["id"]
                )
                outbound_msgs.append(tool_message)

        return {
            "messages": outbound_msgs,
            "todo": state.get("todo", []),
            "finished": state.get("finished", False),
        }

    except Exception as e:
        click.echo(click.style(f"❌ Error structuring plan: {str(e)}", fg="red"))
        error_message = ToolMessage(
            content=f"Error structuring and saving plan: {str(e)}",
            tool_call_id=last_message.tool_calls[0]["id"] if last_message.tool_calls else "error"
        )
        return {
            "messages": [error_message],
            "todo": state.get("todo", []),
            "finished": state.get("finished", False),
        }