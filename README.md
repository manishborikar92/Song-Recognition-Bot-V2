# 🎵 Song Recognition Bot

A Telegram bot that helps you identify songs from instgram link, youtube link, video, audo or voice message by analyzing audio content using the ACRCloud API. The bot downloads the file, extracts audio, and provides song file with details such as title, artist, album, release date, and links usch as YouTube and Spotify. This bot also have a `/search` command to get song file.

---

## 🚀 Features

- Download Instagram reels from links shared by users.
- Extract audio from the reels.
- Identify songs using the ACRCloud API.
- Share song details with users, including title, artist, album, and release date.

---

## 🛠️ Project Structure

```plaintext
Song-Recognition-Bot/
│  
├── data/
│   ├── audios/                # Folder for temporarily storing audio files
│   ├── music/                 # Folder for temporarily storing song files
│   └── videos/                # Folder for temporarily storing video files
│
├── downloaders/ 
│   ├── instagram.py           # Functions to download Instagram video and caption
│   ├── youtube.py             # Functions to download Youtube video and caption
│   └── song.py                # Functions to download song file  
│
├── handlers/
│   ├── acrcloud_handler.py    # Functions to recognition of song
│   ├── command_handler.py     # Functions to hangle commands
│   ├── message_handler.py     # Functions to handle messages
│   └── membership_handler.py  # Functions to check channel membership of telgram
│
├── utils/
│   ├── audio_extractor.py     # Functions to extract audio
│   └── cleardata.py           # Functions to delete files
│
├── bot.py                     # Main entry point for the bot 
├── .env                       # Environment variables 
├── config.py                  # Configuration
├── Dockerfile                 # Dockerfile for easy hosting
├── requirements.txt           # List of Python dependencies
└── README.md                  # Documentation about the project
```

---

## ⚙️ Setup Instructions

### Prerequisites

- Python 3.7 or higher
- ACRCloud account and credentials
- Telegram Bot API token
- [FFmpeg](https://ffmpeg.org/) installed on your system

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/your-username/music-finder-bot.git
cd music-finder-bot
```

### 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ Configure Credentials

- **ACRCloud**: Add your credentials in `config.py`:
  ```python
  HOST = "https://identify-ap-southeast-1.acrcloud.com"
  ACCESS_KEY = "your_acrcloud_access_key"
  ACCESS_SECRET = "your_acrcloud_access_secret"
  ```
- **Telegram Bot Token**: Replace `"your_bot_token"` in `config.py` with your bot token.

### 4️⃣ Run the Bot

```bash
python bot.py
```

---

## 🧪 Testing

Run the unit tests to ensure the components work as expected:

```bash
python -m unittest discover
```

## 📖 Usage Instructions

1. Start the bot on Telegram by sending `/start`.
2. Share an instgram link, youtube link, video, audo or voice message with the bot.
3. Use `/search <song name, artist name>` command to search song 
3. The bot will:
   - Download the video.
   - Extract audio from the video.
   - Identify the song and share the song with details to you.

---

## 🛡️ License

This project is licensed under the [GNU GENERAL PUBLIC LICENSE](LICENSE).

---

## 🙌 Acknowledgements

- [ProjectON3](https://t.me/ProjectON3) bots official telgram channel.
- [ACRCloud](https://www.acrcloud.com/) for song recognition.
- [FFmpeg](https://ffmpeg.org/) for audio extraction.

---