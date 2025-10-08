# Contributing to myquery

Thank you for your interest in contributing to myquery! 🎉

## 🚀 Getting Started

1. **Fork the repository**
2. **Clone your fork:**
   ```bash
   git clone https://github.com/your-username/myquery.git
   cd myquery
   ```

3. **Set up development environment:**
   ```bash
   # Run the setup script
   bash scripts/setup.sh  # Linux/Mac
   # or
   scripts\setup.bat  # Windows
   ```

4. **Create a feature branch:**
   ```bash
   git checkout -b feature/your-feature-name
   ```

## 🛠️ Development Guidelines

### Code Style

- Follow PEP 8 style guide
- Use type hints for function parameters and return values
- Add docstrings to all functions and classes
- Keep functions focused and single-purpose

### Format Code

```bash
# Format with Black
black .

# Lint with Ruff
ruff check .

# Type check with MyPy
mypy .
```

### Testing

- Write tests for new features
- Ensure all tests pass before submitting PR
- Aim for high test coverage

```bash
# Run tests
pytest tests/

# With coverage
pytest --cov=. tests/
```

### Commit Messages

Use clear, descriptive commit messages:

```
✨ Add new feature X
🐛 Fix bug in Y
📚 Update documentation for Z
♻️ Refactor component A
✅ Add tests for B
```

## 📝 Pull Request Process

1. **Update documentation** if you're adding/changing features
2. **Add tests** for new functionality
3. **Ensure all tests pass**
4. **Update CHANGELOG.md** with your changes
5. **Submit PR** with a clear description of changes

### PR Template

```markdown
## Description
Brief description of what this PR does

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
Describe the tests you ran

## Checklist
- [ ] Code follows style guidelines
- [ ] Tests added and passing
- [ ] Documentation updated
- [ ] No breaking changes (or documented)
```

## 🏗️ Project Structure

Understanding the codebase:

```
myquery/
├── cli/              # CLI commands and interface
├── core/             # Core business logic
├── tools/            # LangChain tools
├── mcp/              # MCP protocol implementation
├── config/           # Configuration management
├── tests/            # Test suite
└── examples/         # Usage examples
```

## 💡 Feature Suggestions

We welcome feature suggestions! Please:

1. Check existing issues first
2. Open a new issue with:
   - Clear description of the feature
   - Use cases
   - Potential implementation approach

## 🐛 Bug Reports

When reporting bugs, please include:

1. **Environment:** OS, Python version, myquery version
2. **Steps to reproduce**
3. **Expected behavior**
4. **Actual behavior**
5. **Error messages/logs** (if any)

## 📚 Documentation

Documentation improvements are always welcome:

- Fix typos
- Clarify confusing sections
- Add examples
- Improve README

## ❓ Questions

Have questions? Feel free to:

- Open a GitHub issue
- Start a discussion
- Reach out to maintainers

## 🙏 Thank You

Your contributions make myquery better for everyone. Thank you! ❤️

