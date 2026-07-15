import asyncio
from typing import Any
from .semantic_manager import SemanticManager

class SemanticRuntime:
    """
    Top-level facade for the Semantic Mapping Engine.
    """
    def __init__(self, event_bus: Any, db_path: str = ":memory:"):
        self.manager = SemanticManager(event_bus, db_path)
        
    async def initialize(self):
        await self.manager.start()
        
    def shutdown(self):
        self.manager.stop()
        
    async def ingest_scene_update(self, scene_data: dict):
        await self.manager.scheduler.enqueue_scene(scene_data)
        
    async def request_landmark_creation(self, name: str, x: float, y: float, z: float):
        await self.manager.scheduler.enqueue_landmark(name, x, y, z)
        
    def execute_query(self, cls_name: str) -> list:
        return self.manager.query.find_objects(cls_name)
