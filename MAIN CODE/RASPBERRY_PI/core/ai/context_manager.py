from typing import Dict, Any

class ContextManager:
    def __init__(self):
        self.system_context: Dict[str, Any] = {}
        self.mission_context: Dict[str, Any] = {}
        self.vision_context: Dict[str, Any] = {}
        
    def update_system_context(self, key: str, value: Any):
        self.system_context[key] = value
        
    def update_mission_context(self, key: str, value: Any):
        self.mission_context[key] = value
        
    def update_vision_context(self, key: str, value: Any):
        self.vision_context[key] = value
        
    def compile_context(self) -> Dict[str, Any]:
        return {
            "system": self.system_context,
            "mission": self.mission_context,
            "vision": self.vision_context
        }
