"""
memory_manager.py
Recon Rover V1 - Persistent Memory

Coordinates all memory subsystems.
"""

from typing import List
from .memory_types import MemoryEntry
from .memory_database import MemoryDatabase
from .memory_store import MemoryStore
from .memory_index import MemoryIndex
from .memory_embeddings import MemoryEmbeddings
from .memory_writer import MemoryWriter
from .memory_retriever import MemoryRetriever
from .memory_summarizer import MemorySummarizer
from .memory_decay import MemoryDecay
from .memory_health import MemoryHealth
from .memory_statistics import MemoryStatistics

class MemoryManager:
    def __init__(self):
        self.db = MemoryDatabase()
        self.store = MemoryStore(self.db)
        self.index = MemoryIndex()
        self.embeddings = MemoryEmbeddings()
        
        self.writer = MemoryWriter(self.store, self.index)
        self.retriever = MemoryRetriever(self.index, self.embeddings)
        self.summarizer = MemorySummarizer(self.store, self.index)
        self.decay = MemoryDecay(self.index)
        
        self.health = MemoryHealth()
        self.stats = MemoryStatistics()

    async def initialize(self):
        """Pre-warms the index from the database."""
        await self.db.initialize()
        recent = await self.store.get_recent(limit=500)
        for entry in recent:
            self.index.add(entry)

    async def write_memory(self, entry: MemoryEntry):
        try:
            await self.writer.write(entry)
            self.stats.record_write()
            self.health.record_success()
        except Exception as e:
            self.health.record_error()

    def retrieve_by_tags(self, tags: List[str]) -> List[MemoryEntry]:
        self.stats.record_retrieval()
        return self.retriever.retrieve_by_tags(tags)

    async def run_maintenance(self):
        """Runs slow maintenance tasks like summarization and decay."""
        self.decay.apply_decay()
        self.stats.record_decay()
        
        await self.summarizer.run_summarization_pass()
        self.stats.record_summarization()
