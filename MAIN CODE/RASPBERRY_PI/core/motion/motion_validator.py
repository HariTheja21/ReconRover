"""
Motion Validator Module
Recon Rover V2 - Phase 4.0
"""
import threading

class MotionValidator:
    """Validates if a motion command is structurally sound before processing."""
    def __init__(self):
        self._lock = threading.RLock()
        
    def is_valid(self, lin: float, ang: float) -> bool:
        with self._lock:
            if not isinstance(lin, (int, float)) or not isinstance(ang, (int, float)):
                return False
            # Can catch NaN or Inf here if needed
            return True
