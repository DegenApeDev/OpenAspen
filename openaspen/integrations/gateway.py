"""
Unified Message Gateway for OpenAspen
Handles messages from Telegram, WhatsApp, and other platforms
"""
import logging
from typing import Optional, Dict, Any
from datetime import datetime
import sqlite3
import asyncio

from openaspen.integrations.base import (
    MessagePlatform,
    IncomingMessage,
    OutgoingMessage,
    CommandParser,
    UserSession,
)
from openaspen.integrations.telegram import TelegramBot
from openaspen.integrations.whatsapp import WhatsAppBot

logger = logging.getLogger(__name__)


class UserDatabase:
    """Simple SQLite database for user sessions and API key mapping"""
    
    def __init__(self, db_path: str = "users.db"):
        self.db_path = db_path
        self._init_db()
    
    def _init_db(self):
        """Initialize database tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id TEXT PRIMARY KEY,
                chat_id TEXT NOT NULL,
                platform TEXT NOT NULL,
                api_key TEXT,
                username TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_activity TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sessions (
                session_id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                current_task TEXT,
                preferences TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        """)
        
        conn.commit()
        conn.close()
    
    def get_user(self, user_id: str, platform: str) -> Optional[Dict[str, Any]]:
        """Get user by ID and platform"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT * FROM users WHERE user_id = ? AND platform = ?",
            (user_id, platform)
        )
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return {
                "user_id": row[0],
                "chat_id": row[1],
                "platform": row[2],
                "api_key": row[3],
                "username": row[4],
                "created_at": row[5],
                "last_activity": row[6]
            }
        return None
    
    def create_or_update_user(self, user_id: str, chat_id: str, platform: str, 
                              username: Optional[str] = None, api_key: Optional[str] = None):
        """Create or update user"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO users (user_id, chat_id, platform, username, api_key, last_activity)
            VALUES (?, ?, ?, ?, ?, ?)
            ON CONFLICT(user_id) DO UPDATE SET
                chat_id = excluded.chat_id,
                username = excluded.username,
                api_key = COALESCE(excluded.api_key, api_key),
                last_activity = excluded.last_activity
        """, (user_id, chat_id, platform, username, api_key, datetime.now()))
        
        conn.commit()
        conn.close()


class MessageGateway:
    """Unified gateway for handling messages from all platforms"""
    
    def __init__(self, tree_executor=None, db_path: str = "users.db"):
        self.tree_executor = tree_executor
        self.db = UserDatabase(db_path)
        self.handlers: Dict[MessagePlatform, Any] = {}
        self.command_parser = CommandParser()
    
    def register_telegram(self, token: str) -> TelegramBot:
        """Register Telegram bot handler"""
        bot = TelegramBot(token, self.tree_executor)
        self.handlers[MessagePlatform.TELEGRAM] = bot
        logger.info("Telegram bot registered")
        return bot
    
    def register_whatsapp(self, token: str, phone_number_id: str) -> WhatsAppBot:
        """Register WhatsApp bot handler"""
        bot = WhatsAppBot(token, phone_number_id, self.tree_executor)
        self.handlers[MessagePlatform.WHATSAPP] = bot
        logger.info("WhatsApp bot registered")
        return bot
    
    async def handle_message(self, platform: MessagePlatform, message: IncomingMessage) -> bool:
        """Handle incoming message from any platform"""
        try:
            # Get or create user
            user = self.db.get_user(message.user_id, platform.value)
            if not user:
                self.db.create_or_update_user(
                    message.user_id,
                    message.chat_id,
                    platform.value,
                    message.username
                )
                user = self.db.get_user(message.user_id, platform.value)
            
            # Parse command
            parsed = self.command_parser.parse(message.text)
            command = parsed["command"]
            args = parsed["args"]
            
            # Route to appropriate handler
            if command == "start":
                response = await self._handle_start(message, user)
            elif command == "help":
                response = await self._handle_help(message, user)
            elif command == "show_tree":
                response = await self._handle_show_tree(message, user)
            elif command == "check_status":
                response = await self._handle_status(message, user)
            elif command == "execute_task":
                response = await self._handle_execute(message, user, args)
            elif command in ["crypto_task", "social_task", "content_task"]:
                response = await self._handle_specialized_task(message, user, command, args)
            else:
                response = await self._handle_execute(message, user, message.text)
            
            # Send response
            await self.send_message(platform, message.chat_id, response)
            return True
            
        except Exception as e:
            logger.error(f"Error handling message: {e}")
            await self.send_message(
                platform,
                message.chat_id,
                f"❌ Error processing your message: {str(e)}"
            )
            return False
    
    async def _handle_start(self, message: IncomingMessage, user: Dict) -> str:
        """Handle start/welcome command"""
        return """
