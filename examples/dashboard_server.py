#!/usr/bin/env python3
"""
OpenAspen Dashboard Server
Flask-based web dashboard for local management
"""
import os
from dotenv import load_dotenv

from openaspen import OpenAspenTree
from openaspen.llm.providers import create_llm_config
from openaspen.dashboard import create_dashboard_app

# Load environment variables
load_dotenv()


def main():
    print("=" * 70)
    print("  🌲 OpenAspen Dashboard Server")
    print("=" * 70)
    print()
    
    # Create LLM configs
    llm_configs = {}
    
    # Grok
    grok_key = os.getenv("GROK_API_KEY")
    if grok_key and not grok_key.startswith("xai-your"):
        llm_configs["grok"] = create_llm_config(provider="grok")
        print("✅ Grok configured")
    
    # LM Studio
    llm_configs["lmstudio"] = create_llm_config(
        provider="lmstudio",
        api_base=os.getenv("LMSTUDIO_BASE_URL", "http://localhost:1234/v1")
    )
    print("✅ LM Studio configured")
    
    # Set dummy OpenAI key for embeddings
    os.environ.setdefault("OPENAI_API_KEY", "sk-dummy-for-embeddings")
    
    # Create OpenAspen tree
    tree = None
    try:
        tree = OpenAspenTree(llm_configs=llm_configs, name="DashboardTree")
        print("✅ OpenAspen tree created")
        
        # Add example branch and leaf
        branch = tree.grow_branch(
            "demo_agent",
            description="Demo agent for dashboard testing",
            llm_provider="grok" if "grok" in llm_configs else "lmstudio"
        )
        
        async def demo_skill(query: str) -> str:
            """Demo skill function"""
            return f"Processed: {query}"
        
        import asyncio
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(
            tree.spawn_leaf(branch, "demo_skill", demo_skill, "Demo skill for testing")
        )
        loop.close()
        
        print("✅ Demo agent and skill added")
        
    except Exception as e:
        print(f"⚠️  Tree creation failed: {e}")
        print("   Running in demo mode")
    
    print()
    
    # Create dashboard app
    app, socketio = create_dashboard_app(tree=tree)
    
    print("🚀 Starting dashboard server...")
    print()
    print("📊 Dashboard URL:")
    print("   http://localhost:5000")
    print()
    print("📱 Available Pages:")
    print("   • Dashboard:  http://localhost:5000/")
    print("   • Agent Tree: http://localhost:5000/tree")
    print("   • Execute:    http://localhost:5000/execute")
    print("   • Monitor:    http://localhost:5000/monitor")
    print("   • Messaging:  http://localhost:5000/messaging")
    print("   • Settings:   http://localhost:5000/settings")
    print()
    print("💡 Features:")
    print("   • Real-time system monitoring")
    print("   • Task execution interface")
    print("   • Agent tree visualization")
    print("   • WebSocket live updates")
    print("   • No command line needed!")
    print()
    print("=" * 70)
    print()
    print("Press Ctrl+C to stop the server")
    print()
    
    # Run server
    socketio.run(app, host='0.0.0.0', port=5000, debug=False)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n✅ Dashboard server stopped")
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
