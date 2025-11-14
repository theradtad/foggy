# System Patterns & Architecture

## Core Architecture Patterns

### Multi-Agent Orchestration
```
User Interface (CLI/Web) → Agent Coordinator → Specialized Agents
                                      ↓
                               State Manager
                                      ↓
                            Storage Layer (SQLite + MD)
```

**Agent Types**:
- **Planning Agent**: Goal assessment, prerequisite analysis, plan generation
- **Teaching Agent**: Content delivery, Q&A support, example generation
- **Evaluation Agent**: Work assessment, feedback provision, redo recommendations

### State Management Pattern
- **Section-Based State**: Each learning section maintains isolated state
- **State Transitions**: Clear progression: Assessment → Planning → Teaching → Evaluation → Completion
- **State Persistence**: Critical state data persisted, ephemeral state managed in memory
- **State Recovery**: Ability to resume from any point with minimal data loss

### Content Generation Pipeline
```
Learning Goal → Prerequisite Analysis → Section Planning → Content Templates → User Approval → Content Generation
```

## Key Design Patterns

### Conversational Flow Pattern
- **Question-Answer Loops**: Structured conversation flows with validation
- **Progressive Disclosure**: Information revealed based on user responses and progress
- **Fallback Handling**: Graceful degradation when user input is unclear

### Content Structure Pattern
- **Section Template**: Standardized format for each learning section
  - Conceptual Overview
  - Practical Examples
  - Mini-Project
  - Assessment Criteria
- **Content Versioning**: Track different versions of examples and projects for redo functionality

### Storage Abstraction Pattern
- **Hybrid Storage**: SQLite for relational data, Markdown for human-readable content
- **Migration Support**: Schema evolution with backward compatibility
- **Backup Strategy**: Automated backups with recovery mechanisms

## Component Relationships

### Agent Communication
- **Message Passing**: Structured communication protocol between agents
- **Shared Context**: Common context object accessible to all agents in a session
- **Event-Driven**: Agents respond to events rather than direct method calls

### Data Flow Architecture
```
User Input → Input Processor → Agent Coordinator → Content Generator → Output Formatter → User Display
                                      ↓
                               Progress Tracker → Storage Manager
```

### Error Handling Patterns
- **Graceful Degradation**: System continues functioning with reduced capabilities
- **User-Friendly Messages**: Clear error communication without technical jargon
- **Recovery Mechanisms**: Automatic retry logic with exponential backoff

## Critical Implementation Paths

### Learning Session Lifecycle
1. **Initialization**: User goal capture and prerequisite assessment
2. **Planning**: Structured plan creation with user approval
3. **Execution**: Section-by-section progression with content delivery
4. **Evaluation**: Work assessment and feedback provision
5. **Completion**: Progress persistence and session summary

### Content Generation Flow
1. **Context Gathering**: Collect user knowledge level and learning objectives
2. **Structure Planning**: Design section breakdown and progression
3. **Content Creation**: Generate examples, projects, and assessment criteria
4. **Quality Assurance**: Internal validation of generated content
5. **User Delivery**: Formatted presentation with interaction capabilities

### Progress Tracking Implementation
1. **State Capture**: Record user position and completion status
2. **Progress Metrics**: Track time spent, attempts made, success rates
3. **Persistence Strategy**: Regular state saves with transaction safety
4. **Resume Capability**: Restore exact user state across sessions

## Security & Reliability Patterns

### Input Validation
- **Sanitization**: All user inputs validated and sanitized
- **Type Checking**: Strict type enforcement on data structures
- **Bounds Checking**: Prevent buffer overflows and resource exhaustion

### Session Management
- **Timeout Handling**: Automatic cleanup of inactive sessions
- **Resource Limits**: Prevent resource exhaustion from long-running sessions
- **Concurrent Access**: Safe handling of multiple simultaneous sessions
