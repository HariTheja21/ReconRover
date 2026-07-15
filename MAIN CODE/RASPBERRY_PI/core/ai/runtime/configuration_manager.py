class ConfigurationManager:
    def __init__(self):
        self.config = {
            "max_memory_mb": 2048,
            "gpu_enabled": True,
            "cache_dir": "/tmp/recon_models"
        }
        
    def get(self, key: str) -> any:
        return self.config.get(key)
        
    def set(self, key: str, value: any):
        self.config[key] = value
