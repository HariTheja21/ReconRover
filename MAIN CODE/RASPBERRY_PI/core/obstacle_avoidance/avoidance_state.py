"""
Avoidance State Module
Recon Rover V2 - Phase 3.8
"""
import threading

class AvoidanceState:
    SAFE = "SAFE"
    AVOIDING = "AVOIDING"
    EMERGENCY_STOP = "EMERGENCY_STOP"
    
    def __init__(self):
        self._lock = threading.RLock()
        self.state = self.SAFE
        
    def set(self, new_state: str):
        with self._lock:
            self.state = new_state
            
    def get(self) -> str:
        with self._lock:
            return self.state
