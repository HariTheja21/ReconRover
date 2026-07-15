class DemoHealth:
    def __init__(self):
        self.is_healthy: bool = True
        self.error_count: int = 0
        
    def log_error(self):
        self.error_count += 1
        if self.error_count > 3:
            self.is_healthy = False
