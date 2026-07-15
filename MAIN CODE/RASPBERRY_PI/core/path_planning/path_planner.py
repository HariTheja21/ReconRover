"""
Base Path Planner Interface
Recon Rover V2 - Phase 3.7
"""
from typing import List, Tuple

class BasePathPlanner:
    """Abstract interface for all path planning algorithms."""
    def plan(self, start: Tuple[float, float], goal: Tuple[float, float], map_grid: tuple) -> List[Tuple[float, float]]:
        raise NotImplementedError("Planners must implement the plan() method.")
