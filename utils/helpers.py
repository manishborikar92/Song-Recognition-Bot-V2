### `utils/helpers.py`

import os

def format_song_info(song_info):
    try:
        title = song_info.get("metadata", {}).get("music", [])[0].get("title", "Unknown Title")
        artist = song_info.get("metadata", {}).get("music", [])[0].get("artists", [{}])[0].get("name", "Unknown Artist")
        return f"Title: {title}\nArtist: {artist}"
    except Exception:
        return "Could not retrieve song information."

def is_file_under_limit(file_path, limit_mb=50):
    file_size_mb = os.path.getsize(file_path) / (1024 * 1024)
    return file_size_mb <= limit_mb