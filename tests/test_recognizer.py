import unittest
from services.recognizer import recognize_song

class TestRecognizer(unittest.TestCase):
    def test_song_recognition(self):
        file_path = "test_audio.mp3"
        result = recognize_song(file_path)
        self.assertIn("metadata", result)

if __name__ == "__main__":
    unittest.main()