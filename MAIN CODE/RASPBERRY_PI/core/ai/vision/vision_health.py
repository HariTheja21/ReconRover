class VisionHealth:
    def __init__(self):
        self.is_healthy: bool = True
        self.model_loaded: bool = False
        self.camera_stream_active: bool = False
        self.error_message: str = ""

    def set_error(self, message: str):
        self.is_healthy = False
        self.error_message = message

    def set_model_status(self, loaded: bool):
        self.model_loaded = loaded
