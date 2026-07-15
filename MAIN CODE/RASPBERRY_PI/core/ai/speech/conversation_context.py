from typing import Dict, Any

class ConversationContext:
    def __init__(self):
        # Stores intent context to handle multi-turn conversations
        self.context_state: Dict[str, Any] = {}
        
    def update(self, key: str, value: Any):
        self.context_state[key] = value
        
    def get(self, key: str) -> Any:
        return self.context_state.get(key)
        
    def clear(self):
        self.context_state.clear()
