class ModelUpdater:
    def __init__(self, downloader):
        self.downloader = downloader
        
    async def update(self, model_name: str) -> bool:
        return await self.downloader.download(model_name, "latest")
