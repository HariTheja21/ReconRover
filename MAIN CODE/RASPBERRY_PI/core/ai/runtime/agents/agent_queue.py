import asyncio

class AgentQueue:
    def __init__(self):
        self.queue = asyncio.Queue()
        
    async def put(self, task: dict):
        await self.queue.put(task)
        
    async def get(self) -> dict:
        return await self.queue.get()
        
    def task_done(self):
        self.queue.task_done()
