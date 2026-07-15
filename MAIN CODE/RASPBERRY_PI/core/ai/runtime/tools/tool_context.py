class ToolContext:
    def __init__(self):
        self.current_context = {}
        
    def set_context(self, session_id: str, data: dict):
        self.current_context[session_id] = data
        
    def get_context(self, session_id: str) -> dict:
        return self.current_context.get(session_id, {})
