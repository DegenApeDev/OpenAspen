"""
Flask Dashboard Application
Main dashboard app with routes and views
"""
from flask import Flask, render_template, jsonify, request, redirect, url_for
from flask_socketio import SocketIO, emit
import os
import asyncio
from datetime import datetime
from typing import Optional

from openaspen import OpenAspenTree
from openaspen.llm.providers import create_llm_config
from openaspen.skills.system_monitor import SystemMonitor


def create_dashboard_app(tree: Optional[OpenAspenTree] = None, config: dict = None):
    """Create Flask dashboard application"""
    
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('DASHBOARD_SECRET_KEY', 'openaspen-dashboard-secret')
    
    # Initialize SocketIO for real-time updates
    socketio = SocketIO(app, cors_allowed_origins="*")
    
    # Store tree instance
    app.tree = tree
    app.config.update(config or {})
    
    # Task execution history
    app.task_history = []
    
    @app.route('/')
    def index():
        """Dashboard home page"""
        return render_template('index.html', 
                             tree_name=app.tree.name if app.tree else "Not Configured",
                             timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    
    @app.route('/tree')
    def tree_view():
        """Tree structure visualization"""
        if not app.tree:
            return render_template('tree.html', tree_data=None, error="Tree not configured")
        
        # Build tree structure
        tree_data = {
            "name": app.tree.name,
            "branches": []
        }
        
        for branch in app.tree.branches:
            branch_data = {
                "name": branch.name,
                "description": branch.description,
                "llm_provider": branch.llm_provider,
                "leaves": []
            }
            
            for leaf in branch.leaves:
                branch_data["leaves"].append({
                    "name": leaf.name,
                    "description": leaf.description,
                    "function": leaf.function.__name__ if hasattr(leaf.function, '__name__') else "unknown"
                })
            
            tree_data["branches"].append(branch_data)
        
        return render_template('tree.html', tree_data=tree_data)
    
    @app.route('/execute')
    def execute_page():
        """Task execution page"""
        return render_template('execute.html')
    
    @app.route('/api/execute', methods=['POST'])
    def execute_task():
        """Execute a task via API"""
        data = request.json
        task = data.get('task', '')
        
        if not task:
            return jsonify({"error": "No task provided"}), 400
        
        try:
            # Execute task asynchronously or use demo mode
            if app.tree:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                result = loop.run_until_complete(app.tree.execute(task))
                loop.close()
            else:
                # Demo mode - simulate execution
                result = f"""🌲 OpenAspen Demo Mode

Task: {task}

⚠️ Tree not fully configured (ChromaDB compatibility issue with Python 3.14)

Demo Response:
This is a simulated response. In production mode with a configured tree:
- Your task would be routed to the appropriate agent branch
- The LLM (Grok or LM Studio) would process the request
- Results would be returned with full context

To enable full functionality:
1. Use Python 3.11 or 3.12 for ChromaDB support, OR
2. Configure tree without RAG, OR
3. Use the messaging integration (Telegram/WhatsApp) which works in demo mode

Your LLM providers are configured and ready:
- Grok (grok-4-1-fast-reasoning)
- LM Studio (local)"""
            
            # Store in history
            task_record = {
                "task": task,
                "result": result,
                "timestamp": datetime.now().isoformat(),
                "status": "success"
            }
            app.task_history.insert(0, task_record)
            
            # Keep only last 50 tasks
            app.task_history = app.task_history[:50]
            
            # Emit to WebSocket clients
            socketio.emit('task_completed', task_record)
            
            return jsonify({
                "success": True,
                "result": result,
                "timestamp": task_record["timestamp"]
            })
            
        except Exception as e:
            error_record = {
                "task": task,
                "error": str(e),
                "timestamp": datetime.now().isoformat(),
                "status": "error"
            }
            app.task_history.insert(0, error_record)
            
            return jsonify({
                "success": False,
                "error": str(e)
            }), 500
    
    @app.route('/monitor')
    def monitor_page():
        """System monitoring page"""
        return render_template('monitor.html')
    
    @app.route('/api/system-status')
    def system_status():
        """Get current system status"""
        try:
            system_info = SystemMonitor.get_system_info()
            cpu_info = SystemMonitor.get_cpu_info()
            memory_info = SystemMonitor.get_memory_info()
            disk_info = SystemMonitor.get_disk_info()
            
            return jsonify({
                "system": system_info,
                "cpu": cpu_info,
                "memory": memory_info,
                "disk": disk_info,
                "timestamp": datetime.now().isoformat()
            })
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    @app.route('/api/tree-status')
    def tree_status():
        """Get tree status"""
        if not app.tree:
            return jsonify({
                "configured": False,
                "error": "Tree not configured"
            })
        
        return jsonify({
            "configured": True,
            "name": app.tree.name,
            "branch_count": len(app.tree.branches),
            "branches": [
                {
                    "name": b.name,
                    "leaf_count": len(b.leaves),
                    "llm_provider": b.llm_provider
                }
                for b in app.tree.branches
            ]
        })
    
    @app.route('/api/task-history')
    def task_history():
        """Get task execution history"""
        limit = request.args.get('limit', 20, type=int)
        return jsonify({
            "tasks": app.task_history[:limit],
            "total": len(app.task_history)
        })
    
    @app.route('/settings')
    def settings_page():
        """Settings and configuration page"""
        return render_template('settings.html', config=app.config)
    
    @app.route('/api/llm-providers')
    def llm_providers():
        """Get available LLM providers"""
        if not app.tree:
            return jsonify({"providers": []})
        
        providers = []
        for name, config in app.tree.llm_router.configs.items():
            providers.append({
                "name": name,
                "model": config.model,
                "provider": config.provider,
                "cost_per_1k": config.cost_per_1k_tokens,
                "speed_score": config.speed_score
            })
        
        return jsonify({"providers": providers})
    
    @app.route('/messaging')
    def messaging_page():
        """Messaging integration status page"""
        return render_template('messaging.html')
    
    @app.route('/api/messaging-status')
    def messaging_status():
        """Get messaging integration status"""
        telegram_configured = bool(os.getenv('TELEGRAM_BOT_TOKEN'))
        whatsapp_configured = bool(os.getenv('WHATSAPP_TOKEN') and os.getenv('WHATSAPP_PHONE_ID'))
        
        return jsonify({
            "telegram": {
                "configured": telegram_configured,
                "status": "active" if telegram_configured else "not_configured"
            },
            "whatsapp": {
                "configured": whatsapp_configured,
                "status": "active" if whatsapp_configured else "not_configured"
            }
        })
    
    # WebSocket events
    @socketio.on('connect')
    def handle_connect():
        """Handle client connection"""
        emit('connected', {'message': 'Connected to OpenAspen Dashboard'})
    
    @socketio.on('request_status')
    def handle_status_request():
        """Handle status request via WebSocket"""
        try:
            system_info = SystemMonitor.get_system_info()
            cpu_info = SystemMonitor.get_cpu_info()
            memory_info = SystemMonitor.get_memory_info()
            
            emit('status_update', {
                "cpu": cpu_info.get('usage_percent', 0),
                "memory": memory_info.get('percent_used', 0),
                "uptime": system_info.get('uptime_hours', 0),
                "timestamp": datetime.now().isoformat()
            })
        except Exception as e:
            emit('error', {'message': str(e)})
    
    return app, socketio
