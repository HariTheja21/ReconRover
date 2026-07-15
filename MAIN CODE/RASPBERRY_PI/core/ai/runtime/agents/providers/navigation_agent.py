from .base_agent import BaseAgent

class NavigationAgent(BaseAgent):
    def __init__(self):
        super().__init__("nav_1", "navigation")
        
    async def process_task(self, task: dict) -> dict:
        return {"status": "success", "agent": self.agent_id, "action": "routed"}
