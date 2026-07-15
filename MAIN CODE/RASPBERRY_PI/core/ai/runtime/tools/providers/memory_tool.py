from .base_tool import BaseTool

class MemoryTool(BaseTool):
    def __init__(self):
        super().__init__("memory", "Store or retrieve episodic memories")
        
    def get_schema(self) -> dict:
        return {"type": "object", "properties": {"query": {"type": "string"}}}
        
    async def execute(self, **kwargs) -> dict:
        return {"status": "success", "memory": "Retrieved memory"}
