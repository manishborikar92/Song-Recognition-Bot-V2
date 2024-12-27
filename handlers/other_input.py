from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# Define the handler for location messages
async def process_location(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text(f"You sent a location: {update.message.location}")

# Define the handler for contact messages
async def process_contact(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text(f"You sent a contact: {update.message.contact.first_name} {update.message.contact.last_name}")

# Define the handler for video note messages
async def process_video_note(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("You sent a video note!")

# Define the handler for any other unknown message type
async def process_unknown(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("Received an unknown type of message!")