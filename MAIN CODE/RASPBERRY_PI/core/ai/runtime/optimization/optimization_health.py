class OptimizationHealth:
    def __init__(self):
        self.is_healthy: bool = True
        self.thermal_throttling: bool = False

    def trigger_throttle(self):
        self.thermal_throttling = True

    def clear_throttle(self):
        self.thermal_throttling = False
