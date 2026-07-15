from .base_agent import BaseAgent

class MemoryAgent(BaseAgent):
    def __init__(self):
        super().__init__("memory_1", "memory")
        
    async def process_task(self, task: dict) -> dict:
        return {"status": "success", "agent": self.agent_id, "action": "retrieved"}
