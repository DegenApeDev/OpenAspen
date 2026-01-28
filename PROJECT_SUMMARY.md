# OpenAspen Project Summary

## 🎯 Project Overview

OpenAspen is a complete, production-ready, open-source framework for building tree-structured AI agent systems with multi-LLM orchestration and hierarchical RAG (Retrieval-Augmented Generation).

**Version:** 0.1.0  
**License:** MIT  
**Python:** 3.11+  
**Status:** ✅ Complete and Ready for Use

## 📦 What's Included

### Core Framework (`openaspen/`)

1. **Core Components** (`core/`)
   - `node.py` - Abstract TreeNode base class
   - `branch.py` - Branch (Agent) implementation
   - `leaf.py` - Leaf (Skill/Tool) implementation
   - `tree.py` - OpenAspenTree orchestrator

2. **LLM Integration** (`llm/`)
   - `providers.py` - LLM provider configurations
   - `router.py` - Multi-LLM intelligent routing

3. **RAG System** (`rag/`)
   - `embeddings.py` - Embedding management
   - `store.py` - GroupRAG vector store with ChromaDB

4. **API Server** (`server/`)
   - `api.py` - FastAPI server with OpenAI-compatible endpoints

5. **CLI** (`cli.py`)
   - Commands: init, run, visualize, info

6. **Utilities** (`utils/`)
   - `logging.py` - Logging configuration

### Examples (`examples/`)

- `basic_tree.py` - Simple getting started example
- `advanced_tree.py` - Production-ready crypto intelligence system
- `server_example.py` - API server deployment
- `tree.json` - Example tree configuration
- `README.md` - Examples documentation

### Tests (`tests/`)

- `test_core.py` - Core component tests
- `test_llm.py` - LLM router tests
- `test_tree.py` - Tree orchestration tests
- `test_rag.py` - RAG system tests

### Documentation (`docs/`)

- `ARCHITECTURE.md` - Detailed architecture guide
- `QUICKSTART.md` - Quick start tutorial

### Project Files

- `README.md` - Main documentation (comprehensive)
- `CONTRIBUTING.md` - Contribution guidelines
- `CHANGELOG.md` - Version history
- `LICENSE` - MIT License
- `pyproject.toml` - Poetry dependencies
- `Makefile` - Development commands
- `pytest.ini` - Test configuration
- `.env.example` - Environment variable template
- `.gitignore` - Git ignore rules
- `.pre-commit-config.yaml` - Pre-commit hooks

### CI/CD (`.github/workflows/`)

- `ci.yml` - GitHub Actions workflow

### Scripts (`scripts/`)

- `setup_dev.sh` - Development environment setup
- `run_tests.sh` - Test runner

## 🌟 Key Features

### 1. Tree-Structured Architecture
- Hierarchical organization: Tree → Branches (Agents) → Leaves (Skills)
- Dynamic tree growth and modification
- Path-based navigation and context

### 2. Multi-LLM Support
- **OpenAI** (GPT-4, GPT-3.5)
- **Anthropic** (Claude 3)
- **Grok** (X.AI)
- **Ollama** (Local models)
- **LM Studio** (Local models)

### 3. Intelligent Routing
- Route by cost (cheapest within budget)
- Route by speed (fastest available)
- Route by skill type (coding, creative, etc.)

### 4. Group RAG System
- Shared ChromaDB vector store
- Cross-agent context awareness
- Automatic skill indexing
- Similarity-based search

### 5. Production Features
- Async-first architecture
- Type-safe with Pydantic
- Comprehensive error handling
- Execution history tracking
- OpenAI-compatible API
- CLI tools
- Extensive testing

## 🚀 Quick Start

### Installation

```bash
# Clone and install
git clone <your-repo-url>
cd OpenAspen
poetry install

# Or use setup script
bash scripts/setup_dev.sh
```

### Basic Usage

```python
import asyncio
from openaspen import OpenAspenTree
from openaspen.llm.providers import create_llm_config

async def my_skill(input_data: str) -> str:
    return f"Processed: {input_data}"

async def main():
    llm_configs = {
        "openai": create_llm_config(provider="openai", api_key="sk-...")
    }
    
    tree = OpenAspenTree(llm_configs=llm_configs)
    branch = tree.grow_branch("my_agent")
    await tree.spawn_leaf(branch, "my_skill", my_skill)
    await tree.index_tree()
    
    result = await tree.execute("Hello!")
    print(result)

asyncio.run(main())
```

