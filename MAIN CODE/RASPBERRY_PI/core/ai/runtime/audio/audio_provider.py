class AudioProvider:
    def __init__(self):
        self.is_loaded = False
        
    def load(self, model_path: str, device: str) -> bool:
        self.is_loaded = True
        return True
        
    def unload(self):
        self.is_loaded = False
