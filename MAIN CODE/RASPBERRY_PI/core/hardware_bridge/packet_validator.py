"""
Packet Validator Module
Recon Rover V2 - Phase 4.2
"""
import threading

class PacketValidator:
    """Validates if inputs meet protocol schema bounds before encoding."""
    def __init__(self):
        self._lock = threading.RLock()
        
    def is_valid(self, left: float, right: float) -> bool:
        with self._lock:
            if not isinstance(left, (int, float)) or not isinstance(right, (int, float)):
                return False
            # We expect normalized inputs [-1.0, 1.0] from kinematics
            if abs(left) > 1.001 or abs(right) > 1.001:
                return False
            return True