### CLI Usage

```bash
# Initialize
openaspen init --name my_tree

# Run
openaspen run tree.json --query "Your query"

# Interactive
openaspen run tree.json --interactive
```

### API Server

```bash
python examples/server_example.py
# Server runs on http://localhost:8000
```

## 📊 Project Statistics

- **Total Files:** 40+
- **Lines of Code:** ~3,500+
- **Test Coverage:** Comprehensive unit and integration tests
- **Documentation:** 5 major docs + inline docstrings
- **Examples:** 3 working examples + config
- **Supported LLMs:** 5 providers

## 🏗️ Architecture Highlights

### Component Hierarchy

```
OpenAspenTree (Orchestrator)
├── LLMRouter (Multi-provider routing)
├── GroupRAGStore (Shared vector DB)
└── Branches (Agents)
    └── Leaves (Skills/Tools)
```

### Execution Flow

```
Query → Tree → RAG Search → Best Branch → RAG Search → 
LLM Decision → Best Leaf → Tool Execution → Result
```

### Design Patterns

- **Abstract Base Classes** for extensibility
- **Async/Await** throughout for performance
- **Dependency Injection** for testability
- **Configuration-Driven** for flexibility
- **Type Safety** with Pydantic

## 🧪 Testing

```bash
# Run all tests
make test

# Fast test run
make test-fast

# With coverage report
poetry run pytest --cov=openaspen --cov-report=html
```

## 📚 Documentation Structure

1. **README.md** - Main entry point, features, quick start
2. **QUICKSTART.md** - Step-by-step tutorial
3. **ARCHITECTURE.md** - Deep dive into design
4. **CONTRIBUTING.md** - How to contribute
5. **examples/README.md** - Example explanations

## 🔧 Development

```bash
# Setup
make install
make pre-commit

# Format code
make format

# Lint
make lint

# Run example
make run-example

# Start server
make run-server
```

## 🌐 Deployment Options

### 1. Python Package
```bash
poetry build
poetry publish
pip install openaspen
```

### 2. API Server
```bash
uvicorn openaspen.server.api:app --host 0.0.0.0 --port 8000
```

### 3. Docker (Future)
```bash
docker build -t openaspen .
docker run -p 8000:8000 openaspen
```

## 📈 Roadmap

### Current (v0.1.0)
- ✅ Core tree architecture
- ✅ Multi-LLM routing
- ✅ Group RAG with ChromaDB
- ✅ CLI and API server
- ✅ Comprehensive tests
- ✅ Full documentation

### Future
- [ ] FAISS vector store
- [ ] LangGraph workflows
- [ ] Streaming responses
- [ ] Agent memory
- [ ] Web UI
- [ ] More LLM providers
- [ ] Distributed execution

## 🎓 Learning Resources

### For Beginners
1. Read `README.md`
2. Follow `docs/QUICKSTART.md`
3. Run `examples/basic_tree.py`
4. Experiment with CLI

### For Advanced Users
1. Study `docs/ARCHITECTURE.md`
2. Explore `examples/advanced_tree.py`
3. Review test suite
4. Build custom agents

### For Contributors
1. Read `CONTRIBUTING.md`
2. Run `scripts/setup_dev.sh`
3. Check open issues
4. Submit PRs

## 🤝 Community

- **Issues:** Bug reports and feature requests
- **Discussions:** Questions and ideas
- **PRs:** Code contributions welcome
- **Stars:** Show your support! ⭐

## 📄 License

MIT License - Free for commercial and personal use

## 🙏 Acknowledgments

Built with:
- LangChain & LangGraph
- ChromaDB
- FastAPI
- Pydantic
- Poetry

Inspired by nature's most resilient trees 🌲

## 📞 Support

- GitHub Issues: Technical problems
- GitHub Discussions: General questions
- Documentation: Comprehensive guides
- Examples: Working code samples

---

**OpenAspen v0.1.0** - Build intelligent, interconnected AI agent systems that grow and adapt like nature's most resilient trees.

*Made with ❤️ for the AI agent community*
