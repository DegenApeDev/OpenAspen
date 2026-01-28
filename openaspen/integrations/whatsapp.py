"""
WhatsApp Bot Integration for OpenAspen
Uses Meta WhatsApp Business Cloud API for 24/7 messaging
"""
import logging
from typing import Optional, Dict, Any, List
import aiohttp
import json

from openaspen.integrations.base import (
    MessageHandler as BaseMessageHandler,
    IncomingMessage,
    OutgoingMessage,
    MessagePlatform,
    MessageType,
)

logger = logging.getLogger(__name__)


class WhatsAppBot(BaseMessageHandler):
    """WhatsApp bot handler using Meta Cloud API"""
    
    def __init__(self, token: str, phone_number_id: str, tree_executor=None):
        super().__init__(token, tree_executor)
        self.phone_number_id = phone_number_id
        self.api_base = "https://graph.facebook.com/v18.0"
        self.verify_token = None
    
    async def send_message(self, message: OutgoingMessage) -> bool:
        """Send a message via WhatsApp"""
        try:
            url = f"{self.api_base}/{self.phone_number_id}/messages"
            headers = {
                "Authorization": f"Bearer {self.token}",
                "Content-Type": "application/json"
            }
            
            # Build message payload
            payload = {
                "messaging_product": "whatsapp",
                "recipient_type": "individual",
                "to": message.chat_id,
            }
            
            # Text message
            if message.message_type == MessageType.TEXT:
                payload["type"] = "text"
                payload["text"] = {"body": message.text}
            
            # Interactive message with buttons
            if message.buttons:
                payload["type"] = "interactive"
                payload["interactive"] = {
                    "type": "button",
                    "body": {"text": message.text},
                    "action": {
                        "buttons": [
                            {
                                "type": "reply",
                                "reply": {
                                    "id": btn.get("data", f"btn_{i}"),
                                    "title": btn.get("text", f"Button {i}")[:20]
                                }
                            }
                            for i, btn in enumerate(message.buttons[:3])  # Max 3 buttons
                        ]
                    }
                }
            
            # Send request
            async with aiohttp.ClientSession() as session:
                async with session.post(url, headers=headers, json=payload) as response:
                    if response.status == 200:
                        logger.info(f"WhatsApp message sent to {message.chat_id}")
                        return True
                    else:
                        error_text = await response.text()
                        logger.error(f"WhatsApp API error: {error_text}")
                        return False
                        
        except Exception as e:
            logger.error(f"Error sending WhatsApp message: {e}")
            return False
    
    async def send_template(self, chat_id: str, template_name: str, language: str = "en_US") -> bool:
        """Send a WhatsApp template message (for business messaging)"""
        try:
            url = f"{self.api_base}/{self.phone_number_id}/messages"
            headers = {
                "Authorization": f"Bearer {self.token}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "messaging_product": "whatsapp",
                "to": chat_id,
                "type": "template",
                "template": {
                    "name": template_name,
                    "language": {"code": language}
                }
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(url, headers=headers, json=payload) as response:
                    return response.status == 200
                    
        except Exception as e:
            logger.error(f"Error sending WhatsApp template: {e}")
            return False
    
    async def handle_webhook(self, payload: Dict[str, Any]) -> Optional[IncomingMessage]:
        """Process incoming WhatsApp webhook payload"""
        try:
            # WhatsApp webhook structure
            entry = payload.get("entry", [{}])[0]
            changes = entry.get("changes", [{}])[0]
            value = changes.get("value", {})
            messages = value.get("messages", [])
            
            if not messages:
                return None
            
            msg = messages[0]
            
            return IncomingMessage(
                platform=MessagePlatform.WHATSAPP,
                chat_id=msg.get("from"),
                user_id=msg.get("from"),
                message_id=msg.get("id"),
                text=msg.get("text", {}).get("body"),
                message_type=MessageType.TEXT,
                metadata={"whatsapp_data": msg}
            )
            
        except Exception as e:
            logger.error(f"Error handling WhatsApp webhook: {e}")
            return None
    
    async def verify_webhook(self, mode: str, token: str, challenge: str) -> Optional[str]:
        """Verify WhatsApp webhook (Meta requirement)"""
        if mode == "subscribe" and token == self.verify_token:
            logger.info("WhatsApp webhook verified")
            return challenge
        return None
    
    async def setup_webhook(self, webhook_url: str) -> bool:
        """Configure WhatsApp webhook via Meta Business Manager"""
        logger.info(f"WhatsApp webhook should be configured manually at: {webhook_url}")
        logger.info("Visit: https://developers.facebook.com/apps/")
        logger.info("Go to: WhatsApp > Configuration > Webhook")
        return True
    
    async def delete_webhook(self) -> bool:
        """Remove WhatsApp webhook (manual process)"""
        logger.info("WhatsApp webhook should be removed manually via Meta Business Manager")
        return True
    
    def get_webhook_path(self) -> str:
        """Get the webhook endpoint path"""
        return "/messaging/whatsapp/webhook"
    
    def set_verify_token(self, token: str):
        """Set the verification token for webhook setup"""
        self.verify_token = token
