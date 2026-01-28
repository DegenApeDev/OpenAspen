# LangChain Hub Integration

OpenAspen integrates LangChain Hub tools directly as "leaves" for instant skills—pull 100+ pre-built tools (search, APIs, DBs) without coding, then customize for your crypto/social needs.

## Overview

LangChain Hub ([hub.langchain.com](https://hub.langchain.com)) hosts ready-to-use tools like TavilySearch, Wikipedia, YouTube, Reddit. OpenAspen makes it easy to load these tools and integrate them into your agent tree structure.

## Quick Start

### CLI Usage

```bash
# List available LangChain Hub tools
openaspen grow_leaf --list-tools

# Add a tool to a branch
openaspen grow_leaf crypto_branch tavily_search --hub --config tree.json --leaf-name news_scan

# Add DuckDuckGo search (no API key required)
openaspen grow_leaf research_branch duckduckgo_search --hub --config tree.json
```

### Programmatic Usage

```python
from openaspen import OpenAspenTree
from openaspen.llm.providers import create_llm_config
from openaspen.integrations.langchain_hub import LangChainHubLoader

# Create tree
llm_configs = {
    "openai": create_llm_config(provider="openai", model="gpt-4-turbo-preview"),
}
tree = OpenAspenTree(name="my_tree", llm_configs=llm_configs)
branch = tree.add_branch("crypto_intel", llm_provider="openai")

# Add LangChain Hub tool as a leaf
leaf = await LangChainHubLoader.add_hub_tool_to_branch(
    branch=branch,
    tool_name="tavily_search",
    leaf_name="news_scan",
    rag_db=tree.shared_rag_db,
)
```

## Available Tools

### Top 10 for DEGEN Start

| Category | Hub Tool | Use Case | API Key Required |
|----------|----------|----------|------------------|
| **Search** | `tavily_search` | Trend scanning, real-time web search | TAVILY_API_KEY |
| **Search** | `duckduckgo_search` | Web search (no API key) | None |
| **Social** | `reddit_search` | Reddit posts/comments | None |
| **Social** | `youtube_search` | YouTube videos | None |
| **Finance** | `yahoo_finance_news` | Crypto/stock news | None |
| **Content** | `wikipedia` | Encyclopedic info | None |
| **Utils** | `requests_get` | HTTP GET requests | None |
| **Utils** | `requests_post` | HTTP POST requests | None |
| **Code** | `python_repl` | Execute Python code | None |
| **Research** | `arxiv` | Scientific papers | None |

### Full Tool List

Run `openaspen grow_leaf --list-tools` to see all available tools with descriptions.

## How It Works

### 1. Tool Loading

LangChain Hub tools are loaded dynamically from `langchain_community.tools`:

```python
from openaspen.integrations.langchain_hub import load_hub_tools

# Load single tool
tools = load_hub_tools("duckduckgo_search")

# Load multiple tools
tools = load_hub_tools(["tavily_search", "wikipedia"])
```

### 2. Leaf Creation

Tools are wrapped in OpenAspen `Leaf` objects with async compatibility:

```python
leaf = LangChainHubLoader.create_leaf_from_hub(
    tool_name="tavily_search",
    leaf_name="deep_search",
    custom_params={"max_results": 10},
    llm_provider="openai",
)
```

### 3. Tree Integration

Leaves are added to branches and indexed in RAG for auto-discovery:

```python
# Add to branch
branch.add_child(leaf)

# Index in RAG for semantic search
await tree.shared_rag_db.index_leaf(leaf, branch.name)
```

### 4. Agent Discovery

Agents automatically discover tools via:
- **Descriptions**: Semantic matching of tool descriptions
- **RAG Embeddings**: Vector similarity search across all leaves
- **Tree Context**: Hierarchical organization by branch

## Custom Parameters

Override default parameters when loading tools:

```python
# Tavily with more results
leaf = LangChainHubLoader.create_leaf_from_hub(
    tool_name="tavily_search",
    custom_params={"max_results": 10, "search_depth": "advanced"},
)

# Wikipedia with custom API wrapper
from langchain_community.utilities import WikipediaAPIWrapper
api_wrapper = WikipediaAPIWrapper(top_k_results=5, doc_content_chars_max=4000)
leaf = LangChainHubLoader.create_leaf_from_hub(
    tool_name="wikipedia",
    custom_params={"api_wrapper": api_wrapper},
)
```

## API Keys

Some tools require API keys. Set them in your `.env` file:

```bash
# Tavily Search
TAVILY_API_KEY=your_tavily_api_key

# OpenAI (for LLM)
OPENAI_API_KEY=your_openai_api_key

# Anthropic (optional)
ANTHROPIC_API_KEY=your_anthropic_api_key
```

## Examples

### Example 1: DEGEN Starter Tree

Build a complete crypto intelligence tree in minutes:

```python
import asyncio
from openaspen import OpenAspenTree
from openaspen.llm.providers import create_llm_config
from openaspen.integrations.langchain_hub import LangChainHubLoader

async def build_degen_tree():
    llm_configs = {
        "openai": create_llm_config(provider="openai", model="gpt-4-turbo-preview"),
    }
    
    tree = OpenAspenTree(name="degen_tree", llm_configs=llm_configs)
    
    # Crypto Intelligence Branch
    crypto = tree.add_branch("crypto_intel", llm_provider="openai")
    await LangChainHubLoader.add_hub_tool_to_branch(
        crypto, "duckduckgo_search", "market_search", rag_db=tree.shared_rag_db
    )
    await LangChainHubLoader.add_hub_tool_to_branch(
        crypto, "yahoo_finance_news", "finance_news", rag_db=tree.shared_rag_db
    )
    
    # Social Intelligence Branch
    social = tree.add_branch("social_intel", llm_provider="openai")
    await LangChainHubLoader.add_hub_tool_to_branch(
        social, "reddit_search", "reddit_scan", rag_db=tree.shared_rag_db
    )
    await LangChainHubLoader.add_hub_tool_to_branch(
        social, "youtube_search", "youtube_scan", rag_db=tree.shared_rag_db
    )
    
    print(tree.visualize())
    return tree

asyncio.run(build_degen_tree())
```

### Example 2: Custom DEGEN Leaf

Combine hub tools with custom Python skills:

```python
from openaspen.integrations.langchain_hub import LangChainHubLoader
import asyncio

async def coingecko_price(symbol: str) -> dict:
    """Custom leaf: Get crypto price from CoinGecko API"""
    import aiohttp
    async with aiohttp.ClientSession() as session:
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={symbol}&vs_currencies=usd"
        async with session.get(url) as resp:
            return await resp.json()

# Add custom leaf alongside hub tools
crypto_branch = tree.add_branch("crypto_intel")
await tree.spawn_leaf(crypto_branch, "coingecko_price", coingecko_price, "Get crypto prices")

# Add hub tool
await LangChainHubLoader.add_hub_tool_to_branch(
    crypto_branch, "duckduckgo_search", "market_search", rag_db=tree.shared_rag_db
)
```

### Example 3: CLI Workflow

```bash
# 1. Initialize tree
openaspen init --name degen_tree --output degen.json

# 2. List available tools
openaspen grow_leaf --list-tools

# 3. Add tools to branches
openaspen grow_leaf general_assistant duckduckgo_search --hub --config degen.json
openaspen grow_leaf general_assistant wikipedia --hub --config degen.json

# 4. Visualize tree
openaspen visualize degen.json

# 5. Run queries
openaspen run degen.json -q "What's the latest Bitcoin news?"
```

## Advanced Usage

### Direct LangChain Tool Usage

Use LangChain tools directly without OpenAspen wrapper:

```python
from langchain_community.tools import TavilySearchResults

tool = TavilySearchResults(max_results=5)
result = tool.run("latest crypto trends")
```

### Custom Tool Wrapper

Create your own wrapper for specialized behavior:

```python
from openaspen.core.leaf import Leaf
import asyncio

class CustomTavilyLeaf(Leaf):
    def __init__(self, name: str, max_results: int = 5):
        from langchain_community.tools import TavilySearchResults
        self.tavily = TavilySearchResults(max_results=max_results)
        
        async def wrapper(query: str, **kwargs):
            result = await asyncio.to_thread(self.tavily.run, query)
            # Custom post-processing
            return {"query": query, "results": result, "source": "tavily"}
        
        super().__init__(name=name, tool_func=wrapper, description="Custom Tavily search")
```

## Dependencies

Required packages (already in `pyproject.toml`):

```toml
langchain = "^1.2.0"
langchain-community = "^0.3.0"
```

Optional for specific tools:

```bash
# Tavily Search
pip install tavily-python

# Wikipedia
pip install wikipedia

# DuckDuckGo (usually included)
pip install duckduckgo-search

# Experimental tools (Python REPL)
pip install langchain-experimental
```

## Best Practices

1. **Start with no-API-key tools**: Use `duckduckgo_search`, `wikipedia` for quick testing
2. **Group by domain**: Organize tools into branches (crypto, social, research)
3. **Use RAG indexing**: Always pass `rag_db` for semantic tool discovery
4. **Custom leaves for specialized logic**: Combine hub tools with your own Python functions
5. **Test incrementally**: Add one tool at a time, verify it works before adding more

## Troubleshooting

### Tool not found error

```python
ValueError: Tool 'xyz' not found
```

**Solution**: Run `openaspen grow_leaf --list-tools` to see available tools.

### Import error

```python
ImportError: No module named 'tavily'
```

**Solution**: Install the required package: `pip install tavily-python`

### API key missing

```python
Warning: API key 'TAVILY_API_KEY' not found
```

**Solution**: Add the key to your `.env` file or use tools that don't require API keys.

### Async execution issues

If a tool doesn't support async, the wrapper automatically uses `asyncio.to_thread()` to run it in a thread pool.

## Contributing

To add new LangChain Hub tools to OpenAspen:

1. Add tool info to `AVAILABLE_TOOLS` dict in `langchain_hub.py`
2. Include: `import_path`, `class_name`, `description`, `default_params`, `requires_api_key`
3. Test with the test suite: `pytest tests/test_langchain_hub.py`
4. Update this documentation

## Resources

- [LangChain Tools Documentation](https://docs.langchain.com/oss/python/integrations/tools)
- [LangChain Community Tools](https://reference.langchain.com/v0.3/python/community/tools.html)
- [LangChain Hub](https://hub.langchain.com)
- [OpenAspen Examples](../examples/langchain_hub_example.py)

## Next Steps

1. **MVP in 2 minutes**: Run the DEGEN starter example
2. **Explore tools**: Try different hub tools for your use case
3. **Build custom leaves**: Combine hub tools with your own Python skills
4. **Scale up**: Add more branches and tools as needed
5. **Deploy**: Use OpenAspen server for production deployment

Skip building basics—import, test, and focus your Python skills on custom DEGEN leaves like `coingecko_price`. Your MVP tree is ready today! 🚀
