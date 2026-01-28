#!/usr/bin/env python3
"""
OpenAspen Server - Production-ready API server
Runs with LM Studio (zero API keys) or cloud LLMs (optional)

Usage:
    python start_server.py                    # LM Studio only (no API keys)
    python start_server.py --with-grok        # LM Studio + Grok
    python start_server.py --with-openai      # LM Studio + OpenAI
"""

import asyncio
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import os
import argparse
import logging

from openaspen import OpenAspenTree
from openaspen.llm.providers import create_llm_config
from openaspen.integrations.langchain_hub import LangChainHubLoader

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ChatMessage(BaseModel):
    role: str
    content: str


class ChatCompletionRequest(BaseModel):
    model: str = "openaspen"
    messages: List[ChatMessage]
    temperature: float = 0.7
    max_tokens: int = 2000


class ChatCompletionResponse(BaseModel):
    id: str = "chatcmpl-openaspen"
    object: str = "chat.completion"
    created: int
    model: str
    choices: List[Dict[str, Any]]


class QueryRequest(BaseModel):
    query: str


def create_tree(use_grok: bool = False, use_openai: bool = False) -> OpenAspenTree:
    """Create OpenAspen tree with LM Studio and optional cloud LLMs"""
    
    llm_configs = {
        "lmstudio": create_llm_config(
            provider="ollama",
            api_base="http://localhost:1234/v1",
            api_key="not-needed",
        ),
    }
    
    # Add Grok if requested
    if use_grok:
        grok_key = os.getenv("GROK_API_KEY")
        if grok_key:
            llm_configs["grok"] = create_llm_config(
                provider="openai",
                model="grok-beta",
                api_key=grok_key,
                api_base="https://api.x.ai/v1",
            )
            logger.info("✅ Grok enabled")
        else:
            logger.warning("⚠️  GROK_API_KEY not found in environment")
    
    # Add OpenAI if requested
    if use_openai:
        openai_key = os.getenv("OPENAI_API_KEY")
        if openai_key:
            llm_configs["openai"] = create_llm_config(
                provider="openai",
                model="gpt-4-turbo-preview",
                api_key=openai_key,
            )
            logger.info("✅ OpenAI enabled")
        else:
            logger.warning("⚠️  OPENAI_API_KEY not found in environment")
    
    # Create tree with fake embeddings (no API key needed)
    tree = OpenAspenTree(
        name="openaspen_server",
        llm_configs=llm_configs,
        use_embeddings=True,  # Uses fake embeddings by default
    )
    
    logger.info(f"🌲 Created tree with providers: {list(llm_configs.keys())}")
    
    return tree


async def setup_tree(tree: OpenAspenTree) -> None:
    """Setup tree with branches and tools"""
    
    # Research branch
    research = tree.add_branch(
        "research",
        description="Research and information gathering",
        llm_provider="lmstudio",
        system_prompt="You are a helpful research assistant. Provide concise, accurate information.",
    )
    
    # Try to add hub tools (graceful failure if dependencies missing)
    try:
        # Custom leaf using direct DuckDuckGo (works without LangChain wrapper issues)
        async def web_search(query: str, **kwargs):
            """Search the web using DuckDuckGo"""
            try:
                from duckduckgo_search import DDGS
                results = list(DDGS().text(query, max_results=5))
                return {"query": query, "results": results, "count": len(results)}
            except Exception as e:
                return {"error": str(e), "query": query}
        
        await tree.spawn_leaf(
            research,
            "web_search",
            web_search,
            "Search the web for information"
        )
        logger.info("  ✅ Added web_search leaf")
    except Exception as e:
        logger.warning(f"  ⚠️  Could not add web_search: {e}")
    
    try:
        # Wikipedia search
        async def wiki_search(query: str, **kwargs):
            """Search Wikipedia"""
            try:
                import wikipedia
                summary = wikipedia.summary(query, sentences=3)
                return {"query": query, "summary": summary}
            except Exception as e:
                return {"error": str(e), "query": query}
        
        await tree.spawn_leaf(
            research,
            "wiki_search",
            wiki_search,
            "Search Wikipedia for information"
        )
        logger.info("  ✅ Added wiki_search leaf")
    except Exception as e:
        logger.warning(f"  ⚠️  Could not add wiki_search: {e}")
    
    # Utility branch
    utils = tree.add_branch(
        "utils",
        description="Utility functions and helpers",
        llm_provider="lmstudio",
    )
    
    # Add a simple echo tool
    async def echo(text: str, **kwargs):
        """Echo back the input text"""
        return {"input": text, "output": text}
    
    await tree.spawn_leaf(utils, "echo", echo, "Echo back the input")
    logger.info("  ✅ Added echo leaf")
    
    logger.info(f"🌳 Tree setup complete with {len(tree.branches)} branches")


