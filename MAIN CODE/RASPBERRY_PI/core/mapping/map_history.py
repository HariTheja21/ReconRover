"""
Map History Module
Recon Rover V2 - Phase 3.4
"""
import threading
from collections import deque
import time

class MapHistory:
    """Tracks chronological changes to the map for rollback/undo features."""
    def __init__(self, max_snapshots=10):
        self._lock = threading.RLock()
        self.snapshots = deque(maxlen=max_snapshots)
        
    def save_snapshot(self, occupied: list, free: list):
        with self._lock:
            self.snapshots.append({
                "timestamp": time.time(),
                "occupied_count": len(occupied),
                "free_count": len(free)
            })
