class CollaborationHealth:
    def __init__(self):
        self.is_healthy: bool = True
        self.bridge_healthy: bool = True
        self.error_message: str = ""

    def set_bridge_error(self, error: str):
        self.bridge_healthy = False
        self.is_healthy = False
        self.error_message = error
