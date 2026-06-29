"""
memory_embeddings.py
Recon Rover V1 - Persistent Memory

Abstraction layer for similarity search.
Currently uses basic keyword matching, future-ready for vector DBs (FAISS).
"""

from typing import List, Dict
from .memory_types import MemoryEntry

class MemoryEmbeddings:
    def __init__(self):
        pass

    def compute_similarity(self, query_tags: List[str], entry: MemoryEntry) -> float:
        """
        Placeholder for cosine similarity of vector embeddings.
        Currently performs Jaccard similarity on tags and summary keywords.
        """
        if not query_tags or not entry.tags:
            return 0.0
            
        q_set = set([q.lower() for q in query_tags])
        e_set = set([t.lower() for t in entry.tags])
        
        # Jaccard index
        intersection = len(q_set.intersection(e_set))
        union = len(q_set.union(e_set))
        
        if union == 0:
            return 0.0
            
        return float(intersection) / float(union)
