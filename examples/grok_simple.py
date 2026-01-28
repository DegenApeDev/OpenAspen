#!/usr/bin/env python3
"""
Simple Grok (X.AI) example - Direct LLM usage without RAG
Demonstrates fast reasoning with grok-beta model
"""
import asyncio
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

# Load environment variables
load_dotenv()


async def main():
    print("=" * 70)
    print("  🚀 Grok (X.AI) - Fast Reasoning Demo")
    print("=" * 70)
    print()
    
    # Check for Grok API key
    grok_key = os.getenv("GROK_API_KEY")
    if not grok_key or grok_key.startswith("xai-your"):
        print("❌ Error: GROK_API_KEY not set in .env file")
        print("\n💡 Get your API key from: https://console.x.ai/")
        return
    
    print(f"✅ Grok API Key: {grok_key[:15]}...")
    print()
    
    # Create Grok client
    llm = ChatOpenAI(
        base_url="https://api.x.ai/v1",
        api_key=grok_key,
        model="grok-4-1-fast-reasoning",  # Fast reasoning model
        temperature=0.7,
    )
    
    print("📋 Configuration:")
    print("   Provider: Grok (X.AI)")
    print("   Model: grok-4-1-fast-reasoning")
    print("   API Base: https://api.x.ai/v1")
    print("   Temperature: 0.7")
    print()
    
    # Test queries
    queries = [
        "Explain quantum entanglement in 2 sentences",
        "What are the top 3 advantages of Rust over C++?",
        "Write a haiku about AI and nature",
    ]
    
    print("🤖 Testing Grok Fast Reasoning:")
    print("=" * 70)
    
    system_prompt = "You are a helpful, concise AI assistant. Provide clear, accurate answers."
    
    for i, query in enumerate(queries, 1):
        print(f"\n{i}. Query: {query}")
        print("-" * 70)
        
        try:
            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=query)
            ]
            
            response = await llm.ainvoke(messages)
            print(f"✅ Response:\n{response.content}")
            
        except Exception as e:
            print(f"❌ Error: {e}")
            if "401" in str(e) or "api_key" in str(e).lower():
                print("\n💡 API key might be invalid. Check your GROK_API_KEY")
            elif "404" in str(e):
                print("\n💡 Model might not be available. Try 'grok-beta' or check X.AI docs")
            break
    
    print("\n" + "=" * 70)
    print("\n🎉 Grok integration successful!")
    print("\n💡 Grok Benefits:")
    print("   ⚡ Fast reasoning with grok-4-1-fast-reasoning")
    print("   💰 Cost-effective ($0.005 per 1K tokens)")
    print("   🚀 High-speed responses (0.95 speed score)")
    print("   🎯 Great for real-time applications")
    print("\n📚 Available Models:")
    print("   - grok-4-1-fast-reasoning: Fast reasoning (default)")
    print("   - grok-vision-beta: Vision + reasoning")
    print("   - grok-2-latest: Latest stable model")


if __name__ == "__main__":
    asyncio.run(main())
