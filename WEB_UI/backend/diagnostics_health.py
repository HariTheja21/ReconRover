class DiagnosticsHealth:
    def __init__(self):
        self.is_healthy: bool = True
        self.storage_healthy: bool = True
        self.error_message: str = ""

    def set_storage_error(self, error: str):
        self.storage_healthy = False
        self.is_healthy = False
        self.error_message = error
