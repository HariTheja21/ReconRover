class AudioRegistry:
    def __init__(self):
        self.models = {}
        
    def register(self, name: str, provider_cls: type):
        self.models[name] = provider_cls
        
    def get(self, name: str) -> type:
        return self.models.get(name)
