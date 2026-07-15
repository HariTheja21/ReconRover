"""
World Database Module
Recon Rover V2 - Phase 3.1
"""
from .world_state import WorldState
from .entity_manager import EntityManager
from .obstacle_manager import ObstacleManager
from .landmark_manager import LandmarkManager
from .occupancy_manager import OccupancyManager
from .confidence_manager import ConfidenceManager

class WorldDatabase:
    """Central container for all semantic spatial data."""
    def __init__(self):
        self.state = WorldState()
        self.entities = EntityManager()
        self.obstacles = ObstacleManager()
        self.landmarks = LandmarkManager()
        self.occupancy = OccupancyManager()
        self.confidence = ConfidenceManager()
        
    def sweep_all(self):
        self.obstacles.sweep()
