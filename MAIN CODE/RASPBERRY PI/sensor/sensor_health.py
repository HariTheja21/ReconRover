"""
sensor_health.py
Recon Rover V1 - Sensor Fusion Layer

Monitors raw data streams for timeouts and impossible values, 
and computes a global confidence score.
"""

import time
from typing import Dict, Any
from .sensor_models import HealthState

class SensorHealthMonitor:
    def __init__(self, timeout_ms: int = 1000):
        self.timeout_ms = timeout_ms
        self.last_updates: Dict[str, int] = {}
        self.state = HealthState()

    def update_timestamp(self, sensor_name: str, timestamp_ms: int):
        self.last_updates[sensor_name] = timestamp_ms

    def evaluate_health(self, current_time_ms: int) -> HealthState:
        """Checks timeouts for all monitored sensors."""
        def is_ok(sensor: str) -> bool:
            last = self.last_updates.get(sensor, 0)
            return (current_time_ms - last) < self.timeout_ms and last > 0

        self.state.imu_ok = is_ok("imu")
        self.state.tof_ok = is_ok("tof")
        self.state.ultrasonic_ok = is_ok("ultrasonic")
        self.state.battery_ok = is_ok("battery")
        self.state.gas_ok = is_ok("gas")
        
        return self.state

    def validate_reading(self, sensor_name: str, value: float, min_val: float, max_val: float) -> bool:
        """Returns True if the reading is physically possible."""
        if value < min_val or value > max_val:
            return False
        return True

    def compute_confidence(self, conflicts: int) -> float:
        """
        Calculates the global confidence score (0.0 to 1.0).
        Penalized by offline sensors and conflicting data.
        """
        score = 1.0
        
        # Penalize for offline sensors
        offline_count = 0
        if not self.state.imu_ok: offline_count += 1
        if not self.state.tof_ok: offline_count += 1
        if not self.state.ultrasonic_ok: offline_count += 1
        
        score -= (offline_count * 0.2)
        score -= (conflicts * 0.15)
        
        return max(0.0, min(1.0, score))
