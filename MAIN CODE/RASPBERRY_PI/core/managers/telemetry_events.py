"""
Telemetry Events Module
Recon Rover V2 - Phase 2.3

Defines events for telemetry routing and health monitoring.
"""

from dataclasses import dataclass
from typing import Dict, Any

try:
    from core.event_bus import Event
except ImportError:
    @dataclass
    class Event: pass

@dataclass
class SerialPacketReceived(Event):
    """
    Published when raw bytes are received from the physical transport layer.
    """
    raw_data: bytes
    timestamp_ms: int

@dataclass
class HeartbeatUpdated(Event):
    """
    Published when a valid Heartbeat packet is successfully decoded.
    """
    system_state: int
    operating_mode: int
    mission_mode: int
    battery_v: float
    uptime_ms: int

@dataclass
class SensorUpdated(Event):
    """
    Published when a sensor packet is decoded.
    """
    sensor_type: int
    reading_1: float
    reading_2: float
    reading_3: float
    timestamp_ms: int

@dataclass
class TelemetryHealthUpdated(Event):
    """
    Published by TelemetryHealth to broadcast latency and packet loss stats.
    """
    packet_loss_pct: float
    latency_ms: float
    packets_per_second: float
    is_healthy: bool
