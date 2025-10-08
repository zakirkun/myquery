# Contributing to myquery

Thank you for your interest in contributing to myquery! This document provides guidelines and instructions for contributing.

## Code of Conduct

By participating in this project, you agree to maintain a respectful and inclusive environment for everyone.

## How to Contribute

### Reporting Bugs

If you find a bug, please open an issue with:

- Clear description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Environment details (OS, Python version, database type)
- Error messages or logs (if applicable)

### Suggesting Features

We welcome feature suggestions! Please open an issue with:

- Clear description of the feature
- Use case and benefits
- Proposed implementation (if applicable)

### Pull Requests

1. **Fork and Clone**
   ```bash
   git clone https://github.com/zakirkun/myquery.git
   cd myquery
   ```

2. **Create a Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   pip install -e ".[dev]"
   ```

4. **Make Changes**
   - Write clean, documented code
   - Follow existing code style
   - Add tests for new features
   - Update documentation

5. **Run Tests**
   ```bash
   # Run all tests
   pytest tests/
   
   # Run with coverage
   pytest --cov=. tests/
   
   # Format code
   black .
   
   # Lint
   ruff check .
   ```

6. **Commit Changes**
   ```bash
   git add .
   git commit -m "feat: add amazing feature"
   ```
   
   Use conventional commit messages:
   - `feat:` — New feature
   - `fix:` — Bug fix
   - `docs:` — Documentation changes
   - `style:` — Code style changes
   - `refactor:` — Code refactoring
   - `test:` — Test changes
   - `chore:` — Maintenance tasks

7. **Push and Create PR**
   ```bash
   git push origin feature/your-feature-name
   ```
   
   Then open a Pull Request on GitHub with:
   - Clear description of changes
   - Link to related issues
   - Screenshots (if UI changes)

## Development Guidelines

### Code Style

- Follow PEP 8 style guide
- Use type hints
- Write docstrings for all public functions/classes
- Keep functions small and focused
- Use meaningful variable names

### Project Structure

```
myquery/
├── cli/              # CLI commands
├── core/             # Core business logic
├── tools/            # LangChain tools
├── web/              # Web UI
├── mcp/              # MCP server
├── config/           # Configuration
└── tests/            # Tests
```

### Adding New Features

1. **Tools** — Place in `tools/` directory
   - Inherit from `BaseTool`
   - Use Pydantic for input validation
   - Write comprehensive docstrings

2. **CLI Commands** — Place in `cli/commands/`
   - Use Typer for CLI framework
   - Follow existing command patterns
   - Add help text and examples

3. **Core Logic** — Place in `core/`
   - Keep business logic separate from CLI
   - Make functions testable
   - Use dependency injection

### Testing

- Write tests for all new features
- Aim for >80% code coverage
- Use pytest fixtures for common setup
- Mock external dependencies (OpenAI, databases)

Example test:
```python
def test_export_to_csv():
    tool = ExportDataTool()
    result = tool._run(
        query_result_json=sample_data,
        format="csv",
        filename="test_export"
    )
    assert "✅" in result
    assert os.path.exists("outputs/exports/test_export.csv")
```

### Documentation

- Update README.md for user-facing features
- Update CHANGELOG.md for all changes
- Add docstrings for all public APIs
- Include code examples in docstrings

## Development Setup

### Prerequisites

- Python 3.8+
- pip
- git
- OpenAI API key (for testing AI features)

### Local Development

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e ".[dev]"

# Set up environment
cp .env.example .env
# Edit .env with your credentials

# Run tests
pytest

# Run myquery locally
python -m cli.main --help
```

### Running Locally

```bash
# Start chat
python -m cli.main chat start

# Start web UI
python -m cli.main web start

# Start MCP server
python -m cli.main server start
```

## Release Process

(For maintainers)

1. Update version in `pyproject.toml`
2. Update CHANGELOG.md
3. Create git tag: `git tag v0.x.0`
4. Push tag: `git push origin v0.x.0`
5. Create GitHub release

## Questions?

Feel free to:
- Open an issue for questions
- Start a discussion on GitHub
- Reach out to maintainers

Thank you for contributing! 🎉
