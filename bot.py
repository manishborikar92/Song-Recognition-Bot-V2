import os
import logging
from flask import Flask
from threading import Thread
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from config import BOT_TOKEN
from handlers.command import start_command, help_command, search_command, delete_command, broadcast_command, getinfo_command, getusers_command, history_command
from handlers.message import handle_message

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Get a logger instance
logger = logging.getLogger(__name__)

# Suppress unnecessary logs from the Telegram API and its dependencies
logging.getLogger("telegram").setLevel(logging.WARNING)  # For the main telegram logger
logging.getLogger("telegram.bot").setLevel(logging.WARNING)  # For bot-specific logs
logging.getLogger("telegram.request").setLevel(logging.WARNING)  # For request-related logs
logging.getLogger("telegram.vendor.ptb_urllib3").setLevel(logging.WARNING)  # For telegram's urllib3 logs
logging.getLogger("httpx").setLevel(logging.WARNING)  # For httpx logs (since telegram internally uses httpx)
logging.getLogger("urllib3").setLevel(logging.WARNING)  # For general HTTP requests
        
# Flask app for Render
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

def run_flask():
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

if __name__ == "__main__":
    # Start Flask in a separate thread
    Thread(target=run_flask).start()

    application = ApplicationBuilder().token(BOT_TOKEN).concurrent_updates(True).build()

    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("search", search_command))
    application.add_handler(CommandHandler("delete", delete_command))
    application.add_handler(CommandHandler("broadcast", broadcast_command))
    application.add_handler(CommandHandler("getinfo", getinfo_command))
    application.add_handler(CommandHandler("getusers", getusers_command))
    application.add_handler(CommandHandler("history", history_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_handler(MessageHandler(filters.VIDEO | filters.AUDIO | filters.VOICE, handle_message))

    logging.info("Bot is running...")
    application.run_polling()