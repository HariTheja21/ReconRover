"""
Actuation Events Module
Recon Rover V2 - Phase 2.8

Defines structured asynchronous requests to trigger hardware through the HAL.
"""

from dataclasses import dataclass
from typing import Any, Optional, Dict
import time

try:
    from core.event_bus import Event
except ImportError:
    @dataclass
    class Event: pass

# =============================================================================
# HARDWARE REQUEST EVENTS (To HAL)
# =============================================================================

@dataclass
class MotorCommandRequest(Event):
    """Requests a specific PWM for left and right tracks."""
    left_pwm: int
    right_pwm: int
    duration_ms: int

@dataclass
class ServoCommandRequest(Event):
    """Requests an angle for a specific servo ID."""
    servo_id: int
    angle: int

@dataclass
class OLEDCommandRequest(Event):
    """Requests a display update on the local OLED."""
    lines: list
    clear: bool = True

@dataclass
class RGBCommandRequest(Event):
    """Requests a specific color on the RGB LED."""
    red: int
    green: int
    blue: int
    brightness: int = 100

@dataclass
class BuzzerCommandRequest(Event):
    """Requests an audio tone from the buzzer."""
    frequency_hz: int
    duration_ms: int

# =============================================================================
# TELEMETRY EVENTS
# =============================================================================

@dataclass
class HardwareStatisticsUpdated(Event):
    """Periodic telemetry summarizing actuation throughput."""
    total_commands_routed: int
    commands_per_second: float

@dataclass
class HardwareHealthUpdated(Event):
    """Periodic telemetry summarizing controller states."""
    is_healthy: bool
    status_flags: Dict[str, bool]
