# 🚀 OpenAspen Server - Quick Start Guide

Run OpenAspen as a production API server with **zero API keys required**.

## Start the Server (3 Options)

### Option 1: LM Studio Only (Zero API Keys - Recommended)
```fish
source venv/bin/activate.fish
python start_server.py
```

**Requirements**: LM Studio running on `http://localhost:1234`

### Option 2: LM Studio + Grok (Primary Cloud)
```fish
# Add to .env first:
# GROK_API_KEY=xai-your-key-here

source venv/bin/activate.fish
python start_server.py --with-grok
```

### Option 3: LM Studio + OpenAI (Optional Premium)
```fish
# Add to .env first:
# OPENAI_API_KEY=sk-your-key-here

source venv/bin/activate.fish
python start_server.py --with-openai
```

### Option 4: All LLMs
```fish
source venv/bin/activate.fish
python start_server.py --with-grok --with-openai
```

## Server Options

```bash
python start_server.py [OPTIONS]

Options:
  --host HOST        Host to bind to (default: 0.0.0.0)
  --port PORT        Port to bind to (default: 8000)
  --with-grok        Enable Grok (requires GROK_API_KEY)
  --with-openai      Enable OpenAI (requires OPENAI_API_KEY)
  --reload           Enable auto-reload for development
```

## API Endpoints

Once running, the server provides:

### Main Endpoints
- `GET /` - Server info and status
- `GET /health` - Health check
- `GET /docs` - Interactive API documentation (Swagger UI)

### OpenAI-Compatible Endpoints
- `POST /v1/chat/completions` - Chat completions (OpenAI compatible)
- `GET /v1/models` - List available models

### OpenAspen-Specific Endpoints
- `POST /query` - Direct query execution
- `GET /tree/info` - Tree structure and branches
- `GET /tree/visualize` - ASCII tree visualization

## Example Requests

### 1. Check Server Status
```bash
curl http://localhost:8000/
```

### 2. View Tree Structure
```bash
curl http://localhost:8000/tree/info
```

### 3. Visualize Tree
```bash
curl http://localhost:8000/tree/visualize
```

### 4. Send a Query
```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"query": "What is Python programming?"}'
```

### 5. OpenAI-Compatible Chat
```bash
curl -X POST http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "openaspen",
    "messages": [
      {"role": "user", "content": "Hello!"}
    ]
  }'
```

## Use with OpenAI SDK

The server is OpenAI-compatible, so you can use it with the OpenAI Python SDK:

```python
from openai import OpenAI

# Point to your OpenAspen server
client = OpenAI(
    base_url="http://localhost:8000/v1",
    api_key="not-needed"  # OpenAspen doesn't require API key
)

# Use like normal OpenAI
response = client.chat.completions.create(
    model="openaspen",
    messages=[
        {"role": "user", "content": "What is machine learning?"}
    ]
)

print(response.choices[0].message.content)
```

## Interactive API Docs

Visit `http://localhost:8000/docs` in your browser for interactive API documentation with:
- Try-it-out functionality
- Request/response examples
- Schema definitions

## Server Output

When you start the server, you'll see:

```
============================================================
🌲 OpenAspen API Server
============================================================

Configuration:
  • LM Studio: ✅ (default, no API key)
  • Grok: ❌
  • OpenAI: ❌

✅ LM Studio server detected!

🌲 Building tree...
🌳 Created tree with providers: ['lmstudio']
📊 Setting up branches and tools...
  ✅ Added web_search leaf
  ✅ Added wiki_search leaf
  ✅ Added echo leaf
🌳 Tree setup complete with 2 branches

============================================================
🚀 Server starting...
============================================================

📡 API endpoint: http://0.0.0.0:8000
📚 Docs: http://0.0.0.0:8000/docs
🌳 Tree info: http://0.0.0.0:8000/tree/info

Example requests:
  curl http://localhost:8000/
  curl http://localhost:8000/tree/visualize
  curl -X POST http://localhost:8000/query -H "Content-Type: application/json" -d '{"query": "Hello!"}'

Press Ctrl+C to stop
============================================================
```

## Production Deployment

### Using systemd (Linux)

Create `/etc/systemd/system/openaspen.service`:

```ini
[Unit]
Description=OpenAspen API Server
After=network.target

[Service]
Type=simple
User=your-user
WorkingDirectory=/path/to/OpenAspen
Environment="PATH=/path/to/OpenAspen/venv/bin"
ExecStart=/path/to/OpenAspen/venv/bin/python start_server.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Then:
```bash
sudo systemctl daemon-reload
sudo systemctl enable openaspen
sudo systemctl start openaspen
sudo systemctl status openaspen
```

### Using Docker

Create `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY . .

RUN python -m venv venv && \
    . venv/bin/activate && \
    pip install -e . --no-deps && \
    pip install langchain langgraph langchain-community faiss-cpu \
        pydantic pydantic-settings fastapi uvicorn[standard] \
        click python-dotenv aiohttp psutil flask flask-socketio \
        duckduckgo-search wikipedia

EXPOSE 8000

CMD ["venv/bin/python", "start_server.py", "--host", "0.0.0.0"]
```

Build and run:
```bash
docker build -t openaspen .
docker run -p 8000:8000 openaspen
```

### Using nginx (Reverse Proxy)

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## Monitoring

### Check Server Health
```bash
curl http://localhost:8000/health
```

### View Logs
The server logs to stdout. In production, redirect to a file:
```bash
python start_server.py > server.log 2>&1
```

## Troubleshooting

### Server won't start
```bash
# Check if port is already in use
lsof -i :8000

# Use a different port
python start_server.py --port 8001
```

### LM Studio not detected
```bash
# Check if LM Studio is running
curl http://localhost:1234/v1/models

# If not, start LM Studio and load a model
```

### Import errors
```bash
# Reinstall dependencies
source venv/bin/activate.fish
pip install -e . --no-deps
pip install langchain langgraph langchain-community faiss-cpu \
    pydantic pydantic-settings fastapi uvicorn[standard] \
    click python-dotenv aiohttp psutil flask flask-socketio
```

## Development Mode

Run with auto-reload for development:
```bash
python start_server.py --reload
```

Changes to code will automatically restart the server.

## Next Steps

1. **Start the server**: `python start_server.py`
2. **Test endpoints**: `curl http://localhost:8000/`
3. **View docs**: Open `http://localhost:8000/docs` in browser
4. **Integrate**: Use OpenAI SDK or direct HTTP requests
5. **Deploy**: Use systemd, Docker, or your preferred method

---

**Your AI agent tree is now running as a production API server!** 🎉

**Cost**: $0/month with LM Studio  
**API Keys**: 0 required  
**Compatibility**: OpenAI SDK compatible
