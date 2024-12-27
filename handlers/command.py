from telegram import Update
from telegram.ext import CallbackContext
from db.database import save_user

async def start(update: Update, context: CallbackContext):
    user_id = int(update.message.from_user.id)
    username = update.effective_user.username or "Anonymous"

    # Save user to database
    save_user(user_id, username)

    await update.message.reply_text(
        "🎵 <b>Hello there!</b> I’m <b>@TuneDetectBot</b>, your personal music detective powered by <a href='https://t.me/ProjectON3'>ProjectON3</a>. 🎶\n\n"
        "✨ Simply send me a <b>URL</b>, upload a <b>file</b>, or send a <b>voice message</b>, and I'll work my magic to identify the song for you! 🚀",
        parse_mode='HTML'
    )
