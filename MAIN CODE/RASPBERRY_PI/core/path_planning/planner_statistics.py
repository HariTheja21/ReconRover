"""
Planner Statistics Module
Recon Rover V2 - Phase 3.7
"""
import threading

class PlannerStatistics:
    def __init__(self):
        self._lock = threading.RLock()
        self.paths_generated = 0
        self.paths_optimized = 0
        
    def increment_generated(self):
        with self._lock:
            self.paths_generated += 1
            
    def increment_optimized(self):
        with self._lock:
            self.paths_optimized += 1
