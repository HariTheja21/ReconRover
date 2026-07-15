import time
from typing import Dict, Any, Callable
from .diagnostics_events import HealthStatusEvent

class HealthMonitor:
    def __init__(self, publish_callback: Callable):
        self.publish = publish_callback
        
        self.categories = [
            "System", "Runtime", "ESP32", "Sensors", "Camera", 
            "Communication", "Navigation", "SLAM", "Mission", "Ground Station"
        ]
        
        self.health_state: Dict[str, Dict[str, Any]] = {}
        for cat in self.categories:
            self.health_state[cat] = {"status": "OFFLINE", "message": "No data", "last_update": 0}

    def update_health(self, event: HealthStatusEvent):
        if event.category in self.health_state:
            self.health_state[event.category] = {
                "status": event.status,
                "message": event.message,
                "last_update": event.timestamp
            }
            # Bridge to frontend
            self.publish("LiveHealthEvent", event)

    def get_full_state(self) -> Dict[str, Dict[str, Any]]:
        return self.health_state
