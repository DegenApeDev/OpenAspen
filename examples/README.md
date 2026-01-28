# OpenAspen Examples

This directory contains example implementations demonstrating various OpenAspen features.

## Examples

### 1. Basic Tree (`basic_tree.py`)

**What it demonstrates:**
- Creating a simple tree with multiple branches
- Adding skills (leaves) to branches
- Multi-LLM configuration (OpenAI + Ollama)
- Tree indexing and visualization
- Query execution

**Run:**
```bash
poetry run python examples/basic_tree.py
```

**Use case:** Getting started with OpenAspen, understanding basic concepts.

---

### 2. Advanced Tree (`advanced_tree.py`)

**What it demonstrates:**
- Real-world cryptocurrency intelligence system
- Multiple specialized agents (market data, sentiment, strategy)
- Async API calls with aiohttp
- Multiple LLM providers (OpenAI, Anthropic, Grok)
- Execution history tracking
- Complex skill implementations

**Run:**
```bash
# Set API keys first
export OPENAI_API_KEY=sk-...
export ANTHROPIC_API_KEY=sk-ant-...
export GROK_API_KEY=xai-...

poetry run python examples/advanced_tree.py
```

**Use case:** Production-ready multi-agent system with real API integrations.

---

### 3. Server Example (`server_example.py`)

**What it demonstrates:**
- FastAPI server setup
- OpenAI-compatible API endpoints
- Loading tree from JSON configuration
- RESTful API design

**Run:**
```bash
poetry run python examples/server_example.py
```

**Endpoints:**
- `http://localhost:8000/v1/chat/completions` - Chat endpoint
- `http://localhost:8000/tree/info` - Tree metadata
- `http://localhost:8000/tree/visualize` - ASCII visualization
- `http://localhost:8000/health` - Health check

**Use case:** Deploying OpenAspen as a web service.

---

### 4. Tree Configuration (`tree.json`)

**What it demonstrates:**
- JSON-based tree configuration
- Branch definitions with system prompts
- LLM provider configuration
- Declarative tree structure

**Use with CLI:**
```bash
openaspen run examples/tree.json --query "Your query here"
openaspen visualize examples/tree.json
openaspen info examples/tree.json
```

**Use case:** Configuration-driven tree deployment, version control.

---

## Common Patterns

### Pattern: Local + Cloud LLMs

```python
llm_configs = {
    "openai": create_llm_config(provider="openai", api_key="..."),
    "ollama": create_llm_config(provider="ollama"),  # Free!
}

# Use expensive cloud LLM for complex tasks
important = tree.grow_branch("critical", llm_provider="openai")

# Use free local LLM for simple tasks
simple = tree.grow_branch("basic", llm_provider="ollama")
```

### Pattern: Async Skills

```python
async def fetch_data(url: str) -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            return await resp.json()

await tree.spawn_leaf(branch, "fetch", fetch_data)
```

### Pattern: Error Handling

```python
async def safe_api_call(endpoint: str) -> dict:
    try:
        # API call
        return {"success": True, "data": result}
    except Exception as e:
        return {"success": False, "error": str(e)}

# Leaf automatically wraps in try/except too
await tree.spawn_leaf(branch, "api_call", safe_api_call)
```

### Pattern: Cross-Agent Context

```python
# After indexing, agents can access each other's skills
await tree.index_tree()

# Query automatically finds best branch AND best leaf
result = await tree.execute("Complex query needing multiple skills")
```

## Creating Your Own Examples

1. Copy `basic_tree.py` as a template
2. Define your skills as async/sync functions
3. Configure your LLM providers
4. Create tree and add branches
5. Spawn leaves (skills) on branches
6. Index and execute

## Tips

- **Start simple**: Begin with `basic_tree.py` pattern
- **Use local LLMs**: Ollama is free and fast for development
- **Test skills separately**: Test functions before adding to tree
- **Check logs**: Set `LOG_LEVEL=DEBUG` for detailed output
- **Use .env files**: Keep API keys in `.env`, not code

## Next Steps

- Read [QUICKSTART.md](../docs/QUICKSTART.md) for detailed tutorials
- Check [ARCHITECTURE.md](../docs/ARCHITECTURE.md) for design patterns
- Explore the test suite in `tests/` for more examples
- Build your own tree for your specific use case!

## Need Help?

- GitHub Issues: Report bugs or ask questions
- GitHub Discussions: Share your trees and get help
- Documentation: Check the main README.md

Happy tree growing! 🌲
