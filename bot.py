import traceback
from flask import Flask, request
import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from config import BOT_TOKEN
from handlers.command_handler import start, delete, search
from handlers.massage_handler import handle_message
import asyncio

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Flask app for Render
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

@app.route('/webhook', methods=['POST'])
async def webhook():
    try:
        # Log the raw incoming request data as a string to debug the request
        raw_data = request.get_data(as_text=True)
        logger.debug("Received request data: %s", raw_data)
        
        # Process updates received from Telegram
        update = Update.de_json(request.get_json(), application.bot)
        await application.process_update(update)
        
        return "ok"
    
    except Exception as e:
        # Log the full exception traceback for debugging
        logger.error("Error processing webhook: %s", str(e))
        logger.error("Traceback: %s", traceback.format_exc())
        return "Error", 500

if __name__ == "__main__":
    # Initialize the Application object
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    # Add handlers to the application
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("search", search))
    application.add_handler(CommandHandler("delete", delete))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_handler(MessageHandler(filters.VIDEO | filters.AUDIO | filters.VOICE, handle_message))

    # Set the webhook URL
    WEBHOOK_URL = f"https://song-recognition-bot-v2.onrender.com/webhook"

    # Use asyncio to await the set_webhook method
    asyncio.run(application.bot.set_webhook(WEBHOOK_URL))

    # Start the Flask app
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
