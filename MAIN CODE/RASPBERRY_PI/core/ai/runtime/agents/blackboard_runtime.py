class BlackboardRuntime:
    def __init__(self, publish):
        self.memory = {}
        self.publish = publish
        
    def write(self, key: str, value: Any, writer_id: str):
        self.memory[key] = value
        self.publish("BlackboardUpdated", {"key": key, "writer_id": writer_id, "timestamp": 0.0})
        
    def read(self, key: str) -> Any:
        return self.memory.get(key)
