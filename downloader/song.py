import os
import re
import eyed3
import yt_dlp
import subprocess

def generate_song_filename(song_name, ext="mp3"):
    """
    Generate a filename based on the song name and artist name, with invalid characters removed.
    """
    # Remove invalid characters for Windows filenames
    invalid_chars = r'[<>:"/\\|?*]'
    sanitized_song_name = re.sub(invalid_chars, '', song_name)

    return f"{sanitized_song_name}.{ext}"

def download_song(song_name, artist_name):
    """
    Downloads the song, re-encodes to MP3 if necessary, and tags the artist.
    """
    music_dir = 'data/music'
    os.makedirs(music_dir, exist_ok=True)

    # Generate the filename based on the song name and artist
    filename = generate_song_filename(song_name)
    file_path = os.path.join(music_dir, filename)

    # Check if the song already exists
    if os.path.exists(file_path):
        print(f"Song already exists at {file_path}")
        return file_path

    # Define yt-dlp options for downloading the song
    options = {
        'format': 'bestaudio/best',
        'extractaudio': True,
        'audioquality': 1,
        'outtmpl': file_path,  # Save with the correct filename
        'noplaylist': True,
        'cookiefile': 'youtube_cookies.txt',
    }

    search_query = f"{song_name} {artist_name}" if artist_name else song_name
    print(f"Searching and downloading: {search_query}")

    try:
        # Download the song using yt-dlp
        with yt_dlp.YoutubeDL(options) as ydl:
            ydl.download([f"ytsearch:{search_query}"])

        # Re-encode the audio to ensure it is a valid MP3 format
        print(f"Re-encoding {file_path} to proper MP3 format...")
        reencoded_file_path = os.path.join(music_dir, "reencoded_" + filename)
        ffmpeg_command = ['ffmpeg', '-i', file_path, '-vn', '-acodec', 'libmp3lame', '-ab', '192k', reencoded_file_path]
        subprocess.run(ffmpeg_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # Remove the original downloaded file if re-encoding is successful
        if os.path.exists(reencoded_file_path):
            os.remove(file_path)  # Remove the original file
            os.rename(reencoded_file_path, file_path)  # Rename the re-encoded file to the original name


        # Remove the original downloaded file if re-encoding is successful
        if os.path.exists(reencoded_file_path):
            os.remove(file_path)  # Remove original file
            file_path = reencoded_file_path  # Use the re-encoded file path

        print(f"Loading MP3 file {file_path} for tagging...")

        # Load the MP3 file using eyed3
        audio_file = eyed3.load(file_path)
        if audio_file is None:
            print("Error: Failed to load the MP3 file.")
            return "Error: Failed to load the MP3 file."

        # Edit the artist tag using eyed3
        if artist_name:
            audio_file.tag.artist = artist_name
        else:
            audio_file.tag.artist = "Unknown Artist"

        # Save the tag
        audio_file.tag.save()

        print(f"Song saved and tagged at: {file_path}")
        # Return the path to the downloaded song
        return file_path

    except Exception as e:
        print(f"Error during download or file processing: {e}")
        return f"Error: {e}"

# # Example usage
# song_name = 'Sooiyan (From "Guddu Rangeela")'  # Replace with the song name
# artist_name = "Amit Trivedi, Arijit Singh, Chinmayi Sripada"  # Replace with the artist name (optional)

# song_path = download_song(song_name, artist_name)

# print(f"Song saved at: {song_path}")
