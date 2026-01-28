"""
Base classes for messaging platform integrations
"""
from abc import ABC, abstractmethod
from enum import Enum
from typing import Optional, Dict, Any, List
from pydantic import BaseModel
from datetime import datetime


class MessagePlatform(str, Enum):
    """Supported messaging platforms"""
    TELEGRAM = "telegram"
    WHATSAPP = "whatsapp"


class MessageType(str, Enum):
    """Types of messages"""
    TEXT = "text"
    IMAGE = "image"
    DOCUMENT = "document"
    AUDIO = "audio"
    VIDEO = "video"
    LOCATION = "location"


class IncomingMessage(BaseModel):
    """Standardized incoming message format"""
    platform: MessagePlatform
    chat_id: str
    user_id: str
    username: Optional[str] = None
    message_id: str
    text: Optional[str] = None
    message_type: MessageType = MessageType.TEXT
    media_url: Optional[str] = None
    timestamp: datetime = None
    metadata: Dict[str, Any] = {}
    
    class Config:
        use_enum_values = True


class OutgoingMessage(BaseModel):
    """Standardized outgoing message format"""
    platform: MessagePlatform
    chat_id: str
    text: Optional[str] = None
    message_type: MessageType = MessageType.TEXT
    media_url: Optional[str] = None
    buttons: Optional[List[Dict[str, str]]] = None
    inline_keyboard: Optional[List[List[Dict[str, str]]]] = None
    parse_mode: Optional[str] = "Markdown"
    reply_to_message_id: Optional[str] = None
    
    class Config:
        use_enum_values = True


class MessageHandler(ABC):
    """Abstract base class for platform-specific message handlers"""
    
    def __init__(self, token: str, tree_executor=None):
        self.token = token
        self.tree_executor = tree_executor
    
    @abstractmethod
    async def send_message(self, message: OutgoingMessage) -> bool:
        """Send a message to the platform"""
        pass
    
    @abstractmethod
    async def handle_webhook(self, payload: Dict[str, Any]) -> Optional[IncomingMessage]:
        """Process incoming webhook payload"""
        pass
    
    @abstractmethod
    async def setup_webhook(self, webhook_url: str) -> bool:
        """Configure webhook for the platform"""
        pass
    
    @abstractmethod
    async def delete_webhook(self) -> bool:
        """Remove webhook configuration"""
        pass
    
    @abstractmethod
    def get_webhook_path(self) -> str:
        """Get the webhook endpoint path"""
        pass


class CommandParser:
    """Parse user commands from messages"""
    
    COMMANDS = {
        "/start": "start",
        "/help": "help",
        "/tree": "show_tree",
        "/execute": "execute_task",
        "/status": "check_status",
        "/crypto": "crypto_task",
        "/social": "social_task",
        "/content": "content_task",
        "/stop": "stop_task",
    }
    
    @classmethod
    def parse(cls, text: str) -> Dict[str, Any]:
        """Parse command from message text"""
        if not text:
            return {"command": "unknown", "args": []}
        
        parts = text.strip().split(maxsplit=1)
        command_text = parts[0].lower()
        args_text = parts[1] if len(parts) > 1 else ""
        
        # Check if it's a known command
        command = cls.COMMANDS.get(command_text, "execute_task")
        
        # If not a command, treat as natural language task
        if not command_text.startswith("/"):
            command = "execute_task"
            args_text = text
        
        return {
            "command": command,
            "raw_command": command_text,
            "args": args_text,
            "is_command": command_text.startswith("/")
        }


class UserSession(BaseModel):
    """Track user session state"""
    user_id: str
    chat_id: str
    platform: MessagePlatform
    api_key: Optional[str] = None
    current_task: Optional[str] = None
    last_activity: datetime = None
    preferences: Dict[str, Any] = {}
    
    class Config:
        use_enum_values = True
