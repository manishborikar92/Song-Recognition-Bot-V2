# 🎵 Song Recognition Bot

A Telegram bot that helps you identify songs from Instagram links, YouTube links, videos, audio files, or voice messages by analyzing audio content using the ACRCloud API. The bot downloads the file, extracts audio, recognize song and provides the song file with details such as title, artist, album, release date, and links like YouTube and Spotify. This bot also features a `/search` command to get the song file.

---

## 🚀 Features

- Download videos from links shared by users.
- Send downloaded videos.
- Identify songs using the ACRCloud API.
- Share song files and details with users, including title, artist, album, release date, and links like YouTube and Spotify.
- `/search` command to fetch song files directly.

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
│   ├── instagram.py           # Functions to download Instagram videos and captions
│   ├── youtube.py             # Functions to download YouTube videos and captions
│   └── song.py                # Functions to download song files  
│
├── handlers/
│   ├── acrcloud_handler.py    # Functions for song recognition
│   ├── command_handler.py     # Functions to handle commands
│   ├── message_handler.py     # Functions to handle messages
│   └── membership_handler.py  # Functions to check Telegram channel membership
│
├── utils/
│   ├── audio_extractor.py     # Functions to extract audio
│   └── cleardata.py           # Functions to delete temporary files
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

### 1. Clone the Repository

```bash
git clone https://github.com/manishborikar92/Song-Recognition-Bot-V2.git
cd Song-Recognition-Bot-V2
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create a `.env` file in the root directory and add the following:

```env
ACR_HOST=your_acr_host_url
ACR_ACCESS_KEY=your_acrcloud_access_key
ACR_ACCESS_SECRET=your_acrcloud_access_secret
ACR_ENDPOINT_URL=https://eu-api-v2.acrcloud.com/api/external-metadata/tracks
ACR_BEARER_TOKEN=your_acrcloud_bearer_token
BOT_TOKEN=your_telegram_bot_token
GROUP_ID=-1002267600531
CHANNEL_ID=-1002213319552
EXCEPTION_USER_ID=your_user_id
WEBHOOK_URL=<insert_render_or_railway_website_url_here>
```

### 4. Run the Bot

```bash
python bot.py
```

---

## 🐳 Deploying with Docker (Optional)

### 1. Build the Docker Image

```bash
docker build -t song-recognition-bot .
```

### 2. Run the Container

```bash
docker run -d --env-file .env --name song-recognition-bot song-recognition-bot
```

---

## 🌐 Deploying on Railway

1. Create a new project on [Railway](https://railway.app/).
2. Connect your GitHub repository.
3. Add environment variables in the "Settings" section using the `.env` file values.
4. Deploy the project.

---

## 🌐 Deploying on Render

1. Create a new service on [Render](https://render.com/).
2. Select your GitHub repository.
3. Add environment variables in the "Environment" section using the `.env` file values.
4. Deploy the project.

---

## 🧪 Testing

Run the unit tests to ensure the components work as expected:

```bash
python -m unittest discover
```

## 📖 Usage Instructions

1. Start the bot on Telegram by sending `/start`.
2. Share an Instagram link, YouTube link, video, audio, or voice message with the bot.
3. Use `/search <song name, artist name>` command to search for a song.
4. The bot will:
   - Download the video from link.
   - Send video to user.
   - Identify the song and share it with details.

---

## 🛡️ License

This project is licensed under the [GNU General Public License](LICENSE).

---

## 🙌 Acknowledgements

- [ProjectON3](https://t.me/ProjectON3) - Official Telegram channel for bots.
- [ACRCloud](https://www.acrcloud.com/) - Song recognition API.
- [FFmpeg](https://ffmpeg.org/) - Audio extraction tool.

---