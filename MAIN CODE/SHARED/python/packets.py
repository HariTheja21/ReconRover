# AUTO-GENERATED FILE. DO NOT MODIFY.
import struct
from dataclasses import dataclass
from typing import List

@dataclass
class PacketHeader:
    sync_1: int
    sync_2: int
    protocol_version: int
    source_module: int
    dest_module: int
    priority: int
    sequence_num: int
    timestamp_ms: int
    payload_type: int
    payload_length: int
    header_crc: int

@dataclass
class HeartbeatPacket:
    system_state: int
    operating_mode: int
    mission_mode: int
    battery_v: float
    uptime_ms: int

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

@dataclass
class MissionPacket:
    mission_mode: int
    command_type: int
    waypoint_count: int

@dataclass
class ConfigurationPacket:
    config_id: int
    value: float

@dataclass
class DiagnosticPacket:
    module_id: int
    error_code: int
    free_heap: int
    cpu_usage_pct: int

@dataclass
class EventPacket:
    event_type: int
    event_data: int

@dataclass
class StatusPacket:
    connection_state: int
    health_state: int
    safety_state: int

@dataclass
class OLEDPacket:
    line_number: int
    text: str

@dataclass
class AIPredictionPacket:
    prediction_class: int
    confidence: float
