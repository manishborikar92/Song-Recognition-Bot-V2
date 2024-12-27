from telegram import Update
import asyncio
from telegram.ext import CallbackContext
from downloader.instagram import download_instagram_reel
from db.database import get_state, update_state

async def process_text(update: Update, context: CallbackContext):
    url = update.message.text

    await update.message.reply_text("Downloading reel...", reply_to_message_id=update.message.message_id)

    # Use asyncio.to_thread to handle the blocking operation in a separate thread
    def worker(url):
        return download_instagram_reel(url)

    try:
        video_path, caption = await asyncio.to_thread(worker, url)

        if video_path:
            with open(video_path, "rb") as video:
                await update.message.reply_video(video=video, caption=caption, reply_to_message_id=update.message.message_id)
        else:
            await update.message.reply_text("Failed to process the URL. Please try again.")
    except Exception as e:
        await update.message.reply_text(f"An error occurred: {e}")
