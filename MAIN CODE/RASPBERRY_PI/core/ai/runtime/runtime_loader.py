class RuntimeLoader:
    def __init__(self, provider_mgr, model_repo):
        self.provider_mgr = provider_mgr
        self.model_repo = model_repo
        
    async def load_runtime(self, providers: list):
        return self.provider_mgr.initialize_providers(providers)
