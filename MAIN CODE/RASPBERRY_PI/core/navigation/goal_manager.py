"""
Goal Manager Module
Recon Rover V2 - Phase 3.6
"""
import threading
from typing import Tuple

class GoalManager:
    """Manages the ultimate destination requested by the mission system."""
    def __init__(self):
        self._lock = threading.RLock()
        self.active_goal_id = None
        self.target_x = 0.0
        self.target_y = 0.0
        self.reached = False
        
    def set_goal(self, goal_id: str, x: float, y: float):
        with self._lock:
            self.active_goal_id = goal_id
            self.target_x = x
            self.target_y = y
            self.reached = False
            
    def get_goal(self) -> Tuple[float, float]:
        with self._lock:
            if self.active_goal_id and not self.reached:
                return (self.target_x, self.target_y)
            return None
            
    def mark_reached(self):
        with self._lock:
            self.reached = True
