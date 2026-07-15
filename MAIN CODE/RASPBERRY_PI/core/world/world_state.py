"""
World State Module
Recon Rover V2 - Phase 3.1
"""
import threading
import time

class WorldState:
    """Maintains the robot's own internal pose and telemetry state."""
    def __init__(self):
        self._lock = threading.RLock()
        self.battery_pct = 0.0
        self.pitch = 0.0
        self.roll = 0.0
        self.yaw = 0.0
        self.last_updated = time.time()
        
    def update_battery(self, pct: float):
        with self._lock:
            self.battery_pct = pct
            self.last_updated = time.time()
            
    def update_imu(self, pitch: float, roll: float, yaw: float):
        with self._lock:
            self.pitch = pitch
            self.roll = roll
            self.yaw = yaw
            self.last_updated = time.time()
            
    def get_snapshot(self):
        with self._lock:
            return {
                "battery": self.battery_pct,
                "pitch": self.pitch,
                "roll": self.roll,
                "yaw": self.yaw,
                "timestamp": self.last_updated
            }
