"""
obstacle_avoidance.py
Recon Rover V1 - Cognitive Layer

Evaluates safe directions based on the WorldModel spatial cells.
"""

from typing import Dict, Any
from .navigation_state import NavState

class ObstacleAvoidance:
    """
    Parses the WorldState spatial grid to determine blocked directions.
    """
    
    def __init__(self):
        pass

    def evaluate_directions(self, world_state: Any) -> Dict[str, bool]:
        """
        Returns a dictionary indicating if a direction is FREE (True) or OBSTACLED (False).
        Requires knowledge of CellState enum (value 1 is FREE).
        """
        free_directions = {
            "front": False,
            "left": False,
            "right": False,
            "rear": False
        }
        
        # We parse the world_state dynamically to avoid circular imports of CellState 
        # from world/object_models.py. We rely on the semantic string representations 
        # or enum name if accessible.
        
        grid = world_state.spatial_grid
        
        for direction in free_directions.keys():
            if direction in grid:
                cell = grid[direction]
                # Assuming cell.state.name gives the enum string name
                # This decouples the modules slightly.
                if hasattr(cell.state, 'name') and cell.state.name == "FREE":
                    free_directions[direction] = True
                    
        return free_directions
