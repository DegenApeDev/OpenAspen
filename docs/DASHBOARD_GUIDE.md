# 🎨 OpenAspen Dashboard Guide

## Overview

The OpenAspen Dashboard is a **Flask-based web interface** for managing your AI agent tree without touching the command line. Perfect for visual management, real-time monitoring, and quick task execution.

## Features

### 🏠 Dashboard Home
- **System Overview**: CPU, memory, disk usage at a glance
- **Quick Execute**: Run tasks instantly from the home page
- **Recent Tasks**: View execution history
- **LLM Providers**: See all configured providers
- **Real-time Charts**: Live system resource monitoring

### 🌲 Agent Tree Visualization
- **Interactive Tree View**: Expand/collapse branches
- **Branch Details**: View agents and their skills
- **Statistics**: Total branches, skills, and providers
- **Visual Hierarchy**: Beautiful tree structure display

### ⚡ Task Execution
- **Natural Language Input**: Type tasks naturally
- **Quick Actions**: Pre-configured task templates
- **Live Results**: See output in real-time
- **Task History**: Access previous executions
- **Copy & Share**: Easy result management

### 📊 System Monitor
- **Real-time Metrics**: CPU, memory, disk, uptime
- **Live Charts**: Historical performance graphs
- **System Info**: Hostname, OS, architecture
- **Top Processes**: See what's running
- **Auto-refresh**: Updates every 2 seconds

### 💬 Messaging Integration
- **Telegram Status**: Check bot configuration
- **WhatsApp Status**: View business API setup
- **Quick Setup**: Step-by-step guides
- **Feature Overview**: See what's possible

### ⚙️ Settings
- **LLM Providers**: View all configured models
- **API Keys**: Manage credentials (view only)
- **Dashboard Settings**: Auto-refresh, notifications
- **Quick Stats**: Version, uptime, task count
- **Documentation Links**: Quick access to help

## Quick Start

### Installation

```bash
# Install dependencies
pip install flask flask-socketio psutil

# Or with poetry
poetry add flask flask-socketio psutil
```

### Running the Dashboard

```bash
# Start the dashboard server
python examples/dashboard_server.py
```

The dashboard will be available at:
- **URL**: http://localhost:5000
- **Port**: 5000 (default)

### First Time Setup

1. **Configure LLM Providers** (in `.env`):
   ```bash
   GROK_API_KEY=your-grok-key
   LMSTUDIO_BASE_URL=http://localhost:1234/v1
   ```

2. **Start Dashboard**:
   ```bash
   python examples/dashboard_server.py
   ```

3. **Open Browser**:
   ```
   http://localhost:5000
   ```

4. **Start Using**:
   - View your agent tree
   - Execute tasks
   - Monitor system
   - Check messaging status

## Pages Overview

### 1. Dashboard (`/`)
**Purpose**: Main overview and quick actions

**Features**:
- System status cards (CPU, Memory, Tasks)
- Quick execute form
- Recent task history
- System resources chart
- LLM provider list

**Use Cases**:
- Quick health check
- Fast task execution
- Monitor at a glance

### 2. Agent Tree (`/tree`)
**Purpose**: Visualize agent hierarchy

**Features**:
- Expandable branch view
- Skill listings per branch
- Provider information
- Tree statistics
- Expand all button

**Use Cases**:
- Understand agent structure
- See available skills
- Check provider assignments
- Plan task routing

### 3. Execute Task (`/execute`)
**Purpose**: Run tasks through agents

**Features**:
- Large text input area
- Quick action buttons
- Live execution status
- Result display with formatting
- Task history sidebar
- Copy/share results

**Use Cases**:
- Execute complex tasks
- Test agent responses
- Save task history
- Share results

### 4. System Monitor (`/monitor`)
**Purpose**: Real-time system performance

**Features**:
- Live metric cards
- CPU/Memory charts
- System information table
- Top processes list
- Auto-refresh (2s)

**Use Cases**:
- Performance monitoring
- Resource optimization
- Troubleshooting
- Capacity planning

### 5. Messaging (`/messaging`)
**Purpose**: Telegram & WhatsApp status

**Features**:
- Platform status badges
- Configuration info
- Setup guides
- Feature overview
- Documentation links

**Use Cases**:
- Check bot status
- Setup messaging
- Learn features
- Troubleshoot issues

### 6. Settings (`/settings`)
**Purpose**: Configuration management

**Features**:
- LLM provider list
- API key display (masked)
- Dashboard preferences
- Quick stats
- Action buttons

**Use Cases**:
- View configuration
- Check providers
- Manage preferences
- Access documentation

## API Endpoints

### System Status
```bash
GET /api/system-status
```
Returns CPU, memory, disk, and system information.

### Execute Task
```bash
POST /api/execute
Content-Type: application/json

{
  "task": "Check BTC price"
}
```
Executes a task through the agent tree.

### Task History
```bash
GET /api/task-history?limit=20
```
Returns recent task execution history.

### Tree Status
```bash
GET /api/tree-status
```
Returns agent tree configuration and status.

### LLM Providers
```bash
GET /api/llm-providers
```
Returns list of configured LLM providers.

