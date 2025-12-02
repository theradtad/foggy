# Teach Mode Flow

## Overview

The Teach mode orchestrates interactive learning sessions through a LangGraph workflow that guides users through structured sub-sections of their learning plan.

## Flow Diagram

```
START → Load Next Section → Setup Env Agent → Orchestrator → Worker → END
                                   ↓              ↓            ↓
                              [Read/Write     [Human,      [Finish
                               File Tools]     Flow]     Sub-section]

         ┌─────────────────────────────────────────┘
         │
         └→ Is Section Finished? → END (if true)
                                 → Memory Compaction if Required
```

## Node Details

### 1. Load Next Section
- Entry point for teach mode
- Retrieves next incomplete section from learning plan
- Initializes section context

### 2. Setup Env Agent
- Prepares learning environment
- **Tools**: Read File
- Gathers context on current env. Asks user to update env and follow steps if required.
- Can use the web search tool implemented in the plan flow.
- Uses HumanInTheLoop Middleware and returns structured output.

### 3. Orchestrator
- Central coordination node
- Follows the Orchestrator worker pattern and assigns sub sections to the worker.
- **Tool**: Is Section Finished?
     - Decision node checking completion status
     - Routes to END if section complete
     - Continues to next sub-section otherwise

### 4. Worker
- Executes teaching logic
- Handles content delivery and explanations
- **Current Behavior**: Provides code snippets for user to copy-paste
- **Tool**: Finish Sub-section
     - Marks sub-sections as complete
- **Tool**: Memory Compaction
     - Triggers memory compaction if needed
     - Triggered when conversation grows large

### 5. HITL (Human-in-the-Loop)
- Interactive feedback collection
- Validates understanding
- Adjusts pace based on user responses
- Allows user to ask questions as well. 

## Current Implementation Status

- Agent provides code snippets for copy-paste by user
     - For Teaching as well as env setup.
- Manual file setup required
- Future: Automated environment configuration
- Future: Automated code file generation