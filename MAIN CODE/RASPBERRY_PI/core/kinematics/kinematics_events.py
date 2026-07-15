"""
Kinematics Events Module
Recon Rover V2 - Phase 4.1
"""
from dataclasses import dataclass
from typing import Dict, Any

try:
    from core.event_bus import Event
except ImportError:
    @dataclass
    class Event: pass

@dataclass
class WheelVelocityRequest(Event):
    timestamp: float
    left_velocity: float  # Normalized [-1.0, 1.0]
    right_velocity: float # Normalized [-1.0, 1.0]

@dataclass
class KinematicsUpdated(Event):
    timestamp: float
    state: str

@dataclass
class KinematicsHealthUpdated(Event):
    is_healthy: bool
    status_flags: Dict[str, bool]

@dataclass
class KinematicsStatisticsUpdated(Event):
    timestamp: float
    conversions_performed: int
    saturations_applied: int
