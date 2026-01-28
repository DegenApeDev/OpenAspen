# 📱 Messaging Integration Guide

## Overview

OpenAspen now supports **24/7 mobile access** via Telegram and WhatsApp! Message your AI agent tree from anywhere in the world and get instant responses.

Perfect for:
- 🌍 On-the-go crypto monitoring (Vancouver, Philippines, Japan)
- 📊 Real-time market alerts
- 📱 Social media management from mobile
- ✍️ Content generation while traveling
- 🤖 Autonomous task execution

## Supported Platforms

### 🤖 Telegram Bot
- **Best for:** Quick interactions, crypto communities, developer-friendly
- **Setup time:** 5 minutes
- **Features:** Inline keyboards, rich formatting, instant notifications
- **Cost:** Free

### 💬 WhatsApp Business
- **Best for:** Business messaging, international reach, client communication
- **Setup time:** 15 minutes (requires Meta Business account)
- **Features:** Rich media, buttons, templates, business profiles
- **Cost:** Free tier available

## Quick Start

### 1. Telegram Bot Setup

#### Step 1: Create Bot with BotFather
```bash
# On Telegram, message @BotFather
/newbot

# Follow prompts:
# - Choose bot name: "OpenAspen Bot"
# - Choose username: "openaspen_yourname_bot"
# - Copy the token provided
```

#### Step 2: Configure Environment
```bash
# Add to .env file
TELEGRAM_BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz
```

#### Step 3: Run Bot
```bash
# Polling mode (development)
python examples/telegram_bot.py

# Webhook mode (production)
python examples/messaging_server.py
```

#### Step 4: Test
```
# On Telegram, message your bot:
/start
/execute Check BTC price and sentiment
```

### 2. WhatsApp Business Setup

#### Step 1: Create Meta Business Account
1. Go to https://developers.facebook.com/apps/
2. Create new app → Business → WhatsApp
3. Get Phone Number ID and Access Token

#### Step 2: Configure Environment
```bash
# Add to .env file
WHATSAPP_TOKEN=EAAxxxxxxxxxxxxxxxxx
WHATSAPP_PHONE_ID=1234567890
WHATSAPP_VERIFY_TOKEN=openaspen_verify_token
```

#### Step 3: Setup Webhook
```bash
# Start server
python examples/messaging_server.py

# In Meta Business Manager:
# - Webhook URL: https://your-domain.com/messaging/whatsapp/webhook
# - Verify Token: openaspen_verify_token
# - Subscribe to: messages
```

#### Step 4: Test
```
# Send WhatsApp message to your business number:
Check BTC price
```

## Available Commands

### Global Commands
```
/start      - Welcome message and quick start
/help       - Show all available commands
/tree       - View agent tree structure
/status     - Check system status
/execute    - Run any task
```

### Specialized Commands
```
/crypto     - Crypto-specific tasks
/social     - Social media tasks
/content    - Content generation
```

### Natural Language
You can also just type naturally:
```
"What's BTC doing?"
"Monitor my portfolio hourly"
"Find crypto influencers for campaign"
"Generate TikTok script about AI"
```

## Example Use Cases

### 1. Crypto Monitoring
```
User: /crypto Monitor BTC and alert if it hits $100k
Bot:  ✅ Monitoring BTC
      Current: $98,234 ↑2.3%
      Alert set for $100k
      [Button: View Chart | Stop Monitoring]
```

### 2. Social Media Management
```
User: /social Create tweet thread about this altcoin
Bot:  🌳 Using social_manager branch...
      ✅ Thread created (5 tweets)
      
      1/ 🚀 Breaking down [ALTCOIN]...
      2/ Key metrics: Market cap...
      [Button: Post Now | Edit | Cancel]
```

### 3. Content Generation
```
User: Generate TikTok script from trending topic
Bot:  ✍️ Using content_generator...
      
      📹 TikTok Script: "AI Revolution"
      Duration: 60s
      Hook: "You won't believe what AI can do now..."
      [Button: Download | Regenerate]
```

