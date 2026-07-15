class SharedContext:
    def __init__(self):
        self.context = {}
        
    def update(self, key: str, value: Any):
        self.context[key] = value
        
    def get(self, key: str) -> Any:
        return self.context.get(key)
