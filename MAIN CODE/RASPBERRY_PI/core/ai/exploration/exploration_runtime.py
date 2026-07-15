import asyncio
import numpy as np
from typing import Any
from .exploration_manager import ExplorationManager

class ExplorationRuntime:
    """
    Top-level facade for the Autonomous Exploration Engine.
    """
    def __init__(self, event_bus: Any):
        self.manager = ExplorationManager(event_bus)
        
    async def initialize(self):
        await self.manager.start()
        
    def start_exploration(self):
        self.manager.state.transition("EXPLORING")
        self.manager.bridge.publish_event("ExplorationStateUpdated", {"state": "EXPLORING", "ts": asyncio.get_event_loop().time()})
        
    def stop_exploration(self):
        self.manager.state.transition("IDLE")
        self.manager.bridge.publish_event("ExplorationStateUpdated", {"state": "IDLE", "ts": asyncio.get_event_loop().time()})
        
    async def ingest_occupancy_grid(self, grid: np.ndarray, resolution: float, origin: tuple):
        self.manager.health.map_received = True
        await self.manager.scheduler.enqueue_grid(grid, resolution, origin)
        
    def update_robot_pose(self, x: float, y: float):
        self.manager.health.pose_received = True
        self.manager.engine.update_pose(x, y)
