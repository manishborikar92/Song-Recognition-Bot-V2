from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
from db.database import save_user, update_state, get_state

# Define the handler for video messages
async def process_video(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("You sent a video!")

# Define the handler for audio messages
async def process_audio(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("You sent an audio message!")

# Define the handler for voice messages
async def process_voice(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("You sent a voice message!")

# Define the handler for photo messages
async def process_photo(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("You sent a photo!")

# Define the handler for document messages
async def process_document(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("You sent a document!")