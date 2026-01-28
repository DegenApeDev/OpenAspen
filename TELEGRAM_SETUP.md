# 🤖 OpenAspen Telegram Bot Setup

Control your OpenAspen AI agent tree directly from Telegram - 24/7 mobile access to your agents!

## 📋 Prerequisites

1. **Telegram Account** - Download Telegram app
2. **LM Studio Running** - Local LLM on `http://localhost:1234`
3. **OpenAspen Installed** - Virtual environment set up

## 🚀 Quick Setup (5 Minutes)

### Step 1: Create Your Bot

1. Open Telegram and search for **@BotFather**
2. Send `/newbot` to create a new bot
3. Choose a name (e.g., "My OpenAspen Agent")
4. Choose a username (e.g., "myopenaspen_bot")
5. **Copy the token** - looks like: `1234567890:ABCdefGHIjklMNOpqrsTUVwxyz`

### Step 2: Add Token to .env

Add your bot token to `.env` file:

```bash
# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
```

### Step 3: Install Telegram Dependency

```fish
source venv/bin/activate.fish
pip install python-telegram-bot
```

### Step 4: Start the Bot

```fish
source venv/bin/activate.fish
python start_telegram_bot.py
```

You'll see:
```
============================================================
🤖 OpenAspen Telegram Bot
============================================================

✅ Telegram token found
✅ LM Studio server detected
✅ python-telegram-bot installed

🌲 Building OpenAspen tree...
🤖 Starting Telegram bot...

============================================================
✅ Telegram Bot Running!
============================================================

📱 Your bot is ready to receive messages
```

### Step 5: Talk to Your Bot

1. Open Telegram
2. Search for your bot username (e.g., `@myopenaspen_bot`)
3. Click **Start**
4. Send messages!

## 💬 How to Use

### Available Commands

```
/start  - Welcome message and quick start
/help   - Show all commands
/tree   - View your agent structure
/status - Check system status
```

### Natural Language Queries

Just send messages naturally - no commands needed!

**Examples:**
```
What is Python programming?
Search for latest AI news
Tell me about quantum computing
What's the weather like?
```

The bot will:
1. Receive your message
2. Route to the appropriate agent/tool
3. Execute using LM Studio
4. Send results back to you

## 🌲 What's Running

When you start the bot, it creates an OpenAspen tree with:

```
🌲 telegram_tree
├── 🌿 research (LM Studio)
│   ├── 🍃 web_search (DuckDuckGo)
│   └── 🍃 wiki_search (Wikipedia)
└── 🌿 utils (LM Studio)
    └── 🍃 echo (test tool)
```

## 📱 Example Conversation

```
You: /start

Bot: 🌲 Welcome to OpenAspen!

Your 24/7 AI agent tree is ready.

Quick Start:
• Send any task naturally
• Use /tree to see agents
• Use /help for commands

Example:
"Check BTC price and sentiment"

Let's go! 🚀

---

You: What is machine learning?

Bot: 📚 Wikipedia: machine learning

Machine learning is a field of study in artificial 
intelligence concerned with the development and study 
of statistical algorithms that can learn from data...

---

You: /tree

Bot: 🌲 OpenAspen Tree

📁 Branches:
├─ 🤖 research
│  ├─ 🍃 web_search
│  └─ 🍃 wiki_search
└─ 🤖 utils
   └─ 🍃 echo
```

## 🔧 Advanced Configuration

### Add Cloud LLMs (Optional)

Add to `.env` for faster cloud inference:

```bash
# Grok (primary cloud option)
GROK_API_KEY=xai-your-key-here

# OpenAI (optional premium)
OPENAI_API_KEY=sk-your-key-here
```

The bot will automatically use them if available!

### Customize Your Tree

Edit `start_telegram_bot.py` to add your own branches and tools:

```python
# Add a custom branch
crypto = tree.add_branch(
    "crypto",
    description="Cryptocurrency analysis",
    llm_provider="lmstudio",
)

# Add a custom tool
async def check_btc_price(query: str, **kwargs):
    # Your custom logic here
    return "BTC: $45,000"

await tree.spawn_leaf(crypto, "btc_price", check_btc_price, "Check BTC price")
```

