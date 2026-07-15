"""
Occupancy Manager Module
Recon Rover V2 - Phase 3.1
"""
import threading

class OccupancyManager:
    def __init__(self):
        self._lock = threading.RLock()
        self.grid = set()
        
    def mark_occupied(self, x: int, y: int):
        with self._lock:
            self.grid.add((x, y))
            
    def mark_free(self, x: int, y: int):
        with self._lock:
            if (x, y) in self.grid:
                self.grid.remove((x, y))
