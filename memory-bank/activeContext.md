# Active Context: Current Development Focus

## Immediate Work Focus
Implementing the LangGraph-powered AI agent for Foggy's core conversational tutoring functionality. The system is undergoing a major architecture shift from basic CLI to full conversational AI agent with learning plan generation, progress tracking, and human-in-the-loop validation.

## Current Development Phase
**LangGraph Implementation Phase 1: Foundation Setup**

### Recently Completed
- ✅ Dependencies verified and requirements updated for LangGraph
- ✅ Core data structures defined (PlanState, Tasks pydantic models)
- ✅ LangGraph module directory structure established
- ✅ Search tool implemented with Tavily integration
- ✅ Todo management tools implemented (create_todo, update_todo_status, read_todo, get_pending_todos)
- ✅ Save Learning Plan tool implemented

### In Progress
**Welcome Message Node**: Setting up the initial user interaction node that welcomes users and prompts for learning goals.

### Upcoming Work (Next Steps)
1. **Human Goal Node**: Implement user input handling for learning objectives with exit options
2. **AITodoListGenerator Node**: Create LLM-powered todo generation based on user goals
3. **Human Node**: Build generic human feedback collection node
4. **Planner Node**: Core LLM agent implementation
5. **Write Plan Node**: File output handling for generated plans
6. **Graph Assembly**: Connect all nodes with conditional edges
7. **State Management**: Implement PlanState with messages, todos, and completion tracking

## Important Technical Decisions
- Using LangGraph for stateful conversational AI instead of basic LangChain chains
- Human-in-the-loop validation at every major step of the learning process
- Tool-based architecture with web search, todo management, and file operations
- Section-wise learning with state reset between sections
- Local markdown file storage for learning plans and progress

## Active Patterns & Preferences
- Functions over classes in LangGraph flows (following langchain best practices)
- Comprehensive type annotations on all functions/methods
- Google-style docstrings for all components
- Async/await patterns for I/O operations
- Pydantic models for data validation and serialization
- Click-based CLI framework for command-line interface

## Key Constraints & Considerations
- All major decisions require human validation and approval
- State must be cleanly reset between learning sections
- Learning plans stored in user-accessible markdown format
- Support for Q&A on generated examples and content
- Progressive learning approach: concepts → examples → mini-projects

## Recent Insights
- LangGraph provides excellent framework for complex conversational flows with conditional routing
- Tool calling architecture enables modular, extensible functionality
- Human validation nodes are crucial for maintaining learning quality and user satisfaction
- State management becomes critical when handling multi-step learning processes with persistent data

## Risk Considerations
- Complex graph assembly requires careful edge definition and state management
- Tool calling errors need graceful handling and user feedback
- LLM hallucinations in learning plan generation need validation layers
- File I/O operations require robust error handling and validation

## Next Checkpoints
1. Welcome Message Node completion and testing
2. First end-to-end graph flow (welcome → goal input)
3. Integration testing of todo generation and human validation
4. Full learning plan generation with file persistence
