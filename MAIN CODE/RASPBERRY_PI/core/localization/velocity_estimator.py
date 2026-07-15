"""
Velocity Estimator Module
Recon Rover V2 - Phase 3.3
"""
import threading
import time

class VelocityEstimator:
    """Estimates velocity using time-deltas between fused distances or odometry."""
    def __init__(self):
        self._lock = threading.RLock()
        self.linear_vel = 0.0
        self.angular_vel = 0.0
        
        self.last_dist = None
        self.last_dist_time = None
        
    def update_distance(self, distance_cm: float):
        """Simplistic heuristic: if distance to obstacle changes, we are moving (if obstacle is static).
        Note: True velocity requires wheel encoders (Odometry). This is a placeholder."""
        now = time.time()
        with self._lock:
            if self.last_dist is not None and self.last_dist_time is not None:
                dt = now - self.last_dist_time
                if dt > 0:
                    # Invert the delta since getting closer means positive forward velocity
                    d_dist = self.last_dist - distance_cm 
                    self.linear_vel = d_dist / dt
            
            self.last_dist = distance_cm
            self.last_dist_time = now
            
    def get_velocity(self) -> tuple:
        with self._lock:
            return self.linear_vel, self.angular_vel
