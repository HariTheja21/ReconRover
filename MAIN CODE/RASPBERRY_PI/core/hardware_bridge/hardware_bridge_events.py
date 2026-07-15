"""
Hardware Bridge Events Module
Recon Rover V2 - Phase 4.2
"""
from dataclasses import dataclass
from typing import Dict, Any

try:
    from core.event_bus import Event
except ImportError:
    @dataclass
    class Event: pass

@dataclass
class HardwareCommandPacket(Event):
    timestamp: float
    sequence_number: int
    packet_data: bytes

@dataclass
class HardwareStopPacket(Event):
    timestamp: float
    sequence_number: int
    packet_data: bytes
    reason: str

@dataclass
class HardwareBridgeUpdated(Event):
    timestamp: float
    state: str

@dataclass
class HardwareBridgeHealthUpdated(Event):
    is_healthy: bool
    status_flags: Dict[str, bool]

@dataclass
class HardwareBridgeStatisticsUpdated(Event):
    timestamp: float
    packets_encoded: int
    invalid_requests: int
