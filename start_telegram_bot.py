#!/usr/bin/env python3
"""
OpenAspen Telegram Bot - Control your AI agent tree via Telegram
Zero API keys required with LM Studio

Setup:
1. Create a Telegram bot with @BotFather
2. Add TELEGRAM_BOT_TOKEN to .env
3. Run: python start_telegram_bot.py

Usage:
- Send messages to your bot naturally
- Use /tree to see your agent structure
- Use /help for commands
"""

import asyncio
import os
from dotenv import load_dotenv
import logging

from openaspen import OpenAspenTree
from openaspen.llm.providers import create_llm_config
from openaspen.integrations.gateway import MessageGateway

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()


async def create_tree():
    """Create OpenAspen tree with LM Studio"""
    
    llm_configs = {
        "lmstudio": create_llm_config(
            provider="ollama",
            api_base="http://localhost:1234/v1",
            api_key="not-needed",
        ),
    }
    
    # Add optional cloud LLMs if API keys present
    grok_key = os.getenv("GROK_API_KEY")
    if grok_key:
        llm_configs["grok"] = create_llm_config(
            provider="openai",
            model="grok-beta",
            api_key=grok_key,
            api_base="https://api.x.ai/v1",
        )
        logger.info("✅ Grok enabled")
    
    openai_key = os.getenv("OPENAI_API_KEY")
    if openai_key:
        llm_configs["openai"] = create_llm_config(
            provider="openai",
            model="gpt-4-turbo-preview",
            api_key=openai_key,
        )
        logger.info("✅ OpenAI enabled")
    
    # Create tree
    tree = OpenAspenTree(
        name="telegram_tree",
        llm_configs=llm_configs,
        use_embeddings=True,
    )
    
    logger.info(f"🌲 Created tree with providers: {list(llm_configs.keys())}")
    
    # Add branches and tools
    research = tree.add_branch(
        "research",
        description="Research and information gathering",
        llm_provider="lmstudio",
        system_prompt="You are a helpful research assistant. Provide concise, accurate information.",
    )
    
    # Web search tool
    async def web_search(query: str, **kwargs):
        """Search the web using DuckDuckGo"""
        try:
            from duckduckgo_search import DDGS
            results = list(DDGS().text(query, max_results=3))
            if results:
                summary = "\n\n".join([
                    f"**{r.get('title', 'Result')}**\n{r.get('body', '')[:200]}..."
                    for r in results[:3]
                ])
                return f"🔍 Search results for '{query}':\n\n{summary}"
            return f"No results found for '{query}'"
        except Exception as e:
            return f"❌ Search error: {str(e)}"
    
    await tree.spawn_leaf(research, "web_search", web_search, "Search the web for information")
    logger.info("  ✅ Added web_search")
    
    # Wikipedia tool
    async def wiki_search(query: str, **kwargs):
        """Search Wikipedia"""
        try:
            import wikipedia
            summary = wikipedia.summary(query, sentences=3)
            return f"📚 Wikipedia: {query}\n\n{summary}"
        except Exception as e:
            return f"❌ Wikipedia error: {str(e)}"
    
    await tree.spawn_leaf(research, "wiki_search", wiki_search, "Search Wikipedia")
    logger.info("  ✅ Added wiki_search")
    
    # Utility branch
    utils = tree.add_branch(
        "utils",
        description="Utility functions",
        llm_provider="lmstudio",
    )
    
    async def echo(text: str, **kwargs):
        """Echo back the input"""
        return f"🔊 Echo: {text}"
    
    await tree.spawn_leaf(utils, "echo", echo, "Echo back text")
    logger.info("  ✅ Added echo")
    
    logger.info(f"🌳 Tree setup complete with {len(tree.branches)} branches")
    
    return tree


def main():
    """Main entry point - runs synchronously"""
    
    print("=" * 60)
    print("🤖 OpenAspen Telegram Bot")
    print("=" * 60)
    print()
    
    # Check for Telegram token
    telegram_token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not telegram_token:
        print("❌ TELEGRAM_BOT_TOKEN not found in .env")
        print()
        print("Setup instructions:")
        print("1. Talk to @BotFather on Telegram")
        print("2. Create a new bot with /newbot")
        print("3. Copy the token")
        print("4. Add to .env: TELEGRAM_BOT_TOKEN=your-token-here")
        print()
        return
    
    print("✅ Telegram token found")
    
    # Check if python-telegram-bot is installed
    try:
        import telegram
        print("✅ python-telegram-bot installed")
    except ImportError:
        print("❌ python-telegram-bot not installed")
        print()
        print("Install it with:")
        print("  pip install python-telegram-bot")
        print()
        return
    
    print()
    print("🌲 Building OpenAspen tree...")
    
    # Create tree synchronously
    tree = asyncio.run(create_tree())
    
    print()
    print("🤖 Starting Telegram bot...")
    
    # Create message gateway
    gateway = MessageGateway(tree_executor=tree)
    
    # Register Telegram bot
    telegram_bot = gateway.register_telegram(telegram_token)
    
    # Initialize bot
    asyncio.run(telegram_bot.initialize())
    
    print()
    print("=" * 60)
    print("✅ Telegram Bot Running!")
    print("=" * 60)
    print()
    print("📱 Your bot is ready to receive messages")
    print("🌲 Tree structure:")
    print(tree.visualize())
    print()
    print("💬 Available commands:")
    print("  /start  - Welcome message")
    print("  /help   - Show help")
    print("  /tree   - View agent structure")
    print("  /status - Check system status")
    print()
    print("Or just send any message naturally!")
    print()
    print("Press Ctrl+C to stop")
    print("=" * 60)
    print()
    
    # Start polling - this creates its own event loop
    telegram_bot.application.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()
