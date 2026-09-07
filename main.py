import os
import logging
import base64
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

# Setup logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Fetch Telegram Bot Token from Environment Variable
TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler for /start command."""
    user = update.effective_user.first_name
    welcome_text = (
        f"Hello, {user}! Welcome to **FTDify Utility Bot**.\n\n"
        "Here are the available built-in tools:\n"
        "• `/upper <text>` - Convert text to UPPERCASE\n"
        "• `/lower <text>` - Convert text to lowercase\n"
        "• `/reverse <text>` - Reverse any string\n"
        "• `/encode <text>` - Encode text to Base64\n"
        "• `/decode <text>` - Decode Base64 string\n"
        "• `/stats <text>` - Count characters, words, and lines\n\n"
        "Or simply send me any raw message to get instant text analytics!"
    )
    await update.message.reply_text(welcome_text, parse_mode="Markdown")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler for /help command."""
    help_text = (
        "**FTDify Bot Help Center**\n\n"
        "Commands:\n"
        "/upper <text> - UPPERCASE\n"
        "/lower <text> - lowercase\n"
        "/reverse <text> - txet esreveR\n"
        "/encode <text> - Base64 Encode\n"
        "/decode <text> - Base64 Decode\n"
        "/stats <text> - Text analysis\n"
    )
    await update.message.reply_text(help_text, parse_mode="Markdown")

async def upper_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = " ".join(context.args)
    if not text:
        await update.message.reply_text("Usage: `/upper hello world`", parse_mode="Markdown")
        return
    await update.message.reply_text(text.upper())

async def lower_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = " ".join(context.args)
    if not text:
        await update.message.reply_text("Usage: `/lower HELLO WORLD`", parse_mode="Markdown")
        return
    await update.message.reply_text(text.lower())

async def reverse_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = " ".join(context.args)
    if not text:
        await update.message.reply_text("Usage: `/reverse text`", parse_mode="Markdown")
        return
    await update.message.reply_text(text[::-1])

async def encode_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = " ".join(context.args)
    if not text:
        await update.message.reply_text("Usage: `/encode text to encode`", parse_mode="Markdown")
        return
    encoded = base64.b64encode(text.encode("utf-8")).decode("utf-8")
    await update.message.reply_text(f"`{encoded}`", parse_mode="Markdown")

async def decode_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = " ".join(context.args)
    if not text:
        await update.message.reply_text("Usage: `/decode <base64_string>`", parse_mode="Markdown")
        return
    try:
        decoded = base64.b64decode(text.encode("utf-8")).decode("utf-8")
        await update.message.reply_text(decoded)
    except Exception:
        await update.message.reply_text("❌ Invalid Base64 string.")

async def stats_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = " ".join(context.args)
    if not text and update.message.text:
        text = update.message.text

    if not text:
        await update.message.reply_text("Please provide text after the command or send a message.")
        return

    char_count = len(text)
    char_no_spaces = len(text.replace(" ", ""))
    word_count = len(text.split())
    line_count = len(text.splitlines())

    response = (
        "**Text Statistics:**\n"
        f"• Characters (with spaces): `{char_count}`\n"
        f"• Characters (no spaces): `{char_no_spaces}`\n"
        f"• Words: `{word_count}`\n"
        f"• Lines: `{line_count}`"
    )
    await update.message.reply_text(response, parse_mode="Markdown")

async def echo_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Automatically responds to raw text messages with character stats."""
    if update.message and update.message.text:
        text = update.message.text
        words = len(text.split())
        chars = len(text)
        await update.message.reply_text(
            f"Received your message!\n"
            f"Length: {chars} characters | Words: {words}\n\n"
            "Use /help to see all available tools."
        )

def main():
    if not TOKEN:
        logger.error("No TELEGRAM_BOT_TOKEN environment variable found. Exiting.")
        return

    # Build bot application
    app = ApplicationBuilder().token(TOKEN).build()

    # Register handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("upper", upper_cmd))
    app.add_handler(CommandHandler("lower", lower_cmd))
    app.add_handler(CommandHandler("reverse", reverse_cmd))
    app.add_handler(CommandHandler("encode", encode_cmd))
    app.add_handler(CommandHandler("decode", decode_cmd))
    app.add_handler(CommandHandler("stats", stats_cmd))
    
    # Text message fallback
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), echo_handler))

    logger.info("FTDify123_bot background worker is starting...")
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
