"""
Battery Manager
Recon Rover V2 - Phase 2.9
"""
from typing import Any
from .sensor_events import BatteryUpdated
import struct

class BatteryManager:
    def __init__(self, event_bus: Any):
        self._bus = event_bus
        self.max_voltage = 12.6
        self.min_voltage = 9.6
        
    def update_config(self, config: dict):
        self.max_voltage = config.get("battery", {}).get("max_voltage", 12.6)
        self.min_voltage = config.get("battery", {}).get("min_voltage", 9.6)
        
    def decode_and_publish(self, payload: bytes):
        if len(payload) >= 5:
            # float32 voltage, uint8 is_charging
            voltage, charging_int = struct.unpack('<fB', payload[:5])
            
            # clamp and calculate percentage
            v = max(self.min_voltage, min(self.max_voltage, voltage))
            pct = ((v - self.min_voltage) / (self.max_voltage - self.min_voltage)) * 100.0
            
            self._bus.publish(BatteryUpdated(
                voltage=round(voltage, 2),
                percentage=round(pct, 1),
                is_charging=bool(charging_int)
            ))
