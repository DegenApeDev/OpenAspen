import asyncio
import aiohttp
from openaspen import OpenAspenTree
from openaspen.llm.providers import create_llm_config
import os


async def fetch_coingecko(crypto_id: str) -> dict:
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={crypto_id}&vs_currencies=usd&include_24hr_change=true"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                return data
            return {"error": "Failed to fetch price"}


async def analyze_sentiment(text: str) -> dict:
    positive_words = ["bullish", "moon", "pump", "gain", "profit"]
    negative_words = ["bearish", "dump", "crash", "loss", "fear"]

    text_lower = text.lower()
    pos_count = sum(1 for word in positive_words if word in text_lower)
    neg_count = sum(1 for word in negative_words if word in text_lower)

    if pos_count > neg_count:
        sentiment = "positive"
    elif neg_count > pos_count:
        sentiment = "negative"
    else:
        sentiment = "neutral"

    return {
        "sentiment": sentiment,
        "positive_score": pos_count,
        "negative_score": neg_count,
    }


async def calculate_portfolio_value(holdings: dict) -> dict:
    total_value = sum(holdings.values())
    return {
        "total_value": total_value,
        "holdings": holdings,
        "largest_holding": max(holdings.items(), key=lambda x: x[1])[0] if holdings else None,
    }


async def main() -> None:
    llm_configs = {
        "openai": create_llm_config(
            provider="openai",
            model="gpt-4-turbo-preview",
            api_key=os.getenv("OPENAI_API_KEY"),
        ),
        "anthropic": create_llm_config(
            provider="anthropic",
            model="claude-3-opus-20240229",
            api_key=os.getenv("ANTHROPIC_API_KEY"),
        ),
        "grok": create_llm_config(
            provider="grok",
            model="grok-1",
            api_key=os.getenv("GROK_API_KEY"),
        ),
    }

    tree = OpenAspenTree(llm_configs=llm_configs, name="CryptoIntelligenceTree")

    market_branch = tree.grow_branch(
        "market_data",
        description="Real-time cryptocurrency market data and analysis",
        llm_provider="grok",
        system_prompt="You provide fast, accurate crypto market data.",
    )

    await tree.spawn_leaf(
        market_branch,
        "fetch_price",
        fetch_coingecko,
        "Fetch real-time cryptocurrency prices from CoinGecko API",
    )

    await tree.spawn_leaf(
        market_branch,
        "portfolio_value",
        calculate_portfolio_value,
        "Calculate total portfolio value from holdings",
    )

    sentiment_branch = tree.grow_branch(
        "sentiment_analysis",
        description="Analyze market sentiment from text and social media",
        llm_provider="anthropic",
        system_prompt="You analyze crypto market sentiment with nuance.",
    )

    await tree.spawn_leaf(
        sentiment_branch,
        "analyze_text",
        analyze_sentiment,
        "Analyze sentiment of crypto-related text",
    )

    strategy_branch = tree.grow_branch(
        "trading_strategy",
        description="Trading strategy recommendations and risk analysis",
        llm_provider="openai",
        system_prompt="You provide thoughtful trading strategies with risk awareness.",
    )

    await tree.index_tree()

    print("🌲 Advanced Crypto Intelligence Tree")
    print(tree.visualize())
    print()

    queries = [
        "What's the current price of Bitcoin?",
        "Analyze this text: Bitcoin is going to the moon! Bullish trends everywhere!",
        "Calculate my portfolio value: {'BTC': 50000, 'ETH': 30000, 'SOL': 5000}",
    ]

    for query in queries:
        print(f"\n📊 Query: {query}")
        result = await tree.execute(query)
        print(f"✅ Result: {result}")
        print("-" * 80)

    print(f"\n📈 Execution History:")
    for record in tree.get_execution_history():
        print(f"  - {record['query'][:50]}... -> {record['branch']}")


if __name__ == "__main__":
    asyncio.run(main())
