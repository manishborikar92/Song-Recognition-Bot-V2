from telegram import Update
from telegram.ext import ContextTypes
from services.downloader import download_content, download_song_from_youtube
from services.recognizer import recognize_song
from services.file_handler import extract_audio
from utils.helpers import format_song_info, is_file_under_limit
import os

# Handles incoming messages and determines their type (link, video, audio, or voice)
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text:  # Check if the message is text
        user_input = update.message.text
        await process_link(update, user_input)
    elif update.message.video or update.message.audio or update.message.voice:
        # Handle video, audio, or voice messages
        file = update.message.video or update.message.audio or update.message.voice
        await process_file(update, file, context)

# Process a text link provided by the user
async def process_link(update: Update, link: str):
    await update.message.reply_text("Processing your request...")
    file_path = download_content(link)  # Download content from the link
    if file_path:
        if is_file_under_limit(file_path):  # Check if the file is within size limits
            await update.message.reply_video(video=open(file_path, "rb"))
        await recognize_and_respond(update, file_path)  # Recognize and respond with song info
    else:
        await update.message.reply_text("Failed to process the link.")

# Process video, audio, or voice files uploaded by the user
async def process_file(update: Update, file, context):
    file_path = await context.bot.get_file(file.file_id).download()  # Download the file
    
    # Extract audio if the file is a video
    audio_path = extract_audio(file_path) if file.mime_type.startswith("video/") else file_path
    if audio_path:
        await recognize_and_respond(update, audio_path)  # Recognize and respond with song info
    else:
        await update.message.reply_text("Could not process the uploaded file.")
    
    # Clean up temporary files
    os.remove(file_path)
    if audio_path != file_path:
        os.remove(audio_path)

# Recognize the song in a file and send the response to the user
async def recognize_and_respond(update: Update, file_path: str):
    song_info = recognize_song(file_path)  # Use ACRCloud to recognize the song
    if song_info:
        response = format_song_info(song_info)  # Format the song info for user display
        await update.message.reply_text(response)
        
        # Attempt to download the original song from YouTube
        song_title = song_info.get("metadata", {}).get("music", [])[0].get("title", "Unknown Title")
        song_file = download_song_from_youtube(song_title)
        if song_file:
            await update.message.reply_audio(audio=open(song_file, "rb"))  # Send the song file
            os.remove(song_file)  # Remove the downloaded song file
        else:
            await update.message.reply_text("Could not find the original song file on YouTube.")
    else:
        await update.message.reply_text("Could not recognize the song.")