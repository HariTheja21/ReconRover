"""
memory_decay.py
Recon Rover V1 - Persistent Memory

Gradually reduces the importance of un-accessed memories over time.
"""

import time
from .memory_index import MemoryIndex

class MemoryDecay:
    def __init__(self, index: MemoryIndex):
        self.index = index

    def apply_decay(self, decay_rate: float = 0.1):
        """
        Reduces importance by a flat rate for older entries.
        Called periodically (e.g., once an hour).
        """
        current_time = time.time()
        for entry in self.index.get_all():
            age_hours = (current_time - entry.timestamp) / 3600.0
            
            if age_hours > 24.0 and entry.importance > 1.0:
                # Decay importance but don't drop below 1.0
                entry.importance = max(1.0, entry.importance - decay_rate)
