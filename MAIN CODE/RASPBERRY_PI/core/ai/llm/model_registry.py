class ModelRegistry:
    def __init__(self):
        self.providers = {}
        self.active_provider = None
        
    def register_provider(self, name: str, provider):
        self.providers[name] = provider
        
    def set_active(self, name: str):
        if name in self.providers:
            self.active_provider = self.providers[name]
            
    def get_active(self):
        return self.active_provider
