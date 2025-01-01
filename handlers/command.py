import os
import asyncio
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from config import EXCEPTION_USER_IDS, DEVELOPERS
from downloader.song import download_song
from utils.acrcloud import get_song_info
from utils.send_file import sendsong
from utils.cleardata import delete_cache, delete_file, delete_all
from utils.pdf_generator import create_pdf
from database.db_manager import DBManager
import tempfile


# Initialize the database manager
db = DBManager()

# Start command handler
async def start_command(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    user_name = update.message.from_user.full_name
    db.add_user(user_id, user_name)

    await update.message.reply_text(
        "🎵 <b>Hello there!</b> I’m <b>@TuneDetectBot</b>, your personal music detective powered by <a href='https://t.me/ProjectON3'>ProjectON3</a>. 🎶\n\n"
        "✨ Simply send me a <b>URL</b>, upload a <b>file</b>, or send a <b>voice message</b>, and I'll work my magic to identify the song for you! 🚀",
        parse_mode='HTML'
    )


async def help_command(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    if int(user_id) in EXCEPTION_USER_IDS:
        help_text = (
            "<b>🔊 Song Recognition Bot Help</b>\n\n"
            "Here are the available commands and their usage:\n\n"
            "- <b>/start</b> - Start the bot and get a welcome message. 🤖✨\n"
            "- <b>/help</b> - Display this help message. ❓📖\n"
            "- <b>/search</b> - Search for a song by name or artist (e.g., 'song name - artist name'). 🔍🎶\n"
            "- 📹 Share a video, audio, or voice message - The bot will recognize the song and provide details. 🎧🎵\n"
            "- 🌐 Send a YouTube or Instagram link - The bot will download the video, analyze it, and identify the song. 🎥🎶\n"
            "- <b>/history</b> - View your own message history. 📜\n"
            "- <b>/broadcast</b> - Send a message to all users (Developer only). 📢\n"
            "- <b>/getusers</b> - Retrieve all user IDs and names (Developer only). 🧾\n"
            "- <b>/getinfo</b> - Fetch user history (Developer only). 📄\n"
            "- <b>/deluser</b> - Clear specific or all user data (Developer only). 🗑\n"
            "- <b>/delfiles</b> - Clear all media files and cache. (Developer only). 📁🗑\n\n"
            "<a href='https://t.me/ProjectON3'>ProjectON3</a>"
        )
        await update.message.reply_text(help_text, parse_mode="HTML")

    else:
        help_text = (
            "<b>🔊 Song Recognition Bot Help</b>\n\n"
            "Here are the available commands and their usage:\n\n"
            "- <b>/start</b> - Start the bot and get a welcome message. 🤖✨\n"
            "- <b>/help</b> - Display this help message. ❓📖\n"
            "- <b>/search</b> - Search for a song by name or artist (e.g., 'song name - artist name'). 🔍🎶\n"
            "- 📹 Share a video, audio, or voice message - The bot will recognize the song and provide details. 🎧🎵\n"
            "- 🌐 Send a YouTube or Instagram link - The bot will download the video, analyze it, and identify the song. 🎥🎶\n"
            "- <b>/history</b> - View your own message history. 📜\n\n"
            "For support or issues, feel free to contact the developer! 😊\n"
            "<a href='https://t.me/ProjectON3'>ProjectON3</a>"
        )
        
        # Send the help text as a message to the user
        await update.message.reply_text(help_text, parse_mode="HTML")


async def search_command(update: Update, context: CallbackContext):
    try:
        user_id = update.message.from_user.id
        user_name = update.message.from_user.full_name
        user_input = update.message.text

        if not db.user_exists(user_id):
            db.add_user(user_id, user_name)

        db.log_input(user_id, user_input)

        if len(context.args) == 0:
            await update.message.reply_text("🎵 Wanna find a song?\n\n Use: /search <song title> or /search <song title> - <artist name> 🔍✨")
            return

        full_input = ' '.join(context.args)
        if '-' in full_input:
            title, artists = map(str.strip, full_input.split('-', 1))
        else:
            title = full_input
            artists = ''

        try:
            downloading_message = await update.message.reply_text(
                "🔍 <b>Hunting for the track...</b> 🎶🎧",
                parse_mode='HTML',
                reply_to_message_id=update.message.message_id
            )
            song_data = await asyncio.to_thread(get_song_info, title, artists)
            if not song_data:
                await downloading_message.edit_text("❌ Oops! No matching song found.")
                return
        except Exception as e:
            logging.error(f"Something went wrong while searching for the song: {e}")
            await downloading_message.edit_text(f"⚠️ Something went wrong while searching for the song: {str(e)}")
            return

        try:
            song_title = song_data.get('title')
            song_artist = song_data.get('artists')
            song_album = song_data.get('album', 'Unknown')
            song_release_date = song_data.get('release_date', 'Unknown')
            youtube_link = song_data.get('youtube_link')
            spotify_link = song_data.get('spotify_link')

            await downloading_message.edit_text(
                "⬇️ <b>Getting your jam...</b> 🎶🚀",
                parse_mode='HTML',
            )
            song_path = await asyncio.to_thread(download_song, song_title, song_artist)

            if not song_path:
                await update.message.reply_text(
                    "🚫 <b>Song file not found.</b> I found the song but couldn't fetch the file 🥲",
                    parse_mode='HTML'
                )
                return

            await sendsong(update, downloading_message, song_title, song_artist, song_album, song_release_date, youtube_link, spotify_link, song_path)
        except Exception as e:
            logging.error(f"Something went wrong while sending the song: {e}")
    except Exception as e:
        logging.error(f"Error processing message: {e}")
    finally:
        delete_file(song_path)
        delete_cache()


async def history_command(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    history = db.get_user_history(user_id)
    if not history:
        await update.message.reply_text("❌ You have no history recorded.")
        return

    content = [(h[0], h[1]) for h in history]
    headers = ["Input", "Date and Time"]
    pdf_path = f"your_history_{user_id}.pdf"
    create_pdf(pdf_path, "Your History", headers, content)

    await update.message.reply_document(
        document=open(pdf_path, 'rb'),
        filename=pdf_path,
        caption="📄 Your History"
    )
    os.remove(pdf_path)


async def broadcast_command(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    if int(user_id) in EXCEPTION_USER_IDS:
        if not context.args:
            await update.message.reply_text("❌ Please provide a message to broadcast.")
            return

        message = ' '.join(context.args)
        users = db.get_all_users()
        for user in users:
            try:
                await context.bot.send_message(chat_id=user[0], text=message)
            except Exception as e:
                print(f"Failed to send message to {user[0]}: {e}")

        await update.message.reply_text("✅ Message broadcasted to all users.")
    else:
        await update.message.reply_text("❌ You do not have permission to use this command.")


async def getusers_command(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    if int(user_id) in EXCEPTION_USER_IDS:
        users = db.get_all_users()
        if not users:
            await update.message.reply_text("❌ No users found.")
            return

        content = [(u[0], u[1] or None) for u in users]  # Extract User ID and Name
        headers = ["User ID", "Name"]
        pdf_path = "registered_users.pdf"
        create_pdf(pdf_path, "Registered Users", headers, content)

        await update.message.reply_document(
            document=open(pdf_path, 'rb'),
            filename=pdf_path,
            caption="📄 Registered Users"
        )
        os.remove(pdf_path)
    else:
        await update.message.reply_text("❌ You do not have permission to use this command.")


async def getinfo_command(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    if int(user_id) in DEVELOPERS:
        if not context.args:
            await update.message.reply_text("❌ Please provide a user ID.")
            return

        target_user_id = int(context.args[0])
        history = db.get_user_history(target_user_id)
        if not history:
            await update.message.reply_text("❌ No history found for the specified user.")
            return

        content = [(h[0], h[1]) for h in history]
        headers = ["Input", "Date and Time"]
        pdf_path = f"user_history_{target_user_id}.pdf"
        create_pdf(pdf_path, "User History", headers, content)

        await update.message.reply_document(
            document=open(pdf_path, 'rb'),
            filename=pdf_path,
            caption="📄 User History"
        )
        os.remove(pdf_path)
    else:
        await update.message.reply_text("❌ You do not have permission to use this command.")

async def deluser_command(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    if int(user_id) in DEVELOPERS:
        db.delete_user_data()
        await update.message.reply_text("✅ All user data has been deleted.")
    else:
        await update.message.reply_text("❌")
        await update.message.reply_text(
            "<b>You are not the Developer. Permission denied.</b>",
            parse_mode='HTML'
        )

async def delfiles_command(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    if int(user_id) in DEVELOPERS:
        results = delete_all()
        message = "<b>Deletion Summary:</b>\n\n"
        for folder, status in results.items():
            message += f"• {folder}: {status.capitalize()}\n\n"
        await update.message.reply_text(message, parse_mode='HTML')
        await update.message.reply_text("✅ All user data has been deleted.")
    else:
        await update.message.reply_text("❌")
        await update.message.reply_text(
            "<b>You are not the Developer. Permission denied.</b>",
            parse_mode='HTML'
        )