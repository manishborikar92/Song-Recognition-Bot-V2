import logging
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
from config import BOT_TOKEN
from handlers.command import start
from handlers.media import process_audio, process_video, process_voice, process_document, process_photo
from handlers.message import process_text
from handlers.other_input import process_contact, process_location, process_unknown, process_video_note

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.CRITICAL
)
logger = logging.getLogger(__name__)

# Global error handler
async def error_handler(update: object, context: CallbackContext):
    logger.error(f"Error: {context.error}")
    if update and update.effective_message:
        await update.effective_message.reply_text("An error occurred. Please try again later.")

if __name__ == "__main__":
    app = Application.builder().token(BOT_TOKEN).concurrent_updates(True).build()  # Enable concurrent updates

    # Add the handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, process_text))
    app.add_handler(MessageHandler(filters.VIDEO, process_video))
    app.add_handler(MessageHandler(filters.AUDIO, process_audio))
    app.add_handler(MessageHandler(filters.VOICE, process_voice))
    app.add_handler(MessageHandler(filters.PHOTO, process_photo))
    app.add_handler(MessageHandler(filters.ATTACHMENT, process_document))
    app.add_handler(MessageHandler(filters.LOCATION, process_location))
    app.add_handler(MessageHandler(filters.CONTACT, process_contact))
    app.add_handler(MessageHandler(filters.VIDEO_NOTE, process_video_note))
    app.add_handler(MessageHandler(filters.ALL, process_unknown))

    # Add error handler
    app.add_error_handler(error_handler)

    print("Bot Starting...")
    app.run_polling()