import asyncio
from .base_provider import BaseProvider

class OpenAIProvider(BaseProvider):
    async def generate(self, prompt: str) -> str:
        await asyncio.sleep(0.1)
        return "Stub response from OpenAI"
        
    async def stream(self, prompt: str):
        yield "Stub "
        yield "response "
        yield "from OpenAI"
