import asyncio
from .base_provider import BaseProvider

class vLLMProvider(BaseProvider):
    async def generate(self, prompt: str) -> str:
        await asyncio.sleep(0.1)
        return "Stub response from vLLM"
        
    async def stream(self, prompt: str):
        yield "Stub response from vLLM"
