from .base_agent import BaseAgent

class SpeechAgent(BaseAgent):
    def __init__(self):
        super().__init__("speech_1", "speech")
        
    async def process_task(self, task: dict) -> dict:
        return {"status": "success", "agent": self.agent_id, "action": "synthesized"}
