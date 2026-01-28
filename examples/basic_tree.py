import asyncio
from openaspen import OpenAspenTree
from openaspen.llm.providers import create_llm_config
import os


async def web_search(query: str) -> str:
    return f"Search results for: {query}"


async def fetch_price(crypto: str) -> dict:
    return {"crypto": crypto, "price": 42000, "change_24h": 5.2}


async def code_analyzer(code: str) -> dict:
    return {
        "language": "python",
        "lines": len(code.split("\n")),
        "complexity": "medium",
    }


async def main() -> None:
    llm_configs = {
        "openai": create_llm_config(
            provider="openai",
            model="gpt-4-turbo-preview",
            api_key=os.getenv("OPENAI_API_KEY"),
        ),
        "ollama": create_llm_config(
            provider="ollama",
            model="llama2",
        ),
    }

    async with OpenAspenTree(llm_configs=llm_configs, name="MyFirstTree") as tree:
        crypto_branch = tree.grow_branch(
            "crypto_analyzer",
            description="Cryptocurrency analysis and price tracking",
            llm_provider="openai",
            system_prompt="You are a crypto market analyst.",
        )

        await tree.spawn_leaf(
            crypto_branch,
            "price_check",
            fetch_price,
            "Fetch current cryptocurrency prices from CoinGecko",
        )

        research_branch = tree.grow_branch(
            "research_assistant",
            description="Web research and information gathering",
            llm_provider="ollama",
        )

        await tree.spawn_leaf(
            research_branch,
            "web_search",
            web_search,
            "Search the web for information",
        )

        dev_branch = tree.grow_branch(
            "dev_tools",
            description="Development and code analysis tools",
            llm_provider="openai",
        )

        await tree.spawn_leaf(
            dev_branch,
            "analyze_code",
            code_analyzer,
            "Analyze code complexity and structure",
        )

        await tree.index_tree()

        print(tree.visualize())
        print()

        result = await tree.execute("What's the price of Bitcoin?")
        print("Result:", result)

        tree.save_to_file("examples/tree.json")


if __name__ == "__main__":
    asyncio.run(main())
