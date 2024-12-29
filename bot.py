import traceback
import threading
import os
import logging
from flask import Flask, request
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
def webhook():
    try:
        # Get raw data from the request
        raw_data = request.get_data(as_text=True)
        logger.debug("Received request data: %s", raw_data)
        
        # Parse the incoming data into a Telegram Update object
        update = Update.de_json(request.get_json(), application.bot)

        # Function to handle update asynchronously in a separate thread
        def process_update_async():
            try:
                asyncio.run(application.process_update(update))
            except Exception as e:
                logger.error("Error processing update: %s", str(e))
                logger.error("Traceback: %s", traceback.format_exc())

        # Start the async task in a separate thread
        threading.Thread(target=process_update_async).start()

        return "ok"
    
    except Exception as e:
        # Log the error and traceback
        logger.error("Error in webhook: %s", str(e))
        logger.error("Traceback: %s", traceback.format_exc())
        return "Error", 500


def main():
    # Initialize the Telegram bot application
    global application
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    # Add handlers to the application
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("search", search))
    application.add_handler(CommandHandler("delete", delete))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_handler(MessageHandler(filters.VIDEO | filters.AUDIO | filters.VOICE, handle_message))

    # Set the webhook URL (make sure it's pointing to your active ngrok or production URL)
    WEBHOOK_URL = f"https://akita-causal-rattler.ngrok-free.app/webhook"
    asyncio.run(application.bot.set_webhook(WEBHOOK_URL))

    # Start the Flask app with debugging enabled for detailed error logs
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)  # Enable debug mode


if __name__ == "__main__":
    main()
