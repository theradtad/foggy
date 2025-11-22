# System Patterns: Architecture & Design

## Core Architecture Overview
Foggy follows a **conversational AI agent pattern** using LangGraph as the orchestration framework. The system implements a stateful, graph-based workflow with human-in-the-loop validation at critical decision points.

## Key Technical Decisions

### LangGraph as Orchestration Framework
- **Decision Rationale**: LangGraph provides stateful conversation management with conditional routing, essential for multi-step learning workflows with human validation
- **Benefits**: Clean state management, conditional edge routing, built-in tool calling integration, persistent conversation history
- **Trade-offs**: Higher complexity compared to simple LangChain chains, but necessary for conversational tutoring complexity

### Tool-Based Architecture
- **Pattern**: Modular function based tool system for specific capabilities (web search, todo management, file operations)
- **Implementation**: Custom tools built using LangChain tool framework with proper schema definition
- **Benefits**: Extensible, testable, clear separation of concerns

### Human-in-the-Loop Design
- **Pattern**: Mandatory human validation at all major decision points
- **Nodes**: Dedicated Human nodes for feedback collection on todos, plans, and learning assessments
- **Benefits**: Ensures quality control, user agency, prevents AI hallucinations in learning recommendations

## Design Patterns

### State Management Pattern
- **PlanState**: Central state object containing messages, todos, and completion flags
- **Annotation Pattern**: Uses `add_messages` for conversation history accumulation
- **State Reset**: Clean slate between learning sections as required

### Node Function Pattern
- **Functional Nodes**: Prefer functions over classes for LangGraph nodes (LangChain best practice)
- **Single Responsibility**: Each node handles one specific interaction type
- **Type Annotations**: Complete typing for all node functions and return values

### Tool Implementation Pattern
- **Schema-First**: Pydantic models define tool input/output schemas
- **Error Handling**: Comprehensive exception handling with user-friendly messages
- **Validation**: Input validation using Pydantic model constraints

## Component Relationships

### Core Components
```
CLI Layer (Click) → LangGraph Orchestrator → LLM Agent → Tools → File System
     ↑                                                            ↓
   User Input                                               Learning Data (Markdown)
```

### Node Flow Architecture
```
start → welcome → human_goal → todo_generator → human_validator → planner → [tool_node] → write_plan → end
     ↑           ↑              ↑                                                    ↓
     └───────────┼──────────────┼────────────────────────────────────────────────────┘
                 Human validation checkpoints
```

### Data Flow Patterns
- **Conversation State**: Persistent within session, managed through PlanState
- **Learning Plans**: Serialized to markdown files in user directory
- **Progress Tracking**: Stored locally, accessible across sessions
- **Tool Results**: Temporary, used for immediate decision making

## Critical Implementation Paths

### Learning Plan Generation
1. User goal input → Knowledge prerequisite assessment
2. Web research for current best practices → Plan draft generation
3. Human validation → Plan refinement → File persistence

### Section Learning Cycle
1. Concept introduction → Example generation → Mini-project creation
2. User implementation → AI evaluation → Feedback provision
3. Success check → Progress to next section OR repeat with variations

### Error Handling Strategy
- **Invalid Inputs**: Clear user guidance with examples
- **Tool Failures**: Graceful fallback with user notification
- **LLM Errors**: Retry logic with human intervention option
- **File I/O Issues**: Robust error handling with data integrity checks

## Architectural Constraints

### State Boundaries
- **Session State**: Persistent conversation within tutorial session
- **Section State**: Reset completely between learning sections
- **Learning Data**: Persistent across all sessions for progress tracking

### Concurrency Model
- **Single User**: Assumption of single concurrent user per Foggy instance
- **Sequential Processing**: No concurrent node execution within a session
- **Async I/O**: Tool operations use async patterns for efficiency

### Data Persistence Strategy
- **Local First**: All learning data stored locally
- **Markdown Format**: Human-readable learning plans and progress
- **Structured Naming**: Consistent file organization in user-learning folder

## Scaling Considerations
- **Modular Tools**: New capabilities added as independent tools
- **Graph Extensibility**: New learning workflows supported by extending the graph
- **Learning Content**: Framework-agnostic design supports any technology stack
