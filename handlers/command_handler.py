from telegram import Update
from telegram.ext import ContextTypes

# Handles the /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome to the bot! Send me an Instagram or YouTube link, or upload a file to get started.")