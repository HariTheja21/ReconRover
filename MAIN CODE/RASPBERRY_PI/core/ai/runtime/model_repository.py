class ModelRepository:
    def __init__(self, installer, updater, version_mgr, cache):
        self.installer = installer
        self.updater = updater
        self.version_mgr = version_mgr
        self.cache = cache
        
    async def get_model(self, name: str, version: str = "latest") -> bool:
        v = self.version_mgr.resolve_version(name, version)
        return await self.installer.install(name, v)
