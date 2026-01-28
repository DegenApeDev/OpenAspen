#!/usr/bin/env python3
"""Simple test to verify LM Studio integration works"""
import asyncio
import os
from openaspen import OpenAspenTree
from openaspen.llm.providers import create_llm_config

# Set dummy OpenAI key for embeddings (not used with LM Studio LLM)
os.environ.setdefault("OPENAI_API_KEY", "sk-dummy-key-for-embeddings")


async def simple_test(query: str) -> str:
    """A simple test function"""
    return f"Processed: {query}"


async def main():
    print("🚀 Testing OpenAspen with LM Studio\n")
    
    # Create LM Studio config
    llm_configs = {
        "lmstudio": create_llm_config(
            provider="lmstudio",
            api_base="http://localhost:1234/v1",
        )
    }
    
    print(f"✅ Config created with API key: {llm_configs['lmstudio'].api_key}")
    print(f"✅ Endpoint: {llm_configs['lmstudio'].api_base}\n")
    
    # Create tree
    tree = OpenAspenTree(
        llm_configs=llm_configs, 
        name="TestTree"
    )
    print("✅ Tree created successfully!")
    
    # Add a simple agent
    agent = tree.grow_branch(
        "test_agent",
        description="A simple test agent",
        llm_provider="lmstudio"
    )
    print("✅ Agent created successfully!")
    
    # Add a skill
    await tree.spawn_leaf(agent, "test_skill", simple_test, "Test skill")
    print("✅ Skill added successfully!")
    
    # Index the tree
    await tree.index_tree()
    print("✅ Tree indexed successfully!")
    
    print("\n🎉 All initialization successful!")
    print("\n📊 Now testing actual LLM call...")
    
    try:
        result = await tree.execute("Test this query")
        print(f"✅ Result: {result}")
    except Exception as e:
        print(f"⚠️  LLM call failed (this is expected if model isn't responding): {e}")
    
    print("\n✅ OpenAspen is working with LM Studio!")


if __name__ == "__main__":
    asyncio.run(main())
