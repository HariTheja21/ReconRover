"""
Path Cache Module
Recon Rover V2 - Phase 3.7
"""
import threading
from typing import List, Tuple

class PathCache:
    """Caches previously computed paths to avoid redundant calculations."""
    def __init__(self):
        self._lock = threading.RLock()
        self.cache = {} # Dict[(start_node, end_node), path]
        
    def get(self, start: Tuple[float, float], goal: Tuple[float, float]) -> List[Tuple[float, float]]:
        with self._lock:
            # Note: in real scenarios we'd need loose coordinate matching, e.g. within 5cm radius.
            return self.cache.get((start, goal))
            
    def store(self, start: Tuple[float, float], goal: Tuple[float, float], path: List[Tuple[float, float]]):
        with self._lock:
            self.cache[(start, goal)] = path
            
    def invalidate(self):
        with self._lock:
            self.cache.clear()
