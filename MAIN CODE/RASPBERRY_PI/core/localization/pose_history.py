"""
Pose History Module
Recon Rover V2 - Phase 3.3
"""
import threading
import time
from collections import deque

class PoseHistory:
    """Maintains a sliding window of recent robot poses."""
    def __init__(self, max_length=1000):
        self._lock = threading.RLock()
        self.history = deque(maxlen=max_length)
        
    def add_pose(self, x: float, y: float, theta: float, confidence: float):
        with self._lock:
            self.history.append({
                "x": x,
                "y": y,
                "theta": theta,
                "confidence": confidence,
                "timestamp": time.time()
            })
            
    def get_recent(self) -> dict:
        with self._lock:
            if not self.history:
                return None
            return self.history[-1]
            
    def get_size(self) -> int:
        with self._lock:
            return len(self.history)
