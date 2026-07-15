import asyncio

class ToolScheduler:
    def __init__(self, dispatcher):
        self.dispatcher = dispatcher
        self.queue = asyncio.Queue()
        
    async def schedule_execution(self, tool_name: str, args: dict):
        await self.queue.put((tool_name, args))
        
    async def run_loop(self):
        while True:
            tool_name, args = await self.queue.get()
            asyncio.create_task(self.dispatcher.dispatch(tool_name, args))
            self.queue.task_done()
