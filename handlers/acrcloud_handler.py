import requests
import base64
import hmac
import hashlib
import time
import json
import os
from pydub import AudioSegment
from config import ACR_HOST, ACR_ACCESS_KEY, ACR_ACCESS_SECRET, ACR_BEARER_TOKEN, ACR_ENDPOINT_URL

# Create a session for faster repeated requests
session = requests.Session()

def recognize_song(audio_path):
    """
    Recognize a song using ACRCloud. Automatically trims audio if it's longer than 1 minute.

    Args:
        audio_path (str): The path to the audio file.
        host (str): The ACRCloud host URL.
        access_key (str): Your ACRCloud access key.
        access_secret (str): Your ACRCloud access secret.

    Returns:
        dict: The song recognition result.
    """
    host = ACR_HOST
    access_key = ACR_ACCESS_KEY
    access_secret = ACR_ACCESS_SECRET

    try:
        # Check and trim audio if necessary
        audio = AudioSegment.from_file(audio_path)
        if len(audio) > 60000:  # Check if audio is longer than 60 seconds
            print("Audio is longer than 1 minute. Trimming to 20 seconds.")
            trimmed_audio_path = os.path.splitext(audio_path)[0] + "_trimmed.mp3"
            trimmed_audio = audio[10000:30000]  # Extract 10th to 30th second (20 seconds)
            trimmed_audio.export(trimmed_audio_path, format="mp3")
            audio_path = trimmed_audio_path  # Use trimmed audio for recognition

        # Prepare request data
        http_method = "POST"
        http_uri = "/v1/identify"
        data_type = "audio"
        signature_version = "1"
        timestamp = str(int(time.time()))

        string_to_sign = (
            f"{http_method}\n{http_uri}\n{access_key}\n{data_type}\n{signature_version}\n{timestamp}"
        )

        # Generate the signature
        signature = base64.b64encode(
            hmac.new(
                access_secret.encode(),
                string_to_sign.encode(),
                hashlib.sha1
            ).digest()
        ).decode()

        # Open the audio file
        with open(audio_path, 'rb') as audio_file:
            file_size = os.path.getsize(audio_path)
            files = {
                'sample': ('sample.mp3', audio_file)
            }
            data = {
                'access_key': access_key,
                'data_type': data_type,
                'signature_version': signature_version,
                'signature': signature,
                'sample_bytes': file_size,
                'timestamp': timestamp
            }

            # Debugging
            print("Request Data:", data)

            # Make the POST request
            response = session.post(
                f"{host}{http_uri}",
                data=data,
                files=files,
                timeout=10
            )

        response_data = response.json()
        print("Response JSON:", response_data)

        # Handle errors
        if response_data.get("status", {}).get("code") != 0:
            raise Exception(f"ACRCloud Error: {response_data.get('status', {}).get('msg')}")

        # Extract metadata
        if "metadata" in response_data and "music" in response_data["metadata"]:
            song_info = response_data
            song = song_info["metadata"]["music"][0]
            title = song.get("title", "Unknown Title")
            artists = ", ".join(artist["name"] for artist in song.get("artists", []))
            print(f"Title: {title}\n Artists: {artists}")
        else:
            print("No match found in ACRCloud database.")
            return response_data

        return response_data
    except Exception as e:
        raise Exception(f"Error recognizing song: {e}")
    

def get_song_info(title: str, artist: str):
    """
    Searches for the original song name and artist using the ACRCloud API.
    """
    API_URL = ACR_ENDPOINT_URL
    API_KEY = ACR_BEARER_TOKEN
    
    headers = {
        'Authorization': f'Bearer {API_KEY}'
    }
    params = {
        'query': json.dumps({"track": title, "artists": artist}),
        'format': 'json'
    }

    try:
        response = requests.get(API_URL, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()

        if data.get("data"):
            song = data["data"][0]
            title = song.get("name", "Unknown Title")
            artists = ", ".join(artist["name"] for artist in song.get("artists", []))
            album = song.get("album", {}).get("name", "Unknown Album")
            release_date = song.get("album", {}).get("release_date", "Unknown Release Date")
            youtube_links = [yt.get("link") for yt in song.get("external_metadata", {}).get("youtube", [])]
            spotify_links = [sp.get("link") for sp in song.get("external_metadata", {}).get("spotify", [])]
            
            print(f"Song found: {title}")
            
            return {
                "title": title,
                "artists": artists,
                "album": album,
                "release_date": release_date,
                "youtube_links": youtube_links,
                "spotify_links": spotify_links,
            }

        print("No results found.")
        return None

    except requests.exceptions.RequestException as e:
        print(f"Error fetching song info: {e}")
        return None



# # Example usage
# if __name__ == "__main__":
#     # Paths
#     input_audio_path = r'temp/audios/The Weeknd - Blinding Lights (Official Video).mp3'

#     # ACRCloud credentials from .env
#     acr_host = os.getenv("ACR_HOST")
#     acr_access_key = os.getenv("ACR_ACCESS_KEY")
#     acr_access_secret = os.getenv("ACR_ACCESS_SECRET")

#     if not acr_host or not acr_access_key or not acr_access_secret:
#         raise ValueError("Missing required environment variables: ACR_HOST, ACR_ACCESS_KEY, ACR_ACCESS_SECRET")

#     # Recognize song
#     recognize_song(input_audio_path, acr_host, acr_access_key, acr_access_secret)


# # Example usage
# if __name__ == "__main__":
#     # Paths
#     input_audio_path = r'temp/audios/The Weeknd - Blinding Lights (Official Video).mp3'

#     # ACRCloud credentials from .env
#     acr_host = os.getenv("ACR_HOST")
#     acr_access_key = os.getenv("ACR_ACCESS_KEY")
#     acr_access_secret = os.getenv("ACR_ACCESS_SECRET")

#     if not acr_host or not acr_access_key or not acr_access_secret:
#         raise ValueError("Missing required environment variables: ACR_HOST, ACR_ACCESS_KEY, ACR_ACCESS_SECRET")

#     # Recognize song
#     recognize_song(input_audio_path, acr_host, acr_access_key, acr_access_secret)
