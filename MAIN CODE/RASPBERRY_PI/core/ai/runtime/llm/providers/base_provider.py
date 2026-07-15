class BaseProvider:
    def __init__(self):
        self.is_authenticated = False
        
    async def authenticate(self, api_key: str = None) -> bool:
        self.is_authenticated = True
        return True
        
    async def generate(self, prompt: str) -> str:
        raise NotImplementedError
        
    async def stream(self, prompt: str):
        raise NotImplementedError
