# Development Guide

Contributing to myquery development.

## Setup

### Clone Repository

```bash
git clone https://github.com/zakirkun/myquery.git
cd myquery
```

### Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### Install Dependencies

```bash
# Production dependencies
pip install -r requirements.txt

# Development dependencies
pip install -e ".[dev]"
```

### Configure Environment

```bash
cp .env.example .env
# Edit .env with your settings
```

## Development Workflow

### 1. Create Branch

```bash
git checkout -b feature/your-feature-name
```

### 2. Make Changes

Follow the [project structure](#project-structure).

### 3. Run Tests

```bash
pytest tests/
```

### 4. Format Code

```bash
black .
ruff check .
```

### 5. Commit

```bash
git add .
git commit -m "feat: add amazing feature"
```

Use [conventional commits](https://www.conventionalcommits.org/):
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation
- `style:` - Formatting
- `refactor:` - Code refactoring
- `test:` - Tests
- `chore:` - Maintenance

### 6. Push and PR

```bash
git push origin feature/your-feature-name
```

Then create Pull Request on GitHub.

## Project Structure

```
myquery/
├── cli/              # CLI commands
│   ├── main.py       # Entry point
│   └── commands/     # Command modules
├── core/             # Business logic
├── tools/            # LangChain tools
├── web/              # Web UI
├── mcp/              # MCP server
├── config/           # Configuration
├── tests/            # Tests
├── docs/             # Documentation
└── examples/         # Example scripts
```

## Adding New Features

### New Tool

1. Create file in `tools/`
2. Implement `BaseTool`
3. Add to `tools/__init__.py`
4. Register in `core/agent.py`
5. Add tests
6. Document in `docs/`

### New CLI Command

1. Create file in `cli/commands/`
2. Implement with Typer
3. Register in `cli/main.py`
4. Add tests
5. Document in `docs/cli/commands.md`

## Testing

### Run All Tests

```bash
pytest
```

### Run Specific Test

```bash
pytest tests/test_tools.py::test_export_tool
```

### With Coverage

```bash
pytest --cov=. tests/
```

### Writing Tests

```python
def test_export_to_csv():
    from tools import ExportDataTool
    
    tool = ExportDataTool()
    result = tool._run(
        query_result_json=sample_data,
        format="csv",
        filename="test"
    )
    
    assert "✅" in result
    assert os.path.exists("outputs/exports/test.csv")
```

## Code Style

### Follow PEP 8

```bash
# Format with black
black .

# Check with ruff
ruff check .
```

### Type Hints

Always use type hints:

```python
def process_data(data: list[dict], limit: int = 10) -> str:
    """Process data and return result."""
    pass
```

### Docstrings

Use Google-style docstrings:

```python
def example_function(param1: str, param2: int) -> bool:
    """
    Short description.
    
    Longer description if needed.
    
    Args:
        param1: Description of param1
        param2: Description of param2
        
    Returns:
        Description of return value
        
    Raises:
        ValueError: When something is wrong
    """
    pass
```

## Documentation

### Update Docs

When adding features:
1. Update relevant `.md` files in `docs/`
2. Update README.md if user-facing
3. Update CHANGELOG.md
4. Add code examples

### Building Docs

Documentation is in Markdown, no build step needed.

## Release Process

(For maintainers)

1. Update version in `pyproject.toml`
2. Update CHANGELOG.md
3. Create git tag
4. Push tag
5. Create GitHub release

## Getting Help

- GitHub Issues
- GitHub Discussions
- See [CONTRIBUTING.md](../../CONTRIBUTING.md)

---

[← Back to Documentation](../README.md)

