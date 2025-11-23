# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Foggy is an AI-powered personalized coding tutor using LangGraph orchestration with Google Gemini LLM and Tavily web search. It creates adaptive learning plans through concept→example→project cycles.

**Current Status**: Phase 1 (LangGraph Foundation) - ~25% complete

## Commands

```bash
# Setup
poetry install
cp .env-template .env  # Add GOOGLE_API_KEY, GEMINI_MODEL, TAVILY_API_KEY

# Run
poetry run foggy plan      # Generate learning plans
poetry run foggy teach     # Interactive teaching
poetry run foggy evaluate  # Assess progress

# Code quality
ruff check foggy --fix
ruff format foggy

# Test
pytest
```

## Architecture

```
CLI (Click) → LangGraph Orchestrator → [LLM Agent, Tools, State Management]
                                                    ↓
                                           Data Models (Pydantic)
```

### Key Components

- **`foggy/cli/commands.py`**: Click-based CLI entry point
- **`foggy/langgraph/models.py`**: Pydantic models (`Task`, `PlanState`, `UserGoal`, `LearningPlan`)
- **`foggy/langgraph/tools.py`**: LangGraph tools (`web_search`, `create_todo`, `save_learning_plan`, etc.)
- **`foggy/prompts.py`**: Version-controlled prompt templates
- **`foggy/conversation/`**: Response templates and dummy conversation for testing

### LangGraph Plan Flow

See `docs/plan-langgraph-flow.png` for visual diagram.

```
__start__ → Welcome Message → HumanGoal Node → AI: TodoListGenerator → HumanNode → AINode (planner) → __end__
                                                                           ↕            ↕
                                                                      ToolNode ←→ Write Plan
```

**State Model**:
- `PlanState`: messages (Annotated[list, add_messages]), todo (list[Task]), finished (bool)
- `Task`: name (str), isFinished (bool)

**Nodes**:
- `Welcome Message`: Initial greeting
- `HumanGoal Node`: Captures user's learning goal
- `AI: TodoListGenerator`: LLM generates task list from goal
- `HumanNode`: User feedback on todos, ask about prerequisites, validate plan
- `AINode`: The planner agent (core LLM)
- `ToolNode`: Search, Todo create, Todo read
- `Write Plan`: Update plan in a file

## Code Standards

### Required: Type Annotations
```python
def process_goal(goal: str, prerequisites: List[str]) -> Task:
```

### Required: Google-style Docstrings
```python
def get_pending_todos(runtime: ToolRuntime) -> List[Task]:
    """Get list of pending todos from state.

    Args:
        runtime: LangGraph tool runtime for state access

    Returns:
        List of incomplete todos
    """
```

### Patterns
- Prefer functions over classes for LangGraph nodes
- Use Pydantic models for all data validation
- Specific exception types (no bare `except`)
- Tools need input/output schemas with error handling

## Environment Variables

```bash
GOOGLE_API_KEY=...        # Required: Gemini API
GEMINI_MODEL=gemini-2.5-flash  # Default model
TAVILY_API_KEY=...        # Required for web search
```

## Current Development Focus

- Complete LangGraph node implementation
- Start Teach mode implementation.
- State reset mechanism for section boundaries
- Increase test coverage (currently ~15%, target 90%+)
- End-to-end conversation flow testing
