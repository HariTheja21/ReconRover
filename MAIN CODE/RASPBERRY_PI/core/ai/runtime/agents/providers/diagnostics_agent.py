from .base_agent import BaseAgent

class DiagnosticsAgent(BaseAgent):
    def __init__(self):
        super().__init__("diag_1", "diagnostics")
        
    async def process_task(self, task: dict) -> dict:
        return {"status": "success", "agent": self.agent_id, "action": "diagnosed"}
