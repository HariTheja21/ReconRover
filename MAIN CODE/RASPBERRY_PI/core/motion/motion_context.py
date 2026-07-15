"""
Motion Context Module
Recon Rover V2 - Phase 4.0
"""
import threading
from typing import Any

class MotionContext:
    def __init__(self):
        self._lock = threading.RLock()
        self.context = {
            "estop": False,
            "mission_active": False,
            "paused": False
        }
        
    def set(self, key: str, value: Any):
        with self._lock:
            self.context[key] = value
            
    def get(self, key: str, default=None) -> Any:
        with self._lock:
            return self.context.get(key, default)
