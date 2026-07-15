"""
Collision Checker Module
Recon Rover V2 - Phase 3.8
"""
import threading
from typing import List, Tuple
from .safety_bubble import SafetyBubble
import math

class CollisionChecker:
    """Predicts collisions along the intended trajectory."""
    def __init__(self, bubble: SafetyBubble):
        self._lock = threading.RLock()
        self.bubble = bubble
        
    def check_trajectory(self, trajectory: List[Tuple[float, float]], pose: dict, obstacle: dict) -> Tuple[bool, bool]:
        """
        Projects forward to see if trajectory intersects obstacle.
        Returns (needs_avoidance, needs_estop)
        """
        with self._lock:
            if not obstacle:
                return False, False
                
            px, py, ptheta = pose.get('x', 0), pose.get('y', 0), pose.get('theta', 0)
            
            # Phase 3.8 stub for dynamic obstacle check.
            # In a full implementation, we project the dynamic obstacle's velocity vector.
            # Here we just check static proximity to current pose as a simplified test.
            
            # Calculate obstacle global coordinates based on distance and orientation
            # (Assuming obstacle dictionary contains raw distance forward of robot)
            dist = obstacle.get('distance_cm', 999.0)
            
            ox = px + dist * math.cos(ptheta)
            oy = py + dist * math.sin(ptheta)
            
            warn, crit = self.bubble.is_violated(ox, oy, px, py)
            
            return warn, crit
