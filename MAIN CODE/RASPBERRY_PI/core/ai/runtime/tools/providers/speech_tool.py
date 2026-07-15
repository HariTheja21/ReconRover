from .base_tool import BaseTool

class SpeechTool(BaseTool):
    def __init__(self):
        super().__init__("speech", "Synthesize text to speech")
        
    def get_schema(self) -> dict:
        return {"type": "object", "properties": {"text": {"type": "string"}}}
        
    async def execute(self, **kwargs) -> dict:
        return {"status": "success", "output": "Speech synthesized"}
