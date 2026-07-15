"""
Command Events Module
Recon Rover V2 - Phase 2.5

Defines the cognitive intent events and outbound command lifecycle events.
"""

from dataclasses import dataclass
from typing import Any, Optional

try:
    from core.event_bus import Event
except ImportError:
    @dataclass
    class Event: pass


# =============================================================================
# COGNITIVE INTENTS (Consumed by Command Builder)
# =============================================================================

@dataclass
class MoveIntent(Event):
    """Request to move the rover."""
    left_pwm: int
    right_pwm: int
    duration_ms: int

@dataclass
class StopIntent(Event):
    """Request to immediately halt motion."""
    pass

@dataclass
class ServoIntent(Event):
    """Request to move a specific servo."""
    servo_id: int
    angle: int

@dataclass
class ModeChangeIntent(Event):
    """Request to change the ESP32 hardware operating mode."""
    mode: int

@dataclass
class MissionChangeIntent(Event):
    """Request to send a mission command to the ESP32."""
    mission_mode: int
    command_type: int
    waypoint_count: int

@dataclass
class EmergencyStopIntent(Event):
    """Request a hard emergency stop sequence."""
    reason: str


# =============================================================================
# LIFECYCLE EVENTS (Published by Command Builder)
# =============================================================================

@dataclass
class CommandValidated(Event):
    """Published when an intent passes all safety and mode checks."""
    intent_type: str

@dataclass
class CommandRejected(Event):
    """Published when an intent violates safety bounds or mode rules."""
    intent_type: str
    reason: str

@dataclass
class CommandQueued(Event):
    """Published when a validated command enters the priority queue."""
    priority: int
    queue_size: int

@dataclass
class OutgoingCommandPacket(Event):
    """
    The final product. Consumed by the HAL EventBridge to send via Serial.
    """
    binary_payload: bytes
    priority: int
    command_type: int

@dataclass
class CommandSent(Event):
    """Published when the scheduler successfully dispatches a command."""
    command_type: int
    bytes_sent: int

@dataclass
class CommandStatisticsUpdated(Event):
    """Published periodically to report command throughput."""
    processed: int
    rejected: int
    sent: int
    queue_depth: int
