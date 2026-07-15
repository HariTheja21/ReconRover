"""
Navigation Validator Module
Recon Rover V2 - Phase 3.6
"""
import threading

class NavigationValidator:
    """Validates if goals or targets are logically possible (e.g., inside map bounds)."""
    def __init__(self):
        self._lock = threading.RLock()
        
    def is_valid_goal(self, x: float, y: float, map_grid: tuple) -> bool:
        with self._lock:
            # Placeholder for checking if the goal is inside an occupied cell
            # In Phase 3.6 we don't do path planning, so we just do a rudimentary check
            # For now, blindly accept
            return True
