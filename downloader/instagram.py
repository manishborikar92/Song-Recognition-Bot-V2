import os
import requests
import instaloader

def get_first_sentence(caption: str) -> str:
    """Get the first non-empty line from the caption."""
    lines = caption.split('\n')
    first_line = next((line for line in lines if line.strip()), "")  # Find the first non-empty line
    return first_line

def download_instagram_reel(url):
    # Initialize Instaloader
    L = instaloader.Instaloader()
    
    # Define the directory to save videos
    save_dir = 'data/videos'
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)  # Create the directory if it doesn't exist
    
    # Extract the shortcode from the URL
    try:
        shortcode = url.split("/")[-2]
        if not shortcode:
            raise ValueError("Invalid Instagram URL. Could not extract shortcode.")
    except IndexError:
        return None, "Invalid URL format."

    # Define the file path for the video
    video_path = os.path.join(save_dir, f"{shortcode}.mp4")
    
    # Check if the video already exists
    if os.path.exists(video_path):
        print(f"Instagram video already exists at {video_path}")
        return video_path, "Video already exists."

    # Fetch the post using the shortcode
    try:
        post = instaloader.Post.from_shortcode(L.context, shortcode)
        
        # Check if it's a Reel (video post)
        if post.is_video:
            # Get the video URL
            video_url = post.video_url
            caption = post.caption if post.caption else "No caption"
            
            # Get the first non-empty line of the caption
            first_sentence = get_first_sentence(caption)
            
            # Download the video using requests
            response = requests.get(video_url, stream=True)
            response.raise_for_status()  # Raise an exception for HTTP errors
            with open(video_path, 'wb') as video_file:
                for chunk in response.iter_content(chunk_size=8192):
                    video_file.write(chunk)
                    
            print('Instagram Reel Downloaded')
            return video_path, first_sentence
        else:
            return None, "The provided URL does not point to a reel (video)."
    except Exception as e:
        print(f"Error: {e}")
        return None, str(e)

# Example usage
url = "https://www.instagram.com/reel/DDMhHzkT6m3/?igshid=ZW1yYndoN2piZGM4"
video_path, caption = download_instagram_reel(url)
print(f"Downloaded video path: {video_path}\nCaption: {caption}")