### Multi-User Support

The bot automatically:
- Tracks users in SQLite database (`users.db`)
- Maintains separate sessions per user
- Logs activity timestamps

## 🛡️ Security & Privacy

### Best Practices

1. **Keep token secret** - Never share your bot token
2. **Private bot** - Don't add to public groups initially
3. **Rate limiting** - Consider adding rate limits for production
4. **User validation** - Add user whitelist if needed

### Add User Whitelist (Optional)

Edit `start_telegram_bot.py`:

```python
ALLOWED_USERS = [123456789, 987654321]  # Telegram user IDs

async def check_user(user_id: int):
    if user_id not in ALLOWED_USERS:
        return False
    return True
```

## 🐛 Troubleshooting

### Bot doesn't respond

**Check:**
```fish
# 1. Is the bot script running?
ps aux | grep telegram_bot

# 2. Is LM Studio running?
curl http://localhost:1234/v1/models

# 3. Check logs for errors
# Look at terminal output where bot is running
```

### "python-telegram-bot not installed"

```fish
source venv/bin/activate.fish
pip install python-telegram-bot
```

### "TELEGRAM_BOT_TOKEN not found"

Check your `.env` file has:
```bash
TELEGRAM_BOT_TOKEN=your-actual-token-here
```

### Bot responds slowly

**Options:**
1. Use a faster LM Studio model (e.g., Mistral 7B instead of 13B)
2. Add Grok API key for cloud inference
3. Reduce `max_results` in search tools

## 📊 Monitoring

### View Bot Activity

The bot logs all activity to console:

```
INFO - User 123456789 sent: What is AI?
INFO - Executing query: What is AI?
INFO - Response sent to user 123456789
```

### Check User Database

```fish
sqlite3 users.db "SELECT * FROM users;"
```

## 🚀 Production Deployment

### Run as Background Service

Using systemd (Linux):

```ini
# /etc/systemd/system/openaspen-telegram.service
[Unit]
Description=OpenAspen Telegram Bot
After=network.target

[Service]
Type=simple
User=your-user
WorkingDirectory=/path/to/OpenAspen
Environment="PATH=/path/to/OpenAspen/venv/bin"
ExecStart=/path/to/OpenAspen/venv/bin/python start_telegram_bot.py
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable openaspen-telegram
sudo systemctl start openaspen-telegram
```

### Using Docker

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY . .

RUN python -m venv venv && \
    . venv/bin/activate && \
    pip install -e . && \
    pip install python-telegram-bot duckduckgo-search wikipedia

CMD ["venv/bin/python", "start_telegram_bot.py"]
```

## 💡 Tips & Tricks

### 1. Quick Commands

Set up BotFather commands for easy access:
```
/setcommands
start - Start the bot
help - Show help
tree - View agent structure
status - Check status
```

### 2. Rich Formatting

The bot supports Telegram markdown:
- **Bold**: `**text**`
- *Italic*: `*text*`
- Code: `` `code` ``

### 3. Inline Queries (Advanced)

Enable inline mode in BotFather to query from any chat:
```
@your_bot What is AI?
```

## 📚 Next Steps

1. **Customize your tree** - Add branches for your specific use case
2. **Add more tools** - Integrate APIs, databases, etc.
3. **Set up webhooks** - For production deployment
4. **Add authentication** - User whitelist or API key validation
5. **Monitor usage** - Track queries and optimize performance

---

## 🎯 Summary

**You now have:**
- ✅ Telegram bot connected to OpenAspen
- ✅ 24/7 mobile access to your AI agents
- ✅ Natural language interface
- ✅ Zero API keys required (with LM Studio)
- ✅ Multi-user support
- ✅ Web search & Wikipedia integration

**Cost**: $0/month with LM Studio

**Your AI agent tree is now in your pocket!** 📱🌲
