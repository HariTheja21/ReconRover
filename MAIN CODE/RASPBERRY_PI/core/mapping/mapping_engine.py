"""
Mapping Engine Module
Recon Rover V2 - Phase 3.4
"""
import threading
from typing import Tuple
from .occupancy_grid import OccupancyGrid
from .map_builder import MapBuilder
from .map_history import MapHistory
from .map_optimizer import MapOptimizer
from .map_storage import MapStorage

class MappingEngine:
    """Core logic container for 2D mapping."""
    def __init__(self):
        self._lock = threading.RLock()
        self.grid = OccupancyGrid(resolution_cm=10.0)
        self.builder = MapBuilder(self.grid)
        self.history = MapHistory()
        self.optimizer = MapOptimizer(self.grid.grid)
        self.storage = MapStorage()
        
    def process_fused_obstacle(self, robot_x: float, robot_y: float, robot_theta: float, distance_cm: float):
        """Translates an obstacle into map space."""
        with self._lock:
            self.builder.project_obstacle(robot_x, robot_y, robot_theta, distance_cm)
            
    def tick(self) -> Tuple[int, int]:
        """Optimization sweep and snapshotting. Returns (occupied_count, free_count)."""
        with self._lock:
            self.optimizer.optimize()
            occupied, free = self.grid.get_snapshot()
            self.history.save_snapshot(occupied, free)
            return len(occupied), len(free)
