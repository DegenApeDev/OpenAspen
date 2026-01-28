# 🌲 OpenAspen - Permanent Setup for New Users

**The definitive setup guide - build in the right way from the start**

## Philosophy: Zero API Keys Required

OpenAspen is built to work **completely free** with **no API keys required**:

1. **LM Studio** (Default) - FREE local LLM on your machine
2. **Grok** (Primary Cloud) - Fast, affordable when you need cloud
3. **OpenAI/Anthropic** (Optional) - Premium options if you want them

## One-Command Setup (Fish Shell)

```fish
# Clone, setup venv, install core + hub tools
cd /path/to/OpenAspen
python3 -m venv venv
source venv/bin/activate.fish
pip install -e . --no-deps
pip install langchain langgraph langchain-community faiss-cpu \
    pydantic pydantic-settings fastapi uvicorn[standard] \
    click python-dotenv aiohttp psutil flask flask-socketio \
    duckduckgo-search wikipedia

# Test it works
python examples/minimal_hub_example.py
```

## LM Studio Setup (5 Minutes)

### 1. Install LM Studio
```bash
# Download from: https://lmstudio.ai/
# Install and launch the application
```

### 2. Download a Model
In LM Studio:
- Click "Search" tab
- Search for: `mistral-7b-instruct` or `llama-3.2`
- Download a Q4_K_M quantized version (good balance)

### 3. Start the Server
- Click "Local Server" tab
- Select your downloaded model
- Click "Start Server"
- Verify: `Server running on http://localhost:1234`

### 4. Test with OpenAspen
```fish
source venv/bin/activate.fish
python examples/lmstudio_quickstart.py
```

**That's it! You now have a fully functional AI agent tree with ZERO API costs.**

## Optional: Add Grok (Primary Cloud Option)

If you need cloud inference (faster, no local GPU needed):

### 1. Get Grok API Key
- Sign up at: https://x.ai/
- Get your API key from the dashboard

### 2. Add to .env
```bash
cat >> .env << 'EOF'
# Grok (primary cloud option)
GROK_API_KEY=xai-your-key-here
GROK_API_BASE=https://api.x.ai/v1
EOF
```

### 3. Install Grok Dependencies
```fish
source venv/bin/activate.fish
pip install openai langchain-openai tiktoken
```

### 4. Use in Code
```python
from openaspen.llm.providers import create_llm_config

llm_configs = {
    "lmstudio": create_llm_config(
        provider="ollama",
        api_base="http://localhost:1234/v1",
        api_key="not-needed",
    ),
    "grok": create_llm_config(
        provider="openai",  # Grok uses OpenAI-compatible API
        model="grok-beta",
        api_key=os.getenv("GROK_API_KEY"),
        api_base=os.getenv("GROK_API_BASE"),
    ),
}
```

## Optional: Add OpenAI/Anthropic

Only if you want premium cloud LLMs:

```fish
# Install dependencies
pip install openai langchain-openai anthropic langchain-anthropic tiktoken

# Add to .env
cat >> .env << 'EOF'
OPENAI_API_KEY=sk-your-key-here
ANTHROPIC_API_KEY=sk-ant-your-key-here
EOF
```

## Permanent Workflow

### Daily Development
```fish
# Always activate venv first
source venv/bin/activate.fish

# Start LM Studio server (if not running)
# Then run your code
python your_script.py
```

### Add Shell Aliases (Optional)
Add to `~/.config/fish/config.fish`:

```fish
# OpenAspen shortcuts
alias oa='cd ~/path/to/OpenAspen && source venv/bin/activate.fish'
alias oa-test='oa && python examples/minimal_hub_example.py'
alias oa-lm='oa && python examples/lmstudio_quickstart.py'
alias oa-tools='oa && python -c "from openaspen.integrations.langchain_hub import LangChainHubLoader; print(\"\n\".join(LangChainHubLoader.list_available_tools()))"'
```

Then use:
```fish
oa          # Go to OpenAspen and activate venv
oa-test     # Run minimal example
oa-lm       # Run LM Studio example
oa-tools    # List available hub tools
```

## Project Structure

```
OpenAspen/
├── venv/                    # Virtual environment (always activate!)
├── .env                     # API keys (optional - not needed for LM Studio)
├── examples/
│   ├── minimal_hub_example.py      # No API keys needed
│   ├── lmstudio_quickstart.py      # LM Studio example
│   └── degen_quickstart.py         # Full example (needs API keys)
├── docs/
│   ├── LMSTUDIO_SETUP.md           # Detailed LM Studio guide
│   ├── QUICKSTART_LANGCHAIN_HUB.md # Hub tools quickstart
│   └── LANGCHAIN_HUB_INTEGRATION.md # Full hub integration docs
└── NEW_USER_SETUP.md        # Detailed setup guide
```

## Verification Checklist

- [ ] Virtual environment created and activated
- [ ] Core dependencies installed
- [ ] LangChain Hub tools installed (duckduckgo-search, wikipedia)
- [ ] `python examples/minimal_hub_example.py` works
- [ ] LM Studio installed and server running
- [ ] `python examples/lmstudio_quickstart.py` works
- [ ] (Optional) Grok API key added to .env
- [ ] (Optional) OpenAI/Anthropic API keys added to .env

## Troubleshooting

### Import Error: No module named 'openaspen'
```fish
# Make sure venv is activated
source venv/bin/activate.fish

# Reinstall in editable mode
pip install -e . --no-deps
```

### Import Error: No module named 'telegram'
**Fixed!** Telegram is now optional. This error should not occur.

### LM Studio Connection Refused
```bash
# Check if server is running
curl http://localhost:1234/v1/models

# If not, start it in LM Studio:
# 1. Open LM Studio
# 2. Go to "Local Server" tab
# 3. Load a model
# 4. Click "Start Server"
```

### ChromaDB Installation Fails (Python 3.14)
**Expected!** ChromaDB has issues on Python 3.14. We use FAISS instead (already installed).

## Cost Comparison

| Setup | Monthly Cost | Speed | Quality |
|-------|-------------|-------|---------|
| **LM Studio Only** | $0 | Fast (with GPU) | Good |
| **LM Studio + Grok** | ~$5-20 | Very Fast | Excellent |
| **LM Studio + OpenAI** | ~$20-100 | Very Fast | Excellent |
| **All Cloud (OpenAI/Anthropic)** | ~$50-500 | Very Fast | Excellent |

**Recommendation**: Start with LM Studio (free), add Grok when you need cloud speed.

## Next Steps

1. ✅ **Setup complete** - You can build AI agents with ZERO API costs!

2. **Learn the basics**:
   ```fish
   python examples/minimal_hub_example.py  # Hub tools
   python examples/lmstudio_quickstart.py  # LM Studio
   ```

3. **Read documentation**:
   - `docs/LMSTUDIO_SETUP.md` - LM Studio details
   - `docs/QUICKSTART_LANGCHAIN_HUB.md` - Hub tools quickstart
   - `docs/LANGCHAIN_HUB_INTEGRATION.md` - Full integration guide

4. **Build your first tree**:
   - Use LM Studio for free local inference
   - Add LangChain Hub tools (no coding needed)
   - Add custom leaves for your specific use case
   - Deploy with `openaspen server`

## Support

- **Documentation**: `docs/` directory
- **Examples**: `examples/` directory
- **LM Studio Help**: https://lmstudio.ai/docs
- **GitHub Issues**: Report bugs and request features

---

**Happy building with FREE local AI! 🌲**

*No API keys. No costs. Just powerful AI agent trees.*
