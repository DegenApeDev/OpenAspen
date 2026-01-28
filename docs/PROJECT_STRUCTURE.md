# OpenAspen Project Structure

## Complete File Tree

```
OpenAspen/
├── 📄 README.md                          # Main documentation
├── 📄 LICENSE                            # MIT License
├── 📄 CHANGELOG.md                       # Version history
├── 📄 CONTRIBUTING.md                    # Contribution guide
├── 📄 PROJECT_SUMMARY.md                 # Project overview
├── 📄 pyproject.toml                     # Poetry dependencies
├── 📄 Makefile                           # Development commands
├── 📄 pytest.ini                         # Pytest configuration
├── 📄 .gitignore                         # Git ignore rules
├── 📄 .env.example                       # Environment template
├── 📄 .pre-commit-config.yaml            # Pre-commit hooks
│
├── 📁 .github/
│   └── workflows/
│       └── ci.yml                        # GitHub Actions CI/CD
│
├── 📁 openaspen/                         # Main package
│   ├── __init__.py                       # Package exports
│   │
│   ├── 📁 core/                          # Core architecture
│   │   ├── __init__.py
│   │   ├── node.py                       # TreeNode base class
│   │   ├── branch.py                     # Branch (Agent)
│   │   ├── leaf.py                       # Leaf (Skill)
│   │   └── tree.py                       # OpenAspenTree orchestrator
│   │
│   ├── 📁 llm/                           # LLM integration
│   │   ├── __init__.py
│   │   ├── providers.py                  # Provider configs
│   │   └── router.py                     # Multi-LLM routing
│   │
│   ├── 📁 rag/                           # RAG system
│   │   ├── __init__.py
│   │   ├── embeddings.py                 # Embedding manager
│   │   └── store.py                      # GroupRAG vector store
│   │
│   ├── 📁 server/                        # API server
│   │   ├── __init__.py
│   │   └── api.py                        # FastAPI endpoints
│   │
│   ├── 📁 utils/                         # Utilities
│   │   ├── __init__.py
│   │   └── logging.py                    # Logging setup
│   │
│   └── cli.py                            # CLI interface
│
├── 📁 examples/                          # Usage examples
│   ├── README.md                         # Examples guide
│   ├── basic_tree.py                     # Simple example
│   ├── advanced_tree.py                  # Complex example
│   ├── server_example.py                 # API server
│   └── tree.json                         # Config example
│
├── 📁 tests/                             # Test suite
│   ├── __init__.py
│   ├── test_core.py                      # Core tests
│   ├── test_llm.py                       # LLM tests
│   ├── test_tree.py                      # Tree tests
│   └── test_rag.py                       # RAG tests
│
├── 📁 docs/                              # Documentation
│   ├── ARCHITECTURE.md                   # Architecture guide
│   ├── QUICKSTART.md                     # Quick start
│   └── PROJECT_STRUCTURE.md              # This file
│
└── 📁 scripts/                           # Dev scripts
    ├── setup_dev.sh                      # Setup script
    └── run_tests.sh                      # Test runner
```

## Module Breakdown

### Core Package (`openaspen/`)

**Total:** ~2,500 lines of production code

#### `core/` - Tree Architecture (800 LOC)
- `node.py` (150 LOC) - Abstract base with tree operations
- `branch.py` (200 LOC) - Agent with LLM routing
- `leaf.py` (150 LOC) - Skill with auto async detection
- `tree.py` (300 LOC) - Main orchestrator

#### `llm/` - Multi-LLM System (400 LOC)
- `providers.py` (150 LOC) - 5 provider configs
- `router.py` (250 LOC) - Intelligent routing logic

#### `rag/` - Vector Store (350 LOC)
- `embeddings.py` (100 LOC) - Embedding management
- `store.py` (250 LOC) - ChromaDB integration

#### `server/` - API (300 LOC)
- `api.py` (300 LOC) - FastAPI with 8 endpoints

#### `cli.py` - Command Line (200 LOC)
- 4 commands: init, run, visualize, info

#### `utils/` - Utilities (50 LOC)
- Logging configuration

### Examples (`examples/`)

**Total:** ~400 lines of example code

- `basic_tree.py` - Getting started (80 LOC)
- `advanced_tree.py` - Production example (200 LOC)
- `server_example.py` - API deployment (50 LOC)
- `tree.json` - Configuration (70 LOC)

### Tests (`tests/`)

**Total:** ~600 lines of test code

- `test_core.py` (200 LOC) - 15+ tests
- `test_llm.py` (150 LOC) - 10+ tests
- `test_tree.py` (150 LOC) - 10+ tests
- `test_rag.py` (100 LOC) - 5+ tests

### Documentation (`docs/`)

**Total:** ~15,000 words

- `ARCHITECTURE.md` - Deep technical dive
- `QUICKSTART.md` - Tutorial guide
- `PROJECT_STRUCTURE.md` - This file

## Component Dependencies

