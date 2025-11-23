# LangGraph Implementation Plan for Foggy CLI

## Todo List for LangGraph Migration

### **Phase 1: Foundation Setup**
- [x] **Dependencies Check**: Verify langgraph installation and update requirements if needed
- [x] **Data Structures Design**: Define PlanState and Tasks Pydantic models
- [x] **Project Structure**: Create langgraph module directory structure
- [x] **Search Tool Implementation**: Implement tool for Tavily Search 
- [x] **Todo Tools Implementation**: Implement create_todo, update_todo_status, read_todo, get_pending_todos
- [x] **Save Learning Plan tool**: Implement Save Learning plan tool.
- [ ] **Welcome Message Node**: Implement the welcome message node which acts as the starting point in the graph.
- [ ] **Human Goal Node**: Implement the Human Goal node which takes in the input from user on their goal. User can exit at this step by typing in q or quit. 
- [ ] **AITodoListGenerator Node**: Implement the TodoListGenerator node which uses an LLM to create a set of todos similar to the example mentioned in prompt.py . 
- [ ] **Human Node**: Implement the Human Node which allows the user to input data to the LLM (Ex: Feedback on todos, knowledge on pre-requisites, plan validation).
- [ ] **Planner Node**: The brain of this agent - LLM.
- [ ] **Write Plan Node**: This writes the plan to the file. 
- [ ] **Conditional Edge at HumanNode**: Allows user to either respond to and be redirected to the planner node or exit.  
- [ ] **Conditional Edge at Planner Node**: Based on if tool_call is present (and what type of tool call), routes to tool_node, write_node, edge_node and end.
- [ ] **Implement the Graph**: Implement the end graph connecting all the nodes.  


## Design:
Langgraph nodes:
1. __start__ : the start node
2. Welcome Message node: Just prints a welcome message and asks the user to input their learning goal.
3. HumanGoalNode: The node which takes in input from the user regarding their goal. If user message is q, quit or exit, we exit.
4. AITodoListGenerator: This node takes the user's goal and generates a list of todos. For example: User's goal: I want to learn the basics React. Todos:  - Search the web for requisites of learning react. - Clarify what pre-requisites the user is aware of and their depth of knowledge in it. - Generate an in-depth plan covering pre-requisites, target concepts, examples and simple mini-projects. - Save plan to a file.
5. HumanNode: This is the generic node which takes feedback from the user every step of the way.
6. AINode: This is the planner node which is an LLM , the brains of this research.
7. ToolNode: The langgraph tool node to which we bind tavily search, todo create, todo read.
8. WritePlan: This is a node which uses a tool to save plan to a file.
9. __end__

Edges:
welcome → human_goal
human_goal → todo_list_agent
todo_list_agent → human_validator 
human_validator → planner_agent
planner_agent → tool_node (optional edge)
planner_agent → human_validator (optional edge - when we want human clarification)
tool_node → planner_agent (returns result of tool call)
planner_agent → write_plan (optional edge based on project progress).
write_plan → planner_Agent (returns success or failure)
planner_agent-> end

PlanState: (the state for this langgraph application)
- messages: Annotated[list, add_messages]
- todo: list[Tasks]
- finished: bool

Tasks: (Represents a single task)
- name: str
- isFinished: bool