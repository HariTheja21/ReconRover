# AUTO-GENERATED FILE. DO NOT MODIFY.
import struct
from dataclasses import dataclass
from typing import List

@dataclass
class HeartbeatPacket:
    timestamp_ms: int
    system_state: int
    battery_v: float

@dataclass
class CommandPacket:
    command_type: int
    payload_length: int
    payload: List[int]

@dataclass
class TelemetryPacket:
    telemetry_type: int
    payload_length: int
    payload: List[int]

@dataclass
class MotionCommand:
    left_pwm: int
    right_pwm: int
    duration_ms: int

@dataclass
class ServoCommand:
    servo_id: int
    target_angle: int
    speed: int

@dataclass
class SensorTelemetry:
    sensor_type: int
    reading_1: float
    reading_2: float
    reading_3: float

