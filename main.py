from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from handlers.message_handler import handle_message
from handlers.command_handler import start
import config

if __name__ == "__main__":
    # Create an instance of the bot application with the provided token
    app = ApplicationBuilder().token(config.TELEGRAM_TOKEN).build()
    
    # Add a command handler for the /start command
    app.add_handler(CommandHandler("start", start))
    
    # Add a message handler to handle text, video, audio, and voice messages
    app.add_handler(MessageHandler((filters.TEXT & ~filters.COMMAND) | filters.VIDEO | filters.AUDIO | filters.VOICE, handle_message))
    
    # Start the bot and keep it running
    app.run_polling()