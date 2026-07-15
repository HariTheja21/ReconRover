class PowerManager:
    def __init__(self):
        self.mode = "performance"
        
    def set_power_mode(self, battery_level: float):
        if battery_level < 20.0:
            self.mode = "efficiency"
        else:
            self.mode = "performance"
        return self.mode
