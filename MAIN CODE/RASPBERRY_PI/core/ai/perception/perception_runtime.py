import asyncio
from typing import Any, List, Dict
from .perception_manager import PerceptionManager

class PerceptionRuntime:
    """
    Top-level facade for the Perception Engine.
    Handles data ingestion API.
    """
    def __init__(self, event_bus: Any):
        self.manager = PerceptionManager(event_bus)
        
    async def initialize(self):
        await self.manager.start()
        
    async def ingest_vision(self, detections: List[Dict[str, Any]], depth_map: Any, robot_pose: Dict[str, float]):
        self.manager.health.set_data_status(vision=True)
        # Asynchronously push to scheduler queue
        await self.manager.scheduler.enqueue_data(detections, depth_map, robot_pose)
