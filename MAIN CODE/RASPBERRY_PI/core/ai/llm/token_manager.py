class TokenManager:
    def __init__(self, max_tokens: int = 4096):
        self.max_tokens = max_tokens
        
    def truncate_history(self, history: list) -> list:
        # Stub token truncation
        return history[-10:] # Keep last 10 messages
