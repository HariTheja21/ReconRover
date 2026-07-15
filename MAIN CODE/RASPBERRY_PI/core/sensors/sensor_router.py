"""
Sensor Router
Recon Rover V2 - Phase 2.9
"""
from typing import Any
from .imu_manager import IMUManager
from .ultrasonic_manager import UltrasonicManager
from .lidar_manager import LidarManager
from .battery_manager import BatteryManager

class SensorRouter:
    """Routes incoming raw telemetry packets to proper decoders."""
    
    def __init__(self, event_bus: Any):
        self._bus = event_bus
        self.imu = IMUManager(self._bus)
        self.ultrasonic = UltrasonicManager(self._bus)
        self.lidar = LidarManager(self._bus)
        self.battery = BatteryManager(self._bus)
        
    def update_config(self, config: dict):
        self.imu.update_config(config)
        self.ultrasonic.update_config(config)
        self.lidar.update_config(config)
        self.battery.update_config(config)
        
    def route_packet(self, sensor_type: int, binary_payload: bytes):
        if sensor_type == 0x01: # IMU
            self.imu.decode_and_publish(binary_payload)
        elif sensor_type == 0x02: # Ultrasonic
            self.ultrasonic.decode_and_publish(binary_payload)
        elif sensor_type == 0x03: # LiDAR
            self.lidar.decode_and_publish(binary_payload)
        elif sensor_type == 0x04: # Battery
            self.battery.decode_and_publish(binary_payload)
