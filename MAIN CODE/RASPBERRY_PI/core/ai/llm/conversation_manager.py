class ConversationManager:
    def __init__(self):
        self.history = []
        
    def add_user_message(self, text: str):
        self.history.append({"role": "user", "content": text})
        
    def add_assistant_message(self, text: str):
        self.history.append({"role": "assistant", "content": text})
        
    def get_history(self) -> list:
        return self.history
        
    def clear(self):
        self.history.clear()
