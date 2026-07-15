class RuntimeEnvironment:
    def __init__(self, device_manager, config):
        self.device = device_manager
        self.config = config
        
    def validate_environment(self) -> bool:
        profile = self.device.get_system_profile()
        if profile["memory"]["available_mb"] < self.config.get("max_memory_mb"):
            return False
        return True
