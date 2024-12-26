import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


# Rate limit settings
USER_RATE_LIMIT = 60  # Allow 1 request per minute per user
last_request_time = {}

BOT_TOKEN = os.getenv("BOT_TOKEN")

# Group and Channel IDs
GROUP_ID = os.getenv("GROUP_ID")
CHANNEL_ID = os.getenv("CHANNEL_ID")
EXCEPTION_USER_ID = os.getenv("EXCEPTION_USER_ID")
GROUP_URL = "https://t.me/+b4-OKLiKbMoyODY1"
CHANNEL_URL = "https://t.me/ProjectON3"

# Google Drive API credentials
CLIENT_SECRET_FILE = os.getenv("GOOGLE_CLIENT_SECRET_FILE")  # Path to 'credentials.json'
SCOPES = ['https://www.googleapis.com/auth/drive.file']