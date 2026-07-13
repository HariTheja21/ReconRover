"""
memory_retriever.py
Recon Rover V1 - Persistent Memory

Retrieves memories based on semantic similarity and recency.
"""

import time
from typing import List, Optional
from .memory_types import MemoryEntry
from .memory_index import MemoryIndex
from .memory_embeddings import MemoryEmbeddings

class MemoryRetriever:
    def __init__(self, index: MemoryIndex, embeddings: MemoryEmbeddings):
        self.index = index
        self.embeddings = embeddings

    def retrieve_by_tags(self, tags: List[str], top_k: int = 5, min_score: float = 0.1) -> List[MemoryEntry]:
        """Finds most semantically relevant memories from the fast index."""
        scored_entries = []
        for entry in self.index.get_all():
            score = self.embeddings.compute_similarity(tags, entry)
            # Combine semantic similarity with baseline importance
            final_score = score * (entry.importance / 10.0)
            
            if final_score >= min_score:
                scored_entries.append((final_score, entry))
                
        # Sort by score descending
        scored_entries.sort(key=lambda x: x[0], reverse=True)
        return [e[1] for e in scored_entries[:top_k]]

    def retrieve_recent(self, time_window_sec: float = 300) -> List[MemoryEntry]:
        """Finds memories created within the last N seconds."""
        current_time = time.time()
        recent = []
        for entry in self.index.get_all():
            if current_time - entry.timestamp <= time_window_sec:
                recent.append(entry)
        
        recent.sort(key=lambda x: x.timestamp, reverse=True)
        return recent
