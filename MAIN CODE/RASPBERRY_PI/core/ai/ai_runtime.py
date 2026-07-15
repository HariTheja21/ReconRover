import asyncio
from typing import Any
from .ai_manager import AIManager

class AIRuntime:
    """
    Top-level facade for the AI subsystem. 
    Initializes the AIManager and exposes core APIs for other Rover modules.
    """
    def __init__(self, event_bus: Any):
        self.manager = AIManager(event_bus)
        
    async def initialize(self):
        await self.manager.start()
        
    def register_model(self, model_id: str, metadata: dict) -> bool:
        return self.manager.model_registry.register_model(model_id, metadata)
        
    def load_model(self, model_id: str) -> bool:
        return self.manager.model_manager.load_model(model_id)
        
    def register_tool(self, name: str, description: str, parameters: dict, callback):
        self.manager.tool_registry.register_tool(name, description, parameters, callback)
        
    async def execute_task(self, system_prompt: str, user_request: str) -> str:
        return await self.manager.reasoning.process_task(system_prompt, user_request)
        
    def update_context(self, domain: str, key: str, value: Any):
        if domain == "system":
            self.manager.context.update_system_context(key, value)
        elif domain == "mission":
            self.manager.context.update_mission_context(key, value)
        elif domain == "vision":
            self.manager.context.update_vision_context(key, value)
