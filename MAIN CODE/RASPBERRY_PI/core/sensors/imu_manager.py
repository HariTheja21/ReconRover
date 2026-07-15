"""
IMU Manager
Recon Rover V2 - Phase 2.9
"""
from typing import Any
from .sensor_events import IMUUpdated, OrientationUpdated
import struct

class IMUManager:
    def __init__(self, event_bus: Any):
        self._bus = event_bus
        self.accel_scale = 1.0
        self.gyro_scale = 1.0
        
    def update_config(self, config: dict):
        self.accel_scale = config.get("imu", {}).get("accel_scale", 1.0)
        self.gyro_scale = config.get("imu", {}).get("gyro_scale", 1.0)
        
    def decode_and_publish(self, payload: bytes):
        if len(payload) >= 12:
            # 6 int16 values: ax, ay, az, gx, gy, gz
            ax, ay, az, gx, gy, gz = struct.unpack('<hhhhhh', payload[:12])
            
            # Publish RAW scaled IMU
            self._bus.publish(IMUUpdated(
                accel_x=ax * self.accel_scale,
                accel_y=ay * self.accel_scale,
                accel_z=az * self.accel_scale,
                gyro_x=gx * self.gyro_scale,
                gyro_y=gy * self.gyro_scale,
                gyro_z=gz * self.gyro_scale
            ))
            
            # For phase 2.9, simply pass-through orientation if provided,
            # or we can mock a quick complementary filter here later if needed.
            # But prompt says "convert raw data", no complex math required.
