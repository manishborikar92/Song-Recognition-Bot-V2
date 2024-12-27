import instaloader
import os
import requests
from utils.search_files import search_file

def get_first_sentence(caption: str) -> str:
    # Split the caption by line breaks and get the first non-empty line
    lines = caption.split('\n')
    first_line = next((line for line in lines if line.strip()), "")  # Find the first non-empty line
    return first_line

def download_instagram_reel(url):
    # Extract the shortcode from the URL
    shortcode = url.split("/")[-2]

    # Paths for saving the video and audio
    video_path = os.path.join('data/videos', f"{shortcode}.mp4")

    # Check if the files already exist
    if os.path.exists(video_path):
        return video_path, "@TuneDetectV2BOT"
      
    # Initialize Instaloader
    L = instaloader.Instaloader()
    
    # Ensure the 'temp/videos' directory exists
    save_dir = f'data/videos'
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    
    # Extract the shortcode from the URL
    shortcode = url.split("/")[-2]
    

    # Get the post using the shortcode
    try:
        post = instaloader.Post.from_shortcode(L.context, shortcode)
        
        # Check if it's a Reel (video post)
        if post.is_video:
            # Get video URL
            video_url = post.video_url
            caption = post.caption if post.caption else "No caption"
            
            # Get the first non-empty line of the caption
            first_sentence = get_first_sentence(caption)
            
            # Define the file path to save the video
            video_path = os.path.join(save_dir, f"{shortcode}.mp4")
            
            # Download the video (fast, using requests to stream the video)
            response = requests.get(video_url, stream=True)
            with open(video_path, 'wb') as video_file:
                for chunk in response.iter_content(chunk_size=8192):
                    video_file.write(chunk)
                    
            print('Instagram Video Downloaded')
            return video_path, first_sentence
        else:
            raise ValueError("The provided URL does not point to a reel (video).")
    except Exception as e:
        return None, None

# # Example usage
# url = "https://www.instagram.com/reel/DDMhHzkT6m3/?igsh=ZW1yYndoN2piZGM4"
# video_path, caption = download_instagram_reel(url)
# print(f"Downloaded video path: {video_path}\nCaption: {caption}")
