from acrcloud.recognizer import ACRCloudRecognizer
from config import ACRCLOUD_CONFIG

# Initialize the ACRCloud recognizer with the provided config
acrcloud = ACRCloudRecognizer(ACRCLOUD_CONFIG)

# Recognize a song from an audio file
def recognize_song(file_path):
    try:
        with open(file_path, "rb") as f:
            data = f.read()
            result = acrcloud.recognize_by_filebuffer(data, 0, len(data))
            return result
    except Exception as e:
        print(f"Recognition error: {e}")
        return None