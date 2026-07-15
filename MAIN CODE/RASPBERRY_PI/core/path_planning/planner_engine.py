"""
Planner Engine Module
Recon Rover V2 - Phase 3.7
"""
import threading
from typing import List, Tuple
from .planner_state import PlannerState
from .path_cache import PathCache
from .path_optimizer import PathOptimizer
from .path_validator import PathValidator
from .astar_planner import AStarPlanner

class PlannerEngine:
    """Core orchestrator for Path Planning operations."""
    def __init__(self):
        self._lock = threading.RLock()
        self.state = PlannerState()
        self.cache = PathCache()
        self.optimizer = PathOptimizer()
        self.validator = PathValidator()
        
        # Modular default planner
        self.active_planner = AStarPlanner()
        
    def set_planner(self, planner_instance):
        """Allows switching out A* for D*, RRT, etc."""
        with self._lock:
            self.active_planner = planner_instance
            
    def compute_path(self, start: Tuple[float, float], goal: Tuple[float, float], map_grid: tuple) -> List[Tuple[float, float]]:
        """Generates, optimizes, and validates the path."""
        with self._lock:
            self.state.set(PlannerState.COMPUTING)
            
            # 1. Check Cache
            cached = self.cache.get(start, goal)
            if cached and self.validator.is_valid(cached, map_grid):
                self.state.set(PlannerState.READY)
                return cached
                
            # 2. Plan
            raw_path = self.active_planner.plan(start, goal, map_grid)
            
            if not raw_path:
                self.state.set(PlannerState.FAILED)
                return []
                
            # 3. Optimize
            optimized_path = self.optimizer.optimize(raw_path)
            
            # 4. Cache
            self.cache.store(start, goal, optimized_path)
            
            self.state.set(PlannerState.READY)
            return optimized_path
