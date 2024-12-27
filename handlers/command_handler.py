from telegram import Update
from telegram.ext import CallbackContext
from utils.clear_data import delete_all
from config import EXCEPTION_USER_ID

# Start command handler
async def start(update: Update, context: CallbackContext):
    await update.message.reply_text(
        "🎵 <b>Hello there!</b> I’m <b>@TuneDetectBot</b>, your personal music detective powered by <a href='https://t.me/ProjectON3'>ProjectON3</a>. 🎶\n\n"
        "✨ Simply send me a <b>URL</b>, upload a <b>file</b>, or send a <b>voice message</b>, and I'll work my magic to identify the song for you! 🚀",
        parse_mode='HTML'
    )

async def search(update: Update, context: CallbackContext):
    print("search")
    
async def delete(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    if int(user_id) == int(EXCEPTION_USER_ID):
        delete_all()
        await update.message.reply_text(
            "<b>Data Deleted</b> 🗑",
            parse_mode='HTML'
        )
    else:
        await update.message.reply_text("❌")
        await update.message.reply_text("<b>You are not the owner. Permission denied.</b>", parse_mode='HTML')