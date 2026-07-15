import sqlite3
import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class PersistentStorage:
    def __init__(self, db_path=":memory:"):
        self.db_path = db_path
        self.conn = None
        
    def connect(self):
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self._init_schema()
        
    def _init_schema(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS landmarks (
                id TEXT PRIMARY KEY,
                name TEXT,
                x REAL, y REAL, z REAL
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS objects (
                id TEXT PRIMARY KEY,
                class_name TEXT,
                x REAL, y REAL, z REAL
            )
        ''')
        self.conn.commit()
        
    def execute(self, query: str, params: tuple = ()) -> List[Dict[str, Any]]:
        cursor = self.conn.cursor()
        cursor.execute(query, params)
        if query.strip().upper().startswith("SELECT"):
            return [dict(row) for row in cursor.fetchall()]
        self.conn.commit()
        return []
        
    def close(self):
        if self.conn:
            self.conn.close()
