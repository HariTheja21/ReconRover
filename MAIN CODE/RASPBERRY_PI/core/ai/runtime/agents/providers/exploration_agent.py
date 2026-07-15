from .base_agent import BaseAgent

class ExplorationAgent(BaseAgent):
    def __init__(self):
        super().__init__("explorer_1", "exploration")
        
    async def process_task(self, task: dict) -> dict:
        return {"status": "success", "agent": self.agent_id, "action": "explored"}
