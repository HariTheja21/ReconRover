class ProviderLoader:
    def __init__(self, registry, dep_mgr):
        self.registry = registry
        self.dep_mgr = dep_mgr
        
    def load_provider(self, name: str) -> bool:
        provider = self.registry.get(name)
        if not provider:
            return False
        if not self.dep_mgr.verify_dependencies(provider.get("deps", [])):
            return False
        return True
