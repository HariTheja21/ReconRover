from .base_tool import BaseTool

class DiagnosticsTool(BaseTool):
    def __init__(self):
        super().__init__("diagnostics", "Check rover health and battery")
        
    def get_schema(self) -> dict:
        return {"type": "object", "properties": {}}
        
    async def execute(self, **kwargs) -> dict:
        return {"status": "success", "battery": "85%", "cpu": "30%"}
