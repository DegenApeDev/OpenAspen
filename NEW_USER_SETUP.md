# 🌲 OpenAspen - New User Setup Guide

**Complete setup guide for getting OpenAspen running with LangChain Hub integration**

## LLM Priority (No API Keys Required!)

OpenAspen is designed to work **without requiring any API keys**:

1. **LM Studio** (Minimum/Default) - FREE local LLM, no API keys
2. **Grok** (Primary Cloud Option) - Fast, affordable cloud LLM
3. **OpenAI/Anthropic** (Optional) - Premium cloud LLMs

## Quick Start (2 Minutes - Zero API Keys)

```bash
# 1. Clone and enter directory
cd /path/to/OpenAspen

# 2. Create virtual environment
python3 -m venv venv

# 3. Activate venv (Fish shell)
source venv/bin/activate.fish

# For Bash/Zsh:
# source venv/bin/activate

# 4. Install OpenAspen core (no LLM dependencies)
pip install -e . --no-deps

# 5. Install LangChain Hub tools (no API keys needed)
pip install duckduckgo-search wikipedia

# 6. Test it works!
python examples/minimal_hub_example.py

# 7. (Optional) Install LM Studio for free local LLM
# Download from: https://lmstudio.ai/
python examples/lmstudio_quickstart.py
```

## Detailed Setup

### Prerequisites

- **Python 3.11+** (Python 3.14 supported)
- **Virtual environment** (venv recommended)
- **Git** (for cloning)

### Step 1: Environment Setup

```bash
# Create virtual environment
python3 -m venv venv

# Activate (choose your shell)
source venv/bin/activate.fish  # Fish
source venv/bin/activate        # Bash/Zsh
venv\Scripts\activate           # Windows
```

### Step 2: Install OpenAspen

```bash
# Install in editable mode (for development)
pip install -e . --no-deps

# This installs OpenAspen without pulling in all dependencies
# We'll add them selectively based on what you need
```

### Step 3: Install Dependencies

Choose your installation profile:

#### Profile 1: LM Studio + Hub Tools (Recommended - Zero API Keys!)
```bash
# Install core + hub tools
pip install langchain langgraph langchain-community faiss-cpu \
    pydantic pydantic-settings fastapi uvicorn[standard] \
    click python-dotenv aiohttp psutil flask flask-socketio

# Install LangChain Hub tools (no API keys)
pip install duckduckgo-search wikipedia

# Install LM Studio from: https://lmstudio.ai/
# Then run: python examples/lmstudio_quickstart.py
```

#### Profile 2: Grok (Primary Cloud Option)
```bash
# Install Profile 1 first, then add Grok support
pip install openai langchain-openai tiktoken

# Add to .env:
# GROK_API_KEY=xai-your-key-here
# GROK_API_BASE=https://api.x.ai/v1
```

#### Profile 3: OpenAI/Anthropic (Optional Premium)
```bash
# Install Profile 1 first, then add cloud LLMs
pip install openai langchain-openai anthropic langchain-anthropic tiktoken

# Add to .env:
# OPENAI_API_KEY=sk-your-key-here
# ANTHROPIC_API_KEY=sk-ant-your-key-here
```

#### Profile 4: Everything
```bash
# All dependencies including optional ones
pip install -e .[all]

# Note: ChromaDB has issues on Python 3.14, using FAISS instead
```

### Step 4: Configure API Keys (Optional - Not Required for LM Studio!)

**Default: LM Studio requires NO API keys!**

Only add these if you want cloud LLM options:

```bash
# Create .env file
cat > .env << 'EOF'
# LM Studio (default - no API key needed!)
LMSTUDIO_API_BASE=http://localhost:1234/v1

# Grok (primary cloud option - fast & affordable)
GROK_API_KEY=xai-your-key-here
GROK_API_BASE=https://api.x.ai/v1

# OpenAI (optional premium)
OPENAI_API_KEY=sk-your-key-here

# Anthropic (optional premium)
ANTHROPIC_API_KEY=sk-ant-your-key-here

# Tavily (optional for advanced web search)
TAVILY_API_KEY=your-tavily-key-here

# Ollama (alternative local LLM)
OLLAMA_API_BASE=http://localhost:11434
EOF

# Edit and add your actual keys (if using cloud LLMs)
nano .env
```

### Step 5: Verify Installation

```bash
# Test import
python -c "from openaspen.integrations.langchain_hub import LangChainHubLoader; print('✅ Import successful!')"

# Run minimal example (no API keys needed)
python examples/minimal_hub_example.py

# List available hub tools
python -c "from openaspen.integrations.langchain_hub import LangChainHubLoader; print('\n'.join(LangChainHubLoader.list_available_tools()))"
```

## Usage Examples

### Example 1: List Available Tools (No API Keys)

```python
from openaspen.integrations.langchain_hub import LangChainHubLoader

# List all available tools
tools = LangChainHubLoader.list_available_tools()
for tool in tools:
    info = LangChainHubLoader.get_tool_info(tool)
    print(f"{tool}: {info['description']}")
```

