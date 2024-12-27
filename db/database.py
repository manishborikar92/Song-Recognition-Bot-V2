import sqlite3

def init_db():
    conn = sqlite3.connect("db/data/users.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            state TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_user(user_id, username):
    conn = sqlite3.connect("db/data/users.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR IGNORE INTO users (user_id, username, state)
        VALUES (?, ?, ?)
    """, (user_id, username, None))
    conn.commit()
    conn.close()

def update_state(user_id, state):
    conn = sqlite3.connect("db/data/users.db")
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE users SET state = ?
        WHERE user_id = ?
    """, (state, user_id))
    conn.commit()
    conn.close()

def get_state(user_id):
    conn = sqlite3.connect("db/data/users.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT state FROM users WHERE user_id = ?
    """, (user_id,))
    result = cursor.fetchone()
    conn.close()
    return result [0] if result else None

init_db()

# update_state(100, "Second message")
# data = get_state(100)
# print(data)