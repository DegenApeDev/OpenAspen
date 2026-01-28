import asyncio
import os
from openaspen import OpenAspenTree
from openaspen.llm.providers import create_llm_config


async def greet_user(name: str) -> str:
    """Greet a user by name"""
    return f"Hello, {name}! Welcome to OpenAspen with LM Studio! 🌲"


async def calculate_sum(numbers: str) -> dict:
    """Calculate sum of comma-separated numbers"""
    nums = [float(n.strip()) for n in numbers.split(",")]
    return {"numbers": nums, "sum": sum(nums), "count": len(nums)}


async def get_weather(city: str) -> dict:
    """Get weather information for a city (mock)"""
    return {
        "city": city,
        "temperature": "72°F",
        "condition": "Sunny",
        "humidity": "45%"
    }


async def main():
    print("🚀 OpenAspen with LM Studio Example\n")
    
    # Configure LM Studio
    # Make sure LM Studio is running on http://localhost:1234
    llm_configs = {
        "lmstudio": create_llm_config(
            provider="lmstudio",
            model="local-model",  # This will use whatever model you have loaded in LM Studio
            api_base="http://localhost:1234/v1",  # Default LM Studio endpoint
            temperature=0.7,
            max_tokens=2000,
        )
    }
    
    print("📋 Configuration:")
    print(f"  Provider: LM Studio")
    print(f"  Endpoint: http://localhost:1234/v1")
    print(f"  Model: Whatever is loaded in LM Studio")
    print()
    
    # Create the tree
    tree = OpenAspenTree(
        llm_configs=llm_configs,
        name="LMStudioTree"
    )
    
    # Create branches (agents) for different tasks
    greeting_agent = tree.grow_branch(
        "greeting_assistant",
        description="Handles user greetings and welcomes",
        llm_provider="lmstudio",
        system_prompt="You are a friendly greeter. Keep responses warm and welcoming."
    )
    
    math_agent = tree.grow_branch(
        "math_assistant",
        description="Performs mathematical calculations and analysis",
        llm_provider="lmstudio",
        system_prompt="You are a helpful math assistant. Explain calculations clearly."
    )
    
    weather_agent = tree.grow_branch(
        "weather_assistant",
        description="Provides weather information and forecasts",
        llm_provider="lmstudio",
        system_prompt="You are a weather assistant. Provide clear weather updates."
    )
    
    # Add skills (leaves) to branches
    await tree.spawn_leaf(
        greeting_agent,
        "greet",
        greet_user,
        "Greet users by name with a friendly message"
    )
    
    await tree.spawn_leaf(
        math_agent,
        "sum_numbers",
        calculate_sum,
        "Calculate the sum of comma-separated numbers"
    )
    
    await tree.spawn_leaf(
        weather_agent,
        "get_weather",
        get_weather,
        "Get current weather information for a city"
    )
    
    # Index the tree for RAG-based routing
    print("🔍 Indexing tree for intelligent routing...")
    await tree.index_tree()
    print("✅ Tree indexed!\n")
    
    # Visualize the tree structure
    print("🌲 Tree Structure:")
    print(tree.visualize())
    print()
    
    # Test queries
    queries = [
        "Please greet Alice",
        "What is the sum of 10, 20, 30, 40?",
        "What's the weather like in San Francisco?",
    ]
    
    print("🧪 Testing Queries:\n")
    print("=" * 60)
    
    for i, query in enumerate(queries, 1):
        print(f"\n📝 Query {i}: {query}")
        print("-" * 60)
        
        try:
            result = await tree.execute(query)
            print(f"✅ Result: {result}")
        except Exception as e:
            print(f"❌ Error: {e}")
        
        print()
    
    # Show execution history
    print("=" * 60)
    print("\n📊 Execution History:")
    history = tree.get_execution_history()
    for record in history:
        print(f"\n  Query: {record['query']}")
        print(f"  Branch: {record['branch']}")
        print(f"  Timestamp: {record['timestamp']}")


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("  OpenAspen + LM Studio Integration")
    print("=" * 60 + "\n")
    
    print("⚠️  REQUIREMENTS:")
    print("  1. LM Studio must be running")
    print("  2. A model must be loaded in LM Studio")
    print("  3. Local Server must be started (default: http://localhost:1234)")
    print("\n" + "=" * 60 + "\n")
    
    try:
        asyncio.run(main())
        print("\n✅ Example completed successfully!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\n💡 Troubleshooting:")
        print("  - Make sure LM Studio is running")
        print("  - Check that the local server is started in LM Studio")
        print("  - Verify the endpoint is http://localhost:1234")
        print("  - Ensure a model is loaded")
