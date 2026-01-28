#!/usr/bin/env python3
"""
OpenAspen Setup Script
Automated setup for new users to get started quickly
"""

import subprocess
import sys
import os
from pathlib import Path
import shutil


class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'


def print_header(text):
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'=' * 60}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{text.center(60)}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'=' * 60}{Colors.ENDC}\n")


def print_success(text):
    print(f"{Colors.OKGREEN}✅ {text}{Colors.ENDC}")


def print_info(text):
    print(f"{Colors.OKCYAN}ℹ️  {text}{Colors.ENDC}")


def print_warning(text):
    print(f"{Colors.WARNING}⚠️  {text}{Colors.ENDC}")


def print_error(text):
    print(f"{Colors.FAIL}❌ {text}{Colors.ENDC}")


def run_command(cmd, check=True, capture_output=False):
    """Run a shell command"""
    try:
        if capture_output:
            result = subprocess.run(
                cmd, shell=True, check=check, capture_output=True, text=True
            )
            return result.stdout.strip()
        else:
            subprocess.run(cmd, shell=True, check=check)
            return True
    except subprocess.CalledProcessError as e:
        if check:
            raise
        return False


def check_python_version():
    """Check if Python version is 3.11+"""
    print_info("Checking Python version...")
    version = sys.version_info
    if version.major == 3 and version.minor >= 11:
        print_success(f"Python {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print_error(f"Python 3.11+ required, found {version.major}.{version.minor}.{version.micro}")
        return False


def check_poetry():
    """Check if Poetry is installed"""
    print_info("Checking for Poetry...")
    try:
        version = run_command("poetry --version", capture_output=True)
        print_success(f"Poetry installed: {version}")
        return True
    except:
        print_warning("Poetry not found")
        return False


def install_poetry():
    """Install Poetry"""
    print_info("Installing Poetry...")
    try:
        run_command("curl -sSL https://install.python-poetry.org | python3 -")
        print_success("Poetry installed successfully")
        print_warning("You may need to restart your shell or run: source ~/.bashrc")
        return True
    except:
        print_error("Failed to install Poetry")
        print_info("Install manually: https://python-poetry.org/docs/#installation")
        return False


def install_dependencies(profile="minimal"):
    """Install project dependencies"""
    print_info(f"Installing dependencies (profile: {profile})...")
    
    profiles = {
        "minimal": [],
        "hub-tools": ["--extras", "hub-tools"],
        "full": ["--extras", "hub-tools", "--with", "dev"],
    }
    
    cmd_parts = ["poetry", "install"]
    cmd_parts.extend(profiles.get(profile, []))
    cmd = " ".join(cmd_parts)
    
    try:
        run_command(cmd)
        print_success("Dependencies installed successfully")
        return True
    except:
        print_error("Failed to install dependencies")
        return False


def create_env_file():
    """Create .env file from template"""
    print_info("Setting up environment variables...")
    
    env_path = Path(".env")
    env_example_path = Path(".env.example")
    
    if env_path.exists():
        print_warning(".env file already exists, skipping")
        return True
    
    env_template = """# OpenAspen Environment Variables

# OpenAI API Key (required for most examples)
OPENAI_API_KEY=your_openai_api_key_here

# Anthropic API Key (optional)
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# Grok API Key (optional)
GROK_API_KEY=your_grok_api_key_here

# Tavily Search API Key (optional, for advanced web search)
TAVILY_API_KEY=your_tavily_api_key_here

# Ollama API Base (optional, for local LLMs)
OLLAMA_API_BASE=http://localhost:11434
"""
    
    try:
        env_path.write_text(env_template)
        if not env_example_path.exists():
            env_example_path.write_text(env_template)
        print_success("Created .env file")
        print_warning("⚠️  IMPORTANT: Edit .env and add your API keys!")
        return True
    except Exception as e:
        print_error(f"Failed to create .env file: {e}")
        return False


def create_example_tree():
    """Create an example tree configuration"""
    print_info("Creating example tree configuration...")
    
    tree_path = Path("my_tree.json")
    
    if tree_path.exists():
        print_warning("my_tree.json already exists, skipping")
        return True
    
    tree_config = """{
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
}"""
    
    try:
        tree_path.write_text(tree_config)
        print_success("Created my_tree.json")
        return True
    except Exception as e:
        print_error(f"Failed to create tree config: {e}")
        return False


def run_tests():
    """Run the test suite"""
    print_info("Running tests...")
    try:
        run_command("poetry run pytest tests/test_langchain_hub.py -v")
        print_success("All tests passed!")
        return True
    except:
        print_warning("Some tests failed (this is OK if dependencies are missing)")
        return False


def print_next_steps():
    """Print next steps for the user"""
    print_header("🎉 Setup Complete!")
    
    print(f"{Colors.BOLD}Next Steps:{Colors.ENDC}\n")
    
    print(f"{Colors.OKCYAN}1. Add your API keys to .env:{Colors.ENDC}")
    print(f"   nano .env  # or use your favorite editor\n")
    
    print(f"{Colors.OKCYAN}2. Try the quickstart examples:{Colors.ENDC}")
    print(f"   poetry run python examples/degen_quickstart.py")
    print(f"   poetry run python examples/langchain_hub_example.py\n")
    
    print(f"{Colors.OKCYAN}3. Use the CLI:{Colors.ENDC}")
    print(f"   poetry run openaspen grow_leaf --list-tools")
    print(f"   poetry run openaspen visualize my_tree.json")
    print(f"   poetry run openaspen run my_tree.json -q 'Hello!'\n")
    
    print(f"{Colors.OKCYAN}4. Read the documentation:{Colors.ENDC}")
    print(f"   docs/QUICKSTART_LANGCHAIN_HUB.md")
    print(f"   docs/LANGCHAIN_HUB_INTEGRATION.md\n")
    
    print(f"{Colors.BOLD}Quick Commands:{Colors.ENDC}\n")
    print(f"  List hub tools:  poetry run openaspen grow_leaf --list-tools")
    print(f"  Run tests:       poetry run pytest")
    print(f"  Format code:     poetry run black .")
    print(f"  Type check:      poetry run mypy openaspen\n")
    
    print(f"{Colors.OKGREEN}Happy building! 🌲{Colors.ENDC}\n")


def main():
    """Main setup flow"""
    print_header("🌲 OpenAspen Setup")
    
    print(f"{Colors.BOLD}This script will set up OpenAspen for development.{Colors.ENDC}\n")
    
    # Check Python version
    if not check_python_version():
        print_error("Please install Python 3.11 or higher")
        sys.exit(1)
    
    # Check/install Poetry
    has_poetry = check_poetry()
    if not has_poetry:
        response = input("\nInstall Poetry automatically? [y/N]: ").strip().lower()
        if response == 'y':
            if not install_poetry():
                sys.exit(1)
        else:
            print_info("Please install Poetry manually: https://python-poetry.org/docs/#installation")
            sys.exit(1)
    
    # Ask for installation profile
    print(f"\n{Colors.BOLD}Choose installation profile:{Colors.ENDC}")
    print(f"  1. Minimal (core only)")
    print(f"  2. Hub Tools (core + LangChain Hub tools)")
    print(f"  3. Full (everything including dev tools)")
    
    profile_choice = input("\nEnter choice [1-3] (default: 2): ").strip() or "2"
    profile_map = {"1": "minimal", "2": "hub-tools", "3": "full"}
    profile = profile_map.get(profile_choice, "hub-tools")
    
    # Install dependencies
    if not install_dependencies(profile):
        sys.exit(1)
    
    # Create .env file
    create_env_file()
    
    # Create example tree
    create_example_tree()
    
    # Run tests (optional)
    if profile == "full":
        response = input("\nRun tests? [y/N]: ").strip().lower()
        if response == 'y':
            run_tests()
    
    # Print next steps
    print_next_steps()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.WARNING}Setup cancelled by user{Colors.ENDC}")
        sys.exit(1)
    except Exception as e:
        print_error(f"Setup failed: {e}")
        sys.exit(1)
