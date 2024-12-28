from telegram import Update
from telegram.ext import CallbackContext
from telegram import Update
import sqlite3
from telegram.ext import ContextTypes
from utils.clear_data import delete_all
from config import EXCEPTION_USER_ID

# Start command handler
async def start(update: Update, context: CallbackContext):
    await update.message.reply_text(
        "🎵 <b>Hello there!</b> I’m <b>@TuneDetectBot</b>, your personal music detective powered by <a href='https://t.me/ProjectON3'>ProjectON3</a>. 🎶\n\n"
        "✨ Simply send me a <b>URL</b>, upload a <b>file</b>, or send a <b>voice message</b>, and I'll work my magic to identify the song for you! 🚀",
        parse_mode='HTML'
    )

async def search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handles the /search command to find and return matching songs from the database.

    Args:
        update (telegram.Update): The incoming update from Telegram.
        context (telegram.ext.ContextTypes.DEFAULT_TYPE): The context for the command.
    """
    if len(context.args) == 0:
        await update.message.reply_text("Usage: /search <song title>")
        return

    query = " ".join(context.args).lower()  # Extract the search query
    matches = []

    try:
        # Connect to the SQLite database
        conn = sqlite3.connect("db/songs.db")
        cursor = conn.cursor()

        # Query the database for matching songs (case-insensitive)
        cursor.execute("""
        SELECT title, artists, file_path FROM songs WHERE title LIKE ?;
        """, ('%' + query + '%',))

        # Fetch all matching songs
        matches = cursor.fetchall()

        # Close the connection
        conn.close()

    except Exception as e:
        print(f"Error querying the database: {e}")

    if not matches:
        await update.message.reply_text(f"No songs found matching: {query}")
        return

    # Send matching songs to the user
    bot = context.bot
    for song in matches:
        title, artists, file_path = song
        caption = (
            f"🎶 <b>Song Found: {title}</b>\n"
            f"✨ <b>Artists:</b> {artists}\n\n"
            "<a href='https://t.me/ProjectON3'>ProjectON3</a> | @TuneDetectV2BOT"
        )
        with open(file_path, "rb") as song_file:
            await bot.send_audio(chat_id=update.effective_chat.id, audio=song_file, caption=caption, parse_mode='HTML')

    
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