"""
Odometry Module
Recon Rover V2 - Phase 3.3
"""
import threading
import math
import time

class Odometry:
    """Integrates velocity over time to calculate relative 2D position (Dead Reckoning)."""
    def __init__(self):
        self._lock = threading.RLock()
        self.x = 0.0
        self.y = 0.0
        self.last_update = time.time()
        
    def integrate_velocity(self, linear_vel: float, theta: float):
        """Standard differential drive kinematic update."""
        now = time.time()
        with self._lock:
            dt = now - self.last_update
            # Assuming linear_vel is along the heading vector
            dx = linear_vel * math.cos(theta) * dt
            dy = linear_vel * math.sin(theta) * dt
            
            self.x += dx
            self.y += dy
            self.last_update = now
            
    def get_position(self) -> tuple:
        with self._lock:
            return self.x, self.y
