from .base_agent import BaseAgent

class VisionAgent(BaseAgent):
    def __init__(self):
        super().__init__("vision_1", "vision")
        
    async def process_task(self, task: dict) -> dict:
        return {"status": "success", "agent": self.agent_id, "action": "analyzed_image"}
