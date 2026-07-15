"""
Base Local Planner Interface
Recon Rover V2 - Phase 3.8
"""
from typing import List, Tuple

class BaseLocalPlanner:
    """Abstract interface for all dynamic avoidance algorithms (DWA, APF, VFH)."""
    def plan_local(self, pose: dict, obstacle: dict, global_path: List[Tuple[float, float]]) -> List[Tuple[float, float]]:
        raise NotImplementedError("Local planners must implement plan_local().")
