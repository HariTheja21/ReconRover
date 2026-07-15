import asyncio
from typing import Any
from .executive_manager import ExecutiveManager

class ExecutiveRuntime:
    """
    Top-level facade for the Autonomous Mission Executive layer.
    """
    def __init__(self, event_bus: Any):
        self.manager = ExecutiveManager(event_bus)
        
    async def initialize(self):
        await self.manager.start()
        
    async def execute_mission(self, params: dict):
        return await self.manager.api.start_mission(params)
        
    async def abort_mission(self):
        await self.manager.api.abort_mission()
