"""
Obstacle Manager Module
Recon Rover V2 - Phase 3.1
"""
import threading
import time

class ObstacleManager:
    def __init__(self):
        self._lock = threading.RLock()
        self.obstacles = {}
        self.ttl = 2.0
        
    def add_obstacle(self, sensor_id: str, distance_cm: float, threat: str):
        with self._lock:
            self.obstacles[sensor_id] = {
                "distance_cm": distance_cm,
                "threat": threat,
                "timestamp": time.time()
            }
            
    def get_active(self):
        with self._lock:
            return [{"sensor_id": k, **v} for k, v in self.obstacles.items()]
            
    def sweep(self):
        with self._lock:
            now = time.time()
            expired = [k for k, v in self.obstacles.items() if now - v["timestamp"] > self.ttl]
            for k in expired:
                del self.obstacles[k]
