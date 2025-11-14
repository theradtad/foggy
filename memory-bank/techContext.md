# Technical Context & Environment

## Technology Stack

### Core Language & Runtime
- **Python Version**: 3.13+ (latest stable with modern features)
- **Runtime Environment**: Native Python with virtual environment management
- **Package Management**: Poetry for dependency management and packaging

### Development Tools
- **Code Formatting**: Ruff (unified linter, formatter, and import organizer)
- **Type Checking**: Built-in Python typing with strict annotation requirements
- **Testing Framework**: pytest with comprehensive test coverage requirements
- **Documentation**: Google-style docstrings for all functions and classes

### CLI Framework
- **Command Line Interface**: Click for building CLI applications
- **Script Entry Point**: Poetry script configuration for `foggy` command

### Agent & AI Framework
- **LLM Integration**: LangChain for agent orchestration and LLM interactions
- **Agent Framework**: LangGraph for complex multi-agent workflows
- **Prompt Management**: Structured prompt templates with version control

### Storage & Persistence
- **Relational Database**: SQLite for structured data (users, sessions, progress)
- **Document Storage**: Markdown files for human-readable content and examples
- **Migration Tools**: Alembic for database schema evolution

### Web Interface (Phase 5)
- **Backend Framework**: FastAPI for REST API development
- **Frontend Framework**: Gradio for accessible web UI
- **ASGI Server**: Uvicorn for production deployment

### Development Environment
- **Version Control**: Git with conventional commit messages
- **IDE Support**: VS Code with Python extensions
- **Environment Management**: conda/venv with Poetry integration

## Technical Constraints

### Performance Requirements
- **Response Time**: Sub-second responses for CLI interactions
- **Memory Usage**: Efficient memory management for long-running sessions
- **Storage Efficiency**: Optimized storage for content and progress data

### Compatibility Requirements
- **Platform Support**: Windows, macOS, Linux compatibility
- **Python Version**: Strict 3.13+ requirement (no backward compatibility)
- **Dependency Stability**: Use stable, well-maintained packages

### Security Considerations
- **Input Validation**: Comprehensive validation of all user inputs
- **Data Sanitization**: Prevent injection attacks and malicious content
- **Session Security**: Secure handling of user sessions and data

## Development Setup

### Local Development Environment
```bash
# Clone repository
git clone <repository-url>
cd foggy

# Set up Python environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
poetry install

# Install pre-commit hooks
poetry run pre-commit install

# Run tests
poetry run pytest

# Run application
poetry run foggy
```

### Code Quality Gates
- **Linting**: Ruff checks must pass
- **Type Checking**: mypy strict mode compliance
- **Test Coverage**: Minimum 90% coverage required
- **Documentation**: All public APIs documented

### Build & Deployment
- **Package Building**: Poetry build for distribution
- **Containerization**: Docker support for deployment
- **CI/CD**: GitHub Actions for automated testing and releases

## Tool Usage Patterns

### Code Organization
- **Package Structure**: Modular design with clear separation of concerns
- **Import Strategy**: Absolute imports with explicit module structure
- **Configuration**: Centralized configuration management

### Testing Strategy
- **Unit Tests**: Comprehensive unit test coverage for all modules
- **Integration Tests**: End-to-end testing of critical user flows
- **Mock Strategy**: Extensive use of mocks for external dependencies

### Error Handling
- **Exception Hierarchy**: Custom exception classes for different error types
- **Logging Strategy**: Structured logging with appropriate log levels
- **User Communication**: Clear, actionable error messages

### Performance Optimization
- **Async/Await**: Extensive use of asynchronous programming
- **Caching Strategy**: Intelligent caching for expensive operations
- **Resource Management**: Proper cleanup and resource limits
