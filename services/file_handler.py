### `services/file_handler.py`

import tempfile
import os
from moviepy.editor import VideoFileClip

def extract_audio(file_path):
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio:
            clip = VideoFileClip(file_path)
            clip.audio.write_audiofile(temp_audio.name)
            clip.close()
            return temp_audio.name
    except Exception as e:
        print(f"Audio extraction error: {e}")
        return None