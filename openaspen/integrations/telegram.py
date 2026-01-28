"""
Telegram Bot Integration for OpenAspen
Enables 24/7 mobile access via Telegram messaging
"""
import logging
from typing import Optional, Dict, Any, List
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters,
    ContextTypes,
)
from telegram.constants import ParseMode
import aiohttp

from openaspen.integrations.base import (
    MessageHandler as BaseMessageHandler,
    IncomingMessage,
    OutgoingMessage,
    MessagePlatform,
    MessageType,
    CommandParser,
)

logger = logging.getLogger(__name__)


class TelegramBot(BaseMessageHandler):
    """Telegram bot handler for OpenAspen"""
    
    def __init__(self, token: str, tree_executor=None):
        super().__init__(token, tree_executor)
        self.application = None
        self.webhook_url = None
    
    async def initialize(self):
        """Initialize the Telegram bot application"""
        self.application = Application.builder().token(self.token).build()
        
        # Add command handlers
        self.application.add_handler(CommandHandler("start", self._handle_start))
        self.application.add_handler(CommandHandler("help", self._handle_help))
        self.application.add_handler(CommandHandler("tree", self._handle_tree))
        self.application.add_handler(CommandHandler("execute", self._handle_execute))
        self.application.add_handler(CommandHandler("status", self._handle_status))
        self.application.add_handler(CommandHandler("crypto", self._handle_crypto))
        self.application.add_handler(CommandHandler("social", self._handle_social))
        self.application.add_handler(CommandHandler("content", self._handle_content))
        
        # Handle inline keyboard callbacks
        self.application.add_handler(CallbackQueryHandler(self._handle_callback))
        
        # Handle all other messages
        self.application.add_handler(
            MessageHandler(filters.TEXT & ~filters.COMMAND, self._handle_message)
        )
        
        logger.info("Telegram bot initialized")
    
    async def _handle_start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command"""
        welcome_text = """
🌲 **Welcome to OpenAspen!**

I'm your 24/7 AI agent tree, ready to help with:
• 📊 Crypto monitoring & analysis
• 📱 Social media management
• ✍️ Content generation
• 🤖 Custom AI tasks

**Quick Commands:**
/tree - View agent structure
/execute <task> - Run a task
/status - Check current tasks
/help - Show all commands

**Examples:**
`/execute Check BTC price and sentiment`
`/crypto Monitor whale wallets`
`/social Find trending topics`

