"""
Input Events Module
Recon Rover V2 - Phase 2.6

Defines raw input events and supplementary runtime intents.
"""

from dataclasses import dataclass
from typing import Any, Optional

try:
    from core.event_bus import Event
except ImportError:
    @dataclass
    class Event: pass

# =============================================================================
# RAW INPUT EVENTS (From Hardware Abstraction)
# =============================================================================

@dataclass
class RawJoystickMoved(Event):
    """Raw axis movement from a physical controller."""
    axis_id: int
    value: float  # -1.0 to 1.0

@dataclass
class RawButtonPressed(Event):
    """Raw button press from a physical controller."""
    button_id: int

@dataclass
class RawButtonReleased(Event):
    """Raw button release from a physical controller."""
    button_id: int


# =============================================================================
# SUPPLEMENTARY SEMANTIC INTENTS
# =============================================================================
# Note: MoveIntent, StopIntent, ServoIntent, ModeChangeIntent, MissionChangeIntent, 
# and EmergencyStopIntent are defined in core.command.command_events.

@dataclass
class TurnIntent(Event):
    """A semantic intent specifically for spinning or turning in place."""
    direction: str  # "left" or "right"
    speed: int

@dataclass
class SpeedIntent(Event):
    """Semantic intent to change the global speed multiplier."""
    multiplier: float

@dataclass
class MenuNavigationIntent(Event):
    """Semantic intent for UI navigation via gamepad."""
    action: str  # "up", "down", "select", "back"
