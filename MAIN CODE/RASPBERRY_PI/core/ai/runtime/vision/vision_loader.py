class VisionLoader:
    def __init__(self, registry):
        self.registry = registry
        self.active_models = {}
        
    def load_model(self, name: str, path: str, device: str) -> bool:
        provider_cls = self.registry.get(name)
        if not provider_cls:
            return False
        
        provider = provider_cls()
        success = provider.load(path, device)
        if success:
            self.active_models[name] = provider
        return success
        
    def unload_model(self, name: str):
        if name in self.active_models:
            self.active_models[name].unload()
            del self.active_models[name]
            
    def get_provider(self, name: str):
        return self.active_models.get(name)
