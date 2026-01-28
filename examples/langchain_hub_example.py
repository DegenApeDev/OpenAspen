import asyncio
from openaspen import OpenAspenTree
from openaspen.llm.providers import create_llm_config
from openaspen.integrations.langchain_hub import LangChainHubLoader, load_hub_tools


async def example_basic_hub_integration():
    """
    Example 1: Basic LangChain Hub tool integration
    Load a single tool and add it to a branch
    """
    print("=" * 60)
    print("Example 1: Basic Hub Tool Integration")
    print("=" * 60)

    llm_configs = {
        "openai": create_llm_config(provider="openai", model="gpt-4-turbo-preview"),
    }

    tree = OpenAspenTree(name="degen_tree", llm_configs=llm_configs)
    crypto_branch = tree.add_branch("crypto_intel", llm_provider="openai")

    leaf = await LangChainHubLoader.add_hub_tool_to_branch(
        branch=crypto_branch,
        tool_name="duckduckgo_search",
        leaf_name="web_search",
        rag_db=tree.shared_rag_db,
    )

    print(f"✅ Added leaf: {leaf.name}")
    print(f"📝 Description: {leaf.description}")
    print(f"🌳 Path: {'/'.join(leaf.get_path())}")


async def example_multiple_tools():
    """
    Example 2: Load multiple LangChain Hub tools at once
    Build a DEGEN starter tree with top tools
    """
    print("\n" + "=" * 60)
    print("Example 2: DEGEN Starter Tree with Multiple Hub Tools")
    print("=" * 60)

    llm_configs = {
        "openai": create_llm_config(provider="openai", model="gpt-4-turbo-preview"),
    }

    tree = OpenAspenTree(name="degen_starter", llm_configs=llm_configs)

    crypto_branch = tree.add_branch(
        "crypto_intel",
        description="Crypto market intelligence and news",
        llm_provider="openai",
    )

    social_branch = tree.add_branch(
        "social_intel",
        description="Social media and influencer tracking",
        llm_provider="openai",
    )

    tools_for_crypto = [
        ("duckduckgo_search", "market_search"),
        ("yahoo_finance_news", "finance_news"),
        ("wikipedia", "crypto_wiki"),
    ]

    for tool_name, leaf_name in tools_for_crypto:
        leaf = await LangChainHubLoader.add_hub_tool_to_branch(
            branch=crypto_branch,
            tool_name=tool_name,
            leaf_name=leaf_name,
            rag_db=tree.shared_rag_db,
        )
        print(f"  ✅ {leaf_name}: {leaf.description}")

    tools_for_social = [
        ("reddit_search", "reddit_scan"),
        ("youtube_search", "youtube_scan"),
    ]

    for tool_name, leaf_name in tools_for_social:
        try:
            leaf = await LangChainHubLoader.add_hub_tool_to_branch(
                branch=social_branch,
                tool_name=tool_name,
                leaf_name=leaf_name,
                rag_db=tree.shared_rag_db,
            )
            print(f"  ✅ {leaf_name}: {leaf.description}")
        except Exception as e:
            print(f"  ⚠️  {leaf_name}: {e}")

    print(f"\n🌲 Tree Structure:")
    print(tree.visualize())


async def example_custom_tool_params():
    """
    Example 3: Load hub tool with custom parameters
    """
    print("\n" + "=" * 60)
    print("Example 3: Custom Tool Parameters")
    print("=" * 60)

    llm_configs = {
        "openai": create_llm_config(provider="openai", model="gpt-4-turbo-preview"),
    }

    tree = OpenAspenTree(name="custom_tree", llm_configs=llm_configs)
    search_branch = tree.add_branch("search", llm_provider="openai")

    leaf = LangChainHubLoader.create_leaf_from_hub(
        tool_name="tavily_search",
        leaf_name="deep_search",
        custom_params={"max_results": 10},
        llm_provider="openai",
    )

    search_branch.add_child(leaf)
    await tree.shared_rag_db.index_leaf(leaf, search_branch.name)

    print(f"✅ Created custom leaf: {leaf.name}")
    print(f"📝 Description: {leaf.description}")
    print(f"⚙️  Custom params: max_results=10")


async def example_programmatic_usage():
    """
    Example 4: Direct programmatic usage (no CLI)
    """
    print("\n" + "=" * 60)
    print("Example 4: Programmatic Usage")
    print("=" * 60)

    from langchain_community.tools import DuckDuckGoSearchRun

    llm_configs = {
        "openai": create_llm_config(provider="openai", model="gpt-4-turbo-preview"),
    }

    tree = OpenAspenTree(name="code_tree", llm_configs=llm_configs)
    branch = tree.add_branch("research", llm_provider="openai")

    ddg_tool = DuckDuckGoSearchRun()

    async def search_wrapper(query: str, **kwargs):
        """Custom wrapper for DuckDuckGo search"""
        result = await asyncio.to_thread(ddg_tool.run, query)
        return result

    leaf = await tree.spawn_leaf(
        branch=branch,
        skill_name="custom_search",
        tool_func=search_wrapper,
        description="Custom DuckDuckGo search implementation",
    )

    print(f"✅ Added custom leaf: {leaf.name}")
    print(f"📝 Description: {leaf.description}")


async def example_list_available_tools():
    """
    Example 5: List all available LangChain Hub tools
    """
    print("\n" + "=" * 60)
    print("Example 5: Available LangChain Hub Tools")
    print("=" * 60)

    tools = LangChainHubLoader.list_available_tools()
    print(f"\n🔧 {len(tools)} tools available:\n")

    for tool_name in tools:
        info = LangChainHubLoader.get_tool_info(tool_name)
        api_key_info = f" (requires {info['requires_api_key']})" if info["requires_api_key"] else ""
        print(f"  • {tool_name}{api_key_info}")
        print(f"    {info['description']}")


async def example_load_tools_compatibility():
    """
    Example 6: LangChain load_tools() compatibility
    """
    print("\n" + "=" * 60)
    print("Example 6: LangChain load_tools() Compatibility")
    print("=" * 60)

    tools = load_hub_tools(["duckduckgo_search", "wikipedia"])

    print(f"✅ Loaded {len(tools)} tools using load_hub_tools()")
    for tool in tools:
        print(f"  • {tool.__class__.__name__}")


async def main():
    """Run all examples"""
    print("\n🌲 OpenAspen LangChain Hub Integration Examples\n")

    await example_list_available_tools()
    await example_basic_hub_integration()
    await example_multiple_tools()
    await example_custom_tool_params()
    await example_programmatic_usage()
    await example_load_tools_compatibility()

    print("\n" + "=" * 60)
    print("✅ All examples completed!")
    print("=" * 60)
    print("\n💡 Next steps:")
    print("  1. Set API keys in .env (TAVILY_API_KEY, etc.)")
    print("  2. Try CLI: openaspen grow_leaf --list-tools")
    print("  3. Add tools: openaspen grow_leaf crypto_branch tavily_search --hub --config tree.json")
    print("  4. Build your DEGEN tree with custom leaves!")


if __name__ == "__main__":
    asyncio.run(main())
