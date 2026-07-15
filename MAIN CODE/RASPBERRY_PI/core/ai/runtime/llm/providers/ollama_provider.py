import asyncio
from .base_provider import BaseProvider

class OllamaProvider(BaseProvider):
    async def generate(self, prompt: str) -> str:
        await asyncio.sleep(0.1)
        return "Stub response from Ollama"
        
    async def stream(self, prompt: str):
        yield "Stub "
        await asyncio.sleep(0.05)
        yield "response "
        await asyncio.sleep(0.05)
        yield "from Ollama"
