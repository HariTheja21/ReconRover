"""
Motion Statistics Module
Recon Rover V2 - Phase 4.0
"""
import threading

class MotionStatistics:
    def __init__(self):
        self._lock = threading.RLock()
        self.requests_processed = 0
        self.limits_applied = 0
        
    def increment_processed(self):
        with self._lock:
            self.requests_processed += 1
            
    def increment_limited(self):
        with self._lock:
            self.limits_applied += 1
