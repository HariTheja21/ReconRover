import asyncio
from typing import Any
from .agent_manager import AgentManager

class AgentRuntime:
    """
    Top-level facade for the Multi-Agent Intelligence Framework.
    """
    def __init__(self, event_bus: Any):
        self.manager = AgentManager(event_bus)
        
    async def initialize(self):
        await self.manager.start()
        
    async def dispatch_task(self, agent_id: str, task: dict):
        await self.manager.engine.dispatch_task(agent_id, task)
        
    async def update_shared_context(self, key: str, value: Any):
        await self.manager.engine.update_context(key, value)
