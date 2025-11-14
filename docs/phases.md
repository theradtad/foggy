# Phase Wise implementation of the project.

## Phase 1:
1. The agent should converse with the user to determine their goal and their current knowledge of the pre-requisites.
2. Based on the conversation, the agent should draft a plan for the user.
3. Add support to browse the web while creating the plan.
4. User can modify the plan based on their requirements.
5. The agent should save the plan to a document.
6. Ensure support for multi-agent architecture going forward.
7. Mention token usage at each step.

## Phase 2:
1. Support generating examples step wise according to the plan.
2. Add support to track user progress.
3. Allow user to approve moving to the next step post which the agent can mark the sub-section as completed.
4. Support generating a quiz/assesment. 
5. Support Q&A on generated examples.
6. Add support to summarize and prevent context window from overflowing.

## Phase 3:
1. Add the support to have an evaluator agent.
2. Allow redoing a section by the user.
3. Wipe the Agent's memory post every section.

## Phase 4: SQLite Storage Implementation
1. Design database schema with tables for: users, learning_sessions, sections, progress_tracking, quiz_scores, and agent_summaries.
2. Migrate existing MD file storage to SQLite for structured data (progress, metadata) while keeping MD files for content.
3. Implement user profile management with preferences and learning history.
4. Add session persistence across application restarts.
5. Create migration scripts for evolving database schema.
6. Implement data backup and recovery mechanisms.

## Phase 5: Web Interface Development
1. Build FastAPI backend with REST endpoints for agent interactions and data management.
2. Create Gradio frontend for accessible user interface with plan visualization, progress tracking, and chat interface.
3. Integrate CLI functionality within web commands for seamless workflow.
4. Add real-time agent status updates and progress notifications.
5. Implement user authentication and multi-session support.
6. Add responsive design for mobile and desktop usage.
