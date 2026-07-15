"""
Orientation Tracker Module
Recon Rover V2 - Phase 3.3
"""
import threading
import time
import math

class OrientationTracker:
    """Tracks fused orientation and translates it to an absolute heading (theta)."""
    def __init__(self):
        self._lock = threading.RLock()
        self.pitch = 0.0
        self.roll = 0.0
        self.yaw = 0.0
        self.theta = 0.0 # Standard 2D math heading in radians
        self.last_update = time.time()
        
    def update_from_imu(self, pitch: float, roll: float, yaw: float):
        with self._lock:
            self.pitch = pitch
            self.roll = roll
            self.yaw = yaw
            # Convert yaw degrees to radians for standard geometry
            self.theta = math.radians(yaw)
            self.last_update = time.time()
            
    def get_theta(self) -> float:
        with self._lock:
            return self.theta
