"""
memory_writer.py
Recon Rover V1 - Persistent Memory

Transforms events into MemoryEntry objects and routes them to the store/index.
"""

from .memory_types import MemoryEntry
from .memory_store import MemoryStore
from .memory_index import MemoryIndex

class MemoryWriter:
    def __init__(self, store: MemoryStore, index: MemoryIndex):
        self.store = store
        self.index = index

    async def write(self, entry: MemoryEntry):
        """Asynchronously writes to disk and caches in index."""
        # Add to fast index
        self.index.add(entry)
        
        # Persist to SQLite
        await self.store.insert(entry)
