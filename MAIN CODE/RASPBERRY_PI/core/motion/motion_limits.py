"""
Motion Limits Module
Recon Rover V2 - Phase 4.0
"""
import threading

class MotionLimits:
    """Enforces absolute safety bounds on requested velocities and accelerations."""
    def __init__(self):
        self._lock = threading.RLock()
        # Normalized absolute caps
        self.max_linear_vel = 1.0
        self.max_angular_vel = 1.0
        # Maximum step change per evaluation tick (simulated acceleration)
        self.max_linear_accel = 0.2
        self.max_angular_accel = 0.3
        
    def apply_limits(self, target_lin: float, target_ang: float, current_lin: float, current_ang: float) -> tuple:
        with self._lock:
            # 1. Cap absolute targets
            t_lin = max(-self.max_linear_vel, min(self.max_linear_vel, target_lin))
            t_ang = max(-self.max_angular_vel, min(self.max_angular_vel, target_ang))
            
            # 2. Apply acceleration step limits
            d_lin = t_lin - current_lin
            d_ang = t_ang - current_ang
            
            if abs(d_lin) > self.max_linear_accel:
                d_lin = self.max_linear_accel if d_lin > 0 else -self.max_linear_accel
                
            if abs(d_ang) > self.max_angular_accel:
                d_ang = self.max_angular_accel if d_ang > 0 else -self.max_angular_accel
                
            # If limited, we flag it for stats
            limited = (t_lin != target_lin) or (t_ang != target_ang) or (abs(t_lin - current_lin) > self.max_linear_accel) or (abs(t_ang - current_ang) > self.max_angular_accel)
            
            return current_lin + d_lin, current_ang + d_ang, limited
