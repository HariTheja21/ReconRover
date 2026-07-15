class ModelProvider:
    def __init__(self, name: str):
        self.name = name
        
    async def generate_response(self, prompt: str, context: list) -> str:
        raise NotImplementedError
        
    async def generate_stream(self, prompt: str, context: list):
        raise NotImplementedError
