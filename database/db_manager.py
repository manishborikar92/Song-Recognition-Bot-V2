import sqlite3
from datetime import datetime

# Database file name
DB_NAME = "song_recognition_bot.db"

class DBManager:
    def __init__(self):
        self.conn = sqlite3.connect(DB_NAME, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        """Create necessary tables if they don't exist."""
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            name TEXT,
            join_date TEXT
        )
        """)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS inputs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            input_data TEXT,
            date_time TEXT,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
        """)

        # self.cursor.execute("""
        # CREATE TABLE IF NOT EXISTS history (
        #     id INTEGER PRIMARY KEY AUTOINCREMENT,
        #     user_id INTEGER,
        #     input_data TEXT,
        #     date_time TEXT,
        #     FOREIGN KEY(user_id) REFERENCES users(id)
        # )
        # """)

        self.conn.commit()

    def add_user(self, user_id, name=None):
        """Add a new user to the database."""
        join_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.cursor.execute(
            "INSERT OR IGNORE INTO users (id, name, join_date) VALUES (?, ?, ?)",
            (user_id, name, join_date)
        )
        self.conn.commit()

    def user_exists(self, user_id):
        """Check if a user exists in the database."""
        query = "SELECT COUNT(*) FROM users WHERE id = ?"
        self.cursor.execute(query, (user_id,))
        return self.cursor.fetchone()[0] > 0

    def log_input(self, user_id, input_data):
        """Log user input into the database."""
        date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.cursor.execute(
            "INSERT INTO inputs (user_id, input_data, date_time) VALUES (?, ?, ?)",
            (user_id, input_data, date_time)
        )
        self.conn.commit()

    # def log_action(self, user_id, action):
    #     """Log user actions (commands) into the database."""
    #     date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    #     self.cursor.execute(
    #         "INSERT INTO history (user_id, action, date_time) VALUES (?, ?, ?)",
    #         (user_id, action, date_time)
    #     )
    #     self.conn.commit()

    def get_user_history(self, user_id):
        """Retrieve all history for a specific user."""
        self.cursor.execute("SELECT input_data, date_time FROM inputs WHERE user_id = ?", (user_id,))
        return self.cursor.fetchall()

    def get_all_users(self):
        """Retrieve all users."""
        self.cursor.execute("SELECT id, name FROM users")
        return self.cursor.fetchall()

    def delete_user_data(self, user_id=None):
        """Delete data for a specific user or all users."""
        if user_id:
            self.cursor.execute("DELETE FROM inputs WHERE user_id = ?", (user_id,))
            self.cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
        else:
            self.cursor.execute("DELETE FROM inputs")
            self.cursor.execute("DELETE FROM users")
        self.conn.commit()

    def close(self):
        """Close the database connection."""
        self.conn.close()

# # Example Usage
# if __name__ == "__main__":
#     db = DBManager()

#     db.add_user(12345, "John Doe")
#     db.add_user(67890, "Jane Smith")
#     db.log_input(12345, "https://example.com/song1")
#     db.log_input(67890, "Voice message input")
    
#     print(db.get_all_users())
#     db.close()
