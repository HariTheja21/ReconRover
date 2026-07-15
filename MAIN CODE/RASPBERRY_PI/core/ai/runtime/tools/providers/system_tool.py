from .base_tool import BaseTool

class SystemTool(BaseTool):
    def __init__(self):
        super().__init__("system", "Execute low-level system commands")
        
    def get_schema(self) -> dict:
        return {"type": "object", "properties": {"command": {"type": "string"}}}
        
    async def execute(self, **kwargs) -> dict:
        return {"status": "success", "output": "System command executed"}
