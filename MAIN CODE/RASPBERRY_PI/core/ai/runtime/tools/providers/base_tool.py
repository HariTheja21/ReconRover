class BaseTool:
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        
    def get_schema(self) -> dict:
        raise NotImplementedError
        
    async def execute(self, **kwargs) -> dict:
        raise NotImplementedError
