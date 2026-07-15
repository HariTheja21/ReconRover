import json

class ToolSerializer:
    def __init__(self):
        pass
        
    def serialize(self, result: dict) -> str:
        return json.dumps(result)
        
    def deserialize(self, data: str) -> dict:
        return json.loads(data)
