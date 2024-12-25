### `services/recognizer.py`

from acrcloud.recognizer import ACRCloudRecognizer
from config import ACRCLOUD_CONFIG

acrcloud = ACRCloudRecognizer(ACRCLOUD_CONFIG)

def recognize_song(file_path):
    try:
        with open(file_path, "rb") as f:
            data = f.read()
            result = acrcloud.recognize_by_filebuffer(data, 0, len(data))
            return result
    except Exception as e:
        print(f"Recognition error: {e}")
        return None