### Messaging Status
```bash
GET /api/messaging-status
```
Returns Telegram and WhatsApp configuration status.

## WebSocket Events

### Client → Server

**Request Status**:
```javascript
socket.emit('request_status');
```

### Server → Client

**Connected**:
```javascript
socket.on('connected', (data) => {
  console.log(data.message);
});
```

**Task Completed**:
```javascript
socket.on('task_completed', (data) => {
  // data.task, data.result, data.timestamp
});
```

**Status Update**:
```javascript
socket.on('status_update', (data) => {
  // data.cpu, data.memory, data.uptime
});
```

**Error**:
```javascript
socket.on('error', (data) => {
  console.error(data.message);
});
```

## Customization

### Change Port

Edit `dashboard_server.py`:
```python
socketio.run(app, host='0.0.0.0', port=8080)  # Change to 8080
```

### Custom Theme

Edit `templates/base.html` to modify colors and styling.

### Add Custom Pages

1. Create template in `openaspen/dashboard/templates/`
2. Add route in `openaspen/dashboard/app.py`
3. Add navigation link in `base.html`

### Custom Metrics

Add to `app.py`:
```python
@app.route('/api/custom-metric')
def custom_metric():
    return jsonify({"value": get_custom_data()})
```

## Production Deployment

### Using Gunicorn

```bash
# Install gunicorn
pip install gunicorn

# Run with workers
gunicorn -w 4 -b 0.0.0.0:5000 'examples.dashboard_server:app'
```

### Using Docker

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY . .

RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["python", "examples/dashboard_server.py"]
```

### Nginx Reverse Proxy

```nginx
server {
    listen 80;
    server_name dashboard.example.com;

    location / {
        proxy_pass http://localhost:5000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
    }
}
```

### HTTPS with Let's Encrypt

```bash
# Install certbot
sudo apt install certbot python3-certbot-nginx

# Get certificate
sudo certbot --nginx -d dashboard.example.com
```

## Security

### Authentication

Add basic auth to `app.py`:
```python
from flask_httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()

users = {
    "admin": "password"  # Use environment variables!
}

@auth.verify_password
def verify_password(username, password):
    if username in users and users[username] == password:
        return username

@app.route('/')
@auth.login_required
def index():
    # ...
```

### API Key Protection

```python
API_KEY = os.getenv('DASHBOARD_API_KEY')

@app.before_request
def check_api_key():
    if request.path.startswith('/api/'):
        key = request.headers.get('X-API-Key')
        if key != API_KEY:
            return jsonify({"error": "Unauthorized"}), 401
```

### CORS Configuration

```python
from flask_cors import CORS

CORS(app, resources={
    r"/api/*": {
        "origins": ["https://yourdomain.com"]
    }
})
```

## Troubleshooting

### Dashboard Won't Start

**Error**: `ModuleNotFoundError: No module named 'flask'`
```bash
pip install flask flask-socketio
```

**Error**: `Address already in use`
```bash
# Change port in dashboard_server.py
socketio.run(app, port=5001)  # Use different port
```

### WebSocket Not Connecting

**Issue**: Real-time updates not working

**Solution**:
1. Check browser console for errors
2. Ensure Flask-SocketIO is installed
3. Try different port
4. Check firewall settings

### Charts Not Displaying

**Issue**: Blank chart areas

**Solution**:
1. Check browser console for Chart.js errors
2. Ensure internet connection (CDN)
3. Clear browser cache
4. Try different browser

### Slow Performance

**Issue**: Dashboard is laggy

**Solutions**:
1. Increase auto-refresh interval
2. Reduce chart data points
3. Disable auto-refresh
4. Use production WSGI server (Gunicorn)

## Tips & Tricks

### Keyboard Shortcuts

Add to your templates:
```javascript
document.addEventListener('keydown', (e) => {
    if (e.ctrlKey && e.key === 'e') {
        window.location = '/execute';
    }
});
```

### Dark Mode

Toggle with CSS:
```javascript
document.body.classList.toggle('dark');
```

### Mobile Responsive

The dashboard uses Tailwind CSS and is mobile-responsive by default.

### Bookmarklets

Create quick access:
```javascript
javascript:(function(){window.location='http://localhost:5000/execute'})()
```

## Integration Examples

### With Telegram Bot

```python
# Send dashboard link via Telegram
await bot.send_message(
    chat_id,
    "View dashboard: http://your-server:5000"
)
```

### With Cron Jobs

```bash
# Auto-execute task every hour
0 * * * * curl -X POST http://localhost:5000/api/execute \
  -H "Content-Type: application/json" \
  -d '{"task":"Generate hourly report"}'
```

### With External Monitoring

```bash
# Check dashboard health
curl http://localhost:5000/api/tree-status
```

## Resources

- **GitHub**: https://github.com/DegenApeDev/OpenAspen
- **Flask Docs**: https://flask.palletsprojects.com/
- **Socket.IO**: https://socket.io/docs/
- **Tailwind CSS**: https://tailwindcss.com/docs

## Support

- GitHub Issues: https://github.com/DegenApeDev/OpenAspen/issues
- Documentation: `/docs/`
- Examples: `/examples/`

---

**Built for easy local management. No command line needed!** 🎨🌲
