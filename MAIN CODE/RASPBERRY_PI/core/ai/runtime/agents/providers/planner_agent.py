from .base_agent import BaseAgent

class PlannerAgent(BaseAgent):
    def __init__(self):
        super().__init__("planner_1", "planner")
        
    async def process_task(self, task: dict) -> dict:
        return {"status": "success", "agent": self.agent_id, "action": "planned"}
