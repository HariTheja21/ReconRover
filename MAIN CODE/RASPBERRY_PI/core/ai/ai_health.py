class AIHealth:
    def __init__(self):
        self.is_healthy: bool = True
        self.memory_critical: bool = False
        self.gpu_critical: bool = False
        self.error_message: str = ""

    def set_error(self, message: str):
        self.is_healthy = False
        self.error_message = message

    def set_memory_critical(self, is_critical: bool):
        self.memory_critical = is_critical
        if is_critical:
            self.is_healthy = False
            self.error_message = "Memory capacity critical"
