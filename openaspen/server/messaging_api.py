"""
FastAPI endpoints for messaging integrations
Handles webhooks for Telegram and WhatsApp
"""
from fastapi import APIRouter, Request, HTTPException, Query
from fastapi.responses import PlainTextResponse
import logging
from typing import Optional

from openaspen.integrations.gateway import MessageGateway
from openaspen.integrations.base import MessagePlatform, IncomingMessage

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/messaging", tags=["messaging"])

# Global gateway instance (will be set by server initialization)
_gateway: Optional[MessageGateway] = None


def set_gateway(gateway: MessageGateway):
    """Set the global message gateway instance"""
    global _gateway
    _gateway = gateway


@router.post("/telegram/webhook")
async def telegram_webhook(request: Request):
    """Handle incoming Telegram webhook"""
    if not _gateway:
        raise HTTPException(status_code=503, detail="Message gateway not initialized")
    
    try:
        payload = await request.json()
        logger.debug(f"Telegram webhook payload: {payload}")
        
        # Get Telegram handler
        telegram_handler = _gateway.get_handler(MessagePlatform.TELEGRAM)
        if not telegram_handler:
            raise HTTPException(status_code=503, detail="Telegram handler not registered")
        
        # Parse incoming message
        message = await telegram_handler.handle_webhook(payload)
        
        if message:
            # Process through gateway
            await _gateway.handle_message(MessagePlatform.TELEGRAM, message)
        
        return {"status": "ok"}
        
    except Exception as e:
        logger.error(f"Error processing Telegram webhook: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/whatsapp/webhook")
async def whatsapp_webhook_verify(
    request: Request,
    hub_mode: str = Query(None, alias="hub.mode"),
    hub_verify_token: str = Query(None, alias="hub.verify_token"),
    hub_challenge: str = Query(None, alias="hub.challenge")
):
    """Verify WhatsApp webhook (Meta requirement)"""
    if not _gateway:
        raise HTTPException(status_code=503, detail="Message gateway not initialized")
    
    try:
        whatsapp_handler = _gateway.get_handler(MessagePlatform.WHATSAPP)
        if not whatsapp_handler:
            raise HTTPException(status_code=503, detail="WhatsApp handler not registered")
        
        # Verify webhook
        challenge = await whatsapp_handler.verify_webhook(
            hub_mode, 
            hub_verify_token, 
            hub_challenge
        )
        
        if challenge:
            return PlainTextResponse(challenge)
        else:
            raise HTTPException(status_code=403, detail="Verification failed")
            
    except Exception as e:
        logger.error(f"Error verifying WhatsApp webhook: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/whatsapp/webhook")
async def whatsapp_webhook(request: Request):
    """Handle incoming WhatsApp webhook"""
    if not _gateway:
        raise HTTPException(status_code=503, detail="Message gateway not initialized")
    
    try:
        payload = await request.json()
        logger.debug(f"WhatsApp webhook payload: {payload}")
        
        # Get WhatsApp handler
        whatsapp_handler = _gateway.get_handler(MessagePlatform.WHATSAPP)
        if not whatsapp_handler:
            raise HTTPException(status_code=503, detail="WhatsApp handler not registered")
        
        # Parse incoming message
        message = await whatsapp_handler.handle_webhook(payload)
        
        if message:
            # Process through gateway
            await _gateway.handle_message(MessagePlatform.WHATSAPP, message)
        
        return {"status": "ok"}
        
    except Exception as e:
        logger.error(f"Error processing WhatsApp webhook: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/status")
async def messaging_status():
    """Get messaging integration status"""
    if not _gateway:
        return {
            "status": "not_initialized",
            "platforms": []
        }
    
    platforms = []
    for platform, handler in _gateway.handlers.items():
        platforms.append({
            "platform": platform.value,
            "status": "active",
            "webhook_path": handler.get_webhook_path()
        })
    
    return {
        "status": "active",
        "platforms": platforms,
        "tree_executor": _gateway.tree_executor is not None
    }


@router.post("/setup-webhooks")
async def setup_webhooks(base_url: str):
    """Setup webhooks for all platforms"""
    if not _gateway:
        raise HTTPException(status_code=503, detail="Message gateway not initialized")
    
    try:
        results = await _gateway.setup_webhooks(base_url)
        return {
            "status": "completed",
            "results": results
        }
    except Exception as e:
        logger.error(f"Error setting up webhooks: {e}")
        raise HTTPException(status_code=500, detail=str(e))
