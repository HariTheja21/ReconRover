"""
Navigation Context Module
Recon Rover V2 - Phase 3.6
"""
import threading

class NavigationContext:
    """Context object holding SLAM and World dependencies for navigation decisions."""
    def __init__(self):
        self._lock = threading.RLock()
        self.pose = {"x": 0.0, "y": 0.0, "theta": 0.0}
        self.map_grid = ([], []) # (occupied, free)
        
    def update_pose(self, x: float, y: float, theta: float):
        with self._lock:
            self.pose = {"x": x, "y": y, "theta": theta}
            
    def update_map(self, occupied: list, free: list):
        with self._lock:
            self.map_grid = (occupied, free)
            
    def get_pose(self) -> dict:
        with self._lock:
            return self.pose.copy()
