class AuthenticationManager:
    def __init__(self):
        self.keys = {}
        
    def set_key(self, provider: str, key: str):
        self.keys[provider] = key
        
    def get_key(self, provider: str) -> str:
        return self.keys.get(provider)
