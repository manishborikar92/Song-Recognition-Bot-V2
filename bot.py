import os
import logging
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from telegram import Update
from flask import Flask, request
from config import BOT_TOKEN, WEBHOOK_URL
from handlers.command_handler import start, delete, search
from handlers.massage_handler import handle_message

# Configure logging
logging.basicConfig(level=logging.CRITICAL, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)

# Set up the Telegram bot with webhook
application = ApplicationBuilder().token(BOT_TOKEN).build()

# Add handlers for bot commands and messages
application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("search", search))
application.add_handler(CommandHandler("delete", delete))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
application.add_handler(MessageHandler(filters.VIDEO | filters.AUDIO | filters.VOICE, handle_message))

@app.route('/webhook', methods=['POST'])
def webhook():
    # Get the incoming update from Telegram
    update = Update.de_json(request.get_json(), application.bot)
    application.process_update(update)
    return 'OK', 200

if __name__ == "__main__":
    # Set webhook URL for Telegram Bot
    application.bot.set_webhook(url=WEBHOOK_URL)
    print(f"Webhook set to {WEBHOOK_URL}")
    
    # Run the Flask app
    app.run(host="0.0.0.0", port=5000)
