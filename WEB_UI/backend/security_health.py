class SecurityHealth:
    def __init__(self):
        self.is_healthy: bool = True
        self.storage_healthy: bool = True
        self.error_message: str = ""

    def set_error(self, error: str):
        self.is_healthy = False
        self.error_message = error
