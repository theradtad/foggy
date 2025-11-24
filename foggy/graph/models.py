"""Data models for Foggy LangGraph implementation.

This module contains all Pydantic models used throughout the LangGraph workflow
for state management and data validation.
"""

from typing import List, Annotated, Optional
from pydantic import BaseModel, Field
from langgraph.graph.message import add_messages


class Task(BaseModel):
    """Represents a single task in the learning plan.
    
    Attributes:
        name (str): The description of the task to be completed
        isFinished (bool): Whether the task has been completed
    """
    name: str = Field(..., description="The description of the task to be completed")
    isFinished: bool = Field(default=False, description="Whether the task has been completed")


class PlanState(BaseModel):
    """State management for the Foggy LangGraph workflow.
    
    This model tracks the entire conversation state, todo items, and completion status.
    
    Attributes:
        messages (Annotated[List, add_messages]): Conversation history between user and agents
        todo (List[Task]): List of tasks that need to be completed
        finished (bool): Whether the overall planning process is complete
    """
    messages: Annotated[List, add_messages] = Field(
        default_factory=list, 
        description="Conversation history between user and agents"
    )
    todo: List[Task] = Field(
        default_factory=list, 
        description="List of tasks that need to be completed"
    )
    finished: bool = Field(default=False, description="Whether the overall planning process is complete")


class UserGoal(BaseModel):
    """Model for storing user's learning goal information.
    
    Attributes:
        goal (str): The user's learning objective
        prerequisites (Optional[List[str]]): Known prerequisites for the goal
        current_knowledge (Optional[dict]): User's current knowledge level in prerequisites
    """
    goal: str = Field(..., description="The user's learning objective")
    prerequisites: Optional[List[str]] = Field(
        default=None, 
        description="Required prerequisites for the learning goal"
    )
    current_knowledge: Optional[dict] = Field(
        default=None, 
        description="User's current knowledge level in prerequisites"
    )


class LearningPlan(BaseModel):
    """Model for storing generated learning plans.
    
    Attributes:
        title (str): Title of the learning plan
        sections (List[str]): Structured learning sections
        estimated_duration (Optional[str]): Estimated time to complete
        resources (Optional[List[str]]): Recommended resources
    """
    title: str = Field(..., description="Title of the learning plan")
    sections: List[str] = Field(..., description="Structured learning sections")
    estimated_duration: Optional[str] = Field(
        default=None, 
        description="Estimated time to complete the plan"
    )
    resources: Optional[List[str]] = Field(
        default=None, 
        description="Recommended resources for the learning plan"
    )
