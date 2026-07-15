from .base_tool import BaseTool

class VisionTool(BaseTool):
    def __init__(self):
        super().__init__("vision", "Trigger object detection or capture image")
        
    def get_schema(self) -> dict:
        return {"type": "object", "properties": {"action": {"type": "string"}}}
        
    async def execute(self, **kwargs) -> dict:
        return {"status": "success", "objects": ["person", "chair"]}
