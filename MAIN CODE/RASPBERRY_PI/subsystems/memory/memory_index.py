"""
memory_index.py
Recon Rover V1 - Persistent Memory

In-memory cache for ultra-fast semantic routing without disk I/O.
"""

from typing import List, Dict
from .memory_types import MemoryEntry

class MemoryIndex:
    def __init__(self, max_cache_size: int = 500):
        self.max_cache_size = max_cache_size
        self._cache: Dict[str, MemoryEntry] = {}

    def add(self, entry: MemoryEntry):
        """Adds to cache, evicting lowest importance if full."""
        self._cache[entry.id] = entry
        
        if len(self._cache) > self.max_cache_size:
            self._evict_lowest_importance()

    def get(self, entry_id: str) -> MemoryEntry:
        return self._cache.get(entry_id)

    def get_all(self) -> List[MemoryEntry]:
        return list(self._cache.values())

    def _evict_lowest_importance(self):
        if not self._cache:
            return
            
        # Find ID with lowest importance score
        lowest_id = min(self._cache.items(), key=lambda x: x[1].importance)[0]
        del self._cache[lowest_id]
