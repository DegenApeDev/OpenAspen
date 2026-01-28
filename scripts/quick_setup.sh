#!/bin/bash
# OpenAspen Quick Setup Script
# One-command setup for new users

set -e

echo "🌲 OpenAspen Quick Setup"
echo "========================"
echo ""

# Check Python version
echo "Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
required_version="3.11"

if ! python3 -c "import sys; exit(0 if sys.version_info >= (3, 11) else 1)"; then
    echo "❌ Python 3.11+ required, found $python_version"
    exit 1
fi
echo "✅ Python $python_version"

# Create venv if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists"
fi

# Detect shell and provide activation command
if [ -n "$FISH_VERSION" ]; then
    ACTIVATE_CMD="source venv/bin/activate.fish"
elif [ -n "$ZSH_VERSION" ]; then
    ACTIVATE_CMD="source venv/bin/activate"
elif [ -n "$BASH_VERSION" ]; then
    ACTIVATE_CMD="source venv/bin/activate"
else
    ACTIVATE_CMD="source venv/bin/activate"
fi

echo "📦 Installing dependencies in venv..."
$ACTIVATE_CMD && pip install -e . --no-deps
$ACTIVATE_CMD && pip install duckduckgo-search wikipedia

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file..."
    cat > .env << 'EOF'
# OpenAspen Environment Variables

# OpenAI API Key (required for most examples)
OPENAI_API_KEY=your_openai_api_key_here

# Anthropic API Key (optional)
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# Tavily Search API Key (optional)
TAVILY_API_KEY=your_tavily_api_key_here

# Ollama API Base (optional, for local LLMs)
OLLAMA_API_BASE=http://localhost:11434
EOF
    echo "✅ Created .env file"
    echo "⚠️  IMPORTANT: Edit .env and add your API keys!"
else
    echo "✅ .env file already exists"
fi

# Create example tree config
if [ ! -f my_tree.json ]; then
    echo "📝 Creating example tree..."
    cat > my_tree.json << 'EOF'
{
  "name": "my_first_tree",
  "branches": [
    {
      "name": "general_assistant",
      "description": "General purpose assistant for various tasks",
      "llm_provider": "openai",
      "system_prompt": "You are a helpful AI assistant."
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
EOF
    echo "✅ Created my_tree.json"
else
    echo "✅ my_tree.json already exists"
fi

echo ""
echo "🎉 Setup Complete!"
echo ""
echo "Next Steps:"
echo "  1. Edit .env and add your API keys"
echo "  2. Try: poetry run python examples/degen_quickstart.py"
echo "  3. Or:  poetry run openaspen grow_leaf --list-tools"
echo ""
echo "Documentation:"
echo "  - docs/QUICKSTART_LANGCHAIN_HUB.md"
echo "  - docs/LANGCHAIN_HUB_INTEGRATION.md"
echo ""
echo "Happy building! 🌲"
