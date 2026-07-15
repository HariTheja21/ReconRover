"""
Avoidance Statistics Module
Recon Rover V2 - Phase 3.8
"""
import threading

class AvoidanceStatistics:
    def __init__(self):
        self._lock = threading.RLock()
        self.collisions_predicted = 0
        self.stops_triggered = 0
        
    def increment_collision(self):
        with self._lock:
            self.collisions_predicted += 1
            
    def increment_stop(self):
        with self._lock:
            self.stops_triggered += 1
