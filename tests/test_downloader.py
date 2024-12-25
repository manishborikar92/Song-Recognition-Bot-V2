### `tests/test_downloader.py`

import unittest
from services.downloader import download_content, download_song_from_youtube

class TestDownloader(unittest.TestCase):
    def test_valid_download(self):
        link = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        result = download_content(link)
        self.assertIsNotNone(result)

    def test_song_download(self):
        song_title = "Never Gonna Give You Up"
        result = download_song_from_youtube(song_title)
        self.assertIsNotNone(result)

if __name__ == "__main__":
    unittest.main()