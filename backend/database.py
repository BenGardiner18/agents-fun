import psycopg2
import psycopg2.extras
from contextlib import contextmanager
from typing import Dict, Any, Optional
import os

# Database configuration
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", "5432")),
    "user": os.getenv("DB_USER", "crmuser"),
    "password": os.getenv("DB_PASSWORD", "crmsecret"),
    "dbname": os.getenv("DB_NAME", "crm")
}

class DatabaseManager:
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or DB_CONFIG
    
    def get_connection(self):
        """Get a database connection"""
        conn = psycopg2.connect(**self.config)
        conn.autocommit = True
        return conn
    
    @contextmanager
    def get_cursor(self):
        """Context manager for database cursor"""
        conn = self.get_connection()
        try:
            cur = conn.cursor()
            yield cur
        finally:
            conn.close()
    
    def row_to_dict(self, row, cursor):
        """Convert database row to dictionary"""
        if row is None:
            return None
        return dict(zip([desc[0] for desc in cursor.description], row))
    
    def execute_query(self, query: str, params: tuple = None):
        """Execute a query and return results"""
        with self.get_cursor() as cur:
            cur.execute(query, params)
            return cur.fetchall(), cur
    
    def execute_single(self, query: str, params: tuple = None):
        """Execute a query and return single result"""
        with self.get_cursor() as cur:
            cur.execute(query, params)
            return cur.fetchone(), cur
    
    def execute_insert(self, query: str, params: tuple = None):
        """Execute an insert query and return the inserted record"""
        with self.get_cursor() as cur:
            cur.execute(query, params)
            return cur.fetchone(), cur
    
    def execute_update(self, query: str, params: tuple = None):
        """Execute an update query and return the updated record"""
        with self.get_cursor() as cur:
            cur.execute(query, params)
            return cur.fetchone(), cur
    
    def execute_delete(self, query: str, params: tuple = None):
        """Execute a delete query and return row count"""
        with self.get_cursor() as cur:
            cur.execute(query, params)
            return cur.rowcount

# Global database manager instance
db_manager = DatabaseManager()

# Helper functions for common database operations
def get_db():
    """Get database connection (for backwards compatibility)"""
    return db_manager.get_connection()

def row_to_dict(row, cursor):
    """Convert row to dict (for backwards compatibility)"""
    return db_manager.row_to_dict(row, cursor) 