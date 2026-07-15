"""
Navigation Statistics Module
Recon Rover V2 - Phase 3.6
"""
import threading

class NavigationStatistics:
    def __init__(self):
        self._lock = threading.RLock()
        self.goals_completed = 0
        self.waypoints_reached = 0
        
    def increment_goal(self):
        with self._lock:
            self.goals_completed += 1
            
    def increment_waypoint(self):
        with self._lock:
            self.waypoints_reached += 1
