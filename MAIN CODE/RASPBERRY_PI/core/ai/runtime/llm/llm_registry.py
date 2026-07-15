class LLMRegistry:
    def __init__(self):
        self.providers = {}
        
    def register(self, name: str, provider_cls: type):
        self.providers[name] = provider_cls
        
    def get(self, name: str) -> type:
        return self.providers.get(name)
