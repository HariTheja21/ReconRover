class ToolHealth:
    def __init__(self):
        self.is_healthy: bool = True
        self.active_errors: int = 0

    def record_error(self):
        self.active_errors += 1
        if self.active_errors > 5:
            self.is_healthy = False

    def clear_errors(self):
        self.active_errors = 0
        self.is_healthy = True