### 4. Portfolio Alerts
```
User: Alert me when my portfolio drops 5%
Bot:  ✅ Alert configured
      Current value: $50,000
      Alert threshold: $47,500
      Checking every 5 minutes
```

## Architecture

### Message Flow
```
User Message (Telegram/WhatsApp)
    ↓
Webhook → FastAPI Server
    ↓
MessageGateway → Parse Command
    ↓
OpenAspen Tree → Execute Task
    ↓
Result → Format Response
    ↓
Send Reply (Telegram/WhatsApp)
```

### Components

#### 1. MessageGateway
Unified handler for all platforms:
```python
from openaspen.integrations.gateway import MessageGateway

gateway = MessageGateway(tree_executor=tree)
gateway.register_telegram(token)
gateway.register_whatsapp(token, phone_id)
```

#### 2. Platform Handlers
```python
# Telegram
from openaspen.integrations.telegram import TelegramBot
bot = TelegramBot(token, tree_executor=tree)

# WhatsApp
from openaspen.integrations.whatsapp import WhatsAppBot
bot = WhatsAppBot(token, phone_id, tree_executor=tree)
```

#### 3. FastAPI Endpoints
```
POST /messaging/telegram/webhook  - Telegram webhook
GET  /messaging/whatsapp/webhook  - WhatsApp verification
POST /messaging/whatsapp/webhook  - WhatsApp messages
GET  /messaging/status             - Integration status
POST /messaging/setup-webhooks    - Auto-configure webhooks
```

## Production Deployment

### Docker Compose
```yaml
version: '3.8'

services:
  openaspen:
    build: .
    ports:
      - "8000:8000"
      - "8443:8443"  # HTTPS for Telegram webhook
    environment:
      - TELEGRAM_BOT_TOKEN=${TELEGRAM_BOT_TOKEN}
      - WHATSAPP_TOKEN=${WHATSAPP_TOKEN}
      - GROK_API_KEY=${GROK_API_KEY}
    volumes:
      - ./users.db:/app/users.db
    depends_on:
      - redis
  
  redis:
    image: redis:alpine
    ports:
      - "6379:6379"
```

### HTTPS Setup (Required for Telegram)
```bash
# Using ngrok for development
ngrok http 8000

# Using Let's Encrypt for production
certbot certonly --standalone -d your-domain.com
```

### Environment Variables
```bash
# Production .env
TELEGRAM_BOT_TOKEN=your_production_token
WHATSAPP_TOKEN=your_production_token
WHATSAPP_PHONE_ID=your_phone_id
GROK_API_KEY=your_grok_key
LMSTUDIO_BASE_URL=http://localhost:1234/v1
```

## User Authentication

### API Key Mapping
Users are mapped to API keys in SQLite database:
```python
# Database schema
users (
    user_id TEXT PRIMARY KEY,
    chat_id TEXT,
    platform TEXT,
    api_key TEXT,
    username TEXT,
    created_at TIMESTAMP,
    last_activity TIMESTAMP
)
```

### Setting User API Key
```python
from openaspen.integrations.gateway import UserDatabase

db = UserDatabase()
db.create_or_update_user(
    user_id="telegram_123456",
    chat_id="123456",
    platform="telegram",
    api_key="user_specific_key"
)
```

## Rate Limiting

Implement rate limiting per chat_id:
```python
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter

@router.post("/telegram/webhook")
@limiter.limit("10/minute")
async def telegram_webhook(request: Request):
    # Handle webhook
    pass
```

## Error Handling

### Retry Logic
```python
# Automatic retries for failed messages
async def send_with_retry(message, max_retries=3):
    for attempt in range(max_retries):
        try:
            return await gateway.send_message(message)
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            await asyncio.sleep(2 ** attempt)
```

### User-Friendly Errors
```python
try:
    result = await tree.execute(task)
except Exception as e:
    await send_message(
        chat_id,
        f"❌ Error: {str(e)}\n\n💡 Try:\n- /help for commands\n- Simpler task description"
    )
```

## Testing

### Local Testing (Polling Mode)
```bash
# Run bot in polling mode
python examples/telegram_bot.py

# Test commands in Telegram
/start
/execute Test task
```

