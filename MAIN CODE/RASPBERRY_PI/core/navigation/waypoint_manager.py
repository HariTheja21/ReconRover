"""
Waypoint Manager Module
Recon Rover V2 - Phase 3.6
"""
import threading
from typing import List, Tuple

class WaypointManager:
    """Manages the sub-goals (waypoints) required to reach a final goal."""
    def __init__(self):
        self._lock = threading.RLock()
        self.waypoints: List[Tuple[float, float]] = []
        self.current_index = 0
        
    def set_waypoints(self, points: List[Tuple[float, float]]):
        with self._lock:
            self.waypoints = points
            self.current_index = 0
            
    def get_current_waypoint(self) -> Tuple[float, float]:
        with self._lock:
            if self.current_index < len(self.waypoints):
                return self.waypoints[self.current_index]
            return None
            
    def advance(self) -> bool:
        """Returns True if there is a next waypoint, False if we reached the end."""
        with self._lock:
            self.current_index += 1
            return self.current_index < len(self.waypoints)
