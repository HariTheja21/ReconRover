class StreamHealth:
    def __init__(self):
        self.is_healthy: bool = True
        self.camera_connected: bool = False
        self.encoder_error: bool = False
        self.error_message: str = ""

    def update_status(self, connected: bool, error: bool = False, msg: str = ""):
        self.camera_connected = connected
        self.encoder_error = error
        self.error_message = msg
        self.is_healthy = self.camera_connected and not self.encoder_error
