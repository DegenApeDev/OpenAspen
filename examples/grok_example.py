#!/usr/bin/env python3
"""
Example using Grok (X.AI) as the primary LLM provider
Demonstrates fast reasoning with grok-beta model
"""
import asyncio
import os
from dotenv import load_dotenv
from openaspen import OpenAspenTree
from openaspen.llm.providers import create_llm_config

# Load environment variables from .env file
load_dotenv()


async def analyze_with_grok(query: str) -> str:
    """Simple analysis function"""
    return f"Analyzed: {query}"


async def main():
    print("=" * 70)
    print("  🚀 OpenAspen with Grok (X.AI) - Fast Reasoning")
    print("=" * 70)
    print()
    
    # Check for Grok API key
    grok_key = os.getenv("GROK_API_KEY")
    if not grok_key or grok_key.startswith("xai-your"):
        print("❌ Error: GROK_API_KEY not set in .env file")
        print("\n💡 Get your API key from: https://console.x.ai/")
        print("   Then update .env file with your key")
        return
    
    print(f"✅ Grok API Key found: {grok_key[:10]}...")
    print()
    
    # Create Grok config (uses grok-beta by default)
    llm_configs = {
        "grok": create_llm_config(
            provider="grok",
            # model defaults to "grok-beta" (fast reasoning)
            # You can override with: model="grok-vision-beta" for vision tasks
        )
    }
    
    print(f"📋 Configuration:")
    print(f"   Provider: Grok (X.AI)")
    print(f"   Model: {llm_configs['grok'].model}")
    print(f"   API Base: {llm_configs['grok'].api_base}")
    print(f"   Speed Score: {llm_configs['grok'].speed_score}")
    print(f"   Cost per 1K tokens: ${llm_configs['grok'].cost_per_1k_tokens}")
    print()
    
    # Set dummy OpenAI key for embeddings
    os.environ.setdefault("OPENAI_API_KEY", "sk-dummy-for-embeddings")
    
    # Create tree with Grok
    tree = OpenAspenTree(
        llm_configs=llm_configs,
        name="GrokPoweredTree"
    )
    print("✅ Tree created with Grok as LLM provider")
    
    # Add an agent
    agent = tree.grow_branch(
        "reasoning_agent",
        description="Fast reasoning agent powered by Grok",
        llm_provider="grok",
        system_prompt="You are a fast, efficient reasoning AI. Provide clear, concise answers."
    )
    print("✅ Reasoning agent created")
    
    # Add a skill
    await tree.spawn_leaf(
        agent,
        "analyzer",
        analyze_with_grok,
        "Analyzes queries quickly"
    )
    print("✅ Analyzer skill added")
    
    # Index the tree
    await tree.index_tree()
    print("✅ Tree indexed\n")
    
    # Test queries
    queries = [
        "Explain quantum computing in 2 sentences",
        "What are the top 3 benefits of async programming?",
        "Compare Python and Rust for systems programming",
    ]
    
    print("🤖 Testing Grok Fast Reasoning:")
    print("=" * 70)
    
    for i, query in enumerate(queries, 1):
        print(f"\n{i}. Query: {query}")
        print("-" * 70)
        
        try:
            result = await tree.execute(query)
            print(f"✅ Response: {result}")
        except Exception as e:
            print(f"❌ Error: {e}")
            if "api_key" in str(e).lower():
                print("\n💡 Make sure your GROK_API_KEY is valid")
            break
    
    print("\n" + "=" * 70)
    print("\n🎉 Grok integration complete!")
    print("\n💡 Benefits of using Grok:")
    print("   - Fast reasoning with grok-beta model")
    print("   - Cost-effective ($0.005 per 1K tokens)")
    print("   - High speed score (0.95)")
    print("   - Great for real-time applications")


if __name__ == "__main__":
    asyncio.run(main())
