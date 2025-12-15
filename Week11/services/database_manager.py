import sqlite3
from typing import Any, Iterable, Optional, List, Tuple

class DatabaseManager:
    """Handles SQLite database connections and queries."""
    
    def __init__(self, db_path: str):
        """Initialize database manager.
        
        Args:
            db_path: Path to the SQLite database file
        """
        self._db_path = db_path
        self._connection: Optional[sqlite3.Connection] = None
    
    def connect(self) -> None:
        """Establish database connection if not already connected."""
        if self._connection is None:
            self._connection = sqlite3.connect(self._db_path)
            # Enable row factory for dictionary-like access (optional)
            self._connection.row_factory = sqlite3.Row
    
    def close(self) -> None:
        """Close database connection."""
        if self._connection is not None:
            self._connection.close()
            self._connection = None
    
    def execute_query(self, sql: str, params: Iterable[Any] = ()) -> sqlite3.Cursor:
        """Execute a write query (INSERT, UPDATE, DELETE).
        
        Args:
            sql: SQL query string
            params: Parameters for the query
        
        Returns:
            Cursor object
        """
        if self._connection is None:
            self.connect()
        
        cur = self._connection.cursor()
        cur.execute(sql, tuple(params))
        self._connection.commit()
        return cur
    
    def fetch_one(self, sql: str, params: Iterable[Any] = ()) -> Optional[Tuple]:
        """Fetch a single row from a SELECT query.
        
        Args:
            sql: SQL query string
            params: Parameters for the query
        
        Returns:
            Single row as tuple or None if no results
        """
        if self._connection is None:
            self.connect()
        
        cur = self._connection.cursor()
        cur.execute(sql, tuple(params))
        return cur.fetchone()
    
    def fetch_all(self, sql: str, params: Iterable[Any] = ()) -> List[Tuple]:
        """Fetch all rows from a SELECT query.
        
        Args:
            sql: SQL query string
            params: Parameters for the query
        
        Returns:
            List of rows as tuples
        """
        if self._connection is None:
            self.connect()
        
        cur = self._connection.cursor()
        cur.execute(sql, tuple(params))
        return cur.fetchall()
    
    def __del__(self):
        """Ensure connection is closed when object is destroyed."""
        self.close()