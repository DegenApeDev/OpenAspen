# Installation Guide for OpenAspen

## ✅ Successfully Installed!

OpenAspen has been successfully installed with all dependencies resolved for Python 3.14.

## Installation Summary

### Dependencies Installed:
- **LangChain**: v1.2.7 (upgraded from 0.1.x)
- **LangGraph**: v1.0.7 (upgraded from 0.0.20)
- **LangChain-OpenAI**: v1.1.7
- **LangChain-Anthropic**: v1.3.1
- **ChromaDB**: v0.6.6 (upgraded from 0.3.23)
- **Anthropic**: v0.76.0 (upgraded from 0.8.0)
- **Tiktoken**: v0.12.0 (upgraded from 0.5.2)
- **FastAPI**: Latest
- **Uvicorn**: Latest
- **Pydantic**: v2.x with pydantic-settings

### Development Dependencies:
- **pytest**: v9.0.2
- **pytest-asyncio**: v1.3.0
- **pytest-cov**: v7.0.0
- **black**: v26.1.0
- **ruff**: v0.14.14
- **mypy**: v1.19.1
- **pre-commit**: v4.5.1

## Fixed Issues

### 1. Anthropic Version Conflict
**Problem**: `langchain-anthropic ^0.1.0` required `anthropic >=0.16.0`, but pyproject.toml specified `^0.8.0`
**Solution**: Updated to `anthropic = "^0.23.0"`

### 2. Tiktoken Python 3.14 Compatibility
**Problem**: `tiktoken 0.5.2` used PyO3 0.20.3 which only supports Python up to 3.12
**Solution**: Upgraded to `tiktoken = "^0.8.0"` (installed v0.12.0)

### 3. LangChain Document Import
**Problem**: `from langchain.docstore.document import Document` was deprecated
**Solution**: Updated to `from langchain_core.documents import Document`

### 4. ChromaDB Pydantic Compatibility
**Problem**: Old ChromaDB 0.3.23 incompatible with Pydantic v2
**Solution**: Upgraded to ChromaDB 0.6.6

## Installation Methods

### Method 1: Using pip with venv (Recommended for Python 3.14)

```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate.fish  # or source venv/bin/activate for bash

# Upgrade pip
pip install --upgrade pip setuptools wheel

# Install core dependencies
pip install langchain langgraph langchain-openai langchain-anthropic \
    chromadb faiss-cpu pydantic pydantic-settings fastapi \
    uvicorn[standard] click python-dotenv aiohttp tiktoken openai anthropic

# Install development dependencies
pip install pytest pytest-asyncio pytest-cov black ruff mypy pre-commit
```

### Method 2: Using Poetry (for Python 3.11-3.12)

```bash
# Install Poetry
pip install poetry

# Install dependencies
poetry install
```

## Verification

Test that OpenAspen imports successfully:

```bash
source venv/bin/activate.fish
python -c "import openaspen; print('✅ OpenAspen imported successfully!')"
```

Expected output:
```
✅ OpenAspen imported successfully!
```

## Environment Setup

1. Copy the example environment file:
```bash
cp .env.example .env
```

2. Add your API keys to `.env`:
```bash
OPENAI_API_KEY=sk-your-key-here
ANTHROPIC_API_KEY=sk-ant-your-key-here
# Optional: GROK_API_KEY, etc.
```

## Running Examples

```bash
# Activate virtual environment
source venv/bin/activate.fish

# Run basic example
python examples/basic_tree.py

# Run advanced example
python examples/advanced_tree.py

# Start API server
python examples/server_example.py
```

## Known Warnings

You may see this warning (it's safe to ignore):
```
UserWarning: Core Pydantic V1 functionality isn't compatible with Python 3.14 or greater.
```

This is a deprecation warning from LangChain's internal use of Pydantic v1 compatibility layer. It doesn't affect functionality.

## Troubleshooting

### If you encounter module import errors:
```bash
# Reinstall in the virtual environment
source venv/bin/activate.fish
pip install --force-reinstall langchain langchain-core langchain-community
```

### If ChromaDB fails to initialize:
```bash
# Clear the ChromaDB directory
rm -rf ./chroma_db
```

### If tiktoken build fails:
```bash
# Use the forward compatibility flag
PYO3_USE_ABI3_FORWARD_COMPATIBILITY=1 pip install tiktoken
```

## Next Steps

1. ✅ Dependencies installed
2. ✅ Import verification passed
3. 📝 Configure your API keys in `.env`
4. 🚀 Run the examples
5. 🧪 Run tests: `pytest tests/`
6. 📖 Read the documentation in `docs/`

## Support

- **Documentation**: See `README.md`, `docs/QUICKSTART.md`, `docs/ARCHITECTURE.md`
- **Examples**: Check `examples/` directory
- **Getting Started**: See `GETTING_STARTED.md`

---

**Installation completed successfully! 🎉**