Let's get started! 🚀
"""
        await update.message.reply_text(welcome_text, parse_mode=ParseMode.MARKDOWN)
    
    async def _handle_help(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command"""
        help_text = """
📚 **OpenAspen Commands**

**General:**
/start - Welcome message
/help - This help message
/tree - View agent tree structure
/status - Check task status

**Execute Tasks:**
/execute <task> - Run any task
/crypto <task> - Crypto-specific tasks
/social <task> - Social media tasks
/content <task> - Content generation

**Examples:**
`/execute Analyze BTC market sentiment`
`/crypto Alert me when BTC hits $100k`
`/social Create tweet thread about AI`
`/content Generate TikTok script`

**Natural Language:**
You can also just type naturally:
"What's BTC doing?"
"Monitor my portfolio"
"Find crypto influencers"

🌲 Powered by OpenAspen Tree Architecture
"""
        await update.message.reply_text(help_text, parse_mode=ParseMode.MARKDOWN)
    
    async def _handle_tree(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /tree command - show agent structure"""
        if not self.tree_executor:
            await update.message.reply_text("❌ Tree executor not configured")
            return
        
        try:
            # Get tree structure
            tree_info = await self._get_tree_structure()
            
            # Create inline keyboard for navigation
            keyboard = [
                [
                    InlineKeyboardButton("🔄 Refresh", callback_data="tree_refresh"),
                    InlineKeyboardButton("📊 Status", callback_data="tree_status"),
                ],
                [
                    InlineKeyboardButton("⚡ Execute Task", callback_data="tree_execute"),
                ]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await update.message.reply_text(
                tree_info,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=reply_markup
            )
        except Exception as e:
            logger.error(f"Error showing tree: {e}")
            await update.message.reply_text(f"❌ Error: {str(e)}")
    
    async def _handle_execute(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /execute command"""
        if not context.args:
            await update.message.reply_text(
                "❌ Please provide a task.\n\nExample: `/execute Check BTC price`",
                parse_mode=ParseMode.MARKDOWN
            )
            return
        
        task = " ".join(context.args)
        await self._execute_task(update, task)
    
    async def _handle_crypto(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /crypto command"""
        task = " ".join(context.args) if context.args else "crypto analysis"
        await self._execute_task(update, f"crypto: {task}")
    
    async def _handle_social(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /social command"""
        task = " ".join(context.args) if context.args else "social media task"
        await self._execute_task(update, f"social: {task}")
    
    async def _handle_content(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /content command"""
        task = " ".join(context.args) if context.args else "content generation"
        await self._execute_task(update, f"content: {task}")
    
    async def _handle_status(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /status command"""
        status_text = """
📊 **System Status**

🟢 **Online** - All agents ready
⚡ **Active Tasks:** 0
🌲 **Tree:** Healthy

**Recent Activity:**
• No recent tasks

Use /execute to start a new task!
"""
        await update.message.reply_text(status_text, parse_mode=ParseMode.MARKDOWN)
    
    async def _handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle regular text messages (natural language)"""
        text = update.message.text
        await self._execute_task(update, text)
    
    async def _handle_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle inline keyboard button callbacks"""
        query = update.callback_query
        await query.answer()
        
        if query.data == "tree_refresh":
            tree_info = await self._get_tree_structure()
            await query.edit_message_text(tree_info, parse_mode=ParseMode.MARKDOWN)
        elif query.data == "tree_status":
            await query.edit_message_text("📊 Status: All systems operational")
        elif query.data == "tree_execute":
            await query.edit_message_text("Use /execute <task> to run a task")
    
    async def _execute_task(self, update: Update, task: str):
        """Execute a task through the tree"""
        # Send "processing" message
        processing_msg = await update.message.reply_text(
            f"🌳 Processing: {task[:50]}...\n⏳ Please wait...",
            parse_mode=ParseMode.MARKDOWN
        )
        
        try:
            if not self.tree_executor:
                result = f"✅ Task received: {task}\n\n⚠️ Tree executor not configured (demo mode)"
            else:
                # Execute through OpenAspen tree
                result = await self.tree_executor.execute(task)
            
            # Format result
            response = f"✅ **Task Complete**\n\n{result}"
            
            # Add action buttons
            keyboard = [
                [
                    InlineKeyboardButton("🔄 Run Again", callback_data=f"rerun_{task[:20]}"),
                    InlineKeyboardButton("🌲 View Tree", callback_data="tree_refresh"),
                ]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            # Update message with result
            await processing_msg.edit_text(
                response,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=reply_markup
            )
            
        except Exception as e:
            logger.error(f"Error executing task: {e}")
            await processing_msg.edit_text(
                f"❌ **Error**\n\n{str(e)}\n\nTry /help for command examples",
                parse_mode=ParseMode.MARKDOWN
            )
    
    async def _get_tree_structure(self) -> str:
        """Get formatted tree structure"""
        if not self.tree_executor:
            return """
🌲 **OpenAspen Tree** (Demo Mode)

📁 **Branches:**
├─ 🤖 crypto_analyzer
│  ├─ 📊 price_checker
│  └─ 😊 sentiment_analyzer
├─ 📱 social_manager
│  ├─ 🐦 twitter_poster
│  └─ 📸 content_scheduler
└─ ✍️ content_generator
   ├─ 📝 script_writer
   └─ 🎨 image_generator

Use /execute to interact with agents!
"""
        
        try:
            # Get actual tree structure from executor
            branches = getattr(self.tree_executor, 'branches', [])
            tree_text = "🌲 **OpenAspen Tree**\n\n📁 **Branches:**\n"
            
            for branch in branches:
                tree_text += f"├─ 🤖 {branch.name}\n"
                leaves = getattr(branch, 'leaves', [])
                for leaf in leaves:
                    tree_text += f"│  ├─ 🍃 {leaf.name}\n"
            
            return tree_text
        except Exception as e:
            logger.error(f"Error getting tree structure: {e}")
            return "🌲 **OpenAspen Tree**\n\n⚠️ Unable to load structure"
    
    async def send_message(self, message: OutgoingMessage) -> bool:
        """Send a message via Telegram"""
        try:
            if not self.application:
                await self.initialize()
            
            # Build keyboard if provided
            reply_markup = None
            if message.inline_keyboard:
                keyboard = []
                for row in message.inline_keyboard:
                    button_row = [
                        InlineKeyboardButton(btn["text"], callback_data=btn["data"])
                        for btn in row
                    ]
                    keyboard.append(button_row)
                reply_markup = InlineKeyboardMarkup(keyboard)
            
            # Send message
            await self.application.bot.send_message(
                chat_id=message.chat_id,
                text=message.text,
                parse_mode=message.parse_mode,
                reply_markup=reply_markup
            )
            return True
            
        except Exception as e:
            logger.error(f"Error sending Telegram message: {e}")
            return False
    
    async def handle_webhook(self, payload: Dict[str, Any]) -> Optional[IncomingMessage]:
        """Process incoming webhook payload"""
        try:
            update = Update.de_json(payload, self.application.bot)
            
            if update.message:
                return IncomingMessage(
                    platform=MessagePlatform.TELEGRAM,
                    chat_id=str(update.message.chat_id),
                    user_id=str(update.message.from_user.id),
                    username=update.message.from_user.username,
                    message_id=str(update.message.message_id),
                    text=update.message.text,
                    message_type=MessageType.TEXT,
                    timestamp=update.message.date
                )
            
            return None
            
        except Exception as e:
            logger.error(f"Error handling Telegram webhook: {e}")
            return None
    
    async def setup_webhook(self, webhook_url: str) -> bool:
        """Configure Telegram webhook"""
        try:
            if not self.application:
                await self.initialize()
            
            self.webhook_url = webhook_url
            await self.application.bot.set_webhook(url=webhook_url)
            logger.info(f"Telegram webhook set to: {webhook_url}")
            return True
            
        except Exception as e:
            logger.error(f"Error setting Telegram webhook: {e}")
            return False
    
    async def delete_webhook(self) -> bool:
        """Remove Telegram webhook"""
        try:
            if not self.application:
                await self.initialize()
            
            await self.application.bot.delete_webhook()
            logger.info("Telegram webhook deleted")
            return True
            
        except Exception as e:
            logger.error(f"Error deleting Telegram webhook: {e}")
            return False
    
    def get_webhook_path(self) -> str:
        """Get the webhook endpoint path"""
        return "/messaging/telegram/webhook"
    
    async def start_polling(self):
        """Start bot in polling mode (for development)"""
        if not self.application:
            await self.initialize()
        
        logger.info("Starting Telegram bot in polling mode...")
        await self.application.run_polling()
