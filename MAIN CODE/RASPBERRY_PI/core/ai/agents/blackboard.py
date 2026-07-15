class Blackboard:
    def __init__(self):
        self.data = {}
        
    def write(self, key: str, value: Any):
        self.data[key] = value
        
    def read(self, key: str) -> Any:
        return self.data.get(key)
        
    def clear(self):
        self.data.clear()
