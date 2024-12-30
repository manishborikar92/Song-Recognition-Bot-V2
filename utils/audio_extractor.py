import os
from pydub import AudioSegment

def convert_video_to_mp3(video_path):
    try:
        # Define the directory to save audio files
        save_dir = 'data/audios'
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)  # Create the directory if it doesn't exist

        # Get the video filename without extension
        video_filename = os.path.basename(video_path)
        audio_filename = os.path.splitext(video_filename)[0] + '.mp3'  # Change extension to .mp3
        audio_path = os.path.join(save_dir, audio_filename)
        
        # Check if the audio already exists
        if os.path.exists(audio_path):
            print(f"Audio already exists at: {audio_path}")
            return audio_path
        
        # Convert video to audio using ffmpeg (via pydub)
        # Load the video file (pydub supports mp4 if ffmpeg is correctly installed)
        audio = AudioSegment.from_file(video_path, format='mp4')  # 'mp4' is the video format
        
        # Export the audio as mp3
        audio.export(audio_path, format='mp3')
        
        print(f'Audio Extracted at: {audio_path}')
        return audio_path

    except Exception as e:
        print(f"Error: {e}")
        return str(e)

# # Example usage
# video_path = 'data/videos/Q-FzRg6V-b4.mp4'
# audio_path = convert_video_to_mp3(video_path)
# print(f"Converted audio path: {audio_path}")
