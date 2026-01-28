# LangChain Hub Quickstart - 2 Minute Setup

Get 100+ pre-built tools (search, APIs, DBs) without coding. Perfect for DEGEN crypto/social intelligence trees.

## Install

```bash
# Core package
pip install openaspen

# Optional: Install hub tool dependencies
pip install openaspen[hub-tools]

# Or install specific tools only
pip install duckduckgo-search wikipedia tavily-python
```

## CLI: 2-Minute Tree

```bash
# 1. Initialize tree
openaspen init --name degen_tree --output degen.json

# 2. List available tools
openaspen grow_leaf --list-tools

# 3. Add tools (no API key required)
openaspen grow_leaf general_assistant duckduckgo_search --hub --config degen.json
openaspen grow_leaf general_assistant wikipedia --hub --config degen.json

# 4. Test it
openaspen run degen.json -q "What is Bitcoin?"
```

## Code: 5-Line Integration

```python
import asyncio
from openaspen import OpenAspenTree
from openaspen.llm.providers import create_llm_config
from openaspen.integrations.langchain_hub import LangChainHubLoader

async def main():
    tree = OpenAspenTree(
        name="degen_tree",
        llm_configs={"openai": create_llm_config(provider="openai")}
    )
    
    branch = tree.add_branch("crypto_intel", llm_provider="openai")
    
    # Add LangChain Hub tool as a leaf
    await LangChainHubLoader.add_hub_tool_to_branch(
        branch=branch,
        tool_name="duckduckgo_search",
        leaf_name="web_search",
        rag_db=tree.shared_rag_db,
    )
    
    result = await tree.execute("Latest crypto news")
    print(result)

asyncio.run(main())
```

## Top 10 Tools for DEGEN

| Tool | Use | API Key? |
|------|-----|----------|
| `duckduckgo_search` | Web search | ❌ No |
| `tavily_search` | Advanced search | ✅ TAVILY_API_KEY |
| `wikipedia` | Encyclopedia | ❌ No |
| `reddit_search` | Reddit intel | ❌ No |
| `youtube_search` | YouTube scan | ❌ No |
| `yahoo_finance_news` | Finance news | ❌ No |
| `requests_get` | API calls | ❌ No |
| `python_repl` | Run Python | ❌ No |
| `arxiv` | Research papers | ❌ No |

## Full Example

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
    
    # Crypto branch
    crypto = tree.add_branch("crypto_intel", llm_provider="openai")
    await LangChainHubLoader.add_hub_tool_to_branch(
        crypto, "duckduckgo_search", "market_search", rag_db=tree.shared_rag_db
    )
    await LangChainHubLoader.add_hub_tool_to_branch(
        crypto, "yahoo_finance_news", "finance_news", rag_db=tree.shared_rag_db
    )
    
    # Social branch
    social = tree.add_branch("social_intel", llm_provider="openai")
    await LangChainHubLoader.add_hub_tool_to_branch(
        social, "reddit_search", "reddit_scan", rag_db=tree.shared_rag_db
    )
    
    print(tree.visualize())
    return tree

asyncio.run(build_degen_tree())
```

## Add Custom Leaves

Combine hub tools with your own Python skills:

```python
async def coingecko_price(symbol: str, **kwargs):
    """Get crypto price from CoinGecko"""
    import aiohttp
    async with aiohttp.ClientSession() as session:
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={symbol}&vs_currencies=usd"
        async with session.get(url) as resp:
            return await resp.json()

# Add custom leaf
await tree.spawn_leaf(
    crypto_branch,
    "coingecko_price",
    coingecko_price,
    "Get real-time crypto prices"
)
```

## Next Steps

1. **Run the quickstart**: `python examples/degen_quickstart.py`
2. **Read full docs**: `docs/LANGCHAIN_HUB_INTEGRATION.md`
3. **Run tests**: `pytest tests/test_langchain_hub.py`
4. **Build your tree**: Focus on custom DEGEN leaves, use hub tools for basics

🚀 **MVP ready in 2 minutes. Skip building basics—import, test, ship!**
