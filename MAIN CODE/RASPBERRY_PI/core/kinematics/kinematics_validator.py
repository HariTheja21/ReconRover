"""
Kinematics Validator Module
Recon Rover V2 - Phase 4.1
"""
import threading

class KinematicsValidator:
    """Validates structural integrity of MotionRequest data."""
    def __init__(self):
        self._lock = threading.RLock()
        
    def is_valid(self, lin: float, ang: float) -> bool:
        with self._lock:
            if not isinstance(lin, (int, float)) or not isinstance(ang, (int, float)):
                return False
            if abs(lin) > 1.0 or abs(ang) > 1.0: # Expect normalized inputs
                return False
            return True
