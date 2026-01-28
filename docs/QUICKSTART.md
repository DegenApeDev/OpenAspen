# OpenAspen Quick Start Guide

## Installation

### Prerequisites

- Python 3.11 or higher
- pip or Poetry package manager
- (Optional) Ollama for local LLMs

### Install with Poetry (Recommended)

```bash
# Install Poetry if you haven't
curl -sSL https://install.python-poetry.org | python3 -

# Install OpenAspen
poetry add openaspen

# Or clone and install from source
git clone https://github.com/yourusername/openaspen.git
cd openaspen
poetry install
```

### Install with pip

```bash
pip install openaspen
```

## 5-Minute Tutorial

### Step 1: Set Up API Keys

Create a `.env` file:

```bash
OPENAI_API_KEY=sk-your-openai-key-here
```

Or export in your shell:

```bash
export OPENAI_API_KEY=sk-your-openai-key-here
```

### Step 2: Create Your First Tree

Create `my_first_tree.py`:

```python
import asyncio
from openaspen import OpenAspenTree
from openaspen.llm.providers import create_llm_config
import os

# Define a simple skill
async def get_weather(location: str) -> dict:
    """Get weather for a location"""
    # In real app, call weather API
    return {
        "location": location,
        "temperature": 72,
        "condition": "sunny"
    }

async def main():
    # 1. Configure LLM
    llm_configs = {
        "openai": create_llm_config(
            provider="openai",
            api_key=os.getenv("OPENAI_API_KEY")
        )
    }
    
    # 2. Create tree
    tree = OpenAspenTree(llm_configs=llm_configs, name="WeatherTree")
    
    # 3. Add a branch (agent)
    weather_branch = tree.grow_branch(
        "weather_assistant",
        description="Provides weather information",
        llm_provider="openai"
    )
    
    # 4. Add a leaf (skill)
    await tree.spawn_leaf(
        weather_branch,
        "get_weather",
        get_weather,
        "Get current weather for any location"
    )
    
    # 5. Index the tree for RAG
    await tree.index_tree()
    
    # 6. Visualize
    print(tree.visualize())
    
    # 7. Execute a query
    result = await tree.execute("What's the weather in San Francisco?")
    print("\nResult:", result)

if __name__ == "__main__":
    asyncio.run(main())
```

Run it:

```bash
python my_first_tree.py
```

### Step 3: Use the CLI

Initialize a tree config:

```bash
openaspen init --name my_tree --output tree.json
```

Edit `tree.json` to customize, then run:

```bash
openaspen run tree.json --query "Hello, world!"
```

Or use interactive mode:

```bash
openaspen run tree.json --interactive
```

## Common Patterns

### Pattern 1: Multiple Agents

```python
# Create specialized agents
crypto_agent = tree.grow_branch("crypto_analyzer", llm_provider="openai")
research_agent = tree.grow_branch("research_assistant", llm_provider="anthropic")
code_agent = tree.grow_branch("code_helper", llm_provider="openai")

# Add skills to each
await tree.spawn_leaf(crypto_agent, "get_price", fetch_price_func)
await tree.spawn_leaf(research_agent, "web_search", search_func)
await tree.spawn_leaf(code_agent, "analyze_code", analyze_func)

# Tree automatically routes queries to the right agent
await tree.execute("What's Bitcoin's price?")  # → crypto_analyzer
await tree.execute("Search for AI news")       # → research_assistant
await tree.execute("Review this Python code")  # → code_helper
```

### Pattern 2: Local + Cloud LLMs

```python
llm_configs = {
    "openai": create_llm_config(provider="openai", api_key="..."),
    "ollama": create_llm_config(provider="ollama"),  # Free local
}

# Use expensive LLM for critical tasks
important_agent = tree.grow_branch("critical_tasks", llm_provider="openai")

# Use free local LLM for simple tasks
simple_agent = tree.grow_branch("simple_tasks", llm_provider="ollama")
```

### Pattern 3: Async Skills

```python
import aiohttp

async def fetch_api_data(endpoint: str) -> dict:
    """Async API call"""
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://api.example.com/{endpoint}") as resp:
            return await resp.json()

# OpenAspen automatically detects and handles async functions
await tree.spawn_leaf(branch, "api_fetch", fetch_api_data)
```

