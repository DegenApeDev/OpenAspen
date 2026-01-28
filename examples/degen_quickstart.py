#!/usr/bin/env python3
"""
DEGEN Quickstart: Build a crypto intelligence tree in 2 minutes
Uses LangChain Hub tools for instant skills without coding
"""

import asyncio
from openaspen import OpenAspenTree
from openaspen.llm.providers import create_llm_config
from openaspen.integrations.langchain_hub import LangChainHubLoader


async def build_degen_tree():
    """Build a complete DEGEN crypto intelligence tree with LangChain Hub tools"""
    
    print("🌲 Building DEGEN Crypto Intelligence Tree...\n")
    
    llm_configs = {
        "openai": create_llm_config(
            provider="openai",
            model="gpt-4-turbo-preview",
        ),
    }
    
    tree = OpenAspenTree(name="degen_tree", llm_configs=llm_configs)
    
    print("📊 Adding Crypto Intelligence Branch...")
    crypto = tree.add_branch(
        "crypto_intel",
        description="Crypto market intelligence and news scanning",
        llm_provider="openai",
        system_prompt="You are a crypto market analyst. Provide concise, data-driven insights.",
    )
    
    crypto_tools = [
        ("duckduckgo_search", "market_search", "Search for crypto market trends"),
        ("yahoo_finance_news", "finance_news", "Get latest financial news"),
        ("wikipedia", "crypto_wiki", "Look up crypto concepts"),
    ]
    
    for tool_name, leaf_name, _ in crypto_tools:
        try:
            await LangChainHubLoader.add_hub_tool_to_branch(
                branch=crypto,
                tool_name=tool_name,
                leaf_name=leaf_name,
                rag_db=tree.shared_rag_db,
            )
            print(f"  ✅ Added {leaf_name}")
        except Exception as e:
            print(f"  ⚠️  Skipped {leaf_name}: {e}")
    
    print("\n📱 Adding Social Intelligence Branch...")
    social = tree.add_branch(
        "social_intel",
        description="Social media and influencer tracking",
        llm_provider="openai",
        system_prompt="You are a social media analyst. Track trends and influencer sentiment.",
    )
    
    social_tools = [
        ("reddit_search", "reddit_scan", "Scan Reddit for discussions"),
        ("youtube_search", "youtube_scan", "Find YouTube content"),
    ]
    
    for tool_name, leaf_name, _ in social_tools:
        try:
            await LangChainHubLoader.add_hub_tool_to_branch(
                branch=social,
                tool_name=tool_name,
                leaf_name=leaf_name,
                rag_db=tree.shared_rag_db,
            )
            print(f"  ✅ Added {leaf_name}")
        except Exception as e:
            print(f"  ⚠️  Skipped {leaf_name}: {e}")
    
    print("\n🔧 Adding Utility Branch...")
    utils = tree.add_branch(
        "utils",
        description="Utility tools for API calls and data processing",
        llm_provider="openai",
    )
    
    util_tools = [
        ("requests_get", "api_get", "Make HTTP GET requests"),
        ("arxiv", "research_papers", "Search scientific papers"),
    ]
    
    for tool_name, leaf_name, _ in util_tools:
        try:
            await LangChainHubLoader.add_hub_tool_to_branch(
                branch=utils,
                tool_name=tool_name,
                leaf_name=leaf_name,
                rag_db=tree.shared_rag_db,
            )
            print(f"  ✅ Added {leaf_name}")
        except Exception as e:
            print(f"  ⚠️  Skipped {leaf_name}: {e}")
    
    print("\n" + "=" * 60)
    print("🎉 DEGEN Tree Built Successfully!")
    print("=" * 60)
    print("\n📋 Tree Structure:")
    print(tree.visualize())
    
    print("\n💡 Next Steps:")
    print("  1. Test a query: await tree.execute('What is Bitcoin?')")
    print("  2. Add custom leaves for CoinGecko, DEX APIs, etc.")
    print("  3. Deploy with: openaspen server")
    print("  4. Integrate with Telegram/WhatsApp")
    
    return tree


async def demo_query(tree):
    """Demo: Run a sample query through the tree"""
    
    print("\n" + "=" * 60)
    print("🔍 Running Demo Query...")
    print("=" * 60)
    
    query = "What are the latest trends in cryptocurrency?"
    print(f"\nQuery: {query}\n")
    
    result = await tree.execute(query)
    
    print("Result:")
    print(result)


async def add_custom_degen_leaf(tree):
    """Demo: Add a custom CoinGecko price checker leaf"""
    
    print("\n" + "=" * 60)
    print("🪙 Adding Custom CoinGecko Leaf...")
    print("=" * 60)
    
    async def coingecko_price(symbol: str, **kwargs) -> dict:
        """Get crypto price from CoinGecko API"""
        import aiohttp
        
        symbol = symbol.lower().strip()
        url = f"https://api.coingecko.com/api/v3/simple/price"
        params = {
            "ids": symbol,
            "vs_currencies": "usd",
            "include_24hr_change": "true",
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        return {
                            "symbol": symbol,
                            "price_usd": data.get(symbol, {}).get("usd"),
                            "change_24h": data.get(symbol, {}).get("usd_24h_change"),
                        }
                    else:
                        return {"error": f"API returned status {resp.status}"}
        except Exception as e:
            return {"error": str(e)}
    
    crypto_branch = None
    for child in tree.children:
        if child.name == "crypto_intel":
            crypto_branch = child
            break
    
    if crypto_branch:
        leaf = await tree.spawn_leaf(
            branch=crypto_branch,
            skill_name="coingecko_price",
            tool_func=coingecko_price,
            description="Get real-time crypto prices from CoinGecko API",
        )
        print(f"✅ Added custom leaf: {leaf.name}")
        print(f"📝 Description: {leaf.description}")
        print("\n💡 This is how you combine Hub tools with custom Python skills!")


async def main():
    """Main entry point"""
    
    print("\n" + "=" * 60)
    print("🚀 DEGEN QUICKSTART - OpenAspen + LangChain Hub")
    print("=" * 60)
    print("\nBuild a crypto intelligence tree in 2 minutes!")
    print("Skip building basics—import, test, focus on custom skills.\n")
    
    tree = await build_degen_tree()
    
    await add_custom_degen_leaf(tree)
    
    print("\n" + "=" * 60)
    print("✅ Quickstart Complete!")
    print("=" * 60)
    print("\n🎯 Your DEGEN tree is ready!")
    print("   • 3 branches (crypto, social, utils)")
    print("   • 8+ LangChain Hub tools")
    print("   • 1 custom CoinGecko leaf")
    print("   • RAG-indexed for auto-discovery")
    print("\n📚 Learn more: docs/LANGCHAIN_HUB_INTEGRATION.md")
    print("🔧 Run tests: pytest tests/test_langchain_hub.py")
    print("🌐 Deploy: openaspen server")


if __name__ == "__main__":
    asyncio.run(main())
