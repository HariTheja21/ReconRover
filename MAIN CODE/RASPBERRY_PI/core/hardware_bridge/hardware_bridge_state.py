"""
Hardware Bridge State Module
Recon Rover V2 - Phase 4.2
"""
import threading

class HardwareBridgeState:
    IDLE = "IDLE"
    ACTIVE = "ACTIVE"
    ESTOP = "ESTOP"
    
    def __init__(self):
        self._lock = threading.RLock()
        self.state = self.IDLE
        
    def set(self, new_state: str):
        with self._lock:
            self.state = new_state
            
    def get(self) -> str:
        with self._lock:
            return self.state
