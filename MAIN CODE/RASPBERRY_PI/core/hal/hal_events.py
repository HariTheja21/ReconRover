"""
HAL Events Module
Recon Rover V2 - Phase 2.4

Defines events published by the Hardware Abstraction Layer.
"""

from dataclasses import dataclass
from typing import Dict, Any, Optional

try:
    from core.event_bus import Event
except ImportError:
    @dataclass
    class Event: pass

@dataclass
class SerialConnected(Event):
    """Published when a serial port is successfully opened."""
    port: str
    baudrate: int

@dataclass
class SerialDisconnected(Event):
    """Published when the serial connection drops or is closed."""
    port: str
    reason: str

@dataclass
class PacketSent(Event):
    """Published when a byte array is successfully transmitted."""
    size: int
    timestamp_ms: int

@dataclass
class SerialHealthUpdated(Event):
    """Published by the SerialHealth monitor to track physical layer vitals."""
    is_connected: bool
    bytes_rx: int
    bytes_tx: int
    crc_errors: int
    dropped_packets: int
    uptime_ms: int

@dataclass
class PacketValidationFailed(Event):
    """Published when a received payload fails CRC or length checks."""
    reason: str
    raw_header: Optional[bytes] = None

@dataclass
class CommunicationTimeout(Event):
    """Published by the watchdog when no heartbeat is received in time."""
    threshold_ms: int
    last_seen_ms: int
