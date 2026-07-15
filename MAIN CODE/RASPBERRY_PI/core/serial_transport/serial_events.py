"""
Serial Events Module
Recon Rover V2 - Phase 4.3
"""
from dataclasses import dataclass
from typing import Dict, Any

try:
    from core.event_bus import Event
except ImportError:
    @dataclass
    class Event: pass

@dataclass
class SerialPacketSent(Event):
    timestamp: float
    sequence_number: int
    packet_length: int

@dataclass
class SerialPacketReceived(Event):
    timestamp: float
    packet_data: bytes

@dataclass
class SerialConnected(Event):
    timestamp: float
    port: str
    baudrate: int

@dataclass
class SerialDisconnected(Event):
    timestamp: float
    reason: str

@dataclass
class SerialHealthUpdated(Event):
    is_healthy: bool
    status_flags: Dict[str, bool]
