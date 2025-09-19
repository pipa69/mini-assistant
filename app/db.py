import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), "assistant_logs.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT,
        query TEXT,
        response TEXT,
        intent TEXT,
        confidence REAL,
        created_at TEXT
    );""")
    conn.commit()
    conn.close()

def log_interaction(user_id, query, response, intent, confidence):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("INSERT INTO logs (user_id, query, response, intent, confidence, created_at) VALUES (?, ?, ?, ?, ?, ?)",
                (user_id, query, response, intent, confidence, datetime.utcnow().isoformat()))
    conn.commit()
    conn.close()

init_db()
