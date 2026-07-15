"""
Planner State Module
Recon Rover V2 - Phase 3.7
"""
import threading

class PlannerState:
    IDLE = "IDLE"
    COMPUTING = "COMPUTING"
    READY = "READY"
    FAILED = "FAILED"
    
    def __init__(self):
        self._lock = threading.RLock()
        self.state = self.IDLE
        
    def set(self, new_state: str):
        with self._lock:
            self.state = new_state
            
    def get(self) -> str:
        with self._lock:
            return self.state
