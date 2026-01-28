# Contributing to OpenAspen

Thank you for your interest in contributing to OpenAspen! This document provides guidelines and instructions for contributing.

## Code of Conduct

Be respectful, inclusive, and constructive. We're building this together.

## Getting Started

### 1. Fork and Clone

```bash
git clone https://github.com/yourusername/openaspen.git
cd openaspen
```

### 2. Set Up Development Environment

```bash
# Install Poetry
curl -sSL https://install.python-poetry.org | python3 -

# Install dependencies
poetry install

# Install pre-commit hooks
poetry run pre-commit install
```

### 3. Create a Branch

```bash
git checkout -b feature/your-feature-name
```

## Development Workflow

### Running Tests

```bash
# Run all tests
poetry run pytest

# Run with coverage
poetry run pytest --cov=openaspen --cov-report=html

# Run specific test file
poetry run pytest tests/test_core.py

# Run with verbose output
poetry run pytest -v
```

### Code Formatting

We use Black and Ruff for code formatting:

```bash
# Format code
poetry run black .

# Lint code
poetry run ruff check .

# Type checking
poetry run mypy openaspen
```

Pre-commit hooks will automatically run these on commit.

### Running Examples

```bash
# Basic example
poetry run python examples/basic_tree.py

# Advanced example
poetry run python examples/advanced_tree.py

# Server example
poetry run python examples/server_example.py
```

## Contribution Guidelines

### Code Style

- Follow PEP 8 style guide
- Use type hints for all functions
- Write docstrings for public APIs
- Keep functions focused and small
- Use meaningful variable names

### Example:

```python
async def fetch_data(endpoint: str, timeout: int = 30) -> dict[str, Any]:
    """
    Fetch data from an API endpoint.
    
    Args:
        endpoint: The API endpoint to call
        timeout: Request timeout in seconds
        
    Returns:
        Dictionary containing the API response
        
    Raises:
        aiohttp.ClientError: If the request fails
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(endpoint, timeout=timeout) as response:
            return await response.json()
```

### Testing Requirements

- Write tests for all new features
- Maintain or improve code coverage
- Use pytest fixtures for common setups
- Mock external API calls
- Test both success and error cases

### Example Test:

```python
import pytest
from openaspen.core.leaf import Leaf

async def sample_tool(input_data: str) -> str:
    return f"Processed: {input_data}"

class TestLeaf:
    @pytest.mark.asyncio
    async def test_leaf_execution(self) -> None:
        leaf = Leaf(name="test", tool_func=sample_tool)
        result = await leaf.execute("test input")
        
        assert result["success"] is True
        assert "Processed: test input" in result["result"]
```

### Documentation

- Update README.md for user-facing changes
- Update ARCHITECTURE.md for design changes
- Add docstrings to all public APIs
- Include examples in docstrings
- Update CHANGELOG.md

## Types of Contributions

### 🐛 Bug Fixes

1. Check if issue already exists
2. Create issue if not
3. Reference issue in PR
4. Add regression test

### ✨ New Features

1. Discuss in GitHub Discussions first
2. Create detailed issue
3. Get approval before implementing
4. Include tests and documentation
5. Update examples if relevant

### 📚 Documentation

- Fix typos and improve clarity
- Add examples and tutorials
- Improve API documentation
- Translate documentation

### 🧪 Tests

- Improve test coverage
- Add edge case tests
- Performance benchmarks
- Integration tests

## Pull Request Process

### 1. Before Submitting

- [ ] Tests pass locally
- [ ] Code is formatted (Black, Ruff)
- [ ] Type checking passes (mypy)
- [ ] Documentation updated
- [ ] CHANGELOG.md updated
- [ ] Examples work

### 2. PR Description

Include:
- What changes were made
- Why the changes were needed
- How to test the changes
- Screenshots (if UI changes)
- Related issues

### 3. Review Process

- Maintainers will review within 1 week
- Address feedback promptly
- Keep PR focused and small
- Squash commits before merge

### 4. After Merge

- Delete your branch
- Update your fork
- Celebrate! 🎉

## Project Structure

```
openaspen/
├── openaspen/          # Main package
│   ├── core/          # Core tree components
│   ├── llm/           # LLM routing and providers
│   ├── rag/           # RAG and embeddings
│   ├── server/        # API server
│   └── cli.py         # CLI interface
├── tests/             # Test suite
├── examples/          # Usage examples
├── docs/              # Documentation
└── pyproject.toml     # Dependencies
```

## Adding New Features

### Adding a New LLM Provider

1. Add to `LLMProvider` enum in `llm/providers.py`
2. Add defaults to `PROVIDER_DEFAULTS`
3. Implement in `LLMRouter._create_llm()`
4. Add tests in `tests/test_llm.py`
5. Update documentation

### Adding a New Vector Store

1. Create new class in `rag/`
2. Implement same interface as `GroupRAGStore`
3. Add configuration options
4. Add tests
5. Update documentation

### Adding a New Node Type

1. Inherit from `TreeNode`
2. Implement `execute()` method
3. Add convenience methods to `OpenAspenTree`
4. Add tests
5. Add example

## Release Process

(For maintainers)

1. Update version in `pyproject.toml`
2. Update CHANGELOG.md
3. Create release branch
4. Run full test suite
5. Create GitHub release
6. Publish to PyPI

## Getting Help

- **Questions**: GitHub Discussions
- **Bugs**: GitHub Issues
- **Security**: Email maintainers privately
- **Chat**: Discord (coming soon)

## Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md
- Mentioned in release notes
- Given credit in documentation

Thank you for contributing to OpenAspen! 🌲
