from .base_agent import BaseAgent

class VisionAgent(BaseAgent):
    def __init__(self):
        super().__init__("vision_agent")
        
    async def handle_message(self, msg: dict):
        self.state = "PROCESSING"
        # Logic here
        self.state = "IDLE"

class SpeechAgent(BaseAgent):
    def __init__(self):
        super().__init__("speech_agent")
        
    async def handle_message(self, msg: dict):
        pass

class NavigationAgent(BaseAgent):
    def __init__(self):
        super().__init__("navigation_agent")
        
    async def handle_message(self, msg: dict):
        pass

class ExplorationAgent(BaseAgent):
    def __init__(self):
        super().__init__("exploration_agent")
        
    async def handle_message(self, msg: dict):
        pass

class MemoryAgent(BaseAgent):
    def __init__(self):
        super().__init__("memory_agent")
        
    async def handle_message(self, msg: dict):
        pass

class PlannerAgent(BaseAgent):
    def __init__(self):
        super().__init__("planner_agent")
        
    async def handle_message(self, msg: dict):
        pass

class DiagnosticsAgent(BaseAgent):
    def __init__(self):
        super().__init__("diagnostics_agent")
        
    async def handle_message(self, msg: dict):
        pass
