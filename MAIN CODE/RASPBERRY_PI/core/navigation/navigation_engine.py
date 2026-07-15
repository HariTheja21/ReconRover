"""
Navigation Engine Module
Recon Rover V2 - Phase 3.6
"""
import threading
import math
from typing import Tuple
from .navigation_state import NavigationState
from .goal_manager import GoalManager
from .waypoint_manager import WaypointManager
from .navigation_validator import NavigationValidator
from .navigation_context import NavigationContext

class NavigationEngine:
    """Core logic container for managing navigation targets."""
    def __init__(self):
        self._lock = threading.RLock()
        self.state = NavigationState()
        self.goal = GoalManager()
        self.waypoints = WaypointManager()
        self.validator = NavigationValidator()
        self.context = NavigationContext()
        
        self.reached_threshold = 10.0 # cm radius to consider a point reached
        
    def tick(self) -> Tuple[str, tuple, bool, bool]:
        """
        Executes a single navigation tick.
        Returns (current_state, current_target, waypoint_reached, goal_reached)
        """
        with self._lock:
            current = self.state.get_state()
            target = self.goal.get_goal()
            
            wp_reached = False
            gl_reached = False
            
            if current == NavigationState.IDLE:
                if target is not None:
                    # For Phase 3.6, naive straight line navigation -> waypoint == goal
                    self.waypoints.set_waypoints([target])
                    self.state.set_state(NavigationState.NAVIGATING)
                    current = NavigationState.NAVIGATING
                    
            if current == NavigationState.NAVIGATING:
                pose = self.context.get_pose()
                current_wp = self.waypoints.get_current_waypoint()
                
                if current_wp:
                    dx = current_wp[0] - pose["x"]
                    dy = current_wp[1] - pose["y"]
                    dist = math.hypot(dx, dy)
                    
                    if dist <= self.reached_threshold:
                        wp_reached = True
                        if not self.waypoints.advance():
                            # No more waypoints, goal reached
                            self.goal.mark_reached()
                            self.state.set_state(NavigationState.REACHED)
                            gl_reached = True
                            current = NavigationState.REACHED
                            
            # If target was cleared externally, reset to IDLE
            if target is None and current != NavigationState.IDLE:
                self.state.set_state(NavigationState.IDLE)
                current = NavigationState.IDLE
                
            active_target = self.waypoints.get_current_waypoint() if current == NavigationState.NAVIGATING else None
            return current, active_target, wp_reached, gl_reached
