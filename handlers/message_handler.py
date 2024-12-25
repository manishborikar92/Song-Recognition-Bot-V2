### `handlers/message_handler.py`

from telegram import Update
from telegram.ext import ContextTypes
from services.downloader import download_content, download_song_from_youtube
from services.recognizer import recognize_song
from utils.validation import validate_link
from utils.helpers import format_song_info, is_file_under_limit

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text
    if validate_link(user_input):
        await update.message.reply_text("Processing your request...")
        file_path = download_content(user_input)
        if file_path:
            if is_file_under_limit(file_path):
                await update.message.reply_video(video=open(file_path, "rb"))
            song_info = recognize_song(file_path)
            if song_info:
                response = format_song_info(song_info)
                song_title = song_info.get("metadata", {}).get("music", [])[0].get("title", "Unknown Title")
                song_file = download_song_from_youtube(song_title)
                if song_file:
                    await update.message.reply_text(response)
                    await update.message.reply_audio(audio=open(song_file, "rb"))
                else:
                    await update.message.reply_text("Could not find the original song file on YouTube.")
            else:
                await update.message.reply_text("Could not recognize the song.")
        else:
            await update.message.reply_text("Failed to process the link.")
    else:
        await update.message.reply_text("Invalid link or unsupported format.")