🌲 **Welcome to OpenAspen!**

Your 24/7 AI agent tree is ready.

**Quick Start:**
• Send any task naturally
• Use /tree to see agents
• Use /help for commands

**Example:**
"Check BTC price and sentiment"

Let's go! 🚀
"""
    
    async def _handle_help(self, message: IncomingMessage, user: Dict) -> str:
        """Handle help command"""
        return """
📚 **OpenAspen Commands**

/tree - View agent structure
/status - Check system status
/execute <task> - Run a task

**Or just type naturally:**
"What's BTC doing?"
"Monitor my portfolio"
"Find crypto influencers"

🌲 Powered by OpenAspen
"""
    
    async def _handle_show_tree(self, message: IncomingMessage, user: Dict) -> str:
        """Handle show tree command"""
        if not self.tree_executor:
            return """
🌲 **OpenAspen Tree** (Demo)

📁 **Branches:**
├─ 🤖 crypto_analyzer
├─ 📱 social_manager
└─ ✍️ content_generator

Use /execute to interact!
"""
        
        try:
            branches = getattr(self.tree_executor, 'branches', [])
            tree_text = "🌲 **OpenAspen Tree**\n\n📁 **Branches:**\n"
            
            for branch in branches:
                tree_text += f"├─ 🤖 {branch.name}\n"
                leaves = getattr(branch, 'leaves', [])
                for leaf in leaves:
                    tree_text += f"│  ├─ 🍃 {leaf.name}\n"
            
            return tree_text
        except Exception as e:
            return f"🌲 **OpenAspen Tree**\n\n⚠️ Error: {str(e)}"
    
    async def _handle_status(self, message: IncomingMessage, user: Dict) -> str:
        """Handle status check"""
        return """
📊 **System Status**

🟢 Online - All agents ready
⚡ Active Tasks: 0
🌲 Tree: Healthy

Use /execute to start a task!
"""
    
    async def _handle_execute(self, message: IncomingMessage, user: Dict, task: str) -> str:
        """Handle task execution"""
        if not task or not task.strip():
            return "❌ Please provide a task to execute"
        
        try:
            if not self.tree_executor:
                return f"✅ Task received: {task}\n\n⚠️ Tree executor not configured (demo mode)"
            
            # Execute through OpenAspen tree
            result = await self.tree_executor.execute(task)
            return f"✅ **Task Complete**\n\n{result}"
            
        except Exception as e:
            logger.error(f"Error executing task: {e}")
            return f"❌ **Error**\n\n{str(e)}"
    
    async def _handle_specialized_task(self, message: IncomingMessage, user: Dict, 
                                       task_type: str, args: str) -> str:
        """Handle specialized tasks (crypto, social, content)"""
        task_prefix = task_type.replace("_task", "")
        full_task = f"{task_prefix}: {args}" if args else f"{task_prefix} task"
        return await self._handle_execute(message, user, full_task)
    
    async def send_message(self, platform: MessagePlatform, chat_id: str, 
                          text: str, **kwargs) -> bool:
        """Send message through appropriate platform handler"""
        handler = self.handlers.get(platform)
        if not handler:
            logger.error(f"No handler registered for platform: {platform}")
            return False
        
        message = OutgoingMessage(
            platform=platform,
            chat_id=chat_id,
            text=text,
            **kwargs
        )
        
        return await handler.send_message(message)
    
    async def setup_webhooks(self, base_url: str) -> Dict[str, bool]:
        """Setup webhooks for all registered platforms"""
        results = {}
        
        for platform, handler in self.handlers.items():
            webhook_path = handler.get_webhook_path()
            webhook_url = f"{base_url}{webhook_path}"
            
            success = await handler.setup_webhook(webhook_url)
            results[platform.value] = success
            
            if success:
                logger.info(f"Webhook setup successful for {platform.value}: {webhook_url}")
            else:
                logger.error(f"Webhook setup failed for {platform.value}")
        
        return results
    
    def get_handler(self, platform: MessagePlatform):
        """Get handler for specific platform"""
        return self.handlers.get(platform)
