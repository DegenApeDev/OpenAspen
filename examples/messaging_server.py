#!/usr/bin/env python3
"""
OpenAspen Messaging Server
FastAPI server with Telegram + WhatsApp webhook endpoints
"""
import os
import asyncio
from dotenv import load_dotenv
from fastapi import FastAPI
import uvicorn

from openaspen import OpenAspenTree
from openaspen.llm.providers import create_llm_config
from openaspen.integrations.gateway import MessageGateway
from openaspen.server.messaging_api import router, set_gateway

# Load environment variables
load_dotenv()


def create_messaging_app() -> FastAPI:
    """Create FastAPI app with messaging integration"""
    
    app = FastAPI(
        title="OpenAspen Messaging Server",
        description="24/7 AI agent tree accessible via Telegram and WhatsApp",
        version="0.1.0"
    )
    
    # Create LLM configs
    llm_configs = {}
    
    # Grok
    grok_key = os.getenv("GROK_API_KEY")
    if grok_key and not grok_key.startswith("xai-your"):
        llm_configs["grok"] = create_llm_config(provider="grok")
    
    # LM Studio
    llm_configs["lmstudio"] = create_llm_config(
        provider="lmstudio",
        api_base=os.getenv("LMSTUDIO_BASE_URL", "http://localhost:1234/v1")
    )
    
    # Set dummy OpenAI key for embeddings
    os.environ.setdefault("OPENAI_API_KEY", "sk-dummy-for-embeddings")
    
    # Create OpenAspen tree
    try:
        tree = OpenAspenTree(llm_configs=llm_configs, name="MessagingTree")
        print("✅ OpenAspen tree created")
    except Exception as e:
        print(f"⚠️  Tree creation failed: {e}")
        print("   Running in demo mode")
        tree = None
    
    # Create message gateway
    gateway = MessageGateway(tree_executor=tree)
    
    # Register Telegram bot
    telegram_token = os.getenv("TELEGRAM_BOT_TOKEN")
    if telegram_token:
        gateway.register_telegram(telegram_token)
        print("✅ Telegram bot registered")
    else:
        print("⚠️  TELEGRAM_BOT_TOKEN not set - Telegram disabled")
    
    # Register WhatsApp bot
    whatsapp_token = os.getenv("WHATSAPP_TOKEN")
    whatsapp_phone_id = os.getenv("WHATSAPP_PHONE_ID")
    if whatsapp_token and whatsapp_phone_id:
        whatsapp_bot = gateway.register_whatsapp(whatsapp_token, whatsapp_phone_id)
        whatsapp_verify_token = os.getenv("WHATSAPP_VERIFY_TOKEN", "openaspen_verify")
        whatsapp_bot.set_verify_token(whatsapp_verify_token)
        print("✅ WhatsApp bot registered")
    else:
        print("⚠️  WhatsApp credentials not set - WhatsApp disabled")
    
    # Set gateway for API routes
    set_gateway(gateway)
    
    # Include messaging router
    app.include_router(router)
    
    @app.get("/")
    async def root():
        return {
            "name": "OpenAspen Messaging Server",
            "version": "0.1.0",
            "status": "running",
            "platforms": list(gateway.handlers.keys())
        }
    
    @app.get("/health")
    async def health():
        return {"status": "healthy"}
    
    return app


if __name__ == "__main__":
    print("=" * 70)
    print("  🌲 OpenAspen Messaging Server")
    print("=" * 70)
    print()
    
    app = create_messaging_app()
    
    print()
    print("🚀 Starting server...")
    print("   Host: 0.0.0.0")
    print("   Port: 8000")
    print()
    print("📡 Webhook endpoints:")
    print("   Telegram: http://your-domain.com/messaging/telegram/webhook")
    print("   WhatsApp: http://your-domain.com/messaging/whatsapp/webhook")
    print()
    print("💡 To setup webhooks:")
    print("   POST http://localhost:8000/messaging/setup-webhooks")
    print("   Body: {\"base_url\": \"https://your-domain.com\"}")
    print()
    print("=" * 70)
    print()
    
    uvicorn.run(app, host="0.0.0.0", port=8000)
