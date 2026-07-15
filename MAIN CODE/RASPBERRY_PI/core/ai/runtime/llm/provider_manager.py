class ProviderManager:
    def __init__(self, loader, auth_manager):
        self.loader = loader
        self.auth = auth_manager
        self.active_providers = {}
        self.primary_provider = None
        
    async def activate(self, name: str, is_primary: bool = False):
        if name not in self.active_providers:
            provider = self.loader.load_provider(name)
            if provider:
                api_key = self.auth.get_key(name)
                await provider.authenticate(api_key)
                self.active_providers[name] = provider
                if is_primary:
                    self.primary_provider = name
        return self.active_providers.get(name)
        
    def get_provider(self, name: str = None):
        if name is None:
            name = self.primary_provider
        return self.active_providers.get(name)
