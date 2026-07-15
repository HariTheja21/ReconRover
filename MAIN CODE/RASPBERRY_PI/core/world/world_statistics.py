"""
World Statistics Module
Recon Rover V2 - Phase 3.1
"""
import threading

class WorldStatistics:
    def __init__(self):
        self._lock = threading.RLock()
        self.events_processed = 0
        
    def increment(self):
        with self._lock:
            self.events_processed += 1