def create_app(tree: OpenAspenTree) -> FastAPI:
    """Create FastAPI application"""
    
    app = FastAPI(
        title="OpenAspen API",
        description="OpenAI-compatible API for OpenAspen tree-structured agents",
        version="0.1.0",
    )
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    @app.get("/")
    async def root():
        return {
            "name": "OpenAspen API",
            "version": "0.1.0",
            "status": "running",
            "providers": tree.llm_router.get_available_providers(),
            "branches": [b.name for b in tree.branches],
        }
    
    @app.get("/health")
    async def health():
        return {"status": "healthy"}
    
    @app.get("/v1/models")
    async def list_models():
        return {
            "object": "list",
            "data": [
                {
                    "id": "openaspen",
                    "object": "model",
                    "created": 1234567890,
                    "owned_by": "openaspen",
                }
            ],
        }
    
    @app.post("/v1/chat/completions")
    async def chat_completions(request: ChatCompletionRequest):
        try:
            last_message = request.messages[-1].content if request.messages else ""
            result = await tree.execute(last_message)
            
            response_content = str(result)
            
            import time
            return ChatCompletionResponse(
                created=int(time.time()),
                model=request.model,
                choices=[
                    {
                        "index": 0,
                        "message": {"role": "assistant", "content": response_content},
                        "finish_reason": "stop",
                    }
                ],
            )
        except Exception as e:
            logger.error(f"Chat completion failed: {e}")
            raise HTTPException(status_code=500, detail=str(e))
    
    @app.post("/query")
    async def query(request: QueryRequest):
        """Direct query endpoint"""
        try:
            result = await tree.execute(request.query)
            return {"query": request.query, "result": result}
        except Exception as e:
            logger.error(f"Query failed: {e}")
            raise HTTPException(status_code=500, detail=str(e))
    
    @app.get("/tree/info")
    async def tree_info():
        return {
            "name": tree.name,
            "branches": [
                {
                    "name": b.name,
                    "description": b.description,
                    "leaves": [l.name for l in b.get_leaves()],
                }
                for b in tree.branches
            ],
            "providers": tree.llm_router.get_available_providers(),
        }
    
    @app.get("/tree/visualize")
    async def visualize():
        return {"visualization": tree.visualize()}
    
    return app


async def main():
    parser = argparse.ArgumentParser(description="OpenAspen API Server")
    parser.add_argument("--host", default="0.0.0.0", help="Host to bind to")
    parser.add_argument("--port", type=int, default=8000, help="Port to bind to")
    parser.add_argument("--with-grok", action="store_true", help="Enable Grok (requires GROK_API_KEY)")
    parser.add_argument("--with-openai", action="store_true", help="Enable OpenAI (requires OPENAI_API_KEY)")
    parser.add_argument("--reload", action="store_true", help="Enable auto-reload")
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("🌲 OpenAspen API Server")
    print("=" * 60)
    print()
    print("Configuration:")
    print(f"  • LM Studio: ✅ (default, no API key)")
    print(f"  • Grok: {'✅' if args.with_grok else '❌'}")
    print(f"  • OpenAI: {'✅' if args.with_openai else '❌'}")
    print()
    
    # Check LM Studio
    try:
        import aiohttp
        async with aiohttp.ClientSession() as session:
            async with session.get("http://localhost:1234/v1/models", timeout=2) as resp:
                if resp.status == 200:
                    print("✅ LM Studio server detected!")
                else:
                    print("⚠️  LM Studio server not responding properly")
    except Exception:
        print("❌ LM Studio server not running!")
        print("   Start LM Studio and load a model before continuing.")
        print("   Download from: https://lmstudio.ai/")
        print()
    
    # Create tree
    print("\n🌲 Building tree...")
    tree = create_tree(use_grok=args.with_grok, use_openai=args.with_openai)
    
    # Setup branches and tools
    print("📊 Setting up branches and tools...")
    await setup_tree(tree)
    
    # Create app
    app = create_app(tree)
    
    print()
    print("=" * 60)
    print("🚀 Server starting...")
    print("=" * 60)
    print()
    print(f"📡 API endpoint: http://{args.host}:{args.port}")
    print(f"📚 Docs: http://{args.host}:{args.port}/docs")
    print(f"🌳 Tree info: http://{args.host}:{args.port}/tree/info")
    print()
    print("Example requests:")
    print(f"  curl http://localhost:{args.port}/")
    print(f"  curl http://localhost:{args.port}/tree/visualize")
    print(f'  curl -X POST http://localhost:{args.port}/query -H "Content-Type: application/json" -d \'{{"query": "Hello!"}}\'')
    print()
    print("Press Ctrl+C to stop")
    print("=" * 60)
    print()
    
    # Run server
    config = uvicorn.Config(
        app,
        host=args.host,
        port=args.port,
        reload=args.reload,
        log_level="info",
    )
    server = uvicorn.Server(config)
    await server.serve()


if __name__ == "__main__":
    asyncio.run(main())
