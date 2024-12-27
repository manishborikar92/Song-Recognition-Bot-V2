from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# Define the handler for text messages
async def process_text(update: Update, context: CallbackContext) -> None:
    user_message = update.message.text
    await update.message.reply_text(f"You sent a text message: {user_message}")