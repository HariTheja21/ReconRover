class LLMLoader:
    def __init__(self, registry):
        self.registry = registry
        
    def load_provider(self, name: str):
        provider_cls = self.registry.get(name)
        if provider_cls:
            return provider_cls()
        return None
