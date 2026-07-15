"""
Sensor Confidence Module
Recon Rover V2 - Phase 3.2
"""
import threading
import time

class SensorConfidence:
    """Tracks and updates the reliability score of individual sensors."""
    def __init__(self):
        self._lock = threading.RLock()
        self.confidence_map = {} # sensor_id -> confidence (0.0 to 1.0)
        
    def set_base_confidence(self, sensor_id: str, conf: float):
        with self._lock:
            self.confidence_map[sensor_id] = conf
            
    def get_confidence(self, sensor_id: str) -> float:
        with self._lock:
            return self.confidence_map.get(sensor_id, 0.5)
            
    def apply_decay(self, sensor_id: str, penalty: float):
        with self._lock:
            current = self.get_confidence(sensor_id)
            self.confidence_map[sensor_id] = max(0.0, current - penalty)
