import instaloader
import os
import requests

def get_first_sentence(caption: str) -> str:
    """
    Extracts the first non-empty line from a caption.
    """
    lines = caption.split('\n')
    return next((line for line in lines if line.strip()), "No caption")

def download_instagram_reel(url):
    """
    Downloads an Instagram reel if it doesn't already exist and returns the path and caption.
    """
    # Extract the shortcode from the URL
    shortcode = url.split("/")[-2]

    video_path = os.path.join('data/videos', f"{shortcode}.mp4")

    # Check if the file already exists
    if os.path.exists(video_path):
        return video_path, None

    # Initialize Instaloader
    L = instaloader.Instaloader()

    # Ensure the 'data/videos' directory exists
    save_dir = 'data/videos'
    os.makedirs(save_dir, exist_ok=True)

    try:
        # Get the post using the shortcode
        post = instaloader.Post.from_shortcode(L.context, shortcode)

        # Ensure the post is a video
        if post.is_video:
            video_url = post.video_url
            caption = get_first_sentence(post.caption or "")

            # Download the video
            response = requests.get(video_url, stream=True, timeout=10)
            response.raise_for_status()

            with open(video_path, 'wb') as video_file:
                for chunk in response.iter_content(chunk_size=8192):
                    video_file.write(chunk)

            return video_path, caption
        else:
            return None, "The provided URL does not point to a reel (video)."
    except Exception as e:
        return None, f"Error: {str(e)}"
