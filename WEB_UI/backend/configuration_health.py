class ConfigurationHealth:
    def __init__(self):
        self.is_healthy: bool = True
        self.storage_healthy: bool = True
        self.ota_healthy: bool = True
        self.last_error: str = ""

    def set_storage_error(self, error: str):
        self.storage_healthy = False
        self.is_healthy = False
        self.last_error = error
        
    def set_ota_error(self, error: str):
        self.ota_healthy = False
        self.is_healthy = False
        self.last_error = error

    def reset(self):
        self.is_healthy = True
        self.storage_healthy = True
        self.ota_healthy = True
        self.last_error = ""