### Pattern 4: Sync Skills

```python
def calculate_fibonacci(n: int) -> int:
    """Synchronous computation"""
    if n <= 1:
        return n
    return calculate_fibonacci(n-1) + calculate_fibonacci(n-2)

# Sync functions work too - wrapped in asyncio.to_thread()
await tree.spawn_leaf(branch, "fibonacci", calculate_fibonacci)
```

## Using the API Server

### Start the Server

```python
# server.py
from openaspen.server.api import create_app
import uvicorn

app = create_app(config_file="tree.json")
uvicorn.run(app, host="0.0.0.0", port=8000)
```

Run:

```bash
python server.py
```

### Call from Any Language

**Python:**

```python
import openai

client = openai.OpenAI(
    base_url="http://localhost:8000/v1",
    api_key="not-needed"
)

response = client.chat.completions.create(
    model="openaspen",
    messages=[{"role": "user", "content": "Hello!"}]
)
print(response.choices[0].message.content)
```

**cURL:**

```bash
curl -X POST http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "openaspen",
    "messages": [{"role": "user", "content": "What is 2+2?"}]
  }'
```

**JavaScript:**

```javascript
const response = await fetch('http://localhost:8000/v1/chat/completions', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    model: 'openaspen',
    messages: [{ role: 'user', content: 'Hello!' }]
  })
});
const data = await response.json();
console.log(data.choices[0].message.content);
```

## Configuration Tips

### Environment Variables

```bash
# .env file
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
GROK_API_KEY=xai-...

# ChromaDB settings
CHROMA_DB_PATH=./my_chroma_db

# Server settings
OPENASPEN_HOST=0.0.0.0
OPENASPEN_PORT=8000
```

### Tree Configuration JSON

```json
{
  "name": "MyProductionTree",
  "branches": [
    {
      "name": "customer_support",
      "description": "Handle customer inquiries",
      "llm_provider": "openai",
      "system_prompt": "You are a helpful customer support agent."
    },
    {
      "name": "data_analysis",
      "description": "Analyze data and generate insights",
      "llm_provider": "anthropic",
      "system_prompt": "You are a data analyst."
    }
  ],
  "llm_providers": {
    "openai": {
      "provider": "openai",
      "model": "gpt-4-turbo-preview",
      "temperature": 0.7,
      "max_tokens": 2000
    },
    "anthropic": {
      "provider": "anthropic",
      "model": "claude-3-opus-20240229",
      "temperature": 0.7
    }
  }
}
```

## Troubleshooting

### Issue: "No LLM providers configured"

**Solution**: Make sure you've created `llm_configs` and passed them to `OpenAspenTree`:

```python
llm_configs = {
    "openai": create_llm_config(provider="openai", api_key="...")
}
tree = OpenAspenTree(llm_configs=llm_configs)
```

### Issue: "API key not found"

**Solution**: Set environment variables or pass API keys explicitly:

```python
create_llm_config(provider="openai", api_key="sk-...")
```

### Issue: ChromaDB errors

**Solution**: Install ChromaDB dependencies:

```bash
pip install chromadb
```

Or use a different persist directory:

```python
from openaspen.rag.store import GroupRAGStore

rag_store = GroupRAGStore(persist_directory="./my_custom_db")
tree = OpenAspenTree(llm_configs=llm_configs, shared_rag_db=rag_store)
```

### Issue: Ollama connection failed

**Solution**: Make sure Ollama is running:

```bash
# Install Ollama from https://ollama.ai
ollama serve

# Pull a model
ollama pull llama2
```

## Next Steps

1. **Read the Architecture docs**: Understand how OpenAspen works internally
2. **Explore examples/**: See advanced use cases
3. **Run tests**: `poetry run pytest` to see how components work
4. **Build your own tree**: Start with your specific use case
5. **Join the community**: Contribute, ask questions, share your trees

## Resources

- [Full Documentation](../README.md)
- [Architecture Guide](ARCHITECTURE.md)
- [API Reference](API_REFERENCE.md)
- [Examples](../examples/)
- [GitHub Issues](https://github.com/yourusername/openaspen/issues)

Happy tree growing! 🌲
