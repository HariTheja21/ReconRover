"""
Map Builder Module
Recon Rover V2 - Phase 3.4
"""
import threading
import math
from typing import Tuple

class MapBuilder:
    """Translates relative sensor observations into absolute map coordinates."""
    def __init__(self, grid):
        self._lock = threading.RLock()
        self.grid = grid
        
    def project_obstacle(self, robot_x: float, robot_y: float, robot_theta: float, distance_cm: float) -> Tuple[int, int]:
        """Projects a forward-facing distance reading into the absolute world frame."""
        with self._lock:
            # Simple projection assuming sensor faces exactly forward (theta)
            # For multi-sensor setups, we would add the sensor's angular offset
            abs_x = robot_x + (distance_cm * math.cos(robot_theta))
            abs_y = robot_y + (distance_cm * math.sin(robot_theta))
            
            gx, gy = self.grid.world_to_grid(abs_x, abs_y)
            self.grid.update_cell(gx, gy, occupied=True, confidence=0.2)
            
            # Mark cells between robot and obstacle as free (Raycasting placeholder)
            rx, ry = self.grid.world_to_grid(robot_x, robot_y)
            self.grid.update_cell(rx, ry, occupied=False, confidence=0.2)
            
            return gx, gy
