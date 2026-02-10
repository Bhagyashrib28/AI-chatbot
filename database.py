import sqlite3

DB_NAME = "chat_logs.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    # Stores the conversation history for auditing/analytics
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            user_msg TEXT,
            bot_res TEXT
        )
    ''')
    conn.commit()
    conn.close()

def log_interaction(user_msg, bot_res):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO logs (user_msg, bot_res) VALUES (?, ?)", (user_msg, bot_res))
    conn.commit()
    conn.close()