# Technology Context: Development Environment & Tools

## Core Technology Stack

### Programming Language
- **Python 3.10+**: Base language supporting modern type annotations and async patterns
- **Justification**: Excellent ecosystem for AI/ML, strong typing support, excellent langchain/LangGraph integration

### AI/ML Framework
- **LangChain**: Core framework for LLM application development
- **LangGraph**: Stateful orchestration for conversational AI workflows
- **LangChain Google GenAI**: Google Gemini integration for LLM capabilities
- **LangChain Community**: Additional integrations and tools

### Dependency Management
- **Poetry**: Modern Python dependency management and packaging
- **pyproject.toml**: PEP 621 compliant project configuration

## Development Tools

### Code Quality & Formatting
- **Ruff**: Lightning-fast Python linter and code formatter (replaces flake8, black, isort)
- **Configuration**: Ruff handles code formatting, import sorting, and linting in single tool

### CLI Framework
- **Click**: Pythonic command-line interface creation
- **Structure**: Organized command hierarchy with `foggy.cli.commands` module

### Type System
- **Typing Module**: Comprehensive type annotations for all functions, methods, classes
- **Pydantic**: Data validation and serialization with type enforcement

## Testing & Quality Assurance

### Testing Framework
- **pytest**: Standard Python testing framework
- **Coverage**: 90%+ target coverage for reliability
- **Test Organization**: Located in `tests/` directory with proper structure

### Documentation
- **Google Style Docstrings**: Comprehensive documentation for all public APIs
- **README.md**: Project overview and usage instructions
- **Documentation**: Additional docs in `docs/` directory for features and guides

## External Dependencies

### Core Dependencies
- `langchain (>=1.0.7,<2.0.0)`: LLM application framework
- `langchain-google-genai (>=3.0.3,<4.0.0)`: Google Gemini integration
- `langchain-community (>=0.0.38,<1.0.0)`: Community integrations
- `langgraph (>=1.0.3,<2.0.0)`: Conversational AI orchestration

### Utility Dependencies
- `click (>=8.1.3)`: Command-line interface framework
- `pytest (>=7.4.2)`: Testing framework
- `python-dotenv (>=1.2.1,<2.0.0)`: Environment variable management
- `langchain-tavily (>=0.2.13)`: Web search integration

## Development Environment

### Local Development
- **Poetry Shell**: Isolated development environment
- **VS Code**: Primary IDE with Python extensions
- **Environment Variables**: `.env` file for API keys and configuration

### Version Control
- **Git**: Distributed version control system
- **GitHub**: Remote repository hosting at `https://github.com/theradtad/foggy.git`

## Technical Constraints

### Python Version
- **Minimum**: Python 3.10 required
- **Maximum**: Python 3.13 (future compatibility)
- **Reasoning**: Type annotation features, performance improvements, ecosystem maturity

### API Limitations
- **External APIs**: Google Gemini and Tavily Search have rate limits and costs
- **Local Processing**: Primary computation stays local for privacy and speed
- **Network Dependency**: Web search features require internet connectivity

### Resource Requirements
- **Memory**: Sufficient for LLM context windows and conversation state
- **Storage**: Local storage for learning plans and progress data
- **Network**: Required for AI model calls and web search integration

## Security Considerations

### Data Privacy
- **Local Storage**: All learning data stored locally in markdown files
- **API Keys**: Sensitive keys managed through environment variables
- **No Data Transmission**: Learning progress and plans never sent to external servers

### Input Validation
- **Pydantic Models**: Strict data validation on all inputs
- **Sanitization**: User inputs validated and sanitized before processing
- **Error Handling**: Secure error messages that don't expose system internals

## Deployment & Distribution

### Packaging
- **Poetry Build**: Standard Python wheel/sdist distribution
- **CLI Entry Point**: `foggy` command available after installation
- **Dependencies**: All dependencies bundled for reliable installation

### Environment Setup
- **Installation**: `pip install` or `poetry install`
- **Configuration**: Environment variables for API access
- **First Run**: Automatic setup prompts for initial configuration

## Future Technology Evolution

### Monitoring Upgrades
- **Python Versions**: Track 3.12+ features for modernization
- **LangChain Updates**: Stay current with latest framework features
- **AI Models**: Evaluate newer models for improved learning experiences

### Scalability Preparation
- **Async Architecture**: Foundation for concurrent learning sessions
- **Modular Design**: Easy addition of new learning tools and capabilities
