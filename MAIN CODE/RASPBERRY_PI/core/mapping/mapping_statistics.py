"""
Mapping Statistics Module
Recon Rover V2 - Phase 3.4
"""
import threading

class MappingStatistics:
    def __init__(self):
        self._lock = threading.RLock()
        self.events_processed = 0
        self.cells_updated = 0
        
    def increment_processed(self):
        with self._lock:
            self.events_processed += 1
            
    def increment_cells(self, count: int = 1):
        with self._lock:
            self.cells_updated += count
