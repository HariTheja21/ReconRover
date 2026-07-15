class PerceptionHealth:
    def __init__(self):
        self.is_healthy: bool = True
        self.receiving_vision: bool = False
        self.receiving_slam: bool = False
        self.error_message: str = ""

    def set_error(self, message: str):
        self.is_healthy = False
        self.error_message = message

    def set_data_status(self, vision: bool = None, slam: bool = None):
        if vision !== None:
            self.receiving_vision = vision
        if slam !== None:
            self.receiving_slam = slam
