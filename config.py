### `config.py`

from dotenv import load_dotenv
import os

# Load environment variables from a .env file
load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "your-default-telegram-bot-token")
ACRCLOUD_CONFIG = {
    "host": os.getenv("ACRCLOUD_HOST", "your-default-acrcloud-host"),
    "access_key": os.getenv("ACRCLOUD_ACCESS_KEY", "your-default-access-key"),
    "access_secret": os.getenv("ACRCLOUD_ACCESS_SECRET", "your-default-access-secret"),
}
TEMP_DIR = os.getenv("TEMP_DIR", "./data/temp/")
