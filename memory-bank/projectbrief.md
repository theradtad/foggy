# Project Brief: Foggy - Personalized Coding Tutor

## Core Mission
Build an AI-powered, personalized coding tutor that revolutionizes how developers learn programming languages, libraries, and frameworks through project-based, conversational learning experiences.

## Core Requirements

### Primary Objectives
1. **Interactive Learning**: Enable users to pursue personalized learning goals with AI guidance
2. **Adaptive Planning**: Create comprehensive learning plans based on user goals, prerequisites, and current knowledge
3. **Practical Application**: Teach through conceptual understanding → examples → mini-projects
4. **Continuous Feedback**: Provide real-time evaluation and improvement suggestions
5. **Progress Tracking**: Maintain detailed learning history
6. **Web-Enabled Research**: Leverage web search for current best practices and resources

### Key Features
- **Goal Discovery**: Interactive conversations to identify user learning objectives
- **Knowledge Assessment**: Evaluate prerequisite knowledge levels
- **Dynamic Planning**: Generate section-wise learning plans with concept coverage, examples, and mini-projects
- **Project Management**: Track todo lists and learning progress
- **Q&A Support**: Enable questions on generated examples and concepts
- **Redoing Capability**: Support section redo with varied examples
- **Persistent Storage**: Store learning plans, progress, and examples in markdown files

### Success Criteria
1. Users can successfully learn new technologies through structured yet personalized approaches
2. Learning plans adapt to user's existing knowledge and pace
3. Feedback loop enables continuous improvement of understanding
4. System maintains state across learning sessions while allowing clean section resets
5. Human-in-the-loop ensures quality and user satisfaction at every step

## Technical Scope
- Command-line application built with Python
- LangGraph-powered conversational AI agent
- Tool integrations for web search, todo management, and file operations
- State management for learning progress and conversation history
- Data persistence through local markdown file storage

## Constraints
- Local-first approach with optional external API integrations
- Human-in-the-loop for all major decisions and validations
- Clear state boundaries between learning sections
