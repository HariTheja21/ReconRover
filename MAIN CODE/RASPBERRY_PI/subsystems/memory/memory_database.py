"""
memory_database.py
Recon Rover V1 - Persistent Memory

Asynchronous SQLite backend managing tables and connection.
Requires `aiosqlite`.
"""

import aiosqlite
import asyncio
from typing import List, Tuple, Any

class MemoryDatabase:
    def __init__(self, db_path: str = "rover_memory.db"):
        self.db_path = db_path
        self._conn = None
        
    async def initialize(self):
        """Creates tables if they do not exist."""
        self._conn = await aiosqlite.connect(self.db_path)
        
        await self._conn.execute('''
            CREATE TABLE IF NOT EXISTS memories (
                id TEXT PRIMARY KEY,
                timestamp REAL,
                category TEXT,
                importance REAL,
                mission_id TEXT,
                location TEXT,
                tags TEXT,
                summary TEXT,
                detailed_text TEXT,
                confidence REAL,
                source_module TEXT
            )
        ''')
        
        # Future tables: missions, episodes, semantic, statistics, health
        
        await self._conn.execute('CREATE INDEX IF NOT EXISTS idx_memories_category ON memories (category)')
        await self._conn.execute('CREATE INDEX IF NOT EXISTS idx_memories_timestamp ON memories (timestamp)')
        await self._conn.commit()

    async def execute(self, query: str, parameters: Tuple = ()) -> Any:
        if not self._conn:
            await self.initialize()
        
        async with self._conn.execute(query, parameters) as cursor:
            await self._conn.commit()
            return cursor.lastrowid
            
    async def fetchall(self, query: str, parameters: Tuple = ()) -> List[Tuple]:
        if not self._conn:
            await self.initialize()
            
        async with self._conn.execute(query, parameters) as cursor:
            return await cursor.fetchall()
            
    async def close(self):
        if self._conn:
            await self._conn.close()
