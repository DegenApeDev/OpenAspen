import uvicorn
from openaspen.server.api import create_app


if __name__ == "__main__":
    app = create_app(config_file="examples/tree.json")

    print("🌲 Starting OpenAspen API Server")
    print("📡 OpenAI-compatible endpoint: http://localhost:8000/v1/chat/completions")
    print("🔍 Tree info: http://localhost:8000/tree/info")
    print("🌿 Visualization: http://localhost:8000/tree/visualize")
    print("💚 Health check: http://localhost:8000/health")

    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
