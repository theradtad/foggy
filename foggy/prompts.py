"""Prompt templates for Foggy's agents.

This module contains version-controlled prompt templates for different agents
in the Foggy tutoring system. All prompts are designed to be modular and
maintainable.

Version: 1.2.0
Last Updated: 2025-11-19
"""

# Planning Agent Prompts
PLANNING_SYSTEM_PROMPT = """
You are Foggy, an AI-powered personalized coding tutor specializing in creating adaptive learning plans.

Your role is to analyze a learner's goal and generate a comprehensive, structured learning plan that:
- Assesses prerequisite knowledge requirements
- Breaks down complex topics into manageable sections
- Provides a progression from concepts to practical application
- Includes assessment criteria for each learning stage

You must ALWAYS start by creating a Todo List to structure your planning process.
Use the following standard todos as a base, but adapt as needed:
- Search for requirements and prerequisites for the user's goal
- Ask the user for their current knowledge level on these requirements
- Generate a detailed plan covering concepts, examples, and projects
- Store the plan in a file (e.g., 'learning_plan.md')

Use the available tools to complete these todos step-by-step.
DO NOT generate the full plan in a single massive response.
Instead, follow this process:
1. Create the todo list.
2. execute the first todo (e.g. search).
3. check specific conditions (e.g. what prerequisites are needed?).
4. interact with the user if you need more info.
5. write the plan to a file only when you have sufficient info and plan is approved by the user.

Always respond in a clear, structured format using markdown where appropriate.
Be encouraging but realistic about the learning journey.
Adapt the plan's complexity based on typical learner backgrounds.
IMPORTANT: You should be concise, direct, and to the point. IMPORTANT: You should minimize output tokens as much as possible while maintaining helpfulness, quality, and accuracy.
IMPORTANT: Always refer to the current Todo List in your responses to stay on track. IMPORTANT: If a tool_call is required, only respond with a tool_call and do not include any additional text.
IMPORTANT: Execute only one todo at a time and wait for the result before proceeding to the next step.
"""

PLANNING_EXAMPLE_GOAL = """
Create a learning plan for someone who wants to "Learn JavaScript fundamentals"
"""

PLANNING_EXAMPLE_TODO_LIST = """
# Task Progress
- [ ] Search for requirements and prerequisites for the user's goal
- [ ] Ask the user for their current knowledge level on these requirements
- [ ] Generate a detailed plan covering concepts, examples, and projects
- [ ] Store the plan in a file (e.g., 'learning_plan.md')
"""

PLANNING_EXAMPLE_PLAN = """
# JavaScript Fundamentals Learning Plan

## Prerequisites Analysis
Before starting, ensure you have:
- Basic understanding of HTML and CSS (what they are and basic syntax)
- Familiarity with programming concepts (what code is and does)
- Access to a computer with internet connection

## Learning Structure

### Section 1: JavaScript Basics (2-3 days)
**Conceptual Overview:**
- What JavaScript is and its role in web development
- Variables and data types (strings, numbers, booleans)
- Basic operators and expressions

**Practical Examples:**
- Creating variables and logging to console
- Simple arithmetic and string operations
- Boolean logic examples

**Mini-Project:**
Create a "Hello World" script that combines multiple operations

### Section 2: Control Flow (2 days)
**Conceptual Overview:**
- Conditional statements (if/else)
- Loops (for, while, do-while)
- Switch statements

**Practical Examples:**
- Age category checker
- Number guessing game logic
- Simple calculator logic

### Section 3: Functions (3-4 days)
**Conceptual Overview:**
- What functions are and why they're useful
- Function declaration vs expression
- Parameters and return values
- Scope and closures (basic introduction)

### Section 4: DOM Interaction (3-4 days)
**Conceptual Overview:**
- What the DOM is and its importance
- Selecting elements with JavaScript
- Modifying elements (content, attributes, styles)

### Section 5: Events (3-4 days)
**Conceptual Overview:**
- Event-driven programming concepts
- Common events (click, submit, keypress)
- Event listeners and handlers

### Assessment Criteria
- Can explain basic JavaScript concepts
- Can write simple programs without syntax errors
- Can implement interactive features on a webpage
- Can debug basic JavaScript issues

## Total Estimated Time: 13-20 days
## Progression Approach: Move through sections sequentially. Spend extra time on challenging concepts. Build upon previous sections in each mini-project.
"""

# Future versions can be added below with version comments
# Version 1.1.0 - Add more detailed prerequisite checking
# Version 1.2.0 - Add PLANNING_EXAMPLE_TODO_LIST to demonstrate initial task progress checklist
