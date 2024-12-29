import os
import hashlib
import yt_dlp
import subprocess

def generate_unique_filename(url, ext="mp4"):
    """
    Generate a unique filename based on the URL hash.
    
    Args:
        url (str): The URL of the video.
        ext (str): The file extension (default is 'mp4' for video).
    
    Returns:
        str: Unique filename based on the URL hash.
    """
    hash_object = hashlib.md5(url.encode())
    unique_hash = hash_object.hexdigest()
    return f"{unique_hash}.{ext}"

def download_and_extract(url):
    """
    Downloads video from Instagram or YouTube, converts it to audio,
    and returns the paths for both video and audio.
    
    Args:
        url (str): URL of the Instagram or YouTube post.
    
    Returns:
        tuple: Paths to the downloaded video and extracted audio, or error message if failed.
    """
    # Define output directories for video and audio
    video_dir = 'data/video'
    audio_dir = 'data/audio'
    
    # Create directories if they don't exist
    os.makedirs(video_dir, exist_ok=True)
    os.makedirs(audio_dir, exist_ok=True)

    # Generate unique video and audio file names
    video_file_name = generate_unique_filename(url, "mp4")
    video_file_path = os.path.join(video_dir, video_file_name)
    audio_file_path = os.path.join(audio_dir, video_file_name.rsplit('.', 1)[0] + '.mp3')  # Audio as .mp3

    # Check if video and audio files already exist
    if os.path.exists(video_file_path) and os.path.exists(audio_file_path):
        return video_file_path, audio_file_path

    # Define options for yt-dlp to download the video
    options = {
        'format': 'bestvideo[height<=360]+bestaudio/best[height<=360]',  # Download video at 360p quality
        'outtmpl': f'{video_dir}/{video_file_name}',  # Save video in data/video folder
        'noplaylist': True,  # Only download the single video
        'cookiefile': 'youtube_cookies.txt',
    }

    try:
        # Download the video using yt-dlp
        with yt_dlp.YoutubeDL(options) as ydl:
            info_dict = ydl.extract_info(url, download=False)  # Get video info without downloading
            formats = info_dict.get('formats', [])

            # Find the best format under 50MB
            selected_format = None
            for f in formats:
                filesize = f.get('filesize')
                if filesize and filesize <= 50 * 1024 * 1024:  # 50MB in bytes
                    selected_format = f
                    break
            
            if selected_format:
                # Update options to download the selected format
                options['format'] = selected_format['format_id']
                with yt_dlp.YoutubeDL(options) as ydl:
                    ydl.download([url])
            else:
                # If no suitable format is found under 50MB, download the best format available
                print("No format under 50MB, downloading the best available format.")
                with yt_dlp.YoutubeDL(options) as ydl:
                    ydl.download([url])
                
    except Exception as e:
        return f"Error downloading video: {e}"

    # Check if the video file is downloaded
    if not os.path.exists(video_file_path):
        return "Error: Video download failed."

    # Extract the audio using ffmpeg
    try:
        ffmpeg_command = ['ffmpeg', '-i', video_file_path, '-vn', '-acodec', 'libmp3lame', '-ab', '192k', audio_file_path]
        subprocess.run(ffmpeg_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    except subprocess.CalledProcessError as e:
        return f"Error extracting audio: {e}"

    # Check if the audio file is extracted
    if not os.path.exists(audio_file_path):
        return "Error: Audio extraction failed."

    # Return paths for both video and audio
    return video_file_path, audio_file_path

# # Example usage
# url = "https://www.instagram.com/reel/C--Od2xymKj/"  # Replace with your Instagram or YouTube URL

# result = download_and_extract(url)

# # Check if result is a tuple (video_path, audio_path) or an error string
# if isinstance(result, tuple):
#     video_path, audio_path = result
#     print(f"Video saved at: {video_path}")
#     print(f"Audio saved at: {audio_path}")
# else:
#     # In case of error
#     print(result)
