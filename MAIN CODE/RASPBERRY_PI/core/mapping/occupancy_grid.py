"""
Occupancy Grid Module
Recon Rover V2 - Phase 3.4
"""
import threading
from typing import List, Tuple

class OccupancyGrid:
    """Core mathematical representation of the 2D environment."""
    def __init__(self, resolution_cm: float = 10.0):
        self._lock = threading.RLock()
        self.resolution = resolution_cm
        # Using dicts for sparse grid memory efficiency: (gx, gy) -> probability (0.0 to 1.0)
        self.grid = {} 
        self.threshold_occupied = 0.65
        self.threshold_free = 0.35
        
    def world_to_grid(self, x: float, y: float) -> Tuple[int, int]:
        return int(x // self.resolution), int(y // self.resolution)
        
    def update_cell(self, gx: int, gy: int, occupied: bool, confidence: float = 0.1):
        with self._lock:
            current_prob = self.grid.get((gx, gy), 0.5)
            # Simple Bayesian log-odds update placeholder
            # If occupied, increase probability. If free, decrease it.
            if occupied:
                current_prob = min(1.0, current_prob + confidence)
            else:
                current_prob = max(0.0, current_prob - confidence)
                
            self.grid[(gx, gy)] = current_prob
            return (gx, gy)
            
    def get_snapshot(self) -> Tuple[List[tuple], List[tuple]]:
        """Returns lists of occupied and free cell coordinates."""
        with self._lock:
            occupied = []
            free = []
            for coords, prob in self.grid.items():
                if prob >= self.threshold_occupied:
                    occupied.append(coords)
                elif prob <= self.threshold_free:
                    free.append(coords)
            return occupied, free
