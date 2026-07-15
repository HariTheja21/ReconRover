from .base_tool import BaseTool

class NavigationTool(BaseTool):
    def __init__(self):
        super().__init__("navigation", "Control rover movement")
        
    def get_schema(self) -> dict:
        return {"type": "object", "properties": {"direction": {"type": "string"}}}
        
    async def execute(self, **kwargs) -> dict:
        return {"status": "success", "output": f"Moved {kwargs.get('direction', 'forward')}"}
