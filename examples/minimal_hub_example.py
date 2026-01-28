#!/usr/bin/env python3
"""
Minimal LangChain Hub Example - No API Keys Required
Demonstrates LangChain Hub integration with LM Studio (local LLM)
Default setup: LM Studio (free, local) -> Grok (fast) -> OpenAI/Anthropic (optional)
"""

import asyncio
from openaspen.integrations.langchain_hub import LangChainHubLoader


async def demo_list_tools():
    """Demo: List all available LangChain Hub tools"""
    print("=" * 60)
    print("Available LangChain Hub Tools")
    print("=" * 60)
    print()
    
    tools = LangChainHubLoader.list_available_tools()
    
    for tool_name in tools:
        info = LangChainHubLoader.get_tool_info(tool_name)
        api_key_req = f" (requires {info['requires_api_key']})" if info['requires_api_key'] else " ✅ No API key"
        print(f"• {tool_name}{api_key_req}")
        print(f"  {info['description']}")
        print()


async def demo_load_tool():
    """Demo: Load a tool without API key requirement"""
    print("=" * 60)
    print("Loading DuckDuckGo Search Tool")
    print("=" * 60)
    print()
    
    try:
        # Load DuckDuckGo search (no API key required)
        tool = LangChainHubLoader.load_tool("duckduckgo_search")
        print(f"✅ Loaded tool: {tool.__class__.__name__}")
        print(f"   Tool type: {type(tool)}")
        print()
        
        # Try a simple search
        print("Testing search for 'Python programming'...")
        result = tool.run("Python programming")
        print(f"✅ Search successful!")
        print(f"   Result preview: {result[:200]}...")
        
    except ImportError as e:
        print(f"⚠️  Tool dependencies not installed: {e}")
        print(f"   Install with: pip install duckduckgo-search")
    except Exception as e:
        print(f"❌ Error: {e}")


async def demo_create_leaf():
    """Demo: Create a Leaf from a hub tool"""
    print()
    print("=" * 60)
    print("Creating Leaf from Hub Tool")
    print("=" * 60)
    print()
    
    try:
        # Create a leaf from Wikipedia tool (no API key)
        leaf = LangChainHubLoader.create_leaf_from_hub(
            tool_name="wikipedia",
            leaf_name="wiki_search",
        )
        
        print(f"✅ Created leaf: {leaf.name}")
        print(f"   Description: {leaf.description}")
        print(f"   Metadata: {leaf.metadata}")
        print()
        
        # Test the leaf
        print("Testing leaf with query 'Python (programming language)'...")
        result = await leaf.execute("Python (programming language)")
        
        if result["success"]:
            print(f"✅ Leaf execution successful!")
            print(f"   Result preview: {str(result['result'])[:200]}...")
        else:
            print(f"❌ Leaf execution failed: {result.get('error')}")
            
    except ImportError as e:
        print(f"⚠️  Tool dependencies not installed: {e}")
        print(f"   Install with: pip install wikipedia")
    except Exception as e:
        print(f"❌ Error: {e}")


async def demo_tool_info():
    """Demo: Get detailed info about a specific tool"""
    print()
    print("=" * 60)
    print("Tool Information: DuckDuckGo Search")
    print("=" * 60)
    print()
    
    info = LangChainHubLoader.get_tool_info("duckduckgo_search")
    
    print(f"Name: duckduckgo_search")
    print(f"Description: {info['description']}")
    print(f"Import Path: {info['import_path']}")
    print(f"Class Name: {info['class_name']}")
    print(f"Default Params: {info['default_params']}")
    print(f"API Key Required: {info['requires_api_key'] or 'None'}")


async def main():
    """Run all demos"""
    print()
    print("🌲 OpenAspen LangChain Hub - Minimal Example")
    print("=" * 60)
    print()
    print("This example demonstrates LangChain Hub integration")
    print("WITHOUT requiring OpenAI or Anthropic API keys.")
    print()
    
    await demo_list_tools()
    await demo_tool_info()
    await demo_load_tool()
    await demo_create_leaf()
    
    print()
    print("=" * 60)
    print("✅ Demo Complete!")
    print("=" * 60)
    print()
    print("Next Steps:")
    print("  1. Install hub tools: pip install duckduckgo-search wikipedia")
    print("  2. Try the full example: python examples/langchain_hub_example.py")
    print("  3. Build your tree: python examples/degen_quickstart.py")
    print("     (requires OPENAI_API_KEY in .env)")
    print()


if __name__ == "__main__":
    asyncio.run(main())
