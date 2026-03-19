"""
Database module for MySQL operations.
Handles all database connections and operations.
"""

from sqlalchemy import create_engine, text, MetaData
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
from typing import List, Dict, Any, Optional
import json
from config import config


class DatabaseManager:
    """Manages database connections and operations."""
    
    def __init__(self):
        self.engine = create_engine(config.DATABASE_URL, echo=False)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        self.metadata = MetaData()
    
    @contextmanager
    def get_session(self):
        """Context manager for database sessions."""
        session = self.SessionLocal()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
    
    @contextmanager
    def get_connection(self):
        """Context manager for database connections."""
        conn = self.engine.connect()
        try:
            yield conn
        finally:
            conn.close()
    
    def execute_query(self, query: str, params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Execute a SQL query and return results as list of dictionaries."""
        try:
            with self.get_connection() as conn:
                result = conn.execute(text(query), params or {})
                rows = result.fetchall()
                columns = result.keys()
                
                return [dict(zip(columns, row)) for row in rows]
        except Exception as e:
            print(f"❌ Database query error: {e}")
            return [{"error": str(e)}]
    
    def execute_single_query(self, query: str, params: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
        """Execute a SQL query and return single result as dictionary."""
        try:
            with self.get_connection() as conn:
                result = conn.execute(text(query), params or {})
                row = result.fetchone()
                
                if row:
                    columns = result.keys()
                    return dict(zip(columns, row))
                return None
        except Exception as e:
            print(f"❌ Database query error: {e}")
            return {"error": str(e)}
    
    def test_connection(self) -> bool:
        """Test database connection."""
        try:
            with self.get_connection() as conn:
                result = conn.execute(text("SELECT 1"))
                row = result.fetchone()
                return row[0] == 1
        except Exception as e:
            print(f"❌ Database connection test failed: {e}")
            return False


# Create a global database manager instance
db_manager = DatabaseManager()


# User-specific database operations
class UserRepository:
    """Repository for user-related database operations."""
    
    def __init__(self, db_manager: DatabaseManager = db_manager):
        self.db_manager = db_manager
    
    def get_user_by_id(self, user_id: int) -> Dict[str, Any]:
        """Get user by ID."""
        query = "SELECT * FROM users WHERE userId = :user_id"
        result = self.db_manager.execute_single_query(query, {"user_id": user_id})
        
        if not result:
            return {"error": "User not found"}
        
        return result
    
    def get_all_users(self) -> List[Dict[str, Any]]:
        """Get all users."""
        query = "SELECT * FROM users"
        return self.db_manager.execute_query(query)
    
    def get_high_risk_users(self, credit_threshold: int = 650) -> List[Dict[str, Any]]:
        """Get users with credit score below threshold."""
        query = "SELECT * FROM users WHERE creditScore < :threshold"
        return self.db_manager.execute_query(query, {"threshold": credit_threshold})
    
    def get_users_with_multiple_loans(self, min_loans: int = 1) -> List[Dict[str, Any]]:
        """Get users with more than minimum number of loans."""
        query = "SELECT * FROM users WHERE existingLoans > :min_loans"
        return self.db_manager.execute_query(query, {"min_loans": min_loans})
    
    def get_user_count(self) -> int:
        """Get total number of users."""
        query = "SELECT COUNT(*) as count FROM users"
        result = self.db_manager.execute_single_query(query)
        return result.get("count", 0) if result else 0


# Create global user repository instance
user_repository = UserRepository()
