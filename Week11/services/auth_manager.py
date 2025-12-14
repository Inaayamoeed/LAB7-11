import hashlib
from typing import Optional
from models.user import User
from services.database_manager import DatabaseManager

class SimpleHasher:
    """Simple password hasher using SHA256 (for demo/learning only).
    
    WARNING: In production, use bcrypt, argon2, or scrypt instead!
    """
    
    @staticmethod
    def hash_password(plain: str) -> str:
        """Hash a plain-text password.
        
        Args:
            plain: Plain-text password
        
        Returns:
            SHA256 hash of the password
        """
        return hashlib.sha256(plain.encode("utf-8")).hexdigest()
    
    @staticmethod
    def check_password(plain: str, hashed: str) -> bool:
        """Verify a plain-text password against a hash.
        
        Args:
            plain: Plain-text password
            hashed: Hashed password to compare against
        
        Returns:
            True if password matches, False otherwise
        """
        return SimpleHasher.hash_password(plain) == hashed


class AuthManager:
    """Handles user registration and login authentication."""
    
    def __init__(self, db: DatabaseManager):
        """Initialize auth manager with a database connection.
        
        Args:
            db: DatabaseManager instance
        """
        self._db = db
        self._hasher = SimpleHasher()
    
    def register_user(self, username: str, password: str, role: str = "user") -> bool:
        """Register a new user.
        
        Args:
            username: Username for the new user
            password: Plain-text password (will be hashed)
            role: User role (default: "user")
        
        Returns:
            True if registration successful, False otherwise
        """
        try:
            # Check if user already exists
            existing = self._db.fetch_one(
                "SELECT username FROM users WHERE username = ?",
                (username,),
            )
            if existing is not None:
                return False  # User already exists
            
            # Hash password and insert user
            password_hash = self._hasher.hash_password(password)
            self._db.execute_query(
                "INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
                (username, password_hash, role),
            )
            return True
        except Exception as e:
            print(f"Registration error: {e}")
            return False
    
    def login_user(self, username: str, password: str) -> Optional[User]:
        """Authenticate a user and return User object if successful.
        
        Args:
            username: Username to login
            password: Plain-text password
        
        Returns:
            User object if login successful, None otherwise
        """
        try:
            row = self._db.fetch_one(
                "SELECT username, password_hash, role FROM users WHERE username = ?",
                (username,),
            )
            if row is None:
                return None
            
            username_db, password_hash_db, role_db = row
            
            if self._hasher.check_password(password, password_hash_db):
                return User(username_db, password_hash_db, role_db)
            
            return None
        except Exception as e:
            print(f"Login error: {e}")
            return None
    
    def change_password(self, username: str, old_password: str, new_password: str) -> bool:
        """Change a user's password.
        
        Args:
            username: Username
            old_password: Current password (for verification)
            new_password: New password
        
        Returns:
            True if password changed, False otherwise
        """
        try:
            # Verify old password
            user = self.login_user(username, old_password)
            if user is None:
                return False
            
            # Update to new password
            new_hash = self._hasher.hash_password(new_password)
            self._db.execute_query(
                "UPDATE users SET password_hash = ? WHERE username = ?",
                (new_hash, username),
            )
            return True
        except Exception as e:
            print(f"Password change error: {e}")
            return False