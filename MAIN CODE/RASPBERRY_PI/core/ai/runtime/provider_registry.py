class ProviderRegistry:
    def __init__(self):
        self.providers = {}
        
    def register(self, name: str, config: dict):
        self.providers[name] = config
        
    def get(self, name: str) -> dict:
        return self.providers.get(name)
