import asyncio

class AgentMailbox:
    def __init__(self):
        self.queues = {}
        
    def create_mailbox(self, agent_id: str):
        self.queues[agent_id] = asyncio.Queue()
        
    async def send(self, recipient_id: str, message: dict):
        if recipient_id in self.queues:
            await self.queues[recipient_id].put(message)
            
    async def receive(self, agent_id: str) -> dict:
        if agent_id in self.queues:
            return await self.queues[agent_id].get()
        return None
