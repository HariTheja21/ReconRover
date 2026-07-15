import asyncio
from .base_provider import BaseProvider

class ClaudeProvider(BaseProvider):
    async def generate(self, prompt: str) -> str:
        await asyncio.sleep(0.1)
        return "Stub response from Claude"
        
    async def stream(self, prompt: str):
        yield "Stub response from Claude"
