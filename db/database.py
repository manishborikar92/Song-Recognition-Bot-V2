import sqlite3
import os

# Ensure the 'db' folder exists
os.makedirs("db", exist_ok=True)

# Connect to the SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect("db/songs.db")

# Create a cursor object to interact with the database
cursor = conn.cursor()

# Create the table for storing song metadata (if not already exists)
cursor.execute("""
CREATE TABLE IF NOT EXISTS songs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    artists TEXT NOT NULL,
    file_path TEXT NOT NULL
);
""")

# Commit changes and close the connection
conn.commit()
conn.close()

import sqlite3
from telegram import Bot

def is_song_sent(title, artists):
    """
    Checks if the song with the given title and artists has already been sent.

    Args:
        title (str): The title of the song.
        artists (str): The artists of the song.

    Returns:
        bool: True if the song has already been sent, False otherwise.
    """
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect("db/songs.db")
        cursor = conn.cursor()

        # Query the database for a song with the same title and artists
        cursor.execute("""
        SELECT 1 FROM songs WHERE title = ? AND artists = ?;
        """, (title.lower(), artists.lower()))  # Use lower() for case-insensitive matching

        # Check if any result was returned (1 means the song exists)
        song_exists = cursor.fetchone() is not None

        # Close the connection
        conn.close()

        return song_exists
    except Exception as e:
        print(f"Error checking if song is already sent: {e}")
        return False

def save_song_to_db(title, artists, file_path):
    """
    Saves the song metadata to the database.

    Args:
        title (str): The title of the song.
        artists (str): The artists of the song.
        file_path (str): The file path of the song.
    """
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect("db/songs.db")
        cursor = conn.cursor()

        # Insert the song metadata into the database
        cursor.execute("""
        INSERT INTO songs (title, artists, file_path)
        VALUES (?, ?, ?);
        """, (title, artists, file_path))

        # Commit the changes and close the connection
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Error saving song to database: {e}")