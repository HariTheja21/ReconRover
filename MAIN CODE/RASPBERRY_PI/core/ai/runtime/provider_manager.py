class ProviderManager:
    def __init__(self, registry, loader):
        self.registry = registry
        self.loader = loader
        
    def initialize_providers(self, names: list):
        results = {}
        for name in names:
            results[name] = self.loader.load_provider(name)
        return results
