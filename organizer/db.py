# db.py
import sqlite3
from config import DATABASE_NAME

def get_connection(db_path=DATABASE_NAME):
    return sqlite3.connect(db_path)

def init_db(db_path=DATABASE_NAME):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS files (
            id INTEGER PRIMARY KEY,
            file_path TEXT,
            file_name TEXT,
            file_extension TEXT,
            file_size INTEGER,
            created_time TEXT,
            modified_time TEXT,
            accessed_time TEXT,
            metadata TEXT,
            file_hash TEXT
        )
    ''')
    conn.commit()
    return conn

