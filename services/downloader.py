### `services/downloader.py`

import yt_dlp
import os
from config import TEMP_DIR

def download_content(link):
    options = {
        "outtmpl": os.path.join(TEMP_DIR, "%(title)s.%(ext)s"),
        "format": "bestvideo+bestaudio/best",
        "noplaylist": True,
        "quiet": True,
    }
    try:
        with yt_dlp.YoutubeDL(options) as ydl:
            info = ydl.extract_info(link, download=True)
            return ydl.prepare_filename(info)
    except Exception as e:
        print(f"Download error: {e}")
        return None

def download_song_from_youtube(song_title):
    options = {
        "outtmpl": os.path.join(TEMP_DIR, f"{song_title}.mp3"),
        "format": "bestaudio/best",
        "quiet": True,
    }
    search_query = f"ytsearch1:{song_title}"
    try:
        with yt_dlp.YoutubeDL(options) as ydl:
            info = ydl.extract_info(search_query, download=True)
            return ydl.prepare_filename(info)
    except Exception as e:
        print(f"Song download error: {e}")
        return None