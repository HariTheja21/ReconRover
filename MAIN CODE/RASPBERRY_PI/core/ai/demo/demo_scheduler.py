import asyncio

class DemoScheduler:
    def __init__(self, manager):
        self.manager = manager
        
    async def run_demo_async(self):
        # Fire and forget execution
        asyncio.create_task(self.manager.run_full_demo())
