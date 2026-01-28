# 🌲 OpenAspen

**Open-source tree-structured AI agent framework for multi-LLM orchestration with hierarchical RAG**

OpenAspen is a modular, production-ready framework that structures AI agents like an aspen tree: a shared root system (group RAG) connecting multiple trunks (agents/branches) with specialized leaves (skills/tools). It's 10x more powerful than traditional single-agent systems through intelligent multi-LLM routing and cross-agent context sharing.

[![CI](https://github.com/yourusername/openaspen/workflows/CI/badge.svg)](https://github.com/yourusername/openaspen/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)

## ✨ Features

- 🌳 **Tree-Structured Architecture**: Hierarchical agent organization with branches (agents) and leaves (skills)
- 💰 **Zero API Keys Required**: Works completely FREE with LM Studio (local LLM)
- 🤖 **Multi-LLM Support**: LM Studio (default), Grok (primary cloud), OpenAI/Anthropic (optional)
- 🧠 **Group RAG**: Shared vector database across all agents for cross-context awareness
- 🔧 **LangChain Hub Integration**: 100+ pre-built tools (search, APIs, DBs) as instant skills—no coding required
- ⚡ **Async-First**: Built on asyncio for high-performance concurrent execution
- 🎯 **Smart Routing**: Route by cost, speed, or skill type automatically
- 🔌 **OpenAI-Compatible API**: Drop-in replacement for OpenAI API endpoints
- 🛠️ **CLI Tools**: Initialize, run, and visualize trees from the command line
- 📦 **Production-Ready**: Type-safe with Pydantic, tested with pytest, CI/CD ready

## 🚀 Quick Start

### Installation (Zero API Keys Required!)

```bash
# Clone the repository
git clone https://github.com/yourusername/openaspen.git
cd openaspen

# Create virtual environment
python3 -m venv venv
source venv/bin/activate.fish  # or: source venv/bin/activate

# Install core (no API keys needed)
pip install -e . --no-deps
pip install langchain langgraph langchain-community faiss-cpu \
    pydantic pydantic-settings fastapi uvicorn[standard] \
    click python-dotenv aiohttp psutil flask flask-socketio

# Install LangChain Hub tools (no API keys)
pip install duckduckgo-search wikipedia

# Install LM Studio for FREE local LLM
# Download from: https://lmstudio.ai/
```

### Build Your First Tree in 5 Lines (Zero API Keys!)

```python
import asyncio
from openaspen import OpenAspenTree
from openaspen.llm.providers import create_llm_config
from openaspen.integrations.langchain_hub import LangChainHubLoader

async def main():
    # 1. Configure LM Studio (FREE - no API key!)
    llm_configs = {
        "lmstudio": create_llm_config(
            provider="ollama",
            api_base="http://localhost:1234/v1",
            api_key="not-needed"
        ),
    }
    
    # 2. Create tree
    tree = OpenAspenTree(llm_configs=llm_configs, name="LocalTree")
    
    # 3. Grow a branch (agent)
    research = tree.add_branch(
        "research",
        description="Research assistant",
        llm_provider="lmstudio"
    )
    
    # 4. Add LangChain Hub tool (no coding!)
    await LangChainHubLoader.add_hub_tool_to_branch(
        research, "duckduckgo_search", "web_search", rag_db=tree.shared_rag_db
    )
    
    # 5. Execute queries
    result = await tree.execute("What is Python?")
    print(result)

asyncio.run(main())
```

**Prerequisites**: Install and start LM Studio from [lmstudio.ai](https://lmstudio.ai/)

### 🚀 LangChain Hub: Instant Skills in 2 Minutes

Skip building basics—load 100+ pre-built tools from LangChain Hub:

```python
import asyncio
from openaspen import OpenAspenTree
from openaspen.llm.providers import create_llm_config
from openaspen.integrations.langchain_hub import LangChainHubLoader

async def main():
    llm_configs = {"openai": create_llm_config(provider="openai")}
    tree = OpenAspenTree(name="degen_tree", llm_configs=llm_configs)
    
    # Add crypto intelligence branch
    crypto = tree.add_branch("crypto_intel", llm_provider="openai")
    
    # Load pre-built tools as leaves (no coding!)
    await LangChainHubLoader.add_hub_tool_to_branch(
        crypto, "duckduckgo_search", "market_search", rag_db=tree.shared_rag_db
    )
    await LangChainHubLoader.add_hub_tool_to_branch(
        crypto, "yahoo_finance_news", "finance_news", rag_db=tree.shared_rag_db
    )
    
    # Mix with custom leaves for specialized logic
    async def coingecko_price(symbol: str, **kwargs):
        import aiohttp
        async with aiohttp.ClientSession() as session:
            url = f"https://api.coingecko.com/api/v3/simple/price?ids={symbol}&vs_currencies=usd"
            async with session.get(url) as resp:
                return await resp.json()
    
    await tree.spawn_leaf(crypto, "coingecko_price", coingecko_price, "Get crypto prices")
    
    # Query the tree
    result = await tree.execute("What's the latest Bitcoin news?")
    print(result)

asyncio.run(main())
```

**Available Hub Tools**: `duckduckgo_search`, `tavily_search`, `wikipedia`, `reddit_search`, `youtube_search`, `yahoo_finance_news`, `requests_get`, `python_repl`, `arxiv`, and more!

📚 **See**: [`docs/QUICKSTART_LANGCHAIN_HUB.md`](docs/QUICKSTART_LANGCHAIN_HUB.md) | [`docs/LANGCHAIN_HUB_INTEGRATION.md`](docs/LANGCHAIN_HUB_INTEGRATION.md)

## 🏗️ Architecture

```
🌲 OpenAspenTree (Trunk)
├── 🌿 Branch: crypto_analyzer (Agent)
│   ├── 🍃 Leaf: price_check (Skill)
│   ├── 🍃 Leaf: portfolio_value
│   └── 🍃 Leaf: trend_analysis
├── 🌿 Branch: research_assistant
│   ├── 🍃 Leaf: web_search
│   └── 🍃 Leaf: summarize
└── 🌿 Branch: dev_tools
    ├── 🍃 Leaf: code_analyzer
    └── 🍃 Leaf: debug_helper

💾 Shared RAG Database (Root System)
   └── Cross-agent context sharing
```

### Core Components

1. **TreeNode** (Abstract Base): Foundation for all tree components
2. **Branch** (Agent): Skill hub that routes queries to appropriate leaves
3. **Leaf** (Skill/Tool): Granular, executable function with RAG-enhanced discovery
4. **OpenAspenTree** (Orchestrator): Manages the entire tree, LLM routing, and execution
5. **GroupRAGStore**: Shared ChromaDB vector store for cross-agent context
6. **LLMRouter**: Intelligent multi-provider LLM routing and management

## 📖 Usage Examples

### Multi-LLM Configuration

**Priority: LM Studio (free) → Grok (fast cloud) → OpenAI/Anthropic (optional)**

```python
from openaspen.llm.providers import create_llm_config
import os

llm_configs = {
    # LM Studio - FREE local LLM (default, no API key)
    "lmstudio": create_llm_config(
        provider="ollama",
        api_base="http://localhost:1234/v1",
        api_key="not-needed"
    ),
    
    # Grok - Primary cloud option (fast, affordable)
    "grok": create_llm_config(
        provider="openai",  # Grok uses OpenAI-compatible API
        model="grok-beta",
        api_key=os.getenv("GROK_API_KEY"),
        api_base="https://api.x.ai/v1"
    ),
    
    # OpenAI - Optional premium (if you have API key)
    "openai": create_llm_config(
        provider="openai",
        model="gpt-4-turbo-preview",
        api_key=os.getenv("OPENAI_API_KEY")
    ),
    
    # Anthropic - Optional premium (if you have API key)
    "anthropic": create_llm_config(
        provider="anthropic",
        model="claude-3-opus-20240229",
        api_key=os.getenv("ANTHROPIC_API_KEY")
    ),
}
```

### Dynamic Tree Growth

```python
# Add branches dynamically
research = tree.grow_branch(
    "research_assistant",
    description="Web research and analysis",
    llm_provider="anthropic",
    system_prompt="You are a thorough researcher."
)

# Add skills to branches
await tree.spawn_leaf(
    research,
    "web_search",
    search_function,
    "Search the web for information"
)

# Nested branches for complex hierarchies
sub_branch = Branch(name="specialized_research")
research.add_child(sub_branch)
```

### Smart LLM Routing

```python
# Route by cost (cheapest with acceptable quality)
provider = tree.llm_router.route_by_cost(max_cost_per_1k=0.01)

# Route by speed (fastest available)
provider = tree.llm_router.route_by_speed(min_speed_score=0.8)

# Route by skill type
provider = tree.llm_router.route_by_skill("coding")  # Prefers OpenAI/Anthropic
provider = tree.llm_router.route_by_skill("creative")  # Prefers Anthropic/Grok
provider = tree.llm_router.route_by_skill("local")  # Prefers Ollama/LM Studio
```

### Group RAG (Cross-Agent Context)

```python
# Automatically indexes all branches and leaves
await tree.index_tree()

# Query finds relevant skills across ALL branches
result = await tree.execute("Analyze Bitcoin price trends")
# Might use crypto_analyzer.price_check + research_assistant.web_search

# Get sibling context (what other agents know)
sibling_docs = await tree.shared_rag_db.get_sibling_context(
    branch_name="crypto_analyzer",
    query="market sentiment",
    k=3
)
```

## 🖥️ CLI Usage

```bash
# Initialize a new tree
openaspen init --name my_tree --output tree.json

# Run a tree with a query
openaspen run tree.json --query "What's the weather?"

# Interactive mode
openaspen run tree.json --interactive

# Visualize tree structure
openaspen visualize tree.json

# Get tree information
openaspen info tree.json

# LangChain Hub: List available tools
openaspen grow_leaf --list-tools

# LangChain Hub: Add pre-built tools as leaves
openaspen grow_leaf crypto_branch duckduckgo_search --hub --config tree.json
openaspen grow_leaf research_branch wikipedia --hub --config tree.json --leaf-name wiki_search
```

## 🌐 API Server

Start an OpenAI-compatible API server:

```bash
# Using the CLI
python -m openaspen.server.api

# Or with a config file
python examples/server_example.py
```

**Endpoints:**
- `POST /v1/chat/completions` - OpenAI-compatible chat endpoint
- `GET /v1/models` - List available models
- `GET /tree/info` - Tree structure and stats
- `GET /tree/visualize` - ASCII tree visualization
- `POST /tree/execute` - Direct query execution
- `GET /health` - Health check

**Example Request:**

```bash
curl -X POST http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "openaspen",
    "messages": [{"role": "user", "content": "What is Bitcoin price?"}]
  }'
```

## 🧪 Testing

```bash
# Run all tests
poetry run pytest

# With coverage
poetry run pytest --cov=openaspen --cov-report=html

# Run specific test file
poetry run pytest tests/test_core.py

# Run with verbose output
poetry run pytest -v
```

## 📁 Project Structure

```
openaspen/
├── openaspen/
│   ├── core/
│   │   ├── node.py          # TreeNode base class
│   │   ├── branch.py        # Branch (Agent) implementation
│   │   ├── leaf.py          # Leaf (Skill) implementation
│   │   └── tree.py          # OpenAspenTree orchestrator
│   ├── llm/
│   │   ├── providers.py     # LLM provider configs
│   │   └── router.py        # Multi-LLM routing logic
│   ├── rag/
│   │   ├── embeddings.py    # Embedding management
│   │   └── store.py         # GroupRAG vector store
│   ├── integrations/
│   │   ├── langchain_hub.py # LangChain Hub tool loader
│   │   ├── telegram.py      # Telegram bot integration
│   │   └── whatsapp.py      # WhatsApp integration
│   ├── server/
│   │   └── api.py           # FastAPI server
│   └── cli.py               # CLI interface
├── examples/
│   ├── basic_tree.py        # Simple example
│   ├── advanced_tree.py     # Complex multi-agent example
│   ├── langchain_hub_example.py  # LangChain Hub examples
│   ├── degen_quickstart.py  # DEGEN crypto tree quickstart
│   ├── server_example.py    # API server example
│   └── tree.json            # Example tree config
├── tests/                   # Comprehensive test suite
│   └── test_langchain_hub.py  # LangChain Hub tests
├── docs/
│   ├── LANGCHAIN_HUB_INTEGRATION.md  # Full Hub docs
│   └── QUICKSTART_LANGCHAIN_HUB.md   # 2-min quickstart
├── pyproject.toml           # Poetry dependencies
└── README.md
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file:

```bash
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
GROK_API_KEY=xai-...
```

### Tree Configuration (JSON)

```json
{
  "name": "MyTree",
  "branches": [
    {
      "name": "agent_name",
      "description": "Agent description",
      "llm_provider": "openai",
      "system_prompt": "You are a helpful assistant."
    }
  ],
  "llm_providers": {
    "openai": {
      "provider": "openai",
      "model": "gpt-4-turbo-preview",
      "temperature": 0.7,
      "max_tokens": 2000
    }
  }
}
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Development Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/openaspen.git
cd openaspen

# Install dependencies
poetry install

# Install pre-commit hooks
poetry run pre-commit install

# Run tests
poetry run pytest
```

## 📊 Performance

- **Async-first**: Non-blocking I/O for concurrent agent execution
- **Smart caching**: LLM instances cached and reused
- **Efficient RAG**: ChromaDB with optimized similarity search
- **Minimal overhead**: Direct function calls for leaf execution

## 🗺️ Roadmap

- [x] **LangChain Hub integration** - 100+ pre-built tools as instant skills
- [ ] FAISS vector store support (alternative to ChromaDB)
- [ ] LangGraph integration for complex agent workflows
- [ ] Streaming responses for real-time output
- [ ] Agent memory and conversation history
- [ ] Web UI for tree visualization and management
- [ ] More LLM providers (Cohere, AI21, etc.)
- [ ] Enhanced tool calling / function calling support
- [ ] Distributed execution across multiple machines

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [LangChain](https://github.com/langchain-ai/langchain) and [LangGraph](https://github.com/langchain-ai/langgraph)
- Vector storage powered by [ChromaDB](https://www.trychroma.com/)
- Inspired by the aspen tree's interconnected root system 🌲

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/openaspen/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/openaspen/discussions)
- **Documentation**: [Full Docs](https://openaspen.readthedocs.io) (coming soon)

---

**Made with ❤️ by the OpenAspen community**

*Build intelligent, interconnected AI agent systems that grow and adapt like nature's most resilient trees.*
