# Song-Recognition-Bot-V2

## Overview
Song-Recognition-Bot-V2 is a Telegram bot designed to:
1. Download videos or audio from Instagram and YouTube links.
2. Recognize songs using the AcrCloud API from uploaded files, voice messages, or provided links.
3. Retrieve and send the original song file from YouTube along with its metadata (e.g., title, artist).

The bot is optimized for concurrent user handling, fast processing, and minimal code complexity, making it efficient and scalable.

---

## Features
- **Input Options:**
  - Accepts Instagram/YouTube links, video files, audio files, and voice messages.
- **Video Download:**
  - Downloads and sends videos (up to 50MB) from Instagram/YouTube.
- **Song Recognition:**
  - Recognizes songs using AcrCloud from various input types.
- **Song Retrieval:**
  - Searches for the recognized song on YouTube and sends the original song file with detailed metadata.
- **Concurrency:**
  - Supports multiple users simultaneously through asynchronous operations.

---

## Installation

### Prerequisites
1. Python 3.8+
2. Telegram Bot Token (from [BotFather](https://core.telegram.org/bots#botfather)).
3. AcrCloud API credentials (host, access key, access secret).

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/Song-Recognition-Bot-V2.git
   cd Song-Recognition-Bot-V2
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up configuration:
   - Create a `.env` file or edit `config.py` with your:
     - Telegram bot token
     - AcrCloud API credentials

4. Run the bot:
   ```bash
   python main.py
   ```

---

## Project Structure
```
Song-Recognition-Bot-V2/
│
├── main.py                      # Entry point for the bot
├── config.py                    # Configuration file for storing constants
├── requirements.txt             # Dependencies and libraries
├── README.md                    # Project documentation
│
├── handlers/                    # Contains bot message and command handlers
│   ├── __init__.py
│   ├── message_handler.py
│   ├── command_handler.py
│
├── services/                    # Core processing services
│   ├── __init__.py
│   ├── downloader.py
│   ├── recognizer.py
│   ├── file_handler.py
│
├── utils/                       # Utility functions for validation, logging, etc.
│   ├── __init__.py
│   ├── validation.py
│   ├── helpers.py
│   ├── logger.py
│
├── data/                        # Temporary storage for processing files
│   ├── temp/
│
└── tests/                       # Unit tests for services and handlers
    ├── test_downloader.py
    ├── test_recognizer.py
```

---

## Usage
1. Start the bot with `/start`.
2. Send:
   - An Instagram or YouTube link.
   - A video, audio file, or voice message.
3. The bot will:
   - Process the input.
   - Send the video (if it’s under 50MB).
   - Recognize the song and send its file with metadata.

---

## Technologies Used
- **Python**
- **Telegram Bot API** (via `python-telegram-bot`)
- **AcrCloud API**
- **yt-dlp** (for video and audio downloads)
- **moviepy** (for audio extraction)

---

## Contributing
Feel free to submit issues or pull requests for improvements. Contributions are welcome!

---

## License
This project is licensed under the MIT License. See `LICENSE` for details.

---

## Contact
For questions or feedback, please contact [manishborikar@proton.me].