```
OpenAspenTree
├── depends on → LLMRouter
├── depends on → GroupRAGStore
└── contains → Branch[]
    └── contains → Leaf[]

LLMRouter
├── depends on → LLMConfig[]
└── creates → BaseChatModel instances

GroupRAGStore
├── depends on → EmbeddingManager
└── uses → ChromaDB

Branch (extends TreeNode)
├── uses → LLMRouter
├── uses → GroupRAGStore
└── contains → Leaf[]

Leaf (extends TreeNode)
└── wraps → user function
```

## Data Flow

```
User Query
    ↓
CLI / API / Direct Call
    ↓
OpenAspenTree.execute()
    ↓
GroupRAGStore.similarity_search()
    ↓
Select Best Branch
    ↓
Branch.execute()
    ↓
GroupRAGStore.similarity_search() (for leaves)
    ↓
LLMRouter.get_llm()
    ↓
LLM Decision
    ↓
Select Best Leaf
    ↓
Leaf.execute()
    ↓
User Function Call
    ↓
Result Aggregation
    ↓
Return to User
```

## Configuration Files

### `pyproject.toml`
- Poetry dependencies
- Dev dependencies
- Build configuration
- Tool settings (black, ruff, mypy, pytest)

### `.pre-commit-config.yaml`
- Black formatting
- Ruff linting
- Mypy type checking
- YAML/JSON validation

### `pytest.ini`
- Test discovery
- Coverage settings
- Async mode

### `.env.example`
- API key templates
- Configuration examples

## Entry Points

### Python API
```python
from openaspen import OpenAspenTree, Branch, Leaf
```

### CLI
```bash
openaspen [init|run|visualize|info]
```

### API Server
```bash
python -m openaspen.server.api
# or
uvicorn openaspen.server.api:app
```

## Development Workflow

```
1. Clone repo
2. Run scripts/setup_dev.sh
3. Edit code
4. Pre-commit hooks run (auto)
5. Run tests: make test
6. Submit PR
7. CI runs on GitHub
8. Merge
```

## Build Artifacts

### Generated (gitignored)
- `__pycache__/` - Python bytecode
- `.pytest_cache/` - Pytest cache
- `.mypy_cache/` - Mypy cache
- `.ruff_cache/` - Ruff cache
- `htmlcov/` - Coverage reports
- `chroma_db/` - ChromaDB storage
- `dist/` - Built packages
- `*.egg-info/` - Package metadata

### Persisted
- `poetry.lock` - Locked dependencies (optional)

## Installation Paths

### From PyPI (future)
```bash
pip install openaspen
# Installs to: site-packages/openaspen/
```

### From Source
```bash
poetry install
# Installs to: .venv/lib/python3.11/site-packages/openaspen/
```

### Development Mode
```bash
poetry install
# Editable install, changes reflect immediately
```

## Import Structure

```python
# Top-level imports
from openaspen import OpenAspenTree, Branch, Leaf, TreeNode

# Submodule imports
from openaspen.llm import LLMRouter, LLMProvider
from openaspen.llm.providers import create_llm_config
from openaspen.rag import GroupRAGStore, EmbeddingManager
from openaspen.server import create_app
```

## File Size Summary

| Category | Files | Total Size |
|----------|-------|------------|
| Source Code | 15 | ~100 KB |
| Tests | 4 | ~25 KB |
| Examples | 4 | ~15 KB |
| Documentation | 8 | ~80 KB |
| Config | 6 | ~10 KB |
| **Total** | **37** | **~230 KB** |

## Lines of Code

| Category | Lines |
|----------|-------|
| Production Code | ~2,500 |
| Test Code | ~600 |
| Example Code | ~400 |
| Documentation | ~15,000 words |
| Comments/Docstrings | ~500 |

## Key Design Decisions

1. **Async-First**: All execution paths are async for performance
2. **Type-Safe**: Pydantic models throughout
3. **Modular**: Clear separation of concerns
4. **Extensible**: Abstract bases for custom implementations
5. **Tested**: Comprehensive test coverage
6. **Documented**: Extensive docs and examples

## Extension Points

### Add New LLM Provider
- Edit: `openaspen/llm/providers.py`
- Edit: `openaspen/llm/router.py`
- Add tests: `tests/test_llm.py`

### Add New Vector Store
- Create: `openaspen/rag/new_store.py`
- Implement same interface as `GroupRAGStore`
- Add tests: `tests/test_rag.py`

### Add New Node Type
- Create: `openaspen/core/new_node.py`
- Extend: `TreeNode`
- Add to tree: `OpenAspenTree` methods

### Add New CLI Command
- Edit: `openaspen/cli.py`
- Add `@main.command()` decorator
- Update docs

## Maintenance

### Regular Tasks
- Update dependencies: `poetry update`
- Run tests: `make test`
- Format code: `make format`
- Check types: `make lint`

### Release Process
1. Update version in `pyproject.toml`
2. Update `CHANGELOG.md`
3. Run full test suite
4. Build: `poetry build`
5. Publish: `poetry publish`
6. Tag release on GitHub

---

**Last Updated:** 2026-01-27  
**Version:** 0.1.0  
**Maintainer:** OpenAspen Team
