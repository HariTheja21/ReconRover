"""
Safety Bubble Module
Recon Rover V2 - Phase 3.8
"""
import threading
import math
from typing import Tuple

class SafetyBubble:
    """Manages the configurable safety perimeter around the rover."""
    def __init__(self):
        self._lock = threading.RLock()
        self.radius_cm = 20.0 # Strict collision perimeter
        self.warning_radius_cm = 40.0 # Avoidance triggers here
        
    def is_violated(self, obstacle_x: float, obstacle_y: float, pose_x: float, pose_y: float) -> Tuple[bool, bool]:
        """Returns (is_warning, is_critical)"""
        with self._lock:
            dist = math.hypot(obstacle_x - pose_x, obstacle_y - pose_y)
            return (dist <= self.warning_radius_cm), (dist <= self.radius_cm)
