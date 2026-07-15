"""
World Model Module
Recon Rover V2 - Phase 3.1
"""
from .entity_manager import EntityManager
from .obstacle_manager import ObstacleManager
from .landmark_manager import LandmarkManager
from .occupancy_manager import OccupancyManager

class WorldModel:
    """Central container for all spatial managers."""
    def __init__(self):
        self.entities = EntityManager()
        self.obstacles = ObstacleManager()
        self.landmarks = LandmarkManager()
        self.occupancy = OccupancyManager()
        
    def sweep_all(self) -> int:
        flushed = 0
        flushed += self.obstacles.sweep()
        flushed += self.landmarks.sweep()
        return flushed
