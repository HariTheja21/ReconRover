"""
memory_store.py
Recon Rover V1 - Persistent Memory

CRUD abstraction over MemoryDatabase for MemoryEntry objects.
"""

import json
from typing import List, Optional
from .memory_types import MemoryEntry
from .memory_database import MemoryDatabase

class MemoryStore:
    def __init__(self, db: MemoryDatabase):
        self.db = db

    async def insert(self, entry: MemoryEntry):
        """Asynchronously writes a memory to disk."""
        query = '''
            INSERT OR REPLACE INTO memories 
            (id, timestamp, category, importance, mission_id, location, tags, summary, detailed_text, confidence, source_module)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        '''
        params = (
            entry.id, entry.timestamp, entry.category, entry.importance, 
            entry.mission_id, entry.location, json.dumps(entry.tags), 
            entry.summary, entry.detailed_text, entry.confidence, entry.source_module
        )
        await self.db.execute(query, params)

    async def get_recent(self, limit: int = 50) -> List[MemoryEntry]:
        """Fetches the most recent memories."""
        query = 'SELECT * FROM memories ORDER BY timestamp DESC LIMIT ?'
        rows = await self.db.fetchall(query, (limit,))
        return [self._row_to_entry(row) for row in rows]

    async def delete(self, entry_id: str):
        await self.db.execute('DELETE FROM memories WHERE id = ?', (entry_id,))

    def _row_to_entry(self, row: tuple) -> MemoryEntry:
        return MemoryEntry(
            id=row[0], timestamp=row[1], category=row[2], importance=row[3],
            mission_id=row[4], location=row[5], tags=json.loads(row[6]),
            summary=row[7], detailed_text=row[8], confidence=row[9], source_module=row[10]
        )
