"""
SLAM Statistics Module
Recon Rover V2 - Phase 3.5
"""
import threading

class SLAMStatistics:
    def __init__(self):
        self._lock = threading.RLock()
        self.matches_performed = 0
        self.loop_closures_found = 0
        
    def increment_match(self):
        with self._lock:
            self.matches_performed += 1
            
    def increment_loop_closure(self):
        with self._lock:
            self.loop_closures_found += 1
