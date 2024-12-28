import os
from yt_dlp import YoutubeDL
import eyed3
from telegram import Bot
from db.database import save_song_to_db, is_song_sent
from config import BOT_TOKEN

# Telegram Bot Token
TELEGRAM_BOT_TOKEN = BOT_TOKEN
TELEGRAM_GROUP_ID = -4673323320  # Replace with your group ID

def download_song(title, artist):
    """
    Downloads a song as an MP3 based on the title and artist and tags it with artist info.

    Args:
        title (str): The title of the song.
        artist (str): The artist of the song.

    Returns:
        str: The file path of the downloaded MP3.
    """
    output_dir = "data/music"
    os.makedirs(output_dir, exist_ok=True)
    
    existing_path = os.path.join(output_dir, f"{title}.mp3")
    
    if os.path.exists(existing_path):
        return existing_path

    # Construct the search query
    query = f"{title} {artist} audio"

    # Configure yt-dlp options for faster downloads
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': os.path.join(output_dir, f'{title}.%(ext)s'),
        'quiet': True,  # Reduce console output
        'noplaylist': True,
        'extractaudio': True,  # Avoid downloading video
    }

    try:
        # Download the song
        with YoutubeDL(ydl_opts) as ydl:
            result = ydl.extract_info(f"ytsearch:{query}", download=True)

        # Get the downloaded file path
        if 'entries' in result:
            result = result['entries'][0]
        file_path = os.path.join(output_dir, f"{title}.mp3")

        # Ensure the file exists and is not corrupt
        if not os.path.isfile(file_path):
            raise FileNotFoundError("The MP3 file was not downloaded correctly.")

        # Add artist name as tag using eyed3
        audiofile = eyed3.load(file_path)
        audiofile.tag.artist = artist  # Set artist tag
        audiofile.tag.save()  # Save changes

        # Test if the file can be opened
        with open(file_path, "rb") as song_file:
            song_file.read(1)  # Read the first byte to ensure the file is valid

        # Tag the MP3 file
        tag_mp3_file(file_path, artist)

        return file_path
    
    except Exception as e:
        raise RuntimeError(f"Error downloading the song: {e}")
    
def tag_mp3_file(file_path, artist):
    """
    Adds artist tag to the MP3 file.

    Args:
        file_path (str): The path of the MP3 file.
        artist (str): The artist name to add as a tag.
    """
    try:
        audiofile = eyed3.load(file_path)
        if not audiofile:
            raise ValueError(f"Unable to load MP3 file: {file_path}")
        if audiofile.tag is None:
            audiofile.initTag()
        audiofile.tag.artist = artist
        audiofile.tag.save()
    except Exception as e:
        raise RuntimeError(f"Error tagging MP3 file: {e}")

async def send_song_to_telegram(file_path, title, artists):
    """
    Sends the downloaded song to the specified Telegram group and logs metadata to the database.

    Args:
        file_path (str): The path of the MP3 file.
        title (str): The title of the song.
        artists (str): The artists of the song.
    """
    # Check if the song has already been sent
    if is_song_sent(title, artists):
        print(f"Song '{title}' by {artists} has already been sent. Skipping...")
        return

    try:
        bot = Bot(token=TELEGRAM_BOT_TOKEN)
        caption = (
            f"🎶 <b>Song Found: {title}</b>\n"
            f"✨ <b>Artists:</b> {artists}\n\n"
            "<a href='https://t.me/ProjectON3'>ProjectON3</a> | @TuneDetectV2BOT"
        )
        with open(file_path, "rb") as song_file:
            print("Attempting to send song to Telegram...")
            await bot.send_audio(chat_id=TELEGRAM_GROUP_ID, audio=song_file, caption=caption, parse_mode='HTML')
            print("Song successfully sent to Telegram!")

        # Save song metadata to the database
        save_song_to_db(title, artists, file_path)

    except Exception as e:
        print(f"Error sending the song to Telegram: {e}")



# import asyncio
# async def main():
#     title = "Sooiyan (From Guddu Rangeela)"
#     artists = "Amit Trivedi, Arijit Singh, Chinmayi Sripada"

#     try:
#         # Run the blocking download_song in a thread
#         song_path = await asyncio.to_thread(download_song, title, artists)
#         print(f"Song downloaded: {song_path}")
        
#         # Call the async send_song_to_telegram
#         await send_song_to_telegram(song_path, title, artists)
#         print("Song sent to Telegram successfully!")
#     except Exception as e:
#         print(f"Error: {e}")

# if __name__ == "__main__":
#     asyncio.run(main())
