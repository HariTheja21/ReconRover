import asyncio

class AgentScheduler:
    def __init__(self, queue, dispatcher):
        self.queue = queue
        self.dispatcher = dispatcher
        
    async def schedule_task(self, agent_id: str, task: dict):
        await self.queue.put({"agent_id": agent_id, "task": task})
        
    async def run_loop(self):
        while True:
            item = await self.queue.get()
            asyncio.create_task(self.dispatcher.dispatch(item["agent_id"], item["task"]))
            self.queue.task_done()