### Webhook Testing (ngrok)
```bash
# Start ngrok
ngrok http 8000

# Start server
python examples/messaging_server.py

# Setup webhook
curl -X POST http://localhost:8000/messaging/setup-webhooks \
  -H "Content-Type: application/json" \
  -d '{"base_url": "https://your-ngrok-url.ngrok.io"}'
```

## Monitoring

### Check Integration Status
```bash
curl http://localhost:8000/messaging/status
```

### View Logs
```python
import logging
logging.basicConfig(level=logging.INFO)

# Logs will show:
# - Incoming messages
# - Task executions
# - Errors and retries
```

## Security Best Practices

1. **Webhook Verification**
   - Always verify webhook signatures
   - Use HTTPS in production
   - Validate incoming payloads

2. **User Authentication**
   - Map chat IDs to API keys
   - Implement user allowlists
   - Rate limit per user

3. **Data Privacy**
   - Don't log sensitive data
   - Encrypt API keys in database
   - Clear old sessions regularly

4. **Error Messages**
   - Don't expose internal errors
   - Sanitize user inputs
   - Log security events

## Troubleshooting

### Telegram Issues

**Bot not responding:**
```bash
# Check token
curl https://api.telegram.org/bot<TOKEN>/getMe

# Check webhook
curl https://api.telegram.org/bot<TOKEN>/getWebhookInfo
```

**Webhook not receiving messages:**
- Ensure HTTPS is configured
- Check firewall allows port 8443
- Verify webhook URL is accessible

### WhatsApp Issues

**Webhook verification failing:**
- Check WHATSAPP_VERIFY_TOKEN matches
- Ensure GET endpoint is working
- Verify Meta Business Manager settings

**Messages not sending:**
- Check phone number is verified
- Ensure message templates are approved
- Verify access token is valid

## Advanced Features

### Inline Keyboards (Telegram)
```python
keyboard = [
    [
        InlineKeyboardButton("📊 Chart", callback_data="show_chart"),
        InlineKeyboardButton("🔄 Refresh", callback_data="refresh"),
    ],
    [
        InlineKeyboardButton("🌲 View Tree", callback_data="show_tree"),
    ]
]
```

### Rich Media (WhatsApp)
```python
# Send image
await whatsapp_bot.send_message(OutgoingMessage(
    platform=MessagePlatform.WHATSAPP,
    chat_id=chat_id,
    message_type=MessageType.IMAGE,
    media_url="https://example.com/chart.png",
    text="BTC Price Chart"
))
```

### Scheduled Messages
```python
import schedule

async def send_daily_report():
    report = await tree.execute("Generate daily crypto report")
    await gateway.send_message(
        MessagePlatform.TELEGRAM,
        chat_id,
        report
    )

schedule.every().day.at("09:00").do(send_daily_report)
```

## Mobile-First Tips

### For DEGEN MEDIA Use Cases

**Coffee Shop Workflow:**
```
Morning: "What's trending on crypto Twitter?"
Noon: "Monitor whale wallets, alert on moves >$1M"
Evening: "Generate content calendar for next week"
```

**Travel Mode:**
```
# Set timezone
/execute Set timezone to Asia/Manila

# Auto-responses
/execute Auto-reply to DMs: "Traveling, will respond soon"

# Scheduled posts
/social Schedule tweet thread for 9am PST tomorrow
```

**Quick Checks:**
```
# Just type naturally
"BTC?"
"Portfolio?"
"Trending?"
```

## Resources

- [Telegram Bot API](https://core.telegram.org/bots/api)
- [WhatsApp Business API](https://developers.facebook.com/docs/whatsapp)
- [OpenAspen GitHub](https://github.com/DegenApeDev/OpenAspen)

## Support

Issues? Questions?
- GitHub Issues: https://github.com/DegenApeDev/OpenAspen/issues
- Telegram: @YourSupportBot
- Email: support@example.com

---

**Built for mobile-first AI agent access. Code anywhere, manage everywhere.** 🌲📱
