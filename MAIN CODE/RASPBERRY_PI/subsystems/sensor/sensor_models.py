"""
sensor_models.py
Recon Rover V1 - Sensor Fusion Layer

Data classes representing the unified physical state of the rover.
"""

from dataclasses import dataclass, field
import time

@dataclass
class IMUState:
    pitch: float = 0.0
    roll: float = 0.0
    yaw: float = 0.0
    heading: float = 0.0
    accel_x: float = 0.0
    accel_y: float = 0.0
    accel_z: float = 0.0

@dataclass
class ObstacleMap:
    front_tof: float = -1.0
    front_ultrasonic: float = -1.0
    left_ultrasonic: float = -1.0
    right_ultrasonic: float = -1.0
    rear_ultrasonic: float = -1.0
    front_scan_angle: float = 0.0
    front_scan_distance: float = -1.0

@dataclass
class BatteryState:
    voltage: float = 0.0
    current: float = 0.0
    power: float = 0.0
    percentage: float = 0.0

@dataclass
class EnvironmentState:
    gas_detected: bool = False
    gas_confidence: float = 0.0

@dataclass
class HealthState:
    imu_ok: bool = False
    tof_ok: bool = False
    ultrasonic_ok: bool = False
    battery_ok: bool = False
    gas_ok: bool = False

@dataclass
class WorldSensorState:
    timestamp_ms: int = field(default_factory=lambda: int(time.time() * 1000))
    imu: IMUState = field(default_factory=IMUState)
    obstacle_map: ObstacleMap = field(default_factory=ObstacleMap)
    battery: BatteryState = field(default_factory=BatteryState)
    environment: EnvironmentState = field(default_factory=EnvironmentState)
    health: HealthState = field(default_factory=HealthState)
    confidence_score: float = 1.0