### Example 2: Use DuckDuckGo Search (No API Keys)

```python
from openaspen.integrations.langchain_hub import LangChainHubLoader

# Load and use DuckDuckGo search
tool = LangChainHubLoader.load_tool("duckduckgo_search")
result = tool.run("Python programming")
print(result)
```

### Example 3: Create a Leaf (No API Keys)

```python
import asyncio
from openaspen.integrations.langchain_hub import LangChainHubLoader

async def main():
    # Create a leaf from Wikipedia
    leaf = LangChainHubLoader.create_leaf_from_hub(
        tool_name="wikipedia",
        leaf_name="wiki_search"
    )
    
    # Use the leaf
    result = await leaf.execute("Python (programming language)")
    print(result)

asyncio.run(main())
```

### Example 4: Full Tree with LLM (Requires API Keys)

```python
import asyncio
from openaspen import OpenAspenTree
from openaspen.llm.providers import create_llm_config
from openaspen.integrations.langchain_hub import LangChainHubLoader

async def main():
    # Requires OPENAI_API_KEY in .env
    llm_configs = {
        "openai": create_llm_config(provider="openai")
    }
    
    tree = OpenAspenTree(name="my_tree", llm_configs=llm_configs)
    branch = tree.add_branch("research", llm_provider="openai")
    
    # Add hub tool
    await LangChainHubLoader.add_hub_tool_to_branch(
        branch, "duckduckgo_search", "web_search", rag_db=tree.shared_rag_db
    )
    
    # Query the tree
    result = await tree.execute("What is Python?")
    print(result)

asyncio.run(main())
```

## Common Issues & Solutions

### Issue: `ModuleNotFoundError: No module named 'telegram'`

**Solution**: This is fixed! The telegram integration is now optional.

```python
# This now works without telegram installed:
from openaspen.integrations.langchain_hub import LangChainHubLoader
```

### Issue: `ChromaDB onnxruntime dependency conflict`

**Solution**: ChromaDB has issues on Python 3.14. Use FAISS instead or Python 3.11-3.12.

```bash
# ChromaDB is now optional
pip install -e . --no-deps  # Skip ChromaDB
```

### Issue: `OpenAI API key not found`

**Solution**: Either:
1. Add `OPENAI_API_KEY` to `.env` file
2. Use examples that don't require API keys:
   ```bash
   python examples/minimal_hub_example.py
   ```

### Issue: `Tool dependencies not installed`

**Solution**: Install the specific tool dependencies:

```bash
# For DuckDuckGo
pip install duckduckgo-search

# For Wikipedia
pip install wikipedia

# For Tavily (requires API key)
pip install tavily-python

# For Python REPL
pip install langchain-experimental
```

## Shell-Specific Activation

### Fish Shell
```fish
source venv/bin/activate.fish
```

### Bash/Zsh
```bash
source venv/bin/activate
```

### Windows PowerShell
```powershell
venv\Scripts\Activate.ps1
```

### Windows CMD
```cmd
venv\Scripts\activate.bat
```

## Permanent Aliases (Optional)

Add to your shell config for convenience:

### Fish (~/.config/fish/config.fish)
```fish
# OpenAspen shortcuts
alias oa-activate='source ~/path/to/OpenAspen/venv/bin/activate.fish'
alias oa-test='oa-activate && python examples/minimal_hub_example.py'
alias oa-tools='oa-activate && python -c "from openaspen.integrations.langchain_hub import LangChainHubLoader; print(\"\n\".join(LangChainHubLoader.list_available_tools()))"'
```

### Bash/Zsh (~/.bashrc or ~/.zshrc)
```bash
# OpenAspen shortcuts
alias oa-activate='source ~/path/to/OpenAspen/venv/bin/activate'
alias oa-test='oa-activate && python examples/minimal_hub_example.py'
alias oa-tools='oa-activate && python -c "from openaspen.integrations.langchain_hub import LangChainHubLoader; print(\"\n\".join(LangChainHubLoader.list_available_tools()))"'
```

## Next Steps

1. ✅ **Setup complete** - You can now use OpenAspen!

2. **Try examples**:
   ```bash
   # No API keys needed
   python examples/minimal_hub_example.py
   
   # Requires API keys
   python examples/degen_quickstart.py
   python examples/langchain_hub_example.py
   ```

3. **Read documentation**:
   - `docs/QUICKSTART_LANGCHAIN_HUB.md` - 2-minute quickstart
   - `docs/LANGCHAIN_HUB_INTEGRATION.md` - Full integration guide
   - `README.md` - Main documentation

4. **Build your first tree**:
   - Start with hub tools (no coding)
   - Add custom leaves for specialized logic
   - Deploy with `openaspen server`

## Support

- **Documentation**: `docs/` directory
- **Examples**: `examples/` directory
- **Tests**: `pytest tests/test_langchain_hub.py`
- **Issues**: GitHub Issues

---

**Happy building! 🌲**

*Skip building basics—import hub tools, test, focus on custom skills!*
