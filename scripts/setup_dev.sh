#!/bin/bash
# Development environment setup script for OpenAspen

set -e

echo "🌲 Setting up OpenAspen development environment..."

# Check Python version
echo "Checking Python version..."
python_version=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
required_version="3.11"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "❌ Python 3.11+ required. Found: $python_version"
    exit 1
fi
echo "✅ Python version OK: $python_version"

# Install Poetry if not present
if ! command -v poetry &> /dev/null; then
    echo "Installing Poetry..."
    curl -sSL https://install.python-poetry.org | python3 -
    echo "✅ Poetry installed"
else
    echo "✅ Poetry already installed"
fi

# Install dependencies
echo "Installing dependencies..."
poetry install
echo "✅ Dependencies installed"

# Install pre-commit hooks
echo "Installing pre-commit hooks..."
poetry run pre-commit install
echo "✅ Pre-commit hooks installed"

# Create .env from example if not exists
if [ ! -f .env ]; then
    echo "Creating .env file from example..."
    cp .env.example .env
    echo "✅ .env file created - please add your API keys"
else
    echo "✅ .env file already exists"
fi

# Run tests to verify setup
echo "Running tests to verify setup..."
poetry run pytest tests/ -v
echo "✅ Tests passed"

echo ""
echo "🎉 Development environment setup complete!"
echo ""
echo "Next steps:"
echo "1. Add your API keys to .env file"
echo "2. Run examples: poetry run python examples/basic_tree.py"
echo "3. Start coding: poetry run python your_script.py"
echo "4. Run tests: poetry run pytest"
echo ""
echo "Happy tree growing! 🌲"
