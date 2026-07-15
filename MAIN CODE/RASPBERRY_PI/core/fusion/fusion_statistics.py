"""
Fusion Statistics Module
Recon Rover V2 - Phase 3.2
"""
import threading

class FusionStatistics:
    def __init__(self):
        self._lock = threading.RLock()
        self.events_fused = 0
        self.conflicts_resolved = 0
        
    def increment_fused(self):
        with self._lock:
            self.events_fused += 1
            
    def increment_conflicts(self):
        with self._lock:
            self.conflicts_resolved += 1
