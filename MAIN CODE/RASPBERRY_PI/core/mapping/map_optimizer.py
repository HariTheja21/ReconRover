"""
Map Optimizer Module
Recon Rover V2 - Phase 3.4
"""
import threading

class MapOptimizer:
    """Periodically prunes low-confidence cells or merges regions."""
    def __init__(self, grid_ref):
        self._lock = threading.RLock()
        self.grid_ref = grid_ref # Reference to OccupancyGrid.grid
        
    def optimize(self) -> int:
        """Removes cells that are sitting exactly at 0.5 (unknown) to save RAM."""
        with self._lock:
            to_remove = [k for k, v in self.grid_ref.items() if 0.49 < v < 0.51]
            for k in to_remove:
                del self.grid_ref[k]
            return len(to_remove)
