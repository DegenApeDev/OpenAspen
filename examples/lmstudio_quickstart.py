#!/usr/bin/env python3
"""
LM Studio Quickstart - Zero API Keys Required
Build a complete OpenAspen tree using LM Studio (free local LLM)

Prerequisites:
1. Install LM Studio: https://lmstudio.ai/
2. Download a model (e.g., Llama 3.2, Mistral, Qwen)
3. Start LM Studio server (default: http://localhost:1234)
"""

import asyncio
from openaspen import OpenAspenTree
from openaspen.llm.providers import create_llm_config
from openaspen.integrations.langchain_hub import LangChainHubLoader


async def build_local_tree():
    """Build a complete tree using LM Studio - no API keys needed!"""
    
    print("🌲 Building OpenAspen Tree with LM Studio")
    print("=" * 60)
    print()
    
    # LM Studio config - NO API KEY REQUIRED
    llm_configs = {
        "lmstudio": create_llm_config(
            provider="ollama",  # LM Studio uses OpenAI-compatible API
            model="local-model",  # Model name doesn't matter for LM Studio
            api_base="http://localhost:1234/v1",  # LM Studio default port
            api_key="not-needed",  # LM Studio doesn't need API key
        ),
    }
    
    tree = OpenAspenTree(name="local_tree", llm_configs=llm_configs)
    
    print("📊 Adding Research Branch...")
    research = tree.add_branch(
        "research",
        description="Research and information gathering",
        llm_provider="lmstudio",
        system_prompt="You are a helpful research assistant. Provide concise, accurate information.",
    )
    
    # Add LangChain Hub tools (no API keys needed)
    print("  ✅ Adding DuckDuckGo search (no API key)")
    try:
        await LangChainHubLoader.add_hub_tool_to_branch(
            branch=research,
            tool_name="duckduckgo_search",
            leaf_name="web_search",
            rag_db=tree.shared_rag_db,
        )
    except Exception as e:
        print(f"  ⚠️  Skipped web_search: {e}")
        print(f"     Install with: pip install duckduckgo-search")
    
    print("  ✅ Adding Wikipedia (no API key)")
    try:
        await LangChainHubLoader.add_hub_tool_to_branch(
            branch=research,
            tool_name="wikipedia",
            leaf_name="wiki_lookup",
            rag_db=tree.shared_rag_db,
        )
    except Exception as e:
        print(f"  ⚠️  Skipped wiki_lookup: {e}")
        print(f"     Install with: pip install wikipedia")
    
    print()
    print("🔧 Adding Utility Branch...")
    utils = tree.add_branch(
        "utils",
        description="Utility tools and helpers",
        llm_provider="lmstudio",
    )
    
    print("  ✅ Adding arXiv search (no API key)")
    try:
        await LangChainHubLoader.add_hub_tool_to_branch(
            branch=utils,
            tool_name="arxiv",
            leaf_name="research_papers",
            rag_db=tree.shared_rag_db,
        )
    except Exception as e:
        print(f"  ⚠️  Skipped research_papers: {e}")
    
    print()
    print("=" * 60)
    print("🎉 Tree Built Successfully with LM Studio!")
    print("=" * 60)
    print()
    print("📋 Tree Structure:")
    print(tree.visualize())
    
    return tree


async def demo_query(tree):
    """Demo: Run a query through the local tree"""
    
    print()
    print("=" * 60)
    print("🔍 Testing Query with LM Studio")
    print("=" * 60)
    print()
    
    query = "What is Python programming language?"
    print(f"Query: {query}")
    print()
    
    try:
        result = await tree.execute(query)
        print("✅ Result:")
        print(result)
    except Exception as e:
        print(f"⚠️  Query failed: {e}")
        print()
        print("Make sure LM Studio is running:")
        print("  1. Open LM Studio")
        print("  2. Load a model")
        print("  3. Start the server (default port 1234)")


async def main():
    """Main entry point"""
    
    print()
    print("=" * 60)
    print("🚀 LM STUDIO QUICKSTART - Zero API Keys!")
    print("=" * 60)
    print()
    print("This example uses LM Studio for FREE local LLM inference.")
    print("No OpenAI, Anthropic, or Grok API keys required!")
    print()
    print("Prerequisites:")
    print("  1. Install LM Studio: https://lmstudio.ai/")
    print("  2. Download a model (Llama 3.2, Mistral, Qwen, etc.)")
    print("  3. Start the server in LM Studio")
    print()
    
    # Check if LM Studio is running
    import aiohttp
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get("http://localhost:1234/v1/models", timeout=2) as resp:
                if resp.status == 200:
                    print("✅ LM Studio server detected!")
                    print()
                else:
                    print("⚠️  LM Studio server not responding properly")
                    print("   Make sure a model is loaded and server is started")
                    print()
    except Exception:
        print("❌ LM Studio server not running!")
        print()
        print("To start LM Studio server:")
        print("  1. Open LM Studio application")
        print("  2. Go to 'Local Server' tab")
        print("  3. Load a model")
        print("  4. Click 'Start Server'")
        print()
        print("Continuing anyway to show tree structure...")
        print()
    
    tree = await build_local_tree()
    
    # Uncomment to test queries (requires LM Studio running)
    # await demo_query(tree)
    
    print()
    print("=" * 60)
    print("✅ Quickstart Complete!")
    print("=" * 60)
    print()
    print("🎯 Your local tree is ready!")
    print("   • No API keys required")
    print("   • Free local LLM via LM Studio")
    print("   • LangChain Hub tools integrated")
    print()
    print("Next Steps:")
    print("  1. Start LM Studio server if not running")
    print("  2. Uncomment the demo_query() call to test")
    print("  3. Add custom leaves for your use case")
    print("  4. Optional: Add Grok API key for faster cloud inference")
    print()


if __name__ == "__main__":
    asyncio.run(main())
