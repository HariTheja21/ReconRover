class ThermalManager:
    def __init__(self, publish, health):
        self.publish = publish
        self.health = health
        
    def check_temperature(self, temp_celsius: float):
        if temp_celsius > 85.0:
            self.health.trigger_throttle()
            self.publish("OptimizationHealthUpdated", {"is_healthy": False, "thermal_throttling": True, "timestamp": 0.0})
            return "throttled"
        else:
            if self.health.thermal_throttling:
                self.health.clear_throttle()
                self.publish("OptimizationHealthUpdated", {"is_healthy": True, "thermal_throttling": False, "timestamp": 0.0})
            return "normal"
