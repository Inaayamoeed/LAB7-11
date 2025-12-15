import sqlite3
from pathlib import Path

def initialize_database(db_path: str = "database/platform.db") -> None:
    """Initialize the database with required tables."""
    Path(db_path).parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    # Users table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT DEFAULT 'user',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Security incidents table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS security_incidents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            incident_type TEXT NOT NULL,
            severity TEXT NOT NULL,
            status TEXT DEFAULT 'Open',
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Datasets table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS datasets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            size_bytes INTEGER,
            rows INTEGER,
            source TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # IT Tickets table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS it_tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            priority TEXT NOT NULL,
            status TEXT DEFAULT 'Open',
            assigned_to TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # ✅ Chat History table (for AI Assistant pages)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS chat_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            domain TEXT NOT NULL,
            user_message TEXT NOT NULL,
            assistant_message TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()
    print(f"Database initialized at {db_path}")

if __name__ == "__main__":
    initialize_database()
