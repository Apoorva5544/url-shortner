import sqlite3
from datetime import datetime

DB_PATH = "urls.db"

def get_db():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS urls (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            code TEXT UNIQUE,
            original_url TEXT,
            clicks INTEGER DEFAULT 0,
            created_at TEXT
        );
    """)
    conn.commit()
    conn.close()
