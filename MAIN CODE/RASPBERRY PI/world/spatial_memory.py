"""
spatial_memory.py
Recon Rover V1 - Cognitive Layer

Maintains obstacle locations and free-space estimations.
"""

from typing import Tuple
from .object_models import CellState, SpatialCell
from .world_state import WorldState

class SpatialMemory:
    """
    Evaluates raw distances into discrete cell states.
    """
    def __init__(self, obstacle_threshold_cm: float = 30.0, free_threshold_cm: float = 50.0):
        self.obstacle_threshold = obstacle_threshold_cm
        self.free_threshold = free_threshold_cm
        
    def update(self, state: WorldState, front_dist: float, left_dist: float, right_dist: float, rear_dist: float, confidence: float, timestamp_ms: int) -> list[str]:
        """
        Updates spatial grid in WorldState. 
        Returns a list of directions where an obstacle newly appeared.
        """
        new_obstacles = []
        
        # Helper to process a single cell
        def process_direction(direction: str, distance: float):
            cell = state.spatial_grid[direction]
            old_state = cell.state
            
            # If distance is invalid (-1), decay confidence or mark unknown
            if distance < 0:
                cell.state = CellState.UNKNOWN
                cell.distance_cm = -1.0
                cell.confidence = 0.0
            else:
                cell.distance_cm = distance
                cell.confidence = confidence
                cell.last_updated_ms = timestamp_ms
                
                if distance < self.obstacle_threshold:
                    cell.state = CellState.OBSTACLED
                    if old_state != CellState.OBSTACLED:
                        new_obstacles.append(direction)
                elif distance > self.free_threshold:
                    cell.state = CellState.FREE
                else:
                    # Hysteresis zone; maintain previous state if it was FREE or OBSTACLED
                    if old_state == CellState.UNKNOWN:
                        cell.state = CellState.FREE # Optimistic assumption in hysteresis if unknown
        
        process_direction("front", front_dist)
        process_direction("left", left_dist)
        process_direction("right", right_dist)
        process_direction("rear", rear_dist)
        
        self._update_safe_direction(state)
        
        return new_obstacles
        
    def _update_safe_direction(self, state: WorldState):
        """
        Calculates the last known safe direction based on spatial memory.
        Prioritizes front, then sides, then rear.
        """
        grid = state.spatial_grid
        if grid["front"].state == CellState.FREE:
            state.last_known_safe_direction = "front"
        elif grid["left"].state == CellState.FREE and grid["right"].state != CellState.FREE:
            state.last_known_safe_direction = "left"
        elif grid["right"].state == CellState.FREE and grid["left"].state != CellState.FREE:
            state.last_known_safe_direction = "right"
        elif grid["rear"].state == CellState.FREE:
            state.last_known_safe_direction = "rear"
        else:
            # If nothing is explicitly free, look for unknown or just keep the last one if trapped.
            pass 
