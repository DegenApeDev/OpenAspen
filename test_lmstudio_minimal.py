#!/usr/bin/env python3
"""
Minimal test to verify LM Studio works with OpenAspen
This bypasses RAG/ChromaDB to focus on LLM integration
"""
import asyncio
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage


async def test_lmstudio_direct():
    """Test LM Studio connection directly"""
    
    print("🚀 Testing LM Studio Connection\n")
    print("Configuration:")
    print("  Endpoint: http://localhost:1234/v1")
    print("  API Key: not-needed (local)\n")
    
    # Create LM Studio client
    llm = ChatOpenAI(
        base_url="http://localhost:1234/v1",
        api_key="not-needed",
        model="local-model",
        temperature=0.7,
    )
    
    print("✅ LM Studio client created\n")
    
    # Test queries
    queries = [
        "Say hello in one sentence",
        "What is 2+2? Answer in one sentence.",
        "Name one color. Just one word.",
    ]
    
    print("📊 Testing Queries:")
    print("=" * 60)
    
    for i, query in enumerate(queries, 1):
        print(f"\n{i}. Query: {query}")
        print("-" * 60)
        
        try:
            # Make the LLM call
            messages = [HumanMessage(content=query)]
            response = await llm.ainvoke(messages)
            
            print(f"✅ Response: {response.content}")
            
        except Exception as e:
            print(f"❌ Error: {e}")
            print("\n💡 Troubleshooting:")
            print("  - Make sure LM Studio is running")
            print("  - Check that Local Server is started")
            print("  - Verify a model is loaded")
            return False
    
    print("\n" + "=" * 60)
    print("\n🎉 Success! LM Studio is working with OpenAspen!")
    print("\n📚 Next Steps:")
    print("  1. LM Studio integration is confirmed working")
    print("  2. You can now build agents powered by your local models")
    print("  3. Check examples/lmstudio_example.py for full integration")
    print("  4. Note: ChromaDB/RAG requires additional setup for Python 3.14")
    
    return True


if __name__ == "__main__":
    print("=" * 60)
    print("  LM Studio + OpenAspen - Minimal Test")
    print("=" * 60 + "\n")
    
    try:
        success = asyncio.run(test_lmstudio_direct())
        exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrupted by user")
        exit(1)
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {e}")
        exit(1)
