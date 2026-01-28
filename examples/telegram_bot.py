#!/usr/bin/env python3
"""
Telegram Bot Example for OpenAspen
24/7 mobile access to your agent tree via Telegram
"""
import asyncio
import os
from dotenv import load_dotenv
from openaspen import OpenAspenTree
from openaspen.llm.providers import create_llm_config
from openaspen.integrations.telegram import TelegramBot

# Load environment variables
load_dotenv()


async def main():
    print("=" * 70)
    print("  🤖 OpenAspen Telegram Bot")
    print("=" * 70)
    print()
    
    # Check for Telegram token
    telegram_token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not telegram_token:
        print("❌ Error: TELEGRAM_BOT_TOKEN not set in .env file")
        print("\n💡 Get your bot token from: @BotFather on Telegram")
        print("   1. Message @BotFather")
        print("   2. Send /newbot")
        print("   3. Follow instructions")
        print("   4. Add token to .env file")
        return
    
    print(f"✅ Telegram token found: {telegram_token[:10]}...")
    print()
    
    # Create LLM configs (using Grok as default)
    grok_key = os.getenv("GROK_API_KEY")
    llm_configs = {}
    
    if grok_key and not grok_key.startswith("xai-your"):
        llm_configs["grok"] = create_llm_config(provider="grok")
        print("✅ Grok configured as LLM provider")
    
    # Add LM Studio if available
    llm_configs["lmstudio"] = create_llm_config(
        provider="lmstudio",
        api_base="http://localhost:1234/v1"
    )
    print("✅ LM Studio configured (local)")
    print()
    
    # Set dummy OpenAI key for embeddings
    os.environ.setdefault("OPENAI_API_KEY", "sk-dummy-for-embeddings")
    
    # Create OpenAspen tree (simplified for demo)
    print("🌲 Creating OpenAspen tree...")
    try:
        tree = OpenAspenTree(
            llm_configs=llm_configs,
            name="TelegramBotTree"
        )
        print("✅ Tree created successfully")
    except Exception as e:
        print(f"⚠️  Tree creation failed (ChromaDB issue): {e}")
        print("   Running in demo mode without full tree")
        tree = None
    
    print()
    
    # Create Telegram bot
    print("🤖 Initializing Telegram bot...")
    bot = TelegramBot(telegram_token, tree_executor=tree)
    await bot.initialize()
    print("✅ Bot initialized")
    print()
    
    # Start bot in polling mode
    print("🚀 Starting bot in polling mode...")
    print("   Bot is now running! Send /start to your bot on Telegram")
    print("   Press Ctrl+C to stop")
    print()
    print("📱 Available commands:")
    print("   /start - Welcome message")
    print("   /help - Show help")
    print("   /tree - View agent structure")
    print("   /execute <task> - Run a task")
    print("   /crypto <task> - Crypto-specific task")
    print("   /social <task> - Social media task")
    print("   /content <task> - Content generation")
    print()
    print("💡 Or just send natural language:")
    print("   'Check BTC price'")
    print("   'Monitor my portfolio'")
    print("   'Find crypto influencers'")
    print()
    print("=" * 70)
    print()
    
    try:
        await bot.start_polling()
    except KeyboardInterrupt:
        print("\n\n✅ Bot stopped")


if __name__ == "__main__":
    asyncio.run(main())
