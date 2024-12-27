from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
from config import BOT_TOKEN
from handlers.command import start
from handlers.media import process_audio, process_video, process_voice, process_document, process_photo
from handlers.message import process_text
from handlers.other_input import process_contact, process_location, process_unknown, process_video_note


if __name__ == "__main__":
    BOT_TOKEN = f'{BOT_TOKEN}'
    # Initialize the application with your bot token
    app = Application.builder().token(BOT_TOKEN).build()

    # Add the handlers
    app.add_handler(CommandHandler("start", start))

    # Add message handlers for various types of messages
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, process_text))  # Handles non-command text messages
    app.add_handler(MessageHandler(filters.VIDEO, process_video))  # Handles video messages
    app.add_handler(MessageHandler(filters.AUDIO, process_audio))  # Handles audio messages
    app.add_handler(MessageHandler(filters.VOICE, process_voice))  # Handles voice messages
    app.add_handler(MessageHandler(filters.PHOTO, process_photo))  # Handles photo messages
    app.add_handler(MessageHandler(filters.ATTACHMENT, process_document))  # Handles document messages
    app.add_handler(MessageHandler(filters.LOCATION, process_location))  # Handles location messages
    app.add_handler(MessageHandler(filters.CONTACT, process_contact))  # Handles contact messages
    app.add_handler(MessageHandler(filters.VIDEO_NOTE, process_video_note))  # Handles video note messages

    # Default handler for unknown message types
    app.add_handler(MessageHandler(filters.ALL, process_unknown))  # Handles any other types of messages

        
    print("Bot Starting...")
    # Start polling for messages
    app.run_polling()