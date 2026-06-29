"""
ai_memory.py
Recon Rover V1 - AI Decision Engine

Maintains short-term memory of recent observations. Items automatically expire.
"""

import time
from typing import Dict, Any

class AIMemory:
    def __init__(self, expiry_seconds: float = 5.0):
        self.expiry_seconds = expiry_seconds
        self.memories: Dict[str, float] = {}

    def remember(self, key: str):
        """Records an event with the current timestamp."""
        self.memories[key] = time.perf_counter()

    def has_memory(self, key: str) -> bool:
        """Returns True if the event was observed recently."""
        self._flush_expired()
        return key in self.memories

    def _flush_expired(self):
        current_time = time.perf_counter()
        expired = [k for k, v in self.memories.items() if (current_time - v) > self.expiry_seconds]
        for k in expired:
            del self.memories[k]
