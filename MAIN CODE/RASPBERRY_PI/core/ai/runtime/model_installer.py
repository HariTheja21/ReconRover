class ModelInstaller:
    def __init__(self, downloader, cache):
        self.downloader = downloader
        self.cache = cache
        
    async def install(self, model_name: str, version: str) -> bool:
        if self.cache.is_cached(model_name):
            return True
        success = await self.downloader.download(model_name, version)
        if success:
            self.cache.add_to_cache(model_name)
        return success
