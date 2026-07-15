import asyncio
from typing import Any
from .llm_manager import LLMManager
from .model_provider import ModelProvider

class MockProvider(ModelProvider):
    def __init__(self):
        super().__init__("mock")
    async def generate_response(self, prompt, context):
        return "This is a mock LLM response."

class LLMRuntime:
    """
    Top-level facade for the LLM Intelligence Engine.
    """
    def __init__(self, event_bus: Any):
        self.manager = LLMManager(event_bus)
        
    async def initialize(self):
        # Register default mock provider for testing architecture
        self.manager.registry.register_provider("mock", MockProvider())
        self.manager.registry.set_active("mock")
        await self.manager.start()
        
    async def submit_prompt(self, text: str):
        await self.manager.scheduler.enqueue_prompt(text)
        
    def clear_conversation(self):
        self.manager.cm.clear()
        self.manager.sm.new_session()
