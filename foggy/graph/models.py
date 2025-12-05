"""Data models for Foggy LangGraph implementation.

This module contains all Pydantic models used throughout the LangGraph workflow
for state management and data validation.
"""

from typing import List, Annotated, Optional
from pydantic import BaseModel, Field
from langchain.agents import AgentState
from langgraph.graph.message import add_messages


def merge_todos(existing: List["Task"], new: List["Task"]) -> List["Task"]:
    """Reducer function to merge todo lists.

    This function handles concurrent updates to the todo list by merging
    new todos with existing ones, replacing todos with the same name.

    Args:
        existing: Current list of tasks in state
        new: New list of tasks to merge

    Returns:
        Merged list of tasks with duplicates removed (new values take precedence)
    """
    if not existing:
        return new
    if not new:
        return existing

    # Create a dict from existing todos (name -> task)
    todo_dict = {task.name: task for task in existing}

    # Update with new todos (overwrites existing ones with same name)
    for task in new:
        todo_dict[task.name] = task

    # Return as list
    return list(todo_dict.values())


class Task(BaseModel):
    """Represents a single task in the learning plan.

    Attributes:
        name (str): The description of the task to be completed
        isFinished (bool): Whether the task has been completed
    """

    name: str = Field(..., description="The description of the task to be completed")
    isFinished: bool = Field(
        default=False, description="Whether the task has been completed"
    )


class Subsection(BaseModel):
    """Represents a subsection within a learning plan section.

    Attributes:
        id (str): Unique identifier for the subsection
        name (str): Name of the subsection
        description (str): Description of what will be covered
        concepts (List[str]): List of key concepts covered in this subsection
        isCompleted (bool): Whether the subsection has been completed
    """

    id: str = Field(..., description="Unique identifier for the subsection")
    name: str = Field(..., description="Name of the subsection")
    description: str = Field(..., description="Description of what will be covered")
    concepts: List[str] = Field(
        default_factory=list, description="List of key concepts covered"
    )
    isCompleted: bool = Field(
        default=False, description="Whether the subsection has been completed"
    )


class Section(BaseModel):
    """Represents a section in the learning plan.

    Attributes:
        id (str): Unique identifier for the section
        name (str): Name of the section
        description (str): Description of what will be covered
        subsections (List[Subsection]): List of subsections within this section
    """

    id: str = Field(..., description="Unique identifier for the section")
    name: str = Field(..., description="Name of the section")
    description: str = Field(..., description="Description of what will be covered")
    subsections: List[Subsection] = Field(
        default_factory=list, description="List of subsections"
    )


class LearningPlan(BaseModel):
    """Represents a complete structured learning plan.

    Attributes:
        goal (str): The learning goal
        prerequisites (List[str]): List of prerequisites needed
        sections (List[Section]): List of sections in the learning plan
    """

    goal: str = Field(..., description="The learning goal")
    prerequisites: List[str] = Field(
        default_factory=list, description="List of prerequisites needed"
    )
    sections: List[Section] = Field(
        default_factory=list, description="List of sections in the learning plan"
    )


class PlanState(AgentState):
    """State management for the Foggy LangGraph workflow.

    This model tracks the entire conversation state, todo items, and completion status.

    Attributes:
        messages (Annotated[List, add_messages]): Conversation history between user and agents
        todo (Annotated[List[Task], merge_todos]): List of tasks that need to be completed
        finished (bool): Whether the overall planning process is complete
    """

    messages: Annotated[List, add_messages] = Field(
        default_factory=list, description="Conversation history between user and agents"
    )
    todo: Annotated[List[Task], merge_todos] = Field(
        default_factory=list, description="List of tasks that need to be completed"
    )
    finished: bool = Field(
        default=False, description="Whether the overall planning process is complete"
    )


# Teach Mode Models


class SubsectionStatus(BaseModel):
    """Status of a single subsection.

    Attributes:
        id (str): Unique identifier for the subsection
        name (str): Name of the subsection
        description (str): Description of what will be covered
        concepts (List[str]): List of key concepts covered
        isCompleted (bool): Whether the subsection has been completed
    """

    id: str
    name: str
    description: str
    concepts: List[str]
    isCompleted: bool = False


class SectionInfo(BaseModel):
    """Information about current section.

    Attributes:
        id (str): Unique identifier for the section
        name (str): Name of the section
        description (str): Description of what will be covered
        subsections (List[SubsectionStatus]): List of subsections within this section
    """

    id: str
    name: str
    description: str
    subsections: List[SubsectionStatus]


class TeachState(AgentState):
    """State for Teach mode workflow.

    This model tracks the teaching session state, including current section/subsection,
    progress tracking, and learning plan management.

    Attributes:
        messages (Annotated[List, add_messages]): Message history
        learning_plan (dict): Full plan loaded from JSON
        goal (str): Learning goal
        current_section (Optional[SectionInfo]): Current section being taught
        current_subsection (Optional[SubsectionStatus]): Current subsection being taught
        completed_sections (List[str]): Section IDs that are complete
        completed_subsections (List[str]): Subsection IDs that are complete
    """

    messages: Annotated[List, add_messages] = Field(
        default_factory=list, description="Message history"
    )
    learning_plan: dict = Field(
        default_factory=dict, description="Full plan loaded from JSON"
    )
    goal: str = Field(default="", description="Learning goal")
    current_section: Optional[SectionInfo] = Field(
        default=None, description="Current section being taught"
    )
    current_subsection: Optional[SubsectionStatus] = Field(
        default=None, description="Current subsection being taught"
    )
    completed_sections: List[str] = Field(
        default_factory=list, description="Section IDs that are complete"
    )
    completed_subsections: List[str] = Field(
        default_factory=list, description="Subsection IDs that are complete"
    )
    isSetupFinished: bool = Field(
        default=False, description="Tracks if the setup is finished."
    )


class SubsectionCompletion(BaseModel):
    """Structured output when subsection is finished.

    Attributes:
        subsection_id (str): ID of completed subsection
        key_concepts (List[str]): Main concepts covered
        user_understood (bool): User demonstrated understanding
    """

    subsection_id: str = Field(description="ID of completed subsection")
    key_concepts: List[str] = Field(description="Main concepts covered")
    user_understood: bool = Field(description="User demonstrated understanding")
