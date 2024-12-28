import os
from yt_dlp import YoutubeDL

def get_first_sentence(caption: str) -> str:
    """
    Extract the first non-empty line from the provided caption.
    """
    for line in caption.split('\n'):
        stripped_line = line.strip()
        if stripped_line:
            return stripped_line
    return ""

def download_youtube_video(url):
    """
    Download a YouTube video along with its thumbnail and return the video path and first sentence of the description.
    """
    # Extract the shortcode from the URL (assumes valid YouTube URL structure)
    try:
        shortcode = url.split("/")[3].split("?")[0]
    except IndexError:
        return "Invalid URL structure", None

    # Define output paths
    video_dir = 'data/videos'
    os.makedirs(video_dir, exist_ok=True)  # Ensure the directory exists
    video_path = os.path.join(video_dir, f"{shortcode}.mp4")

    # Check if the video is already downloaded
    if os.path.exists(video_path):
        return video_path, "@TuneDetectV2BOT"

    # yt-dlp options
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',  # Download best video and audio
        'outtmpl': os.path.join(video_dir, f"{shortcode}.%(ext)s"),
        'noplaylist': True,  # Only download the video, not the playlist
        'merge_output_format': 'mp4',  # Merge into MP4 format
        'postprocessors': [
            {'key': 'FFmpegVideoConvertor', 'preferedformat': 'mp4'},
        ],
    }

    try:
        # Download the video using yt-dlp
        with YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            
            # Determine final video path
            downloaded_path = ydl.prepare_filename(info_dict)
            video_path = downloaded_path.rsplit('.', 1)[0] + '.mp4'

            # Extract the first sentence from the video description
            caption = info_dict.get('description', 'No description available')
            first_sentence = get_first_sentence(caption)

        print("YouTube Video Downloaded")
        return video_path, first_sentence
    except Exception as e:
        print(f"Error downloading video: {e}")
        return str(e), None

# # Example usage
# url = "https://youtu.be/PXGycbkbtW0?si=NqaNyI0kWmWFan7N"
# video_path, description = download_youtube_video(url)
# print(f"Downloaded video path: {video_path}\nDescription: {description}")
