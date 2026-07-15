"""
Pose Corrector Module
Recon Rover V2 - Phase 3.5
"""
import threading

class PoseCorrector:
    """Applies mathematically derived offsets to correct dead-reckoning drift."""
    def __init__(self):
        self._lock = threading.RLock()
        # Cumulative error corrections
        self.offset_x = 0.0
        self.offset_y = 0.0
        self.offset_theta = 0.0
        
    def apply_correction(self, raw_x: float, raw_y: float, raw_theta: float) -> tuple:
        with self._lock:
            return (
                raw_x + self.offset_x,
                raw_y + self.offset_y,
                raw_theta + self.offset_theta
            )
            
    def update_offset(self, dx: float, dy: float, dtheta: float):
        with self._lock:
            self.offset_x += dx
            self.offset_y += dy
            self.offset_theta += dtheta
