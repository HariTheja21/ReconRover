"""
Sensor Events Module
Recon Rover V2 - Phase 2.9

Defines structured semantic events published by the Sensor & IMU Bridge.
"""

from dataclasses import dataclass
from typing import Dict, Any

try:
    from core.event_bus import Event
except ImportError:
    @dataclass
    class Event: pass


# INCOMING FROM HAL (Mocked here, typically from Phase 2.4/EventBridge)
@dataclass
class TelemetryPacket(Event):
    """Raw telemetry bytes from HAL."""
    sensor_type: int
    binary_payload: bytes


# OUTGOING SEMANTIC EVENTS
@dataclass
class IMUUpdated(Event):
    accel_x: float
    accel_y: float
    accel_z: float
    gyro_x: float
    gyro_y: float
    gyro_z: float

@dataclass
class OrientationUpdated(Event):
    pitch: float
    roll: float
    yaw: float

@dataclass
class DistanceUpdated(Event):
    sensor_id: str
    distance_cm: float

@dataclass
class ObstacleDetected(Event):
    sensor_id: str
    distance_cm: float
    threat_level: str # 'WARNING', 'CRITICAL'

@dataclass
class BatteryUpdated(Event):
    voltage: float
    percentage: float
    is_charging: bool

@dataclass
class SensorStatisticsUpdated(Event):
    total_packets_decoded: int
    packets_per_second: float

@dataclass
class SensorHealthUpdated(Event):
    is_healthy: bool
    status_flags: Dict[str, bool]
