# 🚀 Messaging Integration - Quick Start

Get your OpenAspen agent tree accessible via Telegram or WhatsApp in **under 10 minutes**.

## 📱 Telegram Bot (5 Minutes)

### Step 1: Get Bot Token
1. Open Telegram and message [@BotFather](https://t.me/botfather)
2. Send `/newbot`
3. Choose a name: `OpenAspen Bot`
4. Choose username: `openaspen_yourname_bot`
5. Copy the token (looks like: `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`)

### Step 2: Configure
```bash
# Add to .env file
echo "TELEGRAM_BOT_TOKEN=your-token-here" >> .env
```

### Step 3: Install Dependencies
```bash
pip install python-telegram-bot
```

### Step 4: Run
```bash
python examples/telegram_bot.py
```

### Step 5: Test
Open Telegram, find your bot, and send:
```
/start
/execute Check BTC price
```

**Done!** 🎉 Your bot is now running.

## 💬 WhatsApp Bot (15 Minutes)

### Step 1: Create Meta Business Account
1. Go to [Meta for Developers](https://developers.facebook.com/apps/)
2. Click "Create App" → "Business" → "WhatsApp"
3. Complete setup wizard

### Step 2: Get Credentials
1. In WhatsApp settings, find:
   - **Access Token** (starts with `EAA...`)
   - **Phone Number ID** (numeric)
2. Create a verify token: `openaspen_verify_123`

### Step 3: Configure
```bash
# Add to .env file
WHATSAPP_TOKEN=EAAxxxxxxxxx
WHATSAPP_PHONE_ID=1234567890
WHATSAPP_VERIFY_TOKEN=openaspen_verify_123
```

### Step 4: Deploy Server
```bash
# For development (use ngrok)
ngrok http 8000

# Start server
python examples/messaging_server.py
```

### Step 5: Setup Webhook
1. In Meta Business Manager → WhatsApp → Configuration
2. Set webhook URL: `https://your-ngrok-url.ngrok.io/messaging/whatsapp/webhook`
3. Set verify token: `openaspen_verify_123`
4. Subscribe to: `messages`

### Step 6: Test
Send a WhatsApp message to your business number:
```
Check BTC price
```

**Done!** 🎉 Your WhatsApp bot is live.

## 🎯 Example Commands

### Natural Language (Just Type)
```
What's BTC doing?
Monitor my portfolio
Find crypto influencers
Generate TikTok script
```

### Slash Commands
```
/execute Check BTC price and sentiment
/crypto Monitor whale wallets
/social Create tweet thread about AI
/content Generate blog post
/tree - View agent structure
/status - Check system
```

## 🔥 Use Cases for DEGEN MEDIA

### Morning Routine
```
User: What's trending on crypto Twitter?
Bot:  📊 Top 3 Trending:
      1. Bitcoin ETF news (+2.3k mentions)
      2. Ethereum upgrade (+1.8k)
      3. New altcoin launch (+1.2k)
```

### On-the-Go Monitoring
```
User: Alert me if BTC hits $100k
Bot:  ✅ Alert set
      Current: $98,234
      Target: $100,000
      Checking every 5 min
```

### Content Creation
```
User: Generate TikTok script from latest crypto news
Bot:  ✍️ Script ready:
      
      Hook: "Bitcoin just did something CRAZY..."
      Duration: 60s
      CTA: "Follow for daily crypto updates"
      
      [Download Script]
```

### Social Management
```
User: Schedule tweet for 9am PST tomorrow
Bot:  📅 Scheduled:
      Time: 9:00 AM PST (Jan 28)
      Content: [Your tweet]
      
      [Edit | Cancel | Post Now]
```

## 🌍 Mobile-First Features

### Timezone Support
```
/execute Set timezone to Asia/Manila
```

### Auto-Responses
```
/execute Auto-reply: "Traveling, will respond in 2 hours"
```

### Scheduled Tasks
```
/execute Send daily crypto report at 9am
```

### Quick Checks
```
# Just type the ticker
BTC?
ETH?
Portfolio?
```

## 🚀 Production Deployment

### Using Docker
```bash
docker-compose up -d
```

### Using PM2
```bash
pm2 start examples/messaging_server.py --name openaspen-bot
pm2 save
```

### HTTPS (Required for Telegram)
```bash
# Development
ngrok http 8000

# Production
certbot certonly --standalone -d your-domain.com
```

## 📊 Monitoring

### Check Status
```bash
curl http://localhost:8000/messaging/status
```

### View Logs
```bash
tail -f logs/openaspen.log
```

## 🛠️ Troubleshooting

### Bot Not Responding (Telegram)
```bash
# Check token
curl https://api.telegram.org/bot<TOKEN>/getMe

# Check webhook
curl https://api.telegram.org/bot<TOKEN>/getWebhookInfo
```

### Webhook Issues (WhatsApp)
- Ensure HTTPS is configured
- Check verify token matches
- Verify phone number is active

### Common Errors
```
Error: "Module not found"
Fix: pip install python-telegram-bot

Error: "Webhook verification failed"
Fix: Check WHATSAPP_VERIFY_TOKEN matches in both .env and Meta settings

Error: "ChromaDB import error"
Fix: This is expected on Python 3.14, bot will run in demo mode
```

## 💡 Pro Tips

### For Coffee Shop Work
- Use Telegram for quick checks
- Set up auto-responses when busy
- Schedule posts for later

### For Travel
- Set timezone to current location
- Use WhatsApp for business contacts
- Enable push notifications

### For Team Collaboration
- Share bot with team members
- Set up different API keys per user
- Use groups for team updates

## 📚 Next Steps

- [Full Documentation](./MESSAGING_INTEGRATION.md)
- [Advanced Features](./MESSAGING_INTEGRATION.md#advanced-features)
- [Security Best Practices](./MESSAGING_INTEGRATION.md#security-best-practices)

## 🆘 Support

- GitHub Issues: https://github.com/DegenApeDev/OpenAspen/issues
- Documentation: https://github.com/DegenApeDev/OpenAspen/tree/main/docs

---

**Built for mobile-first AI. Code from anywhere.** 🌲📱
