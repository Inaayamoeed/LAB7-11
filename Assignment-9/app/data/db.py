import sqlite3

def connect_database(db_path="DATA/intelligence_platform.db"):
    conn = sqlite3.connect(db_path)
    return conn
