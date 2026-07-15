"""
Ultrasonic Manager
Recon Rover V2 - Phase 2.9
"""
from typing import Any
from .sensor_events import DistanceUpdated, ObstacleDetected
import struct

class UltrasonicManager:
    def __init__(self, event_bus: Any):
        self._bus = event_bus
        self.obstacle_threshold_cm = 15.0
        
    def update_config(self, config: dict):
        self.obstacle_threshold_cm = config.get("ultrasonic", {}).get("obstacle_threshold_cm", 15.0)
        
    def decode_and_publish(self, payload: bytes):
        if len(payload) >= 5:
            # uint8 sensor_id, float32 distance
            sid, dist = struct.unpack('<Bf', payload[:5])
            sensor_id_str = f"US_{sid}"
            
            self._bus.publish(DistanceUpdated(sensor_id=sensor_id_str, distance_cm=dist))
            
            if dist < self.obstacle_threshold_cm:
                self._bus.publish(ObstacleDetected(
                    sensor_id=sensor_id_str, 
                    distance_cm=dist, 
                    threat_level="CRITICAL"
                ))
