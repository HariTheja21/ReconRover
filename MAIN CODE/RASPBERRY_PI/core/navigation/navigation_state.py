"""
Navigation State Module
Recon Rover V2 - Phase 3.6
"""
import threading

class NavigationState:
    """Tracks the high-level state machine of the navigation core."""
    IDLE = "IDLE"
    NAVIGATING = "NAVIGATING"
    REACHED = "REACHED"
    FAILED = "FAILED"
    
    def __init__(self):
        self._lock = threading.RLock()
        self.current_state = self.IDLE
        
    def set_state(self, state: str):
        with self._lock:
            self.current_state = state
            
    def get_state(self) -> str:
        with self._lock:
            return self.current_state
