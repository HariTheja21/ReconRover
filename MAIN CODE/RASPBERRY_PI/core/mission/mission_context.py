"""
Mission Context Module
Recon Rover V2 - Phase 3.9
"""
import threading
from typing import Dict, Any

class MissionContext:
    """Holds global execution state independent of the active mission."""
    def __init__(self):
        self._lock = threading.RLock()
        self.global_state = {
            "pose": (0.0, 0.0, 0.0),
            "emergency_stop": False,
            "navigation_state": "IDLE"
        }
        
    def update(self, key: str, value: Any):
        with self._lock:
            self.global_state[key] = value
            
    def get(self, key: str, default=None) -> Any:
        with self._lock:
            return self.global_state.get(key, default)
