import asyncio

class AgentMailbox:
    def __init__(self):
        self.queue = asyncio.Queue()
        
    async def receive(self):
        return await self.queue.get()
        
    def send(self, message: dict):
        self.queue.put_nowait(message)
