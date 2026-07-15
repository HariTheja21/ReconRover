import asyncio
from .base_provider import BaseProvider

class LMStudioProvider(BaseProvider):
    async def generate(self, prompt: str) -> str:
        await asyncio.sleep(0.1)
        return "Stub response from LM Studio"
        
    async def stream(self, prompt: str):
        yield "Stub response from LM Studio